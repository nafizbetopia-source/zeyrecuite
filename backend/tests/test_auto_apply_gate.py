"""Tests for the auto-apply-only gate (Feature A).

The gate condition is URL-based: a job is auto-applicable **iff** it carries a
non-empty ``application_url`` (``collector.is_auto_applicable`` is the single
source of truth). With ``auto_apply_only`` ON (the default):

- scans skip link-less jobs (``RunSummary.skipped``);
- ``POST /api/import/jobs`` skips them with an explicit error;
- ``GET /api/jobs`` hides them;
- startup purges legacy link-less rows and their dependent
  Feedback/Application history in one transaction.

``auto_apply_only: false`` turns every one of those off.
"""
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from zeyrecuite.adapters import BaseAdapter
from zeyrecuite.app import create_app
from zeyrecuite.collector import (
    is_auto_applicable,
    purge_unsubmittable_jobs,
    run_source,
)
from zeyrecuite.config import AppConfig, _build
from zeyrecuite.database import Database
from zeyrecuite.models import Application, Feedback, Job, Profile


class FakeAdapter(BaseAdapter):
    name = "fake"

    def __init__(self, jobs):
        self.jobs = jobs

    def fetch(self, *, client=None):
        return self.jobs


def make_db():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db = Database(f"sqlite:///{tmp.name}")
    db.create_all()
    return db, tmp.name


def raw_job(**kw):
    base = {
        "title": "Business Analyst",
        "company": "Acme",
        "url": "https://x/1",
        "work_mode": "remote",
        "employer_country": "US",
        "job_country": None,
        "worldwide_remote": True,
        "candidate_required_location": None,
        "description": "sql excel reporting",
        "skills": ["SQL", "Excel"],
        "source": "fake",
    }
    base.update(kw)
    return base


# ---------------------------------------------------------------------------
# Config parsing + the single-source-of-truth helper
# ---------------------------------------------------------------------------


class GateConfigTests(unittest.TestCase):
    def test_defaults_on(self):
        self.assertTrue(_build({}).auto_apply_only)
        self.assertTrue(AppConfig().auto_apply_only)

    def test_yaml_off_and_on(self):
        self.assertFalse(_build({"auto_apply_only": False}).auto_apply_only)
        self.assertFalse(_build({"auto_apply_only": "false"}).auto_apply_only)
        self.assertTrue(_build({"auto_apply_only": "true"}).auto_apply_only)


class HelperTests(unittest.TestCase):
    def test_url_based_iff(self):
        self.assertFalse(is_auto_applicable({}))
        self.assertFalse(is_auto_applicable({"application_url": None}))
        self.assertFalse(is_auto_applicable({"application_url": ""}))
        self.assertFalse(is_auto_applicable({"application_url": "   "}))
        self.assertTrue(is_auto_applicable({"application_url": "https://x/apply"}))

    def test_accepts_orm_job(self):
        job = Job(
            title="t", company="c", url="https://x",
            application_url="https://x/a",
        )
        self.assertTrue(is_auto_applicable(job))
        job.application_url = None
        self.assertFalse(is_auto_applicable(job))


# ---------------------------------------------------------------------------
# Collector gate (scans)
# ---------------------------------------------------------------------------


class CollectorGateTests(unittest.TestCase):
    def setUp(self):
        self.db, self.db_path = make_db()
        self.config = AppConfig()
        with self.db.session() as s:
            s.add(Profile(id=1, current_country="Bangladesh", skills=["SQL"]))
            s.commit()

    def tearDown(self):
        self.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_linkless_job_is_skipped_not_stored(self):
        summary = run_source(self.db, self.config, FakeAdapter([raw_job()]))
        self.assertEqual(summary.skipped, 1)
        self.assertEqual(summary.eligible, 0)
        self.assertEqual(summary.review, 0)
        with self.db.session() as s:
            self.assertEqual(s.query(Job).count(), 0)

    def test_applicable_job_is_stored(self):
        job = raw_job(application_url="https://x/1/apply")
        summary = run_source(self.db, self.config, FakeAdapter([job]))
        self.assertEqual(summary.skipped, 0)
        self.assertEqual(summary.eligible, 1)
        with self.db.session() as s:
            self.assertEqual(s.query(Job).count(), 1)

    def test_flag_off_stores_linkless_jobs(self):
        self.config.auto_apply_only = False
        summary = run_source(self.db, self.config, FakeAdapter([raw_job()]))
        self.assertEqual(summary.skipped, 0)
        self.assertEqual(summary.eligible, 1)
        with self.db.session() as s:
            self.assertEqual(s.query(Job).count(), 1)

    def test_skipped_serializes_with_run_summaries(self):
        # POST /api/scan returns [s.__dict__ for s in summaries] — skipped rides along.
        summary = run_source(self.db, self.config, FakeAdapter([raw_job()]))
        self.assertEqual(summary.__dict__["skipped"], 1)


# ---------------------------------------------------------------------------
# Purge helper (cascade + idempotence)
# ---------------------------------------------------------------------------


def seed_purge_rows(db):
    """One link-less job with dependents + one applicable job with history."""
    with db.session() as s:
        old = Job(
            fingerprint="fp-old", title="Legacy", company="OldCo",
            url="https://old/1", application_url=None, source="fake",
            location_status="eligible", status="new",
        )
        keep = Job(
            fingerprint="fp-keep", title="Modern", company="NewCo",
            url="https://new/1", application_url="https://new/1/apply",
            source="fake", location_status="eligible", status="new",
        )
        s.add_all([old, keep])
        s.flush()
        s.add(Application(job_id=old.id, status="ready"))
        s.add(Application(job_id=keep.id, status="ready"))
        s.add(Feedback(job_id=old.id, signal="approve"))
        s.add(Feedback(job_id=keep.id, signal="reject"))
        s.commit()
        return old.id, keep.id


class PurgeHelperTests(unittest.TestCase):
    def setUp(self):
        self.db, self.db_path = make_db()

    def tearDown(self):
        self.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_purge_cascades_and_is_idempotent(self):
        old_id, keep_id = seed_purge_rows(self.db)
        purged = purge_unsubmittable_jobs(self.db)
        self.assertEqual(purged, 1)
        with self.db.session() as s:
            self.assertIsNone(s.get(Job, old_id))
            self.assertIsNotNone(s.get(Job, keep_id))
            self.assertEqual(
                s.query(Application).filter(Application.job_id == old_id).count(), 0
            )
            self.assertEqual(
                s.query(Feedback).filter(Feedback.job_id == old_id).count(), 0
            )
            # The applicable job keeps its history.
            self.assertEqual(
                s.query(Application).filter(Application.job_id == keep_id).count(), 1
            )
        # Second run finds nothing — purge is idempotent.
        self.assertEqual(purge_unsubmittable_jobs(self.db), 0)


# ---------------------------------------------------------------------------
# Startup purge (runs from the lifespan when the flag is ON)
# ---------------------------------------------------------------------------


class StartupPurgeTests(unittest.TestCase):
    def _build_app(self, *, auto_apply_only):
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        db = Database(f"sqlite:///{tmp.name}")
        db.create_all()
        old_id, keep_id = seed_purge_rows(db)
        db.engine.dispose()
        cfg = AppConfig(
            database_url=f"sqlite:///{tmp.name}", auto_apply_only=auto_apply_only
        )
        app = create_app(cfg)
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return app, tmp.name, old_id, keep_id

    def test_startup_purges_linkless_with_history(self):
        app, path, old_id, keep_id = self._build_app(auto_apply_only=True)
        client = TestClient(app)
        with client:  # triggers lifespan → purge
            with app.state.db.session() as s:
                self.assertIsNone(s.get(Job, old_id))
                self.assertIsNotNone(s.get(Job, keep_id))
                self.assertEqual(s.query(Application).count(), 1)
                self.assertEqual(s.query(Feedback).count(), 1)
        app.state.db.engine.dispose()

    def test_flag_off_keeps_legacy_rows(self):
        app, path, old_id, keep_id = self._build_app(auto_apply_only=False)
        client = TestClient(app)
        with client:
            with app.state.db.session() as s:
                self.assertIsNotNone(s.get(Job, old_id))
                self.assertIsNotNone(s.get(Job, keep_id))
        app.state.db.engine.dispose()


# ---------------------------------------------------------------------------
# API gates (import endpoint + GET /api/jobs)
# ---------------------------------------------------------------------------


class ApiGateBase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        self.db_path = tmp.name
        self.cfg = AppConfig(database_url=f"sqlite:///{self.db_path}")
        self.app = create_app(self.cfg)
        self.client = TestClient(self.app)
        with self.client:  # triggers lifespan (seeds user + blank profile)
            r = self.client.post(
                "/api/auth/login", json={"username": "admin", "password": "zeyrecuite"}
            )
            self.token = r.json()["token"]
        self.h = {"Authorization": f"Bearer {self.token}"}
        self.db = self.app.state.db

    def tearDown(self):
        for state_name in ("weekly_report", "daily_submit"):
            runner = getattr(self.app.state, state_name, None)
            if runner is not None:
                runner.stop()
        self.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)


class ImportGateTests(ApiGateBase):
    def test_skips_linkless_rows_with_reason(self):
        payload = {"jobs": [
            {"title": "No Link", "company": "A", "url": "https://a/1"},
            {"title": "With Link", "company": "B", "url": "https://b/1",
             "application_url": "https://b/1/apply"},
        ]}
        r = self.client.post("/api/import/jobs", headers=self.h, json=payload)
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertEqual(body["imported"], 1)
        self.assertEqual(body["skipped"], 1)
        self.assertTrue(any("auto_apply_only" in e for e in body["errors"]))

    def test_flag_off_imports_linkless_rows(self):
        self.cfg.auto_apply_only = False
        payload = {"jobs": [{"title": "No Link", "company": "A", "url": "https://a/1"}]}
        r = self.client.post("/api/import/jobs", headers=self.h, json=payload)
        body = r.json()
        self.assertEqual(body["imported"], 1)
        self.assertEqual(body["skipped"], 0)


class JobsListGateTests(ApiGateBase):
    def _seed(self):
        with self.db.session() as s:
            s.add(Job(
                fingerprint="fp-a", title="Applicable", company="A",
                url="https://a/1", application_url="https://a/1/apply",
                source="fake", location_status="eligible", status="new",
            ))
            s.add(Job(
                fingerprint="fp-b", title="Linkless", company="B",
                url="https://b/1", application_url=None,
                source="fake", location_status="eligible", status="new",
            ))
            s.commit()

    def _titles(self):
        return [j["title"] for j in self.client.get("/api/jobs", headers=self.h).json()]

    def test_list_hides_linkless_jobs(self):
        self._seed()
        titles = self._titles()
        self.assertIn("Applicable", titles)
        self.assertNotIn("Linkless", titles)

    def test_flag_off_lists_everything(self):
        self.cfg.auto_apply_only = False
        self._seed()
        titles = self._titles()
        self.assertIn("Applicable", titles)
        self.assertIn("Linkless", titles)


if __name__ == "__main__":
    unittest.main()



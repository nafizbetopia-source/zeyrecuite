"""Tests for the v2.3 feature set: saved filters (F10), fit trend (F11),
resume variants (F12), cover-letter personalization (F13), and
export/import (F14)."""
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from zeyrecuite.app import create_app, _cover_letter
from zeyrecuite.config import AppConfig
from zeyrecuite.models import Job, Profile, ScrapeRun


def _make_app():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    cfg = AppConfig(database_url=f"sqlite:///{tmp.name}")
    app = create_app(cfg)
    return app, tmp.name


class Base(unittest.TestCase):
    def setUp(self):
        self.app, self.db_path = _make_app()
        self.client = TestClient(self.app)
        with self.client:  # triggers lifespan (seeds user + blank profile)
            r = self.client.post("/api/auth/login", json={"username": "admin", "password": "zeyrecuite"})
            self.token = r.json()["token"]
            self.h = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        self.app.state.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def _seed_job(self, **kw):
        defaults = dict(
            fingerprint="fp1", title="Senior Business Analyst", company="Stripe",
            location="Remote", work_mode="remote", source="fake",
            url="https://x/1", application_url="https://x/1/apply",
            description="Work with stakeholders, write requirements, build SQL reports and dashboards.",
            skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
            location_status="eligible", status="new",
            confidence=88.0, confidence_label="Excellent match",
            eligibility=100.0, eligibility_label="Fully eligible",
        )
        defaults.update(kw)
        with self.app.state.db.session() as s:
            s.add(Job(**defaults))
            s.commit()

    def _set_profile(self, **kw):
        defaults = dict(
            name="Nafiz Ahmed", email="nafiz@real.com", role="Business Analyst",
            summary="BA with 4 years in fintech.",
            skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
        )
        defaults.update(kw)
        with self.app.state.db.session() as s:
            prof = s.get(Profile, 1)
            for k, v in defaults.items():
                setattr(prof, k, v)
            s.commit()


# ---------- F10: Saved filters ----------

class SavedFiltersTests(Base):
    def test_starts_empty(self):
        r = self.client.get("/api/profile/filters", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["filters"], [])

    def test_save_and_get(self):
        filters = [{"id": 1, "label": "“sql”", "search": "sql", "status": "all"}]
        r = self.client.put("/api/profile/filters", headers=self.h, json={"filters": filters})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["filters"], filters)
        r = self.client.get("/api/profile/filters", headers=self.h)
        self.assertEqual(r.json()["filters"], filters)

    def test_rejects_non_list(self):
        r = self.client.put("/api/profile/filters", headers=self.h, json={"filters": "nope"})
        self.assertEqual(r.status_code, 422)

    def test_rejects_too_many(self):
        filters = [{"id": i, "label": "x", "search": "", "status": "all"} for i in range(21)]
        r = self.client.put("/api/profile/filters", headers=self.h, json={"filters": filters})
        self.assertEqual(r.status_code, 422)


# ---------- F11: Fit trend ----------

class FitTrendTests(Base):
    def test_empty(self):
        r = self.client.get("/api/analytics/trend", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["points"], [])

    def test_points_from_runs(self):
        with self.app.state.db.session() as s:
            s.add(ScrapeRun(source="remotive", status="done", fetched=10,
                            avg_confidence=80.0, avg_eligibility=90.0,
                            started_at=datetime(2024, 1, 1, tzinfo=timezone.utc)))
            s.add(ScrapeRun(source="greenhouse", status="done", fetched=5,
                            avg_confidence=70.0, avg_eligibility=85.0,
                            started_at=datetime(2024, 1, 2, tzinfo=timezone.utc)))
            # A run with no averages should be excluded.
            s.add(ScrapeRun(source="lever", status="done", fetched=3,
                            started_at=datetime(2024, 1, 3, tzinfo=timezone.utc)))
            s.commit()
        r = self.client.get("/api/analytics/trend", headers=self.h)
        pts = r.json()["points"]
        self.assertEqual(len(pts), 2)
        self.assertEqual(pts[0]["source"], "remotive")
        self.assertEqual(pts[0]["avg_confidence"], 80.0)
        self.assertEqual(pts[1]["avg_eligibility"], 85.0)


# ---------- F12: Resume variants ----------

class ResumeVariantTests(Base):
    def test_starts_empty(self):
        r = self.client.get("/api/profile/resume-variants", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["variants"], [])

    def test_save_and_get(self):
        variants = [{"id": "v1", "label": "Data Analyst", "skills": ["SQL", "Python"],
                     "summary": "Data-focused BA."}]
        r = self.client.put("/api/profile/resume-variants", headers=self.h, json={"variants": variants})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["variants"], variants)
        r = self.client.get("/api/profile/resume-variants", headers=self.h)
        self.assertEqual(r.json()["variants"], variants)

    def test_rejects_non_list(self):
        r = self.client.put("/api/profile/resume-variants", headers=self.h, json={"variants": 5})
        self.assertEqual(r.status_code, 422)

    def test_rejects_too_many(self):
        variants = [{"id": str(i), "label": "x", "skills": [], "summary": ""} for i in range(11)]
        r = self.client.put("/api/profile/resume-variants", headers=self.h, json={"variants": variants})
        self.assertEqual(r.status_code, 422)


# ---------- F13: Cover-letter personalization ----------

class CoverLetterTests(Base):
    def _profile(self, **kw):
        p = Profile(name="Nafiz", role="Business Analyst",
                    skills=["SQL", "Excel", "Power BI"], summary="BA in fintech.")
        for k, v in kw.items():
            setattr(p, k, v)
        return p

    def test_returns_tuple_with_score(self):
        job = Job(title="Senior Business Analyst", company="Stripe",
                  description="Build SQL reports and dashboards for stakeholders.",
                  skills=["SQL", "Excel", "Power BI"])
        letter, score = _cover_letter(self._profile(), job)
        self.assertIsInstance(letter, str)
        self.assertIsInstance(score, int)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_matched_skills_raise_score(self):
        job = Job(title="Senior Business Analyst", company="Stripe",
                  description="Build SQL reports and dashboards.",
                  skills=["SQL", "Excel", "Power BI"])
        _, with_match = _cover_letter(self._profile(), job)
        job2 = Job(title="Barista", company="Cafe",
                   description="Make coffee.", skills=["Espresso"])
        _, no_match = _cover_letter(self._profile(), job2)
        self.assertGreater(with_match, no_match)

    def test_empty_profile_placeholder(self):
        p = Profile(name=None, role=None, skills=[], summary=None)
        job = Job(title="Analyst", company="X", description="d", skills=["SQL"])
        letter, score = _cover_letter(p, job)
        self.assertIn("not complete yet", letter)
        self.assertEqual(score, 0)

    def test_generate_exposes_score(self):
        self._set_profile()
        self._seed_job()
        r = self.client.post("/api/jobs/1/generate", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertIn("personalization_score", r.json())
        self.assertIsNotNone(r.json()["personalization_score"])


# ---------- F14: Export / import ----------

class ExportImportTests(Base):
    def test_export_jobs_csv(self):
        self._seed_job()
        r = self.client.get("/api/export/jobs?format=csv", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertIn("text/csv", r.headers["content-type"])
        self.assertIn("Senior Business Analyst", r.text)

    def test_export_jobs_json(self):
        self._seed_job()
        r = self.client.get("/api/export/jobs?format=json", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()["jobs"]), 1)

    def test_export_applications_and_analytics(self):
        r = self.client.get("/api/export/applications?format=csv", headers=self.h)
        self.assertEqual(r.status_code, 200)
        r = self.client.get("/api/export/analytics?format=csv", headers=self.h)
        self.assertEqual(r.status_code, 200)

    def test_import_jobs(self):
        payload = {"jobs": [
            {"title": "Data Analyst", "company": "Acme", "url": "https://a/1",
             "skills": ["SQL"], "source": "import",
             "application_url": "https://a/1/apply"},
            {"title": "PM", "company": "Beta", "url": "https://b/1",
             "application_url": "https://b/1/apply"},
        ]}
        r = self.client.post("/api/import/jobs", headers=self.h, json=payload)
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertEqual(body["imported"], 2)
        self.assertEqual(body["skipped"], 0)

    def test_import_dedups(self):
        self._seed_job()  # fingerprint fp1
        payload = {"jobs": [
            {"title": "Senior Business Analyst", "company": "Stripe",
             "url": "https://x/1", "fingerprint": "fp1"},
            {"title": "New Role", "company": "Gamma", "url": "https://g/1",
             "application_url": "https://g/1/apply"},
        ]}
        r = self.client.post("/api/import/jobs", headers=self.h, json=payload)
        body = r.json()
        self.assertEqual(body["imported"], 1)
        self.assertEqual(body["skipped"], 1)

    def test_import_skips_bad_rows(self):
        payload = {"jobs": [
            {"title": "", "company": "NoTitle", "url": "https://n/1"},
            {"title": "Good", "company": "Ok", "url": "https://o/1",
             "application_url": "https://o/1/apply"},
        ]}
        r = self.client.post("/api/import/jobs", headers=self.h, json=payload)
        body = r.json()
        self.assertEqual(body["imported"], 1)
        self.assertEqual(body["skipped"], 1)
        self.assertTrue(body["errors"])

    def test_import_rejects_non_list(self):
        r = self.client.post("/api/import/jobs", headers=self.h, json={"jobs": "nope"})
        self.assertEqual(r.status_code, 422)


if __name__ == "__main__":
    unittest.main()

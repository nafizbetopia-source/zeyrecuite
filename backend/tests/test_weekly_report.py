"""Tests for the weekly Discord report (Feature B).

Covers config parsing (``weekly_report`` block), ``build_week_report``
aggregation (7-day window, by-date counts, goal progress, top-pick heuristic,
learning summary), the Discord message, the never-raising runner with an
injectable poster, the APScheduler cron wrapper, and the authenticated API
endpoints. Everything runs offline.
"""
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from zeyrecuite.app import create_app
from zeyrecuite.config import AppConfig, _build
from zeyrecuite.database import Database
from zeyrecuite.models import Application, Feedback, Job, Profile
from zeyrecuite.notify import MAX_CONTENT_LENGTH
from zeyrecuite.weekly_report import (
    build_message,
    build_week_report,
    build_weekly_report,
    run_weekly,
)

NOW = datetime.now(timezone.utc)


def make_db():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db = Database(f"sqlite:///{tmp.name}")
    db.create_all()
    return db, tmp.name


def add_job(db, **kw):
    defaults = dict(
        title="Business Analyst", company="Acme", url="https://x/1",
        source="fake", location_status="eligible", status="new",
        application_url="https://x/1/apply", confidence=50.0,
    )
    defaults.update(kw)
    defaults.setdefault("fingerprint", f"fp-{defaults['url']}")
    with db.session() as s:
        job = Job(**defaults)
        s.add(job)
        s.commit()
        return job.id


def add_application(db, job_id, *, stage="draft", application_status=None,
                    submitted_at=None):
    with db.session() as s:
        s.add(Application(
            job_id=job_id, status=stage,
            application_status=application_status, submitted_at=submitted_at,
        ))
        s.commit()


# ---------------------------------------------------------------------------
# Config parsing
# ---------------------------------------------------------------------------


class WeeklyConfigTests(unittest.TestCase):
    def test_defaults_off_sunday_evening(self):
        cfg = _build({})
        self.assertFalse(cfg.weekly_report.enabled)
        self.assertEqual(cfg.weekly_report.day, "sun")
        self.assertEqual((cfg.weekly_report.hour, cfg.weekly_report.minute), (18, 0))

    def test_parses_enabled_day_and_at(self):
        cfg = _build({"weekly_report": {"enabled": "true", "day": "monday", "at": "21:05"}})
        self.assertTrue(cfg.weekly_report.enabled)
        self.assertEqual(cfg.weekly_report.day, "mon")
        self.assertEqual((cfg.weekly_report.hour, cfg.weekly_report.minute), (21, 5))

    def test_invalid_day_and_at_fall_back(self):
        cfg = _build({"weekly_report": {"day": "someday", "at": "99:99"}})
        self.assertEqual(cfg.weekly_report.day, "sun")
        self.assertEqual((cfg.weekly_report.hour, cfg.weekly_report.minute), (18, 0))


# ---------------------------------------------------------------------------
# build_week_report aggregation
# ---------------------------------------------------------------------------


class BuildWeekReportTests(unittest.TestCase):
    def setUp(self):
        self.db, self.db_path = make_db()
        with self.db.session() as s:
            s.add(Profile(id=1, weekly_goal=10, current_country="Bangladesh"))
            s.commit()

    def tearDown(self):
        self.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_empty_report_is_all_zeros(self):
        report = build_week_report(self.db, AppConfig())
        self.assertEqual(report["submitted_this_week"], 0)
        self.assertEqual(report["by_date"], {})
        self.assertEqual(report["top_picks"], [])
        self.assertEqual(report["progress"], 0.0)
        self.assertEqual(report["weekly_goal"], 10)
        self.assertFalse(report["learning"]["has_data"])
        self.assertFalse(report["notified"])

    def test_groups_submissions_by_date_and_computes_progress(self):
        day1 = NOW - timedelta(days=2)
        day2 = NOW - timedelta(days=4)
        old = NOW - timedelta(days=10)  # outside the 7-day window
        for when, n, slug in ((day1, 2, "a"), (day2, 1, "b"), (old, 3, "old")):
            for i in range(n):
                jid = add_job(
                    self.db, title=f"J {slug}{i}",
                    url=f"https://{slug}/{when.date()}/{i}",
                    application_url=f"https://{slug}/{when.date()}/{i}/apply",
                )
                add_application(
                    self.db, jid, stage="submitted",
                    submitted_at=when,
                )
        report = build_week_report(self.db, AppConfig())
        self.assertEqual(report["submitted_this_week"], 3)
        self.assertEqual(
            report["by_date"],
            {day1.date().isoformat(): 2, day2.date().isoformat(): 1},
        )
        self.assertEqual(report["progress"], 30.0)

    def test_top_picks_heuristic(self):
        # Eligible, applicable, unsubmitted — ranked by confidence, top 3.
        add_job(self.db, title="High", url="https://h/1", confidence=95.0)
        add_job(self.db, title="Mid", url="https://m/1", confidence=80.0)
        add_job(self.db, title="Low", url="https://l/1", confidence=40.0)
        add_job(self.db, title="Extra", url="https://e/1", confidence=30.0)
        # Excluded: rejected by a prior review.
        add_job(self.db, title="Rejected", url="https://r/1",
                confidence=99.0, status="rejected")
        # Excluded: no apply link.
        add_job(self.db, title="NoLink", url="https://n/1",
                confidence=98.0, application_url=None)
        # Excluded: not location-eligible.
        add_job(self.db, title="Review", url="https://v/1",
                confidence=97.0, location_status="review")
        # Excluded: already submitted.
        done = add_job(self.db, title="Done", url="https://d/1", confidence=96.0)
        add_application(self.db, done, application_status="submitted",
                        submitted_at=NOW - timedelta(days=1))
        report = build_week_report(self.db, AppConfig())
        titles = [p["title"] for p in report["top_picks"]]
        self.assertEqual(titles, ["High", "Mid", "Low"])
        self.assertEqual(report["top_picks"][0]["confidence"], 95.0)
        self.assertEqual(report["top_picks"][0]["job_id"],
                         report["top_picks"][0]["job_id"])

    def test_learning_summary_counts_window_signals(self):
        j1 = add_job(self.db, title="L1", url="https://l1/1", application_url=None)
        j2 = add_job(self.db, title="L2", url="https://l2/1", application_url=None)
        j3 = add_job(self.db, title="L3", url="https://l3/1", application_url=None)
        with self.db.session() as s:
            s.add(Feedback(job_id=j1, signal="approve"))
            s.add(Feedback(job_id=j2, signal="approve"))
            s.add(Feedback(job_id=j3, signal="reject",
                           created_at=NOW - timedelta(days=10)))  # outside window
            s.commit()
        learning = build_week_report(self.db, AppConfig())["learning"]
        self.assertTrue(learning["has_data"])
        self.assertEqual(learning["approve"], 2)
        self.assertEqual(learning["reject"], 0)
        self.assertEqual(learning["select"], 0)

    def test_learning_no_feedback_has_no_data(self):
        add_job(self.db, url="https://x/2")
        learning = build_week_report(self.db, AppConfig())["learning"]
        self.assertFalse(learning["has_data"])
        self.assertEqual(learning["top_skills"], [])


# ---------------------------------------------------------------------------
# Discord message formatting
# ---------------------------------------------------------------------------


def sample_report(**over):
    base = {
        "weekly_goal": 10,
        "submitted_this_week": 4,
        "progress": 40.0,
        "by_date": {"2026-10-01": 2, "2026-10-02": 2},
        "top_picks": [
            {"job_id": 1, "title": "Senior BA", "company": "Acme",
             "confidence": 94.0, "confidence_label": "Excellent match"},
        ],
        "learning": {"approve": 3, "reject": 1, "select": 1,
                     "top_skills": ["SQL", "Excel"], "has_data": True},
        "notified": False,
        "error": None,
    }
    base.update(over)
    return base


class BuildMessageTests(unittest.TestCase):
    def test_full_digest_mentions_every_section(self):
        msg = build_message(sample_report())
        self.assertIn("weekly report", msg)
        self.assertIn("goal 4/10 (40.0%)", msg)
        self.assertIn("2026-10-01", msg)
        self.assertIn("Interview-likely", msg)
        self.assertIn("Senior BA", msg)
        self.assertIn("👍 3", msg)
        self.assertIn("SQL", msg)
        self.assertIn("6 more", msg)
        self.assertLessEqual(len(msg), MAX_CONTENT_LENGTH)

    def test_empty_week_message(self):
        msg = build_message(sample_report(
            submitted_this_week=0, progress=0.0, by_date={}, top_picks=[],
            learning={"approve": 0, "reject": 0, "select": 0,
                      "top_skills": [], "has_data": False},
        ))
        self.assertIn("No applications", msg)
        self.assertIn("no feedback yet", msg)

    def test_goal_met_celebrates(self):
        msg = build_message(sample_report(submitted_this_week=10, progress=100.0))
        self.assertIn("goal met", msg)

    def test_error_message(self):
        msg = build_message({"error": "boom"})
        self.assertIn("failed", msg)
        self.assertIn("boom", msg)


# ---------------------------------------------------------------------------
# run_weekly (injectable poster → offline)
# ---------------------------------------------------------------------------


class RunWeeklyTests(unittest.TestCase):
    def setUp(self):
        self.db, self.db_path = make_db()
        self.cfg = AppConfig()
        self.cfg.discord_webhook_url = "https://discord.example/hook"
        self.posts = []

    def tearDown(self):
        self.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def _poster(self, url, content):
        self.posts.append((url, content))

    def test_posts_digest_to_webhook(self):
        report = run_weekly(self.db, self.cfg, poster=self._poster)
        self.assertTrue(report["notified"])
        self.assertIsNone(report["error"])
        self.assertEqual(len(self.posts), 1)
        self.assertEqual(self.posts[0][0], "https://discord.example/hook")
        self.assertIn("weekly report", self.posts[0][1])

    def test_without_webhook_still_returns_report(self):
        self.cfg.discord_webhook_url = None
        report = run_weekly(self.db, self.cfg, poster=self._poster)
        self.assertFalse(report["notified"])
        self.assertEqual(self.posts, [])
        self.assertIn("submitted_this_week", report)

    def test_builder_crash_is_reported_not_raised(self):
        with patch("zeyrecuite.weekly_report.build_week_report",
                   side_effect=RuntimeError("db exploded")):
            report = run_weekly(self.db, self.cfg, poster=self._poster)
        self.assertEqual(report["error"], "db exploded")
        self.assertTrue(report["notified"])
        self.assertIn("failed", self.posts[0][1])


# ---------------------------------------------------------------------------
# Cron wrapper (APScheduler, offline — never waits for the trigger)
# ---------------------------------------------------------------------------


class CronWrapperTests(unittest.TestCase):
    def setUp(self):
        self.db, self.db_path = make_db()

    def tearDown(self):
        self.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_start_status_stop(self):
        cfg = _build({"weekly_report": {"enabled": "true", "day": "fri", "at": "07:30"}})
        wr = build_weekly_report(self.db, cfg)
        self.addCleanup(wr.stop)
        self.assertFalse(wr.running)
        status = wr.status()
        self.assertTrue(status["enabled"])
        self.assertEqual(status["day"], "fri")
        self.assertEqual(status["at"], "07:30")
        self.assertFalse(status["running"])
        self.assertIsNone(status["next_run"])
        wr.start()
        self.assertTrue(wr.running)
        status = wr.status()
        self.assertTrue(status["running"])
        self.assertIsNotNone(status["next_run"])
        wr.start()  # idempotent second start is a no-op
        self.assertTrue(wr.running)
        wr.stop()
        self.assertFalse(wr.running)

    def test_run_now_returns_report(self):
        cfg = AppConfig()
        cfg.discord_webhook_url = None
        wr = build_weekly_report(self.db, cfg)
        report = wr.run_now()
        self.assertIn("submitted_this_week", report)
        self.assertFalse(report["notified"])


# ---------------------------------------------------------------------------
# API endpoints (authenticated, offline)
# ---------------------------------------------------------------------------


class EndpointTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        self.db_path = tmp.name
        self.cfg = AppConfig(database_url=f"sqlite:///{self.db_path}")
        self.cfg.discord_webhook_url = None  # offline: notify.send returns False
        self.app = create_app(self.cfg)
        self.client = TestClient(self.app)
        with self.client:  # triggers lifespan (seeds user/profile, builds runner)
            r = self.client.post(
                "/api/auth/login", json={"username": "admin", "password": "zeyrecuite"}
            )
            self.token = r.json()["token"]
        self.h = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        for state_name in ("weekly_report", "daily_submit"):
            runner = getattr(self.app.state, state_name, None)
            if runner is not None:
                runner.stop()
        self.app.state.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_lifespan_builds_runner_without_starting(self):
        wr = self.app.state.weekly_report
        self.assertIsNotNone(wr)
        self.assertFalse(wr.running)  # disabled by default → not scheduled
        self.assertFalse(self.cfg.weekly_report.enabled)

    def test_status_endpoint(self):
        r = self.client.get("/api/weekly-report/status", headers=self.h)
        self.assertEqual(r.status_code, 200)
        body = r.json()
        for key in ("enabled", "running", "day", "at", "next_run",
                    "discord_configured"):
            self.assertIn(key, body)
        self.assertEqual(body["day"], "sun")
        self.assertEqual(body["at"], "18:00")
        self.assertFalse(body["discord_configured"])

    def test_run_endpoint_offline(self):
        r = self.client.post("/api/weekly-report/run", headers=self.h)
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertIn("submitted_this_week", body)
        self.assertIn("by_date", body)
        self.assertFalse(body["notified"])
        self.assertIsNone(body["error"])

    def test_requires_auth(self):
        self.assertEqual(
            self.client.get("/api/weekly-report/status").status_code, 401
        )
        self.assertEqual(
            self.client.post("/api/weekly-report/run").status_code, 401
        )


if __name__ == "__main__":
    unittest.main()




"""Tests for the daily auto-submit runner and Discord notifications.

The daily runner picks the highest-confidence directly-submittable job once a
day, approves it, runs the injected submission pipeline, and posts the outcome
to Discord. Everything runs offline: the submitter and webhook poster are
injected fakes, and browser automation is disabled under pytest
(apply.browser_available).
"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from zeyrecuite import notify
from zeyrecuite.app import _submit_application, create_app
from zeyrecuite.config import AppConfig, _build
from zeyrecuite.daily_submit import build_daily_submitter, pick_top_job, pending_count, run_daily
from zeyrecuite.models import Application, Job


# ---------------------------------------------------------------------------
# Config parsing
# ---------------------------------------------------------------------------


class DailyConfigTests(unittest.TestCase):
    def test_defaults_off(self):
        cfg = _build({})
        self.assertFalse(cfg.daily_auto_submit.enabled)
        self.assertEqual((cfg.daily_auto_submit.hour, cfg.daily_auto_submit.minute), (9, 0))
        self.assertIsNone(cfg.discord_webhook_url)

    def test_parses_at_enabled_and_webhook(self):
        cfg = _build({
            "daily_auto_submit": {"enabled": "true", "at": "14:30"},
            "discord_webhook_url": "https://discord.com/api/webhooks/1/abc",
        })
        self.assertTrue(cfg.daily_auto_submit.enabled)
        self.assertEqual((cfg.daily_auto_submit.hour, cfg.daily_auto_submit.minute), (14, 30))
        self.assertEqual(cfg.discord_webhook_url, "https://discord.com/api/webhooks/1/abc")

    def test_invalid_at_falls_back_to_morning(self):
        for bad in ("morning", "25:99", "09", None):
            cfg = _build({"daily_auto_submit": {"at": bad}})
            self.assertEqual(
                (cfg.daily_auto_submit.hour, cfg.daily_auto_submit.minute), (9, 0), bad
            )

    def test_disabled_string_and_blank_webhook(self):
        cfg = _build({"daily_auto_submit": {"enabled": "false"}, "discord_webhook_url": ""})
        self.assertFalse(cfg.daily_auto_submit.enabled)
        self.assertIsNone(cfg.discord_webhook_url)


# ---------------------------------------------------------------------------
# Discord notifier
# ---------------------------------------------------------------------------


class NotifyTests(unittest.TestCase):
    def test_missing_url_skips_without_posting(self):
        posts = []
        ok = notify.send(None, "hello", poster=lambda u, c: posts.append((u, c)))
        self.assertFalse(ok)
        self.assertEqual(posts, [])

    def test_posts_content(self):
        posts = []
        ok = notify.send(
            "https://discord.example/hook", "hello there",
            poster=lambda u, c: posts.append((u, c)),
        )
        self.assertTrue(ok)
        self.assertEqual(posts, [("https://discord.example/hook", "hello there")])

    def test_poster_error_is_swallowed(self):
        def boom(url, content):
            raise RuntimeError("network down")

        self.assertFalse(notify.send("https://x/hook", "hi", poster=boom))

    def test_everyone_ping_is_neutralized(self):
        posts = []
        notify.send(
            "https://x/hook", "@everyone and @here too",
            poster=lambda u, c: posts.append((u, c)),
        )
        self.assertNotIn("@everyone", posts[0][1])
        self.assertNotIn("@here", posts[0][1])
        self.assertIn("and", posts[0][1])

    def test_content_capped_at_discord_limit(self):
        posts = []
        notify.send("https://x/hook", "x" * 5000, poster=lambda u, c: posts.append((u, c)))
        self.assertLessEqual(len(posts[0][1]), notify.MAX_CONTENT_LENGTH)


# ---------------------------------------------------------------------------
# Shared temp-DB harness
# ---------------------------------------------------------------------------


class DailySubmitBase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        self.db_path = tmp.name
        self.cfg = AppConfig(database_url=f"sqlite:///{self.db_path}")
        # Webhook configured so reports can be asserted; poster is injected.
        self.cfg.discord_webhook_url = "https://discord.example/hook"
        self.app = create_app(self.cfg)
        self.client = TestClient(self.app)
        with self.client:  # triggers lifespan (seeds user + blank profile)
            r = self.client.post(
                "/api/auth/login", json={"username": "admin", "password": "zeyrecuite"}
            )
            self.token = r.json()["token"]
        self.h = {"Authorization": f"Bearer {self.token}"}
        self.posts = []
        self._seed_seq = 0

    def tearDown(self):
        ds = getattr(self.app.state, "daily_submit", None)
        if ds is not None:
            ds.stop()
        self.app.state.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def _poster(self, url, content):
        self.posts.append((url, content))

    def _seed(self, **kw):
        self._seed_seq += 1
        defaults = dict(
            fingerprint=f"fp{self._seed_seq}",
            title=f"Job {self._seed_seq}",
            company=f"Co{self._seed_seq}",
            location="Remote", work_mode="remote", source="fake",
            url=f"https://x/{self._seed_seq}",
            application_url=f"https://x/{self._seed_seq}/apply",
            description="Write requirements, build SQL reports and dashboards.",
            skills=["SQL", "Excel"],
            location_status="eligible", status="new",
            confidence=50.0, eligibility=80.0,
        )
        defaults.update(kw)
        with self.app.state.db.session() as s:
            s.add(Job(**defaults))
            s.commit()

    def _run(self, submitter):
        return run_daily(self.app.state.db, self.cfg, submitter=submitter, poster=self._poster)


class PickTopJobTests(DailySubmitBase):
    def test_highest_confidence_among_eligible_wins(self):
        self._seed(title="Low", confidence=60.0)
        self._seed(title="Best", confidence=95.0)
        self._seed(title="NoLink", confidence=99.0, application_url=None)
        self._seed(title="Rejected", confidence=98.0, status="rejected")
        self._seed(title="Gated", confidence=97.0, location_status="review")
        with self.app.state.db.session() as s:
            job = pick_top_job(s)
            self.assertIsNotNone(job)
            self.assertEqual(job.title, "Best")

    def test_skips_submitted_and_exhausted_jobs(self):
        self._seed(title="Done", confidence=99.0)
        self._seed(title="Tried", confidence=98.0)
        self._seed(title="Fresh", confidence=70.0)
        with self.app.state.db.session() as s:
            done = s.query(Job).filter(Job.title == "Done").one()
            tried = s.query(Job).filter(Job.title == "Tried").one()
            s.add(Application(job_id=done.id, status="submitted", attempts=1))
            s.add(Application(job_id=tried.id, status="ready", attempts=3))
            s.commit()
            job = pick_top_job(s)
            self.assertEqual(job.title, "Fresh")
            self.assertEqual(pending_count(s), 1)


# ---------------------------------------------------------------------------
# run_daily: pick → approve → submit → Discord
# ---------------------------------------------------------------------------


class RunDailyTests(DailySubmitBase):
    def _fake_submitter(self, error=None):
        calls = []

        def submit(job):
            calls.append(job.id)
            if error:
                raise error
            return {
                "status": "submitted",
                "submission_url": "https://x/apply",
                "submission_method": "auto-web",
                "submission_message": "Receipt confirmed.",
            }

        submit.calls = calls
        return submit

    def test_approves_submits_and_notifies(self):
        self._seed(title="Daily Pick", confidence=91.0)
        sub = self._fake_submitter()
        report = self._run(sub)
        self.assertEqual(report["outcome"], "submitted")
        self.assertEqual(len(sub.calls), 1)
        self.assertTrue(report["notified"])
        self.assertEqual(report["job"]["title"], "Daily Pick")
        with self.app.state.db.session() as s:
            self.assertEqual(s.query(Job).one().status, "approved")
        joined = "".join(c for _, c in self.posts)
        self.assertIn("Daily Pick", joined)
        self.assertIn("91", joined)
        self.assertIn("auto-web", joined)

    def test_nothing_submittable_reports_and_skips(self):
        sub = self._fake_submitter()
        report = self._run(sub)
        self.assertEqual(report["outcome"], "nothing_to_submit")
        self.assertEqual(sub.calls, [])
        self.assertTrue(report["notified"])
        self.assertIn("No directly submittable job today", "".join(c for _, c in self.posts))

    def test_submitter_crash_is_reported_not_raised(self):
        self._seed(confidence=90.0)
        sub = self._fake_submitter(error=RuntimeError("browser exploded"))
        report = self._run(sub)
        self.assertIsNone(report["outcome"])
        self.assertIn("browser exploded", report["error"])
        self.assertTrue(report["notified"])
        self.assertIn("failed", "".join(c for _, c in self.posts))

    def test_without_webhook_still_returns_report(self):
        self.cfg.discord_webhook_url = None
        self._seed(confidence=90.0)
        sub = self._fake_submitter()
        report = self._run(sub)
        self.assertEqual(report["outcome"], "submitted")
        self.assertFalse(report["notified"])
        self.assertEqual(self.posts, [])

    def test_real_pipeline_records_honest_application(self):
        self._seed(title="Real Pipeline", confidence=92.0, application_url="https://acme.test/apply")
        report = self._run(lambda job: _submit_application(self.app.state.db, job))
        # Browser is disabled under pytest; with a direct link the legacy wording
        # still records a submitted application with the link.
        self.assertEqual(report["outcome"], "submitted")
        with self.app.state.db.session() as s:
            row = s.query(Application).one()
            self.assertEqual(row.status, "submitted")
            self.assertEqual(row.submission_url, "https://acme.test/apply")
            self.assertEqual(row.attempts, 1)
            self.assertTrue(row.submission_method)
            self.assertEqual(s.query(Job).one().status, "approved")


# ---------------------------------------------------------------------------
# Cron wrapper + lifespan wiring + Discord test endpoint
# ---------------------------------------------------------------------------


class SchedulerWrapperTests(DailySubmitBase):
    def test_start_is_idempotent_and_status_reports(self):
        ds = build_daily_submitter(self.app.state.db, self.cfg, submitter=lambda j: {})
        self.addCleanup(ds.stop)
        self.assertFalse(ds.running)
        ds.start()
        ds.start()  # second start is a no-op
        self.assertTrue(ds.running)
        st = ds.status()
        self.assertFalse(st["enabled"])  # config default remains off
        self.assertEqual(st["at"], "09:00")
        self.assertTrue(st["discord_configured"])
        self.assertIsNotNone(st["next_run"])
        ds.stop()
        self.assertFalse(ds.running)

    def test_lifespan_creates_runner_but_does_not_start(self):
        ds = self.app.state.daily_submit
        self.assertIsNotNone(ds)
        self.assertFalse(ds.running)
        self.assertFalse(ds.status()["enabled"])


class DiscordEndpointTests(DailySubmitBase):
    def test_requires_auth(self):
        r = self.client.post("/api/notifications/discord/test")
        self.assertEqual(r.status_code, 401)

    def test_409_without_webhook(self):
        self.cfg.discord_webhook_url = None
        r = self.client.post("/api/notifications/discord/test", headers=self.h)
        self.assertEqual(r.status_code, 409)

    def test_sends_when_configured(self):
        with patch("zeyrecuite.notify.send", return_value=True) as m:
            r = self.client.post("/api/notifications/discord/test", headers=self.h)
        self.assertEqual(r.status_code, 200, r.text)
        self.assertTrue(r.json()["sent"])
        self.assertTrue(m.called)

    def test_502_when_webhook_fails(self):
        with patch("zeyrecuite.notify.send", return_value=False):
            r = self.client.post("/api/notifications/discord/test", headers=self.h)
        self.assertEqual(r.status_code, 502)


if __name__ == "__main__":
    unittest.main()
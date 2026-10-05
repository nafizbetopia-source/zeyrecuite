"""Tests for manual application status tracking (no email connected).

When no email is connected the user still needs to track where each
application stands. This feature adds an ``application_status`` column on the
``Application`` table plus a ``POST /api/jobs/{job_id}/application-status``
endpoint that lets the SPA move an application through:

    draft -> ready -> submitting -> submitted | failed

All tests run fully offline against a temp-file SQLite database.
"""
import tempfile
import unittest

from fastapi.testclient import TestClient

from zeyrecuite.app import create_app
from zeyrecuite.config import AppConfig
from zeyrecuite.models import Job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_app():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    cfg = AppConfig(database_url=f"sqlite:///{tmp.name}")
    app = create_app(cfg)
    return app, tmp.name


def _seed_job(client, headers, **kw):
    from zeyrecuite.models import Job
    defaults = dict(
        fingerprint="fp1", title="Senior Business Analyst", company="Stripe",
        location="Remote", work_mode="remote", source="fake",
        url="https://x/1", application_url="https://x/1/apply",
        description="Work with stakeholders, write requirements, build SQL reports.",
        skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
        location_status="eligible", status="approved",
        confidence=88.0, confidence_label="Excellent match",
        eligibility=100.0, eligibility_label="Fully eligible",
    )
    defaults.update(kw)
    with client.app.state.db.session() as s:
        job = Job(**defaults)
        s.add(job)
        s.commit()
        return job.id


class ApplicationStatusTests(unittest.TestCase):
    def setUp(self):
        self.app, self.tmp = _make_app()
        self.client = TestClient(self.app)
        with self.client:  # triggers lifespan (seeds user + blank profile)
            r = self.client.post("/api/auth/login", json={"username": "admin", "password": "zeyrecuite"})
            self.token = r.json()["token"]
            self.h = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        self.client.close()
        try:
            import os
            os.remove(self.tmp)
        except OSError:
            pass

    def test_invalid_status_rejected(self):
        job_id = _seed_job(self.client, self.h)
        res = self.client.post(
            f"/api/jobs/{job_id}/application-status",
            json={"status": "bogus"},
            headers=self.h,
        )
        self.assertEqual(res.status_code, 422)

    def test_job_not_found(self):
        res = self.client.post(
            "/api/jobs/999999/application-status",
            json={"status": "ready"},
            headers=self.h,
        )
        self.assertEqual(res.status_code, 404)

    def test_unauthorized(self):
        job_id = _seed_job(self.client, self.h)
        res = self.client.post(
            f"/api/jobs/{job_id}/application-status",
            json={"status": "ready"},
        )
        self.assertEqual(res.status_code, 401)

    def test_status_persists_and_roundtrips(self):
        job_id = _seed_job(self.client, self.h)
        for stage in ["draft", "ready", "submitting", "submitted"]:
            res = self.client.post(
                f"/api/jobs/{job_id}/application-status",
                json={"status": stage},
                headers=self.h,
            )
            self.assertEqual(res.status_code, 200, res.text)
            self.assertEqual(res.json()["application"]["application_status"], stage)

    def test_failed_status_allowed(self):
        job_id = _seed_job(self.client, self.h)
        res = self.client.post(
            f"/api/jobs/{job_id}/application-status",
            json={"status": "failed"},
            headers=self.h,
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["application"]["application_status"], "failed")

    def test_creates_application_record_if_missing(self):
        # A job with no Application row yet should get one created on first move.
        job_id = _seed_job(self.client, self.h, status="new")
        res = self.client.post(
            f"/api/jobs/{job_id}/application-status",
            json={"status": "ready"},
            headers=self.h,
        )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertIsNotNone(res.json()["application"])
        self.assertEqual(res.json()["application"]["application_status"], "ready")


if __name__ == "__main__":
    unittest.main()

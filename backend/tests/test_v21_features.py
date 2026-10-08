"""Tests for the v2.1 feature set: multi-factor confidence engine, eligibility,
submission tracking, top-10, analytics, re-score, and DB migration."""
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from zeyrecuite.app import create_app
from zeyrecuite.config import AppConfig
from zeyrecuite.database import Database
from zeyrecuite.models import Job, Profile
from zeyrecuite.scoring import assess_job, eligibility_score, score_job


# ---------- Scoring engine ----------

class AssessJobTests(unittest.TestCase):
    def test_strong_ba_match_high_confidence(self):
        a = assess_job(
            title="Senior Business Analyst",
            description="Work with stakeholders, write requirements, build SQL reports and dashboards.",
            job_skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
            profile_skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
            location_status="eligible",
            work_mode="remote",
            company_overall=4.5,
            posted_date="2 days ago",
            application_url="https://x/apply",
        )
        self.assertGreater(a.confidence, 60)
        self.assertEqual(len(a.factors), 6)
        self.assertIn(a.confidence_label, ("Strong match", "Excellent match"))
        self.assertGreater(a.eligibility, 80)

    def test_unrelated_role_low_confidence(self):
        a = assess_job(
            title="Barista",
            description="Make coffee and serve customers.",
            job_skills=["Espresso"],
            profile_skills=["SQL", "Excel"],
            location_status="eligible",
            work_mode="remote",
        )
        self.assertLess(a.confidence, 45)
        self.assertIn("Weak match", a.confidence_label)

    def test_deterministic(self):
        kwargs = dict(
            title="Business Analyst",
            description="sql excel reporting stakeholder",
            job_skills=["SQL", "Excel", "Reporting"],
            profile_skills=["SQL", "Excel", "Reporting"],
            location_status="eligible",
            work_mode="remote",
            company_overall=4.0,
            posted_date="5 days ago",
        )
        a1 = assess_job(**kwargs)
        a2 = assess_job(**kwargs)
        self.assertEqual(a1.confidence, a2.confidence)
        self.assertEqual(a1.eligibility, a2.eligibility)

    def test_confidence_bounded(self):
        a = assess_job(
            title="Business Analyst",
            description="sql excel reporting stakeholder requirements dashboards",
            job_skills=["SQL", "Excel", "Reporting", "Stakeholder Management"],
            profile_skills=["SQL", "Excel", "Reporting", "Stakeholder Management"],
            location_status="eligible",
            work_mode="remote",
            company_overall=5.0,
            posted_date="today",
            application_url="https://x",
        )
        self.assertGreaterEqual(a.confidence, 0)
        self.assertLessEqual(a.confidence, 100)

    def test_no_skills_no_crash(self):
        a = assess_job(
            title="Business Analyst",
            description="general role",
            job_skills=None,
            profile_skills=["SQL"],
            location_status="eligible",
            work_mode="remote",
        )
        self.assertGreaterEqual(a.confidence, 0)
        self.assertLessEqual(a.confidence, 100)

    def test_no_posted_date_neutral(self):
        a = assess_job(
            title="Business Analyst",
            description="sql excel",
            job_skills=["SQL"],
            profile_skills=["SQL"],
            location_status="eligible",
            work_mode="remote",
            posted_date=None,
        )
        fresh = next(f for f in a.factors if f.key == "freshness")
        self.assertEqual(fresh.value, 50.0)

    def test_factors_have_details(self):
        a = assess_job(
            title="Business Analyst",
            description="sql excel reporting",
            job_skills=["SQL", "Excel"],
            profile_skills=["SQL", "Excel"],
            location_status="eligible",
            work_mode="remote",
        )
        for f in a.factors:
            self.assertTrue(f.detail)
            self.assertGreaterEqual(f.value, 0)
            self.assertLessEqual(f.value, 100)

    def test_score_job_backward_compat(self):
        r = score_job(
            title="Senior Business Analyst",
            description="sql excel reporting stakeholder",
            job_skills=["SQL", "Excel"],
            profile_skills=["SQL", "Excel"],
        )
        self.assertGreater(r.score, 40)
        self.assertIn("matched_skills", r.breakdown)


class EligibilityTests(unittest.TestCase):
    def test_eligible_remote_high(self):
        score, label, _ = eligibility_score(
            location_status="eligible", work_mode="remote", salary=None, min_salary=None
        )
        self.assertGreaterEqual(score, 90)
        self.assertEqual(label, "Fully eligible")

    def test_rejected_zero(self):
        score, label, _ = eligibility_score(
            location_status="rejected", work_mode="remote", salary=None, min_salary=None
        )
        self.assertEqual(score, 0)
        self.assertEqual(label, "Not eligible")

    def test_review_reduced(self):
        score, _, _ = eligibility_score(
            location_status="review", work_mode="remote", salary=None, min_salary=None
        )
        self.assertLess(score, 100)
        self.assertGreater(score, 0)

    def test_onsite_penalized(self):
        remote, _, _ = eligibility_score(
            location_status="eligible", work_mode="remote", salary=None, min_salary=None
        )
        onsite, _, _ = eligibility_score(
            location_status="eligible", work_mode="onsite", salary=None, min_salary=None
        )
        self.assertLess(onsite, remote)

    def test_salary_below_floor_penalized(self):
        ok, _, _ = eligibility_score(
            location_status="eligible", work_mode="remote", salary="$120,000", min_salary=100
        )
        low, _, _ = eligibility_score(
            location_status="eligible", work_mode="remote", salary="$60,000", min_salary=100
        )
        self.assertGreater(ok, low)


# ---------- API-level tests ----------

def _make_app():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    cfg = AppConfig(database_url=f"sqlite:///{tmp.name}")
    app = create_app(cfg)
    return app, tmp.name


class ApiFeatureTests(unittest.TestCase):
    def setUp(self):
        self.app, self.db_path = _make_app()
        self.client = TestClient(self.app)
        with self.client:  # triggers lifespan (seeds user + profile)
            r = self.client.post("/api/auth/login", json={"username": "admin", "password": "zeyrecuite"})
            self.token = r.json()["token"]
            self.h = {"Authorization": f"Bearer {self.token}"}
            # Seed a couple of jobs directly.
            db = self.app.state.db
            with db.session() as s:
                s.add(Job(
                    fingerprint="fp1", title="Senior Business Analyst", company="Stripe",
                    location="Remote", work_mode="remote", source="fake",
                    url="https://x/1", application_url="https://x/1/apply",
                    description="Work with stakeholders, write requirements, build SQL reports and dashboards.",
                    skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
                    location_status="eligible", status="new",
                    confidence=88.0, confidence_label="Excellent match",
                    eligibility=100.0, eligibility_label="Fully eligible",
                ))
                s.add(Job(
                    fingerprint="fp2", title="Barista", company="Coffee Co",
                    location="Remote", work_mode="remote", source="fake",
                    url="https://x/2", application_url=None,
                    description="Make coffee.", skills=["Espresso"],
                    location_status="eligible", status="new",
                    confidence=20.0, confidence_label="Weak match",
                    eligibility=100.0, eligibility_label="Fully eligible",
                ))
                s.commit()

    def tearDown(self):
        self.app.state.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_top_returns_ordered(self):
        r = self.client.get("/api/top?limit=10", headers=self.h)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["title"], "Senior Business Analyst")  # higher confidence first
        self.assertEqual(data[0]["confidence"], 88.0)

    def test_analytics_shape(self):
        r = self.client.get("/api/analytics", headers=self.h)
        self.assertEqual(r.status_code, 200)
        d = r.json()
        self.assertEqual(d["total"], 2)
        self.assertIn("by_status", d)
        self.assertIn("confidence_buckets", d)
        self.assertIn("submissions_by_day", d)
        self.assertEqual(len(d["submissions_by_day"]), 14)
        self.assertIn("applications", d)

    def test_approve_creates_submission(self):
        r = self.client.get("/api/top?limit=10", headers=self.h)
        job_id = r.json()[0]["id"]
        r = self.client.post(f"/api/jobs/{job_id}/approve", headers=self.h)
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertEqual(body["job"]["status"], "approved")
        sub = body["submission"]
        self.assertEqual(sub["status"], "submitted")
        self.assertEqual(sub["submission_status"], "submitted")
        self.assertEqual(sub["attempts"], 1)
        self.assertTrue(sub["submission_url"])

    def test_approve_no_link_ready(self):
        # The auto-apply-only gate hides link-less jobs from the list view…
        r = self.client.get("/api/jobs", headers=self.h)
        self.assertFalse(any(j["title"] == "Barista" for j in r.json()))
        # …but approving one directly still degrades honestly to "ready".
        with self.app.state.db.session() as s:
            barista_id = s.query(Job).filter(Job.title == "Barista").one().id
        r = self.client.post(f"/api/jobs/{barista_id}/approve", headers=self.h)
        self.assertEqual(r.status_code, 200)
        sub = r.json()["submission"]
        self.assertEqual(sub["status"], "ready")
        self.assertEqual(sub["submission_status"], "ready")

    def test_approve_missing_404(self):
        r = self.client.post("/api/jobs/99999/approve", headers=self.h)
        self.assertEqual(r.status_code, 404)

    def test_rescore(self):
        r = self.client.post("/api/rescore", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["rescored"], 2)
        # After re-score, confidence is recomputed (still bounded).
        r = self.client.get("/api/top?limit=10", headers=self.h)
        for j in r.json():
            self.assertGreaterEqual(j["confidence"], 0)
            self.assertLessEqual(j["confidence"], 100)

    def test_detail_includes_application(self):
        r = self.client.get("/api/top?limit=10", headers=self.h)
        job_id = r.json()[0]["id"]
        self.client.post(f"/api/jobs/{job_id}/approve", headers=self.h)
        r = self.client.get(f"/api/jobs/{job_id}", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(r.json()["application"])
        self.assertEqual(r.json()["application"]["submission_status"], "submitted")

    def test_stats_includes_submitted(self):
        r = self.client.get("/api/stats", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertIn("submitted", r.json())
        self.assertIn("ready", r.json())


# ---------- Migration idempotency ----------

class MigrationTests(unittest.TestCase):
    def test_migration_idempotent(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        db = Database(f"sqlite:///{tmp.name}")
        db.create_all()
        # Run again — must not raise or duplicate columns.
        db.create_all()
        db.migrate()
        db.engine.dispose()
        Path(tmp.name).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

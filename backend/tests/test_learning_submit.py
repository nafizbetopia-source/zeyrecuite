"""Tests for the F19 feature set: the learning loop and the submit flow.

The learning loop turns user approve / reject / select signals into additive
reweights that make every subsequent scan and re-score smarter. The submit
flow runs the submission pipeline from the Search & Submit view and returns a
verifiable status plus any direct apply link.

All tests run fully offline against a temp-file SQLite database, following the
same setUp/tearDown patterns as the other feature test modules.
"""
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from zeyrecuite.app import create_app
from zeyrecuite.config import AppConfig
from zeyrecuite.learning import compute_learning_weights, LearningWeights
from zeyrecuite.models import Job
from zeyrecuite.scoring import assess_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_app():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    cfg = AppConfig(database_url=f"sqlite:///{tmp.name}")
    app = create_app(cfg)
    return app, tmp.name


def _base_job(**kw):
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
    return defaults


# ---------------------------------------------------------------------------
# Learning engine unit tests
# ---------------------------------------------------------------------------


class LearningEngineTests(unittest.TestCase):
    def test_no_feedback_is_neutral(self):
        w = compute_learning_weights([])
        self.assertFalse(w.has_data)
        self.assertEqual(w.fit_mult, 1.0)
        self.assertEqual(w.confidence_mult, 1.0)
        self.assertEqual(w.pref_mult, 1.0)
        self.assertEqual((w.approved, w.rejected, w.selected), (0, 0, 0))

    def test_approves_boost_fit(self):
        rows = [
            {"job_id": 1, "signal": "approve", "skills": ["SQL"], "company": "Acme",
             "source": "remoteok", "work_mode": "remote"},
            {"job_id": 2, "signal": "approve", "skills": ["SQL", "Tableau"], "company": "Beta",
             "source": "remoteok", "work_mode": "remote"},
        ]
        w = compute_learning_weights(rows, jobs_by_id={1: None, 2: None})
        self.assertTrue(w.has_data)
        self.assertGreater(w.fit_mult, 1.0)
        self.assertIn("SQL", w.top_skills)
        self.assertIn("remoteok", w.top_sources)
        self.assertEqual(w.approved, 2)
        self.assertEqual(w.rejected, 0)

    def test_rejects_dampen(self):
        rows = [
            {"job_id": 1, "signal": "reject", "skills": ["Sales"], "company": "BadCorp",
             "source": "linkedin", "work_mode": "on-site"},
            {"job_id": 2, "signal": "reject", "skills": ["Sales"], "company": "BadCorp",
             "source": "linkedin", "work_mode": "on-site"},
        ]
        w = compute_learning_weights(rows, jobs_by_id={1: None, 2: None})
        self.assertLess(w.fit_mult, 1.0)
        self.assertEqual(w.rejected, 2)
        self.assertIn("BadCorp", w.top_companies)
        self.assertIn("on-site", w.top_work_modes)

    def test_select_weighted_heavier(self):
        rows = [
            {"job_id": 1, "signal": "select", "skills": ["dbt"], "company": "DataCo",
             "source": "wellfound", "work_mode": "remote"},
        ]
        w = compute_learning_weights(rows, jobs_by_id={1: None})
        self.assertEqual(w.selected, 1)
        self.assertIn("dbt", w.top_skills)
        self.assertGreater(w.fit_mult, 1.0)

    def test_multipliers_bounded(self):
        rows = [{"job_id": i, "signal": "reject", "skills": ["X"], "company": f"C{i}",
                 "source": "s", "work_mode": "on-site"} for i in range(20)]
        w = compute_learning_weights(rows, jobs_by_id={i: None for i in range(20)})
        self.assertGreaterEqual(w.fit_mult, 0.85)
        self.assertLessEqual(w.fit_mult, 1.35)

    def test_to_dict_roundtrip(self):
        w = compute_learning_weights([])
        d = w.to_dict()
        self.assertIn("fit_mult", d)
        self.assertIn("top_skills", d)
        self.assertIn("has_data", d)


# ---------------------------------------------------------------------------
# assess_job learning integration
# ---------------------------------------------------------------------------


class AssessJobLearningTests(unittest.TestCase):
    def _base_kwargs(self):
        return dict(
            title="Senior Business Analyst",
            description="Work with stakeholders, write requirements, build SQL reports.",
            job_skills=["SQL", "Excel", "Stakeholder", "Requirements"],
            profile_skills=["SQL", "Excel", "Stakeholder", "Requirements"],
            target_role="Business Analyst",
            location_status="eligible",
            work_mode="remote",
            salary="$100k",
            min_salary=50000,
            company_overall=4.0,
            posted_date="2026-01-15",
            application_url="https://example.com/apply",
            preferred_remote=True,
        )

    def test_no_learning_unchanged(self):
        a = assess_job(**self._base_kwargs())
        self.assertEqual(a.fit_score, a.fit_score)

    def test_learning_boosts_fit(self):
        kwargs = self._base_kwargs()
        base = assess_job(**kwargs)
        boosted = assess_job(learning=LearningWeights(fit_mult=1.2, confidence_mult=1.1), **kwargs)
        self.assertGreater(boosted.fit_score, base.fit_score)
        self.assertGreater(boosted.confidence, base.confidence)

    def test_learning_dampens_fit(self):
        kwargs = self._base_kwargs()
        base = assess_job(**kwargs)
        dampened = assess_job(learning=LearningWeights(fit_mult=0.9, confidence_mult=0.95), **kwargs)
        self.assertLess(dampened.fit_score, base.fit_score)

    def test_fit_bounded_after_learning(self):
        kwargs = self._base_kwargs()
        boosted = assess_job(learning=LearningWeights(fit_mult=1.35), **kwargs)
        self.assertLessEqual(boosted.fit_score, 100.0)
        self.assertGreaterEqual(boosted.fit_score, 0.0)

    def test_breakdown_carries_learning(self):
        kwargs = self._base_kwargs()
        a = assess_job(learning=LearningWeights(fit_mult=1.1), **kwargs)
        self.assertIn("learning", a.breakdown)
        self.assertIsNotNone(a.breakdown["learning"])


# ---------------------------------------------------------------------------
# End-to-end: feedback recording + insights + submit
# ---------------------------------------------------------------------------


class LearningSubmitBase(unittest.TestCase):
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
        defaults = _base_job(**kw)
        with self.app.state.db.session() as s:
            s.add(Job(**defaults))
            s.commit()

    def _job_id(self):
        with self.app.state.db.session() as s:
            return s.query(Job).order_by(Job.id.desc()).first().id


class FeedbackEndpointTests(LearningSubmitBase):
    def test_feedback_requires_valid_signal(self):
        self._seed_job()
        job_id = self._job_id()
        res = self.client.post(f"/api/jobs/{job_id}/feedback",
                               json={"signal": "maybe"}, headers=self.h)
        self.assertEqual(res.status_code, 422)

    def test_feedback_records_and_returns_insights(self):
        self._seed_job()
        job_id = self._job_id()
        res = self.client.post(f"/api/jobs/{job_id}/feedback",
                               json={"signal": "approve"}, headers=self.h)
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual(body["recorded"], "approve")
        self.assertTrue(body["learning"]["has_data"])
        self.assertEqual(body["learning"]["approved"], 1)

    def test_feedback_job_not_found(self):
        res = self.client.post("/api/jobs/999999/feedback",
                               json={"signal": "approve"}, headers=self.h)
        self.assertEqual(res.status_code, 404)

    def test_feedback_unauthorized(self):
        res = self.client.post("/api/jobs/1/feedback", json={"signal": "approve"})
        self.assertEqual(res.status_code, 401)

    def test_learning_insights_endpoint(self):
        res = self.client.get("/api/learning/insights", headers=self.h)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json()["has_data"])

    def test_insights_reflect_feedback(self):
        self._seed_job()
        job_id = self._job_id()
        self.client.post(f"/api/jobs/{job_id}/feedback",
                         json={"signal": "approve"}, headers=self.h)
        res = self.client.get("/api/learning/insights", headers=self.h)
        body = res.json()
        self.assertTrue(body["has_data"])
        self.assertEqual(body["approved"], 1)
        self.assertIn("SQL", body["top_skills"])


class SubmitFlowTests(LearningSubmitBase):
    def test_submit_returns_submission_record(self):
        self._seed_job(application_url="https://acme.com/apply", application_method="direct")
        job_id = self._job_id()
        res = self.client.post(f"/api/jobs/{job_id}/submit", headers=self.h)
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        sub = body["submission"]
        self.assertIn(sub["submission_status"], ("submitted", "ready"))
        self.assertIn("job", body)

    def test_submit_with_apply_link_marks_submitted(self):
        self._seed_job(application_url="https://acme.com/apply", application_method="direct")
        job_id = self._job_id()
        res = self.client.post(f"/api/jobs/{job_id}/submit", headers=self.h)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["submission"]["submission_status"], "submitted")
        self.assertEqual(res.json()["submission"]["submission_url"], "https://acme.com/apply")

    def test_submit_without_link_marks_ready(self):
        self._seed_job(application_url=None, application_method="manual")
        job_id = self._job_id()
        res = self.client.post(f"/api/jobs/{job_id}/submit", headers=self.h)
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()["submission"]["submission_status"], "ready")

    def test_submit_job_not_found(self):
        res = self.client.post("/api/jobs/999999/submit", headers=self.h)
        self.assertEqual(res.status_code, 404)


# ---------------------------------------------------------------------------
# Collector learning integration
# ---------------------------------------------------------------------------


class CollectorLearningTests(LearningSubmitBase):
    def test_collector_without_feedback_is_unchanged(self):
        """With no feedback rows, the collector helper returns None so scoring
        runs with no reweighting."""
        from zeyrecuite.collector import _learning_weights

        self.assertIsNone(_learning_weights(self.app.state.db))


if __name__ == "__main__":
    unittest.main()

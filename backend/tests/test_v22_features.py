"""Tests for the v2.2 feature set: no-fake-data profile, comprehensive profile
fields, auto-generated Top-10 materials, and the prefilled/editable
application form."""
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from zeyrecuite.app import create_app
from zeyrecuite.config import AppConfig
from zeyrecuite.models import Job, Profile


def _make_app():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    cfg = AppConfig(database_url=f"sqlite:///{tmp.name}")
    app = create_app(cfg)
    return app, tmp.name


class ProfileBase(unittest.TestCase):
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


# ---------- No fake data ----------

class NoFakeDataTests(ProfileBase):
    def test_profile_starts_blank(self):
        r = self.client.get("/api/profile", headers=self.h)
        self.assertEqual(r.status_code, 200)
        p = r.json()
        self.assertIn(p["name"], (None, ""))
        self.assertIn(p["email"], (None, ""))
        self.assertEqual(p["skills"], [])
        self.assertEqual(p["experiences"], [])
        self.assertEqual(p["education"], [])

    def test_fake_seed_is_cleared(self):
        # Simulate the legacy fake seed, then re-run lifespan.
        with self.app.state.db.session() as s:
            prof = s.get(Profile, 1)
            prof.name = "Your Name"
            prof.email = "you@example.com"
            prof.experiences = [{"role": "Business Analyst", "company": "Company A",
                                 "period": "2022 - Present", "bullets": ["x"]}]
            s.commit()
        # Re-enter lifespan to trigger the one-time cleanup.
        with self.client:
            pass
        r = self.client.get("/api/profile", headers=self.h)
        p = r.json()
        self.assertIn(p["name"], (None, ""))
        self.assertEqual(p["experiences"], [])


# ---------- Comprehensive profile ----------

class ComprehensiveProfileTests(ProfileBase):
    def test_update_all_fields(self):
        body = {
            "name": "Nafiz Ahmed", "email": "nafiz@real.com", "phone": "+8801700000000",
            "linkedin": "linkedin.com/in/nafiz", "website": "nafiz.dev", "github": "github.com/nafiz",
            "current_country": "Bangladesh", "city": "Dhaka", "timezone": "UTC+6",
            "availability": "Immediate", "notice_period": "Immediate",
            "role": "Business Analyst", "years_experience": 4,
            "summary": "BA with 4 years in fintech.",
            "skills": ["SQL", "Excel", "Power BI"], "keywords": ["stakeholder", "reporting"],
            "languages": ["English", "Bengali"], "interests": ["data viz"],
            "certifications": [{"name": "PMP", "issuer": "PMI", "year": "2023"}],
            "projects": [{"name": "Dashboards", "tech": "Power BI", "description": "Built KPI dashboards"}],
            "experiences": [{"role": "BA", "company": "Fintech Co", "period": "2022 - Present",
                             "bullets": ["Led requirements", "Built SQL reports"]}],
            "education": [{"degree": "B.Sc. CS", "school": "BUET", "period": "2018 - 2022"}],
            "expected_salary": "$80k", "min_salary": "$60k",
            "work_authorization": "Bangladesh citizen", "visa_status": "N/A",
            "preferred_work_mode": "Remote",
            "target_companies": ["Stripe", "Coinbase"], "deal_breakers": ["no on-site"],
        }
        r = self.client.put("/api/profile", headers=self.h, json=body)
        self.assertEqual(r.status_code, 200)
        p = r.json()
        self.assertEqual(p["name"], "Nafiz Ahmed")
        self.assertEqual(p["city"], "Dhaka")
        self.assertEqual(p["years_experience"], 4)
        self.assertEqual(p["certifications"], [{"name": "PMP", "issuer": "PMI", "year": "2023"}])
        self.assertEqual(p["projects"][0]["name"], "Dashboards")
        self.assertEqual(p["experiences"][0]["company"], "Fintech Co")
        self.assertEqual(p["education"][0]["school"], "BUET")
        self.assertEqual(p["expected_salary"], "$80k")
        self.assertEqual(p["target_companies"], ["Stripe", "Coinbase"])

    def test_clearing_fields(self):
        self.client.put("/api/profile", headers=self.h, json={"name": "Temp", "skills": ["SQL"]})
        r = self.client.put("/api/profile", headers=self.h, json={"name": None, "skills": []})
        self.assertEqual(r.status_code, 200)
        p = r.json()
        self.assertIsNone(p["name"])
        self.assertEqual(p["skills"], [])


# ---------- Auto-generate Top 10 ----------

class AutoGenerateTopTests(ProfileBase):
    def test_rescore_generates_top_materials(self):
        self._seed_job()
        r = self.client.post("/api/rescore", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(r.json()["prepared_top"], 1)
        # The top job should now have a resume PDF + cover letter.
        r = self.client.get("/api/top?limit=10", headers=self.h)
        top = r.json()[0]
        self.assertTrue(top["materials_ready"])
        r = self.client.get(f"/api/jobs/{top['id']}", headers=self.h)
        app = r.json()["application"]
        self.assertIsNotNone(app["resume_pdf"])
        self.assertTrue(app["cover_letter"])

    def test_top_materials_ready_flag(self):
        self._seed_job()
        self.client.post("/api/rescore", headers=self.h)
        r = self.client.get("/api/top?limit=10", headers=self.h)
        self.assertTrue(r.json()[0]["materials_ready"])

    def test_cover_letter_placeholder_when_blank(self):
        self._seed_job()
        self.client.post("/api/rescore", headers=self.h)
        r = self.client.get("/api/top?limit=10", headers=self.h)
        top = r.json()[0]
        r = self.client.get(f"/api/jobs/{top['id']}", headers=self.h)
        letter = r.json()["application"]["cover_letter"]
        self.assertIn("not complete", letter)

    def test_cover_letter_uses_real_data(self):
        self._seed_job()
        self.client.put("/api/profile", headers=self.h, json={
            "name": "Nafiz Ahmed", "role": "Business Analyst",
            "skills": ["SQL", "Excel", "Power BI"], "summary": "Fintech BA.",
        })
        self.client.post("/api/rescore", headers=self.h)
        r = self.client.get("/api/top?limit=10", headers=self.h)
        top = r.json()[0]
        r = self.client.get(f"/api/jobs/{top['id']}", headers=self.h)
        letter = r.json()["application"]["cover_letter"]
        self.assertIn("Nafiz Ahmed", letter)
        self.assertIn("Business Analyst", letter)
        self.assertNotIn("not complete", letter)


# ---------- Application form (prefill + save) ----------

class ApplicationFormTests(ProfileBase):
    def test_prefill_from_profile(self):
        self._seed_job()
        self.client.put("/api/profile", headers=self.h, json={
            "name": "Nafiz Ahmed", "email": "nafiz@real.com", "phone": "+8801700000000",
            "city": "Dhaka", "current_country": "Bangladesh", "timezone": "UTC+6",
            "notice_period": "Immediate", "expected_salary": "$80k",
            "work_authorization": "Bangladesh citizen", "availability": "Immediate",
            "preferred_work_mode": "Remote", "years_experience": 4,
            "languages": ["English", "Bengali"],
            "certifications": [{"name": "PMP", "issuer": "PMI", "year": "2023"}],
        })
        r = self.client.get("/api/jobs/1/application-form", headers=self.h)
        self.assertEqual(r.status_code, 200)
        f = r.json()
        self.assertEqual(f["name"], "Nafiz Ahmed")
        self.assertEqual(f["email"], "nafiz@real.com")
        self.assertEqual(f["current_location"], "Dhaka, Bangladesh")
        self.assertEqual(f["expected_salary"], "$80k")
        self.assertEqual(f["languages"], "English, Bengali")
        self.assertEqual(f["certifications"], "PMP")
        self.assertEqual(f["job_title"], "Senior Business Analyst")
        self.assertFalse(f["saved"])

    def test_save_and_retrieve_edits(self):
        self._seed_job()
        self.client.put("/api/profile", headers=self.h, json={"name": "Nafiz Ahmed"})
        # Save an edited form.
        r = self.client.put("/api/jobs/1/application-form", headers=self.h, json={
            "name": "Nafiz A. Ahmed", "email": "nafiz@real.com", "phone": "+8801700000000",
            "expected_salary": "$90k", "cover_letter": "Dear team, I am excited...",
        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["saved"])
        # Retrieve — saved edits take precedence.
        r = self.client.get("/api/jobs/1/application-form", headers=self.h)
        f = r.json()
        self.assertEqual(f["name"], "Nafiz A. Ahmed")
        self.assertEqual(f["expected_salary"], "$90k")
        self.assertTrue(f["saved"])
        self.assertIn("excited", f["cover_letter"])

    def test_save_syncs_cover_letter(self):
        self._seed_job()
        self.client.put("/api/jobs/1/application-form", headers=self.h, json={
            "name": "Nafiz", "cover_letter": "My custom letter body.",
        })
        r = self.client.get("/api/jobs/1", headers=self.h)
        self.assertEqual(r.json()["application"]["cover_letter"], "My custom letter body.")

    def test_form_404_missing_job(self):
        r = self.client.get("/api/jobs/99999/application-form", headers=self.h)
        self.assertEqual(r.status_code, 404)


if __name__ == "__main__":
    unittest.main()

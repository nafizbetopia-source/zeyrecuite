"""Phase 4 tests: company career-site discovery + browser-submission helpers.

Everything runs fully offline — page fetches are injected (``fetcher=``), ATS
API calls are patched, and the Playwright browser is never launched
(``browser_available()`` is False under pytest unless ZEYRECUITE_BROWSER_SUBMIT=1).
"""
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from fastapi.testclient import TestClient

from zeyrecuite.adapters import (
    CompanySiteAdapter,
    _scrape_jobs_html,
    clear_probe_cache,
    detect_ats,
    probe_careers_page,
)
from zeyrecuite.apply import (
    browser_available,
    detect_submit_target,
    is_success_page,
    plan_fills,
)
from zeyrecuite.app import _submit_application, create_app
from zeyrecuite.config import AppConfig
from zeyrecuite.models import Application, Job

# ---------------------------------------------------------------------------
# Sample pages
# ---------------------------------------------------------------------------

GREENHOUSE_PAGE = """
<html><head>
<script src="https://boards.greenhouse.io/embed/job_widget.js"></script>
<script>const x = "https://job-boards.greenhouse.io/embed?b=acme-corp";</script>
</head><body><a href="/careers/senior-engineer">Senior Engineer</a></body></html>
"""

LEVER_PAGE = '<a href="https://jobs.lever.co/leverdemo/1234-abcd">Backend Developer</a>'

PLAIN_PAGE = """
<html><body>
  <a href="https://www.linkedin.com/company/acme">LinkedIn</a>
  <a href="/careers/senior-backend-engineer">Senior Backend Engineer</a>
  <a href="/careers">Careers</a>
  <a href="#top">Back to top</a>
</body></html>
"""


class DetectAtsTests(unittest.TestCase):
    def test_greenhouse_detected_with_token(self):
        d = detect_ats(GREENHOUSE_PAGE, "https://acme.com/careers")
        self.assertIsNotNone(d)
        self.assertEqual(d["ats"], "greenhouse")
        self.assertEqual(d["token"], "acme-corp")

    def test_lever_detected(self):
        d = detect_ats(LEVER_PAGE, "https://acme.com/careers")
        self.assertEqual(d, {"ats": "lever", "token": "leverdemo"})

    def test_plain_page_has_no_ats(self):
        self.assertIsNone(detect_ats(PLAIN_PAGE, "https://acme.com/careers"))

    def test_careers_url_pointing_at_ats(self):
        d = detect_ats("", "https://jobs.lever.co/someorg")
        self.assertEqual(d, {"ats": "lever", "token": "someorg"})

    def test_workday_tenant_from_url(self):
        d = detect_ats("", "https://acme.wd12.myworkdayjobs.com/External")
        self.assertEqual(d["ats"], "workday")
        self.assertEqual(d["token"], "acme.wd12.myworkdayjobs.com")

    def test_embed_route_word_is_not_a_token(self):
        d = detect_ats(
            '<script src="https://boards.greenhouse.io/embed/job_widget.js"></script>',
            "https://acme.com/careers",
        )
        self.assertIsNotNone(d)
        self.assertIsNone(d["token"])


class ScrapeTests(unittest.TestCase):
    def test_scrapes_same_site_job_links_only(self):
        jobs = _scrape_jobs_html(PLAIN_PAGE, "https://acme.com/careers", "Acme")
        self.assertEqual([j["title"] for j in jobs], ["Senior Backend Engineer"])
        job = jobs[0]
        self.assertEqual(job["url"], "https://acme.com/careers/senior-backend-engineer")
        self.assertEqual(job["company"], "Acme")
        self.assertEqual(job["source"], "companysite")
        self.assertEqual(job["ats"], "html")
        self.assertEqual(job["application_method"], "web")

    def test_remote_flag_from_title(self):
        html = '<a href="/jobs/123">Product Manager - Remote</a>'
        jobs = _scrape_jobs_html(html, "https://acme.com/careers", None)
        self.assertEqual(len(jobs), 1)
        self.assertTrue(jobs[0]["worldwide_remote"])
        self.assertEqual(jobs[0]["work_mode"], "remote")

    def test_empty_html_is_safe(self):
        self.assertEqual(_scrape_jobs_html("", "https://acme.com/careers"), [])

class CompanySiteAdapterTests(unittest.TestCase):
    def test_delegates_to_detected_ats(self):
        adapter = CompanySiteAdapter(
            [{"name": "Acme", "careers_url": "https://acme.com/careers"}],
            fetcher=lambda url, client=None: GREENHOUSE_PAGE,
        )
        fake_board = {
            "jobs": [
                {
                    "id": 1,
                    "title": "Senior Engineer",
                    "absolute_url": "https://acme.com/job/1",
                    "location": {"name": "Remote"},
                    "updated_at": "2026-01-01",
                    "description": "<p>Build things</p>",
                    "metadata": [],
                    "employment_type": "full_time",
                }
            ]
        }
        with mock.patch("zeyrecuite.adapters.http_get_json", return_value=fake_board):
            jobs = adapter.fetch()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["source"], "companysite")
        self.assertEqual(jobs[0]["ats"], "greenhouse")  # proof of delegation
        self.assertEqual(jobs[0]["title"], "Senior Engineer")

    def test_falls_back_to_html_scrape(self):
        adapter = CompanySiteAdapter(
            [{"name": "Acme", "careers_url": "https://acme.com/careers"}],
            fetcher=lambda url, client=None: PLAIN_PAGE,
        )
        jobs = adapter.fetch()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["ats"], "html")
        self.assertEqual(jobs[0]["company"], "Acme")

    def test_fetch_error_skips_site_without_raising(self):
        def boom(url, client=None):
            raise RuntimeError("network down")

        adapter = CompanySiteAdapter(
            [{"careers_url": "https://x.test/careers"}], fetcher=boom
        )
        self.assertEqual(adapter.fetch(), [])

    def test_ats_failure_falls_back_to_scrape(self):
        adapter = CompanySiteAdapter(
            [{"name": "Acme", "careers_url": "https://acme.com/careers"}],
            fetcher=lambda url, client=None: GREENHOUSE_PAGE,
        )
        with mock.patch(
            "zeyrecuite.adapters.http_get_json", side_effect=RuntimeError("api down")
        ):
            jobs = adapter.fetch()
        # greenhouse board API failed → the page's own links are scraped instead
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["ats"], "html")

    def test_site_without_careers_url_ignored(self):
        adapter = CompanySiteAdapter([{"name": "No URL"}, None], fetcher=lambda u, client=None: "")
        self.assertEqual(adapter.sites, [])
        self.assertEqual(adapter.fetch(), [])


class ProbeTests(unittest.TestCase):
    def setUp(self):
        clear_probe_cache()

    def tearDown(self):
        clear_probe_cache()

    def test_probe_reports_ats_and_jobs(self):
        with mock.patch("zeyrecuite.adapters.http_get_json", return_value={"jobs": []}):
            info = probe_careers_page(
                "https://acme.com/careers",
                fetcher=lambda url, client=None: GREENHOUSE_PAGE,
            )
        self.assertEqual(info["ats"], "greenhouse")
        self.assertEqual(info["token"], "acme-corp")
        self.assertIsNone(info["error"])
        # board returned 0 jobs → the page's own links are scraped instead
        self.assertEqual(info["jobs"], 1)
        self.assertIn("Senior Engineer", info["sample"])

    def test_probe_returns_error_not_exception(self):
        def boom(url, client=None):
            raise RuntimeError("dns fail")

        info = probe_careers_page("https://down.test/careers", fetcher=boom)
        self.assertIsNotNone(info["error"])
        self.assertEqual(info["jobs"], 0)

    def test_probe_is_cached(self):
        calls: list[str] = []

        def counting(url, client=None):
            calls.append(url)
            return PLAIN_PAGE

        probe_careers_page("https://acme.com/careers", fetcher=counting)
        first = len(calls)
        self.assertGreater(first, 0)
        probe_careers_page("https://acme.com/careers", fetcher=counting)
        self.assertEqual(len(calls), first)  # cached: no second fetch

class PlanFillsTests(unittest.TestCase):
    @staticmethod
    def _fields(*specs):
        out = []
        for i, s in enumerate(specs):
            d = {"index": i, "label": "", "name": "", "placeholder": "", "id": "",
                 "aria": "", "type": "text", "value": ""}
            d.update(s)
            out.append(d)
        return out

    def test_maps_profile_onto_labels_names_placeholders(self):
        fields = self._fields(
            {"label": "Full name"},
            {"name": "email"},
            {"placeholder": "Phone"},
            {"label": "Years of experience"},  # not a profile field → untouched
        )
        profile = {"name": "Ada Lovelace", "email": "ada@example.com",
                   "phone": "+1 555 0100"}
        plan = dict(plan_fills(fields, profile=profile))
        self.assertEqual(
            plan, {0: "Ada Lovelace", 1: "ada@example.com", 2: "+1 555 0100"}
        )

    def test_cover_letter_goes_to_cover_letter_textarea_only(self):
        fields = self._fields(
            {"type": "textarea", "label": "Cover letter"},
            {"type": "textarea", "label": "Anything else?"},
        )
        plan = dict(plan_fills(fields, profile={}, cover_letter="Dear team,\nHello."))
        self.assertEqual(plan, {0: "Dear team,\nHello."})

    def test_saved_answer_matched_by_question_text(self):
        fields = self._fields({"label": "Why do you want to work here?"})
        plan = dict(plan_fills(
            fields, profile={},
            answers={"Why do you want to work here?": "I admire your product."},
        ))
        self.assertEqual(plan, {0: "I admire your product."})

    def test_already_filled_field_never_overwritten(self):
        fields = self._fields({"label": "Full name", "value": "Ada"})
        self.assertEqual(plan_fills(fields, profile={"name": "Someone Else"}), [])

    def test_unrecognized_field_left_alone(self):
        fields = self._fields({"label": "Resume", "type": "file"},
                              {"label": "How did you hear about us?"})
        self.assertEqual(plan_fills(fields, profile={"name": "X"}), [])


class SubmitTargetTests(unittest.TestCase):
    def test_submit_beats_sibling_apply_now(self):
        buttons = [{"text": "Apply Now", "disabled": False},
                   {"text": "Submit application", "disabled": False}]
        self.assertEqual(detect_submit_target(buttons), 1)

    def test_disabled_buttons_ignored(self):
        self.assertIsNone(detect_submit_target([{"text": "Submit", "disabled": True}]))

    def test_no_matching_buttons(self):
        self.assertIsNone(detect_submit_target([]))
        self.assertIsNone(detect_submit_target([{"text": "Cancel", "disabled": False}]))


class SuccessPageTests(unittest.TestCase):
    def test_url_wins(self):
        self.assertTrue(is_success_page("", "https://x.test/application/success"))

    def test_body_markers(self):
        self.assertTrue(is_success_page("Thank you! Your application was submitted."))
        self.assertTrue(is_success_page("We received your application — #42"))

    def test_plain_form_page_is_not_success(self):
        self.assertFalse(is_success_page(
            "Apply for this job — all fields required", "https://x.test/jobs/1"
        ))


class BrowserAvailabilityTests(unittest.TestCase):
    def test_browser_disabled_under_pytest(self):
        # Offline-safe by design: tests never launch Chromium (see module docstring).
        self.assertFalse(browser_available())

    def test_submit_degrades_honestly_without_browser(self):
        from zeyrecuite.apply import submit_on_company_site

        result = submit_on_company_site(
            "https://acme.com/apply", profile={"name": "Ada"}
        )
        self.assertFalse(result["ok"])
        self.assertFalse(result["submitted"])
        self.assertIn("browser automation unavailable", result["message"])

class _EndpointBase(unittest.TestCase):
    """Temp-DB FastAPI fixture: lifespan seeds the admin user; bearer headers."""

    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        tmp.close()
        self.tmp = tmp.name
        self.app = create_app(AppConfig(database_url=f"sqlite:///{self.tmp}"))
        self.client = TestClient(self.app)
        with self.client:  # triggers lifespan (seeds user + blank profile)
            r = self.client.post(
                "/api/auth/login",
                json={"username": "admin", "password": "zeyrecuite"},
            )
            self.h = {"Authorization": f"Bearer {r.json()['token']}"}

    def tearDown(self):
        self.client.close()
        self.app.state.db.engine.dispose()
        Path(self.tmp).unlink(missing_ok=True)

    def _seed_job(self, **kw):
        defaults = dict(
            fingerprint="fp-cs-1", title="Senior Engineer", company="Acme",
            location="Remote", work_mode="remote", source="companysite",
            url="https://acme.com/careers/senior-engineer",
            application_url="https://acme.com/apply/1",
            description="Build and ship product features with the team.",
            skills=["Python", "SQL"],
            location_status="eligible", status="approved",
            confidence=88.0, confidence_label="Excellent match",
            eligibility=100.0, eligibility_label="Fully eligible",
            ats="greenhouse",
        )
        defaults.update(kw)
        with self.app.state.db.session() as s:
            job = Job(**defaults)
            s.add(job)
            s.commit()
            return job.id

    def _application_for(self, job_id):
        with self.app.state.db.session() as s:
            return s.query(Application).filter(Application.job_id == job_id).first()


class ProbeEndpointTests(_EndpointBase):
    def test_requires_auth(self):
        r = self.client.post(
            "/api/company-sites/probe", json={"url": "https://acme.com/careers"}
        )
        self.assertEqual(r.status_code, 401)

    def test_rejects_url_without_scheme(self):
        r = self.client.post(
            "/api/company-sites/probe",
            json={"url": "acme.com/careers"},
            headers=self.h,
        )
        self.assertEqual(r.status_code, 422)

    def test_returns_probe_payload(self):
        fake = {"url": "https://acme.com/careers", "ats": "greenhouse",
                "token": "acme-corp", "jobs": 3,
                "sample": ["Senior Engineer"], "error": None}
        with mock.patch(
            "zeyrecuite.adapters.probe_careers_page", return_value=fake
        ) as probe:
            r = self.client.post(
                "/api/company-sites/probe",
                json={"url": "https://acme.com/careers"},
                headers=self.h,
            )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["ats"], "greenhouse")
        probe.assert_called_once_with("https://acme.com/careers")

class SubmissionFallbackTests(_EndpointBase):
    """Browser never runs under pytest → the honest fallback paths must hold."""

    def test_apply_link_records_honest_fallback(self):
        job_id = self._seed_job()
        with self.app.state.db.session() as s:
            job = s.get(Job, job_id)
        _submit_application(self.app.state.db, job, auto_submit=True)
        rec = self._application_for(job_id)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.status, "submitted")
        self.assertEqual(rec.submission_status, "submitted")
        self.assertIn("apply link", rec.submission_message)
        self.assertIsNone(rec.screenshot_path)  # no browser ran, no fake proof

    def test_no_apply_link_stays_ready(self):
        job_id = self._seed_job(application_url=None)
        with self.app.state.db.session() as s:
            job = s.get(Job, job_id)
        _submit_application(self.app.state.db, job, auto_submit=True)
        rec = self._application_for(job_id)
        self.assertEqual(rec.status, "ready")
        self.assertIn("upload", rec.submission_message)

    def test_auto_submit_off_never_touches_browser(self):
        job_id = self._seed_job()
        with self.app.state.db.session() as s:
            job = s.get(Job, job_id)
        _submit_application(self.app.state.db, job, auto_submit=False)
        rec = self._application_for(job_id)
        self.assertEqual(rec.status, "submitted")
        self.assertNotEqual(rec.submission_method, "auto-web")
        self.assertIsNone(rec.screenshot_path)


class ScreenshotEndpointTests(_EndpointBase):
    def test_404_when_application_has_no_screenshot(self):
        job_id = self._seed_job()
        r = self.client.get(f"/api/jobs/{job_id}/screenshot", headers=self.h)
        self.assertEqual(r.status_code, 404)

    def test_serves_png_when_present(self):
        job_id = self._seed_job()
        with self.app.state.db.session() as s:
            job = s.get(Job, job_id)
        _submit_application(self.app.state.db, job, auto_submit=True)
        png = Path(self.tmp + ".png")
        png.write_bytes(b"\x89PNG\r\n\x1a\n zey")
        with self.app.state.db.session() as s:
            rec = s.query(Application).filter(Application.job_id == job_id).first()
            rec.screenshot_path = str(png)
            s.commit()
        r = self.client.get(f"/api/jobs/{job_id}/screenshot", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.headers["content-type"].startswith("image/png"))
        self.assertEqual(r.content, png.read_bytes())

    def test_404_when_screenshot_file_missing(self):
        job_id = self._seed_job()
        with self.app.state.db.session() as s:
            job = s.get(Job, job_id)
        _submit_application(self.app.state.db, job, auto_submit=True)
        with self.app.state.db.session() as s:
            rec = s.query(Application).filter(Application.job_id == job_id).first()
            rec.screenshot_path = self.tmp + ".does-not-exist.png"
            s.commit()
        r = self.client.get(f"/api/jobs/{job_id}/screenshot", headers=self.h)
        self.assertEqual(r.status_code, 404)


if __name__ == "__main__":
    unittest.main()

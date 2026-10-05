"""Tests for the v2.4 feature set: new source adapters + registry (F15) and
scheduler + enrichment (F17).

All tests run fully offline: adapters receive a fake httpx client, enrichment
receives canned Wikidata payloads, and the scheduler test monkeypatches
``run_all`` so no real network is touched.
"""
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import httpx
from fastapi.testclient import TestClient

from zeyrecuite.adapters import (
    AdzunaAdapter,
    AshbyAdapter,
    GreenhouseAdapter,
    LeverAdapter,
    RemoteOKAdapter,
    RemotiveAdapter,
    SmartRecruitersAdapter,
    TheMuseAdapter,
    WWRAdapter,
    WorkableAdapter,
    WorkdayAdapter,
    build_adapters,
)
from zeyrecuite.app import create_app
from zeyrecuite.config import AppConfig
from zeyrecuite.enrich import (
    enrich_company,
    extract_main_content,
    get_json_with_retry,
    normalize_skill,
    normalize_skills,
    parse_wikidata_claims,
)
from zeyrecuite.models import Job
from zeyrecuite.scheduler import ScanScheduler


# ---------------------------------------------------------------------------
# Fake httpx clients
# ---------------------------------------------------------------------------


class FakeResponse:
    def __init__(self, payload=None, text=""):
        self._payload = payload
        self.text = text

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeClient:
    """Returns one canned payload for every GET (JSON or text)."""

    def __init__(self, payload=None, text=""):
        self.payload = payload
        self.text = text

    def get(self, url, **kwargs):
        return FakeResponse(self.payload, self.text)


class RoutedClient:
    """Returns a different payload depending on a substring in the URL."""

    def __init__(self, routes: dict[str, object]):
        self.routes = routes

    def get(self, url, **kwargs):
        for key, payload in self.routes.items():
            if key in url:
                return FakeResponse(payload)
        return FakeResponse({})


class FlakyClient:
    """Fails the first ``fail_times`` GETs with a transport error, then succeeds."""

    def __init__(self, fail_times: int, payload):
        self.fail_times = fail_times
        self.payload = payload
        self.calls = 0

    def get(self, url, **kwargs):
        self.calls += 1
        if self.calls <= self.fail_times:
            raise httpx.ConnectError("simulated network failure")
        return FakeResponse(self.payload)


def _make_app():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    cfg = AppConfig(database_url=f"sqlite:///{tmp.name}")
    app = create_app(cfg)
    return app, tmp.name


# ---------------------------------------------------------------------------
# F15 — adapter normalization (TC-15.1, TC-15.2, TC-15.3)
# ---------------------------------------------------------------------------


class LeverAdapterTests(unittest.TestCase):
    def test_normalize(self):
        payload = [
            {
                "text": "Senior Business Analyst",
                "company": "Stripe",
                "hostedUrl": "https://jobs.lever.co/stripe/1",
                "categories": {"location": "Remote"},
                "salary": "$120k - $150k",
                "description": "Work with stakeholders and SQL.",
                "createdAt": "2026-09-29",
            }
        ]
        jobs = LeverAdapter(["stripe"]).fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        j = jobs[0]
        self.assertEqual(j["title"], "Senior Business Analyst")
        self.assertEqual(j["company"], "Stripe")
        self.assertEqual(j["url"], "https://jobs.lever.co/stripe/1")
        self.assertEqual(j["source"], "lever")
        self.assertTrue(j["worldwide_remote"])
        self.assertEqual(j["salary"], "$120k - $150k")

    def test_skips_bad_records(self):
        payload = [
            {"text": "", "hostedUrl": ""},  # bad
            {"text": "BA", "hostedUrl": "https://jobs.lever.co/x/2"},
        ]
        jobs = LeverAdapter(["stripe"]).fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)

    def test_malformed_payload_returns_empty(self):
        # A non-list payload (e.g. an error object) yields no jobs, no crash.
        jobs = LeverAdapter(["stripe"]).fetch(client=FakeClient({"error": "not found"}))
        self.assertEqual(jobs, [])


class AshbyAdapterTests(unittest.TestCase):
    def test_normalize(self):
        payload = {
            "jobs": [
                {
                    "title": "Data Analyst",
                    "company": "Acme",
                    "jobUrl": "https://jobs.ashbyhq.com/acme/1",
                    "location": "Remote",
                    "salary": "$90k",
                    "description": "SQL and dashboards.",
                    "createdAt": "2026-09-29",
                }
            ]
        }
        jobs = AshbyAdapter(["acme"]).fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["source"], "ashby")
        self.assertEqual(jobs[0]["company"], "Acme")
        self.assertTrue(jobs[0]["worldwide_remote"])


class WorkableAdapterTests(unittest.TestCase):
    def test_normalize(self):
        payload = {
            "jobs": [
                {
                    "title": "Business Analyst",
                    "company": "Acme",
                    "url": "https://apply.workable.com/acme/j/1",
                    "location": "Remote",
                    "publishedAt": "2026-09-29",
                }
            ]
        }
        jobs = WorkableAdapter(["acme"]).fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["source"], "workable")


class SmartRecruitersAdapterTests(unittest.TestCase):
    def test_normalize(self):
        payload = {
            "items": [
                {
                    "title": "Business Analyst",
                    "company": "Acme",
                    "applyUrl": "https://smartrecruiters.com/acme/1",
                    "location": "Remote",
                    "publishedAt": "2026-09-29",
                }
            ]
        }
        jobs = SmartRecruitersAdapter(["acme"]).fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["source"], "smartrecruiters")


class WorkdayAdapterTests(unittest.TestCase):
    def test_normalize(self):
        payload = {
            "result": {
                "jobPostingInfo": [
                    {
                        "jobTitle": "Business Analyst",
                        "company": "Acme",
                        "jobPostingUrl": "https://workday.com/acme/1",
                        "location": "Remote",
                        "startDate": "2026-09-29",
                    }
                ]
            }
        }
        jobs = WorkdayAdapter(["acme"]).fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["source"], "workday")


class RemoteOKAdapterTests(unittest.TestCase):
    def test_normalize(self):
        payload = [
            {
                "position": "Senior Business Analyst",
                "company": "Stripe",
                "url": "https://remoteok.com/1",
                "location": "Remote",
                "salary": "$100k",
                "tags": ["SQL", "Excel"],
                "date": "2026-09-29",
            }
        ]
        jobs = RemoteOKAdapter().fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        j = jobs[0]
        self.assertEqual(j["source"], "remoteok")
        self.assertEqual(j["work_mode"], "remote")
        self.assertIn("SQL", j["skills"])

    def test_malformed_payload_returns_empty(self):
        jobs = RemoteOKAdapter().fetch(client=FakeClient({"error": "bad"}))
        self.assertEqual(jobs, [])


class WWRAdapterTests(unittest.TestCase):
    RSS = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<rss version='2.0'><channel>"
        "<item><title>Senior Business Analyst</title>"
        "<link>https://weworkremotely.com/1</link>"
        "<description>Acme is hiring a BA to build SQL reports and dashboards.</description>"
        "<pubDate>Mon, 29 Sep 2026 00:00:00 GMT</pubDate></item>"
        "<item><title></title><link></link></item>"
        "</channel></rss>"
    )

    def test_normalize(self):
        jobs = WWRAdapter().fetch(client=FakeClient(text=self.RSS))
        self.assertEqual(len(jobs), 1)  # the empty item is skipped
        j = jobs[0]
        self.assertEqual(j["title"], "Senior Business Analyst")
        self.assertEqual(j["source"], "weworkremotely")
        self.assertTrue(j["worldwide_remote"])
        self.assertIn("SQL", j["description"])

    def test_malformed_feed_returns_empty(self):
        jobs = WWRAdapter().fetch(client=FakeClient(text="this is not xml <<<"))
        self.assertEqual(jobs, [])


class TheMuseAdapterTests(unittest.TestCase):
    def test_normalize(self):
        payload = {
            "jobs": [
                {
                    "title": "Business Analyst",
                    "company": "Acme",
                    "url": "https://www.themuse.com/job/1",
                    "location": "Remote",
                    "published_at": "2026-09-29",
                }
            ]
        }
        jobs = TheMuseAdapter("business analyst").fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["source"], "themuse")


class AdzunaAdapterTests(unittest.TestCase):
    def test_requires_key(self):
        # No key -> no fetch, no crash.
        jobs = AdzunaAdapter().fetch(client=FakeClient({"results": []}))
        self.assertEqual(jobs, [])

    def test_normalize(self):
        payload = {
            "results": [
                {
                    "title": "Business Analyst",
                    "company": {"display_name": "Acme"},
                    "redirect_url": "https://adzuna.com/1",
                    "location": {"area": "Remote", "display_name": "Remote"},
                    "salary": "50000-70000",
                    "skills": ["SQL"],
                    "created_at": "2026-09-29",
                }
            ]
        }
        jobs = AdzunaAdapter("key", "id").fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["source"], "adzuna")
        self.assertEqual(jobs[0]["company"], "Acme")


# ---------------------------------------------------------------------------
# F15 — registry / build_adapters (TC-15.6)
# ---------------------------------------------------------------------------


class BuildAdaptersTests(unittest.TestCase):
    def _cfg(self):
        return AppConfig(
            database_url="sqlite:///:memory:",
            sources=__import__("zeyrecuite.config", fromlist=["SourceConfig"]).SourceConfig(
                remotive_enabled=False, greenhouse_enabled=False
            ),
        )

    def test_disabled_source_not_instantiated(self):
        registry = {"remoteok": {"enabled": False}, "lever": {"enabled": True, "companies": ["acme"]}}
        with mock.patch("zeyrecuite.registry.load_registry", return_value=registry):
            adapters = build_adapters(self._cfg())
        names = [a.name for a in adapters]
        self.assertIn("lever", names)
        self.assertNotIn("remoteok", names)

    def test_enabled_source_instantiated(self):
        registry = {"remoteok": {"enabled": True}, "weworkremotely": {"enabled": True}}
        with mock.patch("zeyrecuite.registry.load_registry", return_value=registry):
            adapters = build_adapters(self._cfg())
        names = [a.name for a in adapters]
        self.assertIn("remoteok", names)
        self.assertIn("weworkremotely", names)

    def test_company_source_needs_slug(self):
        # Enabled but no companies -> not instantiated.
        registry = {"lever": {"enabled": True, "companies": []}}
        with mock.patch("zeyrecuite.registry.load_registry", return_value=registry):
            adapters = build_adapters(self._cfg())
        self.assertNotIn("lever", [a.name for a in adapters])


# ---------------------------------------------------------------------------
# F17 — enrichment (TC-17.2, TC-17.3, TC-17.4, TC-17.5)
# ---------------------------------------------------------------------------


class WikidataEnrichTests(unittest.TestCase):
    # Real Wikidata claims carry only an "id" (Q-id), not a "text" label.
    CLAIMS = {
        "P159": [{"mainsnak": {"datavalue": {"value": {"id": "Q1214"}}}}],
        "P571": [{"mainsnak": {"datavalue": {"value": {"time": "+2010-06-01T00:00:00Z"}}}}],
        "P112": [{"mainsnak": {"datavalue": {"value": 5000}}}],
        "P452": [{"mainsnak": {"datavalue": {"value": {"id": "Q1234"}}}}],
    }

    def test_parse_claims(self):
        facts = parse_wikidata_claims(self.CLAIMS)
        # Without labels, hq/industry are the raw Q-ids.
        self.assertEqual(facts["hq"], "Q1214")
        self.assertEqual(facts["founded"], 2010)
        self.assertEqual(facts["employees"], 5000)
        self.assertEqual(facts["industry"], "Q1234")

    def test_parse_empty_claims(self):
        facts = parse_wikidata_claims({})
        self.assertEqual(facts, {"hq": None, "founded": None, "employees": None, "industry": None})

    def test_enrich_company_resolves_labels(self):
        client = RoutedClient(
            {
                "wbsearchentities": {"search": [{"id": "Q123"}]},
                "props=claims": {"entities": {"Q123": {"claims": self.CLAIMS}}},
                "props=labels": {
                    "entities": {
                        "Q1214": {"labels": {"en": {"value": "San Francisco"}}},
                        "Q1234": {"labels": {"en": {"value": "Fintech"}}},
                    }
                },
            }
        )
        facts = enrich_company("Stripe", client=client)
        self.assertEqual(facts["hq"], "San Francisco")
        self.assertEqual(facts["founded"], 2010)
        self.assertEqual(facts["employees"], 5000)
        self.assertEqual(facts["industry"], "Fintech")

    def test_enrich_company_no_match_returns_empty(self):
        client = RoutedClient({"wbsearchentities": {"search": []}})
        self.assertEqual(enrich_company("Unknown Co", client=client), {})

    def test_enrich_company_network_error_returns_empty(self):
        class BoomClient:
            def get(self, url, **kwargs):
                raise httpx.ConnectError("down")

        self.assertEqual(enrich_company("Stripe", client=BoomClient()), {})


class SkillNormalizationTests(unittest.TestCase):
    def test_powerbi_alias(self):
        self.assertEqual(normalize_skill("PowerBI"), "Power BI")
        self.assertEqual(normalize_skill("power bi"), "Power BI")
        self.assertEqual(normalize_skill("Power-BI"), "Power BI")

    def test_unknown_skill_unchanged(self):
        self.assertEqual(normalize_skill("  Quantum Flux  "), "Quantum Flux")

    def test_normalize_list_dedupes(self):
        out = normalize_skills(["PowerBI", "power bi", "SQL", "sql"])
        self.assertEqual(out, ["Power BI", "SQL"])


class RetryTests(unittest.TestCase):
    def test_retries_then_succeeds(self):
        client = FlakyClient(fail_times=2, payload={"ok": True})
        result = get_json_with_retry("https://example.com/x", client=client, attempts=3)
        self.assertEqual(result, {"ok": True})
        self.assertEqual(client.calls, 3)

    def test_exhausts_attempts_and_raises(self):
        client = FlakyClient(fail_times=10, payload={"ok": True})
        with self.assertRaises(httpx.HTTPError):
            get_json_with_retry("https://example.com/x", client=client, attempts=2)


class TrafilaturaTests(unittest.TestCase):
    PAGE = """
    <html><head><title>Job</title></head><body>
    <nav><a href="/">Home</a> <a href="/about">About</a> <a href="/careers">Careers</a></nav>
    <article>
      <h1>Senior Business Analyst</h1>
      <p>We are looking for a Senior Business Analyst to join our data team. You will
      work closely with stakeholders, write clear requirements, and build SQL reports
      and dashboards that drive product and business decisions across the company.</p>
      <p>The role requires strong analytical skills, experience with Excel and Power BI,
      and the ability to translate ambiguous problems into concrete, measurable plans
      that engineering and product teams can execute against with confidence.</p>
      <p>You will partner with leadership to define key performance indicators, present
      findings to senior stakeholders, and own the end-to-end process from discovery
      through delivery of actionable, well-documented insights.</p>
    </article>
    <footer>&copy; 2026 Acme Corp. Privacy Policy. Terms of Service. Contact us.</footer>
    </body></html>
    """

    def test_extracts_main_content(self):
        text = extract_main_content(self.PAGE)
        self.assertIn("Senior Business Analyst", text)
        self.assertIn("stakeholders", text)

    def test_excludes_footer(self):
        text = extract_main_content(self.PAGE)
        self.assertNotIn("Privacy Policy", text)

    def test_empty_input(self):
        self.assertEqual(extract_main_content(""), "")


# ---------------------------------------------------------------------------
# F17 — scheduler (TC-17.1)
# ---------------------------------------------------------------------------


class SchedulerTests(unittest.TestCase):
    def test_scan_runs_automatically(self):
        app, db_path = _make_app()
        calls = []

        def fake_run_all(db, config, **kw):
            calls.append(1)
            return []

        with app.state.db.session() as s:
            s.add(Job(fingerprint="fp1", title="BA", company="Acme", url="https://x/1"))
            s.commit()

        scheduler = ScanScheduler(app.state.db, app.state.config)
        try:
            with mock.patch("zeyrecuite.scheduler.run_all", side_effect=fake_run_all):
                scheduler.start(interval_hours=0.001)  # ~3.6s, but we wait only briefly
                self.assertTrue(scheduler.running)
                deadline = time.time() + 5
                while not calls and time.time() < deadline:
                    time.sleep(0.05)
            self.assertTrue(calls, "scheduled scan did not fire")
        finally:
            scheduler.stop()
            app.state.db.engine.dispose()
            Path(db_path).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# F17 — API endpoints (offline-safe)
# ---------------------------------------------------------------------------


class F17ApiTests(unittest.TestCase):
    def setUp(self):
        self.app, self.db_path = _make_app()
        self.client = TestClient(self.app)
        with self.client:
            r = self.client.post("/api/auth/login", json={"username": "admin", "password": "zeyrecuite"})
            self.token = r.json()["token"]
            self.h = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        self.app.state.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_scheduler_status(self):
        r = self.client.get("/api/scheduler", headers=self.h)
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertIn("enabled", body)
        self.assertIn("running", body)
        self.assertIn("interval_hours", body)

    def test_sources_registry(self):
        r = self.client.get("/api/sources", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertIn("sources", r.json())

    def test_enrich_normalizes_skills(self):
        with self.app.state.db.session() as s:
            s.add(Job(
                fingerprint="fp1", title="BA", company="Acme", url="https://x/1",
                skills=["PowerBI", "power bi", "SQL"],
            ))
            s.commit()
        # Patch enrich_company so no network is hit for the company facts.
        with mock.patch("zeyrecuite.app.enrich_company", return_value={}):
            r = self.client.post("/api/enrich", headers=self.h)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["enriched"], 1)
        with self.app.state.db.session() as s:
            job = s.get(Job, 1)
            self.assertEqual(job.skills, ["Power BI", "SQL"])

    def test_endpoints_require_auth(self):
        for path in ("/api/scheduler", "/api/sources"):
            r = self.client.get(path)
            self.assertEqual(r.status_code, 401)
        r = self.client.post("/api/enrich")
        self.assertEqual(r.status_code, 401)


if __name__ == "__main__":
    unittest.main()

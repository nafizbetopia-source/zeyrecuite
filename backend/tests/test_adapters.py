import unittest

from zeyrecuite.adapters import (
    GreenhouseAdapter,
    RemotiveAdapter,
    is_worldwide,
    normalize_country,
)


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeClient:
    """Returns a canned payload for any GET, so adapters run offline."""

    def __init__(self, payload):
        self.payload = payload

    def get(self, url, **kwargs):
        return FakeResponse(self.payload)


class CountryTests(unittest.TestCase):
    def test_normalize_names(self):
        self.assertEqual(normalize_country("India"), "IN")
        self.assertEqual(normalize_country("Dhaka, Bangladesh"), "BD")
        self.assertEqual(normalize_country("United States"), "US")
        self.assertIsNone(normalize_country("Nowhere"))

    def test_worldwide_detection(self):
        self.assertTrue(is_worldwide("Worldwide"))
        self.assertTrue(is_worldwide("Remote - Anywhere"))
        self.assertFalse(is_worldwide("New York, US"))


class RemotiveAdapterTests(unittest.TestCase):
    def test_normalize_worldwide_remote(self):
        payload = {
            "jobs": [
                {
                    "title": "Business Analyst",
                    "company_name": "Acme",
                    "url": "https://remotive.com/1",
                    "job_location": "Remote",
                    "candidate_required_location": "Worldwide",
                    "salary_min": 50000,
                    "salary_max": 70000,
                    "publication_date": "2026-09-29",
                }
            ]
        }
        jobs = RemotiveAdapter().fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        job = jobs[0]
        self.assertTrue(job["worldwide_remote"])
        self.assertIsNone(job["candidate_required_location"])
        self.assertEqual(job["source"], "remotive")

    def test_skips_bad_records(self):
        payload = {"jobs": [{"title": "", "url": ""}, {"title": "BA", "url": "https://x/1"}]}
        jobs = RemotiveAdapter().fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)

    def test_no_candidate_restriction_treated_as_worldwide(self):
        payload = {
            "jobs": [
                {
                    "title": "Business Analyst",
                    "company_name": "Acme",
                    "url": "https://remotive.com/2",
                    "job_location": "Remote",
                    "candidate_required_location": None,
                }
            ]
        }
        jobs = RemotiveAdapter().fetch(client=FakeClient(payload))
        self.assertTrue(jobs[0]["worldwide_remote"])
        self.assertIsNone(jobs[0]["candidate_required_location"])


class GreenhouseAdapterTests(unittest.TestCase):
    def test_normalize_onsite_south_asia(self):
        payload = {
            "jobs": [
                {
                    "title": "Business Analyst",
                    "company_name": "Acme",
                    "absolute_url": "https://greenhouse/1",
                    "apply_url": "https://greenhouse/1/apply",
                    "location": {"name": "Dhaka, Bangladesh"},
                    "updated_at": "2026-09-29",
                    "content": "<p>Requirements and SQL.</p>",
                }
            ]
        }
        jobs = GreenhouseAdapter(["acme"]).fetch(client=FakeClient(payload))
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["job_country"], "BD")
        self.assertEqual(jobs[0]["work_mode"], "onsite")
        self.assertIn("Requirements", jobs[0]["description"])

    def test_remote_no_country_treated_as_worldwide(self):
        payload = {
            "jobs": [
                {
                    "title": "Business Analyst",
                    "company_name": "Acme",
                    "absolute_url": "https://greenhouse/2",
                    "location": {"name": "Remote"},
                    "content": "<p>Remote role.</p>",
                }
            ]
        }
        jobs = GreenhouseAdapter(["acme"]).fetch(client=FakeClient(payload))
        self.assertEqual(jobs[0]["work_mode"], "remote")
        self.assertTrue(jobs[0]["worldwide_remote"])

    def test_escaped_html_description_is_cleaned(self):
        payload = {
            "jobs": [
                {
                    "title": "Business Analyst",
                    "company_name": "Acme",
                    "absolute_url": "https://greenhouse/3",
                    "location": {"name": "Remote"},
                    "content": "&lt;h2&gt;Who we are&lt;/h2&gt;&lt;p&gt;We use SQL.&lt;/p&gt;",
                }
            ]
        }
        jobs = GreenhouseAdapter(["acme"]).fetch(client=FakeClient(payload))
        self.assertNotIn("<", jobs[0]["description"])
        self.assertIn("Who we are", jobs[0]["description"])
        self.assertIn("SQL", jobs[0]["description"])


if __name__ == "__main__":
    unittest.main()

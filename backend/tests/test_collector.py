import tempfile
import unittest
from pathlib import Path

from zeyrecuite.adapters import BaseAdapter
from zeyrecuite.collector import run_source
from zeyrecuite.config import AppConfig
from zeyrecuite.database import Database
from zeyrecuite.models import Job, Profile


class FakeAdapter(BaseAdapter):
    name = "fake"

    def __init__(self, jobs):
        self.jobs = jobs

    def fetch(self, *, client=None):
        return self.jobs


def make_db():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db = Database(f"sqlite:///{tmp.name}")
    db.create_all()
    return db, tmp.name


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.db, self.db_path = make_db()
        self.config = AppConfig()
        with self.db.session() as s:
            s.add(Profile(id=1, current_country="Bangladesh", skills=["SQL", "Excel"]))
            s.commit()

    def tearDown(self):
        self.db.engine.dispose()
        Path(self.db_path).unlink(missing_ok=True)

    def test_south_asia_origin_rejected_worldwide_eligible(self):
        jobs = [
            {  # India-based remote -> rejected
                "title": "BA India", "company": "Acme", "url": "https://x/1",
                "work_mode": "remote", "employer_country": "IN", "job_country": "IN",
                "worldwide_remote": True, "candidate_required_location": None,
                "description": "sql excel", "skills": ["SQL"], "source": "fake",
            },
            {  # US-based worldwide remote -> eligible
                "title": "BA US", "company": "Globex", "url": "https://x/2",
                "work_mode": "remote", "employer_country": "US", "job_country": None,
                "worldwide_remote": True, "candidate_required_location": None,
                "description": "sql excel reporting", "skills": ["SQL", "Excel"], "source": "fake",
            },
        ]
        summary = run_source(self.db, self.config, FakeAdapter(jobs))
        self.assertEqual(summary.rejected, 1)
        self.assertEqual(summary.eligible, 1)
        with self.db.session() as s:
            stored = s.query(Job).all()
            self.assertEqual(len(stored), 1)
            self.assertEqual(stored[0].company, "Globex")
            self.assertEqual(stored[0].status, "new")

    def test_dedup_across_runs(self):
        jobs = [
            {"title": "BA US", "company": "Globex", "url": "https://x/2",
             "work_mode": "remote", "employer_country": "US", "job_country": None,
             "worldwide_remote": True, "candidate_required_location": None,
             "description": "sql", "skills": ["SQL"], "source": "fake"},
        ]
        run_source(self.db, self.config, FakeAdapter(jobs))
        summary2 = run_source(self.db, self.config, FakeAdapter(jobs))
        self.assertEqual(summary2.duplicates, 1)
        self.assertEqual(summary2.eligible, 0)
        with self.db.session() as s:
            self.assertEqual(s.query(Job).count(), 1)

    def test_explicit_restriction_rejects_user_country(self):
        jobs = [
            {"title": "BA US-only", "company": "Globex", "url": "https://x/3",
             "work_mode": "remote", "employer_country": "US", "job_country": None,
             "worldwide_remote": False, "candidate_required_location": ["US"],
             "description": "sql", "skills": ["SQL"], "source": "fake"},
        ]
        summary = run_source(self.db, self.config, FakeAdapter(jobs))
        self.assertEqual(summary.rejected, 1)
        self.assertEqual(summary.eligible, 0)


if __name__ == "__main__":
    unittest.main()

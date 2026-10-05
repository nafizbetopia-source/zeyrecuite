import unittest

from zeyrecuite.scoring import score_job


class ScoringTests(unittest.TestCase):
    def test_strong_ba_match_scores_high(self):
        result = score_job(
            title="Senior Business Analyst",
            description="Work with stakeholders, write requirements, build SQL reports and dashboards.",
            job_skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
            profile_skills=["SQL", "Excel", "Power BI", "Stakeholder Management"],
        )
        self.assertGreater(result.score, 60)
        self.assertIn("matched_skills", result.breakdown)

    def test_unrelated_role_scores_low(self):
        result = score_job(
            title="Barista",
            description="Make coffee and serve customers.",
            job_skills=["Espresso"],
            profile_skills=["SQL", "Excel"],
        )
        self.assertLess(result.score, 40)

    def test_score_bounded_0_to_100(self):
        result = score_job(
            title="Business Analyst",
            description="sql excel reporting stakeholder requirements",
            job_skills=["SQL", "Excel", "Reporting"],
            profile_skills=["SQL", "Excel", "Reporting"],
        )
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)


if __name__ == "__main__":
    unittest.main()

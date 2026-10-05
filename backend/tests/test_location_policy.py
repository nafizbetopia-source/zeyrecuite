import unittest

from zeyrecuite.location_policy import DecisionStatus, evaluate_location


class LocationPolicyTests(unittest.TestCase):
    def test_south_asian_employer_is_rejected_for_remote_job(self):
        decision = evaluate_location(
            employer_country="India",
            job_country=None,
            work_mode="remote",
            current_country="Bangladesh",
            worldwide_remote=True,
        )

        self.assertEqual(decision.status, DecisionStatus.REJECTED)
        self.assertEqual(decision.reason, "south_asia_employer_origin")

    def test_south_asian_actual_job_location_is_rejected(self):
        decision = evaluate_location(
            employer_country="US",
            job_country="Bangladesh",
            work_mode="remote",
            current_country="Bangladesh",
            worldwide_remote=True,
        )

        self.assertEqual(decision.status, DecisionStatus.REJECTED)
        self.assertEqual(decision.reason, "south_asia_job_location")

    def test_worldwide_remote_from_non_south_asian_origin_accepts_user_in_bangladesh(self):
        decision = evaluate_location(
            employer_country="US",
            job_country=None,
            work_mode="remote",
            current_country="Bangladesh",
            worldwide_remote=True,
        )

        self.assertEqual(decision.status, DecisionStatus.ELIGIBLE)
        self.assertEqual(decision.reason, "worldwide_remote_origin_allowed")

    def test_remote_role_restricted_to_us_rejects_user_in_bangladesh(self):
        decision = evaluate_location(
            employer_country="US",
            job_country=None,
            work_mode="remote",
            current_country="BD",
            allowed_applicant_countries={"US"},
        )

        self.assertEqual(decision.status, DecisionStatus.REJECTED)
        self.assertEqual(decision.reason, "current_country_not_allowed")

    def test_explicit_country_restriction_overrides_worldwide_flag(self):
        decision = evaluate_location(
            employer_country="US",
            job_country=None,
            work_mode="remote",
            current_country="BD",
            worldwide_remote=True,
            allowed_applicant_countries={"US"},
        )

        self.assertEqual(decision.status, DecisionStatus.REJECTED)
        self.assertEqual(decision.reason, "current_country_not_allowed")

    def test_remote_role_with_explicit_bangladesh_eligibility_passes(self):
        decision = evaluate_location(
            employer_country="US",
            job_country=None,
            work_mode="remote",
            current_country="BD",
            allowed_applicant_countries={"US", "Bangladesh"},
        )

        self.assertEqual(decision.status, DecisionStatus.ELIGIBLE)

    def test_unknown_employer_origin_remote_worldwide_is_eligible(self):
        # Unknown employer origin is NOT a rejection; a worldwide remote role
        # with no South-Asian signal passes the gate.
        decision = evaluate_location(
            employer_country=None,
            job_country=None,
            work_mode="remote",
            current_country="BD",
            worldwide_remote=True,
        )

        self.assertEqual(decision.status, DecisionStatus.ELIGIBLE)
        self.assertEqual(decision.reason, "worldwide_remote_origin_allowed")

    def test_unknown_employer_origin_remote_unknown_eligibility_is_review(self):
        decision = evaluate_location(
            employer_country=None,
            job_country=None,
            work_mode="remote",
            current_country="BD",
        )

        self.assertEqual(decision.status, DecisionStatus.REVIEW)
        self.assertEqual(decision.reason, "applicant_eligibility_unknown")

    def test_unknown_applicant_eligibility_is_held_for_review(self):
        decision = evaluate_location(
            employer_country="US",
            job_country=None,
            work_mode="remote",
            current_country="BD",
        )

        self.assertEqual(decision.status, DecisionStatus.REVIEW)
        self.assertEqual(decision.reason, "applicant_eligibility_unknown")

    def test_local_role_in_bangladesh_remains_excluded(self):
        decision = evaluate_location(
            employer_country="BD",
            job_country="BD",
            work_mode="onsite",
            current_country="BD",
        )

        self.assertEqual(decision.status, DecisionStatus.REJECTED)
        self.assertEqual(decision.reason, "south_asia_employer_origin")

    def test_local_role_outside_current_country_is_rejected(self):
        decision = evaluate_location(
            employer_country="US",
            job_country="CA",
            work_mode="onsite",
            current_country="US",
        )

        self.assertEqual(decision.status, DecisionStatus.REJECTED)
        self.assertEqual(decision.reason, "local_role_outside_current_country")


if __name__ == "__main__":
    unittest.main()
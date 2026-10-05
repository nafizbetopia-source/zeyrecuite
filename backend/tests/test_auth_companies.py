"""Tests for auth, company ratings, interview questions, and confidence."""
import unittest

from zeyrecuite import auth, companies, questions
from zeyrecuite.scoring import confidence


class TestAuth(unittest.TestCase):
    def test_hash_and_verify(self):
        h, s = auth.hash_password("secret123")
        self.assertTrue(auth.verify_password("secret123", h, s))
        self.assertFalse(auth.verify_password("wrong", h, s))

    def test_unique_salts(self):
        h1, s1 = auth.hash_password("same")
        h2, s2 = auth.hash_password("same")
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(h1, h2)


class TestCompanies(unittest.TestCase):
    def test_known_company(self):
        info = companies.get_company_info("Stripe")
        self.assertTrue(info.has_data)
        self.assertIsNotNone(info.overall)
        self.assertIn("work_life_balance", info.ratings)
        self.assertTrue(info.flags)

    def test_unknown_company_no_data(self):
        info = companies.get_company_info("Totally Unknown Co")
        self.assertFalse(info.has_data)
        self.assertIsNone(info.overall)

    def test_normalization(self):
        self.assertTrue(companies.get_company_info("stripe, inc.").has_data)
        self.assertTrue(companies.get_company_info("  DATADOG ").has_data)

    def test_rating_label(self):
        self.assertEqual(companies.rating_label(4.6), "Excellent")
        self.assertEqual(companies.rating_label(3.2), "Fair")
        self.assertEqual(companies.rating_label(None), "N/A")


class TestQuestions(unittest.TestCase):
    def test_returns_questions(self):
        qs = questions.generate_questions("Senior Business Analyst", "We need SQL and stakeholder management.", ["SQL", "Stakeholder Management"])
        self.assertGreater(len(qs), 3)
        self.assertTrue(any("SQL" in q for q in qs))

    def test_dedup(self):
        qs = questions.generate_questions("Business Analyst", "SQL SQL SQL", ["SQL"])
        self.assertEqual(len(qs), len(set(qs)))


class TestConfidence(unittest.TestCase):
    def test_with_company(self):
        value, label = confidence(80, 4.5)
        self.assertGreater(value, 80)  # company boosts
        self.assertIn(label, ("Strong match", "Excellent match"))

    def test_without_company(self):
        value, label = confidence(40, None)
        self.assertEqual(value, 40)
        self.assertIn("match", label)

    def test_clamped(self):
        value, _ = confidence(120, 5.0)
        self.assertLessEqual(value, 100)


if __name__ == "__main__":
    unittest.main()

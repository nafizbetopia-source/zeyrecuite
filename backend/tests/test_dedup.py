import unittest

from zeyrecuite.dedup import fingerprint


class DedupTests(unittest.TestCase):
    def test_same_title_company_same_fingerprint(self):
        a = fingerprint("Business Analyst", "Acme")
        b = fingerprint("business  analyst", "acme")
        self.assertEqual(a, b)

    def test_different_company_different_fingerprint(self):
        a = fingerprint("Business Analyst", "Acme")
        b = fingerprint("Business Analyst", "Globex")
        self.assertNotEqual(a, b)

    def test_url_fallback_when_title_missing(self):
        a = fingerprint("", "", "https://x.com/1")
        b = fingerprint("", "", "https://x.com/1")
        self.assertEqual(a, b)
        c = fingerprint("", "", "https://x.com/2")
        self.assertNotEqual(a, c)


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path

from zeyrecuite.resume import ResumeData, render_pdf, tailor_resume


class ResumeTests(unittest.TestCase):
    def _resume(self):
        return ResumeData(
            name="Nafiz",
            email="nafiz@example.com",
            phone="+8801700000000",
            summary="Business Analyst.",
            skills=["Excel", "SQL", "Power BI"],
            experiences=[{"role": "BA", "company": "Acme", "period": "2022-Present", "bullets": ["Did things with SQL."]}],
            education=[{"degree": "B.Sc.", "school": "Uni", "period": "2018-2022"}],
        )

    def test_tailor_ranks_relevant_skills_first(self):
        tailored = tailor_resume(self._resume(), "Business Analyst", "We need SQL and reporting.")
        self.assertEqual(tailored.skills[0], "SQL")

    def test_render_pdf_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "resume.pdf"
            render_pdf(self._resume(), "Business Analyst", out)
            self.assertTrue(out.exists())
            self.assertGreater(out.stat().st_size, 500)
            # PDF magic bytes
            self.assertEqual(out.read_bytes()[:4], b"%PDF")


if __name__ == "__main__":
    unittest.main()

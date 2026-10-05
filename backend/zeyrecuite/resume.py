"""Resume tailoring and PDF rendering.

Tailoring is deterministic and truth-preserving: it reorders and emphasizes the
user's *existing* resume content to match the target job. It never invents
skills, employers, or facts. The result is rendered to a clean PDF with
ReportLab.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


@dataclass
class ResumeData:
    name: str = ""
    email: str = ""
    phone: str = ""
    summary: str = ""
    skills: list[str] = field(default_factory=list)
    experiences: list[dict] = field(default_factory=list)  # {role, company, period, bullets}
    education: list[dict] = field(default_factory=list)  # {degree, school, period}


def extract_pdf_text(path: str | Path) -> str:
    """Extract text from a PDF resume using pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def _rank_skills(skills: list[str], job_text: str) -> list[str]:
    """Put job-relevant skills first, preserving the rest in original order."""
    low = job_text.lower()
    relevant = [s for s in skills if s.lower() in low]
    rest = [s for s in skills if s.lower() not in low]
    return relevant + rest


def tailor_resume(resume: ResumeData, job_title: str, job_description: str | None) -> ResumeData:
    """Return a tailored copy of the resume for the given job (no new facts)."""
    job_text = f"{job_title} {job_description or ''}"
    tailored = ResumeData(
        name=resume.name,
        email=resume.email,
        phone=resume.phone,
        summary=resume.summary,
        skills=_rank_skills(resume.skills, job_text),
        experiences=resume.experiences,
        education=resume.education,
    )
    return tailored


def render_pdf(resume: ResumeData, job_title: str, output_path: str | Path) -> Path:
    """Render the tailored resume to a PDF file and return its path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    name_style = ParagraphStyle("Name", parent=styles["Title"], fontSize=20, spaceAfter=2)
    contact_style = ParagraphStyle("Contact", parent=styles["Normal"], fontSize=9, textColor=colors.HexColor("#444444"))
    section_style = ParagraphStyle("Section", parent=styles["Heading2"], fontSize=12, spaceBefore=8, spaceAfter=3, textColor=colors.HexColor("#1a1a1a"))
    body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.5, leading=13)
    bullet_style = ParagraphStyle("Bullet", parent=body_style, leftIndent=10, bulletIndent=2)

    doc = SimpleDocTemplate(str(output_path), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm, bottomMargin=14 * mm)
    story: list = []

    story.append(Paragraph(_esc(resume.name or "Resume"), name_style))
    contact_bits = [b for b in [resume.email, resume.phone] if b]
    if contact_bits:
        story.append(Paragraph("  |  ".join(_esc(b) for b in contact_bits), contact_style))
    if job_title:
        story.append(Paragraph(f"Tailored for: {_esc(job_title)}", contact_style))
    story.append(Spacer(1, 4))

    if resume.summary:
        story.append(Paragraph("Summary", section_style))
        story.append(Paragraph(_esc(resume.summary), body_style))

    if resume.skills:
        story.append(Paragraph("Skills", section_style))
        story.append(Paragraph(", ".join(_esc(s) for s in resume.skills), body_style))

    if resume.experiences:
        story.append(Paragraph("Experience", section_style))
        for exp in resume.experiences:
            header = "  |  ".join(_esc(x) for x in [exp.get("role"), exp.get("company"), exp.get("period")] if x)
            story.append(Paragraph(header, body_style))
            for bullet in exp.get("bullets", []):
                story.append(Paragraph(_esc(bullet), bullet_style, bulletText="•"))
            story.append(Spacer(1, 3))

    if resume.education:
        story.append(Paragraph("Education", section_style))
        for edu in resume.education:
            header = "  |  ".join(_esc(x) for x in [edu.get("degree"), edu.get("school"), edu.get("period")] if x)
            story.append(Paragraph(header, body_style))

    doc.build(story)
    return output_path


def _esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

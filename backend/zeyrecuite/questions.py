"""Interview question generation.

Deterministic and role-aware: it blends a core Business Analyst question bank
with job-specific questions derived from the posting's skills and title. This
gives the user a realistic prep list for each job without any LLM cost.
"""
from __future__ import annotations

import re

_CORE_QUESTIONS = [
    "Walk me through how you gather and document business requirements for a project.",
    "How do you prioritize requirements when stakeholders have conflicting needs?",
    "Describe a time you turned raw data into an insight that changed a decision.",
    "How do you keep stakeholders aligned and informed throughout a project?",
    "Tell me about a process you improved. What was the measurable impact?",
    "How do you validate that a solution actually meets the business need?",
    "Describe how you handle ambiguity or incomplete information in a requirement.",
    "How do you write effective user stories and acceptance criteria?",
]

_SKILL_QUESTIONS = {
    "sql": "Walk me through a complex SQL query you wrote. How did you optimize it?",
    "excel": "Describe the most advanced Excel model or dashboard you've built.",
    "power bi": "How have you used Power BI to communicate insights to non-technical stakeholders?",
    "tableau": "Tell me about a Tableau dashboard you designed and the decisions it drove.",
    "stakeholder": "Give an example of managing a difficult stakeholder to a good outcome.",
    "requirements": "How do you ensure requirements are complete before development starts?",
    "reporting": "How do you decide which metrics and KPIs matter most to a business?",
    "agile": "How do you work within an Agile/Scrum cadence as a business analyst?",
    "data analysis": "Describe your approach to analyzing a large, messy dataset.",
    "process improvement": "Tell me about a process you mapped and then improved.",
}

_TITLE_QUESTIONS = {
    "senior": "As a senior analyst, how do you mentor others and set quality standards?",
    "lead": "How have you led a cross-functional initiative from discovery to delivery?",
    "data": "How do you balance deep data work with clear business communication?",
    "business partner": "How do you act as a true business partner rather than just a requirements taker?",
}


def _tokens(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9+#]+", (text or "").lower()) if t}


def generate_questions(job_title: str, description: str | None, skills: list[str] | None) -> list[str]:
    """Return a deduplicated, ordered list of prep questions for the job."""
    text = f"{job_title} {description or ''}"
    tokens = _tokens(text)
    skill_set = {s.lower() for s in (skills or [])}

    questions: list[str] = []
    seen: set[str] = set()

    def add(q: str) -> None:
        if q not in seen:
            seen.add(q)
            questions.append(q)

    # Job-specific skill questions first (most relevant).
    for skill, q in _SKILL_QUESTIONS.items():
        if skill in skill_set or skill in tokens:
            add(q)

    # Title-specific questions.
    for key, q in _TITLE_QUESTIONS.items():
        if key in tokens:
            add(q)

    # Core BA questions to round out the list.
    for q in _CORE_QUESTIONS:
        add(q)

    return questions[:12]

"""ORM models for ZEYRECUITE.

The schema is intentionally small and local-first. A ``Job`` carries both the
employer/job origin (used by the hard South-Asia gate) and the candidate
eligibility fields (used to decide whether the current user can apply).
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fingerprint: Mapped[str] = mapped_column(String(160), unique=True, index=True)

    title: Mapped[str] = mapped_column(String(300))
    company: Mapped[str] = mapped_column(String(300))
    location: Mapped[str | None] = mapped_column(String(300), nullable=True)
    work_mode: Mapped[str] = mapped_column(String(20), default="remote")

    # Origin (hard gate) vs candidate eligibility (soft gate).
    employer_country: Mapped[str | None] = mapped_column(String(8), nullable=True)
    job_country: Mapped[str | None] = mapped_column(String(8), nullable=True)
    candidate_required_location: Mapped[list | None] = mapped_column(JSON, nullable=True)
    worldwide_remote: Mapped[bool] = mapped_column(Boolean, default=False)

    salary: Mapped[str | None] = mapped_column(String(120), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[list | None] = mapped_column(JSON, nullable=True)

    url: Mapped[str] = mapped_column(String(600))
    source: Mapped[str] = mapped_column(String(40), default="unknown")
    posted_date: Mapped[str | None] = mapped_column(String(40), nullable=True)
    application_url: Mapped[str | None] = mapped_column(String(600), nullable=True)
    application_method: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # Location gate outcome.
    location_status: Mapped[str] = mapped_column(String(20), default="review")
    location_reason: Mapped[str | None] = mapped_column(String(80), nullable=True)

    # Scoring.
    score: Mapped[float] = mapped_column(Float, default=0.0)
    score_breakdown: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Explainable multi-factor assessment.
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_label: Mapped[str | None] = mapped_column(String(40), nullable=True)
    eligibility: Mapped[float] = mapped_column(Float, default=0.0)
    eligibility_label: Mapped[str | None] = mapped_column(String(40), nullable=True)
    confidence_breakdown: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Review workflow state.
    status: Mapped[str] = mapped_column(String(20), default="new", index=True)

    # F17 enrichment: company facts (hq, founded, employees, industry) from
    # Wikidata. Nullable JSON; empty when enrichment has not run or found data.
    company_facts: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "work_mode": self.work_mode,
            "employer_country": self.employer_country,
            "job_country": self.job_country,
            "candidate_required_location": self.candidate_required_location,
            "worldwide_remote": self.worldwide_remote,
            "salary": self.salary,
            "description": self.description,
            "skills": self.skills,
            "url": self.url,
            "source": self.source,
            "posted_date": self.posted_date,
            "application_url": self.application_url,
            "application_method": self.application_method,
            "location_status": self.location_status,
            "location_reason": self.location_reason,
            "score": self.score,
            "score_breakdown": self.score_breakdown,
            "confidence": self.confidence,
            "confidence_label": self.confidence_label,
            "eligibility": self.eligibility,
            "eligibility_label": self.eligibility_label,
            "confidence_breakdown": self.confidence_breakdown,
            "status": self.status,
            "company_facts": self.company_facts,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Identity & contact
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    linkedin: Mapped[str | None] = mapped_column(String(300), nullable=True)
    website: Mapped[str | None] = mapped_column(String(300), nullable=True)
    github: Mapped[str | None] = mapped_column(String(300), nullable=True)
    # Location & availability
    current_country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    availability: Mapped[str | None] = mapped_column(String(120), nullable=True)
    notice_period: Mapped[str | None] = mapped_column(String(120), nullable=True)
    # Role & positioning
    role: Mapped[str | None] = mapped_column(String(120), nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Skills & knowledge
    skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    keywords: Mapped[list | None] = mapped_column(JSON, nullable=True)
    languages: Mapped[list | None] = mapped_column(JSON, nullable=True)
    certifications: Mapped[list | None] = mapped_column(JSON, nullable=True)  # {name, issuer, year}
    projects: Mapped[list | None] = mapped_column(JSON, nullable=True)  # {name, description, tech}
    interests: Mapped[list | None] = mapped_column(JSON, nullable=True)
    # Experience & education
    experiences: Mapped[list | None] = mapped_column(JSON, nullable=True)
    education: Mapped[list | None] = mapped_column(JSON, nullable=True)
    # Compensation & logistics
    expected_salary: Mapped[str | None] = mapped_column(String(120), nullable=True)
    min_salary: Mapped[str | None] = mapped_column(String(120), nullable=True)
    work_authorization: Mapped[str | None] = mapped_column(String(160), nullable=True)
    visa_status: Mapped[str | None] = mapped_column(String(160), nullable=True)
    preferred_work_mode: Mapped[str | None] = mapped_column(String(40), nullable=True)
    # Preferences
    target_companies: Mapped[list | None] = mapped_column(JSON, nullable=True)
    deal_breakers: Mapped[list | None] = mapped_column(JSON, nullable=True)
    standard_answers: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    resume_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_path: Mapped[str | None] = mapped_column(String(400), nullable=True)
    # v2.3 — saved job filters (F10) and resume variants (F12).
    saved_filters: Mapped[list | None] = mapped_column(JSON, nullable=True)
    resume_variants: Mapped[list | None] = mapped_column(JSON, nullable=True)
    # v2.4 — application goals / KPI tracking.
    weekly_goal: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kpi_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "linkedin": self.linkedin,
            "website": self.website,
            "github": self.github,
            "current_country": self.current_country,
            "city": self.city,
            "timezone": self.timezone,
            "availability": self.availability,
            "notice_period": self.notice_period,
            "role": self.role,
            "years_experience": self.years_experience,
            "summary": self.summary,
            "skills": self.skills,
            "keywords": self.keywords,
            "languages": self.languages,
            "certifications": self.certifications,
            "projects": self.projects,
            "interests": self.interests,
            "experiences": self.experiences,
            "education": self.education,
            "expected_salary": self.expected_salary,
            "min_salary": self.min_salary,
            "work_authorization": self.work_authorization,
            "visa_status": self.visa_status,
            "preferred_work_mode": self.preferred_work_mode,
            "target_companies": self.target_companies,
            "deal_breakers": self.deal_breakers,
            "standard_answers": self.standard_answers,
            "resume_path": self.resume_path,
            "saved_filters": self.saved_filters,
            "resume_variants": self.resume_variants,
            "weekly_goal": self.weekly_goal,
            "kpi_state": self.kpi_state,
        }


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[int] = mapped_column(Integer, index=True)
    # draft → ready → submitting → submitted | failed
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True)
    # Manual application-stage tracking (no email connected).
    # draft → ready → submitting → submitted | failed
    application_status: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    resume_pdf_path: Mapped[str | None] = mapped_column(String(400), nullable=True)
    cover_letter: Mapped[str | None] = mapped_column(Text, nullable=True)
    answers: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # Editable, prefilled application form (per-job fields the user can edit).
    application_form: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # v2.3 — cover-letter personalization score (F13).
    personalization_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Submission tracking.
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    submission_method: Mapped[str | None] = mapped_column(String(40), nullable=True)
    submission_url: Mapped[str | None] = mapped_column(String(600), nullable=True)
    submission_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    submission_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "job_id": self.job_id,
            "status": self.status,
            "application_status": self.application_status,
            "resume_pdf": f"/api/jobs/{self.job_id}/resume.pdf" if self.resume_pdf_path else None,
            "cover_letter": self.cover_letter,
            "application_form": self.application_form,
            "personalization_score": self.personalization_score,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "submission_method": self.submission_method,
            "submission_url": self.submission_url,
            "submission_status": self.submission_status,
            "submission_message": self.submission_message,
            "attempts": self.attempts,
            "last_attempt_at": self.last_attempt_at.isoformat() if self.last_attempt_at else None,
        }


class ScrapeRun(Base):
    __tablename__ = "scrape_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="running")
    fetched: Mapped[int] = mapped_column(Integer, default=0)
    eligible: Mapped[int] = mapped_column(Integer, default=0)
    rejected: Mapped[int] = mapped_column(Integer, default=0)
    review: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # v2.3 — fit trend (F11): average confidence/eligibility of jobs from this run.
    avg_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_eligibility: Mapped[float | None] = mapped_column(Float, nullable=True)


class Feedback(Base):
    """User feedback signal used to power the learning loop.

    Records approve / reject / select signals on a job. The learning engine
    aggregates these into skill / company / source / work-mode preferences and
    applies them as additive reweights during scoring.
    """
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[int] = mapped_column(Integer, index=True)
    signal: Mapped[str] = mapped_column(String(20))  # approve | reject | select
    source: Mapped[str | None] = mapped_column(String(40), nullable=True)  # manual | approve-btn | reject-btn | select
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    display_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(120))
    password_salt: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

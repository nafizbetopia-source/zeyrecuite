"""Collection orchestration: fetch, gate, dedup, score, persist.

The location gate runs *before* persistence so excluded jobs never enter the
database. Eligible jobs are scored and stored; review jobs are stored with a
``review`` status so the user can resolve ambiguous eligibility.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx

from .adapters import BaseAdapter, build_adapters
from .companies import get_company_info
from .config import AppConfig
from .database import Database
from .dedup import fingerprint
from .location_policy import DecisionStatus, evaluate_location
from .models import Job, Profile, ScrapeRun
from .scoring import assess_job


@dataclass
class RunSummary:
    source: str
    fetched: int
    eligible: int
    rejected: int
    review: int
    duplicates: int
    error: str | None = None


def _profile_context(db: Database) -> tuple[str, list[str]]:
    with db.session() as session:
        profile = session.get(Profile, 1)
        if profile:
            return profile.current_country or "Bangladesh", list(profile.skills or [])
    return "Bangladesh", []


def _existing_fingerprints(db: Database) -> set[str]:
    with db.session() as session:
        rows = session.query(Job.fingerprint).all()
    return {row[0] for row in rows}


def _apply_gate(raw: dict[str, Any], current_country: str) -> tuple[str, str]:
    decision = evaluate_location(
        employer_country=raw.get("employer_country"),
        job_country=raw.get("job_country"),
        work_mode=raw.get("work_mode", "remote"),
        current_country=current_country,
        worldwide_remote=bool(raw.get("worldwide_remote")),
        allowed_applicant_countries=raw.get("candidate_required_location"),
    )
    return decision.status.value, decision.reason


def run_source(
    db: Database,
    config: AppConfig,
    adapter: BaseAdapter,
    *,
    client: httpx.Client | None = None,
) -> RunSummary:
    """Run one source end to end and persist the outcome."""
    run = ScrapeRun(source=adapter.name, status="running")
    with db.session() as session:
        session.add(run)
        session.commit()
        run_id = run.id

    summary = RunSummary(source=adapter.name, fetched=0, eligible=0, rejected=0, review=0, duplicates=0)
    try:
        raw_jobs = adapter.fetch(client=client)
    except Exception as exc:  # noqa: BLE001
        summary.error = f"{type(exc).__name__}: {exc}"
        _finish_run(db, run_id, summary)
        return summary

    current_country, profile_skills = _profile_context(db)
    seen = _existing_fingerprints(db)
    summary.fetched = len(raw_jobs)
    run_confidences: list[float] = []
    run_eligibilities: list[float] = []

    with db.session() as session:
        for raw in raw_jobs:
            fp = fingerprint(raw.get("title"), raw.get("company"), raw.get("url"))
            if fp in seen:
                summary.duplicates += 1
                continue
            seen.add(fp)

            status, reason = _apply_gate(raw, current_country)
            if status == DecisionStatus.REJECTED.value:
                summary.rejected += 1
                continue

            company_overall = get_company_info(raw.get("company", "")).overall
            assessment = assess_job(
                title=raw.get("title", ""),
                description=raw.get("description"),
                job_skills=raw.get("skills"),
                profile_skills=profile_skills,
                target_role=config.role,
                location_status=status,
                work_mode=raw.get("work_mode", "remote"),
                salary=raw.get("salary"),
                min_salary=config.min_salary,
                company_overall=company_overall,
                posted_date=raw.get("posted_date"),
                application_url=raw.get("application_url"),
                preferred_remote=True,
            )
            job = Job(
                fingerprint=fp,
                title=raw.get("title", ""),
                company=raw.get("company", ""),
                location=raw.get("location"),
                work_mode=raw.get("work_mode", "remote"),
                employer_country=raw.get("employer_country"),
                job_country=raw.get("job_country"),
                candidate_required_location=raw.get("candidate_required_location"),
                worldwide_remote=bool(raw.get("worldwide_remote")),
                salary=raw.get("salary"),
                description=raw.get("description"),
                skills=raw.get("skills"),
                url=raw.get("url", ""),
                source=raw.get("source", adapter.name),
                posted_date=raw.get("posted_date"),
                application_url=raw.get("application_url"),
                application_method=raw.get("application_method"),
                location_status=status,
                location_reason=reason,
                score=assessment.fit_score,
                score_breakdown=assessment.breakdown,
                confidence=assessment.confidence,
                confidence_label=assessment.confidence_label,
                eligibility=assessment.eligibility,
                eligibility_label=assessment.eligibility_label,
                confidence_breakdown={
                    "factors": [
                        {"key": f.key, "label": f.label, "value": f.value,
                         "weight": f.weight, "detail": f.detail}
                        for f in assessment.factors
                    ],
                    "matched_skills": assessment.matched_skills,
                    "missing_skills": assessment.missing_skills,
                    "must_have_present": assessment.must_have_present,
                    "must_have_missing": assessment.must_have_missing,
                    "reasons": assessment.reasons,
                },
                status="new" if status == DecisionStatus.ELIGIBLE.value else "review",
            )
            session.add(job)
            run_confidences.append(assessment.confidence)
            run_eligibilities.append(assessment.eligibility)
            if status == DecisionStatus.ELIGIBLE.value:
                summary.eligible += 1
            else:
                summary.review += 1
        session.commit()

    _finish_run(db, run_id, summary, run_confidences, run_eligibilities)
    return summary


def _finish_run(
    db: Database,
    run_id: int,
    summary: RunSummary,
    confidences: list[float] | None = None,
    eligibilities: list[float] | None = None,
) -> None:
    with db.session() as session:
        run = session.get(ScrapeRun, run_id)
        if run:
            run.status = "error" if summary.error else "done"
            run.fetched = summary.fetched
            run.eligible = summary.eligible
            run.rejected = summary.rejected
            run.review = summary.review
            run.error = summary.error
            run.finished_at = datetime.now(timezone.utc)
            if confidences:
                run.avg_confidence = round(sum(confidences) / len(confidences), 1)
            if eligibilities:
                run.avg_eligibility = round(sum(eligibilities) / len(eligibilities), 1)
            session.commit()


def run_all(db: Database, config: AppConfig, *, client: httpx.Client | None = None) -> list[RunSummary]:
    """Run every enabled source and return per-source summaries."""
    summaries: list[RunSummary] = []
    for adapter in build_adapters(config):
        summaries.append(run_source(db, config, adapter, client=client))
    return summaries

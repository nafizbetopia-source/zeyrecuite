"""Collection orchestration: fetch, gate, dedup, score, persist.

The location gate runs *before* persistence so excluded jobs never enter the
database. Eligible jobs are scored and stored; review jobs are stored with a
``review`` status so the user can resolve ambiguous eligibility.
"""
from __future__ import annotations

import html as html_module
import re
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
from .learning import compute_learning_weights
from .models import Feedback, Job, Profile, ScrapeRun
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


# ---------------------------------------------------------------------------
# Data-cleanup helpers.
#
# Raw job records arrive from a mix of sources in inconsistent shapes: some
# carry real HTML descriptions, some carry already-escaped text, and a few
# carry mojibake (UTF-8 bytes decoded as Latin-1). Before a record is scored
# and persisted we normalise it so the database never stores corrupted text.
# ---------------------------------------------------------------------------

_MOJIBAKE_REPLACEMENTS = {
    "â": "'", "â": '"', "â": '"', "â": "-", "â": "-",
    "â¦": "...", "Â": "", "â": "'", "â": "'", "Â°": "°",
    "Â­": "", "Â¡": "¡", "Â£": "£", "Â¥": "¥", "Â©": "©",
    "Â®": "®", "â¢": "™", "â": "", "â": "", "Ââ": '"',
}


def _unescape(text: str) -> str:
    """Decode HTML entities (``&amp;`` -> ``&``) that were stored literally."""
    if not text:
        return text
    return html_module.unescape(text)


def _fix_mojibake(text: str) -> str:
    """Repair UTF-8-as-Latin-1 mojibake.

    Two complementary cases are handled:

    1. **General 2-byte sequences.** A UTF-8 byte pair ``0xC2/0xC3`` +
       ``0x80-0xBF`` decoded as Latin-1 renders as ``Â/Ã`` followed by a
       character in ``0xB0-0xBF`` (e.g. ``MecÃ¡nico`` -> ``Mecánico``,
       ``Ã©`` -> ``é``). We re-encode those pairs back to UTF-8.
    2. **Known mojibake literals** (smart quotes, dashes, ellipsis) from
       ``_MOJIBAKE_REPLACEMENTS``.

    Any residual lone ``Â`` (from ``°``, ``­``, etc.) is stripped.
    """
    if not text:
        return text

    # Case 1: re-encode the general 2-byte UTF-8-as-Latin-1 sequences.
    # The first byte is U+00C2 (Â) or U+00C3 (Ã); the second is U+0080–U+00BF.
    def _reencode(m: "re.Match[str]") -> str:
        hi = ord(m.group(1))
        lo = ord(m.group(2))
        try:
            return bytes([hi, lo]).decode("utf-8")
        except UnicodeDecodeError:
            return m.group(0)

    # Case 1b: 3-byte UTF-8-as-Latin-1 sequences. A 3-byte UTF-8 char
    # (U+0800-U+FFFF) decoded as Latin-1 becomes U+00C2-U+00EF followed by
    # two bytes in U+0080-U+00BF. Re-encode those triples back to UTF-8.
    # Run BEFORE the 2-byte pass so the shared first byte isn't consumed first.
    def _reencode3(m: "re.Match[str]") -> str:
        b1 = ord(m.group(1))
        b2 = ord(m.group(2))
        b3 = ord(m.group(3))
        try:
            return bytes([b1, b2, b3]).decode("utf-8")
        except UnicodeDecodeError:
            return m.group(0)

    text = re.sub(r"([\u00c2-\u00ef])([\x80-\xbf])([\x80-\xbf])", _reencode3, text)

    # Case 1a: re-encode the general 2-byte UTF-8-as-Latin-1 sequences.
    text = re.sub(r"([\u00c2-\u00df])([\x80-\xbf])", _reencode, text)

    # Case 2: known mojibake literals.
    for mojibake, fixed in _MOJIBAKE_REPLACEMENTS.items():
        if mojibake in text:
            text = text.replace(mojibake, fixed)

    # Strip any residual lone Â (from °, ­, ¡, £, etc. that were single-byte
    # in the original and only got the Â prefix from a partial decode).
    text = text.replace("Â", "")
    return text


def _clean_text(value: str | None) -> str | None:
    """Unescape entities, repair mojibake, and strip HTML to plain text.

    Handles both real HTML (``<p>Hi</p>``) and HTML-escaped content
    (``&lt;p&gt;Hi&lt;/p&gt;``) by unescaping first, then stripping tags.
    """
    if not value:
        return value
    text = _unescape(value)
    text = _fix_mojibake(text)
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
    except Exception:  # noqa: BLE001 - fall back to a regex strip
        text = re.sub(r"<[^>]+>", " ", text)
    # Strip any dangling tags left by truncation (e.g. a cut-off "<br" with no
    # closing ">") so no raw markup survives.
    text = re.sub(r"<[a-zA-Z/][^<>]*$", " ", text)
    text = re.sub(r"<[a-zA-Z/]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _clean_skills(skills: Any) -> list[str] | None:
    """Normalise a skills field into a clean list of non-empty strings.

    Guards against the import path storing a single string (which SQLite/JSON
    then serialises as a list of characters) and against generic filler values.
    """
    if skills is None:
        return None
    if isinstance(skills, str):
        # A bare string was stored as a list of characters; recover the words.
        words = re.findall(r"[A-Za-z0-9+./-]+(?:\s+[A-Za-z0-9+./-]+)*", skills)
        skills = words if words else []
    if not isinstance(skills, list):
        return None
    cleaned = []
    for s in skills:
        if not isinstance(s, str):
            continue
        s = s.strip().lower()
        if not s:
            continue
        cleaned.append(s)
    return cleaned or None


def _clean_raw(raw: dict[str, Any]) -> dict[str, Any]:
    """Apply data-cleanup to a raw job record before scoring/persistence."""
    raw = dict(raw)
    for field in ("title", "company", "location"):
        if raw.get(field):
            raw[field] = _fix_mojibake(_unescape(str(raw[field])))
    if raw.get("description"):
        raw["description"] = _clean_text(raw.get("description"))
    if raw.get("skills") is not None:
        raw["skills"] = _clean_skills(raw.get("skills"))
    return raw


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
    # Compute learning multipliers once per run from the user's feedback
    # history so every job in this scan is scored with the same additive
    # reweights derived from what the user has approved / rejected / selected.
    learning = _learning_weights(db)
    summary.fetched = len(raw_jobs)
    run_confidences: list[float] = []
    run_eligibilities: list[float] = []

    with db.session() as session:
        for raw in raw_jobs:
            raw = _clean_raw(raw)
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
                learning=learning,
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


def _learning_weights(db: Database):
    """Build additive learning multipliers from the user's feedback history.

    Returns ``None`` when there is no feedback yet (scoring is unchanged), so
    the collector path stays byte-for-byte identical for fresh installs.
    """
    with db.session() as session:
        rows = session.query(Feedback).all()
        if not rows:
            return None
        jobs_by_id = {j.id: j for j in session.query(Job).all()}
        return compute_learning_weights(
            (
                {
                    "job_id": r.job_id,
                    "signal": r.signal,
                    "skills": jobs_by_id[r.job_id].skills,
                    "company": jobs_by_id[r.job_id].company,
                    "source": jobs_by_id[r.job_id].source,
                    "work_mode": jobs_by_id[r.job_id].work_mode,
                }
                for r in rows
            ),
            jobs_by_id=jobs_by_id,
        )


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

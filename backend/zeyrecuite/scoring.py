"""Deterministic, explainable matching engine (Tier 0 — no LLM, $0, reproducible).

The engine produces a rich :class:`Assessment` for every job:

* **fit_score** — role fit (title + skill overlap + must-have coverage).
* **eligibility** — how eligible the *current user* is (location policy, work
  mode, salary floor).
* **confidence** — a weighted blend of six independent factors, each scored
  0-100 with a plain-language detail string, so the dashboard can explain
  *exactly* why a job ranked the way it did.

Everything is deterministic: the same inputs always yield the same output,
which keeps rankings stable and the whole system auditable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

# Business-analytic vocabulary used to recognize relevant roles.
_ROLE_KEYWORDS = {
    "business analyst", "business analysis", "ba", "data analyst", "data analysis",
    "analytics", "analyst", "requirements", "stakeholder", "process improvement",
    "reporting", "dashboards", "sql", "excel", "power bi", "tableau", "etl",
    "data modeling", "kpi", "metrics", "insights", "documentation", "agile",
}

_SYNONYMS = {
    "ba": {"business analyst", "business analysis"},
    "analytics": {"analysis", "analyst"},
    "sql": {"mysql", "postgresql", "postgres", "t-sql"},
    "excel": {"microsoft excel", "spreadsheet"},
    "power bi": {"powerbi"},
    "tableau": {"tableau"},
}

# Core skills a strong BA/data-analyst posting is expected to mention.
_MUST_HAVE = {"sql", "excel", "stakeholder", "requirements", "reporting"}

# Factor weights for the confidence blend (must sum to 1.0).
_WEIGHTS = {
    "role_fit": 0.38,
    "skill_coverage": 0.17,
    "eligibility": 0.20,
    "company_quality": 0.13,
    "freshness": 0.06,
    "completeness": 0.06,
}


@dataclass
class ScoreResult:
    score: float
    breakdown: dict = field(default_factory=dict)


@dataclass
class FactorScore:
    key: str
    label: str
    value: float  # 0-100
    weight: float
    detail: str


@dataclass
class Assessment:
    fit_score: float
    confidence: float
    confidence_label: str
    eligibility: float
    eligibility_label: str
    factors: list[FactorScore]
    matched_skills: list[str]
    missing_skills: list[str]
    must_have_present: list[str]
    must_have_missing: list[str]
    reasons: list[str]
    breakdown: dict = field(default_factory=dict)


def _tokens(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9+#]+", text.lower()) if t}


def _expand(skill: str) -> set[str]:
    skill = skill.lower().strip()
    return {skill, *_SYNONYMS.get(skill, set())}


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def _fit_components(
    *,
    title: str,
    description: str | None,
    job_skills: list[str] | None,
    profile_skills: list[str] | None,
    target_role: str = "Business Analyst",
) -> dict:
    """Compute the role-fit sub-scores and the matched/missing skill sets."""
    profile_skills = [s for s in (profile_skills or []) if s]
    job_skills = [s for s in (job_skills or []) if s]
    text = f"{title} {description or ''}".lower()
    text_tokens = _tokens(text)

    # 1) Title relevance (0-30).
    title_tokens = _tokens(title)
    role_hits = sum(1 for kw in _ROLE_KEYWORDS if kw in title_tokens or kw in title.lower())
    title_score = min(30.0, role_hits * 10.0)
    if target_role.lower() in title.lower():
        title_score = 30.0

    # 2) Skill overlap (0-50).
    profile_expanded: set[str] = set()
    for skill in profile_skills:
        profile_expanded |= _expand(skill)
    job_expanded: set[str] = set()
    for skill in job_skills:
        job_expanded |= _expand(skill)
    matched = profile_expanded & job_expanded
    for skill in profile_expanded:
        if skill in text_tokens:
            matched.add(skill)
    overlap = (len(matched) / len(profile_expanded)) if profile_expanded else 0.0
    skill_score = overlap * 50.0

    # 3) Must-have coverage (0-20).
    present = {m for m in _MUST_HAVE if m in text_tokens or m in job_expanded}
    must_score = (len(present) / len(_MUST_HAVE)) * 20.0

    # Skills the job asks for that the profile does NOT cover (for the UI).
    missing = sorted(job_expanded - profile_expanded - matched)
    missing = [m for m in missing if m not in _SYNONYMS]

    return {
        "title_score": title_score,
        "skill_score": skill_score,
        "must_score": must_score,
        "fit_score": round(title_score + skill_score + must_score, 1),
        "matched": matched,
        "missing": missing,
        "must_present": present,
        "must_missing": _MUST_HAVE - present,
        "profile_expanded": profile_expanded,
        "job_expanded": job_expanded,
    }


def score_job(
    *,
    title: str,
    description: str | None,
    job_skills: list[str] | None,
    profile_skills: list[str] | None,
    target_role: str = "Business Analyst",
) -> ScoreResult:
    """Return a 0-100 role-fit score with an explainable breakdown.

    Kept for backward compatibility (used by the collector and existing tests).
    """
    c = _fit_components(
        title=title,
        description=description,
        job_skills=job_skills,
        profile_skills=profile_skills,
        target_role=target_role,
    )
    return ScoreResult(
        score=c["fit_score"],
        breakdown={
            "title": round(c["title_score"], 1),
            "skills": round(c["skill_score"], 1),
            "must_have": round(c["must_score"], 1),
            "matched_skills": sorted(c["matched"]),
        },
    )


# ---------- Eligibility ----------

def _salary_value(salary: str | None) -> float | None:
    """Extract a rough annual figure **in thousands** from a salary string.

    Handles "$120,000", "120k", "120000", and monthly figures like "8000/mo".
    The result is normalized to thousands so it can be compared against a
    ``min_salary`` expressed in thousands (e.g. 100 == $100k).
    """
    if not salary:
        return None
    text = salary.replace("$", "").replace(",", "")
    nums = re.findall(r"\d+(?:\.\d+)?", text)
    if not nums:
        return None
    try:
        raw = float(nums[0])
    except ValueError:
        return None
    low = text.lower()
    monthly = bool(re.search(r"\bmo\b|/mo|month|monthly", low))
    # Normalize to thousands.
    if monthly:
        return raw * 12.0 / 1000.0
    if raw >= 1000:
        return raw / 1000.0  # full dollar amount, e.g. 120000 -> 120k
    if "k" in low:
        return raw  # already in thousands, e.g. "120k"
    if raw < 100:
        return raw * 12.0  # likely monthly/hourly -> annualize
    return raw  # assume already in thousands, e.g. "120"


def eligibility_score(
    *,
    location_status: str,
    work_mode: str,
    salary: str | None,
    min_salary: float | None,
    preferred_remote: bool = True,
) -> tuple[float, str, list[str]]:
    """Score how eligible the current user is for this job (0-100).

    Driven by the location gate outcome, work-mode preference, and salary floor.
    Returns (score, label, reasons).
    """
    reasons: list[str] = []
    score = 100.0

    if location_status == "eligible":
        reasons.append("Location and eligibility checks passed.")
    elif location_status == "review":
        score -= 40.0
        reasons.append("Eligibility needs a quick manual check (location data is ambiguous).")
    else:  # rejected
        score = 0.0
        reasons.append("Not eligible: blocked by the location/origin policy.")

    if score > 0:
        if preferred_remote and work_mode == "remote":
            reasons.append("Remote role — matches your remote preference.")
        elif work_mode == "hybrid":
            score -= 10.0
            reasons.append("Hybrid role — a small penalty vs. fully remote.")
        elif work_mode == "onsite":
            score -= 25.0
            reasons.append("On-site role — penalized against your remote preference.")

        sal = _salary_value(salary)
        if min_salary and sal is not None:
            if sal >= min_salary:
                reasons.append(f"Salary meets your floor (~{min_salary:,.0f}k).")
            else:
                score -= 20.0
                reasons.append(f"Salary is below your floor (~{min_salary:,.0f}k).")

    score = _clamp(score)
    if score >= 85:
        label = "Fully eligible"
    elif score >= 60:
        label = "Mostly eligible"
    elif score >= 30:
        label = "Partially eligible"
    else:
        label = "Not eligible"
    return score, label, reasons


# ---------- Freshness & completeness ----------

def _freshness_score(posted_date: str | None) -> tuple[float, str]:
    """Score how recent the posting is (0-100). Unknown dates are neutral."""
    if not posted_date:
        return 50.0, "Posting date unknown (neutral)."
    text = posted_date.lower()
    now = datetime.now(timezone.utc)
    days = None
    m = re.search(r"(\d+)\s*(day|d)\b", text)
    if m:
        days = int(m.group(1))
    else:
        m = re.search(r"(\d+)\s*(hour|h)\b", text)
        if m:
            days = int(m.group(1)) / 24.0
        else:
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%b %d, %Y", "%d %b %Y"):
                try:
                    dt = datetime.strptime(text.strip()[:19], fmt)
                    dt = dt.replace(tzinfo=timezone.utc)
                    days = (now - dt).total_seconds() / 86400.0
                    break
                except ValueError:
                    continue
    if days is None:
        return 50.0, "Posting date unparseable (neutral)."
    if days < 0:
        days = 0
    # Freshness decays: 0 days → 100, 30+ days → 0.
    value = _clamp(100.0 - (days / 30.0) * 100.0)
    if days < 1:
        detail = "Posted today — very fresh."
    elif days < 7:
        detail = f"Posted ~{days:.0f} days ago — fresh."
    elif days < 30:
        detail = f"Posted ~{days:.0f} days ago."
    else:
        detail = f"Posted ~{days:.0f} days ago — aging."
    return value, detail


def _completeness_score(
    *,
    description: str | None,
    salary: str | None,
    skills: list[str] | None,
    application_url: str | None,
) -> tuple[float, str]:
    """Score how complete the job data is (0-100). More data → more trust."""
    points = 0
    notes = []
    if description and len(description) > 80:
        points += 40
        notes.append("full description")
    else:
        notes.append("missing/short description")
    if skills:
        points += 25
        notes.append("skills listed")
    if salary:
        points += 20
        notes.append("salary shown")
    if application_url:
        points += 15
        notes.append("apply link")
    return _clamp(points), "Data: " + ", ".join(notes) + "."


# ---------- Company quality ----------

def _company_quality_score(overall: float | None) -> tuple[float, str]:
    if overall is None:
        return 50.0, "No curated rating (neutral)."
    value = (overall / 5.0) * 100.0
    return _clamp(value), f"Company rating {overall:.1f}/5."


# ---------- Main assessment ----------

def assess_job(
    *,
    title: str,
    description: str | None,
    job_skills: list[str] | None,
    profile_skills: list[str] | None,
    target_role: str = "Business Analyst",
    location_status: str = "eligible",
    work_mode: str = "remote",
    salary: str | None = None,
    min_salary: float | None = None,
    company_overall: float | None = None,
    posted_date: str | None = None,
    application_url: str | None = None,
    preferred_remote: bool = True,
) -> Assessment:
    """Produce the full, explainable assessment for a single job."""
    c = _fit_components(
        title=title,
        description=description,
        job_skills=job_skills,
        profile_skills=profile_skills,
        target_role=target_role,
    )
    fit = c["fit_score"]

    elig, elig_label, elig_reasons = eligibility_score(
        location_status=location_status,
        work_mode=work_mode,
        salary=salary,
        min_salary=min_salary,
        preferred_remote=preferred_remote,
    )
    fresh, fresh_detail = _freshness_score(posted_date)
    complete, complete_detail = _completeness_score(
        description=description,
        salary=salary,
        skills=job_skills,
        application_url=application_url,
    )
    company, company_detail = _company_quality_score(company_overall)

    # Skill coverage: how much of the job's required skill set the profile covers.
    if c["job_expanded"]:
        covered = len(c["job_expanded"] & c["profile_expanded"]) / len(c["job_expanded"])
    else:
        covered = 0.5  # neutral when the job lists no skills
    skill_coverage = _clamp(covered * 100.0)

    factors = [
        FactorScore("role_fit", "Role fit", _clamp(fit), _WEIGHTS["role_fit"],
                    f"Title + skill overlap + must-have coverage = {fit:.0f}/100."),
        FactorScore("skill_coverage", "Skill coverage", skill_coverage, _WEIGHTS["skill_coverage"],
                    f"Covers {covered:.0%} of the skills this role asks for."),
        FactorScore("eligibility", "Your eligibility", elig, _WEIGHTS["eligibility"],
                    elig_label + " — " + (elig_reasons[0] if elig_reasons else "")),
        FactorScore("company_quality", "Company quality", company, _WEIGHTS["company_quality"],
                    company_detail),
        FactorScore("freshness", "Freshness", fresh, _WEIGHTS["freshness"], fresh_detail),
        FactorScore("completeness", "Data completeness", complete, _WEIGHTS["completeness"],
                    complete_detail),
    ]

    confidence = _clamp(round(sum(f.value * f.weight for f in factors), 1))
    confidence, label = _label(confidence)

    # Plain-language reasons, most important first.
    reasons: list[str] = []
    if fit >= 70:
        reasons.append(f"Strong role fit ({fit:.0f}/100) — the title and skills line up well.")
    elif fit >= 45:
        reasons.append(f"Moderate role fit ({fit:.0f}/100).")
    else:
        reasons.append(f"Weak role fit ({fit:.0f}/100) — limited overlap with your profile.")
    if c["must_missing"]:
        reasons.append("Missing core skills: " + ", ".join(sorted(c["must_missing"])) + ".")
    if c["matched"]:
        reasons.append("Matches your skills: " + ", ".join(sorted(c["matched"])[:6]) + ".")
    reasons.extend(elig_reasons)
    reasons.append(company_detail)
    reasons.append(fresh_detail)

    return Assessment(
        fit_score=fit,
        confidence=confidence,
        confidence_label=label,
        eligibility=elig,
        eligibility_label=elig_label,
        factors=factors,
        matched_skills=sorted(c["matched"]),
        missing_skills=c["missing"],
        must_have_present=sorted(c["must_present"]),
        must_have_missing=sorted(c["must_missing"]),
        reasons=reasons,
        breakdown={
            "title": round(c["title_score"], 1),
            "skills": round(c["skill_score"], 1),
            "must_have": round(c["must_score"], 1),
            "matched_skills": sorted(c["matched"]),
            "factors": {f.key: round(f.value, 1) for f in factors},
        },
    )


def _label(value: float) -> tuple[float, str]:
    if value >= 85:
        return value, "Excellent match"
    if value >= 70:
        return value, "Strong match"
    if value >= 55:
        return value, "Good match"
    if value >= 40:
        return value, "Possible match"
    return value, "Weak match"


def confidence(fit_score: float, company_overall: float | None) -> tuple[float, str]:
    """Legacy 2-factor blend, kept for backward compatibility."""
    if company_overall is not None:
        company_component = (company_overall / 5.0) * 100.0
        value = round(0.7 * fit_score + 0.3 * company_component, 1)
    else:
        value = round(fit_score, 1)
    value = max(0.0, min(100.0, value))
    return value, _label(value)[1]

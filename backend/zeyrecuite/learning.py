"""Learning loop — turns user approve / reject / select signals into
additive reweights that make every subsequent scan smarter.

The scoring core in ``scoring.py`` stays deterministic. Learning is purely
*additive*: it reads the user's feedback history, derives preference signals
for skills, companies, sources, and work modes, and returns a small set of
multipliers that the collector / rescore / assessment path applies on top of
the base weights.

Design goals
------------
* Deterministic given the same feedback history (no randomness, no LLM).
* Bounded — a single signal can never dominate the base score.
* Safe — unknown / empty history yields neutral multipliers (no change).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable, Optional

# --- Tuning knobs -----------------------------------------------------------
# Each multiplier is clamped to [MIN_MULT, MAX_MULT] so feedback is additive
# and never destructive.
MIN_MULT = 0.85
MAX_MULT = 1.35

# How many of the top signals to surface in insights.
INSIGHT_LIMIT = 5


@dataclass
class LearningWeights:
    """Additive reweights applied to the base fit score.

    ``fit_mult`` scales the role-fit component. ``confidence_mult`` scales the
    overall confidence. ``pref_mult`` is folded into fit as a small bonus for
    jobs that line up with what the user has liked.
    """

    fit_mult: float = 1.0
    confidence_mult: float = 1.0
    pref_mult: float = 1.0
    # Derived preference signals, surfaced in the UI.
    top_skills: list = field(default_factory=list)
    top_companies: list = field(default_factory=list)
    top_sources: list = field(default_factory=list)
    top_work_modes: list = field(default_factory=list)
    approved: int = 0
    rejected: int = 0
    selected: int = 0
    has_data: bool = False

    def to_dict(self) -> dict:
        return {
            "fit_mult": round(self.fit_mult, 4),
            "confidence_mult": round(self.confidence_mult, 4),
            "pref_mult": round(self.pref_mult, 4),
            "top_skills": self.top_skills,
            "top_companies": self.top_companies,
            "top_sources": self.top_sources,
            "top_work_modes": self.top_work_modes,
            "approved": self.approved,
            "rejected": self.rejected,
            "selected": self.selected,
            "has_data": self.has_data,
        }


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _signal_weight(signal: str) -> float:
    """Weight of a single feedback signal. Select > approve > reject."""
    return {"select": 2.0, "approve": 1.0, "reject": -1.0}.get(signal, 0.0)


def compute_learning_weights(
    feedback_rows: Iterable[dict],
    jobs_by_id: Optional[dict] = None,
) -> LearningWeights:
    """Compute additive reweights from feedback rows.

    Parameters
    ----------
    feedback_rows:
        Iterable of dicts with keys ``job_id``, ``signal``, and optional
        ``source``. Each row must be able to resolve a job via
        ``jobs_by_id`` (or the caller passes richer dicts that already include
        job attributes).
    jobs_by_id:
        Optional mapping ``job_id -> job-like object`` exposing ``skills``,
        ``company``, ``source``, and ``work_mode``. When provided, feedback is
        attributed to the job's attributes so we can learn skill / company /
        source / work-mode preferences.

    Returns
    -------
    LearningWeights
    """
    jobs_by_id = jobs_by_id or {}
    approved = rejected = selected = 0
    skill_scores: Counter = Counter()
    company_scores: Counter = Counter()
    source_scores: Counter = Counter()
    workmode_scores: Counter = Counter()

    for row in feedback_rows:
        signal = (row.get("signal") or "").lower()
        if signal not in ("approve", "reject", "select"):
            continue
        w = _signal_weight(signal)
        if signal == "approve":
            approved += 1
        elif signal == "reject":
            rejected += 1
        elif signal == "select":
            selected += 1

        job = jobs_by_id.get(row.get("job_id")) if jobs_by_id else None
        if job is None:
            # Fall back to a row that already carries job attributes.
            job = row
        if job is None:
            continue

        # Skills
        job_skills = job.get("skills") if isinstance(job, dict) else getattr(job, "skills", None)
        for sk in job_skills or []:
            skill_scores[sk] += w
        # Company
        company = job.get("company") if isinstance(job, dict) else getattr(job, "company", None)
        if company:
            company_scores[company] += w
        # Source
        source = job.get("source") if isinstance(job, dict) else getattr(job, "source", None)
        if source:
            source_scores[source] += w
        # Work mode
        work_mode = job.get("work_mode") if isinstance(job, dict) else getattr(job, "work_mode", None)
        if work_mode:
            workmode_scores[work_mode] += w

    total = approved - rejected + selected
    has_data = total != 0

    # Build multipliers. Positive net signal boosts fit & confidence; a
    # strongly negative signal (many rejects) slightly dampens confidence so
    # the user re-scan to recalibrate.
    if has_data:
        # Scale the net signal into a bounded multiplier.
        fit_mult = _clamp(1.0 + _net_ratio(total) * 0.15, MIN_MULT, MAX_MULT)
        confidence_mult = _clamp(1.0 + _net_ratio(total) * 0.10, MIN_MULT, MAX_MULT)
        pref_mult = _clamp(1.0 + _net_ratio(total) * 0.05, MIN_MULT, MAX_MULT)
    else:
        fit_mult = confidence_mult = pref_mult = 1.0

    def top(counter: Counter, n: int = INSIGHT_LIMIT):
        return [item for item, _ in counter.most_common(n)]

    return LearningWeights(
        fit_mult=fit_mult,
        confidence_mult=confidence_mult,
        pref_mult=pref_mult,
        top_skills=top(skill_scores),
        top_companies=top(company_scores),
        top_sources=top(source_scores),
        top_work_modes=top(workmode_scores),
        approved=approved,
        rejected=rejected,
        selected=selected,
        has_data=has_data,
    )


def _net_ratio(total: int) -> float:
    """Map a net signal count to a [-1, 1] ratio, saturating at 5."""
    return max(-1.0, min(1.0, total / 5.0))


def apply_learning_to_assessment(
    assessment: dict,
    weights: LearningWeights,
) -> dict:
    """Fold learning multipliers into an already-computed assessment dict.

    Returns a new assessment dict with ``fit_score`` and ``confidence``
    rescaled by the learning multipliers. The base assessment is left intact;
    this is purely additive on top.
    """
    if weights.fit_mult == 1.0 and weights.confidence_mult == 1.0:
        return assessment

    base_fit = assessment.get("fit_score", 0.0)
    base_conf = assessment.get("confidence", 0.0)
    new_fit = _clamp(base_fit * weights.fit_mult, 0.0, 100.0)
    new_conf = _clamp(base_conf * weights.confidence_mult, 0.0, 1.0)
    out = dict(assessment)
    out["fit_score"] = round(new_fit, 2)
    out["confidence"] = round(new_conf, 4)
    # Record the learning contribution in the breakdown for transparency.
    breakdown = dict(out.get("breakdown") or {})
    breakdown["learning"] = weights.to_dict()
    out["breakdown"] = breakdown
    return out

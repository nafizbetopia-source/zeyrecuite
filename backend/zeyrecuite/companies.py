"""Company ratings and flags.

A curated dataset of well-known remote employers with ratings across several
dimensions (1-5) plus positive flags and warnings. Ratings are indicative
benchmarks for the morning-review dashboard, not live Glassdoor pulls.

For companies not in the dataset we return ``has_data=False`` so the UI shows
an honest "no rating data" state instead of inventing numbers.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Dimensions shown in the UI, in display order.
RATING_DIMENSIONS = [
    ("work_life_balance", "Work-life balance"),
    ("culture", "Culture"),
    ("management", "Management"),
    ("compensation", "Compensation"),
    ("career_growth", "Career growth"),
    ("environment", "Work environment"),
]


@dataclass
class CompanyInfo:
    name: str
    has_data: bool = False
    overall: float | None = None
    ratings: dict[str, float] = field(default_factory=dict)
    flags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    size: str | None = None
    founded: int | None = None
    remote_policy: str | None = None


def _entry(name: str, overall: float, ratings: dict[str, float], flags: list[str],
           warnings: list[str], size: str, founded: int, remote_policy: str) -> dict[str, Any]:
    return {
        "overall": overall, "ratings": ratings, "flags": flags,
        "warnings": warnings, "size": size, "founded": founded, "remote_policy": remote_policy,
    }


# Curated benchmarks. Ratings are 1-5.
_DATASET: dict[str, dict[str, Any]] = {
    "stripe": _entry("Stripe", 4.5,
        {"work_life_balance": 4.2, "culture": 4.6, "management": 4.3, "compensation": 4.6, "career_growth": 4.2, "environment": 4.5},
        ["Remote-first", "Strong benefits", "High compensation"], [], "1000+", 2010, "Remote-first"),
    "datadog": _entry("Datadog", 4.3,
        {"work_life_balance": 4.0, "culture": 4.4, "management": 4.2, "compensation": 4.4, "career_growth": 4.3, "environment": 4.3},
        ["Remote-friendly", "Fast-growing"], ["High pace"], "1000+", 2010, "Remote-friendly"),
    "airtable": _entry("Airtable", 4.2,
        {"work_life_balance": 4.1, "culture": 4.5, "management": 4.0, "compensation": 4.2, "career_growth": 4.1, "environment": 4.2},
        ["Remote-first", "Product-led"], [], "500-1000", 2012, "Remote-first"),
    "figma": _entry("Figma", 4.6,
        {"work_life_balance": 4.4, "culture": 4.7, "management": 4.4, "compensation": 4.6, "career_growth": 4.4, "environment": 4.6},
        ["Remote-first", "Strong benefits"], [], "500-1000", 2012, "Remote-first"),
    "notion": _entry("Notion", 4.4,
        {"work_life_balance": 4.2, "culture": 4.5, "management": 4.3, "compensation": 4.4, "career_growth": 4.3, "environment": 4.4},
        ["Remote-first", "Async culture"], [], "500-1000", 2013, "Remote-first"),
    "linear": _entry("Linear", 4.5,
        {"work_life_balance": 4.3, "culture": 4.6, "management": 4.4, "compensation": 4.5, "career_growth": 4.3, "environment": 4.5},
        ["Remote-first", "Small team"], [], "50-200", 2019, "Remote-first"),
    "github": _entry("GitHub", 4.3,
        {"work_life_balance": 4.1, "culture": 4.4, "management": 4.2, "compensation": 4.3, "career_growth": 4.2, "environment": 4.3},
        ["Remote-friendly", "Microsoft"], [], "1000+", 2008, "Remote-friendly"),
    "shopify": _entry("Shopify", 4.2,
        {"work_life_balance": 4.0, "culture": 4.3, "management": 4.1, "compensation": 4.2, "career_growth": 4.2, "environment": 4.2},
        ["Remote-first", "Scale-up"], ["High pace"], "1000+", 2006, "Remote-first"),
    "canva": _entry("Canva", 4.3,
        {"work_life_balance": 4.1, "culture": 4.4, "management": 4.2, "compensation": 4.2, "career_growth": 4.2, "environment": 4.3},
        ["Remote-first", "Global team"], [], "1000+", 2013, "Remote-first"),
    "duolingo": _entry("Duolingo", 4.2,
        {"work_life_balance": 4.0, "culture": 4.4, "management": 4.1, "compensation": 4.2, "career_growth": 4.2, "environment": 4.2},
        ["Remote-first", "Playful culture"], [], "500-1000", 2011, "Remote-first"),
    "gitlab": _entry("GitLab", 4.4,
        {"work_life_balance": 4.3, "culture": 4.5, "management": 4.3, "compensation": 4.3, "career_growth": 4.3, "environment": 4.4},
        ["Fully remote", "Async-first"], [], "1000+", 2014, "Fully remote"),
    "automattic": _entry("Automattic", 4.3,
        {"work_life_balance": 4.2, "culture": 4.4, "management": 4.2, "compensation": 4.2, "career_growth": 4.2, "environment": 4.3},
        ["Fully remote", "WordPress"], [], "500-1000", 2005, "Fully remote"),
    "toptal": _entry("Toptal", 4.1,
        {"work_life_balance": 4.0, "culture": 4.2, "management": 4.0, "compensation": 4.2, "career_growth": 4.0, "environment": 4.1},
        ["Remote-first", "Talent network"], [], "500-1000", 2015, "Remote-first"),
    "rippling": _entry("Rippling", 4.2,
        {"work_life_balance": 4.0, "culture": 4.3, "management": 4.1, "compensation": 4.3, "career_growth": 4.2, "environment": 4.2},
        ["Remote-friendly", "Fast-growing"], ["High pace"], "500-1000", 2010, "Remote-friendly"),
    "asana": _entry("Asana", 4.1,
        {"work_life_balance": 4.0, "culture": 4.2, "management": 4.0, "compensation": 4.2, "career_growth": 4.1, "environment": 4.1},
        ["Remote-friendly"], [], "500-1000", 2008, "Remote-friendly"),
    "monday.com": _entry("monday.com", 4.2,
        {"work_life_balance": 4.0, "culture": 4.3, "management": 4.1, "compensation": 4.2, "career_growth": 4.2, "environment": 4.2},
        ["Remote-friendly", "Global"], [], "1000+", 2012, "Remote-friendly"),
    "clickup": _entry("ClickUp", 4.1,
        {"work_life_balance": 3.9, "culture": 4.2, "management": 4.0, "compensation": 4.1, "career_growth": 4.1, "environment": 4.1},
        ["Remote-first", "Fast-growing"], ["High pace"], "500-1000", 2017, "Remote-first"),
    "webflow": _entry("Webflow", 4.3,
        {"work_life_balance": 4.2, "culture": 4.4, "management": 4.2, "compensation": 4.3, "career_growth": 4.2, "environment": 4.3},
        ["Remote-first"], [], "50-200", 2013, "Remote-first"),
    "intercom": _entry("Intercom", 4.3,
        {"work_life_balance": 4.2, "culture": 4.4, "management": 4.2, "compensation": 4.3, "career_growth": 4.2, "environment": 4.3},
        ["Remote-first", "Customer-first"], [], "500-1000", 2011, "Remote-first"),
    "retool": _entry("Retool", 4.4,
        {"work_life_balance": 4.3, "culture": 4.5, "management": 4.3, "compensation": 4.4, "career_growth": 4.3, "environment": 4.4},
        ["Remote-first", "Developer tools"], [], "50-200", 2017, "Remote-first"),
    "airbyte": _entry("Airbyte", 4.2,
        {"work_life_balance": 4.1, "culture": 4.3, "management": 4.1, "compensation": 4.2, "career_growth": 4.2, "environment": 4.2},
        ["Remote-first", "Open source"], [], "50-200", 2020, "Remote-first"),
    "hasura": _entry("Hasura", 4.3,
        {"work_life_balance": 4.2, "culture": 4.4, "management": 4.2, "compensation": 4.3, "career_growth": 4.2, "environment": 4.3},
        ["Remote-first", "Open source"], [], "50-200", 2016, "Remote-first"),
    "temporal": _entry("Temporal", 4.4,
        {"work_life_balance": 4.3, "culture": 4.5, "management": 4.3, "compensation": 4.4, "career_growth": 4.3, "environment": 4.4},
        ["Remote-first", "Developer tools"], [], "50-200", 2018, "Remote-first"),
    "hashicorp": _entry("HashiCorp", 4.2,
        {"work_life_balance": 4.0, "culture": 4.3, "management": 4.1, "compensation": 4.3, "career_growth": 4.2, "environment": 4.2},
        ["Remote-friendly", "Developer tools"], [], "1000+", 2012, "Remote-friendly"),
    "mongodb": _entry("MongoDB", 4.1,
        {"work_life_balance": 4.0, "culture": 4.2, "management": 4.0, "compensation": 4.2, "career_growth": 4.1, "environment": 4.1},
        ["Remote-friendly", "Public company"], [], "1000+", 2007, "Remote-friendly"),
    "snowflake": _entry("Snowflake", 4.2,
        {"work_life_balance": 4.0, "culture": 4.3, "management": 4.1, "compensation": 4.4, "career_growth": 4.2, "environment": 4.2},
        ["Remote-friendly", "Public company"], [], "1000+", 2012, "Remote-friendly"),
    "databricks": _entry("Databricks", 4.3,
        {"work_life_balance": 4.1, "culture": 4.4, "management": 4.2, "compensation": 4.4, "career_growth": 4.3, "environment": 4.3},
        ["Remote-friendly", "Data platform"], [], "1000+", 2013, "Remote-friendly"),
    "plaid": _entry("Plaid", 4.3,
        {"work_life_balance": 4.2, "culture": 4.4, "management": 4.2, "compensation": 4.3, "career_growth": 4.2, "environment": 4.3},
        ["Remote-first", "Fintech"], [], "500-1000", 2013, "Remote-first"),
    "brex": _entry("Brex", 4.2,
        {"work_life_balance": 4.0, "culture": 4.3, "management": 4.1, "compensation": 4.3, "career_growth": 4.2, "environment": 4.2},
        ["Remote-first", "Fintech"], ["High pace"], "500-1000", 2016, "Remote-first"),
    "ramp": _entry("Ramp", 4.3,
        {"work_life_balance": 4.1, "culture": 4.4, "management": 4.2, "compensation": 4.3, "career_growth": 4.3, "environment": 4.3},
        ["Remote-first", "Fintech"], [], "500-1000", 2019, "Remote-first"),
}


_LEGAL_SUFFIXES = (
    "technologies", "technology", "systems", "solutions", "software", "labs",
    "lab", "group", "holdings", "inc", "ltd", "llc", "corp", "corporation",
    "company", "co", "plc", "pvt", "limited", "global", "digital",
)


def _normalize_company(name: str) -> str:
    """Lowercase and strip punctuation from a company name.

    Internal dots are preserved (e.g. "monday.com") but leading/trailing dots
    are removed so "stripe, inc." -> "stripeinc".
    """
    return re.sub(r"[^a-z0-9.]", "", (name or "").lower()).strip(".")


def _candidate_keys(name: str) -> list[str]:
    """Build candidate lookup keys, longest/most-specific first."""
    base = _normalize_company(name)
    if not base:
        return []
    candidates = [base]
    parts = [p for p in base.split(".") if p]
    # Drop trailing legal suffixes (e.g. "stripe.inc" -> "stripe").
    while parts and parts[-1] in _LEGAL_SUFFIXES:
        parts.pop()
        candidates.append(".".join(parts))
    # For dot-less names, also try stripping a concatenated trailing suffix
    # (e.g. "stripeinc" -> "stripe"). Only used if it matches the dataset.
    if "." not in base:
        for suf in sorted(_LEGAL_SUFFIXES, key=len, reverse=True):
            if base.endswith(suf) and len(base) > len(suf):
                candidates.append(base[: -len(suf)])
    # De-duplicate, preserving order.
    seen = set()
    out = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def get_company_info(name: str | None) -> CompanyInfo:
    """Return rating/flag info for a company, or an honest no-data record."""
    for key in _candidate_keys(name):
        entry = _DATASET.get(key)
        if entry:
            return CompanyInfo(
                name=name or key,
                has_data=True,
                overall=entry["overall"],
                ratings=dict(entry["ratings"]),
                flags=list(entry["flags"]),
                warnings=list(entry["warnings"]),
                size=entry["size"],
                founded=entry["founded"],
                remote_policy=entry["remote_policy"],
            )
    return CompanyInfo(name=name or "Unknown", has_data=False)


def rating_label(value: float | None) -> str:
    """Map a 1-5 rating to a short human label."""
    if value is None:
        return "N/A"
    if value >= 4.5:
        return "Excellent"
    if value >= 4.0:
        return "Great"
    if value >= 3.5:
        return "Good"
    if value >= 3.0:
        return "Fair"
    return "Low"

"""Deterministic job-origin and applicant-eligibility decisions."""

from dataclasses import dataclass
from enum import Enum
from re import fullmatch
from typing import Iterable


SOUTH_ASIA_COUNTRY_CODES = frozenset({"AF", "BD", "BT", "IN", "LK", "MV", "NP", "PK"})

_COUNTRY_ALIASES = {
    "AFGHANISTAN": "AF",
    "BANGLADESH": "BD",
    "BHUTAN": "BT",
    "INDIA": "IN",
    "MALDIVES": "MV",
    "NEPAL": "NP",
    "PAKISTAN": "PK",
    "SRI LANKA": "LK",
    "UNITED STATES": "US",
    "UNITED STATES OF AMERICA": "US",
    "USA": "US",
    "UNITED KINGDOM": "GB",
    "UK": "GB",
}


class DecisionStatus(Enum):
    ELIGIBLE = "eligible"
    REJECTED = "rejected"
    REVIEW = "review"


@dataclass(frozen=True)
class LocationDecision:
    status: DecisionStatus
    reason: str


def normalize_country_code(value: str | None) -> str | None:
    """Normalize supported country names and ISO alpha-2 codes."""
    if value is None:
        return None

    normalized = " ".join(value.strip().replace(".", " ").split()).upper()
    if not normalized:
        return None

    if normalized in _COUNTRY_ALIASES:
        return _COUNTRY_ALIASES[normalized]
    if fullmatch(r"[A-Z]{2}", normalized):
        return normalized
    return None


def evaluate_location(
    *,
    employer_country: str | None,
    job_country: str | None,
    work_mode: str,
    current_country: str | None,
    worldwide_remote: bool = False,
    allowed_applicant_countries: Iterable[str] | None = None,
) -> LocationDecision:
    """Evaluate origin first, then whether the current user can apply.

    ``worldwide_remote`` must only be true when the source explicitly says the
    role is worldwide. Other remote roles need an explicit applicant-country
    list; missing eligibility data is held for review.
    """
    employer_code = normalize_country_code(employer_country)
    job_code = normalize_country_code(job_country)
    current_code = normalize_country_code(current_country)
    normalized_mode = work_mode.strip().lower()

    # Hard exclusion: reject only when we can CONFIRM a South-Asian origin.
    # An unknown employer origin is not a rejection; for remote jobs eligibility
    # is decided by the posting's candidate-location rules below.
    if employer_code in SOUTH_ASIA_COUNTRY_CODES:
        return LocationDecision(DecisionStatus.REJECTED, "south_asia_employer_origin")
    if job_code in SOUTH_ASIA_COUNTRY_CODES:
        return LocationDecision(DecisionStatus.REJECTED, "south_asia_job_location")

    if normalized_mode not in {"remote", "hybrid", "onsite"}:
        return LocationDecision(DecisionStatus.REVIEW, "work_mode_unknown")
    if current_code is None:
        return LocationDecision(DecisionStatus.REVIEW, "current_location_unknown")

    if normalized_mode != "remote":
        if job_code is None:
            return LocationDecision(DecisionStatus.REVIEW, "job_location_unknown")
        if current_code in SOUTH_ASIA_COUNTRY_CODES:
            return LocationDecision(DecisionStatus.REJECTED, "local_role_in_excluded_country")
        if job_code != current_code:
            return LocationDecision(DecisionStatus.REJECTED, "local_role_outside_current_country")
        return LocationDecision(DecisionStatus.ELIGIBLE, "local_role_in_current_country")

    if allowed_applicant_countries is not None:
        allowed_codes = {normalize_country_code(country) for country in allowed_applicant_countries}
        if None in allowed_codes:
            return LocationDecision(DecisionStatus.REVIEW, "applicant_country_unrecognized")
        if current_code not in allowed_codes:
            return LocationDecision(DecisionStatus.REJECTED, "current_country_not_allowed")
        return LocationDecision(DecisionStatus.ELIGIBLE, "current_country_allowed")

    if worldwide_remote:
        return LocationDecision(DecisionStatus.ELIGIBLE, "worldwide_remote_origin_allowed")
    return LocationDecision(DecisionStatus.REVIEW, "applicant_eligibility_unknown")
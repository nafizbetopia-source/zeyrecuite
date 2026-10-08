"""Deterministic job-origin and applicant-eligibility decisions."""

from dataclasses import dataclass
from enum import Enum
from re import fullmatch
from typing import Iterable


SOUTH_ASIA_COUNTRY_CODES = frozenset({"AF", "BD", "BT", "IN", "LK", "MV", "NP", "PK"})

_COUNTRY_ALIASES = {
    # South Asia — the built-in origin deny set.
    "AFGHANISTAN": "AF",
    "BANGLADESH": "BD",
    "BHUTAN": "BT",
    "INDIA": "IN",
    "MALDIVES": "MV",
    "NEPAL": "NP",
    "PAKISTAN": "PK",
    "SRI LANKA": "LK",
    # English short names / variants.
    "UNITED STATES": "US",
    "UNITED STATES OF AMERICA": "US",
    "USA": "US",
    "UNITED KINGDOM": "GB",
    "UK": "GB",
    # Mirrors adapters._COUNTRY_MAP (keep in sync): sources resolve origins to
    # ISO codes, while config.yaml lists country NAMES — both sides must land on
    # the same code for location.excluded_countries matching to work either way
    # ("Germany" in config vs "DE" from a source, or vice versa).
    "CANADA": "CA",
    "AUSTRALIA": "AU",
    "NEW ZEALAND": "NZ",
    "GERMANY": "DE",
    "FRANCE": "FR",
    "NETHERLANDS": "NL",
    "IRELAND": "IE",
    "SPAIN": "ES",
    "PORTUGAL": "PT",
    "SWEDEN": "SE",
    "SINGAPORE": "SG",
    "UNITED ARAB EMIRATES": "AE",
    "UAE": "AE",
    "ISRAEL": "IL",
    "JAPAN": "JP",
    "SOUTH KOREA": "KR",
    "BRAZIL": "BR",
    "MEXICO": "MX",
    "SOUTH AFRICA": "ZA",
    "NIGERIA": "NG",
    "KENYA": "KE",
    "PHILIPPINES": "PH",
    "INDONESIA": "ID",
    "VIETNAM": "VN",
    "THAILAND": "TH",
    "MALAYSIA": "MY",
    "POLAND": "PL",
    "SWITZERLAND": "CH",
    "AUSTRIA": "AT",
    "BELGIUM": "BE",
    "DENMARK": "DK",
    "FINLAND": "FI",
    "NORWAY": "NO",
    "CZECH REPUBLIC": "CZ",
    "HUNGARY": "HU",
    "ROMANIA": "RO",
    "BULGARIA": "BG",
    "ARGENTINA": "AR",
    "CHILE": "CL",
    "COLOMBIA": "CO",
    "PERU": "PE",
    # Common extras beyond the adapter map (config-side convenience).
    "ITALY": "IT",
    "GREECE": "GR",
    "TURKEY": "TR",
    "RUSSIA": "RU",
    "UKRAINE": "UA",
    "CHINA": "CN",
    "TAIWAN": "TW",
    "HONG KONG": "HK",
    "ESTONIA": "EE",
    "LATVIA": "LV",
    "LITHUANIA": "LT",
    "CROATIA": "HR",
    "SLOVAKIA": "SK",
    "SLOVENIA": "SI",
    "SERBIA": "RS",
    "ICELAND": "IS",
    "LUXEMBOURG": "LU",
    "EGYPT": "EG",
    "MOROCCO": "MA",
    "GHANA": "GH",
    "SAUDI ARABIA": "SA",
    "QATAR": "QA",
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


def _clean_country_text(value: str | None) -> str | None:
    """Lowercased, whitespace/period-normalized display form of a country value.

    Fallback key for deny-list matching: two identically-spelled names that
    :func:`normalize_country_code` cannot resolve to an ISO code still match
    each other exactly (e.g. a rare country name in config vs. the same string
    coming from an import).
    """
    if value is None:
        return None
    text = " ".join(str(value).strip().replace(".", " ").split()).lower()
    return text or None


def evaluate_location(
    *,
    employer_country: str | None,
    job_country: str | None,
    work_mode: str,
    current_country: str | None,
    worldwide_remote: bool = False,
    allowed_applicant_countries: Iterable[str] | None = None,
    excluded_countries: Iterable[str] | None = None,
) -> LocationDecision:
    """Evaluate origin first, then whether the current user can apply.

    ``worldwide_remote`` must only be true when the source explicitly says the
    role is worldwide. Other remote roles need an explicit applicant-country
    list; missing eligibility data is held for review.

    ``excluded_countries`` extends the built-in South-Asia origin deny set with
    the user's configured ``location.excluded_countries`` (config.yaml). Only
    employer/job ORIGIN is checked against it, per the documented policy.
    Entries may be ISO alpha-2 codes or country NAMES: both sides are matched
    on the resolved code (via ``_COUNTRY_ALIASES``) so "Germany" in config
    rejects an origin a source resolved to "DE" and vice versa, with an exact
    cleaned-text fallback for names no alias table can resolve.
    """
    employer_code = normalize_country_code(employer_country)
    job_code = normalize_country_code(job_country)
    current_code = normalize_country_code(current_country)
    normalized_mode = work_mode.strip().lower()

    # Hard exclusion: reject when we can CONFIRM the origin is in the deny set
    # (built-in South-Asia codes + user-configured extras). An unknown employer
    # origin is not a rejection; for remote jobs eligibility is decided by the
    # posting's candidate-location rules below. Matching happens on two levels:
    # the normalized ISO code (cross-form: config name <-> source code) and the
    # exact cleaned text (identical spellings no alias table knows).
    deny_codes = set(SOUTH_ASIA_COUNTRY_CODES)
    deny_names: set[str] = set()
    if excluded_countries:
        for entry in excluded_countries:
            code = normalize_country_code(str(entry))
            if code:
                deny_codes.add(code)
            name = _clean_country_text(str(entry))
            if name:
                deny_names.add(name)

    employer_text = _clean_country_text(employer_country)
    job_text = _clean_country_text(job_country)
    employer_denied = (employer_code is not None and employer_code in deny_codes) or (
        employer_text is not None and employer_text in deny_names
    )
    job_denied = (job_code is not None and job_code in deny_codes) or (
        job_text is not None and job_text in deny_names
    )
    if employer_denied:
        return LocationDecision(DecisionStatus.REJECTED, "south_asia_employer_origin")
    if job_denied:
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
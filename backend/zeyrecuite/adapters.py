"""Source adapters: Remotive public API and Greenhouse public job boards.

Each adapter returns a list of normalized job dicts with a common shape so the
collector can apply the location gate, dedup, and scoring uniformly. Adapters
never raise on a single bad record; they skip it and keep going.

Network access is isolated in ``http_get_json`` so tests can inject a fake
client and run fully offline.
"""
from __future__ import annotations

import json
import re
from typing import Any, Callable

import httpx

USER_AGENT = "ZEYRECUITE/1.0 (personal job-search assistant; contact: local)"

# Country name/alias -> ISO 3166-1 alpha-2. Only the countries we need to
# reason about are listed; anything else resolves to None (unknown).
_COUNTRY_MAP = {
    "afghanistan": "AF", "bangladesh": "BD", "bhutan": "BT", "india": "IN",
    "maldives": "MV", "nepal": "NP", "pakistan": "PK", "sri lanka": "LK",
    "united states": "US", "united states of america": "US", "usa": "US",
    "united kingdom": "GB", "uk": "GB", "canada": "CA", "australia": "AU",
    "new zealand": "NZ", "germany": "DE", "france": "FR", "netherlands": "NL",
    "ireland": "IE", "spain": "ES", "portugal": "PT", "sweden": "SE",
    "singapore": "SG", "united arab emirates": "AE", "uae": "AE",
    "israel": "IL", "japan": "JP", "south korea": "KR", "brazil": "BR",
    "mexico": "MX", "south africa": "ZA", "nigeria": "NG", "kenya": "KE",
    "philippines": "PH", "indonesia": "ID", "vietnam": "VN", "thailand": "TH",
    "malaysia": "MY", "poland": "PL", "switzerland": "CH", "austria": "AT",
    "belgium": "BE", "denmark": "DK", "finland": "FI", "norway": "NO",
    "czech republic": "CZ", "hungary": "HU", "romania": "RO", "bulgaria": "BG",
    "argentina": "AR", "chile": "CL", "colombia": "CO", "peru": "PE",
}

_WORLDWIDE_HINTS = ("worldwide", "anywhere", "global", "remote - worldwide", "remote worldwide")


def http_get_json(url: str, *, client: httpx.Client | None = None, timeout: float = 20.0) -> Any:
    """GET a URL and parse JSON. Raises on HTTP/network errors."""
    own_client = client is None
    http = client or httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=timeout)
    try:
        response = http.get(url)
        response.raise_for_status()
        return response.json()
    finally:
        if own_client:
            http.close()


def http_get_text(url: str, *, client: httpx.Client | None = None, timeout: float = 20.0) -> str:
    """GET a URL and return the response body as text. Raises on HTTP/network errors."""
    own_client = client is None
    http = client or httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=timeout)
    try:
        response = http.get(url)
        response.raise_for_status()
        return response.text
    finally:
        if own_client:
            http.close()


def _remote_board_geo(location: str | None) -> tuple[str | None, bool]:
    """Derive (job_country, worldwide_remote) for a dedicated remote board.

    A remote posting that names a specific country is treated as that country
    (not worldwide); one with no country (e.g. "Remote", "Worldwide") is open
    to remote applicants and flagged worldwide.
    """
    country = normalize_country(location)
    worldwide = is_worldwide(location) or country is None
    return country, worldwide


def normalize_country(value: str | None) -> str | None:
    """Map a free-text location to an ISO alpha-2 code, or None if unknown."""
    if not value:
        return None
    text = re.sub(r"\s+", " ", value.strip().lower())
    if not text:
        return None
    if text in _COUNTRY_MAP:
        return _COUNTRY_MAP[text]
    if re.fullmatch(r"[a-z]{2}", text):
        return text.upper()
    # Try to find a known country name inside a longer string (e.g. "Dhaka, Bangladesh").
    for name, code in _COUNTRY_MAP.items():
        if name in text:
            return code
    return None


def is_worldwide(location: str | None) -> bool:
    if not location:
        return False
    low = location.lower()
    return any(hint in low for hint in _WORLDWIDE_HINTS)


def _split_locations(raw: str | None) -> list[str]:
    if not raw:
        return []
    parts = re.split(r"[,;/|]", raw)
    return [p.strip() for p in parts if p.strip()]


def _html_to_text(html: str) -> str:
    """Convert an HTML job description to clean plain text.

    Handles both real HTML and HTML-escaped content (e.g. ``&lt;h2&gt;``) by
    unescaping entities first, then stripping all tags.
    """
    if not html:
        return ""
    import html as html_module

    text = html_module.unescape(html)
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
    except Exception:  # noqa: BLE001 - fall back to a regex strip
        text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _first_country(locations: list[str]) -> str | None:
    for loc in locations:
        code = normalize_country(loc)
        if code:
            return code
    return None


def _candidate_countries(raw: str | None) -> list[str] | None:
    """Return a list of ISO codes for candidate eligibility, or None if unknown.

    A worldwide/anywhere value yields None (handled via the worldwide flag) so
    the gate can treat it as open rather than an explicit restriction.
    """
    if not raw:
        return None
    if is_worldwide(raw):
        return None
    codes = []
    for loc in _split_locations(raw):
        code = normalize_country(loc)
        if code:
            codes.append(code)
    return codes or None


class BaseAdapter:
    name = "base"

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        raise NotImplementedError


class RemotiveAdapter(BaseAdapter):
    name = "remotive"
    URL = "https://remotive.com/api/remote-jobs?limit=100"

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        data = http_get_json(self.URL, client=client)
        jobs = data.get("jobs", []) if isinstance(data, dict) else []
        out: list[dict[str, Any]] = []
        for job in jobs:
            try:
                out.append(self._normalize(job))
            except Exception:  # noqa: BLE001 - skip a bad record, keep the batch
                continue
        return out

    def _normalize(self, job: dict[str, Any]) -> dict[str, Any]:
        title = str(job.get("title") or "").strip()
        company = str(job.get("company_name") or "").strip()
        url = str(job.get("url") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")
        salary = None
        if salary_min or salary_max:
            salary = f"${salary_min or '?'} - ${salary_max or '?'}"
        candidate_raw = job.get("candidate_required_location")
        job_location = job.get("job_location")
        candidate_codes = _candidate_countries(candidate_raw)
        # Remotive is a dedicated remote board: when a posting states no candidate
        # location restriction, it is open to remote applicants (treat as worldwide).
        worldwide = is_worldwide(candidate_raw) or is_worldwide(job_location) or (candidate_codes is None)
        return {
            "title": title,
            "company": company,
            "location": job.get("job_location") or job.get("candidate_required_location"),
            "work_mode": "remote",
            "employer_country": _first_country(_split_locations(job_location)),
            "job_country": _first_country(_split_locations(job_location)),
            "candidate_required_location": candidate_codes,
            "worldwide_remote": worldwide,
            "salary": salary,
            "description": job.get("description"),
            "skills": _split_locations(job.get("category") or "") + _split_locations(job.get("language") or ""),
            "url": url,
            "source": "remotive",
            "posted_date": job.get("publication_date"),
            "application_url": job.get("url"),
            "application_method": "web",
        }


class GreenhouseAdapter(BaseAdapter):
    name = "greenhouse"
    BOARD_URL = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"

    def __init__(self, boards: list[str]):
        self.boards = [b for b in boards if b]

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for token in self.boards:
            try:
                data = http_get_json(self.BOARD_URL.format(token=token), client=client)
            except Exception:  # noqa: BLE001 - one bad board must not kill the run
                continue
            for job in data.get("jobs", []) if isinstance(data, dict) else []:
                try:
                    out.append(self._normalize(job, token))
                except Exception:  # noqa: BLE001
                    continue
        return out

    def _normalize(self, job: dict[str, Any], token: str) -> dict[str, Any]:
        title = str(job.get("title") or "").strip()
        url = str(job.get("absolute_url") or job.get("apply_url") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = (job.get("location") or {}).get("name")
        company = str(job.get("company_name") or token).strip()
        content = job.get("content") or ""
        text = _html_to_text(content)
        work_mode = "remote" if "remote" in (location or "").lower() else "onsite"
        candidate_codes = _candidate_countries(location)
        # A remote posting with no stated country restriction is open to remote
        # applicants (treat as worldwide). Onsite postings keep their location.
        worldwide = is_worldwide(location) or (work_mode == "remote" and candidate_codes is None)
        return {
            "title": title,
            "company": company,
            "location": location,
            "work_mode": work_mode,
            "employer_country": normalize_country(location),
            "job_country": normalize_country(location),
            "candidate_required_location": candidate_codes,
            "worldwide_remote": worldwide,
            "salary": None,
            "description": text[:4000] or None,
            "skills": [],
            "url": url,
            "source": "greenhouse",
            "posted_date": job.get("updated_at"),
            "application_url": job.get("apply_url") or url,
            "application_method": "web",
        }


# ---------------------------------------------------------------------------
# F15 — additional public job-board adapters.
#
# Each returns the same normalized dict shape as Remotive/Greenhouse so the
# collector applies gate -> dedup -> score -> persist unchanged. Adapters never
# raise on a single bad record (they skip it) and isolate per-board network
# errors so one bad source never kills a run.
# ---------------------------------------------------------------------------


class LeverAdapter(BaseAdapter):
    name = "lever"

    def __init__(self, companies: list[str]):
        self.companies = [c for c in companies if c]

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for slug in self.companies:
            try:
                data = http_get_json(f"https://api.lever.co/v0/postings/{slug}?mode=json", client=client)
            except Exception:  # noqa: BLE001
                continue
            for job in data if isinstance(data, list) else []:
                try:
                    out.append(self._normalize(job, slug))
                except Exception:  # noqa: BLE001
                    continue
        return out

    def _normalize(self, job: dict[str, Any], slug: str) -> dict[str, Any]:
        title = str(job.get("text") or job.get("title") or "").strip()
        url = str(job.get("hostedUrl") or job.get("applyUrl") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("categories", {}).get("location") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company") or slug).strip(),
            "location": location or None,
            "work_mode": "remote" if "remote" in location.lower() else "onsite",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("description") or "")[:4000] or None,
            "skills": [],
            "url": url,
            "source": "lever",
            "posted_date": job.get("createdAt"),
            "application_url": url,
            "application_method": "web",
        }


class AshbyAdapter(BaseAdapter):
    name = "ashby"

    def __init__(self, orgs: list[str]):
        self.orgs = [o for o in orgs if o]

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for org in self.orgs:
            try:
                data = http_get_json(f"https://api.ashbyhq.com/posting-api/job-board/{org}", client=client)
            except Exception:  # noqa: BLE001
                continue
            for job in data.get("jobs", []) if isinstance(data, dict) else []:
                try:
                    out.append(self._normalize(job, org))
                except Exception:  # noqa: BLE001
                    continue
        return out

    def _normalize(self, job: dict[str, Any], org: str) -> dict[str, Any]:
        title = str(job.get("title") or "").strip()
        url = str(job.get("jobUrl") or job.get("applyUrl") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("location") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company") or org).strip(),
            "location": location or None,
            "work_mode": "remote" if "remote" in location.lower() else "onsite",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("description") or "")[:4000] or None,
            "skills": [],
            "url": url,
            "source": "ashby",
            "posted_date": job.get("createdAt"),
            "application_url": url,
            "application_method": "web",
        }


class WorkableAdapter(BaseAdapter):
    name = "workable"

    def __init__(self, accounts: list[str]):
        self.accounts = [a for a in accounts if a]

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for account in self.accounts:
            try:
                data = http_get_json(f"https://apply.workable.com/api/v1/accounts/{account}/jobs", client=client)
            except Exception:  # noqa: BLE001
                continue
            for job in data.get("jobs", []) if isinstance(data, dict) else []:
                try:
                    out.append(self._normalize(job, account))
                except Exception:  # noqa: BLE001
                    continue
        return out

    def _normalize(self, job: dict[str, Any], account: str) -> dict[str, Any]:
        title = str(job.get("title") or "").strip()
        url = str(job.get("url") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("location") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company") or account).strip(),
            "location": location or None,
            "work_mode": "remote" if "remote" in location.lower() else "onsite",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("description") or "")[:4000] or None,
            "skills": [],
            "url": url,
            "source": "workable",
            "posted_date": job.get("publishedAt"),
            "application_url": url,
            "application_method": "web",
        }


class SmartRecruitersAdapter(BaseAdapter):
    name = "smartrecruiters"

    def __init__(self, companies: list[str]):
        self.companies = [c for c in companies if c]

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for company in self.companies:
            try:
                data = http_get_json(f"https://api.smartrecruiters.com/v1/companies/{company}/postings", client=client)
            except Exception:  # noqa: BLE001
                continue
            for job in data.get("items", []) if isinstance(data, dict) else []:
                try:
                    out.append(self._normalize(job, company))
                except Exception:  # noqa: BLE001
                    continue
        return out

    def _normalize(self, job: dict[str, Any], company: str) -> dict[str, Any]:
        title = str(job.get("title") or "").strip()
        url = str(job.get("applyUrl") or job.get("url") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("location") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company") or company).strip(),
            "location": location or None,
            "work_mode": "remote" if "remote" in location.lower() else "onsite",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("description") or "")[:4000] or None,
            "skills": [],
            "url": url,
            "source": "smartrecruiters",
            "posted_date": job.get("publishedAt"),
            "application_url": url,
            "application_method": "web",
        }


class WorkdayAdapter(BaseAdapter):
    name = "workday"

    def __init__(self, tenants: list[str]):
        self.tenants = [t for t in tenants if t]

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for tenant in self.tenants:
            try:
                data = http_get_json(f"https://api.workday.com/gateway/external/{tenant}/jobs", client=client)
            except Exception:  # noqa: BLE001
                continue
            result = data.get("result", {}) if isinstance(data, dict) else {}
            for job in result.get("jobPostingInfo", []) if isinstance(result, dict) else []:
                try:
                    out.append(self._normalize(job, tenant))
                except Exception:  # noqa: BLE001
                    continue
        return out

    def _normalize(self, job: dict[str, Any], tenant: str) -> dict[str, Any]:
        title = str(job.get("jobTitle") or "").strip()
        url = str(job.get("jobPostingUrl") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("location") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company") or tenant).strip(),
            "location": location or None,
            "work_mode": "remote" if "remote" in location.lower() else "onsite",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("jobDescription") or "")[:4000] or None,
            "skills": [],
            "url": url,
            "source": "workday",
            "posted_date": job.get("startDate"),
            "application_url": url,
            "application_method": "web",
        }


class RemoteOKAdapter(BaseAdapter):
    name = "remoteok"
    URL = "https://remoteok.com/api"

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        data = http_get_json(self.URL, client=client)
        out: list[dict[str, Any]] = []
        for job in data if isinstance(data, list) else []:
            try:
                out.append(self._normalize(job))
            except Exception:  # noqa: BLE001
                continue
        return out

    def _normalize(self, job: dict[str, Any]) -> dict[str, Any]:
        title = str(job.get("position") or job.get("title") or "").strip()
        url = str(job.get("url") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("location") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company") or "").strip(),
            "location": location or None,
            "work_mode": "remote",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("description") or "")[:4000] or None,
            "skills": [t for t in (job.get("tags") or []) if isinstance(t, str)],
            "url": url,
            "source": "remoteok",
            "posted_date": job.get("date"),
            "application_url": url,
            "application_method": "web",
        }


class WWRAdapter(BaseAdapter):
    name = "weworkremotely"
    URL = "https://weworkremotely.com/categories/remote-jobs.rss"

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        import xml.etree.ElementTree as ET

        text = http_get_text(self.URL, client=client)
        out: list[dict[str, Any]] = []
        try:
            root = ET.fromstring(text)
        except Exception:  # noqa: BLE001 - malformed feed -> no jobs, no crash
            return out
        for item in root.iter("item"):
            try:
                out.append(self._normalize(item))
            except Exception:  # noqa: BLE001
                continue
        return out

    @staticmethod
    def _text(el, tag: str) -> str:
        node = el.find(tag)
        return (node.text or "").strip() if node is not None and node.text else ""

    def _normalize(self, item) -> dict[str, Any]:
        title = self._text(item, "title")
        url = self._text(item, "link")
        if not title or not url:
            raise ValueError("missing title or url")
        description = _html_to_text(self._text(item, "description"))
        # WWR items don't carry a structured company; derive a best-effort name
        # from the first line of the description if it looks like one.
        company = ""
        first_line = description.split(".")[0].strip()
        if first_line and len(first_line) <= 60:
            company = first_line
        return {
            "title": title,
            "company": company,
            "location": "Remote",
            "work_mode": "remote",
            "employer_country": None,
            "job_country": None,
            "candidate_required_location": None,
            "worldwide_remote": True,
            "salary": None,
            "description": description[:4000] or None,
            "skills": [],
            "url": url,
            "source": "weworkremotely",
            "posted_date": self._text(item, "pubDate") or None,
            "application_url": url,
            "application_method": "web",
        }


class TheMuseAdapter(BaseAdapter):
    name = "themuse"

    def __init__(self, query: str = ""):
        self.query = (query or "").strip()

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        params = {"q": self.query} if self.query else {}
        url = "https://api.themuse.com/api/public/jobs"
        if params:
            url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
        data = http_get_json(url, client=client)
        out: list[dict[str, Any]] = []
        for job in data.get("jobs", []) if isinstance(data, dict) else []:
            try:
                out.append(self._normalize(job))
            except Exception:  # noqa: BLE001
                continue
        return out

    def _normalize(self, job: dict[str, Any]) -> dict[str, Any]:
        title = str(job.get("title") or "").strip()
        url = str(job.get("url") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("location") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company") or "").strip(),
            "location": location or None,
            "work_mode": "remote" if "remote" in location.lower() else "onsite",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("description") or "")[:4000] or None,
            "skills": [],
            "url": url,
            "source": "themuse",
            "posted_date": job.get("published_at"),
            "application_url": url,
            "application_method": "web",
        }


class AdzunaAdapter(BaseAdapter):
    name = "adzuna"

    def __init__(self, api_key: str = "", api_id: str = ""):
        self.api_key = (api_key or "").strip()
        self.api_id = (api_id or "").strip()

    def fetch(self, *, client: httpx.Client | None = None) -> list[dict[str, Any]]:
        if not self.api_key or not self.api_id:
            return []
        url = (
            "https://api.adzuna.com/v1/api/jobs/search/1"
            f"?what=business%20analyst&results_per_page=50&api_key={self.api_key}&api_id={self.api_id}"
        )
        data = http_get_json(url, client=client)
        out: list[dict[str, Any]] = []
        for job in data.get("results", []) if isinstance(data, dict) else []:
            try:
                out.append(self._normalize(job))
            except Exception:  # noqa: BLE001
                continue
        return out

    def _normalize(self, job: dict[str, Any]) -> dict[str, Any]:
        title = str(job.get("title") or "").strip()
        url = str(job.get("redirect_url") or job.get("display_url") or "").strip()
        if not title or not url:
            raise ValueError("missing title or url")
        location = str(job.get("location", {}).get("area") or job.get("location", {}).get("display_name") or "").strip()
        country, worldwide = _remote_board_geo(location)
        return {
            "title": title,
            "company": str(job.get("company", {}).get("display_name") or "").strip(),
            "location": location or None,
            "work_mode": "remote" if "remote" in location.lower() else "onsite",
            "employer_country": country,
            "job_country": country,
            "candidate_required_location": None,
            "worldwide_remote": worldwide,
            "salary": job.get("salary"),
            "description": str(job.get("description") or "")[:4000] or None,
            "skills": [s for s in (job.get("skills") or []) if isinstance(s, str)],
            "url": url,
            "source": "adzuna",
            "posted_date": job.get("created_at"),
            "application_url": url,
            "application_method": "web",
        }


def build_adapters(config) -> list[BaseAdapter]:
    """Instantiate every enabled source.

    Remotive and Greenhouse are driven by ``config.sources`` (legacy behaviour).
    The F15 sources are driven by the JSON registry (``sources.json``); a source
    is only built when it is enabled *and* has the slugs/keys it needs.
    """
    from .registry import load_registry, source_enabled, source_entry

    adapters: list[BaseAdapter] = []
    if config.sources.remotive_enabled:
        adapters.append(RemotiveAdapter())
    if config.sources.greenhouse_enabled and config.sources.greenhouse_boards:
        adapters.append(GreenhouseAdapter(config.sources.greenhouse_boards))

    registry = load_registry()
    if source_enabled(registry, "remoteok"):
        adapters.append(RemoteOKAdapter())
    if source_enabled(registry, "weworkremotely"):
        adapters.append(WWRAdapter())
    if source_enabled(registry, "themuse"):
        adapters.append(TheMuseAdapter(source_entry(registry, "themuse").get("query", "")))
    if source_enabled(registry, "lever") and source_entry(registry, "lever").get("companies"):
        adapters.append(LeverAdapter(source_entry(registry, "lever")["companies"]))
    if source_enabled(registry, "ashby") and source_entry(registry, "ashby").get("orgs"):
        adapters.append(AshbyAdapter(source_entry(registry, "ashby")["orgs"]))
    if source_enabled(registry, "workable") and source_entry(registry, "workable").get("accounts"):
        adapters.append(WorkableAdapter(source_entry(registry, "workable")["accounts"]))
    if source_enabled(registry, "smartrecruiters") and source_entry(registry, "smartrecruiters").get("companies"):
        adapters.append(SmartRecruitersAdapter(source_entry(registry, "smartrecruiters")["companies"]))
    if source_enabled(registry, "workday") and source_entry(registry, "workday").get("tenants"):
        adapters.append(WorkdayAdapter(source_entry(registry, "workday")["tenants"]))
    if source_enabled(registry, "adzuna"):
        entry = source_entry(registry, "adzuna")
        if entry.get("api_key") and entry.get("api_id"):
            adapters.append(AdzunaAdapter(entry["api_key"], entry["api_id"]))
    return adapters

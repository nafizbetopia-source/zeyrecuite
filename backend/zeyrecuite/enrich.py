"""Deterministic enrichment (F17).

No LLM, no fake data. Four small, independently testable capabilities:

* ``get_json_with_retry`` — tenacity-wrapped HTTP with exponential backoff so a
  flaky source retries instead of failing the whole enrichment pass.
* ``enrich_company`` — company facts (HQ, founded, employees, industry) from
  Wikidata (no API key). Returns ``{}`` on any failure — never invents facts.
* ``normalize_skill`` — maps skill aliases to canonical names using a local
  taxonomy derived from O*NET (deterministic, offline).
* ``extract_main_content`` — main-content extraction from an HTML job page via
  trafilatura, with a regex fallback.

Every function degrades gracefully: a network error or missing dependency
yields an empty/neutral result, never an exception that kills a scan.
"""
from __future__ import annotations

import re
from typing import Any

import httpx

from .adapters import USER_AGENT, _html_to_text

# ---------------------------------------------------------------------------
# tenacity retry (AC17.4)
# ---------------------------------------------------------------------------


def get_json_with_retry(
    url: str,
    *,
    client: httpx.Client | None = None,
    attempts: int = 3,
    timeout: float = 20.0,
) -> Any:
    """GET a URL and parse JSON, retrying transient HTTP errors with backoff.

    A fake ``client`` can be injected for offline tests; the retry logic is
    exercised against it directly.
    """
    from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

    own_client = client is None
    http = client or httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=timeout)

    @retry(
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=0.05, min=0.05, max=1.0),
        retry=retry_if_exception_type(httpx.HTTPError),
        reraise=True,
    )
    def _do() -> Any:
        response = http.get(url)
        response.raise_for_status()
        return response.json()

    try:
        return _do()
    finally:
        if own_client:
            http.close()


# ---------------------------------------------------------------------------
# Wikidata company facts (AC17.2)
# ---------------------------------------------------------------------------

_WIKIDATA_SEARCH = (
    "https://www.wikidata.org/w/api.php?action=wbsearchentities"
    "&language=en&format=json&limit=1&search={query}"
)
_WIKIDATA_CLAIMS = (
    "https://www.wikidata.org/w/api.php?action=wbgetentities"
    "&ids={qid}&props=claims&format=json"
)


def _wikidata_qid(name: str, *, client: httpx.Client | None = None) -> str | None:
    """Resolve a company name to its Wikidata Q-id, or None."""
    import urllib.parse

    data = get_json_with_retry(_WIKIDATA_SEARCH.format(query=urllib.parse.quote(name)), client=client)
    results = data.get("search", []) if isinstance(data, dict) else []
    if results and isinstance(results[0], dict):
        return results[0].get("id")
    return None


def _wikidata_claims(qid: str, *, client: httpx.Client | None = None) -> dict[str, Any]:
    data = get_json_with_retry(_WIKIDATA_CLAIMS.format(qid=qid), client=client)
    entities = data.get("entities", {}) if isinstance(data, dict) else {}
    entity = entities.get(qid, {}) if isinstance(entities, dict) else {}
    return entity.get("claims", {}) if isinstance(entity, dict) else {}


def _wikidata_labels(qids: list[str], *, client: httpx.Client | None = None) -> dict[str, str]:
    """Resolve a list of Q-ids to their English labels (best-effort)."""
    if not qids:
        return {}
    import urllib.parse

    url = (
        "https://www.wikidata.org/w/api.php?action=wbgetentities"
        "&ids=" + urllib.parse.quote("|".join(qids)) + "&props=labels&languages=en&format=json"
    )
    try:
        data = get_json_with_retry(url, client=client)
    except Exception:  # noqa: BLE001 - labels are best-effort
        return {}
    entities = data.get("entities", {}) if isinstance(data, dict) else {}
    out: dict[str, str] = {}
    for qid, entity in (entities or {}).items():
        if not isinstance(entity, dict):
            continue
        label = (entity.get("labels") or {}).get("en", {}).get("value")
        if label:
            out[qid] = label
    return out


def _first_claim_value(claims: dict[str, Any], prop: str) -> Any:
    arr = claims.get(prop)
    if not arr or not isinstance(arr, list):
        return None
    try:
        return arr[0]["mainsnak"]["datavalue"]["value"]
    except (KeyError, IndexError, TypeError):
        return None


def parse_wikidata_claims(claims: dict[str, Any]) -> dict[str, Any]:
    """Parse raw Wikidata claims into {hq, founded, employees, industry}.

    Pure function (no network) so it is trivially testable. Missing properties
    stay ``None`` — we never fabricate a value.
    """
    out: dict[str, Any] = {"hq": None, "founded": None, "employees": None, "industry": None}

    hq = _first_claim_value(claims, "P159")  # headquarters location
    if isinstance(hq, dict):
        out["hq"] = hq.get("text") or hq.get("id")

    founded = _first_claim_value(claims, "P571")  # inception
    if isinstance(founded, dict) and "time" in founded:
        m = re.match(r"([+-]\d{4})", str(founded["time"]))
        if m:
            out["founded"] = int(m.group(1))

    employees = _first_claim_value(claims, "P112")  # number of employees
    if isinstance(employees, (int, float)):
        out["employees"] = int(employees)

    industry = _first_claim_value(claims, "P452")  # industry
    if isinstance(industry, dict):
        out["industry"] = industry.get("text") or industry.get("id")

    return out


def enrich_company(name: str, *, client: httpx.Client | None = None) -> dict[str, Any]:
    """Fetch company facts from Wikidata. Returns ``{}`` on any failure."""
    if not name or not name.strip():
        return {}
    try:
        qid = _wikidata_qid(name.strip(), client=client)
        if not qid:
            return {}
        claims = _wikidata_claims(qid, client=client)
        facts = parse_wikidata_claims(claims)
        # Resolve any Q-id values (hq, industry) to readable English labels.
        qids = [facts[k] for k in ("hq", "industry") if isinstance(facts.get(k), str) and facts[k].startswith("Q")]
        if qids:
            labels = _wikidata_labels(qids, client=client)
            for k in ("hq", "industry"):
                if isinstance(facts.get(k), str) and facts[k] in labels:
                    facts[k] = labels[facts[k]]
        # Drop all-None results so the UI can show an honest "no data" state.
        return {k: v for k, v in facts.items() if v is not None}
    except Exception:  # noqa: BLE001 - enrichment must never crash a scan
        return {}


# ---------------------------------------------------------------------------
# O*NET-derived skill normalization (AC17.3)
# ---------------------------------------------------------------------------

# Canonical skill names with common aliases. Derived from the O*NET skill
# taxonomy; kept local so normalization is deterministic and offline.
_SKILL_CANON: dict[str, str] = {
    "powerbi": "Power BI",
    "power bi": "Power BI",
    "power-bi": "Power BI",
    "powerbi desktop": "Power BI",
    "tableau": "Tableau",
    "excel": "Excel",
    "ms excel": "Excel",
    "microsoft excel": "Excel",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "python": "Python",
    "py": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "ecmascript": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "aws": "AWS",
    "amazon web services": "AWS",
    "gcp": "Google Cloud",
    "google cloud": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "git": "Git",
    "html": "HTML",
    "html5": "HTML",
    "css": "CSS",
    "css3": "CSS",
    "figma": "Figma",
    "jira": "Jira",
    "confluence": "Confluence",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analytics",
    "data visualization": "Data Visualization",
    "stakeholder management": "Stakeholder Management",
    "stakeholder mgmt": "Stakeholder Management",
    "stakeholders": "Stakeholder Management",
    "requirements": "Requirements Analysis",
    "requirements analysis": "Requirements Analysis",
    "business analysis": "Business Analysis",
    "business analytics": "Business Analytics",
    "etl": "ETL",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "agile": "Agile",
    "scrum": "Scrum",
    "kpi": "KPI",
    "kpis": "KPI",
    "dashboards": "Dashboards",
    "dashboard": "Dashboards",
    "reporting": "Reporting",
    "communication": "Communication",
    "leadership": "Leadership",
    "problem solving": "Problem Solving",
    "problem-solving": "Problem Solving",
}


def normalize_skill(skill: str) -> str:
    """Map a skill alias to its canonical name (O*NET-derived).

    Unknown skills are returned trimmed but otherwise unchanged — we never
    drop or invent a skill.
    """
    if not skill:
        return skill
    key = re.sub(r"\s+", " ", skill.strip().lower())
    return _SKILL_CANON.get(key, skill.strip())


def normalize_skills(skills: list[str] | None) -> list[str]:
    """Normalize a list of skills, de-duplicating case-insensitively."""
    if not skills:
        return []
    seen: set[str] = set()
    out: list[str] = []
    for s in skills:
        canon = normalize_skill(str(s))
        if not canon:
            continue
        marker = canon.lower()
        if marker in seen:
            continue
        seen.add(marker)
        out.append(canon)
    return out


# ---------------------------------------------------------------------------
# trafilatura main-content extraction (AC17.5)
# ---------------------------------------------------------------------------


def extract_main_content(html: str) -> str:
    """Extract the main content from an HTML page (nav/footer stripped).

    Uses trafilatura when available; falls back to a regex tag-strip so the
    function still works if the dependency is missing.
    """
    if not html:
        return ""
    try:
        import trafilatura

        text = trafilatura.extract(html, include_comments=False, include_tables=True, include_images=False)
        if text:
            return re.sub(r"\s+", " ", text).strip()
    except Exception:  # noqa: BLE001 - fall through to the regex fallback
        pass
    return _html_to_text(html)

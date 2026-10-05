"""Source registry (F15).

A small JSON file maps each optional source to an ``enabled`` flag plus the
slugs/keys that source needs (company slugs for Lever/Ashby/Workable/
SmartRecruiters/Workday, an API key for Adzuna, a search query for The Muse).

The registry is deliberately a plain JSON file (not a DB table) so it is easy
to edit by hand and needs no migration. ``build_adapters`` reads it and
instantiates only the enabled sources, so a source can be turned on/off without
code changes. A missing or malformed registry simply disables every optional
source — it never crashes a scan.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parent.parent / "sources.json"

# Sources that need no slug/key and are safe to enable by default (public,
# no-key remote boards). Company career pages and Adzuna stay disabled until
# the user supplies slugs/keys.
DEFAULT_REGISTRY: dict[str, dict[str, Any]] = {
    "remoteok": {"enabled": True},
    "weworkremotely": {"enabled": True},
    "themuse": {"enabled": True, "query": "business analyst"},
    "lever": {"enabled": False, "companies": []},
    "ashby": {"enabled": False, "orgs": []},
    "workable": {"enabled": False, "accounts": []},
    "smartrecruiters": {"enabled": False, "companies": []},
    "workday": {"enabled": False, "tenants": []},
    "adzuna": {"enabled": False, "api_key": "", "api_id": ""},
}


def load_registry(path: str | Path | None = None) -> dict[str, dict[str, Any]]:
    """Load the registry from ``path`` (default: backend/sources.json).

    Falls back to the built-in defaults when the file is absent, and to an
    empty dict when it is present but unreadable/malformed (fail closed).
    """
    p = Path(path) if path else DEFAULT_REGISTRY_PATH
    if not p.exists():
        return dict(DEFAULT_REGISTRY)
    try:
        with open(p, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:  # noqa: BLE001 - a bad registry must not kill a scan
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def source_enabled(registry: dict[str, dict[str, Any]], name: str) -> bool:
    entry = registry.get(name)
    if not isinstance(entry, dict):
        return False
    return bool(entry.get("enabled", False))


def source_entry(registry: dict[str, dict[str, Any]], name: str) -> dict[str, Any]:
    entry = registry.get(name)
    return entry if isinstance(entry, dict) else {}

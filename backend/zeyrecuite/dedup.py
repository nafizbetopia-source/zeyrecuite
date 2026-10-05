"""Stable fingerprinting and deduplication for job listings."""
from __future__ import annotations

import hashlib
import re
import unicodedata


def _norm(text: str | None) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def fingerprint(title: str, company: str, url: str | None = None) -> str:
    """Build a stable, source-agnostic fingerprint.

    Uses normalized title + company, falling back to the URL when either is
    missing so distinct roles from the same company stay distinct.
    """
    base = f"{_norm(title)}|{_norm(company)}"
    if not base.strip("|"):
        base = _norm(url)
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def is_duplicate(existing: set[str], fp: str) -> bool:
    return fp in existing

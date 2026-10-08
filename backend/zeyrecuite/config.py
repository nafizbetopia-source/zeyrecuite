"""Configuration loading for ZEYRECUITE.

Reads ``config.yaml`` from the backend root (or an explicit path) and merges it
over a safe default. Secrets (API keys) are never required for the MVP: the
Remotive public API is unauthenticated and Greenhouse uses public board tokens.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


@dataclass
class SourceConfig:
    remotive_enabled: bool = True
    greenhouse_enabled: bool = True
    greenhouse_boards: list[str] = field(default_factory=list)
    remotive_polls_per_day: int = 4
    remotive_max_per_minute: int = 2


@dataclass
class LocationConfig:
    current: str = "Bangladesh"
    excluded_countries: list[str] = field(
        default_factory=lambda: [
            "Bangladesh", "India", "Pakistan", "Sri Lanka",
            "Nepal", "Bhutan", "Maldives", "Afghanistan",
        ]
    )
    remote_applicant_policy: str = "allow_worldwide_exclude_south_asian_job_origins"


@dataclass
class SchedulerConfig:
    """F17: automatic periodic scans. Off by default (local-first)."""

    enabled: bool = False
    interval_hours: float = 24.0


@dataclass
class DailyAutoSubmitConfig:
    """Daily auto-submit of the top-scored job. Off by default.

    ``hour``/``minute`` come from the ``daily_auto_submit.at`` "HH:MM" string
    (parsed with a safe fallback) and name the local time of the daily run.
    """

    enabled: bool = False
    hour: int = 9
    minute: int = 0


@dataclass
class WeeklyReportConfig:
    """Weekly Discord progress report (off by default).

    ``day`` is a short weekday name (``mon``..``sun``) and ``hour``/``minute``
    come from the ``weekly_report.at`` "HH:MM" string — the local time of the
    weekly run (default: Sunday 18:00).
    """

    enabled: bool = False
    day: str = "sun"
    hour: int = 18
    minute: int = 0


@dataclass
class AppConfig:
    database_url: str = "sqlite:///./zeyrecuite.db"
    sources: SourceConfig = field(default_factory=SourceConfig)
    location: LocationConfig = field(default_factory=LocationConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    role: str = "Business Analyst"
    min_salary: float | None = None
    daily_cap: int = 10
    resume_path: str | None = None
    data_dir: str = "data"
    # Phase 4: submit through the browser on the company's own site (Playwright)
    # when a direct apply URL exists. False = prepare materials + link only.
    auto_submit: bool = True
    # Daily auto-submit (off by default): top-scored job → Phase 4 pipeline →
    # Discord notice at `daily_auto_submit.at`. See config.yaml.
    daily_auto_submit: DailyAutoSubmitConfig = field(default_factory=DailyAutoSubmitConfig)
    # Auto-apply-only gate (default ON): Playwright cannot submit a job that
    # has no direct application_url, so scans/imports skip such jobs, the jobs
    # API hides them, and legacy link-less rows are purged at startup.
    auto_apply_only: bool = True
    # Weekly Discord progress report (off by default); see config.yaml.
    weekly_report: WeeklyReportConfig = field(default_factory=WeeklyReportConfig)
    # Optional Discord webhook URL for notifications; null/empty disables them.
    discord_webhook_url: str | None = None


def _as_bool(value: Any, default: bool) -> bool:
    """Coerce a YAML value to bool without bool()'s string pitfalls.

    ``bool("false")`` is True in Python, so a quoted ``auto_submit: "false"``
    would silently enable auto-submit. Accept real bools, numbers, and the
    usual yes/no strings; anything else falls back to ``default``.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("true", "yes", "on", "1"):
            return True
        if text in ("false", "no", "off", "0"):
            return False
    return default


def _parse_at(value: Any, default: tuple[int, int] = (9, 0)) -> tuple[int, int]:
    """Parse ``daily_auto_submit.at`` ("HH:MM"); fall back on anything invalid."""
    hour_text, sep, minute_text = str(value or "").strip().partition(":")
    if not sep:
        return default
    try:
        hour, minute = int(hour_text), int(minute_text)
    except ValueError:
        return default
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return default
    return hour, minute


_WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


def _parse_weekday(value: Any, default: str = "sun") -> str:
    """Normalise a YAML weekday to APScheduler's short name (``mon``..``sun``)."""
    text = str(value or "").strip().lower()
    if len(text) >= 3 and text[:3] in _WEEKDAYS:
        return text[:3]
    return default


def _build(data: dict[str, Any]) -> AppConfig:
    src = data.get("sources", {}) or {}
    loc = data.get("location", {}) or {}
    sched = data.get("scheduler", {}) or {}
    daily = data.get("daily_auto_submit", {}) or {}
    hour, minute = _parse_at(daily.get("at"))
    weekly = data.get("weekly_report", {}) or {}
    week_hour, week_minute = _parse_at(weekly.get("at"), default=(18, 0))
    raw_webhook = data.get("discord_webhook_url")
    webhook = str(raw_webhook).strip() if raw_webhook else ""
    # min_salary may arrive quoted ("100"); scoring compares it numerically.
    raw_min_salary = data.get("min_salary")
    if raw_min_salary is None or raw_min_salary == "":
        min_salary: float | None = None
    else:
        try:
            min_salary = float(raw_min_salary)
        except (TypeError, ValueError):
            min_salary = None
    return AppConfig(
        database_url=data.get("database_url", AppConfig.database_url),
        sources=SourceConfig(
            remotive_enabled=_as_bool(src.get("remotive", {}).get("enabled", True), True),
            greenhouse_enabled=_as_bool(src.get("greenhouse", {}).get("enabled", True), True),
            greenhouse_boards=list(src.get("greenhouse", {}).get("boards", []) or []),
            remotive_polls_per_day=int(src.get("remotive", {}).get("polls_per_day", 4)),
            remotive_max_per_minute=int(src.get("remotive", {}).get("max_per_minute", 2)),
        ),
        location=LocationConfig(
            current=str(loc.get("current", "Bangladesh")),
            excluded_countries=list(loc.get("excluded_countries", LocationConfig().excluded_countries)),
            remote_applicant_policy=str(loc.get("remote_applicant_policy", "allow_worldwide_exclude_south_asian_job_origins")),
        ),
        scheduler=SchedulerConfig(
            enabled=_as_bool(sched.get("enabled", False), False),
            interval_hours=float(sched.get("interval_hours", 24.0)),
        ),
        daily_auto_submit=DailyAutoSubmitConfig(
            enabled=_as_bool(daily.get("enabled", False), False),
            hour=hour,
            minute=minute,
        ),
        auto_apply_only=_as_bool(data.get("auto_apply_only", True), True),
        weekly_report=WeeklyReportConfig(
            enabled=_as_bool(weekly.get("enabled", False), False),
            day=_parse_weekday(weekly.get("day")),
            hour=week_hour,
            minute=week_minute,
        ),
        discord_webhook_url=webhook or None,
        role=str(data.get("role", "Business Analyst")),
        min_salary=min_salary,
        daily_cap=int(data.get("daily_cap", 10)),
        resume_path=data.get("resume_path"),
        data_dir=str(data.get("data_dir", "data")),
        auto_submit=_as_bool(data.get("auto_submit", True), True),
    )


def load_config(path: str | Path | None = None) -> AppConfig:
    """Load configuration from ``path`` (default: backend/config.yaml)."""
    cfg_path = Path(path) if path else DEFAULT_CONFIG_PATH
    data: dict[str, Any] = {}
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    return _build(data)


def database_url_for(config: AppConfig) -> str:
    """Resolve the SQLite URL to an absolute path so the DB is stable."""
    url = config.database_url
    if url.startswith("sqlite:///"):
        rel = url[len("sqlite:///"):]
        # In-memory DBs are not filesystem locations: os.path.isabs(":memory:")
        # is False, which would otherwise mangle the URL into
        # ".../backend/:memory:" (an invalid filename on Windows).
        if not rel or rel == ":" + "memory:":
            return url
        if not os.path.isabs(rel):
            base = Path(__file__).resolve().parent.parent
            return "sqlite:///" + str(base / rel).replace("\\", "/")
    return url

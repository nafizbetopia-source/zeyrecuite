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


def _build(data: dict[str, Any]) -> AppConfig:
    src = data.get("sources", {}) or {}
    loc = data.get("location", {}) or {}
    sched = data.get("scheduler", {}) or {}
    return AppConfig(
        database_url=data.get("database_url", AppConfig.database_url),
        sources=SourceConfig(
            remotive_enabled=bool(src.get("remotive", {}).get("enabled", True)),
            greenhouse_enabled=bool(src.get("greenhouse", {}).get("enabled", True)),
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
            enabled=bool(sched.get("enabled", False)),
            interval_hours=float(sched.get("interval_hours", 24.0)),
        ),
        role=str(data.get("role", "Business Analyst")),
        min_salary=data.get("min_salary"),
        daily_cap=int(data.get("daily_cap", 10)),
        resume_path=data.get("resume_path"),
        data_dir=str(data.get("data_dir", "data")),
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
        if not os.path.isabs(rel):
            base = Path(__file__).resolve().parent.parent
            return "sqlite:///" + str(base / rel).replace("\\", "/")
    return url

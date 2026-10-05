"""Background scan scheduler (F17).

Wraps APScheduler's ``BackgroundScheduler`` so the app can run an automatic
``run_all`` on a configurable interval (default: daily). Each scheduled scan
goes through the normal collector, so every run is recorded as a ``ScrapeRun``
row exactly like a manual ``POST /api/scan``.

The scheduler is optional and off by default (``scheduler.enabled``). It is
started/stopped from the app lifespan and is safe to start twice (a no-op if
already running). A scan failure is logged, never raised, so a bad source can
never take down the scheduler thread.
"""
from __future__ import annotations

import logging
from typing import Any, Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .collector import run_all
from .config import AppConfig
from .database import Database

logger = logging.getLogger("zeyrecuite.scheduler")

_JOB_ID = "zeyrecuite-scan"


class ScanScheduler:
    """A thin, testable wrapper around a BackgroundScheduler."""

    def __init__(self, db: Database, config: AppConfig, *, scheduler: BackgroundScheduler | None = None):
        self.db = db
        self.config = config
        self._scheduler = scheduler or BackgroundScheduler(daemon=True)

    @property
    def running(self) -> bool:
        return bool(self._scheduler.running)

    def _scan_job(self) -> None:
        try:
            summaries = run_all(self.db, self.config)
            logger.info("scheduled scan complete: %d source(s)", len(summaries))
        except Exception as exc:  # noqa: BLE001 - never let a scan kill the scheduler
            logger.exception("scheduled scan failed: %s", exc)

    def start(self, interval_hours: float | None = None) -> None:
        """Start the scheduler with a scan on the given interval (default daily)."""
        if self.running:
            return
        hours = interval_hours if interval_hours is not None else self.config.scheduler.interval_hours
        self._scheduler.add_job(
            self._scan_job,
            trigger=IntervalTrigger(hours=hours),
            id=_JOB_ID,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        self._scheduler.start()
        logger.info("scheduler started (scan every %.1fh)", hours)

    def stop(self) -> None:
        if self.running:
            self._scheduler.shutdown(wait=False)
            logger.info("scheduler stopped")

    def status(self) -> dict[str, Any]:
        """Return scheduler state for the API/UI."""
        job = self._scheduler.get_job(_JOB_ID)
        return {
            "enabled": self.config.scheduler.enabled,
            "running": self.running,
            "interval_hours": self.config.scheduler.interval_hours,
            "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None,
        }


def build_scheduler(db: Database, config: AppConfig, *, scheduler: BackgroundScheduler | None = None) -> ScanScheduler:
    return ScanScheduler(db, config, scheduler=scheduler)

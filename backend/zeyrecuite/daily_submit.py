"""Daily auto-submit of the top-scored job (off by default).

Once a day at ``daily_auto_submit.at`` (config.yaml), pick the single best
candidate — the highest ``confidence`` job that passed the location gate, has
a direct apply URL, and is not submitted (or exhausted after 3 attempts) —
approve it, and run the exact Phase 4 pipeline the approve button uses
(``_submit_application`` injected from ``app.py``; this module never imports
the app, so there is no import cycle).

Each run posts one message to ``discord_webhook_url`` when configured: what
was submitted (status, receipt link, proof) or that nothing was submittable
today. The pipeline's safety rails apply unchanged: ``auto_submit`` gate,
``daily_cap`` per UTC day, honest degradation without a working browser.
Failures are logged and reported to Discord, never raised into the scheduler.

Scheduling uses APScheduler's cron trigger (same daemon pattern as
``scheduler.py``): exactly one fire per configured local time while the app
runs — no state file, and a restart cannot double-submit the same day.
"""
from __future__ import annotations

import logging
from typing import Any, Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import func, or_, select

from . import notify
from .config import AppConfig
from .database import Database
from .models import Application, Job

logger = logging.getLogger("zeyrecuite.daily_submit")

_JOB_ID = "zeyrecuite-daily-submit"
# After this many attempts a job stops being a daily candidate — it would
# otherwise hog the top slot forever while degrading to "ready" every day.
_MAX_ATTEMPTS = 3

Submitter = Callable[[Job], dict]


def _done_exists():
    """EXISTS clause: this job was already submitted or exhausted its attempts."""
    return select(Application.id).where(
        Application.job_id == Job.id,
        or_(
            Application.status == "submitted",
            func.coalesce(Application.attempts, 0) >= _MAX_ATTEMPTS,
        ),
    ).exists()


def pick_top_job(session) -> Job | None:
    """Best directly-submittable job today, or None.

    Eligible = not rejected, passed the location gate, has a direct apply URL
    (otherwise nothing can be auto-submitted), and is not already submitted or
    exhausted. Highest match score (``confidence``) wins — the same number the
    UI displays.
    """
    return (
        session.query(Job)
        .filter(Job.status != "rejected")
        .filter(Job.location_status == "eligible")
        .filter(Job.application_url.isnot(None), Job.application_url != "")
        .filter(~_done_exists())
        .order_by(Job.confidence.desc(), Job.id.asc())
        .first()
    )


def pending_count(session) -> int:
    """Eligible jobs still waiting — context for the 'nothing today' note."""
    return (
        session.query(func.count(Job.id))
        .filter(Job.status != "rejected")
        .filter(Job.location_status == "eligible")
        .filter(~_done_exists())
        .scalar()
        or 0
    )


def build_message(report: dict[str, Any]) -> str:
    """Compose the Discord body for one daily run (capped by notify.sanitize)."""
    if report.get("error"):
        return (
            "❌ **ZEYRECUITE daily auto-submit failed**\n"
            f"`{(report.get('error') or 'unknown error')[:300]}`\n"
            "Nothing was submitted — retry or submit manually."
        )
    if report.get("outcome") == "nothing_to_submit":
        pending = report.get("pending", 0)
        return (
            "📭 **ZEYRECUITE daily auto-submit**\n"
            f"No directly submittable job today — {pending} eligible job(s) still "
            "waiting (no direct apply link, or all already submitted)."
        )
    job = report.get("job") or {}
    sub = report.get("submission") or {}
    status = str(sub.get("status") or report.get("outcome") or "unknown")
    icon = "✅" if status == "submitted" else "⚠️"
    lines = [
        f"{icon} **ZEYRECUITE daily auto-submit**",
        f"**{job.get('title') or 'Job'}** — {job.get('company') or 'Unknown company'}",
        f"Match score: {float(job.get('confidence') or 0.0):.0f} · status: **{status}**",
    ]
    if sub.get("submission_method"):
        lines.append(f"Method: {sub['submission_method']}")
    if sub.get("submission_url"):
        lines.append(f"Link: {sub['submission_url']}")
    if sub.get("screenshot"):
        lines.append("📸 Proof screenshot saved.")
    if sub.get("submission_message"):
        lines.append(str(sub["submission_message"])[:400])
    return "\n".join(lines)


def run_daily(
    db: Database,
    config: AppConfig,
    *,
    submitter: Submitter,
    poster: notify.Poster | None = None,
) -> dict[str, Any]:
    """Execute one daily auto-submit run.

    Returns an auditable report and never raises: pick → approve → submit (the
    injected pipeline) → Discord notice, all inside one session so the approved
    job stays attached exactly like the approve endpoint does.
    """
    report: dict[str, Any] = {
        "outcome": None,
        "job": None,
        "submission": None,
        "notified": False,
        "error": None,
    }
    try:
        with db.session() as session:
            job = pick_top_job(session)
            if job is None:
                report["outcome"] = "nothing_to_submit"
                report["pending"] = pending_count(session)
            else:
                # Same as the approve endpoint: the pick is approved first.
                job.status = "approved"
                session.commit()
                report["job"] = {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "confidence": float(job.confidence or 0.0),
                }
                submission = submitter(job)
                report["submission"] = submission if isinstance(submission, dict) else {}
                report["outcome"] = str(report["submission"].get("status") or "unknown")
        report["notified"] = notify.send(
            config.discord_webhook_url, build_message(report), poster=poster
        )
        logger.info(
            "daily auto-submit run complete: outcome=%s job_id=%s notified=%s",
            report["outcome"],
            (report["job"] or {}).get("id"),
            report["notified"],
        )
    except Exception as exc:  # noqa: BLE001 - a bad day must not kill the scheduler
        logger.exception("daily auto-submit failed: %s", exc)
        report["error"] = str(exc)
        report["notified"] = notify.send(
            config.discord_webhook_url, build_message(report), poster=poster
        )
    return report


class DailyAutoSubmit:
    """Daily cron wrapper around :func:`run_daily` (mirrors ``ScanScheduler``)."""

    def __init__(
        self,
        db: Database,
        config: AppConfig,
        *,
        submitter: Submitter,
        scheduler: BackgroundScheduler | None = None,
    ):
        self.db = db
        self.config = config
        self.submitter = submitter
        self._scheduler = scheduler or BackgroundScheduler(daemon=True)

    @property
    def running(self) -> bool:
        return bool(self._scheduler.running)

    def _run(self) -> None:
        try:
            report = run_daily(self.db, self.config, submitter=self.submitter)
            logger.info("scheduled daily auto-submit finished: %s", report.get("outcome"))
        except Exception as exc:  # noqa: BLE001 - run_daily shouldn't raise; belt & braces
            logger.exception("scheduled daily auto-submit failed: %s", exc)

    def start(self) -> None:
        """Start the daily cron (no-op if already running)."""
        if self.running:
            return
        settings = self.config.daily_auto_submit
        self._scheduler.add_job(
            self._run,
            trigger=CronTrigger(hour=settings.hour, minute=settings.minute),
            id=_JOB_ID,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            # A slept-through trigger still counts as today's run for an hour.
            misfire_grace_time=3600,
        )
        self._scheduler.start()
        logger.info("daily auto-submit scheduled at %02d:%02d", settings.hour, settings.minute)

    def stop(self) -> None:
        if self.running:
            self._scheduler.shutdown(wait=False)
            logger.info("daily auto-submit stopped")

    def status(self) -> dict[str, Any]:
        """Report state for the API/UI."""
        job = self._scheduler.get_job(_JOB_ID)
        settings = self.config.daily_auto_submit
        return {
            "enabled": settings.enabled,
            "running": self.running,
            "at": f"{settings.hour:02d}:{settings.minute:02d}",
            "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None,
            "discord_configured": bool(self.config.discord_webhook_url),
        }

    def run_now(self) -> dict[str, Any]:
        """Manual trigger (tests / debugging): one submission cycle immediately."""
        return run_daily(self.db, self.config, submitter=self.submitter)


def build_daily_submitter(
    db: Database,
    config: AppConfig,
    *,
    submitter: Submitter,
    scheduler: BackgroundScheduler | None = None,
) -> DailyAutoSubmit:
    return DailyAutoSubmit(db, config, submitter=submitter, scheduler=scheduler)
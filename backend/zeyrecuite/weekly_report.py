"""Weekly Discord progress report (off by default).

Once a week at ``weekly_report.day`` + ``weekly_report.at`` (config.yaml),
compose a rolling 7-day digest of the job hunt and post it to
``discord_webhook_url`` through :func:`zeyrecuite.notify.send` (which
sanitizes pings and enforces Discord's 2000-character cap):

- applications submitted per UTC day + progress against ``weekly_goal``;
- the top 3 "interview-likely" picks — the highest-confidence jobs that are
  auto-applicable (direct apply URL), still location-eligible, and not yet
  submitted;
- a learning summary (👍 approve / 👎 reject / ⭐ select counts plus the
  skills you like) from the same ``compute_learning_weights`` engine that
  reweights future scans.

Design mirrors ``daily_submit.py``: an APScheduler cron (exactly one fire
per configured local time while the app runs), an injectable ``poster`` so
tests run fully offline, and failures that are logged and reported to
Discord but never raised into the scheduler. This module never imports the
app, so there is no import cycle.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import func, select

from . import notify
from .config import AppConfig
from .database import Database
from .learning import compute_learning_weights
from .models import Application, Feedback, Job, Profile

logger = logging.getLogger("zeyrecuite.weekly_report")

_JOB_ID = "zeyrecuite-weekly-report"
#: Rolling window of the report, in days.
_WINDOW_DAYS = 7
#: How many "interview-likely" picks to surface.
_TOP_PICKS = 3
#: How many liked skills to mention in the Discord message.
_SKILL_LINES = 5


def _aware(ts: datetime | None) -> datetime | None:
    """Treat naive datetimes from SQLite as UTC (same rule as the KPI endpoint)."""
    if ts is None:
        return None
    if ts.tzinfo is None:
        return ts.replace(tzinfo=timezone.utc)
    return ts


def _stage(app_row: Application) -> str:
    """Manual stage wins when set; fall back to the pipeline field."""
    return app_row.application_status or app_row.status or ""


def build_week_report(db: Database, config: AppConfig | None = None) -> dict[str, Any]:
    """Aggregate the rolling 7-day window into a plain, JSON-safe report."""
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(days=_WINDOW_DAYS)
    report: dict[str, Any] = {
        "generated_at": now.isoformat(),
        "window_start": window_start.isoformat(),
        "window_end": now.isoformat(),
        "weekly_goal": None,
        "submitted_this_week": 0,
        "progress": 0.0,
        "by_date": {},
        "top_picks": [],
        "learning": {
            "approve": 0,
            "reject": 0,
            "select": 0,
            "top_skills": [],
            "has_data": False,
        },
        "notified": False,
        "error": None,
    }
    with db.session() as session:
        profile = session.get(Profile, 1)
        report["weekly_goal"] = profile.weekly_goal if profile else None

        # --- Applications submitted inside the window, grouped by UTC date --
        by_date: dict[str, int] = {}
        submitted = 0
        for app_row in session.query(Application).all():
            ts = _aware(app_row.submitted_at)
            if _stage(app_row) != "submitted" or ts is None or ts < window_start:
                continue
            submitted += 1
            key = ts.date().isoformat()
            by_date[key] = by_date.get(key, 0) + 1
        report["submitted_this_week"] = submitted
        report["by_date"] = dict(sorted(by_date.items()))
        goal = report["weekly_goal"]
        if goal:
            report["progress"] = min(round((submitted / goal) * 100, 1), 100.0)

        # --- Top-N "interview-likely" picks (confidence heuristic) ---------
        # Best remaining targets: auto-applicable (direct apply URL), passed
        # the location gate, not rejected, and nobody has submitted them yet
        # — ranked by the same confidence the UI displays.
        already_submitted = select(Application.id).where(
            Application.job_id == Job.id,
            func.coalesce(Application.application_status, Application.status)
            == "submitted",
        ).exists()
        picks = (
            session.query(Job)
            .filter(Job.status != "rejected")
            .filter(Job.location_status == "eligible")
            .filter(Job.application_url.isnot(None), Job.application_url != "")
            .filter(~already_submitted)
            .order_by(Job.confidence.desc(), Job.id.asc())
            .limit(_TOP_PICKS)
            .all()
        )
        report["top_picks"] = [
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "confidence": round(job.confidence or 0.0, 1),
                "confidence_label": job.confidence_label,
            }
            for job in picks
        ]

        # --- Learning signals recorded inside the window -------------------
        week_rows: list[Feedback] = []
        for row in session.query(Feedback).all():
            created = _aware(row.created_at)
            if created is not None and created >= window_start:
                week_rows.append(row)
        learning = report["learning"]
        for row in week_rows:
            if row.signal in ("approve", "reject", "select"):
                learning[row.signal] += 1
        if week_rows:
            jobs_by_id = {j.id: j for j in session.query(Job).all()}
            weights = compute_learning_weights(week_rows, jobs_by_id=jobs_by_id)
            learning["top_skills"] = list(weights.top_skills[:_SKILL_LINES])
            learning["has_data"] = True
    return report


def build_message(report: dict[str, Any]) -> str:
    """Compose the Discord body for one weekly run (capped by notify.sanitize)."""
    if report.get("error"):
        return (
            "❌ **ZEYRECUITE weekly report failed**\n"
            f"`{(report.get('error') or 'unknown error')[:300]}`\n"
            "No digest was built — will retry next week."
        )
    goal = report.get("weekly_goal")
    done = int(report.get("submitted_this_week") or 0)
    lines = ["📊 **ZEYRECUITE weekly report** — last 7 days"]
    if goal:
        lines.append(
            f"**Applications:** {done} submitted · "
            f"goal {done}/{goal} ({report.get('progress') or 0}%)"
        )
    else:
        lines.append(f"**Applications:** {done} submitted (no weekly goal set)")
    by_date = report.get("by_date") or {}
    if by_date:
        lines.append("**By day (UTC):**")
        lines.extend(
            f"• `{day}` — {count}"
            for day, count in list(by_date.items())[:_WINDOW_DAYS]
        )
    else:
        lines.append("No applications submitted this week — keep scanning. 🔍")
    picks = report.get("top_picks") or []
    if picks:
        lines.append("**🎯 Interview-likely next:**")
        for i, pick in enumerate(picks, 1):
            label = pick.get("confidence_label")
            suffix = f" ({label})" if label else ""
            lines.append(
                f"{i}. **{pick.get('title')}** @ {pick.get('company')} — "
                f"{pick.get('confidence')}%{suffix}"
            )
    learning = report.get("learning") or {}
    if learning.get("has_data"):
        skills = ", ".join(learning.get("top_skills") or []) or "—"
        lines.append(
            f"**Learning:** 👍 {learning.get('approve', 0)} · "
            f"👎 {learning.get('reject', 0)} · ⭐ {learning.get('select', 0)} "
            f"— skills you like: {skills}"
        )
    else:
        lines.append(
            "**Learning:** no feedback yet — approve/reject jobs to train your matcher."
        )
    if goal:
        remaining = int(goal) - done
        if remaining <= 0:
            lines.append(f"🏆 Weekly goal met ({done}/{goal}) — great week!")
        else:
            lines.append(f"🏁 {remaining} more to hit the weekly goal.")
    return "\n".join(lines)


def run_weekly(
    db: Database,
    config: AppConfig,
    *,
    poster: notify.Poster | None = None,
) -> dict[str, Any]:
    """Build the report, post it to Discord, and never raise (mirrors run_daily)."""
    report: dict[str, Any] = {"notified": False, "error": None}
    try:
        report = build_week_report(db, config)
        report["notified"] = notify.send(
            config.discord_webhook_url, build_message(report), poster=poster
        )
        logger.info(
            "weekly report run complete: submitted=%s picks=%d notified=%s",
            report.get("submitted_this_week"),
            len(report.get("top_picks") or []),
            report["notified"],
        )
    except Exception as exc:  # noqa: BLE001 - a bad week must not kill the scheduler
        logger.exception("weekly report failed: %s", exc)
        report["error"] = str(exc)
        report["notified"] = notify.send(
            config.discord_webhook_url, build_message(report), poster=poster
        )
    return report


class WeeklyReport:
    """Weekly cron wrapper around :func:`run_weekly` (mirrors ``DailyAutoSubmit``)."""

    def __init__(
        self,
        db: Database,
        config: AppConfig,
        *,
        scheduler: BackgroundScheduler | None = None,
    ):
        self.db = db
        self.config = config
        self._scheduler = scheduler or BackgroundScheduler(daemon=True)

    @property
    def running(self) -> bool:
        return bool(self._scheduler.running)

    def _run(self) -> None:
        try:
            report = run_weekly(self.db, self.config)
            logger.info(
                "scheduled weekly report finished: notified=%s", report.get("notified")
            )
        except Exception as exc:  # noqa: BLE001 - run_weekly shouldn't raise; belt & braces
            logger.exception("scheduled weekly report failed: %s", exc)

    def start(self) -> None:
        """Start the weekly cron (no-op if already running)."""
        if self.running:
            return
        settings = self.config.weekly_report
        self._scheduler.add_job(
            self._run,
            trigger=CronTrigger(
                day_of_week=settings.day,
                hour=settings.hour,
                minute=settings.minute,
            ),
            id=_JOB_ID,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            # A slept-through trigger still counts as this week's run for an hour.
            misfire_grace_time=3600,
        )
        self._scheduler.start()
        logger.info(
            "weekly report scheduled at %s %02d:%02d",
            settings.day,
            settings.hour,
            settings.minute,
        )

    def stop(self) -> None:
        if self.running:
            self._scheduler.shutdown(wait=False)
            logger.info("weekly report stopped")

    def status(self) -> dict[str, Any]:
        """Report state for the API/UI."""
        job = self._scheduler.get_job(_JOB_ID)
        settings = self.config.weekly_report
        return {
            "enabled": settings.enabled,
            "running": self.running,
            "day": settings.day,
            "at": f"{settings.hour:02d}:{settings.minute:02d}",
            "next_run": job.next_run_time.isoformat() if job and job.next_run_time else None,
            "discord_configured": bool(self.config.discord_webhook_url),
        }

    def run_now(self) -> dict[str, Any]:
        """Manual trigger (tests / debugging): one report cycle immediately."""
        return run_weekly(self.db, self.config)


def build_weekly_report(
    db: Database,
    config: AppConfig,
    *,
    scheduler: BackgroundScheduler | None = None,
) -> WeeklyReport:
    return WeeklyReport(db, config, scheduler=scheduler)


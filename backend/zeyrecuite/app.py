"""FastAPI application for ZEYRECUITE.

A local-first, authenticated morning-review dashboard. The SPA (static/index.html)
handles login/logout and all views; this module exposes the JSON API.

Auth: a bearer token (or ``zr_token`` cookie) identifies the user. A default
account (admin) is seeded on first run; its password comes from the
``ZEYRECUITE_ADMIN_PASSWORD`` env var (or a random one-time password logged at
startup) — never a hardcoded credential.
"""
from __future__ import annotations

import csv
import io
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import auth, models, notify  # noqa: F401  (register models)
from .collector import (
    _clean_raw,
    _clean_skills,
    is_auto_applicable,
    purge_unsubmittable_jobs,
    run_all,
)
from .companies import get_company_info
from .config import AppConfig, load_config
from .daily_submit import build_daily_submitter
from .database import build_database
from .dedup import fingerprint
from .enrich import enrich_company, normalize_skills
from .learning import compute_learning_weights
from .models import Application, Feedback, Job, Profile, ScrapeRun, User
from .questions import generate_questions
from .resume import ResumeData, render_pdf, tailor_resume
from .scheduler import build_scheduler
from .scoring import (
    _MUST_HAVE,
    _SYNONYMS,
    _expand,
    _fit_components,
    _salary_value,
    _tokens,
    assess_job,
    confidence,
)
from .weekly_report import build_weekly_report

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR.parent / "data"
# Single dedicated folder for ALL screenshots (proof shots from Playwright).
SCREENSHOTS_DIR = BASE_DIR.parent.parent / "screenshots"

logger = logging.getLogger("zeyrecuite.app")


def _is_valid_score(value: Any) -> bool:
    """True when ``value`` is a usable numeric score (not None/empty/garbage)."""
    if value is None:
        return False
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except (TypeError, ValueError):
            return False
    return False


# ---------- Request schemas (module-level so FastAPI resolves type hints) ----------
class LoginIn(BaseModel):
    username: str
    password: str


class PasswordIn(BaseModel):
    current_password: str
    new_password: str


class SiteProbeIn(BaseModel):
    url: str


class ProfileIn(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin: str | None = None
    website: str | None = None
    github: str | None = None
    current_country: str | None = None
    city: str | None = None
    timezone: str | None = None
    availability: str | None = None
    notice_period: str | None = None
    role: str | None = None
    years_experience: int | None = None
    summary: str | None = None
    skills: list[str] | None = None
    keywords: list[str] | None = None
    languages: list[str] | None = None
    certifications: list[dict] | None = None
    projects: list[dict] | None = None
    interests: list[str] | None = None
    experiences: list[dict] | None = None
    education: list[dict] | None = None
    expected_salary: str | None = None
    min_salary: str | None = None
    work_authorization: str | None = None
    visa_status: str | None = None
    preferred_work_mode: str | None = None
    target_companies: list[str] | None = None
    deal_breakers: list[str] | None = None
    weekly_goal: int | None = None
    kpi_state: dict | None = None
    standard_answers: dict | None = None


def _default_profile() -> Profile:
    """A blank profile. No fake data is seeded — the user fills in real details."""
    return Profile(
        name=None,
        email=None,
        phone=None,
        current_country="Bangladesh",
        role=None,
        summary=None,
        skills=[],
        experiences=[],
        education=[],
        standard_answers={},
    )


def _is_fake_seed(profile: Profile) -> bool:
    """Detect the legacy fake seed so it can be cleared exactly once.

    The fake seed is identified by its placeholder experience ("Company A")
    and/or placeholder identity ("Your Name"). A real user's data will not
    match these markers, so the cleanup only ever fires on seeded data.
    """
    exps = profile.experiences or []
    has_fake_company = any(
        (e or {}).get("company") in ("Company A", "Acme Corp", "Some Company")
        for e in exps
    )
    has_fake_name = profile.name in (None, "", "Your Name")
    return has_fake_company or (has_fake_name and not exps)


def _pct(sorted_vals: list[float], p: float) -> float:
    """Linear-interpolation percentile over an already-sorted list."""
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100.0)
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = k - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


def _blank_profile(profile: Profile) -> None:
    """Clear all profile fields so the user starts from a clean, real slate."""
    for field in (
        "name", "email", "phone", "linkedin", "website", "github",
        "city", "timezone", "availability", "notice_period",
        "years_experience", "summary", "expected_salary", "min_salary",
        "work_authorization", "visa_status", "preferred_work_mode",
    ):
        setattr(profile, field, None)
    profile.role = None
    profile.current_country = None
    profile.skills = []
    profile.keywords = []
    profile.languages = []
    profile.certifications = []
    profile.projects = []
    profile.interests = []
    profile.experiences = []
    profile.education = []
    profile.target_companies = []
    profile.deal_breakers = []
    profile.standard_answers = {}


def create_app(config: AppConfig | None = None) -> FastAPI:
    global DATA_DIR

    config = config or load_config()
    # data_dir (config.yaml): resolve relative paths against the backend root
    # so tailored resumes land wherever the user configured, not a fixed "data".
    _configured_data_dir = Path(config.data_dir)
    DATA_DIR = (
        _configured_data_dir
        if _configured_data_dir.is_absolute()
        else BASE_DIR.parent / _configured_data_dir
    )
    db = build_database(config)
    db.create_all()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        with db.session() as session:
            auth.seed_default_user(session)
            profile = session.get(Profile, 1)
            if profile is None:
                profile = _default_profile()
                session.add(profile)
            elif _is_fake_seed(profile):
                # One-time cleanup: the app previously seeded a fake profile.
                # Clear it so the user works only with their real data.
                _blank_profile(profile)
            if config.resume_path and not profile.resume_path:
                # resume_path (config.yaml): pre-fill the master resume pointer
                # so the app can pre-fill materials without manual upload.
                profile.resume_path = config.resume_path
            session.commit()
        # Auto-apply-only gate: purge legacy jobs Playwright cannot submit
        # (no direct application_url) together with their dependent
        # Feedback/Application rows. Idempotent; no-op when the flag is off.
        if config.auto_apply_only:
            purged = purge_unsubmittable_jobs(db)
            if purged:
                logger.info("purged %d link-less job(s) (auto_apply_only)", purged)
        # F17: start the background scan scheduler if enabled in config.
        scheduler = build_scheduler(db, config)
        app.state.scheduler = scheduler
        if config.scheduler.enabled:
            scheduler.start()
        # Daily auto-submit (off by default): each day pick the top-scored
        # directly-submittable job, run the Phase 4 pipeline, notify Discord.
        # The submitter is injected so this module stays import-cycle free.
        daily = build_daily_submitter(
            db, config, submitter=lambda job: _submit_application(db, job)
        )
        app.state.daily_submit = daily
        if config.daily_auto_submit.enabled:
            daily.start()
        # Weekly Discord progress report (off by default): one 7-day digest
        # per configured local time via the same webhook as daily submit.
        weekly = build_weekly_report(db, config)
        app.state.weekly_report = weekly
        if config.weekly_report.enabled:
            weekly.start()
        yield
        weekly.stop()
        daily.stop()
        scheduler.stop()

    app = FastAPI(title="ZEYRECUITE", version="2.0.0", lifespan=lifespan)
    app.state.db = db
    app.state.config = config
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    # ---------- Auth helpers ----------
    def _token_from_request(request: Request) -> str | None:
        header = request.headers.get("Authorization", "")
        if header.startswith("Bearer "):
            return header[len("Bearer "):].strip()
        return request.cookies.get("zr_token")

    def current_user(request: Request) -> User:
        token = _token_from_request(request)
        with db.session() as session:
            user = auth.get_user_for_token(session, token)
        if not user:
            raise HTTPException(401, "Not authenticated")
        return user

    # ---------- Auth endpoints ----------
    # In-memory failed-login throttle, keyed by username (successes reset it).
    _login_failures: dict[str, list[float]] = {}
    _LOGIN_FAIL_LIMIT = 10
    _LOGIN_FAIL_WINDOW_SECONDS = 300.0

    @app.post("/api/auth/login")
    def login(payload: LoginIn):
        import time as _time

        now = _time.monotonic()
        key = (payload.username or "").strip().lower()
        recent = [t for t in _login_failures.get(key, []) if now - t < _LOGIN_FAIL_WINDOW_SECONDS]
        if len(recent) >= _LOGIN_FAIL_LIMIT:
            raise HTTPException(429, "Too many failed attempts. Try again in a few minutes.")
        with db.session() as session:
            user = auth.authenticate(session, payload.username, payload.password)
            if not user:
                recent.append(now)
                _login_failures[key] = recent
                raise HTTPException(401, "Invalid username or password")
            _login_failures.pop(key, None)
            token = auth.create_session(session, user)
            return {"token": token, "user": {"id": user.id, "username": user.username, "display_name": user.display_name}}

    @app.post("/api/auth/logout")
    def logout(request: Request, user: User = Depends(current_user)):
        token = _token_from_request(request)
        with db.session() as session:
            auth.revoke_session(session, token)
        return {"ok": True}

    @app.get("/api/auth/me")
    def me(user: User = Depends(current_user)):
        return {"user": {"id": user.id, "username": user.username, "display_name": user.display_name}}

    # ---------- Profile ----------
    @app.get("/api/profile")
    def get_profile(user: User = Depends(current_user)):
        with db.session() as session:
            profile = session.get(Profile, 1)
            if not profile:
                raise HTTPException(404, "profile not found")
            return profile.to_dict()

    @app.put("/api/profile")
    def update_profile(payload: ProfileIn, user: User = Depends(current_user)):
        with db.session() as session:
            profile = session.get(Profile, 1)
            if not profile:
                raise HTTPException(404, "profile not found")
            # The client always sends the full profile object, so apply every
            # field (including nulls) to allow clearing values.
            for field_name, value in payload.model_dump().items():
                setattr(profile, field_name, value)
            session.commit()
            return profile.to_dict()

    @app.post("/api/profile/password")
    def change_password(payload: PasswordIn, request: Request, user: User = Depends(current_user)):
        with db.session() as session:
            db_user = session.get(User, user.id)
            if not auth.verify_password(payload.current_password, db_user.password_hash, db_user.password_salt):
                raise HTTPException(400, "Current password is incorrect")
            # Keep *this* session alive; every other token for the user is
            # revoked, so a stolen/lost session dies on password change.
            auth.change_password(
                session,
                db_user,
                payload.new_password,
                keep_token=_token_from_request(request),
            )
        return {"ok": True}

    # ---------- Saved filters (F10) ----------
    @app.get("/api/profile/filters")
    def get_saved_filters(user: User = Depends(current_user)):
        with db.session() as session:
            profile = session.get(Profile, 1)
            return {"filters": (profile.saved_filters if profile else None) or []}

    @app.put("/api/profile/filters")
    def put_saved_filters(payload: dict, user: User = Depends(current_user)):
        filters = (payload or {}).get("filters")
        if not isinstance(filters, list):
            raise HTTPException(422, "filters must be a list")
        if len(filters) > 20:
            raise HTTPException(422, "save at most 20 filters")
        with db.session() as session:
            profile = session.get(Profile, 1)
            if not profile:
                raise HTTPException(404, "profile not found")
            profile.saved_filters = filters
            session.commit()
            return {"filters": profile.saved_filters}

    # ---------- Resume variants (F12) ----------
    @app.get("/api/profile/resume-variants")
    def get_resume_variants(user: User = Depends(current_user)):
        with db.session() as session:
            profile = session.get(Profile, 1)
            return {"variants": (profile.resume_variants if profile else None) or []}

    @app.put("/api/profile/resume-variants")
    def put_resume_variants(payload: dict, user: User = Depends(current_user)):
        variants = (payload or {}).get("variants")
        if not isinstance(variants, list):
            raise HTTPException(422, "variants must be a list")
        if len(variants) > 10:
            raise HTTPException(422, "keep at most 10 variants")
        with db.session() as session:
            profile = session.get(Profile, 1)
            if not profile:
                raise HTTPException(404, "profile not found")
            profile.resume_variants = variants
            session.commit()
            return {"variants": profile.resume_variants}

    # ---------- Application goals / KPI (v2.4) ----------
    @app.get("/api/kpi")
    def kpi_status(user: User = Depends(current_user)):
        """Weekly application goals + progress, derived from the applications table.

        Returns the configured weekly target, how many applications were
        submitted this week, the current streak, and the per-stage breakdown.
        """
        import logging
        logger = logging.getLogger(__name__)
        try:
            from datetime import datetime, timedelta, timezone
            from sqlalchemy import func

            with db.session() as session:
                profile = session.get(Profile, 1)
                weekly_goal = profile.weekly_goal if profile else None

                apps = session.query(Application).all()

                def _stage(a: Application) -> str:
                    # The manual stage wins when set; fall back to the pipeline field.
                    return a.application_status or a.status or ""

                submitted = [a for a in apps if _stage(a) == "submitted" and a.submitted_at]
                now = datetime.now(timezone.utc)
                week_ago = now - timedelta(days=7)

                this_week = 0
                for a in submitted:
                    ts = a.submitted_at
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    if ts >= week_ago:
                        this_week += 1

                # Streak: consecutive calendar days (up to 7) ending today — or
                # yesterday, so a streak survives until the day rolls over —
                # with >= 1 submission. Derived straight from the data so it
                # can never go stale or be wiped by a partial profile update.
                days = set()
                for a in submitted:
                    ts = a.submitted_at
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    days.add(ts.date())
                today = now.date()
                yesterday = today - timedelta(days=1)
                anchor = today if today in days else (yesterday if yesterday in days else None)
                streak = 0
                streak_end = None
                if anchor is not None:
                    day = anchor
                    while day in days and streak < 7:
                        streak += 1
                        day -= timedelta(days=1)
                    streak_end = anchor.isoformat()
                elif days:
                    streak_end = max(days).isoformat()

                stage_col = func.coalesce(Application.application_status, Application.status)
                stages = dict(
                    session.query(stage_col, func.count(Application.id))
                    .group_by(stage_col).all()
                )
                total_apps = len(apps)
                submitted_total = stages.get("submitted", 0)

                progress = round((this_week / weekly_goal) * 100, 1) if weekly_goal else 0.0
                progress = min(progress, 100.0)

                return {
                    "weekly_goal": weekly_goal,
                    "submitted_this_week": this_week,
                    "progress": progress,
                    "streak": streak,
                    "streak_end": streak_end,
                    "stages": stages,
                    "total_apps": total_apps,
                    "submitted_total": submitted_total,
                }
        except Exception as e:
            logger.exception("KPI status error")
            raise HTTPException(status_code=500, detail="failed to load KPI status") from e

    @app.put("/api/kpi")
    def kpi_update(payload: dict, user: User = Depends(current_user)):
        """Persist weekly goal and/or KPI progress state."""
        with db.session() as session:
            profile = session.get(Profile, 1)
            if not profile:
                raise HTTPException(404, "profile not found")

            # Only overwrite fields that are actually present in the payload so
            # a partial update (e.g. just {weekly_goal}) cannot wipe the rest.
            if "weekly_goal" in (payload or {}):
                goal = (payload or {}).get("weekly_goal")
                if goal is not None:
                    try:
                        goal = int(goal)
                    except (TypeError, ValueError):
                        raise HTTPException(422, "weekly_goal must be an integer")
                    if goal < 0:
                        raise HTTPException(422, "weekly_goal must be >= 0")
                profile.weekly_goal = goal

            if "kpi_state" in (payload or {}):
                state = (payload or {}).get("kpi_state")
                if state is not None and not isinstance(state, dict):
                    raise HTTPException(422, "kpi_state must be an object")
                profile.kpi_state = state

            session.commit()
            return {
                "weekly_goal": profile.weekly_goal,
                "kpi_state": profile.kpi_state,
            }

    # ---------- Company intel (v2.4) ----------
    @app.get("/api/company/{company}")
    def company_intel(company: str, user: User = Depends(current_user)):
        """Aggregate everything known about a company into one research panel.

        Combines jobs, salary range, sources, application statuses, and
        enrichment facts for the given company name.
        """
        from sqlalchemy import func

        with db.session() as session:
            rows = (
                session.query(Job)
                .filter(func.lower(Job.company) == func.lower(company))
                .all()
            )
            # Batch-load applications once — a per-job query here was an N+1
            # (and referenced the session after it had already been closed).
            app_by_job = {a.job_id: a for a in session.query(Application).all()}

            jobs = []
            salaries = []
            sources: dict[str, int] = {}
            stages: dict[str, int] = {}
            for j in rows:
                jobs.append(_list_item(j, app_record=app_by_job.get(j.id)))
                sources[j.source] = sources.get(j.source, 0) + 1
                v = _salary_value(j.salary)
                if v is not None:
                    salaries.append(v)
                app = app_by_job.get(j.id)
                if app:
                    stage = app.application_status or app.status
                    stages[stage] = stages.get(stage, 0) + 1

        info = get_company_info(company)
        facts = {
            "name": info.name,
            "has_data": info.has_data,
            "overall": info.overall,
            "ratings": info.ratings,
            "flags": info.flags,
            "warnings": info.warnings,
            "size": info.size,
            "founded": info.founded,
            "remote_policy": info.remote_policy,
        }

        salary_range = None
        if salaries:
            sv = sorted(salaries)
            salary_range = {
                "min": round(sv[0], 1),
                "median": round(_pct(sv, 50), 1),
                "max": round(sv[-1], 1),
                "count": len(sv),
            }

        return {
            "company": company,
            "job_count": len(jobs),
            "jobs": jobs,
            "sources": sources,
            "application_stages": stages,
            "salary_range": salary_range,
            "company_info": facts,
        }

    # ---------- Scan ----------
    @app.post("/api/scan")
    def scan(user: User = Depends(current_user)):
        summaries = run_all(db, config)
        prepared = _auto_generate_top(db, limit=10)
        return {"runs": [s.__dict__ for s in summaries], "prepared_top": prepared}

    # ---------- Weekly Discord report (opt-in) ----------
    @app.get("/api/weekly-report/status")
    def weekly_report_status(user: User = Depends(current_user)):
        """Schedule/state of the weekly Discord report cron."""
        return app.state.weekly_report.status()

    @app.post("/api/weekly-report/run")
    def weekly_report_run(user: User = Depends(current_user)):
        """Build + send one weekly report immediately (debugging / manual runs)."""
        return app.state.weekly_report.run_now()

    # ---------- F17: scheduler + enrichment ----------
    @app.get("/api/scheduler")
    def scheduler_status(user: User = Depends(current_user)):
        """Report the background scan scheduler state (F17)."""
        return app.state.scheduler.status()

    @app.post("/api/notifications/discord/test")
    def discord_test(user: User = Depends(current_user)):
        """Send a one-off test message to the configured Discord webhook."""
        url = config.discord_webhook_url
        if not url:
            raise HTTPException(409, "discord_webhook_url is not set in config.yaml")
        if not notify.send(url, "ZEYRECUITE test message — notifications are working ✅"):
            raise HTTPException(502, "Discord webhook rejected the message (check the URL)")
        return {"sent": True}

    @app.get("/api/sources")
    def sources_registry(user: User = Depends(current_user)):
        """List the source registry (F15): which sources are enabled and their config."""
        from .registry import load_registry

        registry = load_registry()
        return {"sources": registry}

    @app.post("/api/enrich")
    def enrich_jobs(limit: int = 0, user: User = Depends(current_user)):
        """Enrich jobs with company facts (Wikidata) and normalized skills (F17).

        Deterministic and offline-safe: a company with no Wikidata match simply
        keeps no facts. Each unique company is fetched at most once per call
        (cached), and ``limit`` bounds how many jobs are processed (0 = all).
        Returns how many jobs were touched.
        """
        enriched = 0
        facts_cache: dict[str, dict] = {}
        with db.session() as session:
            q = session.query(Job)
            if limit > 0:
                q = q.limit(limit)
            for job in q.all():
                changed = False
                if job.company and not job.company_facts:
                    key = job.company.strip().lower()
                    if key not in facts_cache:
                        facts_cache[key] = enrich_company(job.company)
                    facts = facts_cache[key]
                    if facts:
                        job.company_facts = facts
                        changed = True
                if job.skills:
                    normalized = normalize_skills(job.skills)
                    if normalized != list(job.skills):
                        job.skills = normalized
                        changed = True
                if changed:
                    enriched += 1
            session.commit()
        return {"enriched": enriched}

    @app.post("/api/rescore")
    def rescore(user: User = Depends(current_user)):
        """Recompute the full assessment for every job using the current profile.

        Useful after editing the profile (skills, country, salary floor) so the
        confidence, eligibility, and rankings reflect the latest inputs.
        """
        with db.session() as session:
            profile = session.get(Profile, 1)
            profile_skills = list(profile.skills or []) if profile else []
            jobs = session.query(Job).all()
            job_map = {j.id: j for j in jobs}
            # Compute additive learning multipliers from feedback history so a
            # re-score reflects what the user has approved / rejected / selected.
            feedback_rows = session.query(Feedback).all()
            learning = (
                compute_learning_weights(feedback_rows, jobs_by_id=job_map)
                if feedback_rows
                else None
            )
            updated = 0
            for job in jobs:
                company_overall = get_company_info(job.company).overall
                assessment = assess_job(
                    title=job.title,
                    description=job.description,
                    job_skills=job.skills,
                    profile_skills=profile_skills,
                    target_role=config.role,
                    location_status=job.location_status,
                    work_mode=job.work_mode,
                    salary=job.salary,
                    min_salary=config.min_salary,
                    company_overall=company_overall,
                    posted_date=job.posted_date,
                    application_url=job.application_url,
                    preferred_remote=True,
                    learning=learning,
                )
                job.score = assessment.fit_score
                job.score_breakdown = assessment.breakdown
                job.confidence = assessment.confidence
                job.confidence_label = assessment.confidence_label
                job.eligibility = assessment.eligibility
                job.eligibility_label = assessment.eligibility_label
                job.confidence_breakdown = {
                    "factors": [
                        {"key": f.key, "label": f.label, "value": f.value,
                         "weight": f.weight, "detail": f.detail}
                        for f in assessment.factors
                    ],
                    "matched_skills": assessment.matched_skills,
                    "missing_skills": assessment.missing_skills,
                    "must_have_present": assessment.must_have_present,
                    "must_have_missing": assessment.must_have_missing,
                    "reasons": assessment.reasons,
                }
                updated += 1
            session.commit()
        # The profile may have changed, so regenerate the top-10 materials to
        # reflect the latest real data.
        prepared = _auto_generate_top(db, limit=10, force=True)
        return {"rescored": updated, "prepared_top": prepared}

    # ---------- Learning loop (F19) ----------
    @app.post("/api/jobs/{job_id}/feedback")
    def submit_feedback(job_id: int, body: dict, user: User = Depends(current_user)):
        """Record an approve / reject / select signal on a job.

        The signal feeds the learning loop: feedback is aggregated into skill /
        company / source / work-mode preferences and applied as additive
        reweights on every subsequent scan and re-score.
        """
        with db.session() as session:
            job = session.get(Job, job_id)
            if job is None:
                raise HTTPException(status_code=404, detail="Job not found")
            signal = (body.get("signal") or "").lower()
            if signal not in ("approve", "reject", "select"):
                raise HTTPException(
                    status_code=422,
                    detail="signal must be one of: approve, reject, select",
                )
            # Upsert: exactly one feedback row per job (unique index
            # uq_feedback_job_id). Re-sending a signal — double-click, changed
            # mind, corrected mistake — updates the existing row instead of
            # appending duplicates that would double-count in
            # compute_learning_weights and inflate the insights totals.
            feedback = session.query(Feedback).filter(Feedback.job_id == job_id).first()
            if feedback is None:
                feedback = Feedback(
                    job_id=job_id,
                    signal=signal,
                    source=body.get("source", "manual"),
                )
                session.add(feedback)
            else:
                feedback.signal = signal
                feedback.source = body.get("source", "manual")
            session.commit()

            learning = compute_learning_weights(
                session.query(Feedback).all(),
                jobs_by_id={j.id: j for j in session.query(Job).all()},
            )
            return {
                "recorded": signal,
                "job_id": job_id,
                "learning": learning.to_dict(),
            }

    @app.delete("/api/jobs/{job_id}/feedback")
    def delete_feedback(job_id: int, user: User = Depends(current_user)):
        """Remove the recorded signal for a job (lets the user correct mistakes)."""
        with db.session() as session:
            removed = (
                session.query(Feedback)
                .filter(Feedback.job_id == job_id)
                .delete(synchronize_session=False)
            )
            session.commit()
            return {"removed": removed, "job_id": job_id}

    @app.get("/api/learning/insights")
    def learning_insights(user: User = Depends(current_user)):
        """Return the current learning state and derived preferences.

        Surfaced on the Search / Learn view so the user can see what the app
        has learned from their approve / reject / select history.
        """
        with db.session() as session:
            feedback_rows = session.query(Feedback).all()
            if not feedback_rows:
                return {
                    "has_data": False,
                    "approved": 0,
                    "rejected": 0,
                    "selected": 0,
                    "top_skills": [],
                    "top_companies": [],
                    "top_sources": [],
                    "top_work_modes": [],
                    "fit_mult": 1.0,
                    "confidence_mult": 1.0,
                    "pref_mult": 1.0,
                }
            job_map = {j.id: j for j in session.query(Job).all()}
            learning = compute_learning_weights(feedback_rows, jobs_by_id=job_map)
            return learning.to_dict()

    # ---------- Enrichment ----------
    def _company_payload(job: Job) -> dict:
        info = get_company_info(job.company)
        return {
            "name": info.name,
            "has_data": info.has_data,
            "overall": info.overall,
            "ratings": info.ratings,
            "flags": info.flags,
            "warnings": info.warnings,
            "size": info.size,
            "founded": info.founded,
            "remote_policy": info.remote_policy,
        }

    def _list_item(job: Job, materials: set | None = None, app_record=None) -> dict:
        info = get_company_info(job.company)
        item = job.to_dict()
        item["company_overall"] = info.overall if info.has_data else None
        item["company_has_data"] = info.has_data
        item["company_flags"] = info.flags[:2]
        item["materials_ready"] = bool(materials and job.id in materials)
        # Application dates for the Applications view (starting / last / submission).
        if app_record:
            item["app_start"] = app_record.created_at.isoformat() if app_record.created_at else None
            item["app_last"] = app_record.last_attempt_at.isoformat() if app_record.last_attempt_at else (app_record.updated_at.isoformat() if app_record.updated_at else None)
            item["app_submitted"] = app_record.submitted_at.isoformat() if app_record.submitted_at else None
        else:
            item["app_start"] = item.get("created_at")
            item["app_last"] = item.get("created_at")
            item["app_submitted"] = None
        return item

    def _detail(job: Job) -> dict:
        info = get_company_info(job.company)
        item = job.to_dict()
        item["company_info"] = _company_payload(job)
        item["questions"] = generate_questions(job.title, job.description, job.skills)
        with db.session() as session:
            app_record = session.query(Application).filter(Application.job_id == job.id).first()
            item["application"] = app_record.to_dict() if app_record else None
        return item

    # ---------- Side-by-side comparison (F7) ----------
    # NOTE: registered before /api/jobs/{job_id} so "compare" is not captured
    # as a job id.
    @app.get("/api/jobs/compare")
    def compare_jobs(ids: str = "", user: User = Depends(current_user)):
        """Normalize 2-5 jobs for side-by-side comparison with winner highlights."""
        id_list = [int(x) for x in ids.split(",") if x.strip().isdigit()]
        if not id_list:
            raise HTTPException(422, "provide at least one job id (ids=1,2,3)")
        if len(id_list) > 5:
            raise HTTPException(422, "compare at most 5 jobs")

        with db.session() as session:
            jobs = [session.get(Job, i) for i in id_list]
            jobs = [j for j in jobs if j is not None]

        rows = []
        for job in jobs:
            cb = job.confidence_breakdown or {}
            factors = {f["key"]: f["value"] for f in (cb.get("factors") or [])}
            info = get_company_info(job.company)
            rows.append({
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "salary": job.salary,
                "salary_value": _salary_value(job.salary),
                "confidence": job.confidence,
                "factors": factors,
                "eligibility": job.eligibility,
                "work_mode": job.work_mode,
                "company_overall": info.overall if info.has_data else None,
                "matched_skills": cb.get("matched_skills") or [],
                "missing_skills": cb.get("missing_skills") or [],
                "posted_date": job.posted_date,
                "application_method": job.application_method,
            })

        def _best(key, reverse=True):
            vals = []
            for r in rows:
                v = key(r) if callable(key) else r.get(key)
                if v is not None:
                    vals.append((v, r["id"]))
            if not vals:
                return None
            vals.sort(reverse=reverse)
            return vals[0][1]

        best = {
            "confidence": _best("confidence"),
            "eligibility": _best("eligibility"),
            "salary": _best("salary_value"),
            "company": _best("company_overall"),
            # Fewest missing skills is best — compare by count, not by the
            # lexicographic ordering of the skill list itself.
            "skills": _best(lambda r: len(r["missing_skills"] or []), reverse=False),
        }
        return {"jobs": rows, "best": best}

    # ---------- Jobs ----------
    @app.get("/api/jobs")
    def list_jobs(status: str | None = None, user: User = Depends(current_user)):
        from sqlalchemy import case

        with db.session() as session:
            query = session.query(Job)
            if config.auto_apply_only:
                # Mirror collector.is_auto_applicable: only jobs Playwright
                # can submit (non-empty application_url) are listed. This feeds
                # the Jobs, Search, and Top-10 views that read this endpoint.
                query = query.filter(
                    Job.application_url.isnot(None), Job.application_url != ""
                )
            if status:
                query = query.filter(Job.status == status)
            status_rank = case(
                (Job.status == "new", 0),
                (Job.status == "review", 1),
                (Job.status == "approved", 2),
                else_=3,
            )
            jobs = query.order_by(status_rank.asc(), Job.score.desc()).all()
            # Batch-fetch all application records in one query instead of one
            # session per job (avoids an N+1 query across hundreds of jobs).
            app_records = {r.job_id: r for r in session.query(Application).all()}
            return [_list_item(j, app_record=app_records.get(j.id)) for j in jobs]

    @app.get("/api/jobs/{job_id}")
    def get_job(job_id: int, user: User = Depends(current_user)):
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            return _detail(job)

    @app.post("/api/jobs/{job_id}/reject")
    def reject_job(job_id: int, user: User = Depends(current_user)):
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            job.status = "rejected"
            session.commit()
            return _detail(job)

    @app.post("/api/jobs/{job_id}/approve")
    def approve_job(job_id: int, user: User = Depends(current_user)):
        """Approve a job and kick off the submission pipeline."""
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            job.status = "approved"
            session.commit()
            result = _submit_application(db, job)
        return {"job": _detail(job), "submission": result}

    @app.post("/api/jobs/{job_id}/resubmit")
    def resubmit_job(job_id: int, user: User = Depends(current_user)):
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            result = _submit_application(db, job)
        return {"job": _detail(job), "submission": result}

    # ---------- Submit application (F19) ----------
    @app.post("/api/jobs/{job_id}/submit")
    def submit_application(job_id: int, user: User = Depends(current_user)):
        """Run the submission pipeline for a job from the Search & Submit view.

        Prepares the tailored resume + cover letter, records a verifiable
        submission record, and returns the status plus any direct apply link
        so the UI can open the employer's application page. The MVP never
        auto-fills third-party ATS forms.
        """
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            result = _submit_application(db, job)
        return {"job": _detail(job), "submission": result}

    # ---------- Resume scorecard (F2) ----------
    @app.get("/api/jobs/{job_id}/scorecard")
    def job_scorecard(job_id: int, user: User = Depends(current_user)):
        """Per-job resume fit: coverage, matched skills, and the resume gap.

        The *resume gap* is the actionable list: skills the job asks for that are
        absent from BOTH the profile skills and the resume text.
        """
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            profile = session.get(Profile, 1)
            profile_skills = list(profile.skills or []) if profile else []
            resume_text = (profile.resume_text or "") if profile else ""

        c = _fit_components(
            title=job.title,
            description=job.description,
            job_skills=job.skills,
            profile_skills=profile_skills,
            target_role=config.role,
        )
        job_expanded = c["job_expanded"]
        profile_expanded = c["profile_expanded"]
        matched = c["matched"]

        coverage = (
            round(len(job_expanded & profile_expanded) / len(job_expanded) * 100, 1)
            if job_expanded else 50.0
        )

        matched_skills = [
            {"skill": s, "core": s in _MUST_HAVE} for s in sorted(matched)
        ]

        # Resume gap: job skills not covered by profile AND not in resume text.
        resume_tokens = _tokens(resume_text)
        resume_gap = sorted(
            s for s in (job_expanded - profile_expanded)
            if s not in resume_tokens and s not in _SYNONYMS
        )

        suggestions: list[str] = []
        for s in resume_gap:
            if s in _MUST_HAVE:
                suggestions.append(f"Add '{s}' to your resume — it's a core skill for this role.")
        for s in resume_gap:
            if s not in _MUST_HAVE:
                suggestions.append(f"Consider adding '{s}' to strengthen your fit.")
        suggestions = suggestions[:5]

        return {
            "coverage_pct": coverage,
            "matched_skills": matched_skills,
            "missing_skills": c["missing"],
            "resume_gap": resume_gap,
            "suggestions": suggestions,
        }

    # ---------- Kanban status move (F6) ----------
    _JOB_STATUSES = {"new", "review", "approved", "rejected"}

    @app.post("/api/jobs/{job_id}/status")
    def set_job_status(job_id: int, payload: dict, user: User = Depends(current_user)):
        """Move a job to any pipeline lane (Kanban drag-and-drop)."""
        status = (payload or {}).get("status")
        if status not in _JOB_STATUSES:
            raise HTTPException(422, f"invalid status; must be one of {sorted(_JOB_STATUSES)}")
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            job.status = status
            session.commit()
            return _detail(job)

    # ---------- Manual application status (no email connected) ----------
    _APPLICATION_STATUSES = {"draft", "ready", "submitting", "submitted", "failed"}

    @app.post("/api/jobs/{job_id}/application-status")
    def set_application_status(job_id: int, payload: dict, user: User = Depends(current_user)):
        """Manually move an application through its stages.

        Used when no email is connected so the user can still track where each
        application stands: draft → ready → submitting → submitted | failed.
        """
        from datetime import datetime, timezone

        status = (payload or {}).get("status")
        if status not in _APPLICATION_STATUSES:
            raise HTTPException(422, f"invalid status; must be one of {sorted(_APPLICATION_STATUSES)}")
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            app_record = session.query(Application).filter(Application.job_id == job_id).first()
            if not app_record:
                app_record = Application(job_id=job_id, status="draft")
                session.add(app_record)
            app_record.application_status = status
            if status == "submitted" and not app_record.submitted_at:
                # KPI/streak/analytics count submissions by submitted_at, so a
                # manual move to "submitted" must stamp it too.
                app_record.submitted_at = datetime.now(timezone.utc)
            session.commit()
            return _detail(job)

    # ---------- Application timeline (F8) ----------
    @app.get("/api/jobs/{job_id}/timeline")
    def job_timeline(job_id: int, user: User = Depends(current_user)):
        """Ordered event history for a job's application (derived, no new table)."""
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            app_record = session.query(Application).filter(Application.job_id == job.id).first()

        events = []
        if job.created_at:
            events.append({"type": "created", "at": job.created_at.isoformat(),
                           "label": "Job discovered"})
        if app_record:
            if app_record.created_at:
                events.append({"type": "materials", "at": app_record.created_at.isoformat(),
                               "label": "Application package created"})
            if app_record.resume_pdf_path and app_record.updated_at:
                events.append({"type": "ready", "at": app_record.updated_at.isoformat(),
                               "label": "Package ready"})
            if app_record.last_attempt_at:
                events.append({"type": "attempt", "at": app_record.last_attempt_at.isoformat(),
                               "label": f"Submission attempt #{app_record.attempts or 1}"})
            if app_record.submitted_at:
                events.append({"type": "submitted", "at": app_record.submitted_at.isoformat(),
                               "label": "Submitted"})
            if app_record.submission_status == "failed":
                events.append({"type": "failed", "at": (app_record.last_attempt_at or app_record.updated_at).isoformat(),
                               "label": "Submission failed"})
        events.sort(key=lambda e: e["at"])
        return {"events": events}

    # ---------- Follow-up email (F9) ----------
    @app.get("/api/jobs/{job_id}/followup")
    def job_followup(job_id: int, user: User = Depends(current_user)):
        """Deterministic follow-up email for a submitted application."""
        from datetime import datetime, timezone

        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            app_record = session.query(Application).filter(Application.job_id == job.id).first()
            profile = session.get(Profile, 1)
            if not app_record or not app_record.submitted_at:
                raise HTTPException(409, "no submitted application to follow up on")

        name = (profile.name if profile else None) or "there"
        submitted = app_record.submitted_at
        if submitted.tzinfo is None:
            submitted = submitted.replace(tzinfo=timezone.utc)
        days = max(0, (datetime.now(timezone.utc) - submitted).days)

        subject = f"Following up — {job.title} at {job.company}"
        body = (
            f"Hi,\n\n"
            f"I applied for the {job.title} role at {job.company} {days} day"
            f"{'s' if days != 1 else ''} ago and wanted to reiterate my strong "
            f"interest in the position.\n\n"
            f"I'm confident my background in business analysis and data "
            f"analytics would be a great fit for your team, and I'd welcome the "
            f"chance to discuss how I can contribute.\n\n"
            f"Thank you for your time and consideration.\n\n"
            f"Best regards,\n{name}"
        )
        return {"subject": subject, "body": body, "days_since": days}

    # ---------- Application artifacts ----------
    @app.post("/api/jobs/{job_id}/generate")
    def generate(job_id: int, variant: str | None = None, user: User = Depends(current_user)):
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            if session.get(Profile, 1) is None:
                raise HTTPException(404, "profile not found")
        # force=True so the resume always reflects the latest profile data.
        app_record = _ensure_materials(db, job, force=True, variant=variant)
        return {
            "resume_pdf": f"/api/jobs/{job.id}/resume.pdf",
            "cover_letter": app_record.cover_letter,
            "personalization_score": app_record.personalization_score,
            "questions": generate_questions(job.title, job.description, job.skills),
        }

    # ---------- Application form (prefilled, editable) ----------
    def _prefill_form(profile: Profile, job: Job) -> dict:
        """Build the default application form from the user's real profile + job."""
        location = ", ".join(
            x for x in [profile.city, profile.current_country] if x
        )
        return {
            "name": profile.name or "",
            "email": profile.email or "",
            "phone": profile.phone or "",
            "linkedin": profile.linkedin or "",
            "website": profile.website or "",
            "github": profile.github or "",
            "current_location": location,
            "timezone": profile.timezone or "",
            "notice_period": profile.notice_period or "",
            "expected_salary": profile.expected_salary or "",
            "work_authorization": profile.work_authorization or "",
            "visa_status": profile.visa_status or "",
            "availability": profile.availability or "",
            "preferred_work_mode": profile.preferred_work_mode or "",
            "years_experience": profile.years_experience,
            "languages": ", ".join(profile.languages or []),
            "certifications": ", ".join(
                (c.get("name") if isinstance(c, dict) else str(c))
                for c in (profile.certifications or [])
            ),
            "cover_letter": "",
        }

    @app.get("/api/jobs/{job_id}/application-form")
    def get_application_form(job_id: int, user: User = Depends(current_user)):
        """Return the application form for a job, prefilled from the profile.

        If the user already saved edits, those take precedence; otherwise the
        form is prefilled from the current profile + job so it can be edited.
        """
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            profile = session.get(Profile, 1)
            if not profile:
                raise HTTPException(404, "profile not found")
            app_record = session.query(Application).filter(Application.job_id == job.id).first()
            base = _prefill_form(profile, job)
            # Prefill the cover letter from the generated one if present.
            if app_record and app_record.cover_letter:
                base["cover_letter"] = app_record.cover_letter
            base["resume_pdf"] = (
                f"/api/jobs/{job.id}/resume.pdf" if app_record and app_record.resume_pdf_path else None
            )
            # Merge any previously saved edits on top of the fresh prefill.
            saved = (app_record.application_form if app_record else None) or {}
            for key, value in saved.items():
                base[key] = value
            base["job_title"] = job.title
            base["company"] = job.company
            base["saved"] = bool(saved)
            # Completeness meter (F5): required fields for a submittable form.
            required = ["name", "email", "phone", "expected_salary"]
            missing = [k for k in required if not str(base.get(k) or "").strip()]
            filled = len(required) - len(missing)
            base["completeness"] = {
                "filled": filled,
                "total": len(required),
                "pct": round((filled / len(required)) * 100, 1),
                "missing_required": missing,
            }
            # Cover-letter personalization score (F13).
            base["personalization_score"] = app_record.personalization_score if app_record else None
            return base

    @app.put("/api/jobs/{job_id}/application-form")
    def save_application_form(job_id: int, payload: dict, user: User = Depends(current_user)):
        """Save the user's edited application form for a job."""
        with db.session() as session:
            job = session.get(Job, job_id)
            if not job:
                raise HTTPException(404, "job not found")
            app_record = session.query(Application).filter(Application.job_id == job.id).first()
            if app_record is None:
                app_record = Application(job_id=job.id, status="draft")
                session.add(app_record)
            # Strip read-only / context keys before persisting.
            form = {k: v for k, v in payload.items() if k not in ("job_title", "company", "saved", "resume_pdf")}
            app_record.application_form = form
            # If the user edited the cover letter, keep it in sync.
            if isinstance(form.get("cover_letter"), str) and form["cover_letter"].strip():
                app_record.cover_letter = form["cover_letter"]
            session.commit()
            return {"ok": True, "saved": True}

    @app.get("/api/jobs/{job_id}/resume.pdf")
    def resume_pdf(job_id: int, user: User = Depends(current_user)):
        with db.session() as session:
            app_record = session.query(Application).filter(Application.job_id == job_id).first()
            if not app_record or not app_record.resume_pdf_path:
                raise HTTPException(404, "resume not generated")
            path = Path(app_record.resume_pdf_path)
            if not path.exists():
                raise HTTPException(404, "resume file missing")
            return FileResponse(path, media_type="application/pdf", filename=path.name)

    @app.get("/api/jobs/{job_id}/screenshot")
    def job_screenshot(job_id: int, user: User = Depends(current_user)):
        """Proof screenshot captured when the browser submitted this job (Phase 4)."""
        with db.session() as session:
            app_record = session.query(Application).filter(Application.job_id == job_id).first()
            if not app_record or not app_record.screenshot_path:
                raise HTTPException(404, "no screenshot for this job")
            path = Path(app_record.screenshot_path)
            if not path.exists():
                raise HTTPException(404, "screenshot file missing")
            return FileResponse(path, media_type="image/png")

    @app.post("/api/company-sites/probe")
    def probe_company_site(payload: SiteProbeIn, user: User = Depends(current_user)):
        """Probe a company's careers page: the ATS behind it plus how many jobs a
        scan would pick up (Phase 4). Never raises — errors come back in-band."""
        from .adapters import probe_careers_page

        url = (payload.url or "").strip()
        if not url.startswith(("http://", "https://")):
            raise HTTPException(422, "A full careers URL (https://...) is required.")
        return probe_careers_page(url)

    # ---------- Stats & runs ----------
    @app.get("/api/stats")
    def stats(user: User = Depends(current_user)):
        from sqlalchemy import func

        with db.session() as session:
            total = session.query(Job).count()
            eligible = session.query(Job).filter(Job.status == "new").count()
            approved = session.query(Job).filter(Job.status == "approved").count()
            rejected = session.query(Job).filter(Job.status == "rejected").count()
            review = session.query(Job).filter(Job.status == "review").count()
            sources = session.query(Job.source).distinct().count()
            stage = func.coalesce(Application.application_status, Application.status)
            submitted = session.query(Application).filter(stage == "submitted").count()
            ready = session.query(Application).filter(stage == "ready").count()
            return {
                "total": total,
                "eligible": eligible,
                "approved": approved,
                "rejected": rejected,
                "review": review,
                "sources": sources,
                "submitted": submitted,
                "ready": ready,
            }

    @app.get("/api/top")
    def top_matches(limit: int = 10, user: User = Depends(current_user)):
        """The best N matches by confidence (eligible + review jobs only)."""
        with db.session() as session:
            jobs = (
                session.query(Job)
                .filter(Job.status.in_(["new", "review"]))
                .order_by(Job.confidence.desc(), Job.score.desc())
                .limit(max(1, min(limit, 50)))
                .all()
            )
            ids = [j.id for j in jobs]
            if ids:
                rows = session.query(Application.job_id).filter(
                    Application.job_id.in_(ids),
                    Application.resume_pdf_path.isnot(None),
                ).all()
                materials = {r[0] for r in rows}
            else:
                materials = set()
            return [_list_item(j, materials) for j in jobs]

    @app.get("/api/analytics")
    def analytics(user: User = Depends(current_user)):
        """Aggregates for the analytics dashboard (infographics)."""
        from datetime import datetime, timedelta, timezone

        with db.session() as session:
            from sqlalchemy import func

            total = session.query(Job).count()
            by_status = dict(
                session.query(Job.status, func.count(Job.id)).group_by(Job.status).all()
            )
            by_source = dict(
                session.query(Job.source, func.count(Job.id)).group_by(Job.source).all()
            )
            by_work_mode = dict(
                session.query(Job.work_mode, func.count(Job.id)).group_by(Job.work_mode).all()
            )

            # Confidence distribution buckets.
            buckets = {"0-39": 0, "40-54": 0, "55-69": 0, "70-84": 0, "85-100": 0}
            for (conf,) in session.query(Job.confidence).all():
                if conf < 40:
                    buckets["0-39"] += 1
                elif conf < 55:
                    buckets["40-54"] += 1
                elif conf < 70:
                    buckets["55-69"] += 1
                elif conf < 85:
                    buckets["70-84"] += 1
                else:
                    buckets["85-100"] += 1

            # Application pipeline (manual stage wins over the pipeline field).
            app_stage = func.coalesce(Application.application_status, Application.status)
            app_by_status = dict(
                session.query(app_stage, func.count(Application.id)).group_by(app_stage).all()
            )

            # Submissions over the last 14 days.
            since = datetime.now(timezone.utc) - timedelta(days=13)
            daily = {
                (since + timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(14)
            }
            for (ts,) in session.query(Application.submitted_at).filter(
                Application.submitted_at.isnot(None)
            ).all():
                if not ts:
                    continue
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                if ts >= since:
                    key = ts.astimezone(timezone.utc).strftime("%Y-%m-%d")
                    if key in daily:
                        daily[key] += 1

            # Top companies by job count.
            top_companies = [
                {"company": c, "count": n}
                for c, n in session.query(Job.company, func.count(Job.id))
                .group_by(Job.company).order_by(func.count(Job.id).desc()).limit(8).all()
            ]

            # Average confidence.
            avg = session.query(Job.confidence).filter(Job.confidence.isnot(None)).all()
            avg_conf = round(sum(c[0] for c in avg) / len(avg), 1) if avg else 0.0

            return {
                "total": total,
                "by_status": by_status,
                "by_source": by_source,
                "by_work_mode": by_work_mode,
                "confidence_buckets": buckets,
                "applications": app_by_status,
                "submissions_by_day": daily,
                "top_companies": top_companies,
                "avg_confidence": avg_conf,
            }

    # ---------- Analytics: salary insights (F1) ----------
    @app.get("/api/analytics/salary")
    def salary_insights(
        work_mode: str | None = None,
        source: str | None = None,
        role: str | None = None,
        user: User = Depends(current_user),
    ):
        """Salary distribution across jobs + where the user's ask falls.

        Reuses ``scoring._salary_value`` so every figure is normalized to
        thousands. Honest about sparsity: when no salary parses, stats are null.
        """
        with db.session() as session:
            query = session.query(Job)
            if work_mode:
                query = query.filter(Job.work_mode == work_mode)
            if source:
                query = query.filter(Job.source == source)
            if role:
                query = query.filter(Job.title.ilike(f"%{role}%"))
            jobs = query.all()
            profile = session.get(Profile, 1)

        values = []
        for job in jobs:
            v = _salary_value(job.salary)
            if v is not None:
                values.append(v)

        def _pct(sorted_vals: list[float], p: float) -> float:
            if not sorted_vals:
                return 0.0
            k = (len(sorted_vals) - 1) * (p / 100.0)
            lo = int(k)
            hi = min(lo + 1, len(sorted_vals) - 1)
            frac = k - lo
            return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac

        if not values:
            return {
                "count": 0, "min": None, "p25": None, "median": None,
                "p75": None, "max": None, "mean": None, "histogram": [],
                "user_value": None, "user_percentile": None,
                "by_work_mode": {}, "by_source": {},
            }

        sv = sorted(values)
        stats = {
            "count": len(values),
            "min": round(sv[0], 1),
            "p25": round(_pct(sv, 25), 1),
            "median": round(_pct(sv, 50), 1),
            "p75": round(_pct(sv, 75), 1),
            "max": round(sv[-1], 1),
            "mean": round(sum(values) / len(values), 1),
        }

        # ~10 equal-width buckets from min to max.
        lo, hi = sv[0], sv[-1]
        nbuckets = 10
        width = (hi - lo) / nbuckets if hi > lo else 1.0
        histogram = [
            {"label": f"{lo + i * width:.0f}-{lo + (i + 1) * width:.0f}k", "count": 0}
            for i in range(nbuckets)
        ]
        for v in values:
            idx = int((v - lo) / width) if width else 0
            idx = max(0, min(nbuckets - 1, idx))
            histogram[idx]["count"] += 1

        # Map the user's expected salary onto the distribution.
        user_value = None
        user_percentile = None
        if profile:
            uv = _salary_value(profile.expected_salary) or _salary_value(profile.min_salary)
            if uv is not None:
                user_value = round(uv, 1)
                below = sum(1 for v in values if v < uv)
                user_percentile = round((below / len(values)) * 100, 1)

        # Optional breakdowns (median + count per group).
        def _group(key) -> dict:
            groups: dict[str, list[float]] = {}
            for job in jobs:
                v = _salary_value(job.salary)
                if v is None:
                    continue
                groups.setdefault(key(job), []).append(v)
            return {
                k: {"median": round(_pct(sorted(vs), 50), 1), "count": len(vs)}
                for k, vs in sorted(groups.items())
            }

        return {
            **stats,
            "histogram": histogram,
            "user_value": user_value,
            "user_percentile": user_percentile,
            "by_work_mode": _group(lambda j: j.work_mode or "unknown"),
            "by_source": _group(lambda j: j.source or "unknown"),
        }

    # ---------- Salary negotiation assistant (v2.4) ----------
    @app.api_route("/api/negotiation", methods=["GET", "PUT"])
    def salary_negotiation(
        offer: float | None = None,
        role: str | None = None,
        work_mode: str | None = None,
        payload: dict = Body(None),
        user: User = Depends(current_user),
    ):
        """Turn market salary data into a negotiation range + talking points.

        ``offer`` is the candidate's stated ask (thousands). When omitted it
        defaults to the profile's expected salary. The recommended range is
        derived from the market distribution: a floor at the user's ask and a
        stretch target near the 60th–75th percentile of comparable offers.

        Accepts GET (offer as a query param) or PUT (offer in a JSON body) so
        the negotiation assistant can recalculate when the user edits their ask.
        """
        # PUT sends the offer in a JSON body; GET sends it as a query param.
        if offer is None and isinstance(payload, dict):
            offer = payload.get("offer")
        with db.session() as session:
            query = session.query(Job)
            if role:
                query = query.filter(Job.title.ilike(f"%{role}%"))
            if work_mode:
                query = query.filter(Job.work_mode == work_mode)
            jobs = query.all()
            profile = session.get(Profile, 1)

        values = []
        for job in jobs:
            v = _salary_value(job.salary)
            if v is not None:
                values.append(v)

        if not values:
            return {
                "count": 0,
                "market": None,
                "recommendation": None,
                "talking_points": [],
                "market_context": "No salary data in your jobs yet. Scanning more roles will improve the recommendation.",
            }

        sv = sorted(values)
        median = round(_pct(sv, 50), 1)
        p25 = round(_pct(sv, 25), 1)
        p75 = round(_pct(sv, 75), 1)
        p60 = round(_pct(sv, 60), 1)
        p90 = round(_pct(sv, 90), 1)
        mean = round(sum(values) / len(values), 1)

        # Determine the user's ask.
        ask = offer
        if ask is None and profile:
            ask = _salary_value(profile.expected_salary) or _salary_value(profile.min_salary)
        ask = round(ask, 1) if ask is not None else None

        # Build the recommended range.
        recommendation = None
        talking_points = []
        if ask is not None:
            floor = ask
            stretch = round(max(p75, p60, ask * 1.12), 1)
            if stretch <= floor:
                stretch = round(floor * 1.12, 1)
            mid = round((floor + stretch) / 2, 1)
            recommendation = {
                "floor": floor,
                "target": mid,
                "stretch": stretch,
                "ask": ask,
            }
            # Talking points — data-backed, tailored to the ask vs. market.
            if ask < median:
                talking_points.append(
                    f"Market data shows comparable roles median around ${median}k; "
                    f"your ask of ${ask}k sits below that, so there's room to aim higher."
                )
            elif ask > p90:
                talking_points.append(
                    f"Your ask of ${ask}k is above the 90th percentile (${p90}k) — "
                    "lead with your specific, differentiated value and concrete achievements."
                )
            else:
                talking_points.append(
                    f"Your ask of ${ask}k aligns with the market median of ${median}k; "
                    "anchor there and let them name a number first."
                )
            talking_points.append(
                f"Comparable offers in your data range from ${sv[0]:.0f}k to "
                f"${sv[-1]:.0f}k, with the 75th percentile at ${p75}k."
            )
            talking_points.append(
                "Frame the range, not a single number: present the floor as your "
                "comfortable number and the stretch as your target for the right scope."
            )
            talking_points.append(
                "Consider total compensation — equity, PTO, remote flexibility, and "
                "growth — if the base number can't move as much as you'd like."
            )

        return {
            "count": len(values),
            "offer": ask,
            "market": {
                "p25": p25,
                "median": median,
                "p50": median,
                "mean": mean,
                "p60": p60,
                "p75": p75,
                "p90": p90,
                "min": round(sv[0], 1),
                "max": round(sv[-1], 1),
            },
            "recommendation": recommendation,
            "talking_points": talking_points,
            "market_context": "Recommendation based on live salary data from your scanned jobs.",
        }

    # ---------- Analytics: skill gap (F3) ----------
    @app.get("/api/analytics/skills")
    def skill_gap(
        work_mode: str | None = None,
        source: str | None = None,
        user: User = Depends(current_user),
    ):
        """Skill demand across jobs vs. the user's skills (deterministic)."""
        with db.session() as session:
            query = session.query(Job)
            if work_mode:
                query = query.filter(Job.work_mode == work_mode)
            if source:
                query = query.filter(Job.source == source)
            jobs = query.all()
            profile = session.get(Profile, 1)

        freq: dict[str, int] = {}
        for job in jobs:
            for skill in (job.skills or []):
                key = str(skill).strip().lower()
                if key:
                    freq[key] = freq.get(key, 0) + 1

        top_requested = [
            {"skill": s, "count": c}
            for s, c in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:15]
        ]

        profile_skills = [str(s).strip().lower() for s in (profile.skills or []) if str(s).strip()]
        profile_expanded: set[str] = set()
        for s in profile_skills:
            profile_expanded |= _expand(s)

        # In-demand skills the user does not cover (via profile or synonyms).
        you_are_missing = [
            {"skill": s, "count": c}
            for s, c in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
            if s not in profile_expanded
        ][:15]

        # The user's skills ranked by market demand (0-count last).
        your_skills = [
            {"skill": s, "count": freq.get(s, 0)}
            for s in sorted(set(profile_skills), key=lambda s: (-freq.get(s, 0), s))
        ]

        present = sum(1 for s in set(profile_skills) if s in freq)
        coverage = round((present / len(set(profile_skills))) * 100, 1) if profile_skills else 0.0

        return {
            "top_requested": top_requested,
            "you_are_missing": you_are_missing,
            "your_skills_by_demand": your_skills,
            "coverage_pct": coverage,
        }

    # ---------- Analytics: source health (F4) ----------
    @app.get("/api/analytics/sources")
    def source_health(user: User = Depends(current_user)):
        """Per-source reliability derived from scan history."""
        from .models import ScrapeRun

        with db.session() as session:
            runs = session.query(ScrapeRun).order_by(ScrapeRun.started_at.asc()).all()

        by_source: dict[str, list] = {}
        for r in runs:
            by_source.setdefault(r.source, []).append(r)

        sources = []
        for name, rs in sorted(by_source.items()):
            total = len(rs)
            done = sum(1 for r in rs if r.status == "done")
            errors = sum(1 for r in rs if r.error)
            success_rate = round((done / total) * 100, 1) if total else 0.0
            avg_fetched = round(sum(r.fetched or 0 for r in rs) / total, 1) if total else 0.0
            last = rs[-1]
            if success_rate >= 80 and last.status == "done":
                health = "green"
            elif success_rate >= 50:
                health = "amber"
            else:
                health = "red"
            sources.append({
                "source": name,
                "last_scan": last.started_at.isoformat() if last.started_at else None,
                "last_status": last.status,
                "total_scans": total,
                "success_rate": success_rate,
                "avg_fetched": avg_fetched,
                "error_count": errors,
                "sparkline": [r.fetched or 0 for r in rs[-10:]],
                "health": health,
            })
        return {"sources": sources}

    @app.get("/api/analytics/trend")
    def fit_trend(user: User = Depends(current_user)):
        """How average fit (confidence + eligibility) has moved across scans."""
        from .models import ScrapeRun

        with db.session() as session:
            runs = (
                session.query(ScrapeRun)
                .filter(ScrapeRun.status == "done")
                .order_by(ScrapeRun.started_at.asc())
                .all()
            )
        points = [
            {
                "at": r.started_at.isoformat() if r.started_at else None,
                "source": r.source,
                "avg_confidence": r.avg_confidence,
                "avg_eligibility": r.avg_eligibility,
            }
            for r in runs
            if r.avg_confidence is not None or r.avg_eligibility is not None
        ]
        return {"points": points}

    @app.get("/api/runs")
    def runs(limit: int = 10, user: User = Depends(current_user)):
        from .models import ScrapeRun

        with db.session() as session:
            rows = session.query(ScrapeRun).order_by(ScrapeRun.started_at.desc()).limit(limit).all()
            return [
                {
                    "id": r.id,
                    "source": r.source,
                    "status": r.status,
                    "fetched": r.fetched,
                    "eligible": r.eligible,
                    "rejected": r.rejected,
                    "review": r.review,
                    "error": r.error,
                    "started_at": r.started_at.isoformat() if r.started_at else None,
                }
                for r in rows
            ]

    # ---------- Export / Import (F14) ----------
    def _rows_to_csv(rows: list[dict]) -> str:
        if not rows:
            return ""

        def _cell(v):
            # Neutralize spreadsheet formula injection (cells beginning with
            # =, +, -, @, tab or CR are prefixed with an apostrophe).
            if isinstance(v, str) and v[:1] in ("=", "+", "-", "@", "\t", "\r"):
                return "'" + v
            return "" if v is None else v

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _cell(v) for k, v in row.items()})
        return buf.getvalue()

    @app.get("/api/export/jobs")
    def export_jobs(format: str = "csv", user: User = Depends(current_user)):
        with db.session() as session:
            jobs = session.query(Job).order_by(Job.id.asc()).all()
            rows = [j.to_dict() for j in jobs]
        if format == "json":
            return {"jobs": rows}
        return Response(
            content=_rows_to_csv(rows),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=jobs.csv"},
        )

    @app.get("/api/export/applications")
    def export_applications(format: str = "csv", user: User = Depends(current_user)):
        with db.session() as session:
            apps = session.query(Application).order_by(Application.id.asc()).all()
            rows = [a.to_dict() for a in apps]
        if format == "json":
            return {"applications": rows}
        return Response(
            content=_rows_to_csv(rows),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=applications.csv"},
        )

    @app.get("/api/export/analytics")
    def export_analytics(format: str = "csv", user: User = Depends(current_user)):
        from .models import ScrapeRun

        with db.session() as session:
            runs = session.query(ScrapeRun).order_by(ScrapeRun.id.asc()).all()
            rows = [
                {
                    "id": r.id,
                    "source": r.source,
                    "status": r.status,
                    "fetched": r.fetched,
                    "eligible": r.eligible,
                    "rejected": r.rejected,
                    "review": r.review,
                    "avg_confidence": r.avg_confidence,
                    "avg_eligibility": r.avg_eligibility,
                    "started_at": r.started_at.isoformat() if r.started_at else None,
                }
                for r in runs
            ]
        if format == "json":
            return {"runs": rows}
        return Response(
            content=_rows_to_csv(rows),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=analytics.csv"},
        )

    @app.post("/api/import/jobs")
    def import_jobs(payload: dict, user: User = Depends(current_user)):
        """Import jobs from a JSON export. Dedups by fingerprint; skips bad rows."""
        jobs_in = (payload or {}).get("jobs")
        if not isinstance(jobs_in, list):
            raise HTTPException(422, "jobs must be a list")
        imported = 0
        skipped = 0
        errors: list[str] = []
        with db.session() as session:
            existing = {row[0] for row in session.query(Job.fingerprint).all()}
            profile = session.get(Profile, 1)
            profile_skills = list(profile.skills or []) if profile else []
            for i, item in enumerate(jobs_in):
                if not isinstance(item, dict):
                    skipped += 1
                    errors.append(f"row {i}: not an object")
                    continue
                # Normalise the raw record: unescape entities, repair mojibake,
                # strip HTML to text, and clean the skills field.
                raw = _clean_raw(item)
                title = (raw.get("title") or "").strip()
                company = (raw.get("company") or "").strip()
                url = (raw.get("url") or "").strip()
                if not title or not company:
                    skipped += 1
                    errors.append(f"row {i}: missing title or company")
                    continue
                fp = raw.get("fingerprint") or fingerprint(title, company, url)
                if fp in existing:
                    skipped += 1
                    continue
                existing.add(fp)
                # Auto-apply-only gate: rows Playwright cannot submit are
                # skipped with an explicit reason (dedup still wins above so
                # its counters keep their exact meaning).
                if config.auto_apply_only and not is_auto_applicable(raw):
                    skipped += 1
                    errors.append(
                        f"row {i}: no application_url — cannot auto-apply (auto_apply_only)"
                    )
                    continue

                # Score the job if the export did not carry a valid score.
                confidence_val = raw.get("confidence")
                eligibility_val = raw.get("eligibility")
                if not _is_valid_score(confidence_val) or not _is_valid_score(eligibility_val):
                    assessment = assess_job(
                        title=title,
                        description=raw.get("description"),
                        job_skills=raw.get("skills"),
                        profile_skills=profile_skills,
                        target_role=config.role,
                        location_status=raw.get("location_status") or "eligible",
                        work_mode=raw.get("work_mode") or "remote",
                        salary=raw.get("salary"),
                        min_salary=config.min_salary,
                        company_overall=get_company_info(company).overall,
                        posted_date=raw.get("posted_date"),
                        application_url=raw.get("application_url"),
                        preferred_remote=True,
                    )
                    confidence_val = assessment.confidence
                    eligibility_val = assessment.eligibility
                    score_val = assessment.fit_score
                    score_breakdown = assessment.breakdown
                    confidence_breakdown = {
                        "factors": [
                            {"key": f.key, "label": f.label, "value": f.value,
                             "weight": f.weight, "detail": f.detail}
                            for f in assessment.factors
                        ],
                        "matched_skills": assessment.matched_skills,
                        "missing_skills": assessment.missing_skills,
                        "must_have_present": assessment.must_have_present,
                        "must_have_missing": assessment.must_have_missing,
                        "reasons": assessment.reasons,
                    }
                    confidence_label = assessment.confidence_label
                    eligibility_label = assessment.eligibility_label
                else:
                    # Guard a missing/garbage score: Job.score is NOT NULL, so
                    # passing None would abort the whole import with an
                    # IntegrityError (the column default only applies when the
                    # field is omitted entirely — an explicit None overrides it).
                    score_val = (
                        raw.get("score") if _is_valid_score(raw.get("score")) else 0.0
                    )
                    score_breakdown = raw.get("score_breakdown")
                    confidence_breakdown = raw.get("confidence_breakdown")
                    confidence_label = raw.get("confidence_label")
                    eligibility_label = raw.get("eligibility_label")

                session.add(Job(
                    fingerprint=fp,
                    title=title,
                    company=company,
                    location=raw.get("location"),
                    work_mode=raw.get("work_mode") or "remote",
                    employer_country=raw.get("employer_country"),
                    job_country=raw.get("job_country"),
                    candidate_required_location=raw.get("candidate_required_location"),
                    worldwide_remote=bool(raw.get("worldwide_remote")),
                    salary=raw.get("salary"),
                    description=raw.get("description"),
                    skills=raw.get("skills"),
                    url=url,
                    source=raw.get("source") or "import",
                    ats=raw.get("ats"),
                    posted_date=raw.get("posted_date"),
                    application_url=raw.get("application_url"),
                    application_method=raw.get("application_method"),
                    location_status=raw.get("location_status") or "eligible",
                    location_reason=raw.get("location_reason"),
                    score=score_val,
                    score_breakdown=score_breakdown,
                    confidence=confidence_val,
                    confidence_label=confidence_label,
                    eligibility=eligibility_val,
                    eligibility_label=eligibility_label,
                    confidence_breakdown=confidence_breakdown,
                    status=(
                        raw.get("status")
                        if raw.get("status") in _JOB_STATUSES
                        else "new"
                    ),
                ))
                imported += 1
            session.commit()
        return {"imported": imported, "skipped": skipped, "errors": errors[:50]}

    # ---------- Dashboard ----------
    @app.get("/", response_class=HTMLResponse)
    def dashboard():
        return (STATIC_DIR / "index.html").read_text(encoding="utf-8")

    return app


def _ensure_materials(db, job: Job, force: bool = False, variant: str | None = None):
    """Ensure a tailored resume PDF + cover letter exist for the job.

    Creates the Application record if needed and generates the materials if
    they are missing (or always, when ``force`` is set — e.g. after the profile
    changes so the resume reflects the latest real data). When ``variant`` is
    given (a resume-variant id), that variant's summary + skills override the
    profile's for the resume. Returns the record.
    """
    with db.session() as session:
        app_record = session.query(Application).filter(Application.job_id == job.id).first()
        if app_record is None:
            app_record = Application(job_id=job.id, status="draft")
            session.add(app_record)
            session.flush()
        if force or not app_record.resume_pdf_path:
            profile = session.get(Profile, 1)
            if profile:
                # Resolve an optional resume variant (F12).
                summary = profile.summary or ""
                skills = list(profile.skills or [])
                if variant:
                    v = next(
                        (x for x in (profile.resume_variants or []) if str(x.get("id")) == str(variant)),
                        None,
                    )
                    if v:
                        summary = v.get("summary") or summary
                        skills = list(v.get("skills") or skills)
                resume = ResumeData(
                    name=profile.name or "",
                    email=profile.email or "",
                    phone=profile.phone or "",
                    summary=summary,
                    skills=skills,
                    experiences=list(profile.experiences or []),
                    education=list(profile.education or []),
                )
                tailored = tailor_resume(resume, job.title, job.description)
                pdf_path = DATA_DIR / "resumes" / f"resume_{job.id}.pdf"
                render_pdf(tailored, job.title, pdf_path)
                app_record.resume_pdf_path = str(pdf_path)
                letter, score = _cover_letter(profile, job)
                app_record.cover_letter = letter
                app_record.personalization_score = score
                if app_record.status == "draft":
                    app_record.status = "ready"
                if not app_record.application_status or app_record.application_status == "draft":
                    app_record.application_status = "ready"
        session.commit()
        return app_record


def _auto_generate_top(db, limit: int = 10, force: bool = False) -> int:
    """Auto-generate resume + cover letter for the top-N best matches.

    Runs after a scan or re-score so the user's best-fit jobs always have
    ready-to-use materials. ``force`` regenerates even when materials already
    exist (used after a profile change so the resume reflects the latest data).
    Returns the number of jobs prepared.
    """
    with db.session() as session:
        jobs = (
            session.query(Job)
            .filter(Job.status.in_(["new", "review"]))
            .order_by(Job.confidence.desc(), Job.score.desc())
            .limit(limit)
            .all()
        )
        ids = [j.id for j in jobs]
    prepared = 0
    for jid in ids:
        with db.session() as session:
            job = session.get(Job, jid)
            if job:
                _ensure_materials(db, job, force=force)
                prepared += 1
    return prepared


def _submit_application(db, job: Job, auto_submit: bool | None = None) -> dict:
    """Run the submission pipeline for an approved job.

    Phase 4: when the job has a direct apply URL, browser automation is
    available, and ``auto_submit`` (config.yaml, default on) allows it, apply
    directly on the company's own page with Playwright — fill the form from the
    profile + prepared materials, upload the tailored resume PDF, submit, and
    save a proof screenshot.

    Whatever the browser does (or when it cannot run at all), this always
    writes an honest, auditable record and never raises: "submitted" + auto-web
    when the browser confirmed a receipt page; the legacy "submitted" wording
    when a direct apply link exists; otherwise "ready" with the exact next step.
    """
    from datetime import datetime, timezone

    from . import apply as apply_mod

    now = datetime.now(timezone.utc)
    app_record = _ensure_materials(db, job)

    if auto_submit is None:
        try:
            from .config import load_config

            auto_submit = load_config().auto_submit
        except Exception:
            auto_submit = True

    # daily_cap (config.yaml): bound how many applications are pushed through
    # the browser per UTC day. Once the cap is reached, fall back to the
    # prepare-materials-and-link flow instead of auto-submitting.
    if auto_submit:
        try:
            from .config import load_config

            daily_cap = load_config().daily_cap
        except Exception:
            daily_cap = 10
        if daily_cap > 0:
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            with db.session() as session:
                # Only browser-driven submissions consume the cap — manual
                # submissions are not "pushed through the browser" and must
                # not lock the user out of auto-submit for the rest of the day.
                submitted_today = (
                    session.query(Application)
                    .filter(Application.submitted_at >= start_of_day)
                    .filter(Application.submission_method == "auto-web")
                    .count()
                )
            if submitted_today >= daily_cap:
                auto_submit = False

    browser: dict | None = None
    if auto_submit and job.application_url and apply_mod.browser_available():
        with db.session() as session:
            rec = session.get(Application, app_record.id)
            profile = session.get(Profile, 1)
            form = dict(rec.application_form or {})
            for noisy in ("cover_letter", "completeness", "saved"):
                form.pop(noisy, None)
            context = {
                "profile": profile.to_dict() if profile else {},
                "cover_letter": rec.cover_letter or "",
                "answers": {k: v for k, v in form.items() if isinstance(v, str)},
                "resume": rec.resume_pdf_path,
            }
        browser = apply_mod.submit_on_company_site(
            url=job.application_url,
            profile=context["profile"],
            cover_letter=context["cover_letter"],
            answers=context["answers"],
            resume_path=context["resume"],
            screenshot_path=SCREENSHOTS_DIR / f"job_{job.id}.png",
        )
    with db.session() as session:
        app_record = session.get(Application, app_record.id)
        app_record.attempts = (app_record.attempts or 0) + 1
        app_record.last_attempt_at = now
        if browser and browser.get("ok"):
            app_record.submission_method = "auto-web"
        else:
            app_record.submission_method = job.application_method or "manual"
        if browser and browser.get("screenshot"):
            app_record.screenshot_path = browser["screenshot"]

        if browser and browser.get("ok"):
            # The browser confirmed a receipt page on the company's own site.
            app_record.status = "submitted"
            app_record.application_status = "submitted"
            app_record.submitted_at = now
            app_record.submission_status = "submitted"
            app_record.submission_url = browser.get("final_url") or job.application_url
            app_record.submission_message = (
                "Submitted directly on the company's site via browser automation. "
                "A proof screenshot was saved — open it to verify."
            )
        elif job.application_url:
            app_record.status = "submitted"
            app_record.application_status = "submitted"
            app_record.submitted_at = now
            app_record.submission_status = "submitted"
            app_record.submission_url = job.application_url
            message = (
                "Application package prepared and routed to the employer's apply link. "
                "Open the link to confirm submission."
            )
            if browser:
                message += f" Browser attempt: {browser.get('message')}"
            app_record.submission_message = message
        else:
            app_record.status = "ready"
            app_record.application_status = "ready"
            app_record.submission_status = "ready"
            app_record.submission_message = (
                "No direct apply link on this listing. Your tailored resume and cover "
                "letter are ready — open the job page and upload them to submit."
            )
        session.commit()
        return app_record.to_dict()


def _cover_letter(profile: Profile, job: Job) -> tuple[str, int]:
    """Generate a personalized cover letter from the user's real profile data.

    Returns ``(letter, personalization_score)``. The score (0-100) reflects how
    many job-specific hooks (matched skills, a description keyword, company
    reference) were woven in, so the UI can show how tailored the letter is.

    If the profile is still empty, it produces a clearly-marked placeholder
    rather than inventing facts, and prompts the user to complete their profile.
    """
    name = (profile.name or "").strip()
    role = (profile.role or "").strip()
    skills = [s for s in (profile.skills or []) if s][:5]
    summary = (profile.summary or "").strip()

    if not name and not role and not skills and not summary:
        return (
            "Dear Hiring Team,\n\n"
            f"I am writing to express my interest in the {job.title} role at {job.company}.\n\n"
            "[Your profile is not complete yet. Add your name, role, skills, and a short "
            "summary in the Profile tab — this cover letter will be regenerated with your "
            "real details.]\n\n"
            "Thank you for your consideration.\n\n"
            "Best regards,\n[Your name]"
        ), 0

    # --- Job-specific personalization hooks (deterministic, no LLM) ---
    job_skills = [s for s in (job.skills or []) if s]
    profile_skill_set = {s.lower() for s in (profile.skills or [])}
    matched = [s for s in job_skills if s.lower() in profile_skill_set][:3]

    # A keyword from the description that also appears in the profile.
    desc_tokens = _tokens(job.description or "")
    profile_tokens = _tokens(" ".join((profile.skills or []) + [profile.summary or ""]))
    desc_keyword = next((t for t in desc_tokens if t in profile_tokens and len(t) > 3), None)

    hooks = 0
    skill_sentence = ""
    if matched:
        hooks += 1
        skill_sentence = (
            f"Your emphasis on {', '.join(matched)} aligns closely with the work I do "
            f"every day, and I would welcome the chance to bring that experience to {job.company}."
        )
    keyword_sentence = ""
    if desc_keyword:
        hooks += 1
        keyword_sentence = (
            f"Reading the listing, I was drawn to the focus on {desc_keyword} — an area "
            f"where I have delivered measurable results."
        )
    company_sentence = (
        f"I have followed {job.company}'s work and am excited by the opportunity to "
        f"contribute to the {job.title} team."
    )
    hooks += 1  # company reference is always present

    skill_line = f" with hands-on experience in {', '.join(skills)}" if skills else ""
    summary_line = f" {summary}" if summary else ""

    body = (
        f"Dear Hiring Team,\n\n"
        f"I am writing to express my interest in the {job.title} role at {job.company}. "
        f"As a {role or 'professional'}{skill_line}, I am confident I can contribute to your team.{summary_line}\n\n"
    )
    if skill_sentence:
        body += skill_sentence + "\n\n"
    if keyword_sentence:
        body += keyword_sentence + "\n\n"
    body += (
        company_sentence + "\n\n"
        "I am available to start per my stated notice period and am flexible on time zones.\n\n"
        "Thank you for your consideration.\n\n"
        f"Best regards,\n{name or '[Your name]'}"
    )

    # Score: base for a complete profile + points per job-specific hook.
    score = 40 + hooks * 20  # 40..100
    return body, min(100, score)


def main() -> None:
    import uvicorn

    uvicorn.run("zeyrecuite.app:create_app", factory=True, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()

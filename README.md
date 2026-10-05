# ZEYRECUITE — Personal AI Job Agent (MVP)

A local-first, $0 job-search assistant for a **Business Analyst** in **Bangladesh**.
It collects remote jobs from **Remotive** and **Greenhouse**, applies a hard
**South-Asia origin exclusion** (while still allowing worldwide remote roles that
accept South Asian applicants), scores role fit, and lets you review, generate a
tailored resume PDF + cover letter, and approve/reject — all from a morning-review
dashboard.

## Quick start (Windows)

```bat
start.bat
```

Then open **http://127.0.0.1:8000**.

The launcher creates a virtual environment if missing, installs `backend/requirements.txt`,
and starts the FastAPI app. No API keys are required.

## Manual start

```bat
python -m venv .venv
.venv\Scripts\python -m pip install -r backend\requirements.txt
.venv\Scripts\python -m uvicorn zeyrecuite.app:create_app --factory --app-dir backend --host 127.0.0.1 --port 8000
```

## Configuration

Edit `backend/config.yaml`:

- `location.current` — your current country (default `Bangladesh`).
- `location.excluded_countries` — hard deny set for **employer/job origin**.
- `sources.greenhouse.boards` — public Greenhouse board tokens to poll.
- `role`, `min_salary`, `daily_cap` — matching preferences.

## Location policy (authoritative)

- **Hard exclusion:** a job is rejected if its **employer base** or **actual job
  location** is in an excluded South-Asian country — even when labeled remote.
- **Worldwide remote allowed:** a non-South-Asian employer's worldwide remote role
  may accept applicants in South Asia (including Bangladesh).
- **Eligibility check:** the current user's country is checked against each posting's
  explicit applicant-location restrictions. A role that excludes the user's country
  is rejected; unclear eligibility is held for **review**, not auto-rejected.

## Architecture

```
backend/
  zeyrecuite/
    config.py          # config loading (config.yaml)
    database.py        # SQLAlchemy engine/session (SQLite)
    models.py          # Job, Profile, Application, ScrapeRun
    location_policy.py # deterministic origin + eligibility gate
    dedup.py           # stable fingerprinting
    scoring.py         # deterministic role-fit score (Tier 0, no LLM)
    adapters.py        # Remotive + Greenhouse adapters
    collector.py       # fetch -> gate -> dedup -> score -> persist
    resume.py          # tailoring + PDF (ReportLab)
    app.py             # FastAPI app + API + dashboard
    static/            # dashboard (HTML/CSS/JS)
  tests/               # unit + integration tests
  config.yaml
  requirements.txt
start.bat
```

## Tests

```bat
.venv\Scripts\python -m pytest backend\tests -q
```

## Notes

- **No auto-apply.** The MVP never submits applications; it prepares materials for
  your explicit approval.
- **Truth-preserving resume.** Tailoring reorders your existing content; it never
  invents skills, employers, or facts.
- **Local-first.** Data lives in `backend/zeyrecuite.db` (SQLite). Cloud deployment
  is a later, optional phase.

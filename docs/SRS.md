# ZEYRECUITE — Software Requirements Specification (SRS)

**Version:** 2.3
**Companion docs:** `PRD.md` (why), `user-stories.md` (who/what), `test-cases.md` (how to verify)

---

## 1. System Overview

### 1.1 Architecture
- **Backend:** Python 3.14, FastAPI (app factory `create_app(config)`),
  SQLAlchemy 2.x ORM, SQLite (local-first), Pydantic v2, ReportLab (PDF),
  httpx, Playwright (Phase 4).
- **Frontend:** Vanilla-JS SPA (`backend/zeyrecuite/static/app.js`), `style.css`,
  `index.html`. No framework. `api()` fetch helper with Bearer token
  (localStorage key `zr_token`).
- **Auth:** Bearer token; default user `admin` / `zeyrecuite`.
- **Scoring:** Deterministic engine in `scoring.py` (no LLM).

### 1.2 Existing data model (relevant to v2.3)
- `Job`: id, fingerprint (unique), title, company, location, work_mode,
  employer_country, job_country, candidate_required_location (JSON),
  worldwide_remote, salary (String 120), description, skills (JSON), url,
  source, posted_date, application_url, application_method, location_status,
  location_reason, score, score_breakdown (JSON), confidence, confidence_label,
  eligibility, eligibility_label, confidence_breakdown (JSON), status (indexed),
  created_at, updated_at.
- `Application`: id, job_id (indexed), status (draft→ready→submitting→
  submitted|failed), resume_pdf_path, cover_letter, answers (JSON),
  application_form (JSON), submitted_at, submission_method, submission_url,
  submission_status, submission_message, attempts, last_attempt_at, created_at,
  updated_at.
- `ScrapeRun`: id, source, status, fetched, eligible, rejected, review, error,
  started_at, finished_at.
- `Profile`: id (always 1), name, email, phone, linkedin, website, github,
  current_country, city, timezone, availability, notice_period, role,
  years_experience, summary, skills (JSON), keywords, languages, certifications
  (JSON), projects (JSON), interests, experiences (JSON), education (JSON),
  expected_salary, min_salary, work_authorization, visa_status,
  preferred_work_mode, target_companies (JSON), deal_breakers (JSON),
  standard_answers (JSON), resume_text, resume_path, updated_at.

### 1.3 Reusable primitives (do not reinvent)
- `scoring._salary_value(salary) -> float | None` — normalizes a salary string
  to **thousands** (handles `$120,000`, `120k`, `120000`, `8000/mo`).
- `scoring.assess_job(...) -> Assessment` — confidence, eligibility, factors,
  matched_skills, missing_skills, must_have_present/missing, reasons, breakdown.
- `scoring._fit_components(...)` — returns `matched`, `missing`,
  `profile_expanded`, `job_expanded`, `must_present`, `must_missing`.
- `scoring._tokens(text)`, `scoring._expand(skill)`, `scoring._SYNONYMS`.
- `companies.get_company_info(name) -> CompanyInfo` (overall, ratings, flags,
  warnings, size, founded, remote_policy; `has_data=False` when unknown).
- `dedup.fingerprint(title, company, url)`, `dedup.is_duplicate`.
- `collector.run_source / run_all`, `adapters.BaseAdapter / build_adapters`.
- Frontend chart helpers: `donutChart`, `barChart`, `hbarChart`, `statCard`,
  `emptyBox`, `confColor`, `timeAgo`, `esc`.

---

## 2. Functional Requirements

### FR-1 — Salary Insights (F1)

**Endpoint:** `GET /api/analytics/salary?work_mode=&source=&role=`
- Query params (all optional): `work_mode`, `source`, `role` (filter by
  `Job.work_mode`, `Job.source`, and title-contains `role`).
- **Behavior:**
  1. Select jobs matching filters.
  2. For each job, compute `v = _salary_value(job.salary)`; keep only non-None.
  3. Compute: `count`, `min`, `p25`, `median` (p50), `p75`, `max`, `mean`
     (all in thousands, rounded to 1 dp).
  4. Build a histogram of ~10 equal-width buckets from min→max:
     `[{label: "80-90k", count: n}, ...]`.
  5. Compute the user's percentile: map `profile.expected_salary` (and
     `profile.min_salary`) onto the distribution → `user_percentile` (0–100)
     and `user_value` (thousands). If no parseable expected salary, both null.
  6. Optional `by_work_mode` / `by_source` breakdowns (median + count each).
- **Response shape:**
  ```json
  {
    "count": 312, "min": 60, "p25": 85, "median": 100, "p75": 120,
    "max": 200, "mean": 104.3,
    "histogram": [{"label": "60-70k", "count": 20}, ...],
    "user_value": 90, "user_percentile": 62,
    "by_work_mode": {"remote": {"median": 105, "count": 200}},
    "by_source": {"remotive": {"median": 95, "count": 120}}
  }
  ```
- **Edge cases:** `count == 0` → all stats null, empty histogram,
  `user_percentile` null. Percentile = (number of values < user_value) / count
  * 100 (linear, no interpolation required).
- **Frontend:** New "Salary" section on Analytics — histogram (reuse
  `barChart`), a stats card row (median, p25, p75, count), and a "you vs
  market" gauge (a horizontal bar with a marker at `user_percentile`).
- **No model changes.**

### FR-2 — Resume Scorecard per job (F2)

**Endpoint:** `GET /api/jobs/{id}/scorecard`
- **Behavior:**
  1. Load job + profile. 404 if job missing.
  2. Run `_fit_components(title, description, job_skills, profile_skills,
     target_role)` → `matched`, `missing`, `job_expanded`, `profile_expanded`.
  3. `coverage_pct` = `len(job_expanded & profile_expanded) / len(job_expanded)
     * 100` (50.0 neutral when job lists no skills).
  4. `matched_skills` = sorted(matched), each flagged `core` if in
     `_MUST_HAVE`.
  5. **`resume_gap`** = job skills that are NOT in `profile_expanded` AND NOT
     present in `profile.resume_text` (tokenized). This is the actionable
     "add to your resume" list.
  6. `suggestions` = deterministic strings, e.g. "Add 'Tableau' to your resume
     — it's a core skill for this role." (only for core gaps first, then others,
     capped at 5).
- **Response shape:**
  ```json
  {
    "coverage_pct": 66.7,
    "matched_skills": [{"skill": "sql", "core": true}, ...],
    "missing_skills": ["tableau"],
    "resume_gap": ["tableau", "power bi"],
    "suggestions": ["Add 'Tableau' to your resume — core skill for this role."]
  }
  ```
- **Frontend:** "Resume fit" panel in the job detail modal — coverage bar,
  matched chips (green, core starred), resume-gap chips (amber), suggestions
  list.
- **No model changes.**

### FR-3 — Skill Gap Analysis (F3)

**Endpoint:** `GET /api/analytics/skills?work_mode=&source=`
- **Behavior:**
  1. Tokenize every job's `skills` list (lowercase, trimmed, deduped).
  2. Frequency count across all (filtered) jobs.
  3. `top_requested` = top N (default 15) by frequency: `[{skill, count}]`.
  4. `you_are_missing` = top-requested skills NOT in the user's
     `profile.skills` (expanded via `_expand`), sorted by frequency desc.
  5. `your_skills_by_demand` = the user's skills ranked by their frequency in
     the market (include 0-count skills at the end).
  6. `coverage_pct` = (user skills that appear in the market) / (user skills)
     * 100.
- **Response shape:**
  ```json
  {
    "top_requested": [{"skill": "sql", "count": 140}, ...],
    "you_are_missing": [{"skill": "tableau", "count": 60}, ...],
    "your_skills_by_demand": [{"skill": "sql", "count": 140}, ...],
    "coverage_pct": 78.0
  }
  ```
- **Frontend:** "Skills" section on Analytics — two `hbarChart`s (top-requested,
  your skills by demand) + a "you're missing" list with an "add to my skills"
  button per item (calls `PUT /api/profile` with the updated skills list, then
  `doRescore()`).
- **No model changes.**

### FR-4 — Source Health (F4)

**Endpoint:** `GET /api/analytics/sources`
- **Behavior:** For each distinct `ScrapeRun.source`:
  1. `last_scan` = max `started_at`; `last_status` = that run's status.
  2. `total_scans` = count of runs.
  3. `success_rate` = (runs with status `done`) / total * 100.
  4. `avg_fetched` = mean `fetched` over runs.
  5. `error_count` = runs with non-null `error`.
  6. `sparkline` = `fetched` over the last N (default 10) runs, oldest→newest.
  7. `health` = `green` if success_rate ≥ 80 and last_status `done`; `amber`
     if success_rate ≥ 50; else `red`.
- **Response shape:**
  ```json
  {
    "sources": [
      {"source": "remotive", "last_scan": "2026-07-10T06:00:00Z",
       "last_status": "done", "total_scans": 42, "success_rate": 97.6,
       "avg_fetched": 88.2, "error_count": 1,
       "sparkline": [90, 85, 92, ...], "health": "green"}
    ]
  }
  ```
- **Frontend:** "Sources" panel on Analytics — a card per source with a health
  dot, last-scan time, success rate, and a mini trend line (SVG polyline).
- **No model changes.**

### FR-5 — Form Completeness Meter (F5)

**Endpoint:** extend `GET /api/jobs/{id}/application-form`
- **Behavior:** After building the form dict, compute:
  - `required = ["name", "email", "phone", "expected_salary"]`.
  - `filled` = count of required keys with a non-empty value.
  - `total` = len(required).
  - `pct` = filled / total * 100.
  - `missing_required` = required keys that are empty.
  - Add `completeness = {filled, total, pct, missing_required}` to the response.
- **Frontend:** Thin progress bar at the top of the form panel + "N required
  fields missing: name, phone" hint.
- **No model changes.**

### FR-6 — Kanban Pipeline Board (F6)

**Endpoint:** `POST /api/jobs/{id}/status`  body `{"status": "<one of>"}`
- Valid statuses: `new`, `review`, `approved`, `rejected`. (Application-level
  statuses like `submitted`/`ready` are managed by the submission pipeline, not
  this endpoint.)
- **Behavior:** Validate status against the enum; 422 if invalid. Set
  `job.status`, commit, return `_detail(job)`.
- **Frontend:** New "Pipeline" view (add to `TITLES`, nav, `renderCurrent`).
  Columns = the 4 statuses. Each card shows title, company, confidence chip,
  salary. Native HTML5 drag-and-drop (`draggable`, `dragstart`, `dragover`,
  `drop`). Optimistic UI: move the card immediately, call the endpoint, roll
  back + toast on error.
- **No model changes** (`status` exists and is indexed).

### FR-7 — Side-by-Side Comparison (F7)

**Endpoint:** `GET /api/jobs/compare?ids=1,2,3`
- **Behavior:**
  1. Parse `ids` (comma-separated ints). 422 if empty or > 5.
  2. For each existing job, build a normalized row:
     - `id`, `title`, `company`, `salary` (raw + `_salary_value` normalized),
     - `confidence`, `factors` (the 6 factor values from
       `confidence_breakdown.factors`), `eligibility`,
     - `work_mode`, `company_overall` (companies.py), `matched_skills`,
       `missing_skills`, `posted_date`, `application_method`.
  3. Compute per-metric `best` id: highest confidence, highest eligibility,
     highest normalized salary, highest company_overall, fewest missing_skills.
- **Response shape:**
  ```json
  {
    "jobs": [ {id, title, company, salary, salary_value, confidence,
               factors: {role_fit: 80, ...}, eligibility, work_mode,
               company_overall, matched_skills, missing_skills, posted_date,
               application_method}, ... ],
    "best": {"confidence": 2, "eligibility": 2, "salary": 1,
             "company": 3, "skills": 2}
  }
  ```
- **Frontend:** Checkbox on each job row; a floating "Compare (n)" button
  appears when n ≥ 2; opens a comparison table (jobs = columns, metrics =
  rows) with winner cells highlighted; a remove button per column.
- **No model changes.**

### FR-8 — Application Timeline (F8)

**Endpoint:** `GET /api/jobs/{id}/timeline`
- **Behavior:** Derive ordered events from existing `Application` + `Job`
  fields (no new table required for MVP):
  - `created` (job.created_at) — "Job discovered".
  - `materials` (application.created_at) — "Application package created".
  - `ready` (when status first became ready — approximate with
    application.updated_at if resume exists) — "Package ready".
  - `attempt` (application.last_attempt_at, count = attempts) — "Submission
    attempt #n".
  - `submitted` (application.submitted_at) — "Submitted".
  - `failed` (if submission_status == failed) — "Submission failed".
  Sort by timestamp asc; include only events with a non-null timestamp.
- **Response shape:**
  ```json
  {"events": [{"type": "created", "at": "...", "label": "Job discovered"}, ...]}
  ```
- **Frontend:** Vertical timeline in the job detail (icon + timestamp + label).
- **No model changes** (optional `ApplicationEvent` table deferred).

### FR-9 — Follow-up Email Generator (F9)

**Endpoint:** `GET /api/jobs/{id}/followup`
- **Behavior:** Requires an application with `submitted_at`. 404/409 if none.
  Deterministic template using `profile.name`, `job.title`, `job.company`, and
  `days_since = (now - submitted_at).days`. Returns `subject` + `body`.
- **Response shape:**
  ```json
  {"subject": "Following up — Business Analyst at Acme",
   "body": "Hi,\n\nI applied for the Business Analyst role at Acme 12 days ago...",
   "days_since": 12}
  ```
- **Frontend:** "Draft follow-up" button on submitted applications → modal with
  subject + body + copy-to-clipboard.
- **No model changes.**

### FR-10 — Saved Filter Chips (F10)  *(model change)*

**Model:** Add `saved_filters: Mapped[list | None]` (JSON) to `Profile`.
Each entry: `{name, status, work_mode, source, min_salary, company, search}`.
- **Endpoints:**
  - `GET /api/profile/filters` → `{"filters": [...]}`.
  - `PUT /api/profile/filters` body `{"filters": [...]}` → replace list.
  - (Alternatively fold into `ProfileIn`; the dedicated endpoints are preferred
    for clarity.)
- **Frontend:** On the Jobs view, "Save current filters" button → prompt for a
  name → store the current filter state. Render saved filters as chips above
  the list; clicking a chip applies it; an × removes it.
- **Migration:** `Database.migrate()` adds the column (idempotent, nullable).

### FR-11 — Fit Trend Over Time (F11)  *(model change)*

**Model:** Add `avg_confidence: Mapped[float | None]` and
`avg_eligibility: Mapped[float | None]` to `ScrapeRun`.
- **Behavior:** At the end of each `run_source` (and after a full rescore),
  compute the mean confidence/eligibility of the jobs affected and store on the
  run. For rescore (which has no single run), create/update a synthetic
  `ScrapeRun(source="rescore", ...)` row.
- **Endpoint:** `GET /api/analytics/trend` →
  ```json
  {"points": [{"at": "2026-07-01T06:00:00Z", "avg_confidence": 71.2,
               "avg_eligibility": 64.0, "source": "remotive"}, ...]}
  ```
  (chronological, last 30 points).
- **Frontend:** Line chart on Analytics (SVG polyline, two series).
- **Migration:** `Database.migrate()` adds both columns (nullable).

### FR-12 — Resume Variants (F12)  *(model change)*

**Model:** Add `resume_variants: Mapped[list | None]` (JSON) to `Profile`.
Each entry: `{name, text, skills}`. (A `ResumeVariant` table is an acceptable
alternative; JSON is simpler for a single user.)
- **Endpoints:**
  - `GET /api/profile/resume-variants` → `{"variants": [...]}`.
  - `PUT /api/profile/resume-variants` body `{"variants": [...]}`.
- **Behavior:** `POST /api/jobs/{id}/generate?variant=<name>` and
  `_ensure_materials` accept an optional variant name; when provided, build
  `ResumeData` from the variant's `text`/`skills` instead of the base profile.
- **Frontend:** Variant manager on the Profile tab (add/edit/delete); a variant
  picker in the job detail before generating.
- **Migration:** `Database.migrate()` adds the column (nullable).

### FR-13 — Cover-letter Personalization + Score (F13)

**Behavior:** Extend `_cover_letter(profile, job)`:
  1. Deterministically extract 2–3 job-specific phrases from `job.description`
     and `job.skills` (e.g., the top skill tokens and a key responsibility
     phrase) and insert them into template slots. No LLM.
  2. Compute `personalization_score` = (job-specific tokens referenced in the
     letter) / (total distinct job tokens) * 100, clamped 0–100.
  3. Return the letter text; expose the score via the generate/materials
     response and the application-form response.
- **Frontend:** Score badge in the job detail + a "Regenerate" button.
- **No model changes.**

### FR-14 — Data Export / Import (F14)

**Endpoints:**
- `GET /api/export/jobs?format=csv|json` — all jobs (full fields).
- `GET /api/export/applications?format=csv|json` — applications joined to job
  title/company.
- `GET /api/export/analytics?format=json` — the `/api/analytics` payload.
- `POST /api/import/jobs` body = JSON array of job objects.
  - Validate each row (title + company required).
  - Dedup by `fingerprint(title, company, url)` against existing.
  - Insert new rows with `status="new"`, `source="import"`.
  - Return `{imported, skipped, errors: [{row, reason}]}`.
- **Frontend:** Export menu (CSV/JSON) on Jobs/Applications/Analytics; an
  Import button with a file picker on the Jobs view.
- **No model changes.**

### FR-15 — New Source Adapters + Registry (F15)

**Adapters** (each a `BaseAdapter` subclass returning the normalized job dict):
| Source | Endpoint | Notes |
|--------|----------|-------|
| Lever | `api.lever.co/v0/postings/{company}?mode=json` | company slug required |
| Ashby | `api.ashbyhq.com/posting-api/job-board/{org}` | org slug required |
| Workable | `apply.workable.com/api/v1/accounts/{company}/jobs` | account slug |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/{company}/postings` | company slug |
| Workday | `api.workday.com/gateway/external/{company}/jobs` | tenant slug |
| RemoteOK | `remoteok.com/api` | no key |
| WWR | `weworkremotely.com/categories/remote-jobs.rss` | RSS → parse |
| The Muse | `api.themuse.com/api/public/jobs?company=&q=` | no key |
| Adzuna | `api.adzuna.com/v1/api/jobs/search` | free key, strong BD/Asia |

**Registry:** A JSON file (or `Source` table) mapping source → enabled flag +
slugs/keys. `build_adapters(config)` reads the registry and instantiates only
enabled sources. Each adapter isolates network errors (one bad source never
kills a run).
- **No breaking model changes** (registry may be a JSON file first).

### FR-16 — Bangladesh Board Scrapers (F16)

**Adapters:** bdjobs.com, career.com.bd, jobsinbd.com via Playwright.
- **Politeness (C6):** respect robots.txt, rate-limit 1 req/sec/domain, cache
  responses, store a hash of the raw response for change detection.
- **Normalization:** extract BDT salary strings (e.g., "৳ 80,000 - 1,20,000")
  into `salary`; `_salary_value()` must be extended to handle BDT (treat as
  local currency, keep in thousands of BDT, flagged).
- **Failure mode:** any scrape error → `RunSummary.error`, status `error`.

### FR-17 — Scheduler + Enrichment (F17)

- **Scheduler:** APScheduler (BackgroundScheduler) triggers `run_all` on a
  daily interval (configurable). Runs are recorded as `ScrapeRun` rows.
- **Enrichment (deterministic, no LLM):**
  - Wikidata (no key): company HQ, founded, employees, industry.
  - O*NET (no key): skill taxonomy to normalize skill names.
  - trafilatura: main-content extraction from job pages.
  - tenacity: retry/backoff for flaky HTTP.
- **Avoid:** LinkedIn, Indeed, Glassdoor, ZipRecruiter (no public API,
  anti-bot, ToS violations).

---

## 3. Non-Functional Requirements
| ID | Requirement |
|----|-------------|
| NFR-1 | **Determinism:** identical inputs → identical outputs; no wall-clock in scores. |
| NFR-2 | **No fake data:** empty results return empty structures, never synthetic rows. |
| NFR-3 | **Explainability:** every score exposes a plain-language reason. |
| NFR-4 | **Resilience:** one failing source/record never crashes a scan or request. |
| NFR-5 | **Idempotent migrations:** `Database.migrate()` is safe to run repeatedly. |
| NFR-6 | **Performance:** analytics endpoints < 500 ms on a 1k-job DB. |
| NFR-7 | **Security:** all `/api/*` (except login) require a valid Bearer token. |
| NFR-8 | **Portability:** export/import round-trips jobs without data loss. |

---

## 4. API Surface (new endpoints, v2.3)
| Method | Path | Feature |
|--------|------|---------|
| GET | `/api/analytics/salary` | F1 |
| GET | `/api/jobs/{id}/scorecard` | F2 |
| GET | `/api/analytics/skills` | F3 |
| GET | `/api/analytics/sources` | F4 |
| GET | `/api/jobs/{id}/application-form` (extended) | F5 |
| POST | `/api/jobs/{id}/status` | F6 |
| GET | `/api/jobs/compare` | F7 |
| GET | `/api/jobs/{id}/timeline` | F8 |
| GET | `/api/jobs/{id}/followup` | F9 |
| GET/PUT | `/api/profile/filters` | F10 |
| GET | `/api/analytics/trend` | F11 |
| GET/PUT | `/api/profile/resume-variants` | F12 |
| (extended) | `/api/jobs/{id}/generate`, application-form | F13 |
| GET | `/api/export/jobs`, `/api/export/applications`, `/api/export/analytics` | F14 |
| POST | `/api/import/jobs` | F14 |
| (new adapters) | — | F15, F16 |
| (scheduler) | — | F17 |

---

## 5. Data Model Changes (v2.3)
| Table | Column | Type | Feature |
|-------|--------|------|---------|
| `Profile` | `saved_filters` | JSON (nullable) | F10 |
| `ScrapeRun` | `avg_confidence` | Float (nullable) | F11 |
| `ScrapeRun` | `avg_eligibility` | Float (nullable) | F11 |
| `Profile` | `resume_variants` | JSON (nullable) | F12 |

All added via idempotent `ALTER TABLE ... ADD COLUMN` in `Database.migrate()`.

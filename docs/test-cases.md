# ZEYRECUITE — Test Cases (v2.4)

Companion to `PRD.md`, `SRS.md`, `user-stories.md`. Each case: **ID**,
**feature**, **precondition**, **steps**, **expected result**, **type**
(unit / API / frontend-UAT). IDs map to features (F#) and user stories (US#).

**Scope note (v2.4):** F16 (Bangladesh boards) is **DROPPED** per product
decision — it conflicts with the app's South-Asia exclusion policy. All
F16 cases are removed. F15 and F17 now include frontend UAT cases for the
UI wired in v2.4 (Enrich button, Company facts panel, scheduler + registry
cards on Analytics).

**Test command:** `cd backend; & "..\.venv\Scripts\python.exe" -m pytest tests -q`
→ **131 passed** (96 baseline + 35 in `tests/test_v24_features.py`).
**Server:** from `backend/`: `& "..\.venv\Scripts\python.exe" -m zeyrecuite.app`
(app is a `create_app()` factory — do NOT run `uvicorn zeyrecuite.app:app`).
**Auth:** `POST /api/auth/login` with `admin` / `zeyrecuite` → Bearer token.
**Error standard:** all errors return a plain FastAPI body `{"detail": "<message>"}` with the correct HTTP status (401 / 404 / 422 / 409). There is no custom `error_code` envelope.

---

## Phase 1

### F1 — Salary Insights (US-01)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-1.1 | API | 3 jobs with salaries "120k", "$90,000", "8000/mo" | `GET /api/analytics/salary` | `count=3`; values normalized to thousands (120, 90, 96); `median`, `min`, `max` correct |
| TC-1.2 | API | Same as TC-1.1 | Inspect histogram | ~10 buckets; bucket counts sum to `count` |
| TC-1.3 | API | Profile `expected_salary="90k"`; jobs as TC-1.1 | `GET /api/analytics/salary` | `user_value=90`; `user_percentile` between 0–100 and consistent with ordering |
| TC-1.4 | API | No jobs have parseable salaries | `GET /api/analytics/salary` | `count=0`; stats null; empty histogram; `user_percentile` null (no fake data) |
| TC-1.5 | API | Jobs across work modes | `GET /api/analytics/salary?work_mode=remote` | Only remote jobs counted; `by_work_mode` present |
| TC-1.6 | API | No auth | `GET /api/analytics/salary` | 401 |
| TC-1.7 | UAT | Logged in, jobs present | Open Analytics → Salary section | Histogram renders; stats row shows median/p25/p75/count; "you vs market" gauge shows percentile |

### F2 — Resume Scorecard (US-02)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-2.1 | API | Job skills `[sql, excel, tableau]`; profile skills `[sql, excel]`; resume_text lacks tableau | `GET /api/jobs/{id}/scorecard` | `coverage_pct ≈ 66.7`; `matched_skills` includes sql, excel; `resume_gap` includes tableau |
| TC-2.2 | API | Job has a core skill (e.g. sql) matched | Inspect `matched_skills` | The core skill is flagged `core: true` |
| TC-2.3 | API | Job lists no skills | `GET /api/jobs/{id}/scorecard` | `coverage_pct = 50.0` (neutral); no crash |
| TC-2.4 | API | Job id does not exist | `GET /api/jobs/999999/scorecard` | 404 |
| TC-2.5 | API | Resume gap non-empty | Inspect `suggestions` | Non-empty, ≤ 5, references the gap skills |
| TC-2.6 | UAT | Open a job with skills | View "Resume fit" panel | Coverage bar, matched chips (core starred), resume-gap chips, suggestions list |

### F3 — Skill Gap Analysis (US-03)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-3.1 | API | Jobs with skills; profile skills `[sql]` | `GET /api/analytics/skills` | `top_requested` sorted by count desc; `your_skills_by_demand` includes sql |
| TC-3.2 | API | A top skill not in profile | Inspect `you_are_missing` | That skill appears, ranked by frequency |
| TC-3.3 | API | Profile skills all present in market | Inspect `coverage_pct` | 0–100; equals (present/total)*100 |
| TC-3.4 | API | No jobs | `GET /api/analytics/skills` | Empty lists; `coverage_pct` 0; no crash |
| TC-3.5 | API | Filter by source | `GET /api/analytics/skills?source=remotive` | Only remotive jobs counted |
| TC-3.6 | UAT | Open Analytics → Skills | Click "add to my skills" on a missing skill | Profile PUT fires; skill appears in profile; rescore runs |

### F4 — Source Health (US-04)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-4.1 | API | 3 runs for source "remotive" (2 done, 1 error) | `GET /api/analytics/sources` | `total_scans=3`; `success_rate ≈ 66.7`; `error_count=1`; `health` amber |
| TC-4.2 | API | All runs done | Inspect `health` | `green` |
| TC-4.3 | API | Runs with fetched values | Inspect `sparkline` | Length ≤ 10, oldest→newest, matches run order |
| TC-4.4 | API | No runs | `GET /api/analytics/sources` | `sources: []` |
| TC-4.5 | UAT | Open Analytics → Sources | View cards | One card per source with health dot, last scan, success rate, mini trend |

### F5 — Form Completeness (US-05)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-5.1 | API | Profile has name+email but no phone/salary | `GET /api/jobs/{id}/application-form` | `completeness.filled=2`, `total=4`, `pct=50`, `missing_required` lists phone, expected_salary |
| TC-5.2 | API | All required filled | Inspect `completeness` | `pct=100`, `missing_required=[]` |
| TC-5.3 | API | Job id missing | `GET /api/jobs/999999/application-form` | 404 |
| TC-5.4 | UAT | Open a job with partial form | View form panel | Progress bar at correct width; "N required fields missing" hint |

---

## Phase 2

### F6 — Kanban Board (US-06)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-6.1 | API | Job status `new` | `POST /api/jobs/{id}/status` `{"status":"approved"}` | 200; job.status `approved` |
| TC-6.2 | API | Job status `approved` | `POST .../status` `{"status":"new"}` | 200; moves back to `new` (any-lane allowed) |
| TC-6.3 | API | Invalid status | `POST .../status` `{"status":"bogus"}` | 422 |
| TC-6.4 | API | Job id missing | `POST /api/jobs/999999/status` | 404 |
| TC-6.5 | API | No auth | `POST .../status` | 401 |
| TC-6.6 | UAT | Jobs in multiple statuses | Open Pipeline view | 4 columns; cards show title/company/confidence/salary |
| TC-6.7 | UAT | Drag a card to another column | Drop | Card moves instantly (optimistic); persists after reload |
| TC-6.8 | UAT | Simulate a failed move | Drop (server rejects) | Card rolls back; error toast |

### F7 — Comparison (US-07)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-7.1 | API | 3 jobs | `GET /api/jobs/compare?ids=1,2,3` | `jobs` length 3; each has confidence, factors (6), eligibility, salary, work_mode, company_overall, skills |
| TC-7.2 | API | Same | Inspect `best` | `best.confidence` is the id with max confidence; `best.salary` is max normalized salary |
| TC-7.3 | API | Empty ids | `GET /api/jobs/compare?ids=` | 422 |
| TC-7.4 | API | > 5 ids | `GET /api/jobs/compare?ids=1,2,3,4,5,6` | 422 |
| TC-7.5 | API | One id missing | `GET /api/jobs/compare?ids=1,999999` | Missing id omitted; no crash |
| TC-7.6 | UAT | Select 2+ jobs | Click "Compare (n)" | Table opens; jobs as columns, metrics as rows; best cells highlighted |
| TC-7.7 | UAT | In comparison | Remove a column | Table re-renders without that job |

### F8 — Timeline (US-08)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-8.1 | API | Job with a submitted application | `GET /api/jobs/{id}/timeline` | Events include created, materials, submitted; sorted asc |
| TC-8.2 | API | Job with no application | `GET /api/jobs/{id}/timeline` | At least the `created` event; no crash |
| TC-8.3 | API | Job id missing | `GET /api/jobs/999999/timeline` | 404 |
| TC-8.4 | UAT | Open a submitted job | View timeline | Vertical list with icon + timestamp + label per event |

### F9 — Follow-up Email (US-09)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-9.1 | API | Submitted application (submitted_at set) | `GET /api/jobs/{id}/followup` | `subject` + `body` non-empty; `days_since` ≥ 0; body references name, title, company |
| TC-9.2 | API | No application / not submitted | `GET /api/jobs/{id}/followup` | 404 or 409 (clear message) |
| TC-9.3 | API | Job id missing | `GET /api/jobs/999999/followup` | 404 |
| TC-9.4 | UAT | Open a submitted job | Click "Draft follow-up" | Modal shows subject + body; copy button copies to clipboard |

### F10 — Saved Filters (US-10)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-10.1 | API | — | `PUT /api/profile/filters` `{"filters":[{"name":"Remote","status":"new","work_mode":"remote"}]}` | 200; persisted |
| TC-10.2 | API | After TC-10.1 | `GET /api/profile/filters` | Returns the saved filter |
| TC-10.3 | API | — | `PUT /api/profile/filters` `{"filters":[]}` | 200; list cleared |
| TC-10.4 | Migration | Existing DB without column | Start app | `migrate()` adds `saved_filters` column; no error; idempotent on 2nd run |
| TC-10.5 | UAT | Jobs view with a filter active | Click "Save current filters", name it | Chip appears; clicking re-applies; × removes |

---

## Phase 3

### F11 — Fit Trend (US-11)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-11.1 | API | Run a scan | `GET /api/analytics/trend` | New point with `avg_confidence`/`avg_eligibility` for that run |
| TC-11.2 | API | Multiple runs over time | Inspect `points` | Chronological; ≤ 30 points |
| TC-11.3 | API | No runs | `GET /api/analytics/trend` | `points: []` |
| TC-11.4 | Migration | Existing DB | Start app | `migrate()` adds both columns; idempotent |
| TC-11.5 | UAT | Open Analytics | View trend chart | Line chart with two series (confidence, eligibility) |

### F12 — Resume Variants (US-12)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-12.1 | API | — | `PUT /api/profile/resume-variants` `{"variants":[{"name":"Data","text":"...","skills":["sql"]}]}` | 200; persisted |
| TC-12.2 | API | After TC-12.1 | `GET /api/profile/resume-variants` | Returns the variant |
| TC-12.3 | API | Variant "Data" exists | `POST /api/jobs/{id}/generate?variant=Data` | Generated resume uses variant text/skills |
| TC-12.4 | API | Unknown variant | `POST /api/jobs/{id}/generate?variant=Nope` | Falls back to base profile (or 404 with clear message) |
| TC-12.5 | Migration | Existing DB | Start app | `migrate()` adds `resume_variants`; idempotent |
| TC-12.6 | UAT | Profile tab | Add/edit/delete a variant | CRUD works; picker appears in job detail |

### F13 — Cover-letter Personalization (US-13)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-13.1 | API | Job with description + skills | `POST /api/jobs/{id}/generate` | Cover letter contains 2–3 job-specific phrases; `personalization_score` 0–100 |
| TC-13.2 | API | Job with no description/skills | Generate | Letter still produced; score low but not crashing |
| TC-13.3 | Determinism | Same job + profile | Generate twice | Identical letter + score (no LLM, no randomness) |
| TC-13.4 | UAT | Open a job | View score badge + Regenerate | Badge shows score; regenerate updates letter |

### F14 — Export / Import (US-14)

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-14.1 | API | Jobs exist | `GET /api/export/jobs?format=json` | JSON array with full job fields |
| TC-14.2 | API | Jobs exist | `GET /api/export/jobs?format=csv` | CSV with header + one row per job |
| TC-14.3 | API | Applications exist | `GET /api/export/applications?format=json` | Applications joined to job title/company |
| TC-14.4 | API | — | `GET /api/export/analytics?format=json` | Same shape as `/api/analytics` |
| TC-14.5 | API | Export a set, then import it | `POST /api/import/jobs` body `{"jobs": [...]}` | `skipped` = duplicates (fingerprint match); `imported` = 0 for exact re-import |
| TC-14.6 | API | Import with a new job | `POST /api/import/jobs` body `{"jobs": [newRow]}` | `imported` ≥ 1; new row `status=new`, `source=import` |
| TC-14.7 | API | Import a row missing title | `POST /api/import/jobs` | Row in `errors` with reason; others still imported |
| TC-14.8 | API | No auth | `GET /api/export/jobs` | 401 |
| TC-14.9 | UAT | Jobs view | Export CSV/JSON; import a file | Downloads work; import reports imported/skipped/errors |

---

## Phase 4

### F15 — New Source Adapters + Registry (US-15)

Backend: `registry.py` (`load_registry`, `source_enabled`, `source_entry`;
user-editable `backend/sources.json`) + 9 adapters in `adapters.py`
(Lever, Ashby, Workable, SmartRecruiters, Workday, RemoteOK, WWR RSS,
TheMuse, Adzuna). `build_adapters(config)` = remotive/greenhouse (legacy
config) + registry-driven sources (only if enabled AND has required
slugs/keys). Default-enabled: remoteok, weworkremotely, themuse.

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-15.1 | Unit | Fake httpx client returning Lever JSON | `LeverAdapter().fetch(client=fake)` | Normalized dicts with title/company/url/salary/source |
| TC-15.2 | Unit | Fake client for Ashby/Workable/SmartRecruiters/Workday/RemoteOK/WWR/TheMuse/Adzuna | Each `.fetch(client=fake)` | Normalized dicts; bad records skipped, not raised |
| TC-15.3 | Unit | A source returns malformed JSON | `.fetch(client=fake)` | Returns `[]` or skips bad records; no exception |
| TC-15.4 | Unit | Registry with a source enabled but missing required slugs/keys | `build_adapters(config)` | Source NOT instantiated (enabled alone is not enough) |
| TC-15.5 | Unit | Registry disables a source | `build_adapters(config)` | Disabled source not instantiated |
| TC-15.6 | API | — | `GET /api/sources` | 200; `sources` map matches `sources.json` (incl. `_comment`); each entry has `enabled` |
| TC-15.7 | API | No auth | `GET /api/sources` | 401 |
| TC-15.8 | API | Registry enables a new source with slugs | `POST /api/scan` | New source appears in runs; jobs gated/deduped/scored like others |
| TC-15.9 | API | One source errors mid-run | `POST /api/scan` | That run has `status=error`; other sources still complete |
| TC-15.10 | UAT | Logged in | Open Analytics → "Source registry" card | One row per source with on/off badge; enabled sources show their slugs/query; `_comment` hidden |

### F16 — Bangladesh Boards — **DROPPED**

Removed in v2.4 per product decision ("no south asian jobs"): conflicts
with the app's South-Asia exclusion policy. No code, no tests.

### F17 — Scheduler + Enrichment (US-17)

Backend: `enrich.py` (tenacity retry, Wikidata enrichment with Q-id label
resolution, O*NET-derived skill normalization, trafilatura main-content
extraction), `scheduler.py` (APScheduler `BackgroundScheduler` wrapper),
`SchedulerConfig` in `config.py` (`scheduler:` YAML block), endpoints
`GET /api/scheduler`, `POST /api/enrich?limit=N`, `Job.company_facts` JSON
column (auto-migrated).

| ID | Type | Precondition | Steps | Expected |
|----|------|--------------|-------|----------|
| TC-17.1 | Unit | Scheduler configured with a short interval (`0.001`h) | Start scheduler | A scan runs automatically and is recorded (mocked `run_all`) |
| TC-17.2 | Unit | Scheduler already running | `start()` again | No-op; no duplicate job |
| TC-17.3 | Unit | — | `status()` | `{"enabled", "running", "interval_hours", "next_run"}`; `next_run` ISO string when running, else null |
| TC-17.4 | Unit | Fake Wikidata claims (Q-id only) + labels | `enrich_company("Acme", client=fake)` | HQ/founded/employees/industry populated with resolved labels, not Q-ids |
| TC-17.5 | Unit | Wikidata search returns no match | `enrich_company("Unknown Co", client=fake)` | `{}` (no crash, no fake facts) |
| TC-17.6 | Unit | Skill "PowerBI" / "k8s" / "stakeholders" | `normalize_skill` | Mapped to canonical "Power BI" / "Kubernetes" / "Stakeholder Management" |
| TC-17.7 | Unit | Skills `["SQL", "sql", "Excel"]` | `normalize_skills` | Case-insensitive dedup; order preserved |
| TC-17.8 | Unit | Flaky HTTP (fails N times then succeeds) | `get_json_with_retry` | Retries with backoff; succeeds on attempt N+1 |
| TC-17.9 | Unit | Flaky HTTP exhausts all attempts | `get_json_with_retry` | Raises `httpx.HTTPError` (reraise) |
| TC-17.10 | Unit | Sample HTML page with nav/footer | `extract_main_content` | Main content returned; nav/footer excluded |
| TC-17.11 | API | — | `GET /api/scheduler` | 200; matches config (e.g. `enabled:false, running:false, interval_hours:24, next_run:null`) |
| TC-17.12 | API | No auth | `GET /api/scheduler` | 401 |
| TC-17.13 | API | Jobs with unnormalized skills | `POST /api/enrich?limit=N` | `{"enriched": N}`; job skills normalized in place; `company_facts` set when Wikidata resolves |
| TC-17.14 | API | Same company appears in multiple jobs | `POST /api/enrich` | Company fetched once per request (per-request cache); all its jobs get the same facts |
| TC-17.15 | API | No auth | `POST /api/enrich` | 401 |
| TC-17.16 | UAT | Logged in | Click "✦ Enrich" in top bar | Button shows spinner "Enriching…"; on completion toast "Enriched N job(s)"; button re-enabled |
| TC-17.17 | UAT | Job has `company_facts` (e.g. Lemon.io) | Open job detail | "Company facts · Wikidata" panel shows HQ / Founded / Employees / Industry |
| TC-17.18 | UAT | Job has no `company_facts` | Open job detail | No Company facts panel rendered (not an empty box) |
| TC-17.19 | UAT | Logged in | Open Analytics → "Auto-scan scheduler" card | Running/Off badge, interval, enabled-in-config, next run; hint about `config.yaml` |

---

## Cross-cutting / regression

| ID | Type | Steps | Expected |
|----|------|-------|----------|
| TC-X.1 | API | Full existing suite | All 131 tests pass (96 baseline + 35 v2.4) — no regression |
| TC-X.2 | API | Every new endpoint without a token | 401 |
| TC-X.3 | API | Every new endpoint with a bad id | 404 (not 500) |
| TC-X.4 | API | Every new endpoint with invalid params | 422 with `{"detail": "..."}` |
| TC-X.5 | Determinism | Run any scoring/analytics endpoint twice with same data | Identical output |
| TC-X.6 | No-fake-data | Empty DB → hit every analytics endpoint | Honest empty structures, never synthetic rows |
| TC-X.7 | Migration | Start app on a v2.2 DB | `migrate()` adds new columns (incl. `company_facts`); app boots; data intact |
| TC-X.8 | UAT | Walk every view/panel in the browser | No console errors; all interactions work |
| TC-X.9 | API | Any validation error (bad body/params) | 422 with `{"detail": "<reason>"}` (e.g. `invalid status; must be one of [...]`) |
| TC-X.10 | API | Conflict (e.g. follow-up with no submitted application) | 409 with `{"detail": "..."}` |

---

## Coverage matrix

| Feature | Unit | API | UAT |
|---------|------|-----|-----|
| F1 Salary | — | TC-1.1–1.6 | TC-1.7 |
| F2 Scorecard | — | TC-2.1–2.5 | TC-2.6 |
| F3 Skills | — | TC-3.1–3.5 | TC-3.6 |
| F4 Sources | — | TC-4.1–4.4 | TC-4.5 |
| F5 Completeness | — | TC-5.1–5.3 | TC-5.4 |
| F6 Kanban | — | TC-6.1–6.5 | TC-6.6–6.8 |
| F7 Compare | — | TC-7.1–7.5 | TC-7.6–7.7 |
| F8 Timeline | — | TC-8.1–8.3 | TC-8.4 |
| F9 Follow-up | — | TC-9.1–9.3 | TC-9.4 |
| F10 Filters | — | TC-10.1–10.4 | TC-10.5 |
| F11 Trend | — | TC-11.1–11.4 | TC-11.5 |
| F12 Variants | — | TC-12.1–12.5 | TC-12.6 |
| F13 Cover letter | — | TC-13.1–13.3 | TC-13.4 |
| F14 Export/Import | — | TC-14.1–14.8 | TC-14.9 |
| F15 Adapters + registry | TC-15.1–15.5 | TC-15.6–15.9 | TC-15.10 |
| F16 BD boards | **DROPPED** | **DROPPED** | **DROPPED** |
| F17 Scheduler + enrichment | TC-17.1–17.10 | TC-17.11–17.15 | TC-17.16–17.19 |
| Cross-cutting | — | TC-X.1–X.7, X.9–X.10 | TC-X.8 |

# ZEYRECUITE — User Stories (v2.4)

Format: **As a** <role>, **I want** <capability>, **so that** <benefit>.
Each story lists its feature ID (F#), priority, and acceptance criteria (AC).
Priority: **P1** = must-have, **P2** = should-have, **P3** = nice-to-have.

**Role:** the candidate (single user, "Nafiz").

**Scope note (v2.4):** US-16 (F16, Bangladesh boards) is **DROPPED** per product
decision — it conflicts with the app's South-Asia exclusion policy. US-15 (F15)
and US-17 (F17) now include the frontend UI shipped in v2.4 (Enrich button,
Company facts panel, scheduler + registry cards on Analytics). US-18 (F18) is
the new **desktop app** packaging story (Windows + macOS).

---

## Phase 1 — Market intelligence & per-job explainability

### US-01 — Salary insights (F1) · P1
**As a** candidate, **I want** to see the salary distribution across the jobs I
collect and where my expected salary falls, **so that** I can judge whether my
ask is realistic before I apply.

**AC:**
- AC1.1: Analytics shows a salary histogram with min/p25/median/p75/max/mean.
- AC1.2: A "you vs market" gauge shows my expected salary's percentile.
- AC1.3: I can filter by work mode, source, or role.
- AC1.4: When no jobs have parseable salaries, the section shows an honest
  "no salary data" state (no fake numbers).

### US-02 — Resume scorecard (F2) · P1
**As a** candidate, **I want** a per-job scorecard showing how well my resume
covers the role's skills and exactly what's missing, **so that** I can tailor
my resume before applying.

**AC:**
- AC2.1: Job detail shows a coverage percentage for the role's skills.
- AC2.2: Matched skills are listed (core skills flagged).
- AC2.3: A "resume gap" lists job skills absent from both my resume text and
  my profile skills.
- AC2.4: Deterministic suggestions tell me what to add.

### US-03 — Skill gap analysis (F3) · P1
**As a** candidate, **I want** to know which skills are most in demand and which
ones I'm missing, **so that** I can focus my upskilling.

**AC:**
- AC3.1: Analytics shows the most-requested skills across all jobs.
- AC3.2: A "you're missing" list ranks in-demand skills I don't have.
- AC3.3: My own skills are ranked by market demand.
- AC3.4: I can add a missing skill to my profile with one click.

### US-04 — Source health (F4) · P2
**As a** candidate, **I want** to see which sources are working and how reliable
they are, **so that** I trust my pipeline and can disable broken sources.

**AC:**
- AC4.1: Analytics shows a card per source with a health indicator.
- AC4.2: Each card shows last scan time, success rate, avg fetched, and a trend.
- AC4.3: A source that keeps erroring is clearly flagged red.

### US-05 — Form completeness (F5) · P2
**As a** candidate, **I want** to know if my application form is complete before
I submit, **so that** I don't send an incomplete application.

**AC:**
- AC5.1: The form panel shows a completeness progress bar.
- AC5.2: It lists which required fields (name, email, phone, expected salary)
  are still missing.

---

## Phase 2 — Pipeline UX

### US-06 — Kanban board (F6) · P1
**As a** candidate, **I want** a drag-and-drop board of my jobs by status,
**so that** I can see my whole pipeline and re-triage quickly.

**AC:**
- AC6.1: A "Pipeline" view shows columns for New (Eligible), Review, Approved,
  Rejected.
- AC6.2: I can drag a job card between any two columns.
- AC6.3: The move is optimistic (instant) and rolls back with a message if the
  server rejects it.
- AC6.4: Each card shows title, company, confidence, and salary.

### US-07 — Job comparison (F7) · P1
**As a** candidate, **I want** to compare 2–5 jobs side by side, **so that** I
can pick the genuinely best fit.

**AC:**
- AC7.1: I can select multiple jobs and open a comparison.
- AC7.2: The table shows confidence, the 6 factors, eligibility, salary, work
  mode, company rating, and skill match per job.
- AC7.3: The best value per metric is highlighted.
- AC7.4: I can remove a job from the comparison.

### US-08 — Application timeline (F8) · P2
**As a** candidate, **I want** a timeline of what happened to each application,
**so that** I can recall when I applied and what the outcome was.

**AC:**
- AC8.1: Job detail shows a vertical timeline of events.
- AC8.2: Events include discovery, package creation, readiness, attempts, and
  submission.
- AC8.3: Each event has a timestamp and a plain label.

### US-09 — Follow-up email (F9) · P2
**As a** candidate, **I want** a ready-to-send follow-up email for a submitted
application, **so that** I can nudge the recruiter without writing from scratch.

**AC:**
- AC9.1: A "Draft follow-up" button appears on submitted applications.
- AC9.2: The draft references my name, the role, the company, and days since
  submission.
- AC9.3: I can copy the subject and body to the clipboard.

### US-10 — Saved filters (F10) · P2
**As a** candidate, **I want** to save and re-apply my favorite job filters,
**so that** I can get back to a view in one click.

**AC:**
- AC10.1: I can save the current filter set with a name.
- AC10.2: Saved filters appear as chips; clicking one applies it.
- AC10.3: I can delete a saved filter.
- AC10.4: Saved filters persist across sessions.

---

## Phase 3 — Data depth

### US-11 — Fit trend (F11) · P2
**As a** candidate, **I want** to see how my average fit changes over time,
**so that** I can tell whether refining my profile is helping.

**AC:**
- AC11.1: Analytics shows a line chart of average confidence over scans.
- AC11.2: Average eligibility is shown as a second series.
- AC11.3: Each scan/rescore records its averages.

### US-12 — Resume variants (F12) · P3
**As a** candidate, **I want** to keep multiple resume versions and pick one per
job, **so that** I can tailor my resume to different role types.

**AC:**
- AC12.1: I can create, edit, and delete named resume variants.
- AC12.2: I can choose a variant when generating materials for a job.
- AC12.3: The generated resume reflects the chosen variant's text and skills.
- AC12.4: The variants editor is a full-replace save (the whole list is
  submitted on save) and the UI warns before overwriting.

### US-13 — Cover-letter personalization (F13) · P2
**As a** candidate, **I want** my cover letter to reference the specific job and
to know how personalized it is, **so that** it doesn't look generic.

**AC:**
- AC13.1: The cover letter includes 2–3 job-specific phrases.
- AC13.2: A personalization score (0–100) is shown in the job detail.
- AC13.3: I can regenerate the letter.

### US-14 — Export / import (F14) · P2
**As a** candidate, **I want** to export my data and import jobs, **so that** I
can back up or move my data.

**AC:**
- AC14.1: I can export jobs, applications, and analytics as CSV or JSON.
- AC14.2: I can import jobs from a JSON file (body `{"jobs": [...]}`).
- AC14.3: Import dedups by fingerprint and reports imported/skipped/errors.

---

## Phase 4 — Source expansion & automation

### US-15 — More job sources (F15) · P1
**As a** candidate, **I want** more public job boards collected into the same
pipeline, **so that** I see more real opportunities.

**AC:**
- AC15.1: New sources (Lever, Ashby, Workable, SmartRecruiters, Workday,
  RemoteOK, WWR, The Muse, Adzuna) can be enabled via a JSON registry
  (`backend/sources.json`).
- AC15.2: Each source's jobs pass through the same gate → dedup → score →
  persist flow.
- AC15.3: A failing source is recorded as an error run without breaking others.
- AC15.4: `GET /api/sources` returns the registry (per-source enabled state,
  query, and required keys).
- AC15.5: The Analytics view shows a **Source registry** card listing every
  source with an on/off badge (skips `_comment` entries).
- AC15.6: A source with missing required keys is not activated even if enabled.

### US-16 — Bangladesh boards (F16) · **DROPPED**
**DROPPED in v2.4** per product decision ("no south asian jobs"): conflicts with
the app's South-Asia exclusion policy. No code, no tests.

### US-17 — Scheduler + enrichment (F17) · P2
**As a** candidate, **I want** my dashboard to update itself and enrich company
and skill data, **so that** I don't have to scan manually and my data is richer.

**AC:**
- AC17.1: A daily automatic scan runs (APScheduler) and is recorded when
  `scheduler.enabled: true` in `config.yaml`.
- AC17.2: Company facts (HQ, founded, size, industry) are enriched from
  Wikidata (Q-id claims resolved to labels).
- AC17.3: Skill names are normalized using the O*NET-derived taxonomy.
- AC17.4: Flaky HTTP calls retry with backoff (tenacity).
- AC17.5: `GET /api/scheduler` returns `{enabled, running, interval_hours,
  next_run}`; the Analytics view shows an **Auto-scan scheduler** card
  (Running/Off badge, interval, next run).
- AC17.6: A topbar **✦ Enrich** button runs `POST /api/enrich?limit=N` and
  toasts "Enriched N job(s)".
- AC17.7: Job detail shows a **Company facts · Wikidata** panel (HQ / Founded /
  Employees / Industry) when facts exist; no empty box when they don't.
- AC17.8: Enrichment is deterministic — no network, no facts → `{}` (no fake
  data).

---

## Phase 5 — Distribution

### US-18 — Desktop app (F18) · P1
**As a** candidate, **I want** ZEYRECUITE to run as a native desktop app on
Windows and macOS, **so that** I can double-click an icon instead of opening a
browser tab, and it works fully offline.

**AC:**
- AC18.1: A launcher starts the FastAPI server in-process and opens the UI in
  a native window (pywebview) at the local port.
- AC18.2: Windows build produces a single `ZEYRECUITE.exe` (PyInstaller) that
  runs with no Python installed.
- AC18.3: macOS build produces a `ZEYRECUITE.app` bundle that runs with no
  Python installed.
- AC18.4: The SQLite database, `config.yaml`, and `sources.json` are stored in
  a per-user app-data folder (portable, survives app updates).
- AC18.5: Closing the window stops the server cleanly (no orphan process, port
  released).
- AC18.6: If the port is already in use, the app shows a clear error and offers
  to open the existing instance in the browser.
- AC18.7: All existing features (F1–F17) work identically inside the desktop
  window as in the browser.
- AC18.8: The app works fully offline after first launch (no external calls
  except optional job-source/Wikidata fetches the user triggers).

---

## Story map (priority roll-up)
| Priority | Stories |
|----------|---------|
| P1 | US-01, US-02, US-03, US-06, US-07, US-15, US-18 |
| P2 | US-04, US-05, US-08, US-09, US-10, US-11, US-13, US-14, US-17 |
| P3 | US-12 |
| Dropped | US-16 (F16) |

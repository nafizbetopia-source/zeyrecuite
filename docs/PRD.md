# ZEYRECUITE — Product Requirements Document (PRD)

**Version:** 2.3 (feature expansion)
**Status:** Approved for implementation
**Last updated:** 2026-07-10
**Owner:** Product (single-user, local-first)

---

## 1. Product Overview

ZEYRECUITE is a **local-first, personal job-review dashboard** for a Business
Analyst / Data Analyst candidate. It collects real job postings from public
sources, scores each one against the user's real profile using a **deterministic,
explainable engine (no LLM, no external AI, $0)**, and prepares tailored
application materials (resume PDF, cover letter, interview prep, prefilled
application form).

The v2.3 expansion adds **analytics depth, pipeline UX, and source coverage**
while preserving every hard constraint of the product.

### 1.1 Hard constraints (non-negotiable)
| # | Constraint | Rationale |
|---|-----------|-----------|
| C1 | **Local-first SQLite** — no cloud DB, no external state | Privacy, offline, zero cost |
| C2 | **No LLM / no external AI APIs** — all logic deterministic | Reproducible, auditable, $0 |
| C3 | **Real data only** — no fake/seed fallbacks in results | Trust; the user works only with their own data |
| C4 | **Vanilla-JS SPA** — no frontend framework | Keep the bundle dependency-free |
| C5 | **Explainable scoring** — every score has a plain-language reason | The user must understand *why* a job ranked as it did |
| C6 | **Polite scraping** — respect robots.txt, rate-limit, cache, no ToS-violating sources | Legal/ethical |

### 1.2 Target user
A single candidate (the owner) who wants a morning review: *what's new, what
fits me, what should I apply to, and how do I look against the market?*

---

## 2. Goals & Non-Goals

### 2.1 Goals (v2.3)
1. **Market intelligence** — salary distribution, skill demand, source health,
   and fit-over-time so the user can make data-driven decisions.
2. **Per-job explainability** — a resume scorecard and cover-letter
   personalization score for every job.
3. **Pipeline UX** — a Kanban board, side-by-side comparison, and an
   application timeline to manage many jobs at once.
4. **Faster application** — form completeness meter, follow-up email drafts,
   saved filters, and resume variants.
5. **Data portability** — export/import of jobs, applications, and analytics.
6. **Wider coverage** — more public job-board adapters (Lever, Ashby, Workable,
   SmartRecruiters, Workday, RemoteOK, WWR, The Muse, Adzuna) + Bangladesh
   boards, plus a scheduler and enrichment.

### 2.2 Non-Goals
- No multi-tenant / multi-user collaboration.
- No auto-filling third-party ATS web forms (brittle + ToS risk).
- No paid/LLM-based personalization.
- No LinkedIn / Indeed / Glassdoor / ZipRecruiter scraping (no public API,
  anti-bot, ToS violations).
- No mobile-native app (responsive web only).

---

## 3. Personas & Jobs-to-be-Done

**Persona:** "Nafiz", a mid-level Business Analyst in Bangladesh seeking
remote roles worldwide.

| Job-to-be-done | Today (v2.2) | v2.3 improvement |
|----------------|--------------|------------------|
| "Show me what's new and worth my time" | Scan + top-10 | + source health, fit trend |
| "Am I competitive on salary?" | Manual guess | Salary insights + "you vs market" |
| "What skills do I need to learn?" | Manual | Skill gap analysis + quick-add |
| "How well does my resume match this job?" | Matched/missing chips | Resume scorecard + resume gap |
| "Which of these 3 jobs is best?" | Read one by one | Side-by-side comparison |
| "Where is each application?" | Status badge | Kanban + timeline |
| "Did I follow up?" | Memory | Follow-up email generator |
| "Is my data safe / portable?" | No | Export/import |

---

## 4. Feature Requirements (by phase)

Each feature lists: **ID**, **summary**, **user value**, **acceptance criteria
(high-level)**, and **phase**. Detailed functional specs live in `SRS.md`;
testable cases live in `test-cases.md`.

### Phase 1 — Quick wins (no model changes)

**F1. Salary Insights Dashboard**
- *Summary:* Aggregate salary data across jobs into a distribution and map the
  user's expected salary onto it.
- *Value:* "Is my $90k ask realistic for these roles?"
- *Acceptance:* A `GET /api/analytics/salary` returns count, min, p25, median,
  p75, max, mean, a ~10-bucket histogram, and the user's percentile. Analytics
  view shows a histogram, a stats row, and a "you vs market" gauge.
- *Phase:* 1

**F2. Resume Scorecard per job**
- *Summary:* Per-job breakdown of skill coverage, matched skills, and the
  **resume gap** (job skills absent from both the resume text and profile
  skills).
- *Value:* "Exactly what should I add to my resume for this role?"
- *Acceptance:* `GET /api/jobs/{id}/scorecard` returns coverage %, matched
  skills (core flagged), resume-gap list, and deterministic suggestions. Job
  detail shows a "Resume fit" panel.
- *Phase:* 1

**F3. Skill Gap Analysis**
- *Summary:* Frequency of skills across all jobs vs. the user's skills.
- *Value:* "Which skills are most in demand that I'm missing?"
- *Acceptance:* `GET /api/analytics/skills` returns top-requested skills,
  "you're missing" list, "your skills by demand" ranking, and coverage %.
  Analytics shows two bar charts + a gap list with an "add to my skills" action.
- *Phase:* 1

**F4. Source Health / scan diagnostics**
- *Summary:* Per-source reliability from scan history.
- *Value:* "Which sources are actually working for me?"
- *Acceptance:* `GET /api/analytics/sources` returns, per source: last scan
  time, last status, total scans, success rate, avg fetched, error count, and a
  sparkline of fetched over recent runs. Analytics shows a card per source with
  a health dot.
- *Phase:* 1

**F5. Application form completeness meter**
- *Summary:* How complete is the application form for a job.
- *Value:* "Am I missing anything before I submit?"
- *Acceptance:* `GET /api/jobs/{id}/application-form` adds a `completeness`
  object `{filled, total, pct, missing_required}` (required = name, email,
  phone, expected_salary). Form panel shows a progress bar + missing hint.
- *Phase:* 1

### Phase 2 — UX upgrades (mostly frontend)

**F6. Kanban Pipeline Board**
- *Summary:* Drag jobs between status lanes.
- *Value:* "See my whole pipeline at a glance and re-triage fast."
- *Acceptance:* `POST /api/jobs/{id}/status` moves a job to any valid status.
  A new "Pipeline" view renders columns per status with HTML5 drag-and-drop,
  optimistic UI, and rollback on error.
- *Phase:* 2

**F7. Side-by-Side Job Comparison**
- *Summary:* Compare 2–5 jobs on normalized metrics with winner highlights.
- *Value:* "Which of these is genuinely the best fit?"
- *Acceptance:* `GET /api/jobs/compare?ids=1,2,3` returns normalized metrics
  per job + per-metric "best" id. Frontend: select jobs, floating "Compare (n)"
  button, comparison table with winner highlighting.
- *Phase:* 2

**F8. Application Timeline / history**
- *Summary:* Ordered event history per application.
- *Value:* "What happened and when for this application?"
- *Acceptance:* `GET /api/jobs/{id}/timeline` returns ordered events derived
  from existing fields (created, materials, attempts, submission). Job detail
  shows a vertical timeline.
- *Phase:* 2

**F9. Follow-up email generator**
- *Summary:* Deterministic follow-up email for submitted applications.
- *Value:* "Remind the recruiter I'm still interested."
- *Acceptance:* `GET /api/jobs/{id}/followup` returns subject + body using the
  user's name, job title/company, and days since submission. Frontend: "Draft
  follow-up" button → modal + copy-to-clipboard.
- *Phase:* 2

**F10. Saved filter chips**
- *Summary:* Save and re-apply job-list filters.
- *Value:* "One click to get back to 'remote, approved, $100k+'."
- *Acceptance:* `saved_filters` persisted on Profile (JSON). `GET/PUT
  /api/profile/filters`. Frontend: "Save current filters" → name prompt →
  re-applicable chips. **Model change.**
- *Phase:* 2

### Phase 3 — Data depth (small model changes)

**F11. Fit trend over time**
- *Summary:* Average confidence/eligibility per scan over time.
- *Value:* "Is my fit improving as I refine my profile?"
- *Acceptance:* `avg_confidence` + `avg_eligibility` added to `ScrapeRun`,
  populated at end of each scan/rescore. `GET /api/analytics/trend` returns the
  time series. Analytics shows a line chart. **Model change.**
- *Phase:* 3

**F12. Resume variants**
- *Summary:* Multiple named resume versions, selectable per job.
- *Value:* "Use my 'data' resume for analytics roles, 'BA' resume for BA roles."
- *Acceptance:* `resume_variants` persisted (JSON list of `{name, text,
  skills}`) or a `ResumeVariant` table. `GET/PUT /api/profile/resume-variants`;
  generate/materials accept a variant. Frontend: variant manager + picker.
  **Model change.**
- *Phase:* 3

**F13. Cover-letter personalization + score**
- *Summary:* Deterministic job-specific phrasing + a personalization score.
- *Value:* "Does my letter actually reference *this* job?"
- *Acceptance:* `_cover_letter()` pulls 2–3 job-specific phrases from the
  description/skills (template slots, no LLM). Returns `personalization_score`
  (0–100). Job detail shows a score badge + regenerate.
- *Phase:* 3

**F14. Data export/import**
- *Summary:* Export jobs/applications/analytics; import jobs.
- *Value:* "Back up my data or move it to another machine."
- *Acceptance:* `GET /api/export/jobs?format=csv|json`, `/api/export/
  applications`, `/api/export/analytics`; `POST /api/import/jobs` validates,
  dedups by fingerprint, returns `{imported, skipped, errors}`. Frontend:
  export menu + import picker.
- *Phase:* 3

### Phase 4 — Source expansion (biggest long-term value)

**F15. New source adapters + registry**
- *Summary:* Add public job-board adapters behind the existing adapter
  architecture.
- *Value:* "More real jobs, same pipeline."
- *Acceptance:* Adapters for Lever, Ashby, Workable, SmartRecruiters, Workday,
  RemoteOK, WWR, The Muse, Adzuna. A company-slug registry (JSON or `Source`
  table). Each adapter returns the normalized job dict shape; collector applies
  gate → dedup → score → persist unchanged.
- *Phase:* 4

**F16. Bangladesh board scrapers**
- *Summary:* HTML-scrape local boards for BDT salary data.
- *Value:* "Local market context, not just remote."
- *Acceptance:* Adapters for bdjobs.com, career.com.bd, jobsinbd.com via
  Playwright. Politeness: robots.txt, 1 req/sec/domain, cache, store raw
  response hash.
- *Phase:* 4

**F17. Scheduler + enrichment**
- *Summary:* Automatic periodic scans + deterministic enrichment.
- *Value:* "It updates itself; company/skill data is richer."
- *Acceptance:* APScheduler for daily scans; enrichment via Wikidata (HQ,
  founded, employees, industry), O*NET (skill taxonomy normalization),
  trafilatura (main-content extraction), tenacity (retry/backoff).
- *Phase:* 4

---

## 5. Success Metrics
| Metric | Target |
|--------|--------|
| Test suite | 100% pass (existing 75 + new) |
| New endpoints | All return 200 with real data; 404/422 on bad input |
| Determinism | Same inputs → identical outputs (no timestamps in scores) |
| No fake data | Empty results return empty, never synthetic rows |
| UAT | Every feature verified in the browser |
| Performance | Analytics endpoints < 500 ms on a 1k-job DB |

---

## 6. Risks & Mitigations
| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| New source APIs change / rate-limit | Medium | Adapters isolate network; one bad source never kills a run; registry lets us disable any source |
| BD boards block scraping | High | Playwright + robots.txt + rate-limit; treat failures as `error` runs, not crashes |
| Salary data sparse/noisy | High | `_salary_value()` already normalizes; insights report `count` so the user sees sample size |
| Model migrations break existing DB | Medium | `Database.migrate()` is idempotent (ADD COLUMN); new columns nullable |
| Scope creep in Phase 4 | Medium | Phased delivery; Phase 4 items needing new deps get explicit confirmation first |

---

## 7. Out of Scope (explicit)
- Multi-user, teams, sharing.
- ATS auto-submission.
- LLM-based writing or scoring.
- Paid data providers.
- Native mobile apps.

---

## 8. Release Plan
1. **Phase 1** — F1–F5 (analytics + per-job explainability). No model changes.
2. **Phase 2** — F6–F10 (pipeline UX). One model change (saved filters).
3. **Phase 3** — F11–F14 (data depth). Two model changes (trend, variants).
4. **Phase 4** — F15–F17 (sources + scheduler). New dependencies; confirm scope
   before installing.

Each phase ships with: code, tests, and browser UAT. The full suite must pass
before moving to the next phase.

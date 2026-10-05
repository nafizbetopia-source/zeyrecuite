# ZEYRECUITE — Your Personal AI Job Agent (Advanced Edition)

> **Status:** PLANNING (no code yet)
> **Owner:** Personal use only (single user — you, a Business Analyst; currently in Bangladesh, location is a profile field)
> **Budget:** $0 target — local development and validation first; private free cloud is optional and only after current hosting limits and persistence are verified
> **AI constraint:** **Groq free tier** (rate-limited) → the entire intelligence layer is engineered to do **maximum AI work per token**
> **Core model:** Overnight the agent finds + scores + tailors everything; you review in the morning and hit **Approve**; the agent submits on your behalf.
> **Last updated:** 2026-10-01

---

## 0. v2.1 Feature Update (implemented)

This release upgrades the matching engine, the job detail experience, and adds submission tracking plus an analytics dashboard. All of it is **Tier 0 (deterministic, $0, reproducible)** — no LLM tokens are spent.

### 0.1 Smarter, explainable confidence (multi-factor)
Every job now gets a **0-100 confidence** that is a transparent weighted blend of **six factors**, each shown with a plain-language explanation in the job detail:

| Factor | Weight | What it measures |
|---|---|---|
| Role fit | 38% | Title relevance + skill overlap + must-have coverage |
| Your eligibility | 20% | Location policy + work-mode preference + salary floor |
| Skill coverage | 17% | How much of the job's required skill set your profile covers |
| Company quality | 13% | Curated company rating (neutral when unknown) |
| Freshness | 6% | How recent the posting is |
| Data completeness | 6% | How complete the job data is (description, skills, salary, apply link) |

The detail view also shows a **"Why this score"** reason list, a separate **eligibility %** (how eligible *you* are), and a **skills match** panel (matched / core must-have / not-in-your-profile).

### 0.2 Top 10 dashboard
The dashboard now leads with the **Top 10 matches** (highest confidence among eligible + review jobs). Each card shows confidence, eligibility %, company rating, and matched skills.

### 0.3 Submission tracking
**Approve** now runs a submission pipeline: it ensures a tailored resume PDF + cover letter exist, records a verifiable submission (status, method, apply URL, timestamp, attempt count), and returns a clear status. Jobs with a direct apply link are marked **submitted**; jobs without one are marked **ready** with the exact next step. The job detail shows an **application status panel**. This is honest and auditable — the MVP never auto-fills third-party ATS forms.

### 0.4 Analytics dashboard (infographics)
A new **Analytics** view with SVG infographics: application-pipeline donut (submitted/ready/draft + conversion %), submissions over the last 14 days, confidence distribution, jobs by source, jobs by work mode, and top companies.

### 0.5 Re-score
A **Re-score** button (and automatic re-score after saving the profile) recomputes the full assessment for every job using your current profile, so rankings always reflect your latest skills, location, and salary floor.

---

## 1. Vision

**ZEYRECUITE is your personal AI job agent** — a highly capable, intelligent machine that finds jobs passing your role and location rules, prepares application materials, and tracks your decisions. You are a **Business Analyst** (currently in Bangladesh — your location is a profile field you can change anytime). Worldwide remote roles are allowed, including roles open to applicants in South Asia, provided the employer and actual job location are not South Asian.

### What it does, every single day
1. **Finds** remote jobs worldwide, including jobs open to applicants in South Asia, while excluding South Asia-based employers and actual job locations.
2. **Understands** each job with a hybrid intelligence stack (local embeddings + rules + budgeted Groq LLM) — far beyond keyword matching.
3. **Tailors** your master resume for that specific job and renders it to a **PDF**.
4. **Writes** a tailored cover letter and **pre-fills** every application question.
5. **Stages** the top matches into your **morning review queue** — each with the job, tailored resume PDF, cover letter, answers, and a plain-English fit explanation.
6. **You review in the morning** and hit **Approve** (or edit / reject).
7. **On your approval, it submits** the application on your behalf (ATS API / browser / email), captures the confirmation, and tracks it.
8. **Learns** from your decisions and outcomes, getting better about *you* over time.

**The human-in-the-loop is the point:** the agent does 100% of the work; you make the 10-second decision. Nothing is submitted without your approval (full auto-apply is an optional later mode).

---

## 2. Constraints & The Core Design Principle

### Hard constraints
| Constraint | Decision |
|---|---|
| Cost | **$0 target.** No paid API or mandatory paid-hosting dependency. Build and validate locally first; consider private free cloud only after verifying current terms, quotas, persistence, and privacy controls. |
| AI provider | **Groq free tier** — fast inference but **rate-limited** (approx. 30 req/min, ~1,440 req/day, ~200M tokens/month — exact numbers live in `config.yaml` and are treated as a budget, not a guarantee). |
| Hosting | **Phase 1: local Windows development and validation. Phase 2: evaluate private free cloud hosting** against current quotas, storage persistence, privacy/access controls, and scheduler limits. Local operation remains supported. |
| Location | **Current: Bangladesh** (editable in the profile). Exclude employers and actual job locations in South Asia, including remote-labeled jobs. Worldwide remote is allowed, including applicant eligibility in South Asia, when the employer/job origin is outside South Asia. |
| Work mode | **Remote-first** (onsite/hybrid optional later via config). |
| Approval | **Human-in-the-loop:** nothing submits without your morning approval (default). |
| Scale | ~5–50 applications/day. |
| Reliability | Sites change → isolated adapters; one breakage never kills the system. |

### ⭐ The Core Design Principle: "Spend tokens like money"

Groq's free tier is the bottleneck, so the system is architected in **three intelligence tiers**. The rule: **never spend an LLM token on something a cheaper tier can do.**

```
TIER 0 — DETERMINISTIC (free, unlimited, instant)
   parsing, filtering, dedup, keyword scoring, eligibility heuristics,
   resume reordering/keyword alignment, PDF rendering, scheduling,
   retry logic, budget management, caching
        │  only what Tier 0 can't judge
        ▼
TIER 1 — LOCAL MODELS (free, unlimited, runs on your CPU)
   embeddings (semantic similarity), local classifiers
   (work-mode / eligibility / role-fit), semantic cache,
   skill-matching beyond keywords
        │  only the top-N jobs that pass both tiers
        ▼
TIER 2 — GROQ LLM (budgeted, precious)
   deep fit judgment + reasoning, cover letters, resume bullet
   polishing, application answers, edge-case eligibility,
   self-healing selectors, interview prep
```

**Result:** a night with 200 new jobs might cost **~150–300 Groq requests** (top-N deep scoring + letters for the ~10–15 that make your review queue) — comfortably inside the free budget, with headroom for retries and the learning loop.

### Speed & performance targets
| Metric | Target |
|---|---|
| Full overnight cycle (collect → staged queue) | **< 45 min** for ~200 new jobs (local) / **< 90 min** on HF Space (2 vCPU) |
| Dashboard load | **< 1 s** |
| Per-job Tier 0+1 processing | **< 2 s** (embeddings on CPU) |
| Groq request latency (p50) | **< 3 s** (Groq is fast; limits are the issue, not speed) |
| Tailored resume PDF render | **< 2 s** |
| System behavior when Groq budget is exhausted | **Graceful degradation** — Tier 0+1 pipeline keeps finding & scoring jobs; LLM-dependent items queue for the next budget window. The agent never stops. |

---

## 3. Your Profile (seeded from `Res.pdf` — editable anytime in the dashboard)

> ⚠️ This section drives the matching engine. Everything here is **editable at any time in the dashboard's Profile Manager** (§5.10) — this PRD section is just the seed data.

### Identity & contact (from Res.pdf)
- **Name:** MD Nafiz Mahfuz
- **Headline:** Business Analyst | Data Analyst
- **Residence (current location):** Dhaka, Bangladesh — **this field drives the search scope** (§5.2). Change it when you move; the agent immediately complies with the new country.
- **Phone:** +880 1877 014405
- **Email:** nafizmahfuz100@gmail.com
- **LinkedIn / GitHub / portfolio:** TO BE PROVIDED — no URL is embedded in `Res.pdf`. Will be imported from the **official LinkedIn profile export** (PDF or "Get a copy of your data" JSON) — see §5.10 LinkedIn import. No scraping (ToS + account-ban risk).

### Search preferences
- **Target roles:** ✅ **Business Analyst** (related: Data Analyst, Analytics Consultant, Insights Analyst, Product Analyst)
- **Target companies:** ✅ **Any** (no exclusions yet — can add favorites/exclusions later in the dashboard)
- **Location:** ✅ **Current: Bangladesh.** Worldwide remote jobs are allowed, including those accepting Bangladesh-based applicants, provided the employer and actual job location are outside South Asia. South Asia-based jobs remain excluded even when labeled remote. Local roles in South Asia remain excluded.
- **Work mode:** ✅ **Remote (default & primary).** Onsite/hybrid can be enabled later via config/dashboard.
- **Experience level:** ✅ **Junior–Mid** (BSc 2024, ~2 years experience)
- **Expected salary:** ✅ **Dynamic — no fixed minimum.** The agent calculates the fair market rate for *that specific job* (role + company + region + seniority, via the salary-estimation feature in §4.5) and flags jobs paying significantly below market. You see the listed/estimated salary + a "fair?" verdict on every card.
- **Deal-breakers:** _(e.g., no on-call, no travel, no agencies, no "US-only" remote)_ — TO BE FILLED
- **Standard answers:** ✅ **Notice period: immediate (can start any time).** ✅ **Timezone: flexible** — based in UTC+6 (Dhaka), willing to overlap EU and/or US working hours as the job requires.

### Skills (the skill pool — master resume + Skills Manager)
> **Rule:** the skill pool is **always derived from your master resume** (the agent re-scans it whenever you update it) **plus** anything you add manually in the **Skills Manager** (§5.10). The system **suggests** skills it detects in your resume/LinkedIn that you haven't listed yet — you approve or dismiss. You can add/remove skills anytime.
>
> **Tailoring rule (precision, no padding):** each tailored resume includes **only the skills that specific job needs** (JD skills ∩ your real skills) — never extra skills. A technical BA role → Python/SQL surface; a non-technical BA role → they're dropped. Applying to an airline → your domain skills (RASK/CASK, yield management, fare intelligence, overbooking) surface automatically. See §5.6.
- **Seed pool (from Res.pdf):** SQL, Excel (Advanced, VBA, Solver), Power BI, Python (Pandas, NumPy, Scikit-learn), requirements elicitation (BRD/FRD), process mapping, user stories, stakeholder management, Agile/Scrum, data analysis & reporting, dynamic pricing / yield management, RASK/CASK & P&L analysis, demand forecasting, PROS RMS, Amadeus/Sabre concepts, JIRA, Confluence, statistics
- **Categorization (drives smart tailoring):**
  - **Functional BA:** requirements elicitation (BRD/FRD), process mapping, user stories, stakeholder management, Agile/Scrum, documentation
  - **Technical:** SQL, Python (Pandas/NumPy/Scikit-learn), Excel (VBA, Solver), Power BI, JIRA, Confluence
  - **Domain (airline/aviation):** dynamic pricing, yield management, RASK/CASK, P&L & variance, demand forecasting, overbooking, PROS RMS, Amadeus/Sabre, fare class bucketing
  - **General:** data analysis, reporting, statistics

### Resume content (from Res.pdf — becomes the master resume seed)
- **Experience:** Business Analyst @ Betopia Limited (Feb 2026–present); Data Analyst Intern, MD's Office @ Walton Hi-Tech Industries (Jul–Sep 2025); Junior Consultant Intern @ Principio Holdings, remote (Jan–Jun 2025)
- **Projects:** Overbooking/No-Show prediction (Random Forest, 82% accuracy, 4% revenue uplift); Airline Network Profitability RASK/CASK analysis; Competitor Fare Intelligence System (DAC–DXB fare monitoring)
- **Education:** BSc CSE, BRAC University, Dhaka (2020–2024)
- **Certifications:** FAA Scalable SMS; Six Sigma White Belt (CSSC); Microsoft/LinkedIn Data Analysis & PM; Forage simulations (British Airways, Accenture, PwC)
- **Languages:** Bangla (native), English (fluent, IELTS 7.0), Chinese (basic)

> **Note:** `Res.pdf` is the **format sample** of your master resume. The actual master resume will be provided later — it gets imported into the structured profile (§5.10) and becomes the single source of truth.

---

## 4. The Intelligence Architecture (the heart of "100x more advanced")

This is where the system becomes a real agent instead of a scraper. Every subsystem below is designed to **maximize intelligence per token**.

### 4.1 Tier 0 — Deterministic Engine (unlimited, instant)
- **Parsing & normalization:** extract title, company, location, work mode, salary, skills, application URL/method from any source.
- **Hard filters:** remote + current-location eligibility + role + salary + deal-breakers + **South-Asia job-origin exclusion**. Reject employers or actual job locations in South Asia, even if labeled remote. Applicant eligibility in South Asia does not itself disqualify a remote job. Apply the origin filter before persistence, ranking, generation, or display.
- **Keyword scoring (0–100):** weighted skill overlap (must-have > nice-to-have), title match, salary fit, company preference.
- **Dedup:** fingerprint = hash(company + normalized title + location); cross-source merge keeps the best application URL.
- **Resume tailoring (deterministic core):** reorder skills/experience to mirror the JD's priority order; align bullet keywords with JD vocabulary; enforce 1–2 pages. **No LLM needed for 80% of the tailoring.**
- **PDF rendering:** structured JSON → clean ATS-friendly PDF (WeasyPrint).
- **Budget manager, cache manager, retry/backoff, scheduling, audit log.**

### 4.2 Tier 1 — Local Models (free, unlimited, CPU)
- **Embeddings** (e.g., `all-MiniLM-L6-v2` via sentence-transformers, runs on CPU in ms):
  - **Semantic skill matching** — "data viz" ≈ "Power BI/Tableau", "client-facing" ≈ "stakeholder management". Catches what keywords miss.
  - **Semantic dedup** — same job reworded across 3 boards = 1 record (cosine similarity > 0.92).
  - **Semantic cache** — if a new job's embedding is > 0.95 similar to a previously LLM-scored job, **reuse the cached LLM output** (score, reasoning, letter skeleton). This alone can cut Groq usage 30–60% on busy days.
  - **Learning loop** — embed your approved vs rejected jobs; drift the scoring weights toward what you actually like.
- **Local classifiers** (small fine-tuned or thresholded models on embeddings):
  - Work-mode classifier (remote/hybrid/onsite) — higher precision than regex.
  - Location-eligibility classifier — flags "remote — US only", "must be in EU timezone", "based in [South Asian country]", etc., relative to your current location.
  - Role-fit classifier — is this actually a BA job or a "BA in name only" (e.g., a sales role with BA in the title)?

### 4.3 Tier 2 — Groq LLM (budgeted, the "brain")
Spent **only** on the top-N jobs (default N = 15) that pass Tier 0+1, and only for tasks that genuinely need language understanding:
1. **Deep fit judgment** — full JD + master resume → fit score (0–100) + plain-English reasoning + matched/missing skills + risk notes ("asks 5+ yrs, you have 3").
2. **Cover letter** — 150–250 words, tailored, in your voice.
3. **Resume bullet polishing** — rewrites 3–6 key bullets to mirror the JD (strict truthfulness guardrail: rephrase only, never invent).
4. **Application answers** — answers the job's questionnaire questions from your standard answers + resume.
5. **Edge-case eligibility** — only when the local classifier is uncertain (confidence < 0.8).
6. **Self-healing adapters** — when a Playwright selector breaks, the LLM reads a page snapshot and proposes the new selector (see §5.5).
7. **Interview prep** (post-apply) — predicts likely interview questions from the JD for your review.

### 4.4 Token Budget Manager (the "100x" engineering)
- **Daily budget** in `config.yaml` (e.g., 1,200 requests / 15M tokens — safely under Groq free limits). Every LLM call is metered.
- **Priority queue:** deep-scoring top jobs > cover letters > bullet polishing > interview prep > learning. Low-priority work waits for the next window if the budget runs low.
- **Model tiering:** small/fast Groq model (e.g., Llama 3.1 8B) for classification & short tasks; large model (e.g., Llama 3.3 70B) only for cover letters & deep judgment.
- **Prompt prefix caching:** the shared system prompt + your master resume is a stable prefix — Groq caches repeated prefixes, cutting input tokens dramatically.
- **Batching:** one prompt can deep-score 3–5 similar jobs at once (structured JSON output), cutting request count ~3x.
- **Semantic cache** (Tier 1) skips LLM calls for near-duplicate jobs.
- **Incremental generation:** letters are generated once per job; if you edit a job's details, only the delta is regenerated.
- **Graceful degradation:** budget exhausted → Tier 0+1 keeps running; LLM tasks queue automatically for the next window. You're never blocked.
- **Budget dashboard:** live view of today's usage, estimated cost-per-application, and forecast ("at this job volume, budget lasts until 04:30").

### 4.5 Advanced Agent Capabilities (what makes it "highly capable")
- **Job quality & red-flag detection:** LLM (batched, low priority) flags risky postings — "corporate university" language, no salary + vague scope, high-churn signals, agency spam. Shown as a ⚠️ badge in review.
- **Urgency scoring:** posting age + similar-job volume → "apply soon" vs "can wait". Fresh high-fit jobs jump the queue.
- **Salary estimation (also the min-salary filter):** for jobs without listed salary, estimate range from company/role/region signals (local model + cached LLM priors). Since the user has **no fixed minimum salary**, this estimate doubles as the filter: each job gets a "fair?" verdict (listed/estimated vs market rate for that exact role+region+seniority); significantly below-market jobs get a ⚠️ and rank lower.
- **Application success prediction:** per-job probability of getting a response, learned from your outcomes over time.
- **JD change detection:** if a "new" job is a repost of an old one (semantic match), it's marked `REPOST` and not re-applied.
- **Self-healing automation:** broken Playwright selectors → LLM proposes fix from page snapshot → you get a one-tap "apply the fix" in the dashboard. Adapters heal themselves.
- **Agent memory:** every decision, outcome, and your edits are stored (SQLite) and fed back into scoring — the agent remembers that you rejected all agency jobs, all "US-only" roles, and that Power BI-heavy jobs got you interviews.
- **A/B cover letters:** two letter styles generated for top jobs; your approvals/interviews teach which style works.
- **Confidence everywhere:** every LLM output carries a confidence score; low-confidence items are auto-flagged for your review instead of silently trusted.

---

## 5. Core Features

### 5.0 The Daily Loop (the heart of your agent)

```
┌────────────────────────── OVERNIGHT (agent works alone) ──────────────────────────┐
│  1. COLLECT    fetch configured public feeds and curated ATS boards               │
│  2. FILTER     discard South Asia employer/job origins before persistence         │
│  3. DEDUP      fingerprint + semantic dedup among eligible jobs only              │
│  4. SCORE      Tier 0 keyword + Tier 1 semantic → top-N selected                  │
│  5. DEEP-SCORE Groq LLM (budgeted): fit + reasoning + eligibility edge cases      │
│  6. TAILOR     deterministic resume tailoring + LLM bullet polish → PDF           │
│  7. WRITE      cover letter + pre-filled answers (Groq, budgeted)                 │
│  8. STAGE      top matches → Morning Review Queue (with urgency + red flags)      │
└───────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────── MORNING (you, ~5 minutes) ──────────────────────────────┐
│  9. REVIEW     dashboard: job + fit score/reasoning + tailored resume PDF +       │
│                letter + answers + red flags + salary estimate                     │
│ 10. DECIDE     Approve / Edit / Reject  (one click each)                          │
└───────────────────────────────────────────────────────────────────────────────────┘
                                   │  (on Approve)
                                   ▼
┌────────────────────────── ON APPROVAL (agent submits for you) ────────────────────┐
│ 11. SUBMIT     agent applies on your behalf (ATS API / browser / email)           │
│ 12. CONFIRM    capture confirmation (screenshot + URL), update pipeline           │
│ 13. PREP       (optional) predicted interview questions for your review           │
│ 14. LOG        results + "needs you" items shown in the dashboard                 │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### 5.0a The 100% Confidence Gate (quality over quantity)

> Your rule: *"every morning I get the best 10 jobs that we are 100% confident about."*

A job is staged in the Morning Review Queue **only if ALL of these pass**:
- **Fit score ≥ 85** (Tier 0+1+2 blend)
- **Location eligibility = confirmed** (not "maybe")
- **Company legitimacy = ✅** (not ⚠️/❌ — §5.11)
- **No red flags**
- **Skill coverage ≥ 80%** of the JD's required skills

**Fewer than 10 is OK — 5 confident beats 10 "maybe."** Some mornings you get 10, some 4, some 1. The queue is never padded.
- **Second-look queue:** jobs that narrowly missed (80–85) appear in a secondary list — one-click promote if you want them.
- **Calibration:** predicted fit vs actual outcomes is tracked; thresholds auto-tune over time so "100% confident" stays true.

### 5.1 Job Discovery (Collector)
- Runs on a schedule (every 30–60 min overnight) + on-demand "scan now".
- Pluggable **source adapters** (one class per source) → normalized `Job` objects.
- **Scope:** allow remote jobs worldwide, including postings open to South Asian applicants, when employer base and actual job location are outside South Asia. Exclude local roles whose job location is in South Asia. Store employer/job origin separately from `candidate_required_location`; apply the hard origin filter before persistence, deduplication, scoring, resume generation, or display. A remote role restricted to locations that do not include the user's current location is still rejected as ineligible.
- **Async parallel collection** — all adapters run concurrently; slow sources never block the cycle.
- Fields: `title, company, location, work_mode, location_eligible, salary, description, skills, url, source, posted_date, application_url, application_method`.

### 5.2 Work-Mode + Location-Eligibility Filter (the location engine)
- **Current location** lives in the profile (§5.10) — e.g., now `Dhaka, Bangladesh`. Change it when you move; the whole search scope re-complies instantly.
- **Scope rules:**
  - **Remote jobs:** eligible worldwide, including postings accepting South Asian applicants, when employer/job origin is outside South Asia and the posting permits the user's current location.
  - **Local (onsite/hybrid) jobs:** eligible only when both the user's current country and job location are outside South Asia.
  - **Strict exclusion:** employers and actual job locations in Bangladesh, India, Pakistan, Sri Lanka, Nepal, Bhutan, Maldives, or Afghanistan are discarded, even when a role is labeled remote. A non-South-Asian employer's worldwide remote role may accept applicants in those countries.
  - **Eligibility handling:** use `candidate_required_location` to determine whether the current user can apply; “Worldwide” includes the user's current location unless another restriction says otherwise. If eligibility is unclear, hold for review rather than inferring an exclusion from South Asian applicant acceptance.
  - **Empty queue behavior:** when no listing meets all origin, candidate-eligibility, and role constraints, show a clear empty state; never relax the origin exclusion to create matches.

**Authoritative interpretation:** South Asian employer base or actual job location is the hard exclusion. Applicant geography is not a blanket exclusion: worldwide remote roles can include South Asian applicants, including the user in Bangladesh, if the employer/job itself is outside South Asia and the role is otherwise eligible. Unknown employer/job origin is held out until verified. This supersedes the temporary stricter applicant-location exclusion.
- Config:
  ```yaml
  work_mode:
    remote: true      # ← primary, on by default
    onsite: false     # local jobs in current country (when abroad)
    hybrid: false
  location:
    current: "Bangladesh"   # ← from profile; drives everything
    excluded_countries: [Bangladesh, India, Pakistan, Sri Lanka, Nepal, Bhutan, Maldives, Afghanistan]  # strict, South Asia
  ```
- Classification pipeline: **Tier 0 regex heuristics → Tier 1 local classifier → Tier 2 LLM only when confidence < 0.8.**
- "Remote — US only" (when you're not in the US), "EU timezone required" (when you can't overlap), "based in India", "must relocate" → filtered out.
- Changes take effect next scan cycle; no restart.

### 5.3 Deduplication
- Fingerprint = hash(company + normalized title + location) → exact dupes.
- **Semantic dedup** (Tier 1 embeddings, cosine > 0.92) → reworded dupes across boards.
- `REPOST` detection: semantic match against previously applied jobs → never re-apply.
- Cross-source merge keeps the best application URL + richest description.

### 5.4 Intelligent Matching & Scoring (three-stage)
- **Stage 1 — Tier 0 rules (every job, instant):** hard filters + keyword score (0–100).
- **Stage 2 — Tier 1 semantic (every surviving job, ms):** embedding-based skill match, role-fit classifier, eligibility classifier. Composite score.
- **Stage 3 — Tier 2 Groq deep judgment (top-N only):** fit score + reasoning + matched/missing skills + risk notes + eligibility verdict.
- **Final score = weighted blend** (configurable weights, auto-tuned by the learning loop).
- Top matches → **Morning Review Queue**, ordered by final score × urgency.

### 5.5 Application Engine (submits on YOUR approval)
- **Trigger:** your **Approve** click (or optional auto-approve threshold, later).
- **Methods, in order of reliability:**
  1. **Direct ATS APIs** (Greenhouse, Lever, Ashby, Workable, SmartRecruiters) — public JSON + simple forms. Most reliable.
  2. **Playwright browser automation** — fill, attach tailored resume PDF, answer questions, submit.
  3. **Email applications** — "apply via email" parsed from JD → auto-compose with tailored resume attached.
  4. **Manual queue** — LinkedIn Easy Apply / Indeed / CAPTCHA walls → agent prepares everything and opens the page; you click submit.
- **Self-healing:** if a selector breaks, the agent captures a page snapshot, asks Groq (budgeted) for the likely new selector, and offers a one-tap fix in the dashboard.
- **Per-application pipeline (after approval):** use the tailored PDF + letter + pre-filled answers → submit via best method → capture confirmation (screenshot + URL) → on failure/CAPTCHA → `NEEDS_HUMAN` (shown in the dashboard Needs-You panel) with one-click retry.
- **Safety rails:** max applications/day = **10** (confirmed — the agent scans *all* sources and stages the **top 10 best matches** each day; you approve from those), random human-like delays, never submit twice to the same job, full audit log of every field submitted, dry-run mode.

### 5.6 Resume Tailoring Engine (master resume → per-job PDF)
- **Master resume = single source of truth** (structured JSON: contact, summary, skills, experience bullets, projects, education, certifications). Editable in the dashboard; the agent re-scans it whenever you update it.
- **Precision skill selection (the "no extra skills" rule):** the tailored skill section = **JD-required skills ∩ your real skill pool** — nothing else. Skills the job doesn't ask for are **dropped**, not padded. Domain relevance is automatic: an airline company → your aviation skills (RASK/CASK, yield management, fare intelligence, overbooking) surface; a fintech company → they're dropped and your SQL/Python/BI skills lead.
- **Deterministic tailoring (Tier 0, always runs):** select the job-relevant skills (above); reorder skills/experience to mirror JD priority; align bullet keywords with JD vocabulary; adjust summary to the role; enforce 1–2 pages, ATS-safe layout.
- **LLM bullet polish (Tier 2, top-N only):** rewrites 3–6 key bullets to mirror the JD's language — **strict truthfulness guardrail: rephrase only, never invent skills/years/employers.**
- **PDF rendering:** JSON → clean ATS-friendly PDF (WeasyPrint). One PDF per application, stored, versioned, viewable in the dashboard.
- **You see the exact PDF before approving** — what you approve is what gets submitted.

### 5.7 Cover Letter + Answers Generator
- Groq (budgeted, large model): your master resume + JD → 150–250 word letter in your voice + answers to the job's questionnaire.
- **A/B styles** for top jobs; learning loop picks the winner over time.
- Editable in the dashboard before you approve.

### 5.8 Morning Review Dashboard (Local Web UI)

> **Confirmed direction:** a **full-featured dashboard** — not a minimal page. Rich analytics, charts, and every control in one place. Built as plain HTML + JS (no build step, $0, instant load) with Chart.js for analytics — same feature richness, zero framework overhead.

- **Tabs:** 📥 **Review Queue** (home) · 📊 **Pipeline** · 📈 **Analytics** · 👤 **Profile Manager** (§5.10) · 🧠 **Budget** · ⚙️ **Controls**
- **Analytics tab:** applications/day trend, response rate over time, source effectiveness (which boards produce interviews), skill→interview correlation, salary distribution of applied jobs, pipeline funnel (New → Applied → Interview → Offer), Groq spend trend.
- **Morning Review Queue (home screen):** each card shows:
  - Job title, company, location, salary (listed or **estimated**), work mode, source link, posting age.
  - **Company check** (§5.11): legitimacy badge + review summary (salary fairness, environment, culture).
  - **Fit score + LLM reasoning** + matched/missing skills + confidence.
  - **Tailored resume PDF** (inline preview + download).
  - Cover letter + pre-filled answers (all editable).
  - ⚠️ **Red flags** (if any) + **urgency badge** + **success prediction**.
  - One-click **Approve / Edit / Reject**.
- **Needs-You panel:** everything that needs your attention in one place — CAPTCHA / login walls, failed submits, broken adapters (with self-heal suggestions). No push notifications; you check this in the morning.
- **Pipeline view:** New → Scored → Staged → Approved → Applying → Applied → Interview → Offer / Rejected.
- **Budget panel:** today's Groq usage, forecast, cost-per-application.
- **Stats & learning:** applications/day, response rate, source effectiveness, which skills correlate with interviews.
- **Controls:** start/stop scheduler, scan now, dry-run toggle, daily cap, work-mode toggles, **current location + excluded countries**, auto-approve threshold (optional).

### 5.9 Application Tracking & Learning Loop (near-perfect results over time)
- **Every application is tracked end-to-end:** job, tailored resume version, letter style, answers, submit method, confirmation, and **outcome** (you mark: no response / interview / offer / rejected — with date). Nothing is lost; the full history is in the Pipeline + Analytics tabs.
- **Auto-draft follow-up** at day 7 if no response (manual send or auto via email method).
- **Learning loop (the agent gets smarter about YOU):**
  - Embeddings of approved vs rejected jobs → drift scoring weights toward your real preferences.
  - **Per-skill outcome tracking:** which skills on your tailored resume correlate with interviews/offers → reweight skill importance (e.g., if RASK/CASK-heavy resumes get interviews at airline roles, that domain skill's weight rises).
  - **Per-source & per-company success rates** → reweight source priority.
  - **Letter style A/B** → the style that wins interviews gets favored.
  - Your edits to letters/resumes → style memory (what you change is what it stops generating).
  - All stored in SQLite `learning` + `events` + `applications` tables; fully inspectable in the dashboard.

### 5.10 Profile Manager (your full profile — editable in the dashboard)

A dedicated **Profile** page in the dashboard where you can view and edit **everything** about yourself. Every change takes effect immediately (next scan / next tailoring) — no config files, no restarts.

| Section | What you can edit |
|---|---|
| **Identity & contact** | Name, headline/title, residence/location, phone, email, LinkedIn, GitHub/portfolio, photo (optional) |
| **Professional summary** | Your summary paragraph (drives the resume summary + cover-letter voice) |
| **Skills Manager** | The full skill pool: add/remove/reorder skills anytime; **skill suggestions** (the agent detects skills in your resume/LinkedIn you haven't listed — approve or dismiss); categorize (functional / technical / domain / general); mark **must-have** vs **nice-to-have** (drives scoring weights); the pool auto-syncs from your master resume |
| **Work experience** | Add/edit/delete jobs — company, role, dates, location, bullets. **This is how you log new jobs** as you get them. |
| **Projects** | Add/edit/delete projects — name, description, tech, **links** (GitHub / live / demo) |
| **Education** | Degrees, institutions, dates, honors |
| **Certifications** | Name, issuer, date, **links** (verification URLs) |
| **Achievements** | Awards, milestones, highlights (free text + optional links) |
| **Languages** | Language + proficiency |
| **Standard answers** | Notice period, work authorization, visa status, timezone availability, salary expectation — auto-fills application questionnaires |
| **Search preferences** | Target roles, target companies, work mode, min salary, deal-breakers, applications/day cap, **current location** (drives search scope), **excluded countries** (South Asia strict) |

- **Single source of truth:** this profile **is** the master resume (§5.6). The tailoring engine reads from it; every PDF is rendered from it.
- **Version history:** every save is versioned — see what changed and when, roll back anytime.
- **Validation:** required fields checked (email, ≥1 experience entry); a **profile completeness** score shows what's missing.
- **Import:** on first run, `Res.pdf` (or your master resume) is parsed into this profile; you review & fix it in the UI.
- **LinkedIn import (official, no scraping):** LinkedIn blocks scraping (ToS + login wall + account-ban risk — and the user needs that account healthy for job hunting). Instead: download the profile via LinkedIn's official **"Save to PDF"** or **Settings → Data privacy → "Get a copy of your data"** (JSON), drop the file in the workspace, and the agent parses it into the profile (experience, education, skills, certifications, recommendations). Re-run anytime to re-sync; the dashboard shows a diff of what changed before applying.

### 5.11 Company Checker (is this company legit? what's it like to work there?)

Every job card carries a **company check** — legitimacy + real-employee reviews. Companies repeat across jobs, so each is checked **once and cached** (big token savings).
- **Legitimacy signals (Tier 0/1, free):** company website exists + domain age (WHOIS), LinkedIn company page + employee count, Crunchbase/public presence, news mentions, scam patterns (asks for money, no website, brand-new domain, generic email, too-good-to-be-true salary, copy-paste JD).
- **Review summary (Tier 2, budgeted, cached per company):** LLM reads public review snippets (Glassdoor/Indeed/Reddit/Trustpilot via public endpoints) → plain-English verdict on **salary fairness, work environment, management, work-life balance, remote culture**.
- **Output on the review card:** ✅/⚠️/❌ legitimacy badge + one-line review summary (e.g., "Glassdoor 3.8★ — good pay, high pressure, async-friendly remote culture") + expandable details.
- **Legit ❌ or scam-pattern jobs** are auto-demoted or flagged for your review — you decide.
- **Data:** `companies` table (name, domain, domain_age, linkedin_size, legitimacy_score, red_flags, review_summary, rating, sources, checked_at).

### 5.12 Advanced Feature Suite (the "100x" layer)

> Post-MVP features, phased **P9–P11**. Each is small, isolated, and adds compounding value.

#### A. Smarter Matching
| Feature | What it does | Phase |
|---|---|---|
| **Ghost Job Detector** | Flags stale/ghost postings (60+ days old, 3+ reposts, 0 other active roles, dead apply link) → auto-demote | P9 |
| **Resume ATS Simulator** | Simulates what Workday/Greenhouse/Lever parse from your PDF; "ATS compatibility 92/100" + fixes; keyword density check vs JD | P10 |
| **Application Timing Optimizer** | Learns when responses are fastest (day/hour per company timezone); staggers approved submissions at optimal times | P10 |
| **Company Hiring Velocity** | Tracks companies hiring aggressively (5+ roles open = hot) vs stale (90 days = low urgency) → feeds urgency score | P10 |
| **Application Diversity Guard** | Flags over-concentration ("6 of 10 are airline BAs") → suggests diversifying | P10 |
| **Skill Gap Radar** | "You're missing Power BI for 40% of high-fit jobs" + free learning links; tracks match-pool growth over time | P10 |
| **Rejection Pattern Analyzer** | After 20+ outcomes: "agencies reject you 3x more", "5+ year roles reject 80%" → auto-reweights | P10 |
| **Salary Negotiation Playbook** | Per-company/role benchmarks from your own data; counter-offer scripts; tracks your average negotiation gain | P10 |
| **Career Path Advisor** | "Transitioning to Data Analyst would +30% your match pool"; quarterly market-value report | P11 |

#### B. Beyond Applications (outreach + interviews)
| Feature | What it does | Phase |
|---|---|---|
| **Referral Finder + Outreach** | Detects referral-friendly companies; drafts personalized referral requests; tracks referral status | P10 |
| **Hiring Manager Detection** | Infers likely hiring manager from JD clues; drafts personalized outreach; tracks outreach→interview conversion | P10 |
| **Interview Coach** | 8–12 likely questions per job; **mock interview** (Groq plays interviewer, you answer, it coaches); STAR answer builder; salary negotiation simulator; post-interview debrief | P9 |
| **Email Inbox Monitor (IMAP)** | Connects to your Gmail locally; auto-detects interview invites / rejections / confirmations; auto-updates pipeline; drafts replies | P9 |
| **Cover Letter Intelligence** | References company news + hiring manager background; varies tone per company culture; tracks which elements win | P10 |
| **Weekly/Monthly Intelligence Report** | Auto-generated: applications, interviews, best source, top skill gap, salary trend; PDF export | P10 |

#### C. Dashboard & UX
| Feature | What it does | Phase |
|---|---|---|
| **Keyboard-First** | A/R/E approve/reject/edit, J/K navigate, Shift+A approve-all, Ctrl+F search — review 10 jobs in <2 min | P9 |
| **Batch Operations** | "Approve all top 5", "Reject all below 60", bulk edit answers | P10 |
| **Application Receipts** | PDF receipt per submission (what was sent, when, confirmation URL, screenshot); CSV export; full audit trail | P10 |
| **Calendar Integration** | Interview reminders (ICS / Google Calendar); follow-up reminders | P10 |
| **Mobile-Friendly** | Responsive — review + quick-approve from your phone | P9 |
| **Dark Mode + Themes** | Data-dense, color-coded (green/yellow/red fit) | P9 |
| **Streaks & Milestones** | "🔥 7-day streak", "🎉 100 applications" — consistency dopamine | P10 |
| **Backup & Portability** | One-click ZIP backup (DB + profile + resumes); restore on any machine; JSON profile export | P9 |
| **Chat with Your Agent** | "What's the best job today?" / "Why did you reject that?" — RAG over your full application history | P9 |
| **Voice Commands** | Local Whisper: "What's the top job?" / "Approve the airline one" | P11 |

#### D. Moonshots (Phase 11+)
| Feature | What it does | Phase |
|---|---|---|
| **Multi-Profile Mode** | 2–3 resume personas (BA / Data Analyst / Aviation); auto-select per job; track which wins | P11 |
| **Job Market Heatmap** | Which regions have the most BA remote jobs right now; timezone overlap visualization | P11 |
| **Edge-Case Outreach** | For 80%-right jobs: drafts a polite "I have Y, you asked for X — open to a conversation?" email | P11 |
| **Ideal-Candidate Inference** | Infers the "ideal candidate" per job; shows your match % + how to offset gaps | P11 |
| **Auto Portfolio Page** | Generates a personal site from your profile (GitHub Pages, free); auto-updates | P11 |

---

## 6. Job Sources Strategy (all free)

| # | Source | Method | Free? | Reliability | Notes |
|---|--------|--------|-------|-------------|-------|
| 1 | **Greenhouse-hosted career pages** | Public JSON API (`boards-api.greenhouse.io`) | ✅ | ⭐⭐⭐⭐⭐ | Huge startup share; strong remote culture. No auth. |
| 2 | **Remotive (MVP)** | Public JSON API (`remotive.com/api/remote-jobs`) | ✅ | Source-dependent | 24-hour delay; poll max 4/day, never >2/min; show attribution and Remotive link; no signup collection or third-party republication. |
| 3 | **Ashby / Workable / SmartRecruiters** | Public JSON endpoints | ✅ | ⭐⭐⭐⭐ | Growing ATS market share. |
| 4 | **Remote-specific boards** (We Work Remotely, Remote OK, Remote Leaf) | Official API/feed only, if permitted | ✅ | ⭐⭐⭐⭐ | Future source candidates; verify terms and apply the same employer/job-origin and applicant-location exclusions. No unauthorized scraping. |
| 5 | **RSS feeds** (boards & company blogs) | RSS | ✅ | ⭐⭐⭐ | Stable, low volume. |
| 6 | **Adzuna API** | Official API, free tier (~100 req/day) | ✅ | ⭐⭐⭐⭐ | Free API key; remote + country filters. |
| 7 | **The Muse API** | Official, free | ✅ | ⭐⭐⭐ | Curated roles. |
| 8 | **Company career pages (direct)** | Playwright | ✅ | ⭐⭐⭐ | For specific target companies. |
| 9 | **LinkedIn / Indeed** | ⚠️ Manual queue only | — | ⭐⭐ | Login walls + anti-bot → agent prepares, you click. |

**MVP source decision:** begin with #1 Greenhouse public Job Board GET API and Remotive's public JSON API. Greenhouse GET listings are public and require no authentication; configure a curated allowlist of board tokens. Remotive's API is unauthenticated; honor its 24-hour delay, poll no more than four times per day and never more than twice per minute, show Remotive attribution, and link each listing to Remotive. Do not use its listings to collect signups or republish them to third-party job boards. Confirm current source terms at implementation time. Other sources are later roadmap candidates.

References: [Greenhouse Job Board API documentation](https://docs.greenhouse.io/job-board.html); [Remotive API documentation and terms](https://github.com/remotive-com/remote-jobs-api).

> **Location note:** many "remote" jobs are "remote — US/EU only". The location filter (§5.2) evaluates applicant eligibility relative to your **current location** and separately excludes jobs whose employer base or actual job location is South Asian, even if the listing says remote.

---

## 7. Data Model (SQLite)

```
profiles        → identity & contact (name, headline, residence, phone,
                  email, linkedin, github, photo), professional summary,
                  standard answers (notice period, work auth, timezone,
                  salary), search preferences (roles, companies, work_mode,
                  min_salary, deal-breakers, daily cap,
                  current_location, excluded_countries,
                  auto_approve_threshold)
skills          → id, name, category (functional/technical/domain/general),
                  source (master_resume/linked_in/manual), must_have,
                  nice_to_have, status (active/suggested/dismissed),
                  weight (learned), added_at
master_resume   → single source-of-truth resume (structured JSON, versioned):
                  experience[] (company, role, dates, location, bullets),
                  projects[] (name, description, tech, links),
                  education[], certifications[] (with links),
                  achievements[], languages[]
sources         → source config (type, params, enabled, schedule, health)
jobs            → id, fingerprint, title, company, location, work_mode,
                  location_eligible, eligibility_confidence, salary,
                  salary_estimated, description, skills(json), url,
                  application_url, source, posted_date, first_seen,
                  embedding(blob), keyword_score, semantic_score,
                  llm_fit_score, llm_reasoning, red_flags(json),
                  urgency, success_prediction, status
tailored_resumes→ id, job_id, master_resume_id, tailored_json, pdf_path,
                  created_at
applications    → id, job_id, tailored_resume_id, cover_letter,
                  letter_style, answers(json), status (STAGED/APPROVED/
                  APPLYING/APPLIED/NEEDS_HUMAN/FAILED/REJECTED_BY_USER),
                  confirmation_url, screenshot_path, approved_at,
                  submitted_at, error, outcome
followups       → application_id, due_date, sent_at, outcome
llm_cache       → semantic_key, job_embedding_ref, task_type, model,
                  input_hash, output(json), tokens_used, created_at
llm_budget      → date, requests_used, tokens_used, by_task(json)
events          → audit log (every action the bot takes, with timestamp)
learning        → approved/rejected/interviewed signals, tuned weights,
                  style preferences
companies       → id, name, domain, domain_age, linkedin_size,
                  legitimacy_score, red_flags(json), review_summary
                  (salary, environment, management, culture), rating,
                  sources(json), checked_at
outreach        → id, job_id, type (referral/hiring_manager/edge_case),
                  target_name, message, status (draft/sent/replied/
                  accepted/declined), sent_at, replied_at
interviews      → id, application_id, questions(json), mock_sessions(json),
                  star_answers(json), debrief, outcome
documents       → id, name, type (writing_sample/case_study/portfolio/
                  certificate), tags(json), file_path, added_at
watchlist       → id, company, role_keywords, last_checked, new_jobs_count
salary_benchmarks → role, region, company_size, n, median, p25, p75,
                  updated_at
```

---

## 8. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      SCHEDULER (APScheduler)                     │
└──────┬───────────────────────┬───────────────────────┬───────────┘
       │                       │                       │
┌──────▼──────────┐   ┌────────▼─────────┐   ┌─────────▼──────────┐
│ COLLECTORS      │   │  TIER 0          │   │  TIER 1 (local)    │
│ async adapters  │──►│  parse, filter,  │──►│  embeddings,       │
│ (remote/BD)     │   │  dedup, keyword  │   │  classifiers,      │
└─────────────────┘   │  score, tailoring│   │  semantic cache    │
                      └────────┬─────────┘   └─────────┬──────────┘
                               │        top-N          │
                               │                       │
                      ┌────────▼───────────────────────▼──────────┐
                      │  BUDGET MANAGER (meter, priority queue,   │
                      │  batching, prefix cache, degradation)     │
                      └────────────────────┬──────────────────────┘
                                           │
                      ┌────────────────────▼──────────────────────┐
                      │  TIER 2 — GROQ LLM (deep score, letters,  │
                      │  bullet polish, answers, self-heal, prep) │
                      └────────────────────┬──────────────────────┘
                                           │
                      ┌────────────────────▼──────────────────────┐
                      │  PIPELINE: score → rank → stage queue     │
                      └────────────────────┬──────────────────────┘
                                           │
                          ┌────────────────┴────────────────┐
                          │                                 │
                   ┌──────▼──────┐                ┌────────▼─────────┐
                   │  DASHBOARD  │                │  APPLICATION     │
                   │ Morning     │                │  ENGINE (on      │
                   │ Review +    │                │  APPROVAL:       │
                   │ Approve     │                │  ATS/Playwright/ │
                   └──────┬──────┘                │  Email)          │
                          │                       └────────┬─────────┘
                          └────────────────┬───────────────┘
                                           │
                          ┌──────────────▼───────────────────┐
                          │  SQLite (jobs, apps, cache,      │
                          │  budget, events, learning)  +    │
                          │  PDF RENDERER (WeasyPrint)       │
                          └──────────────────────────────────┘
```

**Components:**
1. **Collector service** — async adapters; discard South Asia-origin employers/jobs before persistence; keep worldwide remote listings eligible when the current user can apply; retain local roles only outside excluded countries.
2. **Tier 0 engine** — deterministic parse/filter/score/tailor/render.
3. **Tier 1 local models** — embeddings + classifiers + semantic cache.
4. **Budget manager** — meters every Groq call; priority queue; batching; graceful degradation.
5. **Tier 2 Groq client** — the "brain"; only spends where it matters.
6. **Pipeline** — score → rank → stage.
7. **Application service** — submits **only after your approval**; self-healing selectors.
8. **API + Dashboard** — FastAPI + Morning Review UI (includes the Needs-You panel).
9. **Learning loop** — decisions + outcomes → tuned weights + style memory.

---

## 9. Tech Stack (100% Free)

| Layer | Choice | Why |
|---|---|---|
| Language | **Python 3.11+** | Best ecosystem for scraping/automation/ML. |
| Backend | **FastAPI** | Async, fast, serves API + dashboard. |
| Database | **SQLite** | Zero setup, single file, perfect for 1 user. |
| ORM | **SQLAlchemy** | Standard, reliable. |
| Scheduling | **APScheduler** | In-process cron-like scheduling. |
| Browser automation | **Playwright** | Best free browser automation; JS-heavy forms. |
| HTTP/RSS | **httpx + feedparser** | Async HTTP + RSS parsing. |
| LLM (Tier 2) | **Groq free tier** (Llama 3.3 70B for generation, Llama 3.1 8B for classification) | Extremely fast inference; free; budgeted by our manager. |
| Local models (Tier 1) | **sentence-transformers** (all-MiniLM-L6-v2) + lightweight classifiers | Free, unlimited, CPU-fast semantic intelligence. |
| Resume → PDF | **WeasyPrint** (HTML→PDF) | Free, local, clean ATS-friendly PDFs. |
| Dashboard UI | **Plain HTML + JS + Chart.js** (full-featured: analytics, charts, all controls) | No build step, $0, instant load — full functionality without React overhead for 1 user. |
| Runtime phase 1 | **Local Windows** | Develop and validate core workflows locally; no always-on host required. |
| Cloud evaluation (later) | **Hugging Face Space or another currently suitable free host** | Optional; verify current quotas, privacy/access controls, persistent storage, sleep behavior, and scheduler support before adoption. |
| Dashboard wrapper (if needed for selected host) | **Host-compatible wrapper** | Choose only after cloud feasibility is verified; not a prerequisite for local MVP. |
| Config | **YAML** (`config.yaml`) | Profile, sources, thresholds, **Groq budget** in one file. |
| Packaging | **Local Windows setup and `start.bat` first; cloud packaging later if feasible** | One codebase; cloud-specific packaging follows the hosting evaluation. |

---

## 10. Groq Budget & Performance Plan

### Assumed free-tier limits (in `config.yaml`, adjustable)
- ~30 requests/min, ~1,440 requests/day, ~200M tokens/month.

### Estimated nightly consumption (200 new jobs)
| Task | Model | Requests | Notes |
|---|---|---|---|
| Deep fit scoring (top 15, batched 3–5/prompt) | 70B | ~4–5 | prefix-cached system+resume |
| Cover letters (top 15) | 70B | ~15 | one per job |
| Bullet polish (top 15) | 8B | ~15 | short outputs |
| Answers (top 15) | 8B | ~15 | short outputs |
| Eligibility edge cases | 8B | ~5–10 | only low-confidence |
| Red flags (batched, low priority) | 8B | ~5 | skipped if budget low |
| Self-heal / interview prep | 8B/70B | ~0–5 | event-driven |
| **Total** | | **~60–70 req/night** | **~5% of daily free budget** |

**Headroom:** retries, re-runs, "scan now", learning tasks, and growth to 500+ jobs/day all fit comfortably. The budget manager enforces the cap regardless.

### Performance engineering
- **Async everywhere** — collectors, HTTP, and LLM calls run concurrently.
- **Embeddings precomputed at collection time** — scoring never waits on Tier 1.
- **Prefix caching** — stable system prompt + master resume prefix cuts input tokens ~50% on repeated calls.
- **Batched prompts** — 3–5 similar jobs per deep-scoring request.
- **Semantic cache** — near-duplicate jobs reuse LLM outputs (30–60% savings on busy days).
- **Model tiering** — 8B for short/classification tasks, 70B only for letters + deep judgment.
- **Graceful degradation** — budget exhausted → Tier 0+1 keeps the pipeline alive; LLM tasks queue for the next window.

---

## 11. Milestones / Phases

| Phase | Deliverable | Est. effort |
|---|---|---|
| **P0 — Setup** | Repo structure, venv, config.yaml (incl. Groq budget), SQLite schema, master resume import, `start.bat` | Small |
| **P1 — Collect** | Greenhouse + Remotive adapters, source-compliant polling, strict South Asia employer/job-origin exclusion before storage, current-location eligibility checks, dedup eligible jobs, job storage, "scan now" | Medium |
| **P2 — Tier 1 Local Brain** | Embeddings pipeline, semantic dedup/cache, work-mode + eligibility + role-fit classifiers | Medium |
| **P3 — Groq Brain + Budget** | Groq client, budget manager (meter/priority/batch/prefix-cache/degrade), deep scoring, letters, answers, red flags, **Company Checker** (legitimacy + cached review summary) | Medium–Large |
| **P4 — Resume Tailoring** | Master resume model, deterministic tailoring + LLM bullet polish, **PDF rendering**, storage | Medium |
| **P5 — Morning Review Dashboard** | Review queue (job + PDF + letter + answers + reasoning + flags + budget panel), Approve/Edit/Reject, pipeline, stats, **Profile Manager** (full editable profile: contact, skills, experience incl. new jobs, projects + links, education, certifications, achievements, standard answers, preferences) | Medium–Large |
| **P6 — Apply (ATS)** | Application engine **triggered on approval**: ATS APIs + email, confirmation capture, safety rails | Large |
| **P7 — Apply (Web) + Self-Heal** | Playwright adapters for 2–3 company sites + LLM self-healing selectors | Large |
| **P8 — Learning + Polish** | Learning loop (weight drift, style memory), follow-ups, interview prep, dry-run, hardening | Medium |
| **P9 — Advanced Suite 1** | 100% confidence gate + second-look, email inbox monitor (auto outcomes), ghost job detector, interview coach (mock interview + STAR), chat with agent, keyboard-first + mobile + dark mode + backup | Large |
| **P10 — Advanced Suite 2** | ATS simulator, timing optimizer, hiring velocity, diversity guard, skill gap radar, rejection analyzer, salary playbook, referral + hiring-manager outreach, cover-letter intelligence, weekly reports, batch ops, receipts, calendar, streaks | Large |
| **P11 — Moonshots** | Voice commands, multi-profile personas, market heatmap, edge-case outreach, ideal-candidate inference, auto portfolio page, career path advisor | Medium |

**MVP = P0–P5:** the full morning loop — finds remote location-eligible jobs overnight, scores them with the three-tier brain, tailors your resume to a PDF, writes the letter, and you review + approve in the morning. **P6** makes approval actually submit. P7–P8 expand coverage and intelligence. **P9–P11** add the 100x feature suite (§5.12).

---

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **Groq free limits change / tighten** | Less LLM budget | Budget manager reads limits from config; Tier 0+1 pipeline is fully functional without any LLM; batching/caching stretch the budget; model tiering minimizes token cost. |
| Groq rate limit hit mid-cycle | Delayed LLM tasks | Priority queue + exponential backoff; low-priority tasks defer to next window; system never blocks. |
| Site HTML/API changes | Adapter breaks | Isolated adapters; health checks; **LLM self-healing selectors**; alert you, others keep running. |
| CAPTCHA / anti-bot | Application blocked | Pause → `NEEDS_HUMAN` (shown in dashboard Needs-You panel). Never paid solvers. |
| IP throttling/ban | Source stops working | Rate limits, random delays, daily caps, per-source backoff. |
| **LLM fabricates resume facts** | Damaged credibility | **Truthfulness guardrail:** tailoring only rephrases/reorders your master resume; never invents. You review the PDF before approving. |
| **LLM misjudges location eligibility** | You apply to a job you can't get | Three-tier check (rules → local classifier → LLM); reasoning visible in review; one-click reject. |
| Bad application (wrong answers) | Damaged impression | You approve every application (default); answers editable; full audit log. |
| Weak letters | Lower response rate | 70B model for letters; A/B styles; learning loop; editable before submit. |
| ToS concerns | Account/site issues | Prefer official/public endpoints; personal use only; no login-wall bypass. |
| **Free cloud limits / service sleep** | Pipeline delayed or data at risk | Do not depend on cloud for MVP validation; verify current limits and persistent storage before optional deployment, and retain tested local operation. |
| Local models slow on weak CPU | Slower Tier 1 | MiniLM is tiny (ms per job on CPU); embeddings batched; worst case, Tier 1 degrades to Tier 0 keyword mode. |

---

## 13. Open Questions (answer these, I'll update the PRD)

1. ~~Target role?~~ ✅ **Business Analyst**
2. ~~Country + work mode?~~ ✅ **South Asian employer/job origins are excluded; worldwide remote is allowed, including South Asian applicants, while current-user eligibility remains checked. Current location is a profile field.**
3. ~~Approval model?~~ ✅ **Morning review → Approve → agent submits**
4. ~~AI provider?~~ ✅ **Groq free tier** (budgeted three-tier architecture)
5. ~~Master resume?~~ ✅ **`Res.pdf` provided as format sample** — the actual master resume comes later; it gets imported into the Profile Manager (§5.10).
6. ~~Seniority?~~ ✅ **Junior–Mid**
7. ~~Min salary?~~ ✅ **Dynamic** — agent calculates the fair market rate per job; flags below-market pay.
8. ~~Standard answers?~~ ✅ **Notice period: immediate. Timezone: flexible (UTC+6, can overlap EU/US hours).**
9. ~~Target companies?~~ ✅ **Any** (favorites/exclusions can be added later in the dashboard).
10. ~~Applications/day cap?~~ ✅ **10** — agent scans all sources, stages the **top 10 best matches** daily.
11. ~~Dashboard style?~~ ✅ **Full-featured dashboard** — analytics, charts, all controls (plain HTML + JS + Chart.js, no build step).
12. ~~Deal-breakers?~~ ✅ **Strictly exclude South Asian employer/job origins; worldwide remote is allowed, including applicants in South Asia.** Other deal-breakers (on-call, travel, agencies) can be added anytime in the dashboard.
13. **LinkedIn:** no scraping (ToS + account-ban risk). Instead — download your LinkedIn profile **PDF** (⋯ → "Save to PDF") or the official **"Get a copy of your data"** JSON and drop it in the workspace; the agent imports it into the Profile Manager (§5.10). Also paste your LinkedIn/portfolio URL for the contact section.
14. ~~Skill list?~~ ✅ **Skills come from your master resume** (always re-scanned) + Skills Manager (add/remove + agent suggestions). No manual list needed — the pool auto-syncs.
15. **Runtime/deployment:** ✅ Local Windows development and validation first. Revisit private free cloud hosting after confirming current quotas, persistent disk, privacy/access controls, sleep behavior, and scheduler support; do not assume any provider is permanently free.

---

## 14. Master Plan — How We'll Build It

> Step-by-step build order. Each phase ends in a working, testable state. Value early, risk low.

### Phase 0 — Foundation (Day 1)
- [ ] Repo structure (`backend/`, `frontend/`, `config/`, `data/`, `resumes/`, `output/`).
- [ ] venv + deps (FastAPI, SQLAlchemy, APScheduler, httpx, feedparser, Playwright, Groq SDK, sentence-transformers, WeasyPrint).
- [ ] `config.yaml` — profile, work mode (remote), **location engine (current country + South-Asia exclusion)**, sources, thresholds, **Groq budget**, daily cap.
- [ ] SQLite schema (all §7 tables) + migrations.
- [ ] **Import master resume** → structured JSON.
- ✅ **Done when:** app boots, DB created, resume loaded, `start.bat` works.

### Phase 1 — Collect (Days 2–4)
- [ ] Adapter framework (one class per source → normalized `Job`).
- [ ] MVP adapters: **Greenhouse public Job Board GET API** (finite curated board-token allowlist) and **Remotive public API** under attribution and polling terms.
- [ ] Async collection + normalization + **strict South Asia origin/applicant-location filter before persistence (Tier 0)**.
- [ ] Dedup (fingerprint) + job storage + scheduler + "scan now".
- ✅ **Done when:** a scan pulls supported source data, discards excluded jobs before persistence, and stores only eligible listings (an empty result is valid).

### Phase 2 — Tier 1 Local Brain (Days 5–7)
- [ ] Embedding pipeline (MiniLM) at collection time.
- [ ] Semantic dedup + semantic cache.
- [ ] Local classifiers: work-mode, location-eligibility, role-fit.
- [ ] Semantic skill matching in scoring.
- ✅ **Done when:** jobs get semantic scores; near-dupes merged; eligibility classified without any API call.

### Phase 3 — Groq Brain + Budget (Days 8–11)
- [ ] Groq client (8B + 70B tiering) + **budget manager** (meter, priority queue, batching, prefix caching, graceful degradation).
- [ ] Deep fit scoring (top-N) with reasoning + risk notes.
- [ ] Cover letters + application answers.
- [ ] Red-flag detection (batched, low priority).
- [ ] **Company Checker:** legitimacy signals (domain age, LinkedIn size, scam patterns) + cached LLM review summary (salary, environment, culture).
- [ ] Budget panel data (usage, forecast).
- ✅ **Done when:** top-N jobs get LLM judgment + letters within budget; budget exhaustion degrades gracefully.

### Phase 4 — Resume Tailoring + PDF (Days 12–14)
- [ ] Master resume model (editable in dashboard).
- [ ] Deterministic tailoring (reorder/keyword-align) + LLM bullet polish (truthfulness guardrail).
- [ ] **PDF rendering** (WeasyPrint) → ATS-friendly PDF per job.
- ✅ **Done when:** each top job has a tailored, job-specific resume PDF.

### Phase 5 — Morning Review Dashboard (Days 15–19)
- [ ] FastAPI serves dashboard.
- [ ] **Review queue:** job + fit/reasoning + PDF + letter + answers + red flags + urgency + salary estimate.
- [ ] **Approve / Edit / Reject** + pipeline view + stats + budget panel.
- [ ] **Profile Manager:** full editable profile — identity/contact, summary, skills, experience (add new jobs), projects + links, education, certifications, achievements, languages, standard answers, search preferences; versioned saves; completeness check.
- ✅ **Done when:** you open the dashboard in the morning and can review/approve/reject last night's matches, and can edit any part of your profile.

### Phase 6 — Apply on Approval (Days 20–25)
- [ ] Application engine **triggered by approval**.
- [ ] ATS API submitters (Greenhouse, Lever) + email applications.
- [ ] Confirmation capture + pipeline update + safety rails (cap, delays, audit, dry-run).
- ✅ **Done when:** Approve → agent submits with your tailored PDF → confirmation stored.

### Phase 7 — Web Applications + Self-Heal (Days 26–31)
- [ ] Playwright adapters for 2–3 direct company sites.
- [ ] CAPTCHA/login-wall → `NEEDS_HUMAN` (dashboard Needs-You panel).
- [ ] **Self-healing selectors** (page snapshot → Groq → one-tap fix).
- ✅ **Done when:** agent submits on non-ATS web forms and heals broken selectors.

### Phase 8 — Learning + Polish (Days 32–35)
- [ ] Learning loop: weight drift from approvals/rejections/outcomes; style memory from your edits.
- [ ] Follow-up drafts (day 7) + outcome tracking.
- [ ] Interview prep (predicted questions from JD).
- [ ] Dry-run mode, error hardening, per-source health checks.
- ✅ **Done when:** the agent measurably gets smarter about you and runs reliably unattended.

### Phase 9 — Advanced Suite 1 (Days 36–42)
- [ ] **100% confidence gate** + second-look queue + calibration.
- [ ] **Email inbox monitor** (IMAP): auto-detect interview invites / rejections / confirmations → auto-update pipeline.
- [ ] **Ghost job detector** (stale-posting signals → auto-demote).
- [ ] **Interview coach:** likely questions, mock interview (Groq plays interviewer), STAR builder, negotiation simulator.
- [ ] **Chat with your agent** (RAG over full application history).
- [ ] Keyboard-first + mobile-friendly + dark mode + one-click backup.
- ✅ **Done when:** outcomes update themselves from email; you can mock-interview before any real interview; 30-second morning scan.

### Phase 10 — Advanced Suite 2 (Days 43–52)
- [ ] ATS simulator, application timing optimizer, hiring velocity, diversity guard.
- [ ] Skill gap radar, rejection pattern analyzer, salary negotiation playbook.
- [ ] Referral finder + hiring-manager outreach (drafts + tracking).
- [ ] Cover-letter intelligence, weekly/monthly reports, batch ops, receipts, calendar, streaks.
- ✅ **Done when:** the agent optimizes *when* and *how* you apply, and tells you exactly what to learn next.

### Phase 11 — Moonshots (Days 53+)
- [ ] Voice commands (local Whisper), multi-profile personas, market heatmap.
- [ ] Edge-case outreach, ideal-candidate inference, auto portfolio page, career path advisor.
- ✅ **Done when:** the system feels like a full-time career assistant, not a tool.

## 12. Detailed Operational Behaviors and Edge Cases

### 12.1 Search Philosophy
The system is designed to behave like a high-trust personal research assistant, not a spam bot. It deliberately sacrifices raw volume to protect quality. For every job, it asks five questions:
1. Is it in scope?
2. Is it truly a fit for your profile?
3. Is the company credible?
4. Can the job be done from your current location and timezone?
5. Is the risk worth the effort?

A job only reaches the review queue if the answer is clearly yes to all five.

### 12.2 Role-Specific Matching Rules
The system is heavily role-aware. Because the user is a Business Analyst, matching is not generic. It should identify and differentiate:
- functional BA work
- data analyst / product analyst work
- operations analytics roles
- airline / revenue / pricing analytics work
- stakeholder-facing BA work
- data-heavy but not BA-heavy roles

The engine should infer when a job title includes the word “analyst” but the content is actually:
- account management
- sales enablement
- marketing analytics
- general operations without stakeholder translation work

In those cases, the job may still match partially but loses score if it does not align with your declared BA identity.

### 12.3 Location and Legal Constraints
The search engine must encode rules in a way that is explicit, maintainable, and understandable. This includes:
- remote jobs with explicit “US only” or “EU only” restrictions
- jobs requiring local citizenship or work authorization
- jobs needing onsite attendance from specific city or country
- jobs with timezone requirements incompatible with your schedule
- jobs discovered in excluded locations (strict South Asian exclusion)

This logic lives in the filtering layer and should produce a machine-readable reason for rejecting each job, such as:
- `country_excluded`
- `role_mismatch`
- `salary_below_market`
- `not_remote`
- `work_auth_required`
- `timezone_conflict`
- `company_red_flag`

### 12.4 Exact Morning Review Flow
The morning review flow is the product’s single most important user experience. The user should never need to open multiple tools to decide. A job card must support the following:
- open job description
- view source link
- open tailored resume PDF
- open generated cover letter
- see prefilled answer sheet
- edit answer text inline
- mark as approve / edit / reject
- view company legitimacy score and summary
- adjust urgency / apply later / skip
- add a manual note

The system should keep the review under 5 minutes for 10 jobs.

### 12.5 Application Submission Rules
The agent may apply only after user approval. Required rules:
- no application without explicit approval
- no duplicate submission to same job
- no repeated attempts beyond a configured retry cap
- no submission when there is a red flag or unresolved “needs you” issue
- any failed or blocked submission is automatically marked `NEEDS_HUMAN`
- all confirmation evidence is stored for the user

### 12.6 LLM Safety Rules
The LLM is assistive, not authoritative. It should never:
- invent past job titles or employers
- add fake certifications
- claim a skill the user does not explicitly have or have validated
- create misleading salary claims
- alter facts without user review

The system should display a small “source evidence” area for every generated resume bullet or cover-letter sentence, showing the original resume context, job requirement, and generated adaptation.

### 12.7 Budget Fallback Behaviors
When the Groq budget is exhausted, the system should degrade gracefully:
- still collect jobs
- still filter and dedupe
- still score with Tier 0 and Tier 1
- still rank jobs
- still create a plain resume draft without LLM polish if needed
- queue deeper LLM work for the next cycle

The dashboard should show the user “LLM queue paused at 18:50 due to budget cap; next budget window 00:30.”

### 12.8 User Edit Memory
The system should record what the user edits and use those edits to improve future generations.
Examples:
- the user removes “marketing” wording from every cover letter → store as a style preference
- the user consistently shortens the summary → adjust the default summary template
- the user rejects all consulting roles with “travel-heavy” language → set travel-based weights lower

This is not just personalization; it is a crucial learning feature.

### 12.9 Evidence and Audit Model
Every job in the system should be auditable. For each job, the system should retain:
- original source URL
- original raw payload
- normalized data
- filters passed/failed
- exact score components
- company check result
- tailored resume version ID
- cover-letter version ID
- answer version ID
- submission method
- screenshot / confirmation URL
- final outcome

This makes the product reliable and explainable.

### 12.10 Failure Recovery Model
The system must recover from partial failures without losing queue state. Recovery tools include:
- retry queue for failed scrapers
- resume generation retry with last good version
- stale company review refresh
- failed job-stage recovery on restart
- reprocessing of cached jobs when new profile fields are changed

### 12.11 Future Personalization Layers
The product becomes much stronger when it remembers patterns over time, such as:
- which company types are most likely to respond
- which role wording attracts better interviews
- which salary ranges get positive responses
- which resume narratives convert best for BA roles
- which days of the week yield the strongest results

These patterns should show in analytics and influence future rank ordering.

---

## 13. Detailed UI / Screen Specifications

### 13.1 Dashboard Home – Review Queue
Purpose: single-page review and action center.

Each job row includes:
- company logo or brand placeholder
- job title
- company name
- location
- work mode
- posted time
- salary info
- fit score
- company check badge
- urgency indicator
- “why this job?” explanation
- actions: preview, approve, edit, reject, save for later

### 13.2 PDF Preview Panel
Purpose: let the user review the exact resume they would submit.

The preview should include:
- version number
- job title and company name
- selected skills only
- summary tailored to the JD
- ATS-safe layout
- key project bullets
- clear separation of “user facts” and “adaptation” sections

### 13.3 Cover Letter Panel
Purpose: show a polished, editable draft.

Should include:
- opening statement
- fit summary with JD-specific language
- selected experience and project references
- closing line
- edit mode with markdown/plain text support

### 13.4 Answers Panel
Purpose: display the pre-filled questionnaire answers.

It should show:
- each question
- answer text
- confidence label
- editable fields
- ability to mark “use standard answer” or “customize manually”

### 13.5 Needs-You Panel
Purpose: manage manual intervention tasks.

Examples:
- playright form failed due to CAPTCHA
- application portal requires login
- Groq budget queue paused
- a source adapter stopped working
- a company check is stale and needs a refresh

### 13.6 Profile Manager Screen
Purpose: let the user maintain all personal data with versioning.

Sections:
- personal information
- skills
- experience
- projects
- education
- certifications
- achievements
- languages
- preferences
- standard answers
- security / privacy / export

Every change should appear in version history and have a dashboard completeness indicator.

### 13.7 Analytics Screen
Purpose: give the user confidence the system is working.

Charts should include:
- jobs discovered per day
- jobs scored and queued
- approval rate
- response rate by source
- response rate by skill cluster
- company legitimacy distribution
- LLM spend over time
- interview conversion by role type

### 13.8 Budget Screen
Purpose: show AI usage discipline.

Fields:
- total requests used today
- total tokens used
- model allocation
- queued tasks
- estimated remaining budget
- performance warnings

---

## 14. Detailed Configuration Example

```yaml
profile:
  name: "MD Nafiz Mahfuz"
  headline: "Business Analyst | Data Analyst"
  current_country: "Bangladesh"
  location_mode: "remote_first"
  remote_allowed: true
  excluded_countries:
    - Bangladesh
    - India
    - Pakistan
    - Sri Lanka
    - Nepal
    - Bhutan
    - Maldives
    - Afghanistan
  remote_applicant_policy: "allow_worldwide_exclude_south_asian_job_origins"
  timezone: "UTC+6"
  notice_period: "immediate"
  experience_level: "junior_mid"
  daily_application_cap: 10
  work_modes:
    remote: true
    hybrid: false
    onsite: false

search:
  sources:
    greenhouse: true
    remotive: true
    lever: false
    workable: false
    remote_ok: false
    remote_leaf: false
    rss: false
    adzuna: false
    direct_company_pages: false
  greenhouse_board_tokens: []  # Add only verified public board tokens; no global discovery.
  min_fit_score: 85
  second_look_threshold: 80
  use_llm_for_deep_score: true
  max_jobs_per_day: 50

ai:
  llm_provider: "groq"
  budget_daily_requests: 1440
  budget_daily_tokens: 20000000
  tier0_enabled: true
  tier1_enabled: true
  tier2_enabled: true
  semantic_cache_enabled: true
  use_prefix_cache: true

resume:
  strict_truthfulness: true
  max_pages: 2
  prefer_ats_layout: true
  include_only_job_relevant_skills: true

submission:
  require_user_approval: true
  default_delay_ms_min: 1500
  default_delay_ms_max: 5000
  dry_run_mode: true
```

---

## 15. Technical Implementation Notes

### 15.1 Local-first Strategy
The system should always prefer:
- deterministic logic
- local semantics
- cached outputs
- user-controlled settings

Only after those are exhausted should the LLM be used.

### 15.2 Single-User Database Design
This is not a multi-tenant SaaS product. It should be built for one user with a simple but structured schema. SQLite is sufficient for the initial product and makes backups easy.

### 15.3 Deployment Model
- Phase 1: local Windows mode for development, testing, and MVP validation.
- Phase 2: optional private cloud deployment after current provider pricing/quotas, persistence, privacy controls, and scheduler behavior are verified.
- Maintain one codebase and reliable local operation; cloud hosting is not an MVP dependency.

### 15.4 Security and Privacy Model
- no personal data in public repos
- use env secrets for API keys
- keep resumes and PDFs in local or private storage
- store analytics and logs but never expose them publicly

---

## 16. Definition of Done for MVP
The MVP is complete when all of the following are true:
1. jobs are discovered from multiple free sources
2. jobs are normalized and deduplicated
3. jobs pass location and role filters
4. fit is scored using deterministic + semantic + LLM reasoning
5. top matches are placed into the review queue
6. the user can review a tailored PDF and editable cover letter/answers
7. the user can approve or reject each item
8. approval triggers application submission using the configured method
9. application status and results are recorded
10. all outcomes are visible in analytics and pipeline views

---

### Build Principles
1. **Small, working steps** — every phase ends with something you can use.
2. **Isolated adapters** — one broken source never kills the system.
3. **Human-in-the-loop by default** — nothing submits without your approval.
4. **Truthfulness guardrail** — the tailorer never invents facts.
5. **Spend tokens like money** — Tier 0 → Tier 1 → Tier 2; LLM only where it matters.
6. **Free & local** — no paid APIs, no cloud, runs on your PC.

### What "Intelligent & Highly Capable" Means Here
- **Understands** jobs (embeddings + LLM reading, not keyword matching).
- **Tailors** your resume per job into a real PDF.
- **Judges** location-eligibility and fit with reasoning you can read.
- **Acts** on your behalf (submits) once you approve.
- **Heals itself** (broken selectors → LLM-proposed fixes).
- **Budgets its own brain** (meters, batches, caches, degrades — never wastes, never stops).
- **Learns** from your decisions and outcomes to get better about *you* over time.

---

## 15. Changelog

| Date | Change |
|---|---|
| 2026-09-30 | Initial PRD drafted. |
| 2026-09-30 | User confirmed: role = **Business Analyst**; work mode = user-settable; system = fully autonomous personal agent. |
| 2026-09-30 | **Historical pivot (location scope superseded):** this revision targeted remote jobs doable from Bangladesh. Final policy excludes South Asian employer/job origins but allows worldwide remote roles that accept South Asian applicants. Retained product decisions: master resume tailored per job into a PDF; morning review and approval flow; Daily Loop, Resume Tailoring Engine, Morning Review Dashboard, Learning Loop, Master Plan. |
| 2026-09-30 | **Advanced rewrite:** AI constraint = **Groq free tier** → new **three-tier intelligence architecture** (deterministic → local embeddings/classifiers → budgeted Groq LLM), **Token Budget Manager** (metering, priority queue, batching, prefix caching, graceful degradation), semantic cache/dedup, self-healing selectors, red-flag detection, urgency + success prediction, A/B letters, budget panel, performance targets, and a full Groq budget plan. |
| 2026-09-30 | **Removed notifications** (Telegram/email push) per user — you check the dashboard every morning anyway. Added a **Needs-You panel** to the dashboard for CAPTCHA / failed submits / broken adapters. Renumbered phases (P8 Notify removed; Learning+Polish is now P8). |
| 2026-09-30 | **Profile seeded from `Res.pdf`** (contact, skills, experience, projects, education, certifications, languages). Added **§5.10 Profile Manager** — a full editable profile page in the dashboard (identity/contact, summary, skills, experience incl. new jobs, projects + links, education, certifications, achievements, languages, standard answers, preferences; versioned saves, completeness check). Data model expanded; P5 now includes the Profile Manager. |
| 2026-09-30 | **User answers integrated:** seniority = Junior–Mid; min salary = **dynamic market-rate calculation per job** (below-market flagged); notice period = immediate; timezone = flexible (EU/US overlap); target companies = any; daily cap = **top 10 best matches/day**; dashboard = **full-featured with analytics tab + all controls** (HTML+JS+Chart.js); skills = seed list, user will refine incrementally. LinkedIn URL still missing (not in Res.pdf). |
| 2026-09-30 | **LinkedIn strategy decided: no scraping** (ToS violation + account-ban risk for a job seeker). Added **official LinkedIn import** to the Profile Manager — user downloads the profile PDF ("Save to PDF") or the "Get a copy of your data" JSON export, drops it in the workspace, agent parses + diffs + updates the profile. Re-syncable anytime. |
| 2026-09-30 | **Precision tailoring + Skills Manager:** skill pool = master resume (always re-scanned) + manual adds + agent **skill suggestions**; tailored resume includes **only the skills that job needs** (JD ∩ your skills, no padding) with automatic domain relevance (airline → aviation skills surface). Added `skills` table (categorized, weighted, learned). Strengthened **§5.9** — every application tracked end-to-end with outcomes; per-skill/per-source/per-style learning for near-perfect results over time. |
| 2026-09-30 | **Historical location policy (superseded):** this earlier revision allowed worldwide remote jobs and excluded South Asia job origins. A temporary stricter revision also rejected South Asian applicants, but that restriction has since been removed. Current rule: exclude South Asian employer/job origins; allow worldwide remote when the user is eligible. Other changes in this entry: current location became a profile field and the Company Checker was added. |
| 2026-09-30 | **Cloud + 100x suite:** hosting moved to **Hugging Face Space** (free, private, scheduled nightly runs, persistent disk; PC = browser only; local fallback kept). Added **§5.0a 100% Confidence Gate** (fit ≥85 + confirmed eligibility + legit company + no red flags + ≥80% skill coverage; fewer than 10 is OK; second-look queue; calibration). Added **§5.12 Advanced Feature Suite** — 30 features in 4 groups (smarter matching, outreach + interviews, dashboard/UX, moonshots) phased P9–P11. New tables: outreach, interviews, documents, watchlist, salary_benchmarks. |
| 2026-09-30 | **Final implementation decisions:** MVP starts with local Windows development/validation, then optionally evaluates private free cloud after checking current quotas, persistence, privacy, and scheduler support. Initial sources: public Greenhouse Job Board GET API with curated board tokens and Remotive public API under attribution/linking, 24-hour delay, and polling limits. Exclude South Asian employer bases and actual job locations even when remote; worldwide remote roles may accept applicants in South Asia, including Bangladesh. Candidate eligibility is still checked against the user's current location. This entry supersedes earlier location and cloud-first wording. |

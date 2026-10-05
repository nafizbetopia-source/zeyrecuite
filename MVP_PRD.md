# MVP PRD — ZEYRECUITE

## 1. Product Summary

ZEYRECUITE MVP is a personal AI-powered job review assistant for a Business Analyst user looking for remote work opportunities. The system collects job listings, evaluates them against the user profile, ranks the best-fit roles, tailors the user’s resume for each role, and presents a morning review dashboard where the user can approve or reject jobs before applying.

The MVP is intentionally narrow and focused. It is not a full autonomous AI recruiter. It is a trusted review system that saves the user time and reduces manual searching and tailoring work.

---

## 2. Goal

The primary goal of the MVP is to help the user do the following every morning:

1. find relevant jobs from a limited set of reliable sources
2. filter out unusable jobs
3. rank the strongest matches
4. generate a tailored resume version for each strong match
5. generate a cover letter draft
6. show the user a simple review queue
7. let the user approve or reject before applying
8. store the outcome and improve suggestions over time

---

## 3. Core User Problem

The user is a Business Analyst currently in Bangladesh. The system must exclude jobs whose employer or actual job location is in South Asia, while allowing worldwide remote roles, including those open to South Asian applicants, if the current user is eligible. The user does not want to manually:
- search many websites
- read dozens of job posts
- compare skills to each job
- rewrite resume content repeatedly
- prepare custom cover letters manually
- track applications in scattered places

The MVP solves this problem by reducing the work to a morning review cycle.

---

## 4. MVP Vision

The MVP acts like a personal job-review assistant. It does the repetitive work in the background, but the user remains in control of final decisions.

It is designed to be:
- personal
- low-cost
- transparent
- human-approved
- privacy-aware
- accurate enough to trust

---

## 5. Target Persona

### User Type
- single user
- Business Analyst / Data Analyst profile
- remote-first search
- current location tracked in profile
- strict South Asian exclusion rules
- wants clear morning review workflow

### User Needs
- save time
- avoid irrelevant jobs
- avoid repeated manual resume editing
- apply only to jobs with strong fit
- review decisions in one dashboard
- preserve control of the final application decision

---

## 6. MVP Scope

### In Scope
- job collection from a small set of public sources
- normalization and deduplication
- role and location filtering
- skill matching and ranking
- master profile management
- master resume management
- job-specific resume tailoring
- PDF generation
- cover letter generation
- review queue dashboard
- approval/rejection flow
- basic status tracking
- basic learning from user actions

### Out of Scope
- full autonomous application submission across all sites
- full browser automation for all job portals
- email inbox parsing
- referrals and outreach engine
- interview coaching
- voice commands
- multi-profile personas
- advanced research assistant features
- full company review intelligence beyond basic legitimacy signals

---

## 7. Hard Constraints

### Business Constraints
- project must be free to build and run
- no paid subscription dependency
- personal use only
- no scraping or misuse of public profiles
- no fake resume facts
- user approval required before application action

### Technical Constraints
- Python-based implementation preferred
- SQLite for simple single-user data storage
- FastAPI for API backend
- HTML/JS dashboard for simplicity
- LLM use must be budgeted
- local processing should work before LLM is invoked

### MVP Runtime Decision
- Build and validate on the user's local Windows machine first.
- Consider private free cloud deployment only after the MVP works locally and the provider's current quotas, persistence, privacy, and scheduled-task limits have been verified.
- Do not make the MVP dependent on a cloud free tier that may change or sleep.

---

## 8. Core User Workflow

### Morning Review Flow
1. The system collects jobs overnight or on-demand.
2. Jobs are normalized and deduplicated.
3. Jobs are filtered against role and location rules.
4. Jobs are scored and ranked.
5. Strong jobs are turned into tailored resume drafts.
6. Cover letters are generated.
7. The user reviews the job review queue in the dashboard.
8. The user approves, edits, or rejects each job.
9. Approved jobs are tracked in the application pipeline.
10. Outcomes are stored and used to improve recommendations.

---

## 9. MVP Functional Requirements

### FR-01: Job Collection
The MVP shall collect jobs from these two sources:
- Remotive public Remote Jobs API (`GET https://remotive.com/api/remote-jobs`), polled no more than four times per day and never more than twice per minute; results are delayed by 24 hours and the dashboard must attribute Remotive and link each listing to its Remotive URL.
- Selected employers' public Greenhouse Job Board API (`GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true`), using a finite, user-maintained allowlist of public board tokens. The MVP must seed and validate this list; it must not attempt an unbounded company-board crawl. Read-only GET endpoints require no authentication; the MVP does not use Greenhouse's authenticated application-submission endpoint.

Source references: [Remotive API documentation and terms](https://github.com/remotive-com/remote-jobs-api), [Greenhouse Job Board API documentation](https://docs.greenhouse.io/job-board.html).

Adapters must be independent. Respect source terms, retain source attribution and canonical apply links, and do not bypass access controls. Additional sources are future scope after the two MVP adapters are validated.

### FR-02: Job Normalization
The system shall convert raw job postings into a standard internal job model containing title, company, location, work mode, description, salary, URL, posted date, and source.

### FR-03: Deduplication
The system shall remove duplicate jobs across sources using a stable fingerprint and basic semantic deduplication.

### FR-04: Filtering
The system shall reject jobs that fail location, role, work-mode, or obvious quality constraints. Reject a job if its employer base or actual job location is in a South Asian excluded country, regardless of remote label. Normalize job-origin country names and aliases to ISO 3166-1 alpha-2 codes and apply the hard deny set `BD, IN, PK, LK, NP, BT, MV, AF`. Worldwide remote roles may include applicants in South Asia; use `candidate_required_location` to determine whether the current user is eligible. A remote role restricted to locations that exclude the user's current country is rejected. Unknown employer/job origin is held for verification and cannot be included until resolved. The deterministic origin gate cannot be overridden by scoring, embeddings, or an LLM. An empty eligible queue is valid when no roles satisfy these rules.

### FR-05: Role Fit Scoring
The system shall compute a role-fit score using profile, skill matching, and job description analysis.

### FR-06: Resume Tailoring
The system shall generate a job-specific resume from the master profile and master resume without inventing facts.

### FR-07: PDF Output
The system shall generate a PDF version of each tailored resume for user review.

### FR-08: Cover Letter Draft
The system shall generate a short tailored cover letter for the job.

### FR-09: Dashboard Review Queue
The system shall present jobs in a review queue with fit score, reasoning, PDF preview, cover letter preview, source, and action buttons.

### FR-10: User Approval Actions
The dashboard shall allow the user to approve, edit, or reject each job.

### FR-11: Application Tracking
The system shall track approved jobs and their statuses in a pipeline.

### FR-12: Outcomes Learning
The system shall store user decisions and outcomes so future scoring can improve.

---

## 10. MVP Non-Functional Requirements

### NFR-01: Ease of Use
The dashboard must be fast to review and easy to understand.

### NFR-02: Trust and Transparency
Every job should contain a simple explanation of why it matched or why it was rejected.

### NFR-03: Data Safety
User data must remain private and not be exposed publicly.

### NFR-04: Reliability
A failure in one source or one adapter must not break the entire system.

### NFR-05: Low Cost
LLM usage must be tightly controlled and should not exceed a defined free-tier budget.

---

## 11. MVP User Experience Requirements

### UX-01: Morning-only workflow
The system should be optimized for a quick morning review, not a large daily deep-dive.

### UX-02: Simple decision model
Each job card should be easy to act on with Approve, Edit, or Reject.

### UX-03: Clear reasoning
The user should understand why the system thinks a job fits.

### UX-04: One dashboard
Everything relevant to the morning review should exist in one place.

---

## 12. MVP Success Criteria

The MVP is successful when:
- the user can collect jobs from multiple supported sources
- the user can see relevant ranked jobs in a dashboard
- the system produces tailored resumes and cover letters for strong matches
- the user can approve or reject jobs from the same review screen
- application progress is recorded and visible
- the system has a basic learning loop

---

## 13. MVP Release Gate

The MVP is release-ready only when:
- real job data can be ingested successfully
- a ranked queue is produced without manual intervention
- a tailored resume PDF is generated for a real job
- the user can review the results in a simple dashboard
- user actions are stored and reflected in the pipeline

---

## 14. MVP Completion Definition

The MVP is complete when it can reliably perform the core job-review workflow for the user and provide a trustworthy daily decision queue.

It does not need to be the final complete career assistant; it only needs to become a strong and useful first version.

---

## 15. Final MVP Recommendation

The MVP should not try to fully automate the entire job application lifecycle.
It should focus on:
- finding jobs
- filtering intelligently
- tailoring materials
- reviewing them quickly
- tracking user decisions

That is the correct first milestone.

# MVP SRS — ZEYRECUITE

## 1. Document Purpose

This document defines the requirements for the MVP of ZEYRECUITE, a personal AI-assisted job review system for a Business Analyst user. The purpose of the MVP is to provide a working, trustworthy, single-user job review system that helps the user find relevant jobs, rank them, tailor materials, and review them before applying.

This MVP is intentionally narrower than the full vision. It is designed to be implementable and useful without attempting to build the full autonomous career assistant in one release.

---

## 2. Product Objective

The MVP shall help the user:
- discover jobs from a limited set of public and reliable sources
- filter out low-quality or irrelevant jobs
- match the best roles to the user profile
- generate tailored resume versions for selected jobs
- generate cover letters for selected jobs
- review jobs in a morning dashboard
- approve or reject jobs before application
- track results and store user decisions

---

## 3. Scope

### In Scope
- job collection
- job normalization
- deduplication
- filtering
- ranking
- profile and resume management
- resume tailoring
- PDF rendering
- cover letter generation
- dashboard review queue
- approval tracking
- basic analytics
- learning from user action history

### Out of Scope
- full automated job application engine for all sites
- browser automation across every portal
- inbox monitoring
- mock interview system
- outreach automation
- referral and hiring manager workflow
- voice assistant features
- multi-profile management
- advanced market intelligence features

---

## 4. User Needs

### Primary User Need
The user needs a way to reduce the time spent searching, filtering, tailoring, and reviewing job applications.

### Secondary User Needs
- avoid low-quality jobs
- keep the process simple
- trust that the system is using their actual profile and not inventing facts
- review everything in one dashboard
- make decisions with low effort

---

## 5. Functional Requirements

### FR-01: Source Collection
The MVP shall collect jobs from two independent public sources:
- Remotive public API at `https://remotive.com/api/remote-jobs`, using unauthenticated GET requests. Poll no more than four times per day and never more than twice per minute; honor its 24-hour publication delay, display Remotive attribution, and link to the original Remotive listing.
- Greenhouse Job Board API at `https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true`, using a finite, user-maintained allowlist of public employer board tokens. Seed and validate this list for the MVP; do not attempt an unbounded company-board crawl. Public GET endpoints require no authentication. Application submission endpoints are out of MVP scope.

Use only these sources in the initial MVP; add adapters later after validating the core workflow. References: [Remotive API documentation and terms](https://github.com/remotive-com/remote-jobs-api), [Greenhouse Job Board API documentation](https://docs.greenhouse.io/job-board.html).

### FR-02: Data Normalization
Each collected job shall be normalized into a shared job format with all required fields.

### FR-03: Deduplication
The system shall remove duplicate job entries across sources.

### FR-04: Filter Engine
The system shall remove jobs that do not match the user’s role, location, work-mode, and basic quality constraints. Reject a job if its employer base or actual job location is in a South Asian excluded country, even if remote. Normalize job-origin country names and aliases to ISO 3166-1 alpha-2 codes and apply the hard deny set `BD, IN, PK, LK, NP, BT, MV, AF`. Worldwide remote roles may include South Asian applicants; use `candidate_required_location` to check whether the current user can apply. Reject remote roles that exclude the user's current location. Unknown employer/job origin is held for verification and cannot be included until resolved. The deterministic origin gate cannot be overridden by scoring, embeddings, or an LLM. An empty eligible queue is valid when no role passes.

### FR-05: Role Fit Score
The system shall score jobs based on user profile and job requirements.

### FR-06: Skill Match
The system shall compare user skills with job requirements and score the match.

### FR-07: Master Profile
The system shall maintain a master profile with personal details, skills, work history, education, certifications, projects, and preferences.

### FR-08: Resume Versioning
The system shall maintain versioned resume records for each tailored job-specific resume.

### FR-09: Resume Tailoring
The system shall create a tailored resume per job using the user’s master profile and master resume without inventing facts.

### FR-10: PDF Generation
The system shall export the tailored resume to PDF for user review.

### FR-11: Cover Letter Generation
The system shall generate a short cover letter draft using the job and user profile.

### FR-12: Dashboard Review Queue
The system shall display pending jobs in a clear, curated review queue.

### FR-13: Review Actions
The dashboard shall allow the user to approve, edit, or reject a job.

### FR-14: Tracking Pipeline
The system shall keep a record of approved and rejected jobs and their statuses.

### FR-15: Learning Engine
The system shall store user responses and outcomes and use them to improve future job rankings.

---

## 6. Non-Functional Requirements

### NFR-01: Performance
The dashboard and review workflow should be fast enough for a daily morning cycle.

### NFR-02: Trustworthiness
The resume generation must avoid fabricated facts or invented experience.

### NFR-03: Usability
The dashboard must be easy to understand and quick to act on.

### NFR-04: Maintainability
The system must keep source adapters independent so a broken source does not stop the whole product.

### NFR-05: Cost Control
The system must enforce a limited AI budget and degrade gracefully when the budget is exhausted.

### NFR-06: Privacy
The system must protect personal data and operate on a private, single-user basis.

---

## 7. User Stories

### US-01
As a user, I want the system to collect relevant jobs automatically so I do not need to search manually.

### US-02
As a user, I want low-fit jobs filtered out so I do not waste time.

### US-03
As a user, I want each job to show a clear fit score and explanation.

### US-04
As a user, I want a tailored resume PDF so I do not rewrite it every time.

### US-05
As a user, I want a simple morning dashboard so I can review jobs quickly.

### US-06
As a user, I want to approve or reject jobs before any application action happens.

### US-07
As a user, I want my decisions to improve future recommendations.

---

## 8. Functional Workflow

### 8.1 Daily Workflow
1. The system collects jobs from selected sources.
2. Jobs are normalized and deduplicated.
3. Obvious mismatches are filtered out.
4. The system ranks jobs by fit.
5. The user opens the morning review dashboard.
6. Each job shows fit score, resume PDF, cover letter, and decision actions.
7. The user approves, edits, or rejects jobs.
8. The system records the result and updates the learning layer.

### 8.2 Review Queue Behavior
The queue must present the best-fit job cards first and include:
- job title
- company
- likely location
- salary or estimate
- score
- a reason it matches
- link to source
- preview of generated resume
- preview of cover letter
- approve/edit/reject buttons

---

## 9. Data Requirements

### Core Entities
- user_profile
- skills
- resume_versions
- jobs
- applications
- events
- learning_records
- companies

### Required Data Fields
- user profile data
- work experience and education
- certifications and projects
- skill list with categories
- job source and URL
- status and timestamps
- outcome state
- resume version link

---

## 10. UI Requirements

### Dashboard Views
- review queue
- job details
- resume preview
- cover-letter preview
- application pipeline
- simple analytics view

### Interaction Requirements
- approve
- reject
- edit
- filter
- sort by score or date

---

## 11. Acceptance Criteria

The MVP shall be accepted when the following are true:
- it can collect jobs from supported sources
- it can store and normalize them
- it can filter out bad-fit jobs
- it can rank jobs by fit
- it can generate tailored resume PDFs for strong matches
- it can create cover letter drafts
- it can show a review queue for user decisions
- it stores user approvals and rejections
- it tracks each application state in a pipeline

---

## 12. Risks and Constraints

### Risk 1: Source instability
Job sites change frequently. Adapter logic must be isolated.

### Risk 2: Inaccurate fit scoring
A weak scoring model can produce bad ranking. The user must always be able to review and reject.

### Risk 3: Resume trust risk
The system must never invent facts. Truthfulness must be treated as a hard rule.

### Risk 4: Budget pressure
LLM use must remain below free-tier limits through budgeting and filtering.

---

## 13. MVP Definition of Done

The MVP is done when all of the following are true:
1. jobs are collected and normalized
2. jobs are deduplicated and filtered
3. the user sees a ranked review queue
4. tailored PDFs are generated
5. cover letters are generated
6. the user can approve or reject jobs
7. the application status is recorded
8. user decisions improve future suggestions

---

## 14. Implementation Strategy

The MVP should be implemented in the following order:
1. data model and profile setup
2. source adapters
3. filtering and ranking
4. resume and cover letter generation
5. dashboard review flow
6. tracking and learning

This sequence keeps the project stable and minimizes wasted engineering effort.

---

## 15. Final Summary

This MVP is focused on one purpose: helping the user review and select the best-fit jobs quickly without doing all the repetitive work manually.

It is deliberately smaller than the full long-term product but still valuable enough to be useful, realistic, and buildable.

### Agreed Implementation Decisions
- Local Windows development and validation come first; private cloud deployment is a later optional phase, subject to checking current free-tier limits, persistent storage, privacy/access controls, and scheduler support.
- The initial source pair is Remotive public API plus selected public Greenhouse job boards, under each source's documented access and attribution requirements.
- Exclude South Asian employer bases and actual job locations, even for remote listings. Worldwide remote roles may accept applicants in South Asia, including Bangladesh; check that the current user is eligible. With the current Bangladesh profile, an empty queue is possible only if no role passes origin, candidate-eligibility, and other filters.

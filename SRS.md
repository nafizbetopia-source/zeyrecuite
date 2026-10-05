# Software Requirements Specification (SRS)

## 1. Document Control

- Document Name: ZEYRECUITE — Personal AI Job Agent
- Version: 2.1
- Status: Planning / Highly Detailed Requirements Specification (v2.1 features implemented)
- Date: 2026-10-01
- Owner: Personal user project (single user)
- Scope: Personal job application assistance with a hard exclusion of South Asian employer/job locations and worldwide remote-role support, including South Asian applicants; current profile location is Bangladesh

---

## 2. Introduction

### 2.1 Purpose
This document defines the software requirements for ZEYRECUITE, a personal AI-driven job search and application assistant. The system is designed to help one user discover high-fit remote jobs, evaluate company legitimacy, tailor a resume and cover letter to each job, review applications in a morning dashboard, and submit approved applications on the user's behalf while preserving strict human approval before submission.

The system is intended to be:
- $0 target with local-first operation; cloud hosting is optional and must be verified against current costs and limits
- personal-use only
- low-risk and privacy-conscious
- local-first for MVP development and validation; optional private cloud deployment later
- optimized for a single user and daily review workflow
- built with a strong human-in-the-loop model

### 2.2 Product Vision
ZEYRECUITE acts as a personal AI hiring agent that continuously searches, filters, scores, customizes, and tracks job opportunities. It reduces manual effort to a manageable morning review process while maximizing the probability of strong-fit applications.

### 2.3 Product Philosophy
The system follows a strict rule: it must spend AI tokens like money. It uses deterministic automation first, local inference second, and LLMs only for high-value tasks. It never submits an application without explicit user approval, and it surfaces every critical signal in dashboard-friendly form.

### 2.4 Business Context
The user is a Business Analyst currently in Bangladesh. The system must exclude jobs whose employer base or actual job location is in South Asia, even if labeled remote. Worldwide remote roles may accept applicants located in South Asia, including Bangladesh, provided the employer/job origin is outside South Asia and the posting permits the user's current location. The system must also support a broad “company review” taxonomy that helps the user assess whether a company is legitimate, fair, and healthy.

### 2.5 Detailed System Architecture Summary
The system is composed of several tightly coupled subsystems that operate as a single personal workflow engine rather than a monolithic job board scraper. The architecture is intentionally modular so one source adapter, one scraper, or one AI pipeline can fail without collapsing the entire application.

The system has six core layers:
1. Data ingestion and source adapters
2. Filtering and candidate evaluation
3. Matching and scoring
4. Resume and document personalization
5. Human review and application execution
6. Learning, analytics, and optimization

### 2.6 Critical Business Rules
These rules govern all product behavior and must be treated as hard constraints:
- The system must never submit an application without explicit approval.
- The system must never invent resume facts or employer details.
- Jobs based at employers or actual job locations in South Asia are always excluded, even if remote.
- Worldwide remote jobs may accept South Asian applicants, including the user in Bangladesh.
- Candidate eligibility is checked against the user's current location; explicitly incompatible roles (for example, US-only while the user is in Bangladesh) are rejected. Unknown eligibility is held for review rather than rejected merely because South Asian applicants may be allowed.
- An empty eligible queue is valid when no job passes both origin and candidate-eligibility checks; the system must not include South Asia-origin jobs to fill it.
- The system must prioritize strong-fit roles above volume.
- AI usage must be monitored by a token budget and downgrade gracefully when budget is low.
- Each application must maintain an auditable trail with states, evidence, and timestamps.
- The dashboard must be optimized for a morning review workflow, not for deep exploration.

### 2.7 Functional Architecture
The main runtime modules are as follows:

#### 2.7.1 Job Ingestion Layer
Responsible for collecting jobs from job boards, corporate career sites, RSS feeds, and manual imports. Each source is implemented as a pluggable adapter that emits a common normalized job model.

#### 2.7.2 Candidate Filtering Layer
Responsible for rejecting jobs that violate hard constraints such as excluded countries, wrong role, salary mismatch, legal restrictions, or untrusted company signals.

#### 2.7.3 Matching and Ranking Layer
Scores jobs using a weighted combination of deterministic rules, semantic similarity, and LLM reasoning.

**v2.1 (implemented, Tier 0):** the deterministic engine produces an explainable **0-100 confidence** as a weighted blend of six factors — role fit (38%), eligibility (20%), skill coverage (17%), company quality (13%), freshness (6%), and data completeness (6%). Each factor is stored with a plain-language detail string, and a separate **eligibility %** (location policy + work-mode preference + salary floor) is computed. The engine is deterministic and reproducible. A **re-score** operation recomputes the full assessment for all jobs using the current profile.

#### 2.7.4 Profile and Skills Layer
Maintains the canonical profile, resume, skill taxonomy, and user preferences. This layer feeds the matching and tailoring engines.

#### 2.7.5 Personalization Layer
Creates job-specific resumes, cover letters, and answer drafts grounded in the user profile and original evidence.

#### 2.7.6 Submission and Follow-Up Layer
Manages application execution, confirmation, status updates, and follow-up tasks after approval.

**v2.1 (implemented):** on approval the system runs a submission pipeline that ensures a tailored resume PDF and cover letter exist, then records a verifiable submission (status, method, apply URL, timestamp, attempt count). Jobs with a direct apply link are marked **submitted**; jobs without one are marked **ready** with the exact next step. The MVP never auto-fills third-party ATS forms. Application states: `draft → ready → submitted | failed`.

#### 2.7.7 Learning and Analytics Layer
Tracks user approvals, rejections, offers, interviews, and missed opportunities to improve the quality of recommendations over time.

**v2.1 (implemented):** an analytics service aggregates pipeline status, submissions over the last 14 days, confidence distribution, jobs by source, jobs by work mode, and top companies. The dashboard renders these as SVG infographics (donut, bar, and horizontal-bar charts).

### 2.8 Stateful Operating Model
The product is not a one-off script. It operates as a recurring background workflow with daily recurring jobs, manual actions, and persistent memory. The system must maintain a live state for:
- search runs
- job inventory
- company review cache
- skill weights
- application records
- approval queue
- user edits and overrides
- budget usage and rate limits

---

## 3. Scope

### 3.1 In Scope
- Job discovery from free public sources
- Job normalization and deduplication
- Work-mode and location filtering
- Job ranking and fit scoring
- Skill extraction and targeted tailoring
- ATS-friendly resume rendering to PDF
- Cover letter generation and answer drafting
- Approval dashboard with analytics and controls
- Profile manager with editable master profile
- Application tracking and status updates
- Learning from outcomes and user decisions
- Company legitimacy and review analysis
- Local-first runtime with optional cloud deployment after feasibility verification
- Optional future phases: outreach, mock interviews, referral tracking, and advanced intelligence

### 3.2 Out of Scope
- Paid job boards or paid account features
- Login-wall bypass or violating website ToS
- Automated scraping of LinkedIn profiles without official export
- Posting fake or invented resume facts
- Any feature requiring paid cloud services in the primary design

---

## 4. Stakeholders and Users

### 4.1 Primary User
- Single end user: a Business Analyst / Data Analyst candidate
- Wants an automated, high-confidence, human-reviewed job search loop
- Prefers worldwide remote jobs from employers/job locations outside South Asia; current location is checked against each posting and can change later
- Wants to inspect all job matches before approval
- Requires strong role precision and no irrelevant skill padding

### 4.2 Secondary Stakeholders
- Future versions may include career coach or recruiter-like operations
- Potential future admin user for configuration and maintenance

### 4.3 User Goals
- Save time doing repetitive job search work
- Find only strong-matching jobs
- Tailor application materials immediately per job
- Read clear job fit rationales
- Approve only the jobs they truly want
- Maintain a strong profile and increase application success
- Reduce low-quality or deceptive job opportunities

---

## 5. User Needs and High-Level Requirements

### 5.1 Core Functional Needs
The system shall:
1. Discover new jobs across free job sources and company career pages.
2. Normalize and deduplicate jobs from multiple sources.
3. Filter jobs based on role, location, salary fairness, stage, and strict exclusion rules.
4. Match jobs to the user profile using deterministic scoring and local embeddings.
5. Use an LLM only for high-value tasks after the job clears the filter.
6. Tailor the master resume into a job-specific PDF.
7. Generate a concise cover letter and prefilled answers.
8. Stage only highly qualified jobs into the morning review queue.
9. Allow the user to review, edit, approve, reject, or request changes.
10. Submit approved applications through ATS APIs, browser automation, or email when appropriate.
11. Confirm and log each application.
12. Track outcomes and continuously improve recommendations.

### 5.2 Strategic Quality Requirements
The system should feel like a real “job agent,” not just a scraper. It should be:
- High-confidence rather than broad/low-quality
- Transparent about why it selected a job
- Strict on data truthfulness and user approval
- Calm under rate limits and failures
- Observable via dashboard analytics and logs

---

## 6. Functional Requirements

### 6.1 Job Collection

#### FR-01: Source Adapter Framework
The system shall support a pluggable adapter architecture for job sources. Each source adapter shall normalize job data into a common internal representation.

#### FR-02: Supported Sources
The MVP shall support these two sources first:
- Remotive public JSON API (`GET https://remotive.com/api/remote-jobs`): unauthenticated; honor the 24-hour publication delay, poll no more than four times per day or twice per minute, display Remotive attribution, and link each listing to its Remotive URL.
- Selected employers' Greenhouse public Job Board API (`GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true`): unauthenticated GET endpoints; board tokens come from a curated allowlist. Application POST endpoints are outside MVP scope.

Lever, Ashby, Workable, SmartRecruiters, RSS, Adzuna, The Muse, and other adapters are later extensions; verify each provider's current access terms before enabling. References: [Remotive API documentation and terms](https://github.com/remotive-com/remote-jobs-api), [Greenhouse Job Board API documentation](https://docs.greenhouse.io/job-board.html).

#### FR-03: Scheduled and On-Demand Collection
The system shall allow collection jobs to run:
- On schedule (e.g., overnight tasks)
- On-demand via user-triggered “scan now” action

#### FR-04: Data Normalization
Each collected job shall be normalized to include:
- title
- company
- location
- work mode
- location eligibility
- salary info
- description
- skill tags
- source URL
- posted date
- application URL
- application method

### 6.2 Filtering

#### FR-05: Work-Mode Filter
The system shall support filtering for remote / onsite / hybrid roles.

#### FR-06: Location Filter
The system shall use the current user location stored in the profile. The default behavior shall be:
- reject jobs based at an employer or actual job location in an excluded South Asian country, including remote-labeled jobs
- allow worldwide/anywhere remote roles that accept South Asian applicants when employer/job origin is outside South Asia
- reject remote roles whose explicit applicant-location restrictions exclude the user's current location
- hold unclear candidate eligibility for review; do not reject solely because South Asian applicants are permitted
- keep local roles only when both the job country and user's current country are outside the excluded list
- show an empty eligible queue only when no job satisfies origin, current-user eligibility, and other matching conditions; a South Asian residence does not block worldwide remote roles by itself
- normalize country names and aliases to ISO 3166-1 alpha-2 codes and apply the fixed deny set `BD, IN, PK, LK, NP, BT, MV, AF`
- enforce the location gate deterministically before database persistence; scoring, embeddings, and LLM output must never override it

#### FR-07: Hard Deal-Breaker Filter
The system shall support detection of deal-breakers such as:
- travel requirements
- on-call requirements
- agency-only postings
- US-only remote restrictions when not applicable
- location mismatches
- time-zone incompatibility

#### FR-08: South Asian Exclusion
The system shall strictly exclude jobs whose employer base or actual job/listing location is in the following countries, regardless of remote label. Applicant eligibility in these countries is not itself an exclusion:
- Bangladesh
- India
- Pakistan
- Sri Lanka
- Nepal
- Bhutan
- Maldives
- Afghanistan

### 6.3 Matching and Ranking

#### FR-09: Tier 0 Scoring
The system shall compute deterministic keyword and rule-based score using:
- skill overlap
- title match
- salary fit
- company preference
- role preference
- work-mode compatibility

#### FR-10: Tier 1 Semantic Matching
The system shall use local embeddings to compute:
- semantic skill alignment
- semantic deduplication
- clustering of similar jobs
- semantic resume-to-job relevance

#### FR-11: Tier 2 LLM Scoring
The system shall use LLMs only for the highest-value jobs and only for selected tasks, including:
- fit judgment
- risk notes
- missing skills analysis
- red-flag detection
- edge-case eligibility decisions

#### FR-12: Final Ranking
The system shall generate a final score and ranking order using a weighted model from deterministic, semantic, and LLM contributions.

### 6.4 100% Confidence Gate

#### FR-13: Minimum Qualification Gate
A job shall only appear in the Morning Review Queue if all of the following conditions pass:
- fit score >= 85
- location eligibility confirmed
- company legitimacy accepted
- no major red flags
- skill coverage >= 80% of JD requirements

#### FR-14: Secondary Queue
Jobs that miss the gate narrowly shall be placed into a second-look queue for manual promotion.

#### FR-15: Calibration
The system shall track the real-world outcome of each approved/rejected job and adjust thresholds over time to preserve trust in the confidence gate.

### 6.5 Profile and Skills Management

#### FR-16: Master Profile
The system shall maintain a master profile containing:
- identity and contact information
- summary
- work experience
- projects and links
- education
- certifications
- achievements
- skills
- standard answers
- role preferences and search settings

#### FR-17: Master Resume
The system shall maintain a single master resume as the source of truth. It shall be updatable by the user and re-scanned whenever changed.

#### FR-18: Skills Manager
The system shall provide a skills management interface to:
- add skills
- remove skills
- reorder skills
- categorize them
- mark must-have / nice-to-have
- accept or reject suggestions from the AI

#### FR-19: Skill Pool Rules
The system shall use skill pool data to produce a job-specific skill subset. The tailored resume must include only the skills relevant to the job and no extra padding.

### 6.6 Tailoring Engine

#### FR-20: Master Resume Tailoring
The system shall transform the master resume into a job-specific version based on the JD and user skill set.

#### FR-21: Deterministic Tailoring
The system shall reorder sections and align wording based on job requirements and user profile data.

#### FR-22: Truthfulness Guardrail
The system shall never invent job facts, employers, years of experience, certifications, or technical skills.

#### FR-23: PDF Rendering
The system shall render the final tailored resume to an ATS-friendly PDF document and store a versioned copy.

#### FR-24: Job-Specific Skill Injection
If a company is in airline operations, the system shall surface relevant domain skills (e.g., yield management, RASK/CASK, fare intelligence, overbooking, demand forecasting) if the user possesses them. For non-technical BA roles, the system shall not insert technical requirements that are irrelevant.

### 6.7 Cover Letter and Answers

#### FR-25: Letter Generation
The system shall generate cover letters tailored to the company and role.

#### FR-26: Answer Generation
The system shall generate pre-filled questionnaire answers based on standard profile answers and job data.

#### FR-27: Editability
The user shall be able to edit the generated cover letter, answers, and resume before approval.

### 6.8 Dashboard and Morning Review

#### FR-28: Review Queue
The dashboard shall show at minimum:
- company, role, salary, source link, posting age
- fit score and reasoning
- tailored resume PDF preview
- cover letter preview
- answers preview
- red flags and urgency
- company review summary

#### FR-29: Controls
The dashboard shall allow:
- Approve
- Edit
- Reject
- View pipeline
- View analytics
- Manage profile
- Set controls and thresholds

#### FR-30: Needs-You Panel
The dashboard shall display failed submissions, CAPTCHAs, broken selectors, and other manual intervention requests.

### 6.9 Application Execution

#### FR-31: Application Submission Trigger
Applications shall submit only after the user approves the job.

#### FR-32: ATS / Web / Email Modes
The system shall support the following execution modes:
- ATS API
- Playwright browser automation
- Email-based application
- Manual queue fallback

#### FR-33: Confirmation Capture
The system shall capture:
- confirmation URL
- screenshot
- timestamp
- status

#### FR-34: Safety Guards
The system shall enforce:
- daily cap
- no duplicate submissions
- human-like delay patterns
- audit log of actions
- dry-run capability

### 6.10 Tracking, Learning, and Optimization

#### FR-35: Outcome Tracking
The system shall track application outcomes for each job, including:
- no response
- rejected
- interviewed
- offered

#### FR-36: Per-Skill Learning
The system shall track which skills correlate with interview and offer success, then adjust their weighting.

#### FR-37: Source Learning
The system shall track which sources are most productive and adjust ranking or scheduling accordingly.

#### FR-38: Style Memory
The system shall learn what resume and letter styles the user edits or prefers.

### 6.11 Company Checker

#### FR-39: Company Legitimacy Scoring
The system shall evaluate each company for legitimacy using free/public signals and assign a score.

#### FR-40: Review Summary
The system shall aggregate company review summaries about:
- salary fairness
- work environment
- management quality
- work-life balance
- remote culture

#### FR-41: Company Cache
Companies shall be checked once and cached, with stale checks refreshed on schedule.

### 6.12 Advanced Features

#### FR-42: Ghost Job Detection
The system shall detect jobs that are stale, reposted, or dead before the user applies.

#### FR-43: Interview Coach
The system shall provide mock interview support and generate likely interview questions.

#### FR-44: Email Inbox Monitor
The system shall parse incoming email to detect application replies and update status automatically.

#### FR-45: Referral Finder and Outreach
The system shall draft and track referral requests and hiring-manager outreach.

#### FR-46: ATS Simulator
The system shall simulate ATS parsing to identify problems in resume formatting and keyword density.

#### FR-47: Chat with Agent
The system shall support a simple conversational interface over the user's job activity and profile history.

#### FR-48: Backup and Portability
The system shall support backup and restore of SQLite data, profile, resumes, and PDFs.

### 6.13 Cloud Hosting

#### FR-49: Cloud Deployment
After local MVP validation, the system may support private free cloud hosting (including Hugging Face Spaces) only if current quotas, privacy/access controls, persistent storage, sleep/restart behavior, and scheduling support are verified. Cloud hosting is optional and local operation remains supported.

#### FR-50: No PC Dependency
For a future cloud deployment, the system should allow the user's PC to act primarily as a browser endpoint. This is not an MVP prerequisite; the MVP is developed and validated locally.

---

## 7. Non-Functional Requirements

### 7.1 Performance
- Full overnight cycle target: under 45 minutes for around 200 new jobs on local runtime, and under 90 minutes on HF Space under typical load.
- Dashboard load target: under 1 second for the queue page.
- Job processing time: under 2 seconds per job for Tier 0/1 in typical conditions.
- PDF render target: under 2 seconds per job.

### 7.2 Reliability
- A broken source adapter must not bring down the whole system.
- Failures shall be isolated and surfaced.
- Graceful degradation shall occur when the LLM budget is exhausted.

### 7.3 Security and Privacy
- User data shall remain local or in a controlled private environment.
- No scraping of LinkedIn profiles without official export or user action.
- Secrets such as Groq API keys shall be stored in protected environment variables or secrets store.
- The system shall not publish personal data publicly.

### 7.4 Maintainability
- Source adapters shall be modular and independent.
- Model code shall be separated from API code and dashboard code.
- Database schema shall support migration-friendly evolution.

### 7.5 Scalability
- The architecture shall support an increase in collected jobs without rewriting core logic.
- The core queue and scoring systems shall remain fairly linear and easy to extend.

### 7.6 Usability
- Dashboard shall be fast, readable, and easy to scan in under ~5 minutes per morning.
- Review actions shall be one-click and keyboard-friendly.
- Analytics and logs shall be plain-language and easy to interpret.

---

## 8. User Stories

### 8.1 Daily Workflow Stories
- As a user, I want the system to find the top remote roles overnight so I can review them in the morning.
- As a user, I want to see the reason a job is a good fit so I can trust the system.
- As a user, I want to review a tailored PDF before I approve.
- As a user, I want to reject jobs quickly without complicated steps.
- As a user, I want the dashboard to show what needs my attention.

### 8.2 Profile Management Stories
- As a user, I want to edit my full profile from one place.
- As a user, I want new skills to automatically be available in the matching engine.
- As a user, I want my master resume to stay canonical and always be re-scanned.
- As a user, I want future location changes to instantly update search scope.

### 8.3 Company and Fit Stories
- As a user, I want to know if a company is legit and healthy before I apply.
- As a user, I want domain-specific skills to appear only when relevant.
- As a user, I want to know if a company is paying fairly for the role.

### 8.4 Learning Stories
- As a user, I want the system to learn from my rejection and approval decisions.
- As a user, I want the system to track which skills correlate with interviews.
- As a user, I want the system to tell me what I should improve next.

---

## 9. Functional Workflow

### 9.1 Daily Loop
1. Jobs are collected from configured sources.
2. Data is normalized and deduplicated.
3. Rules and local classifiers filter for role, work mode, location, and search exclusions.
4. Jobs are scored and ranked.
5. Top-N jobs are sent to Groq for deep reasoning and cover letter generation.
6. The system tailors the master resume and renders a PDF.
7. Jobs pass the 100% confidence gate before reaching the morning queue.
8. The user reviews the queue and decides approve / edit / reject.
9. Approved jobs are submitted via the selected mechanism.
10. Submission results are logged and outcomes tracked.
11. The learning engine updates skill weights, source weights, and future scoring.

### 9.2 Morning Review
The user checks the dashboard and sees:
- top 10 confident jobs
- their fit reasoning
- company check
- tailored resume PDF
- cover letter and answers
- approval/reject actions
- needs-you panel

### 9.3 Multi-Country Movement Workflow
If the user changes current location from Bangladesh to the US, UK, NZ, or AU:
- the profile’s current location changes
- the scope may include local jobs in that country
- worldwide remote jobs may accept applicants in South Asia; candidate eligibility is checked against the user's new current country
- local jobs in South Asia remain excluded
- the strict South-Asia exclusion remains active

### 9.4 Application Lifecycle State Model
Every application must have a formal lifecycle state. Required states include:
- discovered
- normalized
- filtered_out
- scored
- queued_for_review
- reviewed
- approved
- editing
- rejected
- submitted
- awaiting_response
- interview_stage
- offer
- closed
- archived

Transitions must be logged and must be reversible only when the business rules permit it. For example, approved jobs can go back to editing, but a submitted job cannot move back to queued_for_review without explicit user action and audit logging.

### 9.5 Operational Workflow for a Single Job
1. A job is collected by an adapter.
2. The system validates the required fields and computes a dedupe hash.
3. The system compares against prior jobs and existing applications.
4. Geographic and role filters are applied.
5. Score models run in order: deterministic rules, semantic similarity, LLM reasoning.
6. The system checks company legitimacy and red-flag score.
7. If the job passes the quality threshold, it enters the review queue.
8. The system generates a tailored resume, cover letter, and answer drafts.
9. The user reviews the outputs.
10. The system awaits explicit approval.
11. The application is submitted through the selected method.
12. The status is updated and tracked until closure.

---

## 10. Data Requirements

### 10.1 Core Data Entities
- User Profile
- Master Resume
- Skills
- Job
- Company
- Application
- Follow-up
- Learning record
- LLM cache
- Event log
- Budget records
- Outreach records
- Interview records
- Watchlist entries
- Salary benchmarks

### 10.1.1 Detailed Entity Definitions

#### User Profile
Represents the canonical user state. Must include:
- personal details and contact data
- current city and country
- work mode preferences
- remote policy
- job role preference
- salary target range
- notice period
- timezone flexibility
- deal-breakers
- self-description and career summary
- education and certifications
- skills and level metadata
- preferred companies
- application thresholds

#### Master Resume
Contains the single source-of-truth resume the system uses as the base for job tailoring. It must be versioned and re-generated whenever the user edits it. Every tailored document should trace back to a specific resume version.

#### Skills
Contains every user skill and related metadata, including:
- name
- category
- proficiency level
- source (manual / imported / inferred)
- relevance to target roles
- recent usage frequency
- validation status
- optional domain tags

#### Job
Represents a normalized job opportunity from any source. Minimum required fields include:
- source_name
- original_url
- normalized_title
- company_id
- location_text
- country
- remote_status
- work_mode
- salary_min / salary_max
- posted_at
- expires_at
- job_description
- parsed_skills
- rank_score
- fit_score
- status
- dedupe_hash
- retention_flags

#### Company
Represents the employer or hiring organization. Must include:
- name
- website
- domain
- company_size
- legitimacy_score
- review_summary
- red_flag_tags
- last_checked_at
- source reliability

#### Application
Represents a candidate action or potential submission. Fields include:
- job_id
- tailored_resume_version_id
- cover_letter_version_id
- status
- submitted_at
- approval_state
- approval_reason
- manual_notes
- outcome
- final_result

#### Follow-Up
Tracks repeated outreach, check-ins, interview reminders, and other post-application actions.

#### Learning Record
Stores weights and signals derived from user behavior, including:
- user approval / rejection reason
- observed interview conversion
- source quality score
- skill-level success rate
- company quality signals

#### Event Log
Stores every significant action in chronological order for debugging, auditability, and explainability.

#### Budget Record
Stores LLM API usage, token budgets, estimated spend, and degradation thresholds.

#### Outreach Record
Tracks referral requests, outreach emails, and implementation status for future advanced features.

### 10.2 Data Quality Rules
- Profile fields must be validated before acceptance.
- Resume must not contain invented facts.
- Job duplicates must be merged by fingerprint and/or semantic similarity.
- Company checks must be cached to avoid repeated analysis.
- Every application must have a status lifecycle value.

### 10.3 Data Retention
- Job and application history should remain available for learning and analytics.
- Weekly/monthly reports should use aggregated data.
- Backups should be easy to create and restore.

---

## 11. User Interface Requirements

### 11.1 Dashboard Views
- Review Queue
- Pipeline View
- Analytics View
- Profile Manager
- Controls
- Budget View
- Needs-You Panel

### 11.2 UI Behaviors
- One-click approve/reject actions
- Inline editing
- PDF preview
- Search and filter
- Sort by fit score, urgency, source, salary, date
- Mobile-friendly layout
- Dark mode option

### 11.3 Accessibility Requirements
- Clear contrast
- Keyboard navigation
- Simple inferable labels
- Screen-reader-friendly structure

---

## 12. System and Deployment Requirements

### 12.1 Cloud Hosting
Deployment shall be phased:
1. Develop and validate locally on the supported Windows environment using the same codebase and start procedure intended for later deployment.
2. Evaluate private free cloud hosting (including Hugging Face Spaces) only after confirming current free-tier quotas, privacy/access controls, persistent storage behavior, sleep/restart behavior, and scheduled-task support.

Cloud hosting is optional and must not be assumed to remain free or retain data unless verified. Local operation remains the initial validation environment and supported fallback.

### 12.2 Primary Runtime Components
- Python app server
- SQLite database
- Job collectors
- scoring engine
- LLM client
- PDF generator
- dashboard front-end
- scheduler

### 12.3 External Dependencies
- Groq API endpoint
- job source APIs
- public company information sources
- email inbox access (optional for later phase)

---

## 13. Risks and Mitigations

### 13.1 Technical Risks
- API changes in job sites
- Rate limiting from Groq or job sources
- Playwright selector failures
- Cloud resource limits or sleep issues
Mitigation: isolation, retries, graceful degradation, local fallback.

### 13.2 Data Quality Risks
- Resume inaccuracies
- Incomplete JD parsing
- False positives in company legitimacy detection
Mitigation: user review before approval, truthfulness guardrails, human-in-the-loop design.

### 13.3 Security and Privacy Risks
- API key leakage
- misuse of LinkedIn data
- exposure of personal data
Mitigation: secrets management, no scraping, restrictive access controls.

---

## 14. Acceptance Criteria

### 14.1 MVP Acceptance
The system shall be considered complete for MVP when:
- it finds jobs across free sources
- filters for location and role
- deduplicates and scores jobs
- renders a tailored PDF
- presents a queue in the dashboard
- allows user approval and rejection
- allows application submission after approval
- stores outcomes and logs all actions

### 14.2 Advanced Acceptance
The system shall be considered advanced when:
- 100% confidence gate is enforced
- company checks are active
- outputs are tracked and optimized
- mock interview and email-monitoring enhancements run
- the system learns from outcomes and continues improving

---

## 15. Future Enhancements
- Multi-profile mode
- Voice commands
- AI career planner
- deeper recruiter outreach workflows
- portfolio automation
- multilingual applications
- auto-generated personal website

---

## 16. Glossary
- ATS: Applicant Tracking System
- JD: Job Description
- Groq: AI inference provider used for budgeted LLM tasks
- Tier 0: deterministic rules and filtering layer
- Tier 1: local embedding/classification layer
- Tier 2: LLM-powered reasoning layer
- Confidence Gate: strict threshold for queue inclusion
- Master Resume: the canonical source-of-truth resume
- Needs-You Panel: dashboard area for manual decisions and fixes

---

## 17. Detailed Requirement Traceability Matrix

| Requirement ID | Requirement Category | Requirement Summary | Primary Component | Validation Method |
|---|---|---|---|---|
| FR-01 | Functional | Source adapter architecture | Collectors | Unit test + integration test |
| FR-05 | Functional | Work-mode filter | Filtering engine | Scenario test |
| FR-06 | Functional | Location filter | Location engine | Scenario test |
| FR-08 | Functional | South Asian exclusion | Filtering engine | Rule test |
| FR-09 | Functional | Tier 0 scoring | Deterministic engine | Unit test |
| FR-10 | Functional | Semantic matching | Local embeddings | Unit test |
| FR-11 | Functional | Tier 2 deep judgment | Groq client | Integration test |
| FR-13 | Functional | Confidence gate | Pipeline | Acceptance test |
| FR-16 | Functional | Master profile | Profile manager | UI validation |
| FR-17 | Functional | Master resume | Resume model | Data validation |
| FR-18 | Functional | Skill manager | Skills engine | UI validation |
| FR-20 | Functional | Resume tailoring | Tailoring engine | PDF output validation |
| FR-25 | Functional | Cover letter generation | LLM generation | Regression test |
| FR-28 | Functional | Review queue | Dashboard | UI acceptance test |
| FR-31 | Functional | Approval-based submission | Application engine | End-to-end test |
| FR-35 | Functional | Outcome tracking | Learning pipeline | Data check |
| FR-39 | Functional | Company legitimacy | Company checker | Integration test |
| NFR-01 | Non-functional | Performance | Runtime pipeline | Benchmark test |
| NFR-03 | Non-functional | Security/privacy | Runtime config | Security review |
| NFR-04 | Non-functional | Maintainability | Architecture | Code review |

### 17.1 Acceptance Scenarios

#### Scenario A: Daily job collection and filtering
Given a set of jobs from several sources, when the daily collection pipeline runs, then all jobs should be normalized, deduplicated, filtered by location and work-mode rules, and stored in the job table.

#### Scenario B: Top queue generation
Given jobs that pass scoring thresholds, when the pipeline ranks them, then only the highest-confidence jobs should be staged into the review queue and jobs below threshold should be kept in the second-look queue.

#### Scenario C: Resume generation
Given a valid master profile and a job description, when the tailoring engine runs, then a job-specific resume PDF is generated from the actual user profile and stored as a versioned artifact.

#### Scenario D: User review and approval
Given a staged job, when the user approves it, then the application engine creates a submission payload and records the approval event.

#### Scenario E: Failed application handling
Given a submission fails because of CAPTCHA or a broken page, when the error is detected, then the job is moved to the Needs-You panel with actionable guidance.

#### Scenario F: Learning update
Given the user rejects or approves jobs, when outcomes are recorded, then the learning layer updates skill weight and source quality metrics for future scoring.

---

## 18. Detailed Risk Matrix

| Risk Type | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Source site changes | High | High | Isolated adapters + health checks |
| Groq budget exhaustion | Medium | Medium | Budget manager + graceful degradation |
| Duplicate jobs across boards | High | Medium | Exact + semantic dedup |
| Company legitimacy false positives | Medium | High | Human review + red-flag review |
| Resume truthfulness violation | Low | Very High | Strict guardrail + pre-approval preview |
| CAPTCHA / anti-bot blocks | Medium | High | Needs-You panel + manual fallback |
| Cloud resource sleep issues | Medium | Medium | Local fallback + persistent disk |

---

## 19. Operational Standards

### 19.1 Logging and Observability
The system shall log all major steps with timestamps and status. Logs must include:
- scan start/end
- adapter health
- dedup summary
- filter summary
- score breakdown
- LLM calls and budget usage
- application submission events
- user approval/rejection actions

### 19.2 Error Handling Standards
All user-facing errors should follow a consistent structure:
- code
- message
- timestamp
- affected object ID
- recommended action

### 19.3 Backup and Recovery
The product must support:
- job database export
- resume export
- uploaded profile imports
- PDF backup
- restore of application state

---

## 20. Summary
ZEYRECUITE is designed as a personal AI job agent with a strong emphasis on trust, relevance, precision, and daily review. It combines free public job sources, deterministic filtering, local AI matching, budgeted Groq reasoning, and a user-first dashboard. The system is designed to help the user find only the best jobs, tailor materials for each one, review them quickly, and apply with high confidence while keeping full human control of the final decisions.

This SRS captures the complete functional and architectural foundation for the system, including detailed workflows, product constraints, data requirements, acceptance scenarios, risk controls, and the implementation roadmap needed to realize the full project vision.

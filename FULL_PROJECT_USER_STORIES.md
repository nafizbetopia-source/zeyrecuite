# ZEYRECUITE — Comprehensive Full-Project User Stories

## 1. Purpose

This document expands the full-project user stories into a more complete product backlog for ZEYRECUITE. It covers the entire end-to-end lifecycle of the system, from initial job discovery and profile setup to matching, personalization, approval, submission, outcome tracking, learning, and future career intelligence features.

The goal is to make the product story comprehensive enough to guide engineering, design, and roadmap decisions while remaining grounded in the real use case: a single user seeking only jobs that pass strict South Asia employer/job-origin and applicant-location exclusions, with a human-in-the-loop approval flow.

---

## 2. Product Scope Overview

ZEYRECUITE is a personal AI career optimization and job-application assistant. It is designed to:
- discover relevant jobs from public sources
- filter noise and unqualified roles
- rank and explain the best-fit opportunities
- tailor resume and cover letter materials
- give the user a clear review queue
- ask for approval before applying
- log outcomes and improve itself over time
- eventually evolve into a broader career assistant

The product should feel like a personal job co-pilot rather than a generic job board or a bot that blindly applies everywhere.

---

## 3. User Personas

### 3.1 Primary User
Name: Personal user / Business Analyst candidate
Characteristics:
- single-user product
- seeks remote or flexible jobs
- wants to save time and reduce manual work
- values trust and transparency
- wants efficient morning review workflow
- has a defined profile, location, skills, and preferences
- does not want mass automation without review

### 3.2 Power User / Admin User
Characteristics:
- manages profile, settings, job preferences, and thresholds
- may edit scoring/configuration manually
- may want to inspect analytics and adjust settings
- wants visibility into AI budget and job pipeline

### 3.3 Future Growth Persona
Characteristics:
- wants advanced features like interview practice, outreach support, market intelligence, and career planning
- may be added in later phases when the product proves useful

---

## 4. Product Story Categories

1. Account and profile setup
2. Job discovery and source integration
3. Job filtering and quality control
4. Job fit and scoring
5. Candidate profile and skill management
6. Resume tailoring and cover-letter generation
7. Dashboard and morning workflow
8. Application execution and tracking
9. Trust, safety, and company checks
10. Learning and optimization
11. Advanced career assistant features
12. Maintenance, analytics, and long-term growth

---

## 5. Comprehensive User Stories

## Epic 1: Account, Preferences, and Profile Setup

### US-01: Create profile from master resume
As a user, I want the system to create a working profile from my resume and profile details so I do not need to enter everything manually.

Acceptance Criteria:
- profile is created from imported resume data or manual input
- name, skills, experience, certifications, and education are captured
- imported data can be edited after import
- the user can confirm or correct extracted information

### US-02: Edit profile at any time
As a user, I want to update my profile, skills, and preferences at any time so the system reflects my current situation.

Acceptance Criteria:
- the user can change location, experience, skills, summary, and work preferences
- updates are saved with versioning
- old versions remain accessible

### US-03: Manage search configuration
As a user, I want to control my job search settings so the system filters only the roles and work patterns I actually want.

Acceptance Criteria:
- user can define remote, hybrid, on-site, and role preferences
- deal-breakers are editable
- current location and excluded countries are configurable
- daily application cap is configurable

### US-04: Handle location changes cleanly
As a user, I want my current country or location to change the search scope automatically so my job search adapts when I move.

Acceptance Criteria:
- changing location updates filtering rules
- jobs based in excluded countries are blocked even when labeled remote and after a location change
- worldwide/anywhere remote roles may accept South Asian applicants when employer/job origin is outside South Asia
- explicit candidate-location restrictions that exclude the user's current country are enforced
- unclear candidate eligibility is held for review; it is not rejected merely because South Asian applicants may be permitted
- a Bangladesh-based user may receive eligible worldwide remote roles when employer/job origin is outside South Asia and the posting permits Bangladesh
- if no listing passes origin, candidate-eligibility, and other filters, an empty queue is shown without relaxing the origin rule

### US-05: Complete profile status
As a user, I want to know how complete my profile is so I can improve it before running the system aggressively.

Acceptance Criteria:
- profile completeness score or checklist is visible
- missing required fields are highlighted
- user can fill in missing sections from the dashboard

---

## Epic 2: Job Discovery and Source Integration

### US-06: Collect jobs automatically
As a user, I want the system to collect jobs continuously so I do not need to manually search every source.

Acceptance Criteria:
- scheduled collection runs automatically
- user can trigger a manual refresh
- jobs are stored with timestamps and source metadata

### US-07: Support multiple sources
As a user, I want jobs from several reliable sources so I do not miss good opportunities across different platforms.

Acceptance Criteria:
- multiple public sources are supported
- each source is normalized into a common job model
- source health is visible in logs or dashboard

### US-08: Handle source failures gracefully
As a user, I want one broken source or failed API not to crash the whole job search process.

Acceptance Criteria:
- source errors are isolated
- failed adapters are retried or marked unhealthy
- other sources continue running

### US-09: Import jobs from direct company career pages
As a user, I want the system to collect company-hosted jobs when they are not in a standard aggregator so I do not miss direct hiring opportunities.

Acceptance Criteria:
- company career pages can be scanned
- extracted jobs are normalized into the same model
- direct jobs are scored the same way as other sources

### US-10: Support manual or semi-manual sources
As a user, I want manual or blocked sources to be queued for review instead of being silently ignored.

Acceptance Criteria:
- some sources may require user intervention or manual actions
- blocked jobs are clearly marked
- the user sees why the system could not auto-submit or auto-collect

---

## Epic 3: Filtering, Deduplication, and Data Quality

### US-11: Deduplicate jobs across sources
As a user, I want duplicate job listings removed so the review queue is not cluttered and noisy.

Acceptance Criteria:
- exact and near-duplicate jobs are merged
- one canonical job record remains
- best URL or best metadata is retained

### US-12: Filter out irrelevant jobs
As a user, I want obviously weak or wrong jobs removed early so I do not spend time on dead ends.

Acceptance Criteria:
- jobs with wrong role, wrong location, or wrong work mode are filtered out
- reasons for filtering are visible to the user or in system logs
- filtered jobs can be reviewed in debug mode if needed

### US-13: Exclude South Asia job origins
As a user, I want employers and actual job locations in South Asia excluded while still allowing worldwide remote jobs from outside South Asia.

Acceptance Criteria:
- employers based in excluded countries and jobs actually located there never enter stored eligible jobs, scoring, generation, or dashboard results
- remote jobs from outside South Asia remain eligible even if applicants from South Asia are permitted
- explicit candidate-location restrictions are checked against the user's current location
- unknown employer/job origin is held out pending verification
- unclear candidate eligibility is held for review rather than rejected solely because South Asian applicants are allowed
- region rules run before persistence and ranking
- an empty eligible queue is valid when no job passes origin, candidate eligibility, and role requirements
- filter reason is available in sanitized diagnostics without exposing blocked listings in the main product

### US-14: Handle role ambiguity
As a user, I want the system to distinguish true Business Analyst work from similar-looking but not equivalent roles so I do not waste time on bad matches.

Acceptance Criteria:
- similar job titles are classified by role fit
- jobs with weak BA relevance are ranked lower
- role mismatch is explained in output

### US-15: Reject ghost or stale jobs
As a user, I want stale or reposted jobs filtered out so I avoid wasting time on outdated listings.

Acceptance Criteria:
- stale jobs are flagged automatically
- repeated postings are recognized and de-prioritized
- ghost-job reason is visible in the job record

---

## Epic 4: Ranking, Scoring, and Confidence Gates

### US-16: Score jobs by relevance
As a user, I want each job to get a fit score so I can quickly understand what is most promising.

Acceptance Criteria:
- a score is displayed on the job card
- the score reflects profile fit and job requirements
- the user can see which factors raised or lowered the score

### US-17: Differentiate strong fit from weak fit
As a user, I want jobs above a confidence threshold to stand out so I only review the best opportunities.

Acceptance Criteria:
- jobs above threshold are highlighted
- jobs below threshold are demoted or delayed
- threshold settings are configurable

### US-18: Use semantic matching beyond raw keywords
As a user, I want the system to understand similar language and skills so it does not miss good jobs because of wording differences.

Acceptance Criteria:
- local embedding or semantic scoring is included
- similar concepts are matched even with different phrases
- semantic match is part of final ranking logic

### US-19: Handle salary fairness evaluation
As a user, I want low-paying jobs to be flagged or prioritized lower so I do not waste effort applying to unfair offers.

Acceptance Criteria:
- salary is evaluated relative to job role and market range
- fair vs weak offer indicators appear on the card
- below-market jobs are not silently treated as strong matches

### US-20: Manage urgency without panic
As a user, I want urgency signals to show the best timing for applying without overwhelming me with low-value jobs.

Acceptance Criteria:
- urgency score is visible
- job maturity and freshness affect ranking
- strong but not urgent jobs remain visible for later review

---

## Epic 5: Profile, Skills, and Resume Intelligence

### US-21: Maintain a master profile
As a user, I want a complete master profile so the system has a trusted source of truth for matching and tailoring.

Acceptance Criteria:
- profile includes summary, skills, jobs, education, certifications, languages, preferences, answers
- profile is version-controlled
- profile changes are easy to review and edit

### US-22: Manage skill pool with precision
As a user, I want to manage my skills manually and through AI suggestions so the system reflects my actual capabilities accurately.

Acceptance Criteria:
- skills can be added, edited, removed, and categorized
- suggested skills can be accepted or rejected
- must-have and nice-to-have status is supported

### US-23: Keep resume truthful
As a user, I want the system to tailor the resume only from verified facts so I never risk submitting invented experience.

Acceptance Criteria:
- all resume changes are derived from known profile data
- the system blocks suggested content that cannot be supported
- the user can review all generated text before approval

### US-24: Build job-specific resume versions
As a user, I want a unique resume for each job so the resume highlights what matters most for that position.

Acceptance Criteria:
- each job has a separate resume version
- the tailored version reflects key job requirements
- non-relevant skills and sections are reduced or removed

### US-25: Maintain resume version history
As a user, I want to review and restore past resume versions so I can compare and recover if needed.

Acceptance Criteria:
- each resume version is stored with timestamps
- the user can inspect generations
- versions can be restored or compared

---

## Epic 6: Tailoring, Cover Letters, and Application Drafts

### US-26: Tailor resume to the exact job
As a user, I want the system to tailor my resume to each job description so it speaks directly to the role I am applying for.

Acceptance Criteria:
- resume summary and bullets are adapted to the role
- relevant skills and experience are prioritized
- irrelevant content is reduced

### US-27: Generate ATS-friendly PDF outputs
As a user, I want my tailored resume in PDF format so I can review it in the same format that would be submitted.

Acceptance Criteria:
- output is PDF
- layout remains readable and ATS-friendly
- document is stored and downloadable

### US-28: Generate cover letters
As a user, I want the system to write a tailored cover letter for each job so I do not have to start from scratch.

Acceptance Criteria:
- each job has a letter draft
- letter aligns with job needs and user profile
- letter is editable before approval

### US-29: Draft prefilled application answers
As a user, I want the system to prepare application answers so I can review them quickly and avoid manual writing.

Acceptance Criteria:
- questionnaire answers are generated from profile data
- answers are editable and versioned
- candidate can reject or revise before submission

### US-30: Preserve truth in cover letters and answers
As a user, I want generated writing to stay honest and grounded in my actual experience and resume.

Acceptance Criteria:
- AI output is validated against known facts
- unsupported claims are rejected or flagged
- the user sees the source material used for generation

---

## Epic 7: Dashboard, Review Queue, and User Decision Flow

### US-31: Review top jobs in one place
As a user, I want a single dashboard that surfaces the best-fit jobs so I do not have to juggle multiple tabs and tools.

Acceptance Criteria:
- review queue contains top ranked jobs only
- each job has clear metadata and action controls
- the user can sort and filter by fit, salary, or urgency

### US-32: Approve or reject with one click
As a user, I want to approve, edit, or reject jobs quickly so the morning review is fast and low-friction.

Acceptance Criteria:
- approve/edit/reject actions exist on each card
- a status change updates the workflow immediately
- the user remains in one page without extra navigation

### US-33: See why a job matched
As a user, I want a plain-English explanation of the match so I can trust the recommendation before approving.

Acceptance Criteria:
- each job includes a fit reason summary
- matched skills and missing skills are visible
- any risk or blocker is explained clearly

### US-34: Show the exact materials to be submitted
As a user, I want to inspect the resume PDF, cover letter, and answers before approval so I know exactly what will be sent.

Acceptance Criteria:
- user can view all generated materials in dashboard
- each material is previewable
- user can edit before submission

### US-35: See tasks that need human intervention
As a user, I want a separate panel for blocked tasks or manual actions so nothing gets lost.

Acceptance Criteria:
- needs-you panel exists
- blocked or failed items are clearly visible
- required action is described clearly

---

## Epic 8: Application Execution and Tracking

### US-36: Submit only after approval
As a user, I want applications to submit only after I explicitly approve them so I control the process.

Acceptance Criteria:
- no auto-submission without user approval
- the approval action is recorded
- the submission attempt is logged

### US-37: Support multiple application methods
As a user, I want supported application methods to vary by site so the system can handle different job portals without manual rework.

Acceptance Criteria:
- ATS routes are used where possible
- form-based automation is available for supported sites
- email-based applications are supported when applicable

### US-38: Capture submission proof
As a user, I want confirmation data stored so I know that I actually submitted the right application.

Acceptance Criteria:
- confirmation URL or response is saved
- screenshot or record is captured if possible
- final state is updated in the pipeline

### US-39: Failed apps do not disappear
As a user, I want failed submissions to remain visible so I can see what broke and resolve it.

Acceptance Criteria:
- failed or blocked submissions remain in the pipeline
- failures include reason codes and error context
- retry or manual intervention is possible

### US-40: Track lifecycle states
As a user, I want each application to have a clear status so I know what stage it is in.

Acceptance Criteria:
- each application has a lifecycle state
- states are explicit and visible
- historical transition logs are available

---

## Epic 9: Trust, Company Checks, and Safety

### US-41: Check company legitimacy
As a user, I want risky or suspicious companies flagged before I apply so I do not waste time or expose myself to fraud.

Acceptance Criteria:
- company legitimacy score is visible
- red flags are displayed clearly
- suspicious companies are deprioritized

### US-42: Understand company culture and fairness
As a user, I want a readable company review summary so I can decide whether a company is worth pursuing.

Acceptance Criteria:
- summary includes culture, environment, salary fairness, and management style
- summary is easy to read in one glance
- stale summaries are refreshed on a schedule

### US-43: Balance trust with opportunity
As a user, I want the system to reduce risk without hiding promising jobs so I do not miss good companies with limited public signal.

Acceptance Criteria:
- company risk affects rank but does not fully block all jobs automatically
- important job opportunities can still be manually reviewed

### US-44: Avoid unsafe AI behavior
As a user, I want the system to never invent facts or misrepresent my experience so my job search remains truthful and professional.

Acceptance Criteria:
- all generated resume and letter content is traceable to the profile
- unsupported claims are blocked or alerted
- user review remains a requirement before final submission

### US-45: Protect privacy and data
As a user, I want the system to protect my personal and application data so I am comfortable using it for job search.

Acceptance Criteria:
- private data is stored securely
- API keys and credentials remain protected
- sensitive data is not exposed publicly

---

## Epic 10: Learning, Analytics, and Improvement

### US-46: Learn from outcomes
As a user, I want the system to learn from my rejections, approvals, interviews, and offers so it gets smarter over time.

Acceptance Criteria:
- each outcome is recorded
- future recommendations improve based on past outcomes
- learning is visible in analytics

### US-47: Understand which skills lead to better outcomes
As a user, I want the system to show which skills correlate with stronger job outcomes so I can improve my profile deliberately.

Acceptance Criteria:
- skill and outcome data is tracked
- analytics show which skills matter most
- future rankings can reweight those skills

### US-48: Learn from source performance
As a user, I want the system to identify which job sources produce the best outcomes so I can focus on the most productive channels.

Acceptance Criteria:
- source-level conversion metrics are tracked
- source ranking adjusts over time
- user can inspect source quality in dashboard analytics

### US-49: Remember my editing style
As a user, I want the system to remember how I edit my resume and cover letters so future drafts align with my preferences.

Acceptance Criteria:
- user edits are captured as patterns
- preferred phrasing or structure is reused
- user can override style preferences whenever needed

### US-50: See my job search statistics
As a user, I want analytics about my pipeline so I can understand my search efficiency and performance over time.

Acceptance Criteria:
- analytics includes approvals, rejections, response rates, and success by source
- metrics are displayed clearly and simply
- data is exportable or stored for review

---

## Epic 11: Future Career Support Features

### US-51: Interview preparation and practice
As a user, I want likely interview questions and mock interviews so I can prepare for real interviews without needing a separate tool.

Acceptance Criteria:
- likely questions are generated per role
- the user can practice or review them
- interview prep is stored with the application or role

### US-52: Follow-up reminder workflow
As a user, I want reminders for follow-ups and check-ins so I do not miss pending interview or application steps.

Acceptance Criteria:
- follow-up due dates are tracked
- reminders are visible or sent in supported channels
- status is updated after follow-up action

### US-53: Referral and outreach support
As a user, I want help drafting referrals or outreach messages so I can approach promising roles more strategically.

Acceptance Criteria:
- referral candidates can be stored
- outreach drafts are generated or managed
- outreach outcomes are tracked

### US-54: ATS resume feedback
As a user, I want resume compatibility feedback so I can improve ATS formatting before submitting high-value applications.

Acceptance Criteria:
- resume quality score is computed
- weak sections or formatting issues are pointed out
- user can improve the document based on feedback

### US-55: Ask the agent questions about my job search
As a user, I want to ask the system about my applications, outcomes, and next best steps so it feels like a helpful personal assistant.

Acceptance Criteria:
- a chat or query interface is available
- it answers from past jobs and profile data
- it can summarize the pipeline or suggest next steps

### US-56: Market insight and strategy guidance
As a user, I want insights about skill gaps and career positioning so I can improve my strategy and focus on the right opportunities.

Acceptance Criteria:
- skill gap analysis is visible
- market or role trend insights are available
- recommendations are shown in a readable format

---

## Epic 12: Long-Term Growth and Platform Expansion

### US-57: Multi-profile support
As a user, I want multiple profiles or job personas so I can target different roles without losing context.

Acceptance Criteria:
- multiple profiles can be created and switched
- each profile has its own resume and preferences
- data remains isolated per profile

### US-58: Voice interaction support
As a user, I want to use quick voice commands so the dashboard remains fast and ergonomic.

Acceptance Criteria:
- voice-based commands are optional
- commands support common actions like review or approve
- voice is never used as a substitute for explicit approval

### US-59: Portfolio and public profile integration
As a user, I want my work and credentials to be visible in a portfolio or public profile so my job search improves beyond resume-only applications.

Acceptance Criteria:
- portfolio or personal site generation is possible later
- profile information can be exported or linked
- generated content stays aligned with the master profile

### US-60: Long-term career planning
As a user, I want the system to suggest smarter career moves and skill-building steps so I can improve my market value over time.

Acceptance Criteria:
- career advice is based on historical job outcomes and skill gaps
- suggestions are contextual and explainable
- the user can choose to ignore or accept them

---

## 6. Cross-Cutting Acceptance Criteria

The full product is accepted when:
- the user can manage a full profile and resume from one place
- the system can discover, filter, rank, and explain jobs
- it generates tailored materials for jobs in a trusted workflow
- the user controls final approvals before any application is submitted
- status tracking and learning are reliable
- company and trust checks reduce risky applications
- analytics and feedback loops help improve future performance
- support features can be added without redesigning the core architecture

---

## 7. Quality Attributes

### Trust
The system must feel reliable and truthful.

### Transparency
The user must understand why a job was accepted or rejected.

### Speed
The morning workflow should be quick and efficient.

### Privacy
User profile and application data must be protected.

### Modularity
The system should be built in layers so individual services can improve over time.

### Cost control
AI usage must be governed by a strict budget and degradation strategy.

---

## 8. Final Note

These stories define the product as a full AI-powered career assistant, but they also make it clear that the implementation must be phased. The first priority is the stable job-review workflow: job discovery, fit scoring, tailored resume, dashboard review, and user approval. Once that works reliably, the product can expand into interview support, outreach, market intelligence, and a broader AI career coach experience.

# ZEYRECUITE — 702 Test Cases

## 1. Purpose

This document contains a broad QA and validation suite for the ZEYRECUITE project. It covers functional, negative, edge, security, UX, performance, reliability, and regression scenarios for the full product lifecycle.

The cases are structured to support:
- MVP validation
- production readiness checks
- regression testing
- backlog refinement
- QA sign-off before release

---

## 2. Legend

- Priority: P0 = critical, P1 = high, P2 = medium, P3 = low
- Type: Functional / Negative / Edge / UI / Performance / Security / Regression / Integration
- Scope: The suite covers the end-to-end workflow from profile setup to job review, application approval, tracking, analytics, and future enhancements

---

## 3. Test Case Matrix

## 3.1 Profile and Account Setup

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| PROF-001 | P0 | Functional | User creates an account with valid email and password | Account is created and verification email or onboarding flow starts |
| PROF-002 | P0 | Functional | User signs in with correct credentials | User is authenticated and redirected to dashboard |
| PROF-003 | P1 | Negative | User signs in with wrong password | System rejects login and shows clear error |
| PROF-004 | P1 | Negative | User signs in with unregistered email | System shows invalid credentials message |
| PROF-005 | P0 | Functional | User updates personal name and phone number | Profile is updated successfully |
| PROF-006 | P1 | Functional | User updates current country and location | New location is saved and applied to search filters |
| PROF-007 | P1 | Negative | User enters invalid phone number format | System validates and rejects invalid input |
| PROF-008 | P1 | Negative | User enters invalid email format | Validation prevents saving invalid email |
| PROF-009 | P0 | Functional | User imports a master resume | Resume is parsed and profile fields are populated |
| PROF-010 | P1 | Negative | User imports a corrupted or empty PDF | System warns and prevents invalid import |
| PROF-011 | P0 | Functional | User edits summary text | Summary is saved without affecting other profile sections |
| PROF-012 | P1 | Functional | User adds multiple work experiences | All experiences are stored and displayed correctly |
| PROF-013 | P1 | Negative | User enters duplicate experience entries | System allows or warns according to business rule |
| PROF-014 | P0 | Functional | User adds a certification | Certification appears in profile and future matches |
| PROF-015 | P1 | Functional | User removes a skill | Skill disappears from profile and future matching logic |
| PROF-016 | P0 | Functional | User marks a skill as must-have | It weighs more heavily in ranking logic |
| PROF-017 | P1 | Functional | User marks a skill as nice-to-have | It influences ranking with lower weight |
| PROF-018 | P1 | Negative | User enters a blank skill name | Validation rejects blank entries |
| PROF-019 | P0 | Functional | User saves profile after editing multiple sections | All sections persist without data loss |
| PROF-020 | P1 | Edge | User edits profile while a job collection job is running | No data corruption or session interruption |
| PROF-021 | P0 | Functional | User sets remote preference to true | Remote jobs are prioritized in matching |
| PROF-022 | P1 | Functional | User sets hybrid preference | Hybrid jobs are included with adequate weighting |
| PROF-023 | P1 | Functional | User sets on-site preference | On-site jobs are included only when allowed |
| PROF-024 | P0 | Functional | User sets deal-breaker location exclusion | Jobs in excluded locations are filtered out |
| PROF-025 | P1 | Functional | User sets a daily application cap | System enforces cap during application workflow |
| PROF-026 | P1 | Negative | User sets zero or negative daily cap | Validation prevents invalid values |
| PROF-027 | P0 | Functional | User completes profile checklist | Completion score updates correctly |
| PROF-028 | P1 | Functional | User leaves some profile fields blank | Profile completeness still works and warns missing fields |
| PROF-029 | P1 | Functional | User switches between profile versions | Recent version is displayed and older versions remain accessible |
| PROF-030 | P1 | Negative | User tries to save duplicate profile version | System prevents unnecessary clone or handles gracefully |
| PROF-031 | P1 | Functional | User deletes a profile section | Section is removed and all dependent logic updates |
| PROF-032 | P1 | Negative | User deletes an essential required section | System refuses or prompts for confirmation |
| PROF-033 | P0 | Security | User accesses profile with expired session | System logs out or denies access |
| PROF-034 | P1 | Security | User tries to edit another user's profile | Access is denied |
| PROF-035 | P1 | UI | User view profile page on mobile | Layout remains readable and interactive |
| PROF-036 | P1 | UI | User view profile page on desktop | Layout remains aligned and complete |
| PROF-037 | P2 | Regression | Profile data remains after logout/login | User data persists correctly |
| PROF-038 | P2 | Regression | Existing profile values remain after partial update | Unchanged fields are not reset |
| PROF-039 | P1 | Edge | User imports resume with duplicate entries | Duplicate items are deduplicated or flagged |
| PROF-040 | P1 | Edge | User imports resume with unsupported format | System rejects with clear error |

## 3.2 Job Discovery and Collection

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| JOB-001 | P0 | Functional | Scheduled job fetch runs for a supported source | Jobs are collected and stored |
| JOB-002 | P1 | Functional | Manual refresh triggers collection | Fresh data is fetched and displayed |
| JOB-003 | P0 | Functional | Multiple sources produce same job listing | Duplicate is removed and canonical record remains |
| JOB-004 | P1 | Negative | One job source fails during collection | Other sources continue to function |
| JOB-005 | P0 | Functional | Source returns malformed job data | System records error and skips invalid entries |
| JOB-006 | P1 | Edge | Source returns empty result set | No crash; empty state is displayed |
| JOB-007 | P1 | Functional | Job title and description are scraped successfully | Normalized job record is created |
| JOB-008 | P0 | Functional | URL is missing from source data | Job is rejected or flagged for manual review |
| JOB-009 | P1 | Functional | Source uses different jurisdiction time format | Time is normalized consistently |
| JOB-010 | P1 | Functional | Job has remote tag but also on-site requirement | Matching logic resolves work mode correctly |
| JOB-011 | P1 | Functional | Company name is inconsistent across sources | System consolidates or stores canonical name |
| JOB-012 | P2 | Integration | Career page is crawled without API access | Data is extracted reliably if supported |
| JOB-013 | P1 | Negative | Job site blocks scraper or requires CAPTCHA | System marks source as blocked and continues |
| JOB-014 | P1 | Functional | New jobs appear while dashboard is open | User can refresh or job list updates appropriately |
| JOB-015 | P0 | Functional | Stale job record persists beyond expiry | It is demoted or excluded from active queue |
| JOB-016 | P1 | Functional | Old jobs are removed from active queue after threshold | Queue reflects current listings only |
| JOB-017 | P1 | Functional | Source has duplicate job entries within a single run | Duplicates are deduplicated before storage |
| JOB-018 | P0 | Functional | User modifies search preferences before next collection | New collection respects updates |
| JOB-019 | P1 | Functional | System collects jobs from direct company pages | They appear in queue with proper metadata |
| JOB-020 | P1 | Edge | Collection runs during maintenance window | It queues or pauses without corrupting data |
| JOB-021 | P1 | Functional | Data includes salary range in text form | Salary is parsed and normalized |
| JOB-022 | P1 | Functional | Data contains currency with commas or decimals | Parser handles format correctly |
| JOB-023 | P1 | Functional | Data contains non-English title | Title is stored and still scored appropriately |
| JOB-024 | P1 | Negative | Source data contains broken HTML | System strips HTML safely |
| JOB-025 | P1 | Functional | Job company uses limited URL or no domain | System stores sanitized URL and company name |
| JOB-026 | P1 | UI | User sees collection status in dashboard | Status is clear, readable, and timestamped |
| JOB-027 | P2 | Functional | Manual trigger occurs while auto-collection is active | System deduplicates and avoids duplicate inserts |
| JOB-028 | P1 | Regression | Daily collection job runs after restart | Scheduler resumes without duplicate jobs |
| JOB-029 | P1 | Functional | Source is disabled by user | Collection is skipped and logged |
| JOB-030 | P1 | Negative | User enters invalid source URL | Config validation blocks it |
| JOB-031 | P1 | Functional | Job listing includes multiple locations | System stores primary location and tags secondary ones |
| JOB-032 | P1 | Functional | Job includes remote + on-site hybrid requirement | Score weights reflect mixed work mode |
| JOB-033 | P1 | Functional | Source includes posting date in the future | System does not rank as current if it is not valid |
| JOB-034 | P1 | Edge | Job listing has missing description | System flags incomplete job and lowers confidence |
| JOB-035 | P1 | Functional | Data includes keywords not in profile | System stores unscored keywords but does not overfit |
| JOB-036 | P1 | Functional | Job has expired date | It is excluded from active queue |
| JOB-037 | P0 | Functional | Duplicate job records across sources with different title case | System normalizes and merges |
| JOB-038 | P1 | Functional | A source returns same job multiple times in same job run | It is deduplicated in-memory |
| JOB-039 | P1 | Functional | User filters on source name | Only selected source jobs remain visible |
| JOB-040 | P1 | Functional | User filters on company | Relevant jobs are displayed only |
| JOB-041 | P1 | Functional | User applies location filter | Only jobs satisfying filter remain |
| JOB-042 | P1 | Functional | User applies role filter | Correct roles remain active |
| JOB-043 | P1 | Functional | User applies salary floor | Low-paid roles drop out |
| JOB-044 | P1 | Functional | User applies skill filter | Jobs with missing required skills are hidden |
| JOB-045 | P1 | Functional | User changes search profile during job run | New collection respects new user settings |
| JOB-046 | P2 | Functional | Collection logs are accessible | User can review source health and timestamps |
| JOB-047 | P1 | Functional | Fresh jobs are prioritized over stale jobs | Ranking reflects recency |
| JOB-048 | P1 | Functional | Source quality is poor but still returns jobs | System warns and lowers weight |
| JOB-049 | P1 | Edge | Source has no jobs for several days | System shows empty-state without error bounce |
| JOB-050 | P1 | Regression | Duplicate deduplication runs across multiple systems | No duplication after restart or sync |
| JOB-051 | P0 | Integration | Remotive API adapter requests job listings | Unauthenticated JSON is normalized and the Remotive listing URL is retained |
| JOB-052 | P0 | Compliance | Remotive results appear in the dashboard | Remotive attribution and direct source link are visible |
| JOB-053 | P0 | Compliance | Remotive polling schedule is configured | Requests stay at or below four per day and never exceed two per minute |
| JOB-054 | P1 | Compliance | Remotive listing was posted less than 24 hours ago | Expected API delay is understood; system does not treat the feed as real-time |
| JOB-055 | P0 | Integration | Greenhouse board token is configured | Public GET endpoint returns listings without application credentials |
| JOB-056 | P0 | Security | Greenhouse submission endpoint is available | MVP collector never makes application POST requests |
| JOB-057 | P1 | Configuration | Greenhouse allowlist contains no board tokens | Greenhouse source reports not configured and does not attempt broad discovery |
| JOB-058 | P1 | Resilience | One Greenhouse board token is invalid | That board is marked unhealthy while other configured boards continue |

## 3.3 Filtering, Deduplication, and Data Quality

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| FIL-001 | P0 | Functional | Job in excluded country should be ignored | Job is filtered before ranking |
| FIL-002 | P0 | Functional | Job in blocked South Asian region is present | Job is rejected based on hard rule |
| FIL-003 | P0 | Functional | Job outside user’s desired remote setting | It is filtered or penalized |
| FIL-004 | P1 | Negative | Job with no title but valid description | It is marked incomplete and not top-ranked |
| FIL-005 | P0 | Functional | Job is employer scam or fake listing | It is flagged and deprioritized |
| FIL-006 | P1 | Functional | Company name has repeated spaces or punctuation | System normalizes and stores cleanly |
| FIL-007 | P1 | Functional | Duplicate job with alternate URL is found | One canonical snapshot remains |
| FIL-008 | P1 | Functional | Duplicate title but different company | It remains distinct; not merged incorrectly |
| FIL-009 | P1 | Functional | Job has missing salary tag | It is scored without salary signal and not rejected |
| FIL-010 | P1 | Functional | Job has invalid date format | It is sanitized or rejected |
| FIL-011 | P1 | Functional | Job role is completely unrelated to BA candidate profile | It receives low match score or is filtered |
| FIL-012 | P1 | Functional | Job role is similar but not exact match | Semantic matching keeps it relevant |
| FIL-013 | P0 | Functional | User sets strict location exclusion | Filter is applied on all collection and scoring paths |
| FIL-014 | P1 | Functional | Role filter is set to analyst only | Non-analyst roles are hidden |
| FIL-015 | P1 | Functional | User changes profile to “data analyst” | Matching adapts immediately |
| FIL-016 | P1 | Functional | User adds custom skill requirement | Jobs missing the skill are lower-ranked |
| FIL-017 | P1 | Functional | Job uses synonyms like “analytics” and “insights” | Matching recognizes semantic equivalent |
| FIL-018 | P1 | Functional | Job uses broad wording with irrelevant optimization | It is scored lower due to poor fit |
| FIL-019 | P1 | Negative | Skill list contains empty values | Empty entries are ignored |
| FIL-020 | P1 | Functional | Job includes duplicate skills in JD | Duplicates are treated once |
| FIL-021 | P1 | Functional | User excludes certain companies | Jobs from those companies are hidden |
| FIL-022 | P1 | Functional | Job is expired but still stored in queue | Expired jobs are hidden from active review |
| FIL-023 | P1 | Functional | Job metadata missing description but has title | System warns and lowers match confidence |
| FIL-024 | P1 | Functional | Job is posted in an excluded locale but remote from blocked country | System uses hard rule and removes it |
| FIL-025 | P1 | Functional | Job contains only generic requirement text | It is given low relevance score |
| FIL-026 | P1 | Functional | Source has low quality but valid jobs | Jobs still appear but with lower trust |
| FIL-027 | P1 | Functional | User modifies filter for salary threshold | Jobs below threshold disappear from queue |
| FIL-028 | P1 | Functional | Job qualifies on title but not on required skills | Score reflects missing skills and lowers rank |
| FIL-029 | P1 | Functional | Job qualifies on skills but lacks remote mode | Quality is reduced but not deleted |
| FIL-030 | P1 | Functional | Jobs with contract-only details are considered | System marks contract status correctly |
| FIL-031 | P1 | Functional | Job has unrealistic salary or impossible compensation | It is flagged for review or demoted |
| FIL-032 | P1 | Functional | Jobs with missing company details are still valid | They remain visible with lower trust |
| FIL-033 | P1 | Functional | User defines must-have skill list | Missed must-haves are visible in explanation |
| FIL-034 | P1 | Functional | One job duplicates another after title normalization | System merges and retains single canonical job |
| FIL-035 | P1 | Functional | User wants jobs with 6+ years experience only | Jobs below threshold filtered |
| FIL-036 | P1 | Negative | User enters impossible threshold values | Validation rejects or normalizes input |
| FIL-037 | P1 | Functional | A job with remote and on-site options remains valid | User preference determines ranking |
| FIL-038 | P1 | Functional | Job description contains hidden HTML or scripts | System sanitizes and parses safely |
| FIL-039 | P1 | Functional | Two different jobs from same company but different pathways | System keeps both distinct |
| FIL-040 | P1 | Regression | Filter rules persist after logout | User state is still enforced upon next session |
| FIL-041 | P0 | Functional | Remote posting belongs to employer based in India | Posting is excluded despite worldwide candidate eligibility |
| FIL-042 | P0 | Functional | Actual job/listing location is in Bangladesh but employer is based elsewhere | Posting is excluded by the job-origin rule |
| FIL-043 | P0 | Functional | Non-South-Asian employer explicitly accepts applicants in Bangladesh | Posting passes origin and current-user eligibility checks and may enter matching |
| FIL-044 | P0 | Edge | Employer/job origin cannot be determined | Posting is held out of eligible jobs until origin is verified |
| FIL-045 | P0 | Regression | User changes current residence country | South Asian job-origin and applicant-location exclusions remain in force |
| FIL-046 | P0 | Functional | Non-South-Asian employer permits remote applicants worldwide, including Bangladesh | Posting passes origin and current-user eligibility checks and may enter matching |
| FIL-047 | P0 | Functional | Remote posting explicitly lists only non-South-Asian applicant countries and includes current non-excluded user location | Posting may proceed to remaining filters |
| FIL-048 | P0 | Functional | Current user location is Bangladesh and a remote job explicitly excludes all South Asian applicants | Posting is rejected because current user location is not eligible |
| FIL-049 | P0 | Edge | Source omits employer/job origin | Posting is held out until origin is verified; unknown candidate eligibility alone does not imply South Asian origin |
| FIL-050 | P0 | Functional | Every collected listing is blocked by location policy | Dashboard shows an explanatory empty state and does not relax filters |
| FIL-051 | P0 | Regression | Country appears under an alias or alternate spelling | It normalizes to the correct ISO code and the exclusion is enforced |
| FIL-052 | P0 | Security | LLM or semantic scorer rates an excluded remote job highly | Deterministic location gate still rejects it before persistence |
| FIL-053 | P0 | Regression | Employer/job origin resolves to South Asia after initial parse | Record is discarded before ranking, persistence, or document generation |
| FIL-054 | P1 | Edge | Non-South-Asian employer origin is known but applicant-location eligibility is unclear | Posting is held for eligibility review; it is not rejected solely because South Asian applicants may be permitted |

## 3.4 Matching, Scoring, and Confidence Gates

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| SCO-001 | P0 | Functional | Job matches most profile skills strongly | Score is high and visible on dashboard |
| SCO-002 | P0 | Functional | Job matches only a few skills | Score remains low and appears in lower queue |
| SCO-003 | P0 | Functional | Job includes all must-have skills | Score increases and job qualifies for review |
| SCO-004 | P0 | Functional | Job misses must-have skills | Score drops and system warns user |
| SCO-005 | P1 | Functional | Semantic match recognizes “stakeholder communication” as relevant to BA work | Job is scored more favorably |
| SCO-006 | P1 | Functional | Job title is broad but description fits strongly | Score is adjusted appropriately |
| SCO-007 | P1 | Functional | Job title matches but actual duties do not | Final score falls after deeper analysis |
| SCO-008 | P1 | Functional | One job is remote but weak skill match | It ranks below strong on-site role |
| SCO-009 | P0 | Functional | Missing essential certification lowers confidence | Score declines with explanation |
| SCO-010 | P1 | Functional | Job has salary range in acceptable range | Score improves slightly |
| SCO-011 | P1 | Functional | Salary is below market range | Job is demoted or flagged as below-fit |
| SCO-012 | P1 | Functional | Job is newly posted and relevant | Score includes freshness value |
| SCO-013 | P1 | Functional | Aging job is still relevant but old | Staleness penalty reduces score |
| SCO-014 | P1 | Functional | Job matches user’s preferred domain heavily | Domain score increases |
| SCO-015 | P1 | Functional | Job score explanation is generated | User sees plain-language breakdown |
| SCO-016 | P1 | Functional | User views fit explanation | It explains major reasons for match or mismatch |
| SCO-017 | P0 | Functional | Job below minimum fit threshold | It is excluded from review queue |
| SCO-018 | P1 | Functional | Job slightly above threshold | It appears in review queue and is not excluded |
| SCO-019 | P1 | Negative | Threshold is set to invalid number | System rejects invalid configuration |
| SCO-020 | P0 | Functional | Jobs are reordered by score descending | Highest-fit jobs appear first |
| SCO-021 | P1 | Functional | Multiple jobs have identical score | Tie-break logic is deterministic |
| SCO-022 | P1 | Functional | User adjusts score threshold | Review queue updates immediately |
| SCO-023 | P1 | Functional | User has no jobs after filtering | Empty state shows explanation |
| SCO-024 | P1 | Functional | One job has poor company trust but strong fit | Trust score reduces final ranking |
| SCO-025 | P1 | Functional | Company review is unavailable | Job stays visible but with lower confidence |
| SCO-026 | P0 | Functional | Strong role fit with poor visa or location support | System reduces score or warns |
| SCO-027 | P1 | Functional | Strong remote role outside preferred countries | It is filtered as regional mismatch |
| SCO-028 | P1 | Functional | Job mentions “analyst” but is really a sales analyst role | It is ranked lower than BA-specific roles |
| SCO-029 | P1 | Functional | Job mentions “business data analyst” | It is ranked as strong fit |
| SCO-030 | P1 | Functional | Big portfolio or project description raises relevance | Score reflects domain knowledge without overfitting |
| SCO-031 | P1 | Functional | User skill set is outdated compared to JD | Score decreases and recommendation is clear |
| SCO-032 | P0 | Functional | User profile has missing experience field | Matching still works but with lower confidence |
| SCO-033 | P1 | Functional | User role target changed from BA to product analyst | Matches follow new target role |
| SCO-034 | P1 | Functional | Job requires SQL and Excel heavily | Resume with strong SQL but weak Excel reduces score |
| SCO-035 | P1 | Functional | Job requires stakeholder analytics and reporting | Matching sees those skills as highly relevant |
| SCO-036 | P1 | Functional | A title uses unusual term not in profile | Semantic match still identifies relation |
| SCO-037 | P1 | Functional | A job requires certifications not in profile | Lower score and explicit missing item |
| SCO-038 | P1 | Functional | Job shows strong salary but poor fit | Salary weight is not enough to override poor fit |
| SCO-039 | P1 | Functional | User toggles to focus only on remote jobs | Non-remote jobs are demoted or excluded |
| SCO-040 | P1 | Functional | Job is high fit but from a suspicious company | Final rank stays lower than trusted employer |
| SCO-041 | P1 | Functional | Score explanation shows different weights for must-have skills | Breakdown is visible and consistent |
| SCO-042 | P1 | Negative | Score generation fails for one job | System queues job as pending and does not crash all jobs |
| SCO-043 | P1 | Functional | Job record is updated after scoring | New score is recalculated and saved |
| SCO-044 | P1 | Regression | Re-scoring after profile update removes previous job score | New score appears correctly |
| SCO-045 | P1 | Functional | Pending scoring jobs are shown separately | User can see they are being processed |
| SCO-046 | P1 | Functional | User sees historical score change over time | Versioned tracking works |
| SCO-047 | P1 | Functional | The scoring engine uses the same profile over time | It remains stable and not mutated unexpectedly |
| SCO-048 | P1 | Functional | Soft skill match contributes modestly | It improves score without dominating technical skills |
| SCO-049 | P1 | Functional | Job requires heavily domain-specific terms | Profile with domain work is ranked higher |
| SCO-050 | P1 | Functional | User wants analyst roles plus program manager overlap | Matching handles role crossover sensibly |
| SCO-051 | P1 | Functional | A job from a company with strong brand but risk signal | Trust penalty and fit score combine appropriately |
| SCO-052 | P1 | Functional | User sets scoring emphasis on salary rather than fit | Ranking responds to custom weighting |
| SCO-053 | P1 | Negative | User sets unsupported weighting value | System rejects invalid configuration |
| SCO-054 | P1 | Functional | Score is recalculated after a job source refresh | Updated record uses new match insight |
| SCO-055 | P1 | Functional | Jobs with zero score are handled | They do not crash the interface |
| SCO-056 | P1 | Functional | Job relation is explained as “missing required skills” | Explanation content is concise and clear |
| SCO-057 | P1 | Functional | Job with low confidence but strong match to high-value skill | It still stays in queue depending on thresholds |
| SCO-058 | P1 | Functional | User toggles “Include all roles” | Ranking behavior updates and queue changes |
| SCO-059 | P1 | Functional | User toggles “exclude contract” | Contract-only jobs are hidden |
| SCO-060 | P1 | Functional | Ranking remains deterministic across repeated score runs | Same inputs yield same order |

## 3.5 Resume and Tailoring

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| RES-001 | P0 | Functional | User generates tailored resume for a strong-fit job | Resume is generated successfully |
| RES-002 | P0 | Functional | User generates tailored resume for a weak-fit job | System warns and still generates a lower-confidence draft |
| RES-003 | P0 | Functional | Resume generation uses verified profile facts only | Unsupported claims are not inserted |
| RES-004 | P0 | Functional | Generated resume includes relevant job keywords | Matching language is present without padding |
| RES-005 | P1 | Functional | Resume omits irrelevant extra skills | Tailored version stays focused |
| RES-006 | P1 | Functional | User opens generated resume preview | PDF or HTML preview loads without errors |
| RES-007 | P0 | Functional | User downloads tailored resume | File downloads successfully |
| RES-008 | P1 | Negative | Resume generation with incomplete profile | System warns and produces minimal version |
| RES-009 | P1 | Functional | User edits generated resume inline | Changes are saved and persisted |
| RES-010 | P1 | Functional | User restores earlier resume version | Previous version is recovered correctly |
| RES-011 | P1 | Functional | Resume contains multiple experiences | Correct experience entries are selected for the job |
| RES-012 | P1 | Functional | Resume includes projects relevant to role | Project section highlights relevant work |
| RES-013 | P1 | Functional | Resume excludes unrelated projects | Irrelevant projects are dropped |
| RES-014 | P0 | Functional | Cover letter is generated for selected role | It is generated with job-specific content |
| RES-015 | P1 | Functional | Cover letter references real user experience | It matches profile truthfully |
| RES-016 | P1 | Negative | Cover letter invents credentials | System blocks or flags unsupported claims |
| RES-017 | P1 | Functional | User edits cover letter text | Updated version is saved and tracked |
| RES-018 | P0 | Functional | User previews cover letter with PDF/HTML view | Document is readable and complete |
| RES-019 | P1 | Functional | Job-specific answer drafts are generated | Answers align with job requirements |
| RES-020 | P1 | Functional | User approves generated answer version | It is marked approved and associated to application |
| RES-021 | P1 | Functional | User rejects generated answer version | It remains editable or regenerates after rejection |
| RES-022 | P0 | Functional | Resume generation respects ATS-friendly formatting | Document remains clean and readable by parsers |
| RES-023 | P1 | Functional | Resume with tables or complex formatting | System retains readability and avoids broken layout |
| RES-024 | P1 | Functional | Resume contains special characters | They render correctly in generated output |
| RES-025 | P1 | Functional | Resume generation for a location outside country | It reflects any required work authorization notes |
| RES-026 | P1 | Functional | User edits skill ordering | Final resume section order remains sensible |
| RES-027 | P1 | Functional | Resume generation includes keywords from job description | It balances relevance without stuffing |
| RES-028 | P1 | Functional | Resume generation excludes excessive generic filler | Output stays concise and credible |
| RES-029 | P1 | Functional | User compares two resume versions | Version diff is readable |
| RES-030 | P1 | Functional | Resume update after profile edit is reflected in new generation | New version is generated from current profile |
| RES-031 | P1 | Functional | User generates multiple resumes for same job | Each version is tracked and distinct |
| RES-032 | P1 | Functional | Resume status history is visible | User can inspect when and why a version was produced |
| RES-033 | P1 | Functional | User downloads multiple tailored documents | Each file is named distinctly and correctly |
| RES-034 | P1 | Functional | Cover letter generation falls back gracefully if profile is sparse | Minimal version still exists |
| RES-035 | P0 | Functional | User sees resume summary before approval | Summary proves correctness before submission |
| RES-036 | P1 | Functional | Resume includes only skills relevant to the role | Unrelated skills are not emphasized |
| RES-037 | P1 | Functional | User changes ordering of experience items | Order is reflected in generated resume |
| RES-038 | P1 | Functional | Resume generation with project data | Project list is included appropriately |
| RES-039 | P1 | Negative | Resume generation if model output fails | System raises controlled error and preserves previous version |
| RES-040 | P1 | Functional | User submits resume without cover letter if job doesn’t require it | Workflow still proceeds without failure |
| RES-041 | P1 | Functional | Resume bullet points are tailored for job style | They match role language and tone |
| RES-042 | P1 | Functional | Percentages or numeric achievements are preserved | Data remains accurate and not fabricated |
| RES-043 | P1 | Functional | User adds custom notes to generated resume | They persist and are visible in final review |
| RES-044 | P1 | Functional | Resume is generated with appropriate action verbs | Output remains professional and polished |
| RES-045 | P1 | Functional | System avoids duplicate bullet points | Output remains concise and non-repetitive |
| RES-046 | P1 | Functional | System prefers strongest professional experience | Premium experience appears earlier |
| RES-047 | P1 | Functional | User marks a project as confidential | System excludes or sanitizes it appropriately |
| RES-048 | P1 | Functional | AI output has unsupported claim detection | System warns before allowing approval |
| RES-049 | P1 | Functional | User regenerates tailored resume | Old version remains archived and new one is active |
| RES-050 | P1 | Functional | Resume generation for job with no relevant experience still produces realistic output | It avoids false claims |
| RES-051 | P1 | Functional | User compares old and new resume | Differences are understandable and honest |
| RES-052 | P1 | Functional | Resume generation supports multiple templates | Templates render cleanly |
| RES-053 | P1 | Functional | Job-specific answer uses verified facts | It does not fabricate client names or metrics |
| RES-054 | P1 | Functional | User chooses to use shorter resume format | Tailored short version is generated correctly |
| RES-055 | P1 | Functional | Resume includes education and certification only when relevant | Less relevant sections are reduced |
| RES-056 | P1 | Functional | User deletes a project from profile | It is removed from future resume generation |
| RES-057 | P1 | Functional | User edits summary after tailoring | Future resume generation uses updated version |
| RES-058 | P1 | Functional | PDF export is visible in browser | Output opens correctly or downloads |
| RES-059 | P1 | Functional | Resume is created as a new version even if same content | It is tracked as a distinct event |
| RES-060 | P1 | Functional | User tries to generate resume for invalid job ID | System returns controlled error with no crash |
| RES-061 | P1 | Functional | Resume generation after job update uses newest data | Output changes when JD changes |
| RES-062 | P1 | Functional | System preserves formatting across supported browsers | Output remains consistent |
| RES-063 | P1 | Performance | Resume generation completes within expected time | User receives output within acceptable threshold |
| RES-064 | P1 | Security | Generated document does not include hidden malicious script | Safe output only |
| RES-065 | P1 | Edge | Resume generation under large profile data | Output remains stable and correct |
| RES-066 | P1 | Functional | Resume contains final job title as context | It appears in heading or summary when appropriate |
| RES-067 | P1 | Functional | Resume references only relevant achievements | Less relevant metrics are excluded |
| RES-068 | P1 | Functional | User can add custom remarks to resume | The system stores them safely |
| RES-069 | P1 | Functional | User toggles between ATS and standard resume style | Correct version renders based on user choice |
| RES-070 | P1 | Functional | System warns when resume has too many sections | It suggests simplifying it |
| RES-071 | P1 | Functional | User uses master profile to generate a general resume | It works without a specific job |
| RES-072 | P1 | Functional | Resume-specific metadata is stored with the job record | It can be traced later |
| RES-073 | P1 | Functional | System generates or reuses cover letter when no job required | It flags optional status correctly |
| RES-074 | P1 | Functional | User rejects resume and asks for regeneration | New version is generated without affecting older versions |
| RES-075 | P1 | Functional | User can compare final resume against master resume | Differences are understandable |
| RES-076 | P1 | Functional | Editable resume content is not overwritten by re-generation unless user confirms | This safety rule is enforced |
| RES-077 | P1 | Functional | User selects template before generation | Correct template is applied |
| RES-078 | P1 | Functional | Resume generation is logged with timestamp | Auditing is possible |
| RES-079 | P1 | Functional | Generated answer is saved with job and profile snapshot | Reproducibility is ensured |
| RES-080 | P1 | Functional | User uses resume for manual application with no automation | Workflow remains supported |

## 3.6 Dashboard and Review Queue

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| DASH-001 | P0 | Functional | User opens main dashboard | Top jobs and queue are visible |
| DASH-002 | P0 | Functional | Jobs show fit score | Score is displayed with clear value |
| DASH-003 | P0 | Functional | Jobs show company name and title | Metadata is visible and correct |
| DASH-004 | P1 | Functional | User filters jobs by fit score | Only matching jobs remain on screen |
| DASH-005 | P0 | Functional | User approves a job | Status updates to approved |
| DASH-006 | P0 | Functional | User rejects a job | Status updates to rejected and is removed or marked accordingly |
| DASH-007 | P0 | Functional | User edits a job before approval | Updates are saved before final action |
| DASH-008 | P1 | Functional | User sorts jobs by newest first | Sorting reflects selected order |
| DASH-009 | P1 | Functional | User sorts jobs by highest score | Correct ordering is visible |
| DASH-010 | P1 | Functional | User sorts jobs by salary | Salary sorting works accurately |
| DASH-011 | P1 | Functional | User uses search box to find a job | Search returns relevant jobs |
| DASH-012 | P1 | Functional | User resets filters | All jobs reappear correctly |
| DASH-013 | P0 | Functional | Summary cards show total jobs, strong fits, approved, rejected | Values are accurate |
| DASH-014 | P1 | Functional | Budget summary is visible | Cost usage and remaining credits show correctly |
| DASH-015 | P1 | Functional | Budget threshold warning triggers | User sees warning before hitting limit |
| DASH-016 | P1 | Functional | User sees “needs you” queue | Blocked actions appear separately |
| DASH-017 | P1 | Functional | Job card expansion shows explanation details | User can inspect why it matched/lacked fit |
| DASH-018 | P1 | Functional | User sees schedule status for job collection | Updated status is visible and correct |
| DASH-019 | P1 | UI | Dashboard on large desktop screen | Layout remains readable and resizable |
| DASH-020 | P1 | UI | Dashboard on tablet | It remains usable and not clipped |
| DASH-021 | P1 | UI | Dashboard on mobile | Components stack correctly and remain accessible |
| DASH-022 | P1 | Functional | User sees job age and posting date | It is displayed clearly |
| DASH-023 | P1 | Functional | User sees source label | Source is clearly identified |
| DASH-024 | P1 | Functional | User sees company trust signal | Risk or trust rating is shown |
| DASH-025 | P0 | Functional | User clicks “review details” for a job | Job detail panel or page opens |
| DASH-026 | P1 | Functional | User edits job notes | Notes save and persist |
| DASH-027 | P1 | Functional | User marks a job as favorite | Favorite status persists |
| DASH-028 | P1 | Functional | User unmarks a job as favorite | Favorite status is removed |
| DASH-029 | P1 | Functional | Job card includes salary indicator | Salary range displays correctly |
| DASH-030 | P1 | Functionality | User saves custom filters | Filters remain in next session |
| DASH-031 | P1 | Functional | User clears custom filter state | It resets to default behavior |
| DASH-032 | P1 | UI | Empty queue shows proper message | The user understands there are no jobs |
| DASH-033 | P1 | Functional | Queue updates after manual refresh | New jobs appear without reload issues |
| DASH-034 | P1 | Functional | A rejected job can be restored to candidate queue | User can reopen it with reason tracked |
| DASH-035 | P1 | Functional | Job detail panel includes full description | It is readable and not truncated incorrectly |
| DASH-036 | P1 | Functional | Long job description is handled gracefully | Layout and readability remain intact |
| DASH-037 | P1 | Functional | User clicks view application materials | Resume and cover letter preview open correctly |
| DASH-038 | P1 | Functional | The dashboard shows only active queue by default | Hidden items are not shown unexpectedly |
| DASH-039 | P1 | Functional | Filtering by source works | Only selected source jobs remain |
| DASH-040 | P1 | Functional | Filtering by role works | Only relevant jobs remain |
| DASH-041 | P1 | Functional | Filtering by salary range works | Matching range is enforced |
| DASH-042 | P1 | Functional | Sorting by newest vs oldest is accurate | Date sorting matches actual timestamps |
| DASH-043 | P1 | Functional | Approve action retains job in approved pipeline | It appears in correct queue |
| DASH-044 | P1 | Functional | Reject action keeps a reason or flag | User can inspect reason later |
| DASH-045 | P1 | Functional | User reviews a job from needs-you queue | Action is available and trail remains |
| DASH-046 | P1 | Functional | Job data remains readable after profile update | The queue does not lose metadata |
| DASH-047 | P1 | Functional | Dashboard shows all pipeline counts | Count totals match actual records |
| DASH-048 | P1 | Regression | Dashboard refresh does not duplicate jobs | UI remains stable and not repeated |
| DASH-049 | P1 | Functional | User marks a job as follow-up needed | It appears in follow-up list |
| DASH-050 | P1 | Functional | User sees reminder count for follow-up | Count is accurate across records |
| DASH-051 | P1 | Functional | Review queue updates after application outcome | Job status shifts correctly |
| DASH-052 | P1 | Functional | User can export job list | File contains accurate summary data |
| DASH-053 | P1 | Functional | User can open analytics from dashboard | Analytics page loads correctly |
| DASH-054 | P1 | Functional | Dashboard remains responsive under 100 jobs | It handles large queue without serious lag |
| DASH-055 | P1 | Functional | Dashboard runs with zero jobs | It shows empty-safe state without breakage |
| DASH-056 | P1 | UI | Action buttons are visible and labeled clearly | No ambiguous or hidden buttons |
| DASH-057 | P1 | Functional | User can switch between queue tabs | Data persists and view changes correctly |
| DASH-058 | P1 | Functional | Mixed state jobs display proper icon or badge | User can tell status at a glance |
| DASH-059 | P1 | Functional | User sees explanation for blocked or low-confidence queue items | Why it is there is clear |
| DASH-060 | P1 | Functional | Job detail page still works after a delayed background refresh | No stale or broken data |

## 3.7 Application Execution and Tracking

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| APP-001 | P0 | Functional | User approves a job for application | Application process starts only after explicit approval |
| APP-002 | P0 | Functional | User rejects a job before any submission | No application attempt is made |
| APP-003 | P0 | Functional | System submits through ATS-supported flow | Submission succeeds or fails cleanly with reason |
| APP-004 | P1 | Functional | System uses web form route for supported site | It fills required fields with user-approved data |
| APP-005 | P1 | Functional | System uses email-based application flow | It sends or prepares email correctly |
| APP-006 | P0 | Functional | Application attempt is logged | Job status and audit trail update |
| APP-007 | P1 | Functional | Submission confirmation URL is stored | It is available for review |
| APP-008 | P1 | Functional | Confirmation page or payload is captured | System stores proof and updates status |
| APP-009 | P1 | Functional | Submission fails due to page timeout | System marks failure reason and logs details |
| APP-010 | P1 | Functional | Submission fails due to login requirement | Job moves to needs-you queue |
| APP-011 | P1 | Functional | CAPTCHA blockers occur | Job is marked manual intervention required |
| APP-012 | P1 | Functional | User receives retry option | Retry path is available and uses stored draft |
| APP-013 | P0 | Functional | Application moves through states: pending → submitted → confirmed | Flow is accurate and traceable |
| APP-014 | P1 | Functional | Application status is updated after email response | System reflects outcome changes |
| APP-015 | P1 | Functional | User reviews application history | Old events appear with timestamps |
| APP-016 | P1 | Functional | User opens a submitted application | Relevant details and documents appear |
| APP-017 | P1 | Functional | Submission fails with generic error | User sees general message without unhandled app crash |
| APP-018 | P1 | Functional | Manual override is available | User can mark success/failure manually |
| APP-019 | P1 | Functional | A job is resubmitted after correction | It follows expected path without duplication |
| APP-020 | P1 | Negative | User tries to submit without approval | System prevents and says approval required |
| APP-021 | P0 | Security | User attempts to apply for a job with expired token or session | System rejects and prompts re-login |
| APP-022 | P1 | Functional | Outbound form submission uses sanitized data | No malformed values are sent |
| APP-023 | P1 | Functional | User pauses or cancels application | Job remains in pending state and is not lost |
| APP-024 | P1 | Functional | Application track page loads after a long time | It remains responsive and accurate |
| APP-025 | P1 | Functional | Job lifecycle includes rejection, interview, and offer states | Correct statuses are tracked |
| APP-026 | P1 | Functional | User approves multiple jobs in one batch | System handles queue and tracking without collisions |
| APP-027 | P1 | Functional | User approves while another job is being submitted | Queue serialization prevents duplicate actions |
| APP-028 | P1 | Functional | Job status transitions persist after refresh | User does not lose progress |
| APP-029 | P1 | Functional | Submission attempts are deduplicated | Duplicate sends are prevented |
| APP-030 | P1 | Functional | A failed application is retried after fix | Updated trace shows new submission attempt |
| APP-031 | P1 | Functional | Manual intervention entry is stored | User can later revisit and continue |
| APP-032 | P1 | Functional | Application outcome audit trail is available | User can inspect who/what changed status |
| APP-033 | P1 | Functional | User sees reason codes for failure | They are understandable and actionable |
| APP-034 | P1 | Functional | Job is auto-moved to manual queue after blocked form | Queue status correct |
| APP-035 | P1 | Functional | Application is tracked even when no automation is used | manual and automated flows are consistent |
| APP-036 | P1 | Functional | User attaches application notes | Notes appear in history and are accessible |
| APP-037 | P1 | Functional | User sees next recommended action after submission | Workflow suggests next step |
| APP-038 | P1 | Functional | Application is stored even when system external page does not respond | It is marked as pending or failed explicitly |
| APP-039 | P1 | Functional | Resume and cover letter are linked to submitted job | User can inspect exact documents used |
| APP-040 | P1 | Functional | Rejected app can be reopened for future decision | It no longer blocks future process |
| APP-041 | P1 | Functional | Approve action requires final confirmation | Prevents accidental submission |
| APP-042 | P1 | Functional | Application process respects daily cap | User cannot exceed configured cap |
| APP-043 | P1 | Functional | Manual application status update does not create duplicate record | No data duplication |
| APP-044 | P1 | Functional | Job status remains correct after browser refresh | No UI mismatch |
| APP-045 | P1 | Functional | User can sort applications by date or status | Correct order is maintained |
| APP-046 | P1 | Functional | Application result is stored with timestamps | Data is auditable |
| APP-047 | P1 | Functional | Follow-up reminder is created after submission | It appears in user tasks |
| APP-048 | P1 | Functional | System marks submission as confirmed only when proof exists | False positives are avoided |
| APP-049 | P1 | Functional | User sees “pending approval” banner before submit | There is no ambiguity |
| APP-050 | P1 | Functional | User can review all drafts associated with an application | Draft history is accessible |
| APP-051 | P1 | Functional | User can ask for resubmission after job changed | Resume and letter reconstruct properly |
| APP-052 | P1 | Functional | Application lifecycle respects audit log integrity | No missing state transitions |
| APP-053 | P1 | Functional | System prevents duplicate submissions for same job within same period | Repeated clicks are blocked |
| APP-054 | P1 | Functional | User marks application as withdrawn | Status changes and no further actions occur |
| APP-055 | P1 | Functional | Manual status updates are logged | History remains reliable |

## 3.8 Trust, Safety, and Company Checks

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| TRUST-001 | P0 | Functional | Company has strong public trust signals | Job score includes trust boost |
| TRUST-002 | P1 | Functional | Company has suspicious patterns | System flags and reduces trust score |
| TRUST-003 | P1 | Functional | Company legitimacy data is unavailable | System handles gracefully without full failure |
| TRUST-004 | P1 | Functional | Job from suspicious company is still assessed | Risk is clearly shown |
| TRUST-005 | P0 | Security | System does not fabricate company reviews | Only real or clearly labeled signals are used |
| TRUST-006 | P1 | Functional | User can view company summary | Summary includes key trust indicators |
| TRUST-007 | P1 | Functional | Company summary is cached | Repeated checks don’t regenerate unnecessarily |
| TRUST-008 | P1 | Functional | Company review is stale | System refreshes or flags stale data |
| TRUST-009 | P1 | Functional | Suspicious listing is deprioritized | It is shown lower in queue |
| TRUST-010 | P1 | Functional | Valid job from trusted company remains visible | It is not hidden by trust logic |
| TRUST-011 | P1 | Functional | User review of company insights is legible | Plain-language summary is concise |
| TRUST-012 | P1 | Functional | User sees trust summary in job card | No need to open details for basic understanding |
| TRUST-013 | P1 | Functional | Job from a red-flag company gets explicit risk message | User knows why it was demoted |
| TRUST-014 | P1 | Functional | Data source for trust score is visible | User can understand where the signal came from |
| TRUST-015 | P1 | Negative | Trust check service is down | System continues but marks trust as unknown |
| TRUST-016 | P1 | Functional | User suppresses a trust warning | It is stored as override but still audit-logged |
| TRUST-017 | P1 | Functional | Trust override is temporary or explicit | It is visible to user and future review |
| TRUST-018 | P1 | Functional | Company data is sanitized before display | Dangerous input is escaped |
| TRUST-019 | P1 | Security | Malicious company description is input | It is sanitized and displayed safely |
| TRUST-020 | P1 | Functional | Job quality is not reduced solely because source is less known | Trust is balanced with fit |
| TRUST-021 | P1 | Functional | Red flags are shown with severity levels | User sees how serious they are |
| TRUST-022 | P1 | Functional | Users can filter suspicious jobs out | They no longer appear in default queue |
| TRUST-023 | P1 | Functional | Reference company signals are accurate | The trust score doesn’t randomize or drift unpredictably |
| TRUST-024 | P1 | Functional | Job from company with no public signal is not treated as guaranteed bad | It remains reviewable |
| TRUST-025 | P1 | Functional | Trust logic is reused by ranking model | It impacts score without overpowering fit |
| TRUST-026 | P1 | Functional | Job with expired listing and suspicious company | Both issues are surfaced clearly |
| TRUST-027 | P1 | Functional | User marks a company as safe or unsafe | Override is stored and used later |
| TRUST-028 | P1 | Functional | Trust check remains on a single company record | Duplicate company entries are merged |
| TRUST-029 | P1 | Functional | User sees a final company-risk summary for the job | It is aggregated and not contradictory |
| TRUST-030 | P1 | Functional | Company review summary updates after new information | Cache refresh behavior works |
| TRUST-031 | P1 | Functional | User can hide trust warnings for a while | They remain but with clear override status |
| TRUST-032 | P1 | Functional | Privacy settings ensure trust data is not overexposed | Sensitive profile is not linked improperly |
| TRUST-033 | P1 | Functional | A risky company with strong candidate fit is still reviewable | Not blocked indefinitely |
| TRUST-034 | P1 | Functional | “Unknown trust” state is distinct from “low trust” | User sees correct semantics |
| TRUST-035 | P1 | Functional | Tools for trust review remain within allowed scope | No unapproved external data leakage |

## 3.9 Learning, Analytics, and Improvement

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| LEARN-001 | P1 | Functional | User approves a job | Outcome is recorded for learning |
| LEARN-002 | P1 | Functional | User rejects a job | Rejection is stored with reason |
| LEARN-003 | P1 | Functional | User gets interview callback | Outcome updates job status and learning data |
| LEARN-004 | P1 | Functional | User receives offer | Offer state is stored and contributes to analytics |
| LEARN-005 | P1 | Functional | User rejects a role after interviewing | The outcome is preserved for future tuning |
| LEARN-006 | P1 | Functional | Analytics page loads | Summary metrics are visible |
| LEARN-007 | P1 | Functional | Skill performance summary is shown | Relevant skill trends are visible |
| LEARN-008 | P1 | Functional | Source performance data is shown | Best sources are visible |
| LEARN-009 | P1 | Functional | Resume tailoring quality is tracked | Variation of success outcomes is tracked |
| LEARN-010 | P1 | Functional | User edits profile to change skill weight | Learning data remains consistent with profile version |
| LEARN-011 | P1 | Functional | Job outcome is associated to profile version | Learning remains auditable |
| LEARN-012 | P1 | Functional | User sees success rate by source | Metric is accurate |
| LEARN-013 | P1 | Functional | User sees success rate by skill | Metric is meaningfully displayed |
| LEARN-014 | P1 | Functional | System recalculates learning after many outcomes | Analytics remain updated |
| LEARN-015 | P1 | Functional | One invalid outcome record is entered | System rejects or flags it without breaking analytics |
| LEARN-016 | P1 | Functional | Learning model updates after enough sample size | It triggers ranking improvement only when valid |
| LEARN-017 | P1 | Functional | No outcomes exist yet | Empty analytics state is shown respectfully |
| LEARN-018 | P1 | Functional | User chooses to export analytics data | Export completes successfully |
| LEARN-019 | P1 | Functional | Progress over time is displayed | Visualized trend is clear |
| LEARN-020 | P1 | Functional | User sees approvals vs rejections | Chart or table reflects real data |
| LEARN-021 | P1 | Functional | Source or keyword quality data is stale | System warns or refreshes it |
| LEARN-022 | P1 | Functional | Learning data is retained after logout/login | It is not lost |
| LEARN-023 | P1 | Functional | User can filter analytics by date | Response reflects selected time window |
| LEARN-024 | P1 | Functional | Data is grouped by role or source | User sees different contexts correctly |
| LEARN-025 | P1 | Functional | System stores outcome record for manual job activity | It is not lost even if no automation exists |
| LEARN-026 | P1 | Functional | A failed application is recorded as low outcome | It contributes to optimization appropriately |
| LEARN-027 | P1 | Functional | Interview follow-up data updates outcome metrics | It stays consistent with real status |
| LEARN-028 | P1 | Functional | User sees recommendation quality improvement over time | Trend is accurate and not fabricated |
| LEARN-029 | P1 | Functional | Analytics does not misreport zero values | Empty stats are displayed correctly |
| LEARN-030 | P1 | Functional | Historical data remains after profile modification | Learning is not deleted inadvertently |
| LEARN-031 | P1 | Functional | Role-specific analytics are isolated | Cross-role data does not contaminate each other |
| LEARN-032 | P1 | Functional | Learning module handles sparse data gracefully | It warns instead of failing |
| LEARN-033 | P1 | Functionality | AI suggestions from learning are visible to user | They are understandable and editable |
| LEARN-034 | P1 | Functional | User can disable learning-based tweaks | Setting is respected in ranking |
| LEARN-035 | P1 | Functional | Learning settings are saved per profile | Different profiles do not bleed together |

## 3.10 Advanced Career Features and Future Enhancements

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| ADV-001 | P2 | Functional | User requests interview prep | Likely questions are generated |
| ADV-002 | P2 | Functional | User asks for follow-up reminders | Reminder tasks are created |
| ADV-003 | P2 | Functional | User asks for referral assistance | Draft message or action is generated |
| ADV-004 | P2 | Functional | User requests ATS simulation | Resume quality score appears |
| ADV-005 | P2 | Functional | User asks conversational questions about job search | Agent responds using stored data |
| ADV-006 | P2 | Functional | User asks for market insight | Strategy suggestions are shown |
| ADV-007 | P2 | Functional | User adds second profile | It is created and isolated |
| ADV-008 | P2 | Functional | User switches profiles | Correct data and settings become active |
| ADV-009 | P2 | Functional | Multi-profile data remains independent | Cross-profile mixing does not occur |
| ADV-010 | P2 | Functional | Voice command triggers common actions | It performs expected function safely |
| ADV-011 | P2 | Negative | Voice action is ambiguous | System asks for clarification or rejects |
| ADV-012 | P2 | Functional | Portfolio support is configured | Public or private portfolio data is stored properly |
| ADV-013 | P2 | Functional | Career planning suggestions are shown | They are based on analytics and profile data |
| ADV-014 | P2 | Functional | User ignores suggestion | No data corruption occurs |
| ADV-015 | P2 | Functional | Interview prep content is stored with the job | Relevant data stays associated |

## 3.11 Non-Functional, Security, and Performance

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| NFR-001 | P0 | Performance | Dashboard loads under normal conditions | It loads in acceptable time |
| NFR-002 | P1 | Performance | 100 jobs are processed in the queue | It remains responsive |
| NFR-003 | P1 | Performance | Resume generation with medium profile loads within threshold | It completes quickly enough |
| NFR-004 | P1 | Performance | Job collection across 5 sources completes | It does not crash or hang |
| NFR-005 | P0 | Security | User password is not stored in plain text | Proper hashing or encryption is used |
| NFR-006 | P0 | Security | Session tokens are protected | They are not exposed in URLs or logs |
| NFR-007 | P0 | Security | User data access requires authentication | Unauthorized access is blocked |
| NFR-008 | P0 | Security | Authorization checks are enforced for all user-specific endpoints | Only owner can access their data |
| NFR-009 | P1 | Security | API returns sanitized errors | No sensitive internals are exposed |
| NFR-010 | P1 | Security | SQL injection attempts fail gracefully | System rejects malicious input |
| NFR-011 | P1 | Security | XSS payload in job description is rendered safely | Unsafe HTML is escaped |
| NFR-012 | P1 | Security | CSRF protection exists for state-changing operations | Requests without valid token are blocked |
| NFR-013 | P1 | Security | Secret keys are not exposed in frontend or source | No leaks in runtime or logs |
| NFR-014 | P1 | Security | Downloaded files are safe and not executable | Content type is correct |
| NFR-015 | P1 | UI | Application is usable under low connectivity | Graceful fallback behavior | 
| NFR-016 | P1 | UI | Input validation messages are clear | User understands what to fix |
| NFR-017 | P1 | UI | Keyboard navigation works for dashboard | Actions remain accessible without mouse |
| NFR-018 | P1 | UI | Focus order is logical in form flows | Keyboard flow is sensible |
| NFR-019 | P1 | Functional | App remains stable through long active sessions | Memory and state do not degrade unexpectedly |
| NFR-020 | P1 | Performance | Job refresh does not lock the app | User can still interact during refresh |
| NFR-021 | P1 | Performance | Standard database queries are efficient | Searches remain fast under realistic data |
| NFR-022 | P1 | Performance | Large profile data does not crash generation | It handles volume successfully |
| NFR-023 | P1 | Security | API rate-limits abuse attempts | Excessive requests are controlled |
| NFR-024 | P1 | Security | File upload or import checks are strict | Invalid formats are rejected |
| NFR-025 | P1 | Functional | Error logs are useful for debugging | No blank or meaningless exceptions |
| NFR-026 | P1 | Functional | App continues if one external service fails | Degradation strategy is enforced |
| NFR-027 | P1 | Functional | Jobs remain available after a temporary backend restart | Data persistence is maintained |
| NFR-028 | P1 | Security | User cannot access admin tools without privilege | Authorization is enforced |
| NFR-029 | P1 | Accessibility | Screen readers can interpret dashboard | Semantic structure is valid |
| NFR-030 | P1 | Accessibility | Color contrast is acceptable for text | Reading remains accessible |
| NFR-031 | P1 | Accessibility | Buttons and links are identifiable | Labels are not ambiguous |
| NFR-032 | P1 | Functional | Timezones are handled correctly | Dates remain accurate across user settings |
| NFR-033 | P1 | Functional | Data exports reflect correct date/time | Export output is not shifted or corrupted |
| NFR-034 | P1 | Functional | Browser back/forward navigation remains sane | State is not unexpectedly lost |
| NFR-035 | P1 | Functional | App shows loading states during async work | User knows work is in progress |
| NFR-036 | P1 | Functional | Long-running task is cancellable if supported | User can stop or rerun it |
| NFR-037 | P1 | Functional | Retry logic works for network or temporary service errors | System recovers gracefully |
| NFR-038 | P1 | Functional | Cache invalidation works when profile updates | stale data is not served |
| NFR-039 | P1 | Functional | App functions with large numbers of recorded jobs | No index or query explosion |
| NFR-040 | P1 | Functional | System logs remain readable | Operators can debug real issues |

## 3.12 AI Budget, Provider Limits, and Degradation

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| AI-001 | P0 | Functional | A deterministic rule decides a case | Result is produced without an LLM call or usage charge |
| AI-002 | P0 | Functional | Local semantic model scores a supported job | Score is returned without hosted LLM usage |
| AI-003 | P0 | Functional | Tier 2 reasoning runs with available budget | Result and request/token usage are recorded |
| AI-004 | P0 | Functional | Daily request budget is exhausted mid-batch | LLM tasks pause; collection and local scoring continue |
| AI-005 | P0 | Functional | Daily token budget is exhausted before request cap | Token limit stops new calls and explains the deferral |
| AI-006 | P0 | Functional | Monthly budget is exhausted | LLM work waits for reset; non-LLM workflow remains available |
| AI-007 | P0 | Integration | Provider returns rate-limit response | Retry-after/backoff is honored and calls remain bounded |
| AI-008 | P1 | Integration | Provider returns temporary server error | Bounded retry occurs, then task is queued with a failure state |
| AI-009 | P1 | Negative | Provider returns malformed or empty completion | Output is rejected and never treated as trusted content |
| AI-010 | P0 | Security | Provider key is missing | Non-LLM fallback works and dependent features report unavailable |
| AI-011 | P0 | Security | Provider key is invalid | Secret is not exposed; useful local processing continues |
| AI-012 | P1 | Security | Provider key is rotated | New key is used after reload without logging either value |
| AI-013 | P1 | Functional | Usage approaches configured limit | Dashboard warning reflects actual remaining usage |
| AI-014 | P1 | Functional | Budget forecast has no historical data | UI indicates insufficient history rather than false precision |
| AI-015 | P1 | Functional | High- and low-priority LLM tasks compete | Configured task priority controls execution order |
| AI-016 | P1 | Functional | Low-priority work is deferred | Work remains queued and can run in a later budget window |
| AI-017 | P1 | Functional | Equivalent job is processed again | Valid cache hit avoids redundant provider usage |
| AI-018 | P1 | Functional | Cached analysis is past its validity period | Stale analysis is refreshed or labeled stale |
| AI-019 | P1 | Regression | Profile changes after analysis is cached | Profile-dependent cached result is invalidated |
| AI-020 | P1 | Regression | Job description changes after analysis is cached | Changed input does not reuse an incompatible result |
| AI-021 | P1 | Functional | Completed calls add usage records | Dashboard totals reconcile with the usage ledger |
| AI-022 | P1 | Edge | Provider omits usage fields | Record is marked incomplete, not silently counted as zero |
| AI-023 | P1 | Regression | Usage event is delivered twice | Duplicate event does not double-count usage |
| AI-024 | P1 | Functional | User retries a failed generation | Retry is logged separately and respects remaining budget |
| AI-025 | P1 | Regression | Service restarts after budget exhaustion | Usage and reset boundary persist across restart |
| AI-026 | P1 | Edge | Daily usage period crosses midnight | Counter resets at the configured timezone boundary |
| AI-027 | P1 | Edge | System timezone changes during a budget period | Accounting remains consistent and auditable |
| AI-028 | P1 | Functional | Per-task model selection is configured | Each task uses an allowed model or documented fallback |
| AI-029 | P1 | Negative | Unsupported model is configured | Validation reports the invalid setting clearly |
| AI-030 | P0 | Security | Job text contains prompt-injection instructions | Untrusted text cannot override system instructions or policies |
| AI-031 | P0 | Security | LLM output asks to submit an application | Model output alone cannot authorize or trigger submission |
| AI-032 | P0 | Security | LLM output invents a resume claim | Claim is blocked or flagged before approval |
| AI-033 | P1 | Resilience | Provider is unavailable for an entire scan | Tier 0/1 work completes and dependent work remains queued |
| AI-034 | P1 | Negative | LLM response violates required output schema | Validation rejects it and records a controlled failure |
| AI-035 | P1 | Performance | Large batch contains a limited top-N LLM set | Calls stay within configured per-run limit |

## 3.13 Scheduler, Configuration, and Runtime Controls

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| OPS-001 | P0 | Functional | Scheduler starts with the application | Exactly one configured scheduler instance runs |
| OPS-002 | P0 | Regression | Service restarts with a scheduled scan pending | Schedule resumes without duplicate jobs |
| OPS-003 | P1 | Functional | User pauses scheduled collection | Future scans stop and existing data remains intact |
| OPS-004 | P1 | Functional | User resumes scheduled collection | Next eligible scan follows configured schedule |
| OPS-005 | P1 | Concurrency | Manual scan starts during scheduled scan | Work is serialized or safely deduplicated |
| OPS-006 | P1 | Functional | User cancels a long scan | Cancellation is recorded and completed work remains valid |
| OPS-007 | P1 | Resilience | Scan exceeds its time limit | It terminates or is marked timed out without wedging later scans |
| OPS-008 | P1 | Edge | Scheduled time crosses daylight-saving transition | Run follows configured timezone policy |
| OPS-009 | P1 | Functional | Scheduler timezone changes | Future runs use new timezone without unexpected replay |
| OPS-010 | P1 | Recovery | Process crashes with a task marked active | Stale task is detected and safely resumed or retried |
| OPS-011 | P1 | Concurrency | Two scheduler triggers arrive together | One logical run is created or collision is reported safely |
| OPS-012 | P1 | Negative | Schedule expression is malformed | Validation identifies the setting and prevents unsafe startup |
| OPS-013 | P1 | Functional | Valid configuration is loaded | Defaults and overrides resolve to documented effective values |
| OPS-014 | P0 | Negative | Required setting has the wrong type | Startup fails clearly or uses an explicitly safe default |
| OPS-015 | P0 | Security | Configuration contains a secret | Secret is masked in UI, logs, and errors |
| OPS-016 | P1 | Functional | Excluded-country list changes | Updated rules apply across collection and scoring paths |
| OPS-017 | P1 | Functional | User changes residence country | Search scope updates while permanent exclusions remain enforced |
| OPS-018 | P1 | Functional | Daily application cap changes | New cap applies before the next submission attempt |
| OPS-019 | P1 | Functional | User disables a job source | Source is skipped and preference persists after restart |
| OPS-020 | P0 | Security | Dry-run mode is enabled | No external submission occurs; intended action is marked simulated |
| OPS-021 | P0 | Regression | Dry-run mode is disabled | Explicit per-application approval is still required |
| OPS-022 | P1 | Functional | User starts or stops scheduler in dashboard | Displayed state agrees with actual scheduler state |
| OPS-023 | P1 | Concurrency | Configuration changes during active task | Active task uses a consistent snapshot; later task uses new values |
| OPS-024 | P1 | Negative | Configuration contains unknown keys | Unknown keys follow documented warn/ignore policy |
| OPS-025 | P1 | Functional | Optional configuration is absent | Safe defaults load and are visible where relevant |

## 3.14 Backup, Restore, and Portability

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| REC-001 | P0 | Functional | User creates a full backup | Database, profile, resumes, PDFs, and required metadata are included |
| REC-002 | P0 | Recovery | Valid backup is restored into an empty instance | Profiles, jobs, applications, and documents are recovered consistently |
| REC-003 | P0 | Recovery | Backup is restored over existing data | Replace/merge behavior is explained before destructive changes |
| REC-004 | P0 | Negative | Backup archive is corrupt | Restore is rejected and current data remains unchanged |
| REC-005 | P1 | Negative | Required database file is missing from archive | Restore reports missing component without partial overwrite |
| REC-006 | P1 | Performance | Backup contains many generated documents | Archive completes and integrity checks pass |
| REC-007 | P1 | Functional | User downloads a backup | Filename, timestamp, and completion status are correct |
| REC-008 | P1 | Security | Backup contains personal data | Download and storage follow configured access protections |
| REC-009 | P0 | Portability | Backup is restored on another supported machine | Paths are portable and documents remain accessible |
| REC-010 | P1 | Migration | Backup uses an older schema version | Migration succeeds or restore provides a clear upgrade path |
| REC-011 | P1 | Recovery | Restore is interrupted | Active state is preserved or rollback is performed |
| REC-012 | P1 | Concurrency | Backup runs while database writes occur | Backup is consistent and database integrity check passes |
| REC-013 | P1 | Security | User exports profile as JSON | Export includes supported profile data and excludes secrets |
| REC-014 | P1 | Functional | User imports valid profile JSON | Values import with preview and validation |
| REC-015 | P1 | Negative | Imported JSON has invalid types or fields | Errors are reported without corrupting current profile |
| REC-016 | P1 | Concurrency | User requests backup while one is running | Duplicate operation is blocked or safely queued |
| REC-017 | P1 | Security | User verifies backup integrity | Checksum or equivalent confirms archive integrity |
| REC-018 | P1 | Regression | Restored application has historical status changes | Audit history remains linked and ordered |
| REC-019 | P1 | Functional | Backup excludes disposable caches | Restore does not depend on temporary cache files |
| REC-020 | P1 | Regression | Backup includes document/application relationships | Applications reference the correct resume and letter versions |

## 3.15 Deployment, Startup, and Environment Portability

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| DEP-001 | P0 | Integration | App starts in private cloud deployment | Health endpoint becomes ready and dashboard is reachable |
| DEP-002 | P0 | Security | Deployment is configured as private | Unauthenticated public access is denied |
| DEP-003 | P1 | Integration | App starts on supported local Windows setup | Required services initialize and dashboard is available |
| DEP-004 | P1 | Recovery | Cloud service restarts or sleeps | Persistent user data remains available after restart |
| DEP-005 | P0 | Functional | Persistent cloud storage is configured | Database and documents survive restart/redeployment |
| DEP-006 | P1 | Negative | Persistent storage is absent or read-only | App reports storage problem instead of silently using ephemeral data |
| DEP-007 | P1 | Security | Required environment variables are present | Runtime config loads without printing secret values |
| DEP-008 | P0 | Security | Required secret is missing | Service fails closed or disables the dependent feature safely |
| DEP-009 | P1 | Functional | Database directory does not exist | Startup creates it with appropriate permissions |
| DEP-010 | P1 | Negative | Database path is not writable | Startup reports a useful storage error and does not claim healthy status |
| DEP-011 | P1 | Functional | Health probe runs during startup | It distinguishes starting, ready, and unhealthy states |
| DEP-012 | P1 | Resilience | LLM is down during health probe | Core service remains healthy when fallback is operating |
| DEP-013 | P1 | Migration | New release starts against existing database | Migration completes without losing user data |
| DEP-014 | P0 | Recovery | Deployment update fails during startup | Recovery path is available and data remains intact |
| DEP-015 | P1 | Security | Deployment logs are inspected | No API keys, resume contents, or personal answers are logged |
| DEP-016 | P1 | Integration | App binds to platform-provided port | Service is reachable on the assigned port |
| DEP-017 | P1 | Functional | Local model cache is absent at startup | Model downloads or disables per documented policy with clear status |
| DEP-018 | P1 | Performance | Cold start loads semantic model | Startup meets target or exposes a clear warming state |
| DEP-019 | P1 | Resilience | Free cloud resource limit is approached | Noncritical work is throttled without corrupting persistent data |
| DEP-020 | P1 | Portability | User selects local fallback mode | Supported core workflows operate locally with same stored state |

## 3.16 Privacy, Retention, and Data Lifecycle

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| PRIV-001 | P0 | Security | Protected application data is requested without authentication | Access is denied |
| PRIV-002 | P0 | Privacy | User requests profile/data deletion | Defined data is removed or anonymized and completion is confirmed |
| PRIV-003 | P1 | Privacy | User deletes a job linked to an application | Dependency and audit-retention behavior is explained and consistent |
| PRIV-004 | P1 | Privacy | User deletes a generated resume version | File and references are handled without deleting unrelated versions |
| PRIV-005 | P1 | Functional | Retention period is configured for old listings | Expired records follow that policy |
| PRIV-006 | P1 | Security | User exports personal data | Export is readable and excludes provider secrets |
| PRIV-007 | P1 | Security | Profile fields are sent to hosted AI | Only permitted/minimized fields are transmitted |
| PRIV-008 | P1 | Security | User disables external LLM processing | No new profile or job content is sent to provider |
| PRIV-009 | P0 | Security | Logs are inspected for sensitive data | Logs do not expose resume text, credentials, or tokens |
| PRIV-010 | P1 | Security | User clears browser session | Session credentials are removed or invalidated |
| PRIV-011 | P1 | Security | Protected request follows session expiration | Request is denied and session is not silently renewed |
| PRIV-012 | P1 | Security | Job content contains hostile instructions | It is treated as untrusted and cannot alter settings/profile |
| PRIV-013 | P1 | Consistency | Export occurs during concurrent profile edits | Export is consistent and has a generation timestamp |
| PRIV-014 | P1 | Privacy | Profile is deleted but application history is retained | Configured retention choice is followed and disclosed |
| PRIV-015 | P1 | Security | Backup archive is accessed by an unauthorized person | Documented encryption/access controls protect its contents |
| PRIV-016 | P1 | Privacy | User deletes cached AI results | Cache is removed without deleting source job records |
| PRIV-017 | P0 | Security | Public dashboard URL is guessed | Private deployment requires authentication/access control |
| PRIV-018 | P1 | Privacy | Retention period expires | Eligible data is deleted/anonymized and action is auditable |
| PRIV-019 | P1 | Security | User enters a secret in a profile field | UI warns or masks as appropriate; value is not logged |
| PRIV-020 | P1 | Regression | Privacy setting changes while work is queued | Queued work observes the new setting or is safely cancelled |

## 3.17 External Integrations, Rate Limits, and Data Contracts

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| INT-001 | P1 | Integration | Source returns valid documented payload | Adapter maps fields to canonical job model |
| INT-002 | P1 | Integration | Source adds an unknown response field | Adapter ignores or preserves it safely |
| INT-003 | P1 | Integration | Source removes a required field | Affected records are rejected and source health is reported |
| INT-004 | P1 | Integration | Source responds with HTTP 429 | Retry guidance is honored and attempts are capped |
| INT-005 | P1 | Integration | Source responds with HTTP 401/403 | Authorization/block state is recorded without aggressive retries |
| INT-006 | P1 | Resilience | Source responds with HTTP 5xx | Bounded backoff occurs; other adapters continue |
| INT-007 | P1 | Resilience | Source request times out | Timeout is recorded and other sources still run |
| INT-008 | P0 | Security | Source redirects to private/local network address | Request is blocked to prevent server-side request forgery |
| INT-009 | P1 | Security | Source URL uses unsupported scheme | URL is rejected before network access |
| INT-010 | P1 | Security | Source returns oversized response | Response is bounded and safely rejected or truncated |
| INT-011 | P1 | Integration | API results require pagination | Pages are fetched once within configured limit |
| INT-012 | P1 | Resilience | Pagination token repeats or loops | Adapter detects loop and stops without duplicating records |
| INT-013 | P1 | Integration | API response uses unexpected encoding | Content is decoded safely or marked invalid |
| INT-014 | P1 | Integration | External response has unexpected content type | Adapter rejects safely with source-specific diagnostic |
| INT-015 | P1 | Resilience | Network drops during response | Partial record is not committed as complete |
| INT-016 | P1 | Regression | External record changes between scans | Canonical record updates and meaningful history is retained |
| INT-017 | P1 | Integration | Email application draft is prepared | Recipient, subject, attachments, and body match reviewed material |
| INT-018 | P0 | Security | Email integration is configured without application approval | No email is sent |
| INT-019 | P0 | Safety | Browser automation encounters changed form structure | No blind submission occurs; job moves to manual intervention |
| INT-020 | P1 | Regression | Duplicate external confirmation event arrives | Application remains unique and confirmation handling is idempotent |

## 3.18 Observability, Audit, and Operational Recovery

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| OBS-001 | P0 | Audit | Job scan starts and completes | Run ID, times, source outcomes, and final state are recorded |
| OBS-002 | P1 | Audit | One source fails in multi-source run | Failure is attributed to source and summary remains accurate |
| OBS-003 | P1 | Audit | User changes critical setting | Change and time are logged without recording secret values |
| OBS-004 | P0 | Audit | User approves an application | Approval, job, document versions, and timestamp are linked |
| OBS-005 | P0 | Audit | Submission attempt occurs | Event records live/dry-run mode and result |
| OBS-006 | P1 | Audit | Application status changes manually | Old/new states, time, and change source are recorded |
| OBS-007 | P1 | Resilience | Log storage reaches configured limit | Rotation occurs without stopping critical workflow |
| OBS-008 | P1 | Security | Error contains internal provider/database details | User message is sanitized and secrets are absent from logs |
| OBS-009 | P1 | Recovery | Background task crashes | Task is marked failed and remains inspectable/retryable |
| OBS-010 | P1 | Recovery | App restarts with unfinished task | Recovery prevents duplicate side effects and exposes task state |
| OBS-011 | P0 | Safety | User retries task with external side effect | Idempotency prevents duplicate application submission |
| OBS-012 | P1 | Monitoring | Queue backlog metric is requested | Metric reflects persisted pending work, not stale memory |
| OBS-013 | P0 | Recovery | Database integrity check detects corruption | App provides recovery guidance and avoids destructive repair |
| OBS-014 | P1 | Audit | Audit history is queried after many events | Events remain ordered and correctly linked |
| OBS-015 | P1 | Functional | User filters operational logs by run ID | Only events from the selected run are shown |

## 3.19 Upgrade, Migration, and Release Readiness

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| REL-001 | P0 | Regression | Fresh install initializes current schema | Required tables and indexes are available |
| REL-002 | P0 | Migration | Existing supported database is upgraded | Profile, jobs, applications, and documents are preserved |
| REL-003 | P0 | Negative | Migration encounters invalid legacy data | Upgrade stops safely and identifies affected data |
| REL-004 | P1 | Regression | Migration runs a second time | It is idempotent or reports already applied |
| REL-005 | P0 | Recovery | Migration fails midway | Database can be restored from pre-migration backup |
| REL-006 | P1 | Compatibility | Older client reads newer API response | Compatibility policy is followed and unknown fields fail safely |
| REL-007 | P1 | Regression | API validation error occurs | Response uses standard structured error format |
| REL-008 | P1 | Security | Release starts with development mode disabled | Production-safe settings are active |
| REL-009 | P0 | Security | Production configuration enables debug mode | Deployment check blocks or prominently warns |
| REL-010 | P1 | Smoke | Post-deployment smoke checks run | Health, dashboard, profile, and job-list checks pass |
| REL-011 | P0 | Safety | Release approval-gate smoke test runs | Unapproved job cannot invoke live submission |
| REL-012 | P1 | Recovery | Release is rolled back | Service starts and data compatibility is verified |
| REL-013 | P1 | Regression | Dependency update changes transitive package | Build and tests expose incompatibility before release |
| REL-014 | P1 | Security | Dependency audit finds high-severity issue | Release process flags issue for remediation or risk acceptance |
| REL-015 | P1 | Process | Future-only feature has no implementation | Its cases are marked Not Run/Not Applicable, never falsely passed |

---

## 3.20 Multi-Factor Confidence, Eligibility, Submission Tracking & Analytics (v2.1)

| ID | Priority | Type | Scenario | Expected Result |
|---|---|---|---|---|
| CONF-001 | P0 | Functional | A job is assessed by the multi-factor engine | Confidence is a 0-100 blend of role fit, skill coverage, eligibility, company quality, freshness, and completeness |
| CONF-002 | P0 | Functional | Each confidence factor is stored with a detail string | The dashboard can explain every factor in plain language |
| CONF-003 | P1 | Functional | A strong BA match is scored | Role-fit factor is high and confidence label is "Strong/Excellent match" |
| CONF-004 | P1 | Negative | An unrelated role is scored | Role-fit is low and confidence label is "Weak match" |
| CONF-005 | P0 | Functional | Confidence is deterministic | The same inputs always produce the same confidence value |
| CONF-006 | P1 | Edge | A job lists no skills | Skill coverage uses a neutral value and does not crash |
| CONF-007 | P1 | Edge | A job has no posted date | Freshness is neutral (50) and does not crash |
| CONF-008 | P2 | Functional | A job has a very recent posted date | Freshness factor is high |
| CONF-009 | P2 | Functional | A job is 30+ days old | Freshness factor decays toward 0 |
| ELIG-001 | P0 | Functional | An eligible remote job is assessed | Eligibility is high and label is "Fully eligible" |
| ELIG-002 | P0 | Functional | A job blocked by the location policy is assessed | Eligibility is 0 and label is "Not eligible" |
| ELIG-003 | P1 | Functional | A review-status job is assessed | Eligibility is reduced and a manual-check reason is shown |
| ELIG-004 | P1 | Functional | A hybrid job is assessed with remote preference | A small penalty is applied vs. fully remote |
| ELIG-005 | P1 | Functional | An on-site job is assessed with remote preference | A larger penalty is applied |
| ELIG-006 | P1 | Functional | Salary is below the configured floor | A penalty is applied and a reason is shown |
| ELIG-007 | P2 | Edge | Salary is missing | No salary penalty is applied and no crash occurs |
| SUBM-001 | P0 | Functional | User approves a job with an apply link | Application status becomes "submitted", a resume PDF is generated, and a submission record with timestamp is stored |
| SUBM-002 | P0 | Functional | User approves a job without an apply link | Application status becomes "ready" with a clear next-step message |
| SUBM-003 | P0 | Functional | Approve returns a submission object | The response includes status, method, URL, attempts, and message |
| SUBM-004 | P1 | Functional | User re-approves an already-submitted job | Attempts increment and the record is updated, not duplicated |
| SUBM-005 | P1 | Functional | Job detail shows the submission panel | Status, message, and apply link (when present) are displayed |
| SUBM-006 | P1 | Functional | A submitted job's resume PDF is downloadable | The PDF endpoint returns a valid PDF |
| SUBM-007 | P2 | Negative | Approve is called on a missing job | A 404 is returned |
| TOP-001 | P0 | Functional | The dashboard shows the top 10 matches | The 10 highest-confidence eligible/review jobs are listed |
| TOP-002 | P1 | Functional | Top matches are ordered by confidence | Higher-confidence jobs appear first |
| TOP-003 | P1 | Functional | Job cards show confidence, eligibility %, rating, and matched skills | All four signals are visible on each card |
| RESC-001 | P0 | Functional | User clicks Re-score | All jobs are re-assessed with the current profile and counts are returned |
| RESC-002 | P1 | Functional | User edits profile then saves | Profile saves and a re-score runs automatically |
| RESC-003 | P1 | Functional | Re-score after adding a skill | Confidence for matching jobs increases |
| ANLY-001 | P0 | Functional | The Analytics view loads | Stat cards, pipeline donut, submissions bar, confidence distribution, source, work-mode, and top-companies charts render |
| ANLY-002 | P0 | Functional | Application pipeline donut reflects statuses | Submitted/Ready/Draft counts and conversion % are correct |
| ANLY-003 | P1 | Functional | Submissions chart shows the last 14 days | Daily submission counts are plotted with readable labels |
| ANLY-004 | P1 | Functional | Confidence distribution buckets are correct | Jobs are bucketed into 0-39/40-54/55-69/70-84/85-100 |
| ANLY-005 | P1 | Functional | Jobs-by-source and work-mode charts are correct | Counts match the stored jobs |
| ANLY-006 | P1 | Edge | No submissions exist yet | The submissions chart renders empty state without error |
| ANLY-007 | P1 | Edge | A submitted timestamp is naive (SQLite) | The 14-day comparison normalizes to UTC and does not error |
| MIGR-001 | P0 | Migration | An existing DB gains new columns on startup | confidence, eligibility, confidence_breakdown, and submission columns are added |
| MIGR-002 | P0 | Regression | Migration runs a second time | It is idempotent and does not error or duplicate columns |
| MIGR-003 | P1 | Regression | Existing jobs are preserved after migration | All prior jobs and applications remain intact |

---

## 4. Test Execution Readiness

This is a design-level test inventory. A test is not passed merely because the feature appears in a requirement. Before execution, connect each case to a build, concrete test data, observed result, and evidence.

### 4.1 Execution Record Fields

- Test case ID and document revision
- Build/version, environment, browser, and operating system
- Execution date, tester, and run identifier
- Preconditions and synthetic test-data identifiers
- Actual steps and observed result
- Status: Not Run / Pass / Fail / Blocked / Not Applicable
- Evidence link (screenshot, sanitized log, or run output)
- Defect ID and retest result, when applicable

### 4.2 Environment and Data Preparation

- Use an isolated test database and synthetic candidate/job data; do not use the real resume in automated runs unless specifically required.
- Use mocked or sandbox provider/source endpoints for repeatable integration tests; retain a smaller real-service smoke suite for deployment checks.
- Keep real application submission disabled in test environments. Verify approval gates with a fake ATS or email sink.
- Include fixtures for eligible remote roles, region-restricted roles, excluded-country postings, stale jobs, malformed records, duplicates, salary variants, and prompt-injection text.
- Record timezone, configured country, excluded countries, AI request/token limits, and provider/model settings for each run.
- Separate implemented MVP cases from planned features. Planned cases remain Not Run or Not Applicable until implemented.

### 4.3 Exit Gates

- Release smoke: all P0 cases for shipped scope pass, including location exclusions, truthful document generation, approval gate, persistence, and critical recovery checks.
- MVP gate: all implemented MVP P0 cases pass, with no unresolved critical/high defects in discovery-to-review workflow.
- Full-product gate: applicable P0/P1 cases pass or have an explicitly approved risk exception.
- Any real external submission test needs a separate controlled approval and must not run unattended in CI.

## 5. Coverage Summary

This test suite includes validation across the following core workflows:

- Profile creation and editing
- Resume import and data parsing
- Search preferences and exclusions
- Source collection and normalization
- Deduplication and quality filtering
- Ranking, scoring, and gating
- Resume tailoring and PDF generation
- Job review queue and approvals
- Application execution tracking
- Trust and safety checks
- Learning and analytics
- AI budget, caching, provider fallback, and rate limits
- Scheduler, configuration, and runtime controls
- Backup, restore, deployment, and portability
- Privacy, retention, auditability, and release migrations
- Security, accessibility, performance, and operational recovery

---

## 6. Recommended Execution Strategy

1. Run all P0 tests first.
2. Complete all P1 critical business flows.
3. Validate P2 future-feature scenarios in a non-blocking cycle.
4. Re-test every fix with regression cases.
5. Perform final QA sign-off after smoke and full suite pass.

---

## 7. Final Note

This document provides a comprehensive QA pack for ZEYRECUITE with 702 test-case rows, designed to support MVP verification and continued future product maturity.

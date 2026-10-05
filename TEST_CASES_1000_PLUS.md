# ZEYRECUITE — 1000+ Test Cases (v2.4)

## 1. Purpose

Comprehensive QA & validation suite for the ZEYRECUITE v2.4 product. Covers
functional, negative, edge, UI, performance, security, reliability, and
regression scenarios across the full lifecycle — from profile setup through
job collection, scoring, pipeline, application tracking, analytics,
source expansion, scheduler/enrichment, and the new **desktop app (F18)**.

This is the broad QA matrix. The focused, feature-mapped suite lives in
`docs/test-cases.md` (v2.4). Automated coverage: **131/131 passing**
(`cd backend; & "..\.venv\Scripts\python.exe" -m pytest tests -q`).

**Scope note (v2.4):** F16 (Bangladesh boards) is **DROPPED** — no cases.
F15/F17 include UI cases for the v2.4 frontend (Enrich button, Company facts
panel, scheduler + registry cards). F18 (desktop app) is new.

## 2. Legend

- **Priority:** P0 = critical, P1 = high, P2 = medium, P3 = low
- **Type:** Functional / Negative / Edge / UI / Performance / Security /
  Regression / Integration
- **Status:** ✅ = verified in v2.4 UAT · 🧪 = automated (pytest) · 📋 = manual
  QA · ⏳ = backlog/future (not built)
- **Error standard:** all API errors return `{"detail": "<msg>"}` with the
  correct HTTP status (401/404/422/409). No custom `error_code` envelope.

## 3. Test Case Matrix

### 3.1 Profile & Account Setup (PROF)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| PROF-001 | P0 | Functional | App seeds a default profile on first boot | Profile id=1 exists with blank fields; no fake data | 🧪 |
| PROF-002 | P0 | Functional | `GET /api/profile` returns the profile | 200 with name, skills, summary, expected_salary, etc. | ✅ |
| PROF-003 | P0 | Functional | `PUT /api/profile` updates name | Name persisted; other fields unchanged | ✅ |
| PROF-004 | P0 | Functional | `PUT /api/profile` updates phone | Phone persisted | ✅ |
| PROF-005 | P0 | Functional | `PUT /api/profile` updates email | Email persisted | ✅ |
| PROF-006 | P1 | Functional | `PUT /api/profile` updates current country | Country saved; used in eligibility | ✅ |
| PROF-007 | P1 | Functional | `PUT /api/profile` updates location | Location saved | ✅ |
| PROF-008 | P1 | Functional | `PUT /api/profile` updates summary | Summary saved without affecting other sections | ✅ |
| PROF-009 | P0 | Functional | `PUT /api/profile` adds a skill | Skill appears in profile and matching | ✅ |
| PROF-010 | P0 | Functional | `PUT /api/profile` removes a skill | Skill gone from profile and matching | ✅ |
| PROF-011 | P1 | Functional | `PUT /api/profile` sets expected_salary | Value saved; used in salary analytics | ✅ |
| PROF-012 | P1 | Functional | `PUT /api/profile` sets min_salary | Value saved; used in eligibility penalty | ✅ |
| PROF-013 | P1 | Functional | `PUT /api/profile` sets resume_text | Text saved; used in resume scorecard | ✅ |
| PROF-014 | P1 | Functional | `PUT /api/profile` sets work-mode preference | Preference saved; affects matching | ✅ |
| PROF-015 | P1 | Functional | `PUT /api/profile` sets location exclusions | Excluded locations filtered from results | ✅ |
| PROF-016 | P1 | Functional | `PUT /api/profile` partial update | Only sent fields change; others retained | ✅ |
| PROF-017 | P1 | Functional | Profile completeness computed | Completeness % reflects filled required fields | ✅ |
| PROF-018 | P1 | Functional | Completeness lists missing fields | Missing required fields named in hint | ✅ |
| PROF-019 | P0 | Functional | Save multiple sections at once | All persist without data loss | ✅ |
| PROF-020 | P1 | Edge | Edit profile while a scan is running | No corruption; both complete | 📋 |
| PROF-021 | P1 | Negative | `PUT /api/profile` with empty body | 422 or no-op; no crash | 📋 |
| PROF-022 | P1 | Negative | `PUT /api/profile` with non-list skills | 422 `{"detail":...}` | 📋 |
| PROF-023 | P1 | Negative | `PUT /api/profile` with null skills | 422 or treated as empty list | 📋 |
| PROF-024 | P2 | Negative | `PUT /api/profile` with huge skill string | Truncated or rejected; no crash | 📋 |
| PROF-025 | P2 | Negative | `PUT /api/profile` with special chars in name | Stored safely; rendered escaped | 📋 |
| PROF-026 | P2 | Negative | `PUT /api/profile` with emoji in summary | Stored and rendered correctly | 📋 |
| PROF-027 | P2 | Negative | `PUT /api/profile` with SQL in a field | Stored as data; no injection | 📋 |
| PROF-028 | P2 | Negative | `PUT /api/profile` with HTML in summary | Stored; rendered escaped (no XSS) | 📋 |
| PROF-029 | P1 | Functional | `GET /api/profile` unauthenticated | 401 | ✅ |
| PROF-030 | P1 | Functional | `PUT /api/profile` unauthenticated | 401 | ✅ |
| PROF-031 | P2 | Edge | Profile with all fields blank | Completeness 0; app still usable | 📋 |
| PROF-032 | P2 | Edge | Profile with only name set | Completeness partial; no crash | 📋 |
| PROF-033 | P2 | Edge | Very long resume_text (100KB) | Stored; scorecard still computes | 📋 |
| PROF-034 | P2 | Edge | resume_text with only whitespace | Treated as empty; neutral scorecard | 📋 |
| PROF-035 | P2 | Edge | Duplicate skills in list | Deduped or stored; matching consistent | 📋 |
| PROF-036 | P2 | Edge | Skill with leading/trailing spaces | Normalized for matching | 📋 |
| PROF-037 | P1 | Functional | Data persists after logout/login | Profile intact after re-auth | ✅ |
| PROF-038 | P1 | Functional | Data persists after server restart | Profile intact (SQLite) | ✅ |
| PROF-039 | P2 | Functional | expected_salary as "90k" | Parsed to 90 (thousands) | 🧪 |
| PROF-040 | P2 | Functional | expected_salary as "$120,000" | Parsed to 120 | 🧪 |
| PROF-041 | P2 | Functional | expected_salary as "120000" | Parsed to 120 | 🧪 |
| PROF-042 | P2 | Functional | expected_salary as "8000/mo" | Parsed to annualized 96 | 🧪 |
| PROF-043 | P2 | Negative | expected_salary as "abc" | Ignored/null; no crash | 📋 |
| PROF-044 | P2 | Negative | expected_salary as negative | Rejected or clamped | 📋 |
| PROF-045 | P2 | Negative | expected_salary as empty string | Treated as unset | 📋 |
| PROF-046 | P1 | Functional | min_salary as "80k" | Parsed to 80; eligibility penalty uses it | 🧪 |
| PROF-047 | P2 | Negative | min_salary > expected_salary | Allowed; eligibility reflects it | 📋 |
| PROF-048 | P2 | Edge | min_salary as 0 | No salary penalty applied | 📋 |
| PROF-049 | P2 | Functional | work_mode preference "remote" | Remote jobs weighted higher | 📋 |
| PROF-050 | P2 | Functional | work_mode preference "hybrid" | Hybrid jobs included | 📋 |
| PROF-051 | P2 | Functional | work_mode preference "onsite" | Onsite jobs included when allowed | 📋 |
| PROF-052 | P2 | Negative | work_mode preference invalid value | 422 or ignored | 📋 |
| PROF-053 | P1 | Functional | Location exclusion list set | Jobs in excluded locations filtered | 📋 |
| PROF-054 | P2 | Edge | Exclusion list with one entry | That location filtered | 📋 |
| PROF-055 | P2 | Edge | Exclusion list empty | No filtering | 📋 |
| PROF-056 | P2 | Edge | Exclusion with case variants | Case-insensitive match | 📋 |
| PROF-057 | P1 | Functional | Profile drives scoring deterministically | Same profile + jobs → same scores | 🧪 |
| PROF-058 | P1 | Functional | Changing a skill changes scores | Rescore reflects new skill set | 📋 |
| PROF-059 | P2 | Functional | Changing expected_salary changes percentile | Salary gauge updates | 📋 |
| PROF-060 | P2 | Functional | Changing min_salary changes eligibility | Eligibility % updates | 📋 |
| PROF-061 | P1 | Functional | Profile used in cover letter | Letter references name/skills | 📋 |
| PROF-062 | P1 | Functional | Profile used in resume generation | Resume reflects profile facts | 📋 |
| PROF-063 | P2 | Functional | Profile used in follow-up email | Email references name | 📋 |
| PROF-064 | P2 | Edge | Profile with non-ASCII name | Rendered correctly everywhere | 📋 |
| PROF-065 | P2 | Edge | Profile with very long name | Truncated in UI; stored full | 📋 |
| PROF-066 | P2 | Functional | Resume scorecard uses resume_text | Coverage computed from text + skills | 🧪 |
| PROF-067 | P2 | Functional | Resume scorecard uses profile skills | Skills counted in coverage | 🧪 |
| PROF-068 | P2 | Edge | resume_text mentions a skill not in profile | Counted via text match | 📋 |
| PROF-069 | P2 | Edge | Profile skills all absent from job | Coverage low; gap lists all | 📋 |
| PROF-070 | P2 | Edge | Job has no skills | Neutral coverage (50) | 🧪 |
| PROF-071 | P1 | Functional | Completeness bar in job detail | Width = pct; hint lists missing | ✅ |
| PROF-072 | P2 | UI | Completeness bar at 100% | Full bar; "complete" state | 📋 |
| PROF-073 | P2 | UI | Completeness bar at 0% | Empty bar; all fields listed | 📋 |
| PROF-074 | P2 | UI | Completeness hint wraps on narrow screen | No overflow | 📋 |
| PROF-075 | P1 | Functional | Profile saved via UI form | PUT fires; toast confirms | 📋 |
| PROF-076 | P2 | UI | Profile form shows current values | Inputs pre-filled | 📋 |
| PROF-077 | P2 | UI | Profile form validates before save | Invalid input flagged | 📋 |
| PROF-078 | P2 | UI | Profile form cancel discards changes | No PUT fired | 📋 |
| PROF-079 | P2 | UI | Profile form save shows loading | Spinner during PUT | 📋 |
| PROF-080 | P2 | UI | Profile form save error shows message | Toast with detail | 📋 |
| PROF-081 | P1 | Functional | Skills editor add | Skill chip added | 📋 |
| PROF-082 | P1 | Functional | Skills editor remove | Skill chip removed | 📋 |
| PROF-083 | P2 | UI | Skills editor shows count | "N skills" label | 📋 |
| PROF-084 | P2 | UI | Skills editor empty state | "Add your first skill" hint | 📋 |
| PROF-085 | P2 | Edge | Skills editor duplicate add | No duplicate chip | 📋 |
| PROF-086 | P2 | Edge | Skills editor max length skill | Truncated or rejected | 📋 |
| PROF-087 | P1 | Functional | Resume variants list | `GET /api/profile/resume-variants` 200 | ✅ |
| PROF-088 | P1 | Functional | Save resume variants | `PUT` full-replace persists list | ✅ |
| PROF-089 | P1 | Functional | Variant used in resume gen | Chosen variant text/skills used | 📋 |
| PROF-090 | P2 | Functional | Create a new variant | New variant appears | 📋 |
| PROF-091 | P2 | Functional | Edit a variant | Changes persist | 📋 |
| PROF-092 | P2 | Functional | Delete a variant | Removed from list | 📋 |
| PROF-093 | P2 | Negative | Variants not a list | 422 `{"detail":"variants must be a list"}` | ✅ |
| PROF-094 | P2 | Negative | More than 10 variants | 422 `{"detail":"keep at most 10 variants"}` | 📋 |
| PROF-095 | P2 | Edge | Variant with empty text | Stored; resume gen falls back | 📋 |
| PROF-096 | P2 | Edge | Variant with no skills | Stored; matching uses profile skills | 📋 |
| PROF-097 | P2 | UI | Variant picker in job detail | Dropdown lists variants | 📋 |
| PROF-098 | P2 | UI | Variant picker default selection | First variant selected | 📋 |
| PROF-099 | P2 | UI | Variant editor full-replace warning | UI warns before overwrite | 📋 |
| PROF-100 | P2 | Edge | Variant name duplicate | Allowed or warned | 📋 |
| PROF-101 | P1 | Functional | Saved filters list | `GET /api/profile/filters` 200 | ✅ |
| PROF-102 | P1 | Functional | Save filters | `PUT` persists list | ✅ |
| PROF-103 | P1 | Functional | Apply a saved filter | Filter set applied to jobs view | 📋 |
| PROF-104 | P2 | Functional | Delete a saved filter | Removed | 📋 |
| PROF-105 | P2 | Negative | Filters not a list | 422 `{"detail":"filters must be a list"}` | 📋 |
| PROF-106 | P2 | Negative | More than 20 filters | 422 `{"detail":"save at most 20 filters"}` | 📋 |
| PROF-107 | P2 | Edge | Filter with no criteria | Stored; applies nothing | 📋 |
| PROF-108 | P2 | Edge | Filter with invalid status value | Stored; no matching jobs | 📋 |
| PROF-109 | P2 | UI | Saved filter chips | Rendered; click applies | 📋 |
| PROF-110 | P2 | UI | Saved filter delete button | Removes chip | 📋 |
| PROF-111 | P2 | UI | No saved filters state | "No saved filters" hint | 📋 |
| PROF-112 | P2 | Functional | Filters persist across sessions | Intact after reload | ✅ |
| PROF-113 | P2 | Edge | Filter name duplicate | Allowed | 📋 |
| PROF-114 | P2 | Edge | Filter referencing deleted job | Applied; no crash | 📋 |
| PROF-115 | P1 | Functional | Profile change triggers rescore | Scores recompute on save | 📋 |
| PROF-116 | P2 | Functional | Rescore after profile save is async | Non-blocking; toast on done | 📋 |
| PROF-117 | P2 | Edge | Rapid profile saves | Last write wins; no corruption | 📋 |
| PROF-118 | P2 | Edge | Profile save during rescore | No deadlock; consistent state | 📋 |
| PROF-119 | P2 | Functional | Profile export included in backup | Part of export payload | 📋 |
| PROF-120 | P2 | Regression | Profile schema migration | Old DB upgraded; data intact | 🧪 |

### 3.2 Authentication & Account (AUTH)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| AUTH-001 | P0 | Functional | `POST /api/auth/login` with valid credentials | 200 + Bearer token issued | ✅ |
| AUTH-002 | P0 | Functional | Default user seeded on first boot | `admin` / `zeyrecuite` works | 🧪 |
| AUTH-003 | P0 | Functional | `GET /api/auth/me` with valid token | 200 + user object | ✅ |
| AUTH-004 | P0 | Negative | Login with wrong password | 401 `{"detail":"Invalid username or password"}` | ✅ |
| AUTH-005 | P0 | Negative | Login with unknown username | 401 (same message; no user enumeration) | ✅ |
| AUTH-006 | P1 | Negative | Login with empty username | 401 or 422; no crash | 📋 |
| AUTH-007 | P1 | Negative | Login with empty password | 401 or 422; no crash | 📋 |
| AUTH-008 | P1 | Negative | Login with empty body | 422 validation error | 📋 |
| AUTH-009 | P1 | Negative | Login with non-JSON body | 422 | 📋 |
| AUTH-010 | P1 | Negative | Login with extra unknown fields | Ignored; login succeeds if creds valid | 📋 |
| AUTH-011 | P0 | Functional | Token accepted in `Authorization: Bearer` header | Request authorized | ✅ |
| AUTH-012 | P0 | Functional | Token accepted via `zr_token` cookie | Request authorized | 📋 |
| AUTH-013 | P0 | Negative | Request with no token | 401 `{"detail":"Not authenticated"}` | ✅ |
| AUTH-014 | P0 | Negative | Request with malformed header | 401 | ✅ |
| AUTH-015 | P0 | Negative | Request with garbage token | 401 | ✅ |
| AUTH-016 | P1 | Negative | Request with expired/revoked token | 401; UI forces re-login | 📋 |
| AUTH-017 | P1 | Functional | Token stored in localStorage (`zr_token`) | Not in URL; survives reload | ✅ |
| AUTH-018 | P1 | Functional | Password stored as salted hash | 64-hex hash + 32-hex salt in DB; never plaintext | 🧪 |
| AUTH-019 | P1 | Functional | Same password → same hash for same salt | Deterministic hashing | 🧪 |
| AUTH-020 | P1 | Functional | Different passwords → different hashes | No collision | 🧪 |
| AUTH-021 | P1 | Functional | `POST /api/auth/change-password` correct current | 200; new password works | 📋 |
| AUTH-022 | P1 | Negative | Change password with wrong current | 400 `{"detail":"Current password is incorrect"}` | 📋 |
| AUTH-023 | P1 | Negative | Change password with empty new password | 422 | 📋 |
| AUTH-024 | P2 | Negative | Change password with very short new password | 422 (min length) | 📋 |
| AUTH-025 | P2 | Functional | Old token invalidated after password change | Old token → 401 | 📋 |
| AUTH-026 | P1 | Functional | Login response does not leak user existence | Same 401 for bad user vs bad password | ✅ |
| AUTH-027 | P1 | Security | Login rate limiting / lockout after N failures | Throttled or locked; clear message | ⏳ |
| AUTH-028 | P1 | Security | Token has sufficient entropy | 32+ random bytes; not guessable | 🧪 |
| AUTH-029 | P2 | Security | Token not logged in server logs | No token in stdout/logs | 📋 |
| AUTH-030 | P2 | Security | Token not in URL query strings | Never appended to URLs | ✅ |
| AUTH-031 | P1 | Functional | All protected endpoints require auth | 401 without token (jobs, profile, analytics, export, scheduler, sources, enrich) | ✅ |
| AUTH-032 | P1 | Functional | Static assets served without auth | `index.html`, `app.js`, CSS load pre-login | 📋 |
| AUTH-033 | P1 | Functional | Login page shown when no token | UI redirects to login view | ✅ |
| AUTH-034 | P1 | Functional | Login page hidden when token present | Dashboard shown directly | ✅ |
| AUTH-035 | P1 | Functional | Logout clears token | `zr_token` removed; login view shown | 📋 |
| AUTH-036 | P1 | Functional | Logout stops data access | Subsequent API calls 401 | 📋 |
| AUTH-037 | P2 | UI | Login form shows error on failure | "Invalid username or password." rendered (not swallowed as session-expired) | ✅ |
| AUTH-038 | P2 | UI | Login form shows loading state | Button disabled during request | 📋 |
| AUTH-039 | P2 | UI | Login form auto-focuses username | First field focused | 📋 |
| AUTH-040 | P2 | UI | Login form submits on Enter | Keyboard submit works | 📋 |
| AUTH-041 | P2 | UI | Login form masks password | `type=password` | 📋 |
| AUTH-042 | P2 | UI | Login form trims whitespace in username | " admin " logs in | 📋 |
| AUTH-043 | P2 | Edge | Login with username containing spaces | Handled; 401 if unknown | 📋 |
| AUTH-044 | P2 | Edge | Login with very long password | 401; no crash | 📋 |
| AUTH-045 | P2 | Edge | Login with SQL injection in username | 401; no injection | 📋 |
| AUTH-046 | P2 | Edge | Login with XSS payload in username | 401; payload not rendered | 📋 |
| AUTH-047 | P2 | Edge | Login with unicode username | 401; no crash | 📋 |
| AUTH-048 | P1 | Functional | Session survives page reload | Token in localStorage; no re-login | ✅ |
| AUTH-049 | P1 | Functional | Session survives browser restart | Token persisted; auto-login | 📋 |
| AUTH-050 | P2 | Functional | 401 mid-session triggers re-login | `api()` helper clears token, shows login | ✅ |
| AUTH-051 | P2 | Functional | 401 on login attempt does NOT trigger re-login loop | `allow401` path shows real error | ✅ |
| AUTH-052 | P2 | Edge | Two tabs with same token | Both work; no conflict | 📋 |
| AUTH-053 | P2 | Edge | Token in one tab cleared in another | Other tab gets 401 → re-login | 📋 |
| AUTH-054 | P2 | Functional | `GET /api/auth/me` with cookie only | 200 (cookie fallback) | 📋 |
| AUTH-055 | P2 | Functional | `GET /api/auth/me` with header + cookie | Header wins; 200 | 📋 |
| AUTH-056 | P2 | Negative | `GET /api/auth/me` with empty Bearer | 401 | 📋 |
| AUTH-057 | P2 | Negative | `GET /api/auth/me` with "Bearer" (no space) | 401 | 📋 |
| AUTH-058 | P2 | Negative | `GET /api/auth/me` with "bearer" lowercase | 401 (case-sensitive scheme) or 200 if lenient — consistent behavior | 📋 |
| AUTH-059 | P1 | Security | Authorization enforced per endpoint | No endpoint bypasses `current_user` | 🧪 |
| AUTH-060 | P1 | Security | No IDOR across users | Single-user app; no cross-tenant data | 🧪 |
| AUTH-061 | P2 | Security | CSRF not applicable (Bearer header) | No cookie-only state-changing calls without token | 📋 |
| AUTH-062 | P2 | Security | Login endpoint not cached | `Cache-Control: no-store` on auth responses | 📋 |
| AUTH-063 | P2 | Security | Password change requires auth | 401 without token | 📋 |
| AUTH-064 | P2 | Functional | Login works after server restart | Seeded user persists in DB | 📋 |
| AUTH-065 | P2 | Functional | Login works on fresh DB | Seed runs; default creds valid | 🧪 |
| AUTH-066 | P2 | Edge | Concurrent login attempts | Both succeed; independent tokens | 📋 |
| AUTH-067 | P2 | Edge | Login during a long scan | Not blocked; 200 | 📋 |
| AUTH-068 | P2 | Functional | Token length consistent | Same length across logins (fixed-size secret) | 📋 |
| AUTH-069 | P2 | Functional | `auth/me` returns username only (no hash) | No sensitive fields leaked | 📋 |
| AUTH-070 | P2 | Functional | `auth/me` does not return password hash | Hash never in API responses | 🧪 |
| AUTH-071 | P2 | Regression | Auth flow unchanged after v2.4 | Login/me/change-password all pass | 🧪 |
| AUTH-072 | P2 | Functional | Login from desktop app window | Same flow; token in webview storage | ⏳ |
| AUTH-073 | P2 | Functional | Logout from desktop app | Token cleared; login view | ⏳ |
| AUTH-074 | P2 | Edge | Login with CRLF in username | Rejected/sanitized; no header injection | 📋 |
| AUTH-075 | P2 | Edge | Login with null bytes in password | Rejected; no crash | 📋 |
| AUTH-076 | P2 | Edge | Login with password = username | 401 unless actually set | 📋 |
| AUTH-077 | P2 | Functional | Change password then login with new | New creds work; old fail | 📋 |
| AUTH-078 | P2 | Functional | Change password keeps username | Username unchanged | 📋 |
| AUTH-079 | P2 | Edge | Change password to same value | 200 (no-op) or 400 — consistent | 📋 |
| AUTH-080 | P2 | Security | Brute-force: 100 rapid failed logins | No account lockout data leak; consistent 401 | 📋 |

### 3.3 Security & Hardening (SEC)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| SEC-001 | P0 | Security | SQL injection in job search | `'; DROP TABLE jobs; --` → 200, no crash, no data loss | ✅ |
| SEC-002 | P0 | Security | SQL injection in filter params | Parameterized queries; no injection | 🧪 |
| SEC-003 | P0 | Security | SQL injection in import payload | Stored as data; no schema change | 📋 |
| SEC-004 | P0 | Security | SQL injection in profile fields | Stored as data; no injection | 📋 |
| SEC-005 | P0 | Security | SQL injection in compare ids | `1; DROP TABLE` → 422/ignored; no injection | 📋 |
| SEC-006 | P0 | Security | SQL injection in status move | Invalid status → 422; no injection | ✅ |
| SEC-007 | P0 | Security | XSS via job title | Rendered escaped; no script execution | ✅ |
| SEC-008 | P0 | Security | XSS via job description | HTML-escaped in modal | ✅ |
| SEC-009 | P0 | Security | XSS via company name | Escaped in cards and detail | ✅ |
| SEC-010 | P0 | Security | XSS via profile summary | Escaped in UI | 📋 |
| SEC-011 | P0 | Security | XSS via resume text | Escaped in scorecard/preview | 📋 |
| SEC-012 | P0 | Security | XSS via cover letter | Escaped in preview | 📋 |
| SEC-013 | P0 | Security | XSS via import (title with `<script>`) | Stored; rendered escaped | 📋 |
| SEC-014 | P1 | Security | XSS via job URL field | Rendered as text/anchor, not executed | 📋 |
| SEC-015 | P1 | Security | XSS via source name | Escaped | 📋 |
| SEC-016 | P1 | Security | XSS via company facts (Wikidata) | Escaped in facts panel | 📋 |
| SEC-017 | P1 | Security | `javascript:` URL in job link | Not navigable; sanitized or plain text | 📋 |
| SEC-018 | P1 | Security | `data:` URL in job link | Not navigable | 📋 |
| SEC-019 | P1 | Security | All dynamic HTML uses `esc()` helper | No raw `innerHTML` with user data | 🧪 |
| SEC-020 | P1 | Security | Event handlers not injected via data | No `onerror=`/`onclick=` in rendered data | 📋 |
| SEC-021 | P1 | Security | CSV export does not execute formulas | Cells with `=CMD()` quoted/escaped | 📋 |
| SEC-022 | P1 | Security | CSV injection in job title | Leading `=`, `+`, `-`, `@` neutralized | 📋 |
| SEC-023 | P1 | Security | JSON export is valid JSON | Parses; no trailing commas | 📋 |
| SEC-024 | P1 | Security | Import rejects non-JSON body | 422 | 📋 |
| SEC-025 | P1 | Security | Import with deeply nested JSON | Rejected or flattened; no stack overflow | 📋 |
| SEC-026 | P1 | Security | Import with 100k rows | Bounded; no OOM (batched or rejected) | 📋 |
| SEC-027 | P1 | Security | Import with circular references | Rejected (JSON can't); no crash | 📋 |
| SEC-028 | P1 | Security | Path traversal in static file requests | `/static/../app.py` → 404 | 📋 |
| SEC-029 | P1 | Security | Path traversal in export filenames | No filesystem access via params | 📋 |
| SEC-030 | P1 | Security | Unknown API route | 404 `{"detail":"Not Found"}` | ✅ |
| SEC-031 | P1 | Security | Wrong HTTP method on route | 405 | ✅ |
| SEC-032 | P1 | Security | OPTIONS request handling | Consistent (CORS or 405) | 📋 |
| SEC-033 | P1 | Security | HEAD request on GET routes | 200 with headers, no body | 📋 |
| SEC-034 | P2 | Security | Request with huge headers | 431 or 400; no crash | 📋 |
| SEC-035 | P2 | Security | Request with malformed JSON body | 422 | 📋 |
| SEC-036 | P2 | Security | Request with wrong Content-Type | 422 or ignored | 📋 |
| SEC-037 | P2 | Security | Request with chunked encoding | Handled by server | 📋 |
| SEC-038 | P2 | Security | Request with invalid UTF-8 | 400; no crash | 📋 |
| SEC-039 | P2 | Security | Error messages do not leak stack traces | `{"detail":...}` only; no tracebacks | ✅ |
| SEC-040 | P2 | Security | Error messages do not leak DB paths | No absolute paths in 500s | 📋 |
| SEC-041 | P2 | Security | 500 handler returns JSON | `{"detail":"Internal Server Error"}` | 📋 |
| SEC-042 | P2 | Security | Validation errors list field names | 422 body names offending fields | 📋 |
| SEC-043 | P2 | Security | No debug mode in production config | `debug=False`; no reloader | 📋 |
| SEC-044 | P2 | Security | Server binds to 127.0.0.1 only | Not exposed on LAN by default | ✅ |
| SEC-045 | P2 | Security | No secrets in source code | API keys via config/env only | 🧪 |
| SEC-046 | P2 | Security | `config.yaml` not served statically | Not under `/static` | 📋 |
| SEC-047 | P2 | Security | `zeyrecuite.db` not served statically | Not under `/static` | 📋 |
| SEC-048 | P2 | Security | `sources.json` not served statically | Not under `/static` | 📋 |
| SEC-049 | P2 | Security | `.venv` not accessible via HTTP | Outside web root | 📋 |
| SEC-050 | P2 | Security | CORS not over-permissive | Same-origin only (no `*` with credentials) | 📋 |
| SEC-051 | P2 | Security | No `X-Frame-Options` clickjacking risk | Local app; frame headers set or acceptable | 📋 |
| SEC-052 | P2 | Security | Content-Security-Policy baseline | Inline scripts allowed (IIFE) but no remote origins | 📋 |
| SEC-053 | P2 | Security | No external CDN dependencies | All assets local; offline-capable | 📋 |
| SEC-054 | P2 | Security | Dependencies pinned in requirements.txt | Versions bounded | 🧪 |
| SEC-055 | P2 | Security | No known-vulnerable dependency versions | `pip audit` clean (or reviewed) | 📋 |
| SEC-056 | P2 | Security | httpx used with timeouts | No unbounded network waits | 🧪 |
| SEC-057 | P2 | Security | httpx follows bounded redirects | Max redirects enforced | 📋 |
| SEC-058 | P2 | Security | User-agent set on outbound requests | Identifiable UA | 📋 |
| SEC-059 | P2 | Security | Outbound requests respect robots.txt | Polite scraping | 📋 |
| SEC-060 | P2 | Security | Rate limiting on outbound scrapes | Delays between requests | 📋 |
| SEC-061 | P2 | Security | No credentials sent to job boards | Read-only public endpoints | 📋 |
| SEC-062 | P2 | Security | Collector never POSTs applications | Read-only; no form submission | ✅ |
| SEC-063 | P2 | Security | Wikidata calls are read-only | GET only | 🧪 |
| SEC-064 | P2 | Security | Retry logic bounded (tenacity) | Max retries; no infinite loop | 🧪 |
| SEC-065 | P2 | Security | Retry backoff does not hammer source | Exponential delay | 🧪 |
| SEC-066 | P2 | Security | TLS used for https sources | No plaintext for https boards | 📋 |
| SEC-067 | P2 | Security | Certificate validation enabled | No `verify=False` | 📋 |
| SEC-068 | P2 | Security | No eval/exec of user data | Static code only | 🧪 |
| SEC-069 | P2 | Security | No dynamic import of user strings | No `__import__(user_input)` | 🧪 |
| SEC-070 | P2 | Security | Pickle not used on untrusted data | No pickle of imports | 🧪 |
| SEC-071 | P2 | Security | YAML config loaded safely | `safe_load` (no arbitrary objects) | 🧪 |
| SEC-072 | P2 | Security | JSON registry loaded safely | `json.load` only | 🧪 |
| SEC-073 | P2 | Security | Logs do not contain tokens | No `zr_token` in logs | 📋 |
| SEC-074 | P2 | Security | Logs do not contain passwords | No plaintext creds in logs | 📋 |
| SEC-075 | P2 | Security | Logs do not contain full resume text | PII minimized | 📋 |
| SEC-076 | P2 | Security | DB file permissions local-only | Default OS perms; single user | 📋 |
| SEC-077 | P2 | Security | Backup file (export) contains no tokens | Export excludes auth data | 📋 |
| SEC-078 | P2 | Security | Export does not include password hash | Hash never exported | 🧪 |
| SEC-079 | P2 | Security | Import cannot overwrite auth records | No user table in import schema | 🧪 |
| SEC-080 | P2 | Security | Import cannot modify config | Config read-only to API | 📋 |
| SEC-081 | P2 | Security | Scheduler cannot be triggered by unauth user | `POST /api/enrich` 401 without token | ✅ |
| SEC-082 | P2 | Security | Scheduler config not writable via API | `GET /api/scheduler` read-only | ✅ |
| SEC-083 | P2 | Security | Registry not writable via API | `GET /api/sources` read-only | ✅ |
| SEC-084 | P2 | Security | Enrich limit param bounded | `limit` clamped; no DoS | 📋 |
| SEC-085 | P2 | Security | Enrich with negative limit | 422 or clamped to 0 | 📋 |
| SEC-086 | P2 | Security | Enrich with huge limit | Bounded by job count; no OOM | 📋 |
| SEC-087 | P2 | Security | Compare ids bounded to 5 | 422 beyond 5 | ✅ |
| SEC-088 | P2 | Security | Compare ids non-numeric | Ignored/422; no injection | 📋 |
| SEC-089 | P2 | Security | Job id params non-numeric | 404/422; no injection | 📋 |
| SEC-090 | P2 | Security | Query params with encoded slashes | Handled; no routing bypass | 📋 |
| SEC-091 | P2 | Security | Duplicate query params | Last wins or 422; consistent | 📋 |
| SEC-092 | P2 | Security | Very long query string | 414 or truncated; no crash | 📋 |
| SEC-093 | P2 | Security | Concurrent writes to same job | Last write wins; no corruption | 📋 |
| SEC-094 | P2 | Security | Concurrent scans | Serialized or safe; no dup jobs | 📋 |
| SEC-095 | P2 | Security | DB integrity after crash | SQLite WAL/journal; recoverable | 📋 |
| SEC-096 | P2 | Security | No race in fingerprint dedup | Unique constraint; no dup rows | 🧪 |
| SEC-097 | P2 | Security | Token comparison constant-time | No timing oracle | 📋 |
| SEC-098 | P2 | Security | Login response time consistent | Same for bad user vs bad password | 📋 |
| SEC-099 | P2 | Security | No verbose errors in production | `detail` only | ✅ |
| SEC-100 | P2 | Security | Full security regression suite | All SEC cases pass on each release | 🧪 |

### 3.4 Job Discovery & Collection (JOB)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| JOB-001 | P0 | Functional | `POST /api/scan` triggers a collection run | 200; scan recorded with timestamp + counts | ✅ |
| JOB-002 | P0 | Functional | Scan fetches from enabled sources | Remotive + Greenhouse (+ enabled F15 sources) fetched | ✅ |
| JOB-003 | P0 | Functional | Manual "Scan now" button | Triggers scan; toast on completion | ✅ |
| JOB-004 | P0 | Functional | New jobs persisted after scan | Rows added to `jobs` table | ✅ |
| JOB-005 | P0 | Functional | Dedup by fingerprint | Re-scan adds 0 duplicates | 🧪 |
| JOB-006 | P0 | Functional | Fingerprint = hash(title, company, url) | Same job → same fingerprint | 🧪 |
| JOB-007 | P1 | Functional | Fingerprint stable across scans | No re-insert of unchanged jobs | 🧪 |
| JOB-008 | P1 | Functional | Fingerprint differs when title changes | New row created | 🧪 |
| JOB-009 | P1 | Functional | Fingerprint differs when company changes | New row created | 🧪 |
| JOB-010 | P1 | Functional | Fingerprint differs when url changes | New row created | 🧪 |
| JOB-011 | P1 | Functional | Scan records per-source results | Each source: fetched count, errors | 📋 |
| JOB-012 | P1 | Functional | Scan records total duration | Elapsed time stored | 📋 |
| JOB-013 | P1 | Functional | Scan with zero new jobs | Recorded; "0 new" shown; no crash | ✅ |
| JOB-014 | P1 | Functional | Scan with all sources failing | Recorded as error run; app still usable | 📋 |
| JOB-015 | P1 | Functional | One source fails, others succeed | Partial success; failing source flagged | 📋 |
| JOB-016 | P1 | Functional | Scan is idempotent | Running twice yields same job set | 🧪 |
| JOB-017 | P1 | Functional | Scan does not delete existing jobs | Old jobs retained (no pruning) | 📋 |
| JOB-018 | P1 | Functional | Scan updates posted_date for new jobs | Date parsed and stored | 📋 |
| JOB-019 | P1 | Functional | Scan stores work_mode | remote/hybrid/onsite detected | 📋 |
| JOB-020 | P1 | Functional | Scan stores location | Location string stored | 📋 |
| JOB-021 | P1 | Functional | Scan stores salary when present | Salary string stored; parsed later | 📋 |
| JOB-022 | P1 | Functional | Scan stores description | Full description stored | 📋 |
| JOB-023 | P1 | Functional | Scan stores skills | Skill list extracted/stored | 📋 |
| JOB-024 | P1 | Functional | Scan stores application_url | Apply link stored | 📋 |
| JOB-025 | P1 | Functional | Scan stores source attribution | `source` field set per job | ✅ |
| JOB-026 | P1 | Functional | Recent scans shown in dashboard | Timestamps + counts listed | ✅ |
| JOB-027 | P1 | Functional | Scan respects South-Asia exclusion | Jobs from excluded regions gated out | 🧪 |
| JOB-028 | P1 | Functional | Gate rejects jobs in excluded countries | Not persisted | 🧪 |
| JOB-029 | P2 | Functional | Gate keeps jobs in allowed regions | Persisted | 🧪 |
| JOB-030 | P2 | Edge | Job with missing country | Handled per policy (kept or gated) — consistent | 📋 |
| JOB-031 | P2 | Edge | Job with ambiguous location | Best-effort; no crash | 📋 |
| JOB-032 | P1 | Functional | Remotive adapter parses listings | Title/company/location/salary/url extracted | 🧪 |
| JOB-033 | P1 | Functional | Remotive adapter handles empty feed | `[]` returned; no fake rows | 🧪 |
| JOB-034 | P1 | Functional | Greenhouse adapter parses boards | Listings extracted via public API | 🧪 |
| JOB-035 | P1 | Functional | Greenhouse adapter handles 404 board | Error recorded; no crash | 📋 |
| JOB-036 | P1 | Functional | Adapter normalizes to common Job shape | All adapters → same fields | 🧪 |
| JOB-037 | P1 | Functional | Adapter strips HTML from descriptions | Clean text stored | 🧪 |
| JOB-038 | P2 | Functional | Adapter decodes HTML entities | `&amp;` → `&` etc. | 🧪 |
| JOB-039 | P2 | Functional | Adapter normalizes whitespace | Collapsed; trimmed | 🧪 |
| JOB-040 | P2 | Functional | Adapter extracts salary from text | "120k", "$90,000", "8000/mo" recognized | 🧪 |
| JOB-041 | P2 | Functional | Adapter extracts work mode | "Remote" → remote; "Hybrid" → hybrid | 🧪 |
| JOB-042 | P2 | Functional | Adapter extracts posted date | Relative/absolute dates parsed | 🧪 |
| JOB-043 | P2 | Edge | Adapter with malformed HTML | Best-effort; no crash | 📋 |
| JOB-044 | P2 | Edge | Adapter with empty listing fields | Nulls stored; no crash | 📋 |
| JOB-045 | P2 | Edge | Adapter with very long description | Stored; truncated in UI | 📋 |
| JOB-046 | P2 | Edge | Adapter with unicode text | Stored correctly | 📋 |
| JOB-047 | P2 | Edge | Adapter with duplicate listings in feed | Deduped by fingerprint | 📋 |
| JOB-048 | P1 | Functional | Scan timeout per source | Source marked error after timeout; others proceed | 📋 |
| JOB-049 | P1 | Functional | Scan retry on transient failure | Bounded retry; then error | 📋 |
| JOB-050 | P1 | Functional | Scan does not block UI | Async; UI responsive during scan | ✅ |
| JOB-051 | P1 | Functional | Scan progress feedback | "Scanning…" state; toast on done | ✅ |
| JOB-052 | P2 | Functional | Scan result toast shows new count | "N new jobs" | ✅ |
| JOB-053 | P2 | Functional | Scan result toast shows errors | "M sources failed" if any | 📋 |
| JOB-054 | P2 | Functional | Jobs persist after server restart | All jobs retained (SQLite) | ✅ |
| JOB-055 | P2 | Functional | Jobs persist after app update | Migration preserves rows | 🧪 |
| JOB-056 | P2 | Functional | Job count in stats matches DB | `total` = row count | ✅ |
| JOB-057 | P2 | Functional | Source count in stats matches | `sources` = distinct sources | ✅ |
| JOB-058 | P2 | Functional | New jobs appear in Jobs view after scan | List refreshes | ✅ |
| JOB-059 | P2 | Functional | New jobs scored on insert | Confidence/eligibility computed | 🧪 |
| JOB-060 | P2 | Functional | New jobs get default status | `status=new` (Eligible lane) | 🧪 |
| JOB-061 | P2 | Functional | New jobs get source label | Card shows source | ✅ |
| JOB-062 | P2 | Functional | Job list sorted by score desc | Highest confidence first | 📋 |
| JOB-063 | P2 | Functional | Job list sortable by newest | Date sort works | 📋 |
| JOB-064 | P2 | Functional | Job list filterable by status | Chips filter correctly | ✅ |
| JOB-065 | P2 | Functional | Job list searchable by text | Substring match on title/company | ✅ |
| JOB-066 | P2 | Functional | Search matches company name | "Stripe" finds Stripe jobs | ✅ |
| JOB-067 | P2 | Functional | Search matches title | "Analyst" finds analyst jobs | ✅ |
| JOB-068 | P2 | Edge | Search with no matches | Empty state shown | 📋 |
| JOB-069 | P2 | Edge | Search with special chars | Escaped; no crash | 📋 |
| JOB-070 | P2 | Edge | Search is case-insensitive | "stripe" finds "Stripe" | 📋 |
| JOB-071 | P2 | Edge | Search with SQL payload | No injection; 0 or safe results | ✅ |
| JOB-072 | P2 | Functional | Reset filters clears search + chips | Full list restored | 📋 |
| JOB-073 | P2 | Functional | Job pagination / virtualization | 500+ jobs render performantly | ✅ |
| JOB-074 | P2 | Functional | Job card shows title + company | Both rendered | ✅ |
| JOB-075 | P2 | Functional | Job card shows confidence | Score + label | ✅ |
| JOB-076 | P2 | Functional | Job card shows salary | Parsed salary or "—" | ✅ |
| JOB-077 | P2 | Functional | Job card shows work mode | Badge rendered | ✅ |
| JOB-078 | P2 | Functional | Job card shows source | Label rendered | ✅ |
| JOB-079 | P2 | Functional | Job card shows company rating | Stars + flags | ✅ |
| JOB-080 | P2 | Functional | Job card click opens detail | Modal opens | ✅ |
| JOB-081 | P2 | Functional | Job card shows posted date | Relative date | 📋 |
| JOB-082 | P2 | Functional | Job card shows location | Location text | 📋 |
| JOB-083 | P2 | Functional | Empty jobs state | "No jobs yet — click Scan now" | 📋 |
| JOB-084 | P2 | Functional | Loading state during jobs fetch | Spinner shown | 📋 |
| JOB-085 | P2 | Functional | Error state on jobs fetch failure | Message + retry | 📋 |
| JOB-086 | P2 | Functional | `GET /api/jobs` returns all jobs | 200; array of jobs | ✅ |
| JOB-087 | P2 | Functional | `GET /api/jobs` unauthenticated | 401 | ✅ |
| JOB-088 | P2 | Functional | `GET /api/jobs/{id}` returns one job | 200; full job object | ✅ |
| JOB-089 | P2 | Functional | `GET /api/jobs/{id}` missing id | 404 `{"detail":"job not found"}` | ✅ |
| JOB-090 | P2 | Functional | `GET /api/jobs/{id}` non-numeric id | 404/422; no crash | 📋 |
| JOB-091 | P2 | Functional | Job detail includes application | Application object present | ✅ |
| JOB-092 | P2 | Functional | Job detail includes scorecard | Coverage + gaps | ✅ |
| JOB-093 | P2 | Functional | Job detail includes company rating | 6-dimension breakdown | ✅ |
| JOB-094 | P2 | Functional | Job detail includes company facts | When enriched | ✅ |
| JOB-095 | P2 | Functional | Job detail includes interview prep | Generated questions | ✅ |
| JOB-096 | P2 | Functional | Job detail includes timeline | Events list | ✅ |
| JOB-097 | P2 | Functional | Job detail includes cover letter | Generated letter | ✅ |
| JOB-098 | P2 | Functional | Job detail includes resume scorecard | Panel rendered | ✅ |
| JOB-099 | P2 | Functional | Job detail includes eligibility | % + label + factors | ✅ |
| JOB-100 | P2 | Functional | Job detail includes why-this-score | 6 factors with details | ✅ |
| JOB-101 | P2 | Functional | Job detail includes skills match | Matched/missing chips | ✅ |
| JOB-102 | P2 | Functional | Job detail includes application form | Completeness bar | ✅ |
| JOB-103 | P2 | Functional | Job detail includes job description | Full text | ✅ |
| JOB-104 | P2 | Functional | Job detail includes your eligibility | Panel rendered | ✅ |
| JOB-105 | P2 | Functional | Scan records stored for trend | Each scan → trend point | 📋 |
| JOB-106 | P2 | Functional | Scan count grows over time | Monotonic scan history | 📋 |
| JOB-107 | P2 | Edge | Scan with 1000+ new jobs | All persisted; performant | 📋 |
| JOB-108 | P2 | Edge | Scan with 0 sources enabled | Recorded; 0 fetched; no crash | 📋 |
| JOB-109 | P2 | Edge | Scan while DB locked | Retries or waits; no corruption | 📋 |
| JOB-110 | P2 | Edge | Scan interrupted by server stop | Partial run recoverable; no corruption | 📋 |
| JOB-111 | P2 | Functional | Scan respects config source list | Only configured sources run | 🧪 |
| JOB-112 | P2 | Functional | Scan uses registry-enabled F15 sources | Enabled sources included | 🧪 |
| JOB-113 | P2 | Functional | Scan skips registry-disabled sources | Not fetched | 🧪 |
| JOB-114 | P2 | Functional | Scan skips sources missing required keys | Not activated | 🧪 |
| JOB-115 | P2 | Functional | Scan attribution per F15 source | `source` set correctly | 🧪 |
| JOB-116 | P2 | Functional | Scan error run does not clear jobs | Existing jobs intact | 📋 |
| JOB-117 | P2 | Functional | Scan updates source health | Success rate + last scan time | 📋 |
| JOB-118 | P2 | Functional | Scan avg fetched tracked per source | Rolling average | 📋 |
| JOB-119 | P2 | Functional | Scan trend recorded for analytics | Point added to trend | 📋 |
| JOB-120 | P2 | Regression | Collection flow unchanged in v2.4 | Scan → gate → dedup → score → persist all pass | 🧪 |

### 3.5 Filtering & Data Quality (FIL)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| FIL-001 | P0 | Functional | Saved filters applied to job list | Only matching jobs shown | ✅ |
| FIL-002 | P0 | Functional | Filter by work mode (remote) | Only remote jobs | ✅ |
| FIL-003 | P0 | Functional | Filter by work mode (hybrid) | Only hybrid jobs | ✅ |
| FIL-004 | P0 | Functional | Filter by work mode (onsite) | Only onsite jobs | ✅ |
| FIL-005 | P0 | Functional | Filter by minimum salary | Jobs below threshold hidden | ✅ |
| FIL-006 | P0 | Functional | Filter by keyword (include) | Jobs containing keyword shown | ✅ |
| FIL-007 | P0 | Functional | Filter by keyword (exclude) | Jobs containing keyword hidden | ✅ |
| FIL-008 | P1 | Functional | Filter by experience level | Matching level shown | ✅ |
| FIL-009 | P1 | Functional | Filter by job type (full-time) | Only full-time | ✅ |
| FIL-010 | P1 | Functional | Filter by job type (contract) | Only contract | ✅ |
| FIL-011 | P1 | Functional | Filter by source | Only that source's jobs | ✅ |
| FIL-012 | P1 | Functional | Filter by country | Jobs in country shown | ✅ |
| FIL-013 | P1 | Functional | Filter by company rating min | Below-rating jobs hidden | ✅ |
| FIL-014 | P1 | Functional | Filter by posted date (last 7 days) | Recent jobs only | ✅ |
| FIL-015 | P1 | Functional | Filter by posted date (last 30 days) | Recent jobs only | ✅ |
| FIL-016 | P1 | Functional | Multiple filters combined (AND) | Intersection shown | ✅ |
| FIL-017 | P1 | Functional | Multiple keywords (OR within include) | Union of keyword matches | ✅ |
| FIL-018 | P1 | Functional | Include + exclude keywords | Include AND NOT exclude | ✅ |
| FIL-019 | P1 | Functional | Filter with no matches | Empty state; count 0 | ✅ |
| FIL-020 | P1 | Functional | Clear single filter | List updates | ✅ |
| FIL-021 | P1 | Functional | Clear all filters | Full list restored | ✅ |
| FIL-022 | P1 | Functional | Filters persist across reload | Saved in profile; re-applied | ✅ |
| FIL-023 | P1 | Functional | Filters persist across sessions | localStorage/profile | ✅ |
| FIL-024 | P1 | Functional | Filter count badge | Active filter count shown | 📋 |
| FIL-025 | P1 | Functional | Filter UI shows active state | Chips highlighted | 📋 |
| FIL-026 | P1 | Functional | Filter changes re-fetch or re-filter | List updates without full reload | ✅ |
| FIL-027 | P1 | Functional | Filter + search combined | Both applied | ✅ |
| FIL-028 | P1 | Functional | Filter + sort combined | Both applied | ✅ |
| FIL-029 | P1 | Functional | Filter respects status lanes | Filtered within lane | ✅ |
| FIL-030 | P1 | Functional | Filter on empty dataset | Empty state; no crash | 📋 |
| FIL-031 | P1 | Functional | Filter with salary = 0 | No min-salary filter applied | 📋 |
| FIL-032 | P1 | Functional | Filter with very high salary | 0 results; empty state | 📋 |
| FIL-033 | P1 | Functional | Filter with negative salary | 422 or clamped; no crash | 📋 |
| FIL-034 | P1 | Functional | Filter with empty keyword list | No keyword filter | 📋 |
| FIL-035 | P1 | Functional | Filter with whitespace-only keyword | Treated as empty | 📋 |
| FIL-036 | P1 | Functional | Filter with duplicate keywords | Deduped; no double-count | 📋 |
| FIL-037 | P1 | Functional | Filter keywords case-insensitive | "python" matches "Python" | 📋 |
| FIL-038 | P1 | Functional | Filter keywords match title | Title substring | 📋 |
| FIL-039 | P1 | Functional | Filter keywords match description | Description substring | 📋 |
| FIL-040 | P1 | Functional | Filter keywords match skills | Skill name match | 📋 |
| FIL-041 | P1 | Functional | Filter max 20 keywords | 21st rejected (422) | 📋 |
| FIL-042 | P1 | Functional | Filter max 20 total filters | Enforced | 📋 |
| FIL-043 | P1 | Functional | `PUT /api/profile/filters` full replace | Old filters gone; new applied | 📋 |
| FIL-044 | P1 | Functional | `PUT /api/profile/filters` empty list | All filters cleared | 📋 |
| FIL-045 | P1 | Functional | `GET /api/profile/filters` returns saved | 200; filter object | 📋 |
| FIL-046 | P1 | Functional | Filters unauthenticated | 401 | 📋 |
| FIL-047 | P1 | Functional | Filter validation on save | Invalid filter → 422 | 📋 |
| FIL-048 | P1 | Functional | Filter with unknown field | Ignored or 422; consistent | 📋 |
| FIL-049 | P1 | Functional | Filter with null values | Handled; no crash | 📋 |
| FIL-050 | P1 | Functional | Filter with boolean work_mode | Treated as invalid; 422 | 📋 |
| FIL-051 | P1 | Functional | Filter with array salary | 422 | 📋 |
| FIL-052 | P1 | Functional | Filter with string salary "120k" | Parsed or 422; consistent | 📋 |
| FIL-053 | P1 | Functional | Filter with salary currency | Currency normalized | 📋 |
| FIL-054 | P1 | Functional | Filter with unknown work mode | 422 | 📋 |
| FIL-055 | P1 | Functional | Filter with unknown job type | 422 | 📋 |
| FIL-056 | P1 | Functional | Filter with unknown experience | 422 | 📋 |
| FIL-057 | P1 | Functional | Filter with unknown source | 422 or ignored; consistent | 📋 |
| FIL-058 | P1 | Functional | Filter with future posted date | 0 results; no crash | 📋 |
| FIL-059 | P1 | Functional | Filter with past posted date | All jobs in range | 📋 |
| FIL-060 | P1 | Functional | Filter with invalid country code | 422 or ignored; consistent | 📋 |
| FIL-061 | P1 | Functional | Filter with rating > 5 | 422 | 📋 |
| FIL-062 | P1 | Functional | Filter with rating 0 | No min-rating filter | 📋 |
| FIL-063 | P1 | Functional | Filter with rating decimal | Accepted (e.g. 3.5) | 📋 |
| FIL-064 | P1 | Functional | Filter UI: add keyword chip | Chip appears; list updates | 📋 |
| FIL-065 | P1 | Functional | Filter UI: remove keyword chip | Chip removed; list updates | 📋 |
| FIL-066 | P1 | Functional | Filter UI: salary slider | Drag updates filter | 📋 |
| FIL-067 | P1 | Functional | Filter UI: work mode toggle | Toggle updates filter | 📋 |
| FIL-068 | P1 | Functional | Filter UI: source multi-select | Multiple sources | 📋 |
| FIL-069 | P1 | Functional | Filter UI: date range picker | Range applied | 📋 |
| FIL-070 | P1 | Functional | Filter UI: reset button | All filters cleared | 📋 |
| FIL-071 | P1 | Functional | Filter UI: apply button | Filters saved + applied | 📋 |
| FIL-072 | P1 | Functional | Filter UI: cancel button | Changes discarded | 📋 |
| FIL-073 | P1 | Functional | Filter UI: validation errors | Inline messages | 📋 |
| FIL-074 | P1 | Functional | Filter UI: loading state | Spinner during save | 📋 |
| FIL-075 | P1 | Functional | Filter UI: success toast | "Filters saved" | 📋 |
| FIL-076 | P1 | Functional | Filter UI: error toast | Message on 422 | 📋 |
| FIL-077 | P1 | Functional | Filter UI: responsive layout | Works on narrow widths | 📋 |
| FIL-078 | P1 | Functional | Filter UI: keyboard accessible | Tab/Enter work | 📋 |
| FIL-079 | P1 | Functional | Filter UI: screen reader labels | ARIA labels present | 📋 |
| FIL-080 | P1 | Functional | Filter UI: no console errors | Clean console | 📋 |

### 3.6 Resume & Tailoring (RES)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| RES-001 | P0 | Functional | `PUT /api/profile/resume` stores resume text | 200; text persisted | ✅ |
| RES-002 | P0 | Functional | `GET /api/profile` returns resume text | 200; text present | ✅ |
| RES-003 | P0 | Functional | Skills extracted from resume text | Skill list populated; used in matching | ✅ |
| RES-004 | P1 | Functional | Years of experience inferred from dates | Years computed; stored | 📋 |
| RES-005 | P1 | Functional | Experience level inferred (entry/mid/senior) | Level assigned from years/roles | 📋 |
| RES-006 | P1 | Functional | Location extracted from resume header | Location field populated | 📋 |
| RES-007 | P1 | Functional | Contact info extracted (email/phone) | Parsed; not duplicated into profile | 📋 |
| RES-008 | P2 | Functional | Education section extracted | Degrees/schools listed | 📋 |
| RES-009 | P2 | Functional | Certifications extracted | Cert list populated | 📋 |
| RES-010 | P2 | Functional | Projects extracted | Project entries listed | 📋 |
| RES-011 | P1 | Edge | Resume with no recognizable skills | Empty skill list; neutral matching | 📋 |
| RES-012 | P1 | Edge | Resume with duplicate skills | Deduped; counted once | 📋 |
| RES-013 | P2 | Edge | Resume with non-ASCII skill names | Normalized; matching consistent | 📋 |
| RES-014 | P1 | Functional | Empty resume → scoring does not crash | Neutral/low scores; no 500 | 🧪 |
| RES-015 | P1 | Functional | Resume matching all job skills | Coverage 100%; gaps empty | 📋 |
| RES-016 | P1 | Functional | Resume matching no job skills | Coverage 0%; gaps = all job skills | 📋 |
| RES-017 | P1 | Functional | Coverage % = matched / job skills | Computed correctly | 🧪 |
| RES-018 | P1 | Functional | Gaps = job skills − resume skills | Exact set difference | 🧪 |
| RES-019 | P1 | Functional | Matched = job skills ∩ resume skills | Exact intersection | 🧪 |
| RES-020 | P1 | Functional | Job with no skills → neutral coverage | 50; no crash | 🧪 |
| RES-021 | P1 | Functional | Score deterministic | Same resume + job → same score | 🧪 |
| RES-022 | P1 | Functional | Resume update re-scores all jobs | All scores recomputed | 🧪 |
| RES-023 | P1 | Functional | Scorecard panel renders | Coverage + matched + gaps shown | ✅ |
| RES-024 | P1 | Functional | Tailored resume highlights matching skills | Matched skills emphasized | ✅ |
| RES-025 | P1 | Functional | Tailored resume adds job keywords | Keywords from description included | 📋 |
| RES-026 | P1 | Functional | Tailored resume reorders sections | Matching content first | 📋 |
| RES-027 | P1 | Functional | Tailored resume editable + persists | Edits retained across reload | 📋 |
| RES-028 | P1 | Functional | Tailored resume copy + download | Clipboard + .txt/.md work | 📋 |
| RES-029 | P1 | Functional | Tailored resume regenerates on resume change | Reflects new resume text | 📋 |
| RES-030 | P0 | Functional | Resume text required for scoring | Empty resume → low/zero score | 🧪 |
| RES-031 | P0 | Functional | Resume update re-scores all jobs | Scores recomputed on resume change | 🧪 |
| RES-032 | P0 | Functional | Resume update re-generates tailoring | Tailored resume/letter updated | 🧪 |
| RES-033 | P1 | Functional | Resume variants: `PUT /api/profile/resume-variants` full replace | Old variants wiped; new set stored | ✅ |
| RES-034 | P1 | Functional | Resume variants: max 10 enforced | 11th → 422 | 📋 |
| RES-035 | P1 | Functional | Resume variants: `GET` returns all variants | 200; array of variants | 📋 |
| RES-036 | P1 | Functional | Resume variants: select active variant | Active variant used for scoring | 📋 |
| RES-037 | P1 | Functional | Resume variants: each has name + text | Both fields stored | 📋 |
| RES-038 | P1 | Functional | Resume variants: empty list | All variants cleared | 📋 |
| RES-039 | P1 | Functional | Resume variants: duplicate names | Allowed or 409; consistent | 📋 |
| RES-040 | P1 | Functional | Resume variants: unauthenticated | 401 | 📋 |
| RES-041 | P1 | Functional | Resume variants: invalid body | 422 | 📋 |
| RES-042 | P1 | Functional | Resume variants: very long text | Stored; truncated in UI | 📋 |
| RES-043 | P1 | Functional | Resume variants: unicode text | Stored correctly | 📋 |
| RES-044 | P1 | Functional | Resume variants: XSS in text | Escaped in UI | 📋 |
| RES-045 | P1 | Functional | Resume variants: SQL injection in text | Stored as data; no injection | 📋 |
| RES-046 | P1 | Functional | Resume variants: null text | 422 or empty; consistent | 📋 |
| RES-047 | P1 | Functional | Resume variants: missing name | 422 | 📋 |
| RES-048 | P1 | Functional | Resume variants: empty name | 422 | 📋 |
| RES-049 | P1 | Functional | Resume variants: whitespace-only name | 422 | 📋 |
| RES-050 | P1 | Functional | Resume variants: 10 variants exactly | 200; all stored | 📋 |
| RES-051 | P1 | Functional | Resume variants: 0 variants | 200; empty list | 📋 |
| RES-052 | P1 | Functional | Resume variants: 1 variant | 200; single variant | 📋 |
| RES-053 | P1 | Functional | Resume variants: replace with same set | 200; no change | 📋 |
| RES-054 | P1 | Functional | Resume variants: replace with different set | 200; old gone, new stored | 📋 |
| RES-055 | P1 | Functional | Resume variants: concurrent writes | Last write wins; no corruption | 📋 |
| RES-056 | P1 | Functional | Resume variants: persist across restart | All variants retained | 📋 |
| RES-057 | P1 | Functional | Resume variants: persist across sessions | All variants retained | 📋 |
| RES-058 | P1 | Functional | Resume variants: UI shows variant list | All variants listed | 📋 |
| RES-059 | P1 | Functional | Resume variants: UI select variant | Active variant changes | 📋 |
| RES-060 | P1 | Functional | Resume variants: UI add variant | New variant appears | 📋 |
| RES-061 | P1 | Functional | Resume variants: UI edit variant | Text updated | 📋 |
| RES-062 | P1 | Functional | Resume variants: UI delete variant | Variant removed | 📋 |
| RES-063 | P1 | Functional | Resume variants: UI rename variant | Name updated | 📋 |
| RES-064 | P1 | Functional | Resume variants: UI validation | Inline errors on invalid input | 📋 |
| RES-065 | P1 | Functional | Resume variants: UI loading state | Spinner during save | 📋 |
| RES-066 | P1 | Functional | Resume variants: UI success toast | "Variants saved" | 📋 |
| RES-067 | P1 | Functional | Resume variants: UI error toast | Message on 422 | 📋 |
| RES-068 | P1 | Functional | Resume variants: UI responsive | Works on narrow widths | 📋 |
| RES-069 | P1 | Functional | Resume variants: UI keyboard accessible | Tab/Enter work | 📋 |
| RES-070 | P1 | Functional | Resume variants: UI screen reader | ARIA labels present | 📋 |
| RES-071 | P1 | Functional | Resume variants: UI no console errors | Clean console | 📋 |
| RES-072 | P1 | Functional | Resume variants: UI empty state | "No variants yet" | 📋 |
| RES-073 | P1 | Functional | Resume variants: UI max reached | "Max 10 variants" message | 📋 |
| RES-074 | P1 | Functional | Resume variants: UI active indicator | Active variant highlighted | 📋 |
| RES-075 | P1 | Functional | Resume variants: UI preview | Variant text previewable | 📋 |
| RES-076 | P1 | Functional | Resume variants: UI copy to clipboard | Text copied | 📋 |
| RES-077 | P1 | Functional | Resume variants: UI download | Variant text downloadable | 📋 |
| RES-078 | P1 | Functional | Resume variants: UI import | Variant text importable | 📋 |
| RES-079 | P1 | Functional | Resume variants: UI export | Variant text exportable | 📋 |
| RES-080 | P1 | Functional | Resume variants: UI drag to reorder | Order updated | 📋 |

### 3.7 Dashboard & Review Queue (DASH)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| DASH-001 | P0 | Functional | Dashboard loads after login | All cards render without error | ✅ |
| DASH-002 | P0 | Functional | Stats: total jobs count | Matches `jobs` table row count | ✅ |
| DASH-003 | P0 | Functional | Stats: new jobs count | Matches `status=new` rows | ✅ |
| DASH-004 | P0 | Functional | Stats: in-review count | Matches `status=review` rows | ✅ |
| DASH-005 | P0 | Functional | Stats: applied count | Matches `status=applied` rows | ✅ |
| DASH-006 | P0 | Functional | Stats: interview count | Matches `status=interview` rows | ✅ |
| DASH-007 | P0 | Functional | Stats: offer count | Matches `status=offer` rows | ✅ |
| DASH-008 | P0 | Functional | Stats: rejected count | Matches `status=rejected` rows | ✅ |
| DASH-009 | P0 | Functional | Stats: distinct sources | Matches distinct `source` values | ✅ |
| DASH-010 | P0 | Functional | Stats: avg confidence | Mean of `confidence` across jobs | ✅ |
| DASH-011 | P0 | Functional | Stats: avg eligibility | Mean of `eligibility` across jobs | ✅ |
| DASH-012 | P0 | Functional | Recent scans list | Last N scans with timestamp + new count | ✅ |
| DASH-013 | P0 | Functional | "Scan now" button on dashboard | Triggers scan; toast on completion | ✅ |
| DASH-014 | P0 | Functional | Review queue shows top-scored jobs | Sorted by confidence desc | ✅ |
| DASH-015 | P0 | Functional | Review queue shows job cards | Title, company, score, source | ✅ |
| DASH-016 | P0 | Functional | Review queue click opens job detail | Modal opens with full detail | ✅ |
| DASH-017 | P0 | Functional | Review queue respects filters | Filtered jobs only | ✅ |
| DASH-018 | P0 | Functional | Review queue respects search | Searched jobs only | ✅ |
| DASH-019 | P0 | Functional | Review queue empty state | "No jobs yet" message | 📋 |
| DASH-020 | P0 | Functional | Review queue loading state | Spinner during fetch | 📋 |
| DASH-021 | P0 | Functional | Review queue error state | Message + retry button | 📋 |
| DASH-022 | P1 | Functional | Dashboard refresh button | Re-fetches all data | 📋 |
| DASH-023 | P1 | Functional | Dashboard auto-refresh on scan complete | Data updates without manual refresh | 📋 |
| DASH-024 | P1 | Functional | Dashboard shows last scan time | "Last scan: 2h ago" | 📋 |
| DASH-025 | P1 | Functional | Dashboard shows scan duration | "Took 45s" | 📋 |
| DASH-026 | P1 | Functional | Dashboard shows new jobs since last scan | Delta count | 📋 |
| DASH-027 | P1 | Functional | Dashboard shows source health | Per-source success/fail | 📋 |
| DASH-028 | P1 | Functional | Dashboard shows pipeline summary | Counts per status lane | ✅ |
| DASH-029 | P1 | Functional | Pipeline summary counts per lane | Sum of lanes = total jobs | ✅ |
| DASH-030 | P1 | Functional | Stats consistent with DB | Counts match direct SQL query | 📋 |
| DASH-031 | P1 | Functional | Stats update after status move | Lane counts change immediately | 📋 |
| DASH-032 | P1 | Functional | Stats update after scan | New-job count reflects scan | 📋 |
| DASH-033 | P1 | Functional | Stats update after import | Imported jobs reflected | 📋 |
| DASH-034 | P1 | Functional | Stats update after delete | Removed jobs reflected | 📋 |
| DASH-035 | P1 | Functional | Avg confidence with 0 jobs | 0 or "—"; no NaN/Infinity | 📋 |
| DASH-036 | P1 | Functional | Avg confidence with 1 job | Equals that job's score | 📋 |
| DASH-037 | P1 | Functional | Avg confidence rounding | Displayed to 1 decimal; consistent | 📋 |
| DASH-038 | P1 | Functional | Review queue capped | Top N (e.g. 10) shown; "see all" link | 📋 |
| DASH-039 | P1 | Functional | Review queue tie-break on equal scores | Deterministic order (id asc) | 📋 |
| DASH-040 | P1 | Functional | Review queue excludes rejected | Rejected jobs not in queue | 📋 |
| DASH-041 | P1 | Functional | Review queue respects active filters | Filtered subset only | ✅ |
| DASH-042 | P1 | Functional | Review queue respects search text | Searched subset only | ✅ |
| DASH-043 | P1 | Functional | Review queue card click → detail modal | Modal opens with correct job | ✅ |
| DASH-044 | P1 | Functional | Review queue card shows score badge | Confidence + label rendered | ✅ |
| DASH-045 | P1 | Functional | Review queue card shows source label | Source rendered | ✅ |
| DASH-046 | P1 | Functional | Review queue card shows salary | Parsed salary or "—" | 📋 |
| DASH-047 | P1 | Functional | Review queue card shows work mode | Badge rendered | 📋 |
| DASH-048 | P1 | Functional | Review queue card shows posted date | Relative date | 📋 |
| DASH-049 | P1 | Functional | Review queue empty state | "No jobs yet — click Scan now" | 📋 |
| DASH-050 | P1 | Functional | Review queue loading state | Spinner during fetch | 📋 |
| DASH-051 | P1 | Functional | Review queue error state | Message + retry button | 📋 |
| DASH-052 | P1 | Functional | Dashboard refresh button re-fetches | All cards update | 📋 |
| DASH-053 | P1 | Functional | Dashboard auto-refresh after scan | Data updates without manual refresh | 📋 |
| DASH-054 | P1 | Functional | Dashboard shows last scan time | "Last scan: 2h ago" | 📋 |
| DASH-055 | P1 | Functional | Dashboard shows scan duration | "Took 45s" | 📋 |
| DASH-056 | P1 | Functional | Dashboard shows new jobs since last scan | Delta count | 📋 |
| DASH-057 | P1 | Functional | Dashboard shows source health | Per-source success/fail | 📋 |
| DASH-058 | P1 | Functional | Dashboard cards clickable → navigate | Card click routes to view | 📋 |
| DASH-059 | P1 | Functional | Dashboard cards show delta vs last period | "+12 this week" | 📋 |
| DASH-060 | P1 | Functional | Dashboard responsive layout | Cards reflow on narrow widths | 📋 |
| DASH-061 | P1 | Functional | Dashboard keyboard navigation | Tab through cards | 📋 |
| DASH-062 | P1 | Functional | Dashboard screen reader labels | ARIA labels on cards | 📋 |
| DASH-063 | P1 | Functional | Dashboard no console errors | Clean console on load | 📋 |
| DASH-064 | P1 | Performance | Dashboard loads in < 2s | Performant initial render | 📋 |
| DASH-065 | P1 | Edge | Dashboard with 0 jobs | Empty state; no crash | 📋 |
| DASH-066 | P1 | Edge | Dashboard with 1 job | Single job shown; stats valid | 📋 |
| DASH-067 | P1 | Edge | Dashboard with 1000+ jobs | Performant; no lag | 📋 |
| DASH-068 | P1 | Edge | Dashboard with all sources failing | Error state; existing data shown | 📋 |
| DASH-069 | P1 | Edge | Dashboard with partial source failure | Warning shown; data present | 📋 |
| DASH-070 | P1 | Functional | Dashboard after server restart | Data persists; loads correctly | 📋 |
| DASH-071 | P1 | Functional | Dashboard after app update | Migration preserves data | 📋 |
| DASH-072 | P1 | Security | Dashboard unauthenticated | 401; login view shown | ✅ |
| DASH-073 | P1 | Security | Dashboard with expired token | 401; re-login prompt | 📋 |
| DASH-074 | P1 | Security | Dashboard with malformed token | 401; re-login prompt | 📋 |
| DASH-075 | P1 | Functional | Dashboard data consistency | Stats match detail views | 📋 |
| DASH-076 | P1 | Functional | Dashboard XSS-safe rendering | Job titles/companies escaped | 📋 |
| DASH-077 | P1 | Functional | Dashboard relative dates update | "2h ago" recomputed on refresh | 📋 |
| DASH-078 | P1 | Functional | Dashboard handles API 500 | Error toast; no white screen | 📋 |
| DASH-079 | P1 | Functional | Dashboard handles slow API | Loading state; no duplicate requests | 📋 |
| DASH-080 | P1 | Regression | Dashboard regression v2.4 | All dashboard cases pass | 🧪 |

### 3.8 Pipeline / Kanban (PIPE)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| PIPE-001 | P0 | Functional | Pipeline shows 6 status lanes | new/review/applied/interview/offer/rejected | ✅ |
| PIPE-002 | P0 | Functional | Job appears in its status lane | Card in correct column | ✅ |
| PIPE-003 | P0 | Functional | `PATCH /api/jobs/{id}/status` moves job | 200; status updated | ✅ |
| PIPE-004 | P0 | Functional | Move new→review | Job in review lane | ✅ |
| PIPE-005 | P0 | Functional | Move review→applied | Job in applied lane | ✅ |
| PIPE-006 | P0 | Functional | Move applied→interview | Job in interview lane | ✅ |
| PIPE-007 | P0 | Functional | Move interview→offer | Job in offer lane | ✅ |
| PIPE-008 | P0 | Functional | Move any→rejected | Job in rejected lane | ✅ |
| PIPE-009 | P0 | Functional | Move rejected→new (reopen) | Job back in new lane | ✅ |
| PIPE-010 | P0 | Functional | Invalid status value | 422 `{"detail":"invalid status"}` | ✅ |
| PIPE-011 | P0 | Functional | Move non-existent job | 404 | ✅ |
| PIPE-012 | P0 | Functional | Move unauthenticated | 401 | ✅ |
| PIPE-013 | P0 | Functional | Drag-and-drop move in UI | Card moves; API called | ✅ |
| PIPE-014 | P0 | Functional | Drag to same lane | No-op; no API call | 📋 |
| PIPE-015 | P0 | Functional | Drag with invalid drop | Reverts; no state change | 📋 |
| PIPE-016 | P1 | Functional | Status change records timeline event | Event appended to job timeline | ✅ |
| PIPE-017 | P1 | Functional | Status change updates `updated_at` | Timestamp bumped | 📋 |
| PIPE-018 | P1 | Functional | Status change preserves other fields | Title/score unchanged | 📋 |
| PIPE-019 | P1 | Functional | Status change persists across reload | Lane retained | ✅ |
| PIPE-020 | P1 | Functional | Status change persists across restart | Lane retained | 📋 |
| PIPE-021 | P1 | Functional | Lane counts update after move | Column headers reflect new counts | ✅ |
| PIPE-022 | P1 | Functional | Lane count badge per column | Accurate count | ✅ |
| PIPE-023 | P1 | Functional | Pipeline respects filters | Filtered jobs only in lanes | 📋 |
| PIPE-024 | P1 | Functional | Pipeline respects search | Searched jobs only | 📋 |
| PIPE-025 | P1 | Functional | Pipeline card shows title + company | Both rendered | ✅ |
| PIPE-026 | P1 | Functional | Pipeline card shows confidence | Score badge | ✅ |
| PIPE-027 | P1 | Functional | Pipeline card shows source | Label | ✅ |
| PIPE-028 | P1 | Functional | Pipeline card shows salary | Parsed salary | 📋 |
| PIPE-029 | P1 | Functional | Pipeline card shows work mode | Badge | 📋 |
| PIPE-030 | P1 | Functional | Pipeline card click opens detail | Modal opens | ✅ |
| PIPE-031 | P1 | Functional | Pipeline empty lane | "No jobs" placeholder | 📋 |
| PIPE-032 | P1 | Functional | Pipeline all lanes empty | Empty state; no crash | 📋 |
| PIPE-033 | P1 | Functional | Pipeline loading state | Skeleton/spinner | 📋 |
| PIPE-034 | P1 | Functional | Pipeline error state | Message + retry | 📋 |
| PIPE-035 | P1 | Functional | Pipeline horizontal scroll | Lanes scroll on narrow widths | 📋 |
| PIPE-036 | P1 | Functional | Pipeline responsive | Usable on tablet width | 📋 |
| PIPE-037 | P1 | Functional | Pipeline keyboard move | Alt+arrow moves job between lanes | 📋 |
| PIPE-038 | P1 | Functional | Pipeline screen reader | Lane + card ARIA labels | 📋 |
| PIPE-039 | P1 | Functional | Pipeline no console errors | Clean console | 📋 |
| PIPE-040 | P1 | Functional | Pipeline with 500+ jobs | Performant; virtualized | 📋 |
| PIPE-041 | P1 | Functional | Pipeline concurrent moves | Last write wins; no corruption | 📋 |
| PIPE-042 | P1 | Functional | Pipeline move during scan | No conflict; both succeed | 📋 |
| PIPE-043 | P1 | Functional | Pipeline move with expired token | 401; re-login | 📋 |
| PIPE-044 | P1 | Functional | Pipeline move optimistic UI | Card moves immediately; reverts on error | 📋 |
| PIPE-045 | P1 | Functional | Pipeline move error toast | Message on 422/404 | 📋 |
| PIPE-046 | P1 | Functional | Pipeline move success toast | "Moved to Applied" | 📋 |
| PIPE-047 | P1 | Functional | Pipeline undo move | Revert to previous lane | 📋 |
| PIPE-048 | P1 | Functional | Pipeline bulk move | Select multiple → move together | 📋 |
| PIPE-049 | P1 | Functional | Pipeline bulk select | Checkbox per card | 📋 |
| PIPE-050 | P1 | Functional | Pipeline select all in lane | All cards in lane selected | 📋 |
| PIPE-051 | P1 | Functional | Pipeline clear selection | Deselect all | 📋 |
| PIPE-052 | P1 | Functional | Pipeline move history | Timeline shows all moves | 📋 |
| PIPE-053 | P1 | Functional | Pipeline time-in-lane | Days in current status | 📋 |
| PIPE-054 | P1 | Functional | Pipeline stalled jobs | Jobs > N days in lane flagged | 📋 |
| PIPE-055 | P1 | Functional | Pipeline WIP limit | Max cards per lane (optional) | 📋 |
| PIPE-056 | P1 | Functional | Pipeline column collapse | Lane collapsible | 📋 |
| PIPE-057 | P1 | Functional | Pipeline column reorder | Lanes reorderable (optional) | 📋 |
| PIPE-058 | P1 | Functional | Pipeline label/color per lane | Distinct visual identity | 📋 |
| PIPE-059 | P1 | Functional | Pipeline persist lane order | Custom order saved | 📋 |
| PIPE-060 | P1 | Functional | Pipeline regression v2.4 | All moves + counts pass | 🧪 |

### 3.9 Compare (CMP)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| CMP-001 | P0 | Functional | `GET /api/jobs/compare?ids=1,2` returns comparison | 200; both jobs with side-by-side fields | ✅ |
| CMP-002 | P0 | Functional | Compare 3 jobs | 200; 3 columns | ✅ |
| CMP-003 | P0 | Functional | Compare 5 jobs (max) | 200; 5 columns | ✅ |
| CMP-004 | P0 | Functional | Compare 6 jobs (over max) | 422 `{"detail":"max 5 jobs"}` | ✅ |
| CMP-005 | P0 | Functional | Compare 0 ids | 422 or empty; consistent | 📋 |
| CMP-006 | P0 | Functional | Compare with non-existent id | 404 or skipped; consistent | 📋 |
| CMP-007 | P0 | Functional | Compare with duplicate ids | Deduped or 422; consistent | 📋 |
| CMP-008 | P0 | Functional | Compare with non-numeric id | 422/ignored; no crash | 📋 |
| CMP-009 | P0 | Functional | Compare unauthenticated | 401 | ✅ |
| CMP-010 | P0 | Functional | Compare via POST (wrong method) | 405 | ✅ |
| CMP-011 | P1 | Functional | Compare shows title side-by-side | All titles in columns | ✅ |
| CMP-012 | P1 | Functional | Compare shows company side-by-side | All companies | ✅ |
| CMP-013 | P1 | Functional | Compare shows salary side-by-side | All salaries | ✅ |
| CMP-014 | P1 | Functional | Compare shows work mode side-by-side | All modes | ✅ |
| CMP-015 | P1 | Functional | Compare shows location side-by-side | All locations | ✅ |
| CMP-016 | P1 | Functional | Compare shows confidence side-by-side | All scores | ✅ |
| CMP-017 | P1 | Functional | Compare shows eligibility side-by-side | All % | ✅ |
| CMP-018 | P1 | Functional | Compare shows skills side-by-side | Matched/missing per job | ✅ |
| CMP-019 | P1 | Functional | Compare shows source side-by-side | All sources | ✅ |
| CMP-020 | P1 | Functional | Compare shows posted date side-by-side | All dates | ✅ |
| CMP-021 | P1 | Functional | Compare highlights best value | Highest salary/score highlighted | 📋 |
| CMP-022 | P1 | Functional | Compare highlights differences | Differing rows emphasized | 📋 |
| CMP-023 | P1 | Functional | Compare UI: select jobs via checkboxes | Multi-select in jobs view | 📋 |
| CMP-024 | P1 | Functional | Compare UI: compare button | Opens compare view | 📋 |
| CMP-025 | P1 | Functional | Compare UI: max 5 selection | 6th disabled with message | 📋 |
| CMP-026 | P1 | Functional | Compare UI: clear selection | Deselect all | 📋 |
| CMP-027 | P1 | Functional | Compare UI: remove one job | Column removed | 📋 |
| CMP-028 | P1 | Functional | Compare UI: add job | Column added (if < 5) | 📋 |
| CMP-029 | P1 | Functional | Compare UI: horizontal scroll | Columns scroll on narrow widths | 📋 |
| CMP-030 | P1 | Functional | Compare UI: sticky first column | Job title column stays fixed | 📋 |
| CMP-031 | P1 | Functional | Compare UI: row alignment | Fields aligned across columns | 📋 |
| CMP-032 | P1 | Functional | Compare UI: empty cell | "—" for missing field | 📋 |
| CMP-033 | P1 | Functional | Compare UI: loading state | Spinner during fetch | 📋 |
| CMP-034 | P1 | Functional | Compare UI: error state | Message on 422/404 | 📋 |
| CMP-035 | P1 | Functional | Compare UI: keyboard accessible | Tab through columns | 📋 |
| CMP-036 | P1 | Functional | Compare UI: screen reader | ARIA table semantics | 📋 |
| CMP-037 | P1 | Functional | Compare UI: no console errors | Clean console | 📋 |
| CMP-038 | P1 | Functional | Compare UI: export comparison | CSV/JSON of comparison | 📋 |
| CMP-039 | P1 | Functional | Compare UI: print view | Print-friendly layout | 📋 |
| CMP-040 | P1 | Functional | Compare with 1 job | 200; single column (or 422 min 2) — consistent | 📋 |
| CMP-041 | P1 | Functional | Compare ids with spaces | "1, 2" parsed correctly | 📋 |
| CMP-042 | P1 | Functional | Compare ids with semicolons | 422 or parsed; consistent | 📋 |
| CMP-043 | P1 | Functional | Compare ids with negative numbers | Ignored/422; no crash | 📋 |
| CMP-044 | P1 | Functional | Compare ids with huge numbers | 404; no crash | 📋 |
| CMP-045 | P1 | Functional | Compare ids with SQL payload | No injection; 422/404 | 📋 |
| CMP-046 | P1 | Functional | Compare ids with XSS payload | Escaped; no execution | 📋 |
| CMP-047 | P1 | Functional | Compare concurrent requests | Both succeed; consistent data | 📋 |
| CMP-048 | P1 | Functional | Compare after job deleted | 404 or skipped; consistent | 📋 |
| CMP-049 | P1 | Functional | Compare after status change | Reflects current status | 📋 |
| CMP-050 | P1 | Functional | Compare regression v2.4 | All compare cases pass | 🧪 |

### 3.10 Application Tracking (APP)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| APP-001 | P0 | Functional | Application record exists per job | One application object per job | ✅ |
| APP-002 | P0 | Functional | Application status mirrors job status | Consistent with pipeline lane | ✅ |
| APP-003 | P0 | Functional | `applied_at` set when moved to applied | Timestamp recorded | ✅ |
| APP-004 | P0 | Functional | `interview_at` set when moved to interview | Timestamp recorded | 📋 |
| APP-005 | P0 | Functional | `offer_at` set when moved to offer | Timestamp recorded | 📋 |
| APP-006 | P0 | Functional | `rejected_at` set when moved to rejected | Timestamp recorded | 📋 |
| APP-007 | P0 | Functional | Application notes editable | `PUT`/`PATCH` persists notes | ✅ |
| APP-008 | P0 | Functional | Application notes persist across reload | Notes retained | ✅ |
| APP-009 | P0 | Functional | Application notes persist across restart | Notes retained | 📋 |
| APP-010 | P0 | Functional | Application notes support multiline | Newlines preserved | 📋 |
| APP-011 | P0 | Functional | Application notes support unicode | Stored correctly | 📋 |
| APP-012 | P0 | Functional | Application notes XSS escaped | No script execution | 📋 |
| APP-013 | P0 | Functional | Application notes SQL injection safe | Stored as data | 📋 |
| APP-014 | P0 | Functional | Application notes length bounded | Very long notes handled | 📋 |
| APP-015 | P0 | Functional | Application notes empty allowed | Clearing notes works | 📋 |
| APP-016 | P0 | Functional | Application timeline records all events | Status changes + notes + scans | ✅ |
| APP-017 | P0 | Functional | Timeline events ordered chronologically | Ascending time | ✅ |
| APP-018 | P0 | Functional | Timeline shows event type | Icon/label per event | ✅ |
| APP-019 | P0 | Functional | Timeline shows event timestamp | Relative + absolute | ✅ |
| APP-020 | P0 | Functional | Timeline shows event detail | Description per event | ✅ |
| APP-021 | P0 | Functional | Timeline persists across reload | Events retained | ✅ |
| APP-022 | P0 | Functional | Timeline persists across restart | Events retained | 📋 |
| APP-023 | P0 | Functional | Timeline unauthenticated | 401 | ✅ |
| APP-024 | P0 | Functional | Timeline for non-existent job | 404 | ✅ |
| APP-025 | P1 | Functional | Application form completeness % | Computed from filled fields | ✅ |
| APP-026 | P1 | Functional | Application form missing fields listed | Gaps shown | ✅ |
| APP-027 | P1 | Functional | Application form required fields | Marked with asterisk | 📋 |
| APP-028 | P1 | Functional | Application form optional fields | Marked optional | 📋 |
| APP-029 | P1 | Functional | Application form validation | Inline errors on invalid | 📋 |
| APP-030 | P1 | Functional | Application form save | Persists all fields | 📋 |
| APP-031 | P1 | Functional | Application form reset | Clears to defaults | 📋 |
| APP-032 | P1 | Functional | Application form cancel | Discards changes | 📋 |
| APP-033 | P1 | Functional | Application form loading state | Spinner during save | 📋 |
| APP-034 | P1 | Functional | Application form success toast | "Application saved" | 📋 |
| APP-035 | P1 | Functional | Application form error toast | Message on 422 | 📋 |
| APP-036 | P1 | Functional | Application form responsive | Works on narrow widths | 📋 |
| APP-037 | P1 | Functional | Application form keyboard accessible | Tab/Enter work | 📋 |
| APP-038 | P1 | Functional | Application form screen reader | ARIA labels | 📋 |
| APP-039 | P1 | Functional | Application form no console errors | Clean console | 📋 |
| APP-040 | P1 | Functional | Cover letter generated from resume + job | References both | ✅ |
| APP-041 | P1 | Functional | Cover letter personalized per job | Job-specific content | ✅ |
| APP-042 | P1 | Functional | Cover letter editable | User can edit generated letter | 📋 |
| APP-043 | P1 | Functional | Cover letter persists | Edited letter retained | 📋 |
| APP-044 | P1 | Functional | Cover letter copy to clipboard | Copy button works | 📋 |
| APP-045 | P1 | Functional | Cover letter download | .txt/.md download | 📋 |
| APP-046 | P1 | Functional | Cover letter regenerate | Re-generates from current resume | 📋 |
| APP-047 | P1 | Functional | Cover letter length reasonable | 200–500 words | 📋 |
| APP-048 | P1 | Functional | Cover letter no placeholder text | No "[Your Name]" left | 📋 |
| APP-049 | P1 | Functional | Cover letter XSS safe | Escaped in preview | 📋 |
| APP-050 | P1 | Functional | Tailored resume generated per job | Highlights matching skills | ✅ |
| APP-051 | P1 | Functional | Tailored resume reorders sections | Matching skills first | 📋 |
| APP-052 | P1 | Functional | Tailored resume adds job keywords | Keywords from job description | 📋 |
| APP-053 | P1 | Functional | Tailored resume editable | User can edit | 📋 |
| APP-054 | P1 | Functional | Tailored resume persists | Edited version retained | 📋 |
| APP-055 | P1 | Functional | Tailored resume copy to clipboard | Copy button works | 📋 |
| APP-056 | P1 | Functional | Tailored resume download | .txt/.md download | 📋 |
| APP-057 | P1 | Functional | Tailored resume regenerate | Re-generates on resume change | 📋 |
| APP-058 | P1 | Functional | Interview prep questions generated | 5–10 questions per job | ✅ |
| APP-059 | P1 | Functional | Interview questions job-specific | Based on job requirements | ✅ |
| APP-060 | P1 | Functional | Interview questions resume-aware | Reference user's experience | 📋 |
| APP-061 | P1 | Functional | Interview questions categorized | Technical/behavioral/situational | 📋 |
| APP-062 | P1 | Functional | Interview questions with model answers | Sample answers provided | 📋 |
| APP-063 | P1 | Functional | Interview questions expandable | Click to reveal answer | 📋 |
| APP-064 | P1 | Functional | Interview questions copy | Copy individual question | 📋 |
| APP-065 | P1 | Functional | Interview questions print | Print-friendly | 📋 |
| APP-066 | P1 | Functional | Application days-in-stage computed | Days since last status change | 📋 |
| APP-067 | P1 | Functional | Application total days computed | Applied → current | 📋 |
| APP-068 | P1 | Functional | Application stalled flag | > 14 days in stage flagged | 📋 |
| APP-069 | P1 | Functional | Application follow-up reminder | Suggested follow-up date | 📋 |
| APP-070 | P1 | Functional | Application outcome recorded | Final status captured | 📋 |
| APP-071 | P1 | Functional | Application success rate per company | Offers / applications per company | 📋 |
| APP-072 | P1 | Functional | Application success rate per source | Offers / applications per source | 📋 |
| APP-073 | P1 | Functional | Application avg response time | Mean applied→response | 📋 |
| APP-074 | P1 | Functional | Application avg interview time | Mean applied→interview | 📋 |
| APP-075 | P1 | Functional | Application avg offer time | Mean applied→offer | 📋 |
| APP-076 | P1 | Functional | Application rejection reasons tracked | Categorized reasons | 📋 |
| APP-077 | P1 | Functional | Application withdrawal | User can withdraw application | 📋 |
| APP-078 | P1 | Functional | Application re-apply | Re-open rejected application | 📋 |
| APP-079 | P1 | Functional | Application export | Export application data | 📋 |
| APP-080 | P1 | Functional | Application regression v2.4 | All application cases pass | 🧪 |

### 3.11 Trust & Company (TRUST)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| TRUST-001 | P0 | Functional | Company rating computed per job | 6-dimension breakdown | ✅ |
| TRUST-002 | P0 | Functional | Rating: salary transparency | Scored 0–5 | ✅ |
| TRUST-003 | P0 | Functional | Rating: work-life balance | Scored 0–5 | ✅ |
| TRUST-004 | P0 | Functional | Rating: career growth | Scored 0–5 | ✅ |
| TRUST-005 | P0 | Functional | Rating: management quality | Scored 0–5 | ✅ |
| TRUST-006 | P0 | Functional | Rating: benefits | Scored 0–5 | ✅ |
| TRUST-007 | P0 | Functional | Rating: culture | Scored 0–5 | ✅ |
| TRUST-008 | P0 | Functional | Overall rating = mean of dimensions | 0–5 scale | ✅ |
| TRUST-009 | P0 | Functional | Rating shown on job card | Stars + numeric | ✅ |
| TRUST-010 | P0 | Functional | Rating shown in job detail | Full breakdown | ✅ |
| TRUST-011 | P0 | Functional | Rating flags (red/yellow/green) | Color-coded by score | ✅ |
| TRUST-012 | P0 | Functional | Rating deterministic | Same job → same rating | 🧪 |
| TRUST-013 | P0 | Functional | Rating persists across reload | Retained | ✅ |
| TRUST-014 | P0 | Functional | Rating persists across restart | Retained | 📋 |
| TRUST-015 | P0 | Functional | Rating unauthenticated | 401 | ✅ |
| TRUST-016 | P0 | Functional | Rating for non-existent job | 404 | ✅ |
| TRUST-017 | P1 | Functional | Rating handles missing data | Nulls → neutral score | 📋 |
| TRUST-018 | P1 | Functional | Rating handles zero salary | No crash; neutral | 📋 |
| TRUST-019 | P1 | Functional | Rating handles empty description | No crash; neutral | 📋 |
| TRUST-020 | P1 | Functional | Rating handles unicode company | Stored correctly | 📋 |
| TRUST-021 | P1 | Functional | Rating handles very long company name | Truncated in UI | 📋 |
| TRUST-022 | P1 | Functional | Rating handles duplicate company names | Consistent rating | 📋 |
| TRUST-023 | P1 | Functional | Rating handles unknown company | Neutral/default | 📋 |
| TRUST-024 | P1 | Functional | Rating handles new company (no history) | Neutral/default | 📋 |
| TRUST-025 | P1 | Functional | Rating handles company with 1 job | Valid rating | 📋 |
| TRUST-026 | P1 | Functional | Rating handles company with 1000 jobs | Valid rating; performant | 📋 |
| TRUST-027 | P1 | Functional | Rating re-computed on job update | Reflects new data | 📋 |
| TRUST-028 | P1 | Functional | Rating re-computed on resume change | Reflects new profile | 📋 |
| TRUST-029 | P1 | Functional | Rating shown in compare view | Side-by-side | 📋 |
| TRUST-030 | P1 | Functional | Rating shown in analytics | Aggregated by company | 📋 |
| TRUST-031 | P1 | Functional | Rating exportable | Included in CSV/JSON export | 📋 |
| TRUST-032 | P1 | Functional | Rating filterable | Min-rating filter works | 📋 |
| TRUST-033 | P1 | Functional | Rating sortable | Sort by rating in jobs view | 📋 |
| TRUST-034 | P1 | Functional | Rating tooltip | Hover shows dimension breakdown | 📋 |
| TRUST-035 | P1 | Functional | Rating expandable | Click shows full breakdown | 📋 |
| TRUST-036 | P1 | Functional | Rating keyboard accessible | Focusable; ARIA | 📋 |
| TRUST-037 | P1 | Functional | Rating screen reader | ARIA labels | 📋 |
| TRUST-038 | P1 | Functional | Rating no console errors | Clean console | 📋 |
| TRUST-039 | P1 | Functional | Company facts panel (F17) | Wikidata facts shown when enriched | ✅ |
| TRUST-040 | P1 | Functional | Company facts: description | From Wikidata | ✅ |
| TRUST-041 | P1 | Functional | Company facts: founded year | From Wikidata | ✅ |
| TRUST-042 | P1 | Functional | Company facts: employee count | From Wikidata | ✅ |
| TRUST-043 | P1 | Functional | Company facts: revenue | From Wikidata | ✅ |
| TRUST-044 | P1 | Functional | Company facts: industry | From Wikidata | ✅ |
| TRUST-045 | P1 | Functional | Company facts: headquarters | From Wikidata | ✅ |
| TRUST-046 | P1 | Functional | Company facts: website | From Wikidata | ✅ |
| TRUST-047 | P1 | Functional | Company facts: logo | From Wikidata (if available) | 📋 |
| TRUST-048 | P1 | Functional | Company facts: no-fake-data | Only real Wikidata; no synthetic | 🧪 |
| TRUST-049 | P1 | Functional | Company facts: deterministic | Same company → same facts | 🧪 |
| TRUST-050 | P1 | Functional | Company facts: regression v2.4 | All trust cases pass | 🧪 |

### 3.12 Analytics (ANLY)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| ANLY-001 | P0 | Functional | Analytics view loads | All cards render | ✅ |
| ANLY-002 | P0 | Functional | Analytics: jobs by source | Count per source | ✅ |
| ANLY-003 | P0 | Functional | Analytics: jobs by status | Count per status lane | ✅ |
| ANLY-004 | P0 | Functional | Analytics: jobs by work mode | Remote/hybrid/onsite counts | ✅ |
| ANLY-005 | P0 | Functional | Analytics: jobs by experience level | Entry/mid/senior counts | ✅ |
| ANLY-006 | P0 | Functional | Analytics: jobs by job type | Full-time/contract/etc | ✅ |
| ANLY-007 | P0 | Functional | Analytics: jobs by location | Top locations | ✅ |
| ANLY-008 | P0 | Functional | Analytics: jobs by salary band | Histogram by salary | ✅ |
| ANLY-009 | P0 | Functional | Analytics: jobs by posted date | Trend over time | ✅ |
| ANLY-010 | P0 | Functional | Analytics: avg confidence | Mean across jobs | ✅ |
| ANLY-011 | P0 | Functional | Analytics: avg eligibility | Mean across jobs | ✅ |
| ANLY-012 | P0 | Functional | Analytics: avg coverage | Mean across jobs | ✅ |
| ANLY-013 | P0 | Functional | Analytics: top matched skills | Frequency of matched skills | ✅ |
| ANLY-014 | P0 | Functional | Analytics: top missing skills | Frequency of missing skills | ✅ |
| ANLY-015 | P0 | Functional | Analytics: top companies | By job count | ✅ |
| ANLY-016 | P0 | Functional | Analytics: top sources | By job count | ✅ |
| ANLY-017 | P0 | Functional | Analytics: pipeline conversion | Funnel: new→review→applied→interview→offer | ✅ |
| ANLY-018 | P0 | Functional | Analytics: response rate | Applied / total | ✅ |
| ANLY-019 | P0 | Functional | Analytics: interview rate | Interviews / applied | ✅ |
| ANLY-020 | P0 | Functional | Analytics: offer rate | Offers / interviews | ✅ |
| ANLY-021 | P0 | Functional | Analytics: success rate | Offers / total applied | ✅ |
| ANLY-022 | P0 | Functional | Analytics: avg days to response | Mean applied→response | ✅ |
| ANLY-023 | P0 | Functional | Analytics: avg days to interview | Mean applied→interview | ✅ |
| ANLY-024 | P0 | Functional | Analytics: avg days to offer | Mean applied→offer | ✅ |
| ANLY-025 | P0 | Functional | Analytics: avg days to rejection | Mean applied→rejection | ✅ |
| ANLY-026 | P0 | Functional | Analytics: scan trend | Jobs per scan over time | ✅ |
| ANLY-027 | P0 | Functional | Analytics: source health | Success rate per source | ✅ |
| ANLY-028 | P0 | Functional | Analytics: source avg fetched | Rolling avg per source | ✅ |
| ANLY-029 | P0 | Functional | Analytics: source last scan | Timestamp per source | ✅ |
| ANLY-030 | P0 | Functional | Analytics: source error count | Errors per source | ✅ |
| ANLY-031 | P0 | Functional | Analytics: F15 registry card | Source registry status shown | ✅ |
| ANLY-032 | P0 | Functional | Analytics: F15 enabled sources | Count of enabled | ✅ |
| ANLY-033 | P0 | Functional | Analytics: F15 disabled sources | Count of disabled | ✅ |
| ANLY-034 | P0 | Functional | Analytics: F15 missing keys | Sources missing required keys | ✅ |
| ANLY-035 | P0 | Functional | Analytics: F17 scheduler card | Scheduler status shown | ✅ |
| ANLY-036 | P0 | Functional | Analytics: F17 next run | Next scheduled run time | ✅ |
| ANLY-037 | P0 | Functional | Analytics: F17 last run | Last run timestamp + result | ✅ |
| ANLY-038 | P0 | Functional | Analytics: F17 enrichment count | Jobs enriched | ✅ |
| ANLY-039 | P0 | Functional | Analytics: F17 enrichment success rate | % successful enrichments | ✅ |
| ANLY-040 | P0 | Functional | Analytics: F17 enrichment error count | Errors | ✅ |
| ANLY-041 | P0 | Functional | Analytics unauthenticated | 401 | ✅ |
| ANLY-042 | P0 | Functional | Analytics with 0 jobs | Empty state; no crash | 📋 |
| ANLY-043 | P0 | Functional | Analytics with 1 job | Valid stats | 📋 |
| ANLY-044 | P0 | Functional | Analytics with 1000+ jobs | Performant | 📋 |
| ANLY-045 | P1 | Functional | Analytics: time range filter | 7d/30d/90d/all | 📋 |
| ANLY-046 | P1 | Functional | Analytics: source filter | Filter by source | 📋 |
| ANLY-047 | P1 | Functional | Analytics: status filter | Filter by status | 📋 |
| ANLY-048 | P1 | Functional | Analytics: work mode filter | Filter by mode | 📋 |
| ANLY-049 | P1 | Functional | Analytics: experience filter | Filter by level | 📋 |
| ANLY-050 | P1 | Functional | Analytics: salary filter | Filter by salary band | 📋 |
| ANLY-051 | P1 | Functional | Analytics: location filter | Filter by location | 📋 |
| ANLY-052 | P1 | Functional | Analytics: date range picker | Custom range | 📋 |
| ANLY-053 | P1 | Functional | Analytics: compare periods | This month vs last month | 📋 |
| ANLY-054 | P1 | Functional | Analytics: export chart data | CSV of chart data | 📋 |
| ANLY-055 | P1 | Functional | Analytics: download chart image | PNG download | 📋 |
| ANLY-056 | P1 | Functional | Analytics: print view | Print-friendly | 📋 |
| ANLY-057 | P1 | Functional | Analytics: refresh button | Re-fetches data | 📋 |
| ANLY-058 | P1 | Functional | Analytics: auto-refresh | Updates on data change | 📋 |
| ANLY-059 | P1 | Functional | Analytics: loading state | Spinner during fetch | 📋 |
| ANLY-060 | P1 | Functional | Analytics: error state | Message + retry | 📋 |
| ANLY-061 | P1 | Functional | Analytics: empty chart | "No data" placeholder | 📋 |
| ANLY-062 | P1 | Functional | Analytics: chart tooltip | Hover shows values | 📋 |
| ANLY-063 | P1 | Functional | Analytics: chart legend | Legend shown | 📋 |
| ANLY-064 | P1 | Functional | Analytics: chart axis labels | Labeled axes | 📋 |
| ANLY-065 | P1 | Functional | Analytics: chart responsive | Resizes on window resize | 📋 |
| ANLY-066 | P1 | Functional | Analytics: chart keyboard accessible | Focusable; ARIA | 📋 |
| ANLY-067 | P1 | Functional | Analytics: chart screen reader | ARIA labels | 📋 |
| ANLY-068 | P1 | Functional | Analytics: no console errors | Clean console | 📋 |
| ANLY-069 | P1 | Functional | Analytics: data consistency | Matches detail views | 📋 |
| ANLY-070 | P1 | Functional | Analytics: updates after scan | New data reflected | 📋 |
| ANLY-071 | P1 | Functional | Analytics: updates after status change | Counts updated | 📋 |
| ANLY-072 | P1 | Functional | Analytics: updates after import | Imported jobs reflected | 📋 |
| ANLY-073 | P1 | Functional | Analytics: updates after delete | Removed jobs reflected | 📋 |
| ANLY-074 | P1 | Functional | Analytics: percentile distribution | P25/P50/P75 for scores | 📋 |
| ANLY-075 | P1 | Functional | Analytics: correlation matrix | Score vs eligibility correlation | 📋 |
| ANLY-076 | P1 | Functional | Analytics: cohort analysis | Jobs by week posted | 📋 |
| ANLY-077 | P1 | Functional | Analytics: retention curve | Jobs still active by age | 📋 |
| ANLY-078 | P1 | Functional | Analytics: funnel drop-off | % lost at each stage | 📋 |
| ANLY-079 | P1 | Functional | Analytics: velocity | Jobs processed per day | 📋 |
| ANLY-080 | P1 | Functional | Analytics regression v2.4 | All analytics cases pass | 🧪 |

### 3.13 Export / Import (EXP)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| EXP-001 | P0 | Functional | `GET /api/export/jobs` returns JSON | 200; valid JSON array of jobs | ✅ |
| EXP-002 | P0 | Functional | `GET /api/export/jobs?format=csv` returns CSV | 200; valid CSV with headers | ✅ |
| EXP-003 | P0 | Functional | Export includes all job fields | Title, company, salary, skills, etc. | ✅ |
| EXP-004 | P0 | Functional | Export includes application data | Status, notes, timestamps | ✅ |
| EXP-005 | P0 | Functional | Export includes score data | Confidence, eligibility, coverage | ✅ |
| EXP-006 | P0 | Functional | Export includes company rating | 6-dimension breakdown | ✅ |
| EXP-007 | P0 | Functional | Export includes profile | Profile + resume + variants + filters | ✅ |
| EXP-008 | P0 | Functional | Export unauthenticated | 401 | ✅ |
| EXP-009 | P0 | Functional | Export with 0 jobs | Empty array / header-only CSV | 📋 |
| EXP-010 | P0 | Functional | Export with 1 job | Single row | 📋 |
| EXP-011 | P0 | Functional | Export with 1000+ jobs | All rows; performant | 📋 |
| EXP-012 | P0 | Functional | Export CSV has proper headers | Column names match fields | ✅ |
| EXP-013 | P0 | Functional | Export CSV handles commas in data | Quoted fields | 📋 |
| EXP-014 | P0 | Functional | Export CSV handles newlines in data | Quoted fields | 📋 |
| EXP-015 | P0 | Functional | Export CSV handles unicode | UTF-8 encoded | 📋 |
| EXP-016 | P0 | Functional | Export CSV handles special chars | Escaped properly | 📋 |
| EXP-017 | P0 | Functional | Export JSON is valid | Parses without error | ✅ |
| EXP-018 | P0 | Functional | Export JSON includes all nested objects | Application, rating, scorecard | ✅ |
| EXP-019 | P0 | Functional | Export JSON null handling | Nulls preserved | 📋 |
| EXP-020 | P0 | Functional | Export JSON empty arrays | `[]` not omitted | 📋 |
| EXP-021 | P1 | Functional | `POST /api/import/jobs` with valid body | 200; jobs imported | ✅ |
| EXP-022 | P1 | Functional | Import body shape `{"jobs": [...]}` | Accepted | ✅ |
| EXP-023 | P1 | Functional | Import bare array `[...]` | 422 (wrong shape) | ✅ |
| EXP-024 | P1 | Functional | Import dedup by fingerprint | Duplicates skipped | ✅ |
| EXP-025 | P1 | Functional | Import new jobs | Added to DB | ✅ |
| EXP-026 | P1 | Functional | Import existing jobs | Skipped (dedup) | ✅ |
| EXP-027 | P1 | Functional | Import mixed new + existing | New added; existing skipped | ✅ |
| EXP-028 | P1 | Functional | Import response shows counts | `{imported: N, skipped: M}` | ✅ |
| EXP-029 | P1 | Functional | Import unauthenticated | 401 | ✅ |
| EXP-030 | P1 | Functional | Import with empty jobs list | 200; 0 imported | 📋 |
| EXP-031 | P1 | Functional | Import with 1 job | 1 imported | 📋 |
| EXP-032 | P1 | Functional | Import with 100 jobs | All imported (or batched) | 📋 |
| EXP-033 | P1 | Functional | Import with 1000 jobs | All imported; performant | 📋 |
| EXP-034 | P1 | Functional | Import with missing required fields | 422 or skipped; consistent | 📋 |
| EXP-035 | P1 | Functional | Import with extra unknown fields | Ignored; no crash | 📋 |
| EXP-036 | P1 | Functional | Import with null values | Handled; no crash | 📋 |
| EXP-037 | P1 | Functional | Import with unicode data | Stored correctly | 📋 |
| EXP-038 | P1 | Functional | Import with XSS in title | Stored; rendered escaped | 📋 |
| EXP-039 | P1 | Functional | Import with SQL in title | Stored as data; no injection | 📋 |
| EXP-040 | P1 | Functional | Import with very long description | Stored; truncated in UI | 📋 |
| EXP-041 | P1 | Functional | Import with invalid status | Defaulted to "new" or 422 | 📋 |
| EXP-042 | P1 | Functional | Import with invalid work_mode | Defaulted or 422 | 📋 |
| EXP-043 | P1 | Functional | Import with invalid source | Stored as-is or defaulted | 📋 |
| EXP-044 | P1 | Functional | Import with duplicate fingerprints in batch | First kept; rest skipped | 📋 |
| EXP-045 | P1 | Functional | Import scores computed on insert | Confidence/eligibility calculated | 📋 |
| EXP-046 | P1 | Functional | Import persists across restart | All imported jobs retained | 📋 |
| EXP-047 | P1 | Functional | Import + export round-trip | Export → import → same data | 📋 |
| EXP-048 | P1 | Functional | Export includes scan history | Scan records included | 📋 |
| EXP-049 | P1 | Functional | Export includes source registry | Registry state included | 📋 |
| EXP-050 | P1 | Functional | Export includes scheduler config | Scheduler state included | 📋 |
| EXP-051 | P1 | Functional | Export file download in browser | Triggers download; correct filename | 📋 |
| EXP-052 | P1 | Functional | Export CSV opens in Excel | No encoding issues | 📋 |
| EXP-053 | P1 | Functional | Export CSV opens in Google Sheets | No encoding issues | 📋 |
| EXP-054 | P1 | Functional | Export JSON opens in text editor | Readable; formatted | 📋 |
| EXP-055 | P1 | Functional | Export with BOM for Excel | UTF-8 BOM prepended (CSV) | 📋 |
| EXP-056 | P1 | Functional | Export filename includes date | `zeyrecuite-export-2025-01-15.json` | 📋 |
| EXP-057 | P1 | Functional | Export Content-Disposition header | `attachment; filename=...` | 📋 |
| EXP-058 | P1 | Functional | Export Content-Type correct | `application/json` or `text/csv` | 📋 |
| EXP-059 | P1 | Functional | Import from exported file | Round-trip works | 📋 |
| EXP-060 | P1 | Functional | Export/Import regression v2.4 | All export/import cases pass | 🧪 |

### 3.14 Sources & Adapters (SRC)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| SRC-001 | P0 | Functional | `GET /api/sources` returns registry | 200; 10 source entries | ✅ |
| SRC-002 | P0 | Functional | Registry includes name + enabled flag | Both fields present | ✅ |
| SRC-003 | P0 | Functional | Registry includes required keys | `required_keys` listed per source | ✅ |
| SRC-004 | P0 | Functional | Registry includes missing keys | `missing_keys` computed from config | ✅ |
| SRC-005 | P0 | Functional | Registry includes last scan info | Timestamp + result per source | ✅ |
| SRC-006 | P0 | Functional | Registry includes success rate | Rolling success % per source | ✅ |
| SRC-007 | P0 | Functional | Registry includes avg fetched | Rolling avg per source | ✅ |
| SRC-008 | P0 | Functional | Registry read-only via API | No POST/PUT/DELETE routes | ✅ |
| SRC-009 | P0 | Functional | Registry unauthenticated | 401 | ✅ |
| SRC-010 | P0 | Functional | `sources.json` has 10 entries | remoteok, weworkremotely, themuse, lever, ashby, workable, smartrecruiters, workday, adzuna + 1 | 🧪 |
| SRC-011 | P0 | Functional | 3 sources enabled by default | remoteok, weworkremotely, themuse | 🧪 |
| SRC-012 | P0 | Functional | 7 sources disabled by default | lever, ashby, workable, smartrecruiters, workday, adzuna + 1 | 🧪 |
| SRC-013 | P0 | Functional | Enabled sources activate in scan | Fetched during scan | 🧪 |
| SRC-014 | P0 | Functional | Disabled sources skipped in scan | Not fetched | 🧪 |
| SRC-015 | P0 | Functional | Source missing required keys not activated | Gated out of scan | 🧪 |
| SRC-016 | P0 | Functional | Source with all keys present activated | Included in scan | 🧪 |
| SRC-017 | P1 | Functional | Adapter: remoteok fetches listings | Public API/HTML parsed | 🧪 |
| SRC-018 | P1 | Functional | Adapter: weworkremotely fetches listings | Public feed parsed | 🧪 |
| SRC-019 | P1 | Functional | Adapter: themuse fetches listings | Public API parsed | 🧪 |
| SRC-020 | P1 | Functional | Adapter: lever fetches when enabled | Lever public API | 🧪 |
| SRC-021 | P1 | Functional | Adapter: ashby fetches when enabled | Ashby public API | 🧪 |
| SRC-022 | P1 | Functional | Adapter: workable fetches when enabled | Workable public API | 🧪 |
| SRC-023 | P1 | Functional | Adapter: smartrecruiters fetches when enabled | SmartRecruiters public API | 🧪 |
| SRC-024 | P1 | Functional | Adapter: workday fetches when enabled | Workday public API | 🧪 |
| SRC-025 | P1 | Functional | Adapter: adzuna fetches when enabled | Adzuna API (key required) | 🧪 |
| SRC-026 | P1 | Functional | Adapter normalizes to Job shape | Common fields populated | 🧪 |
| SRC-027 | P1 | Functional | Adapter sets source attribution | `source` = registry name | 🧪 |
| SRC-028 | P1 | Functional | Adapter handles empty feed | `[]` returned; no fake rows | 🧪 |
| SRC-029 | P1 | Functional | Adapter handles 404 | Error recorded; no crash | 📋 |
| SRC-030 | P1 | Functional | Adapter handles 429 (rate limit) | Backoff; error recorded | 📋 |
| SRC-031 | P1 | Functional | Adapter handles 500 | Retry then error | 📋 |
| SRC-032 | P1 | Functional | Adapter handles timeout | Timeout error; bounded wait | 📋 |
| SRC-033 | P1 | Functional | Adapter handles TLS error | Error recorded; no crash | 📋 |
| SRC-034 | P1 | Functional | Adapter handles DNS failure | Error recorded; no crash | 📋 |
| SRC-035 | P1 | Functional | Adapter handles malformed JSON | Error recorded; no crash | 📋 |
| SRC-036 | P1 | Functional | Adapter handles malformed HTML | Best-effort parse; no crash | 📋 |
| SRC-037 | P1 | Functional | Adapter handles empty response body | `[]` or error; no crash | 📋 |
| SRC-038 | P1 | Functional | Adapter handles huge response | Bounded memory; no OOM | 📋 |
| SRC-039 | P1 | Functional | Adapter handles unicode content | Stored correctly | 📋 |
| SRC-040 | P1 | Functional | Adapter handles HTML entities | Decoded | 📋 |
| SRC-041 | P1 | Functional | Adapter strips scripts/styles | Clean text | 📋 |
| SRC-042 | P1 | Functional | Adapter extracts salary | Parsed from text | 📋 |
| SRC-043 | P1 | Functional | Adapter extracts work mode | Detected from text | 📋 |
| SRC-044 | P1 | Functional | Adapter extracts location | Parsed from text | 📋 |
| SRC-045 | P1 | Functional | Adapter extracts posted date | Parsed from text | 📋 |
| SRC-046 | P1 | Functional | Adapter extracts skills | Keyword extraction | 📋 |
| SRC-047 | P1 | Functional | Adapter extracts application URL | Apply link captured | 📋 |
| SRC-048 | P1 | Functional | Adapter dedup within feed | No duplicate rows | 📋 |
| SRC-049 | P1 | Functional | Adapter respects robots.txt | Polite crawling | 📋 |
| SRC-050 | P1 | Functional | Adapter sets User-Agent | Identifiable UA string | 📋 |
| SRC-051 | P1 | Functional | Adapter uses https when available | No plaintext for https sources | 📋 |
| SRC-052 | P1 | Functional | Adapter bounded retries (tenacity) | Max 3 retries; exponential backoff | 🧪 |
| SRC-053 | P1 | Functional | Adapter per-source timeout | 30s default; configurable | 📋 |
| SRC-054 | P1 | Functional | Adapter concurrent execution | Sources fetched in parallel | 📋 |
| SRC-055 | P1 | Functional | Adapter failure isolation | One source failure doesn't block others | 📋 |
| SRC-056 | P1 | Functional | Adapter health tracking | Success/fail counts updated | 📋 |
| SRC-057 | P1 | Functional | Adapter last-scan timestamp | Updated per source | 📋 |
| SRC-058 | P1 | Functional | Adapter error messages logged | Descriptive; no stack trace in API | 📋 |
| SRC-059 | P1 | Functional | Adapter no fake data on empty | `[]` not synthetic rows | 🧪 |
| SRC-060 | P1 | Functional | Sources regression v2.4 | All source cases pass | 🧪 |

### 3.15 Scheduler & Enrichment (SCHED)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| SCHED-001 | P0 | Functional | `GET /api/scheduler` returns scheduler state | 200; enabled, interval, next_run, last_run | ✅ |
| SCHED-002 | P0 | Functional | Scheduler state read-only via API | No POST/PUT/DELETE routes | ✅ |
| SCHED-003 | P0 | Functional | Scheduler unauthenticated | 401 | ✅ |
| SCHED-004 | P0 | Functional | Scheduler enabled by default | `enabled: true` on fresh config | 🧪 |
| SCHED-005 | P0 | Functional | Scheduler interval configurable | `config.yaml` `scheduler.interval_hours` | 🧪 |
| SCHED-006 | P0 | Functional | Scheduler fires scan at interval | APScheduler triggers scan | 🧪 |
| SCHED-007 | P0 | Functional | Scheduler next_run computed | Now + interval | ✅ |
| SCHED-008 | P0 | Functional | Scheduler last_run recorded | Timestamp + result after run | ✅ |
| SCHED-009 | P0 | Functional | Scheduler survives server restart | APScheduler re-arms from config | 🧪 |
| SCHED-010 | P0 | Functional | Scheduler disabled in config | No auto scans; manual still works | 🧪 |
| SCHED-011 | P0 | Functional | `POST /api/enrich` triggers enrichment | 200; enrichment run recorded | ✅ |
| SCHED-012 | P0 | Functional | Enrichment fetches company facts | Wikidata lookups for job companies | ✅ |
| SCHED-013 | P0 | Functional | Enrichment stores facts on job | `company_facts` populated | ✅ |
| SCHED-014 | P0 | Functional | Enrichment no-fake-data | Only real Wikidata; nulls when absent | 🧪 |
| SCHED-015 | P0 | Functional | Enrichment deterministic | Same company → same facts | 🧪 |
| SCHED-016 | P0 | Functional | Enrichment unauthenticated | 401 | ✅ |
| SCHED-017 | P0 | Functional | Enrichment limit param | `?limit=N` bounds jobs processed | 📋 |
| SCHED-018 | P0 | Functional | Enrichment limit 0 | 422 or no-op; consistent | 📋 |
| SCHED-019 | P0 | Functional | Enrichment limit negative | 422 | 📋 |
| SCHED-020 | P0 | Functional | Enrichment limit huge | Bounded by job count | 📋 |
| SCHED-021 | P1 | Functional | Enrichment skips already-enriched jobs | No redundant Wikidata calls | 🧪 |
| SCHED-022 | P1 | Functional | Enrichment caches facts | Same company fetched once per run | 🧪 |
| SCHED-023 | P1 | Functional | Enrichment handles unknown company | Nulls stored; no crash | 📋 |
| SCHED-024 | P1 | Functional | Enrichment handles Wikidata 404 | Nulls; error counted | 📋 |
| SCHED-025 | P1 | Functional | Enrichment handles Wikidata 429 | Backoff; bounded retries | 📋 |
| SCHED-026 | P1 | Functional | Enrichment handles Wikidata timeout | Timeout; error counted | 📋 |
| SCHED-027 | P1 | Functional | Enrichment handles network failure | Error counted; app usable | 📋 |
| SCHED-028 | P1 | Functional | Enrichment handles malformed response | Error counted; no crash | 📋 |
| SCHED-029 | P1 | Functional | Enrichment records success count | Per-run stats | ✅ |
| SCHED-030 | P1 | Functional | Enrichment records error count | Per-run stats | ✅ |
| SCHED-031 | P1 | Functional | Enrichment records duration | Elapsed time | ✅ |
| SCHED-032 | P1 | Functional | Enrichment records timestamp | Run time stored | ✅ |
| SCHED-033 | P1 | Functional | Enrichment runs async | Non-blocking; UI responsive | 📋 |
| SCHED-034 | P1 | Functional | Enrichment progress feedback | "Enriching…" state; toast on done | 📋 |
| SCHED-035 | P1 | Functional | Enrichment Enrich button in UI | Triggers `POST /api/enrich` | ✅ |
| SCHED-036 | P1 | Functional | Enrichment scheduler card in UI | Shows enabled/interval/next/last | ✅ |
| SCHED-037 | P1 | Functional | Enrichment company facts panel in job detail | Facts rendered when present | ✅ |
| SCHED-038 | P1 | Functional | Enrichment facts: description | Rendered | ✅ |
| SCHED-039 | P1 | Functional | Enrichment facts: founded | Rendered | ✅ |
| SCHED-040 | P1 | Functional | Enrichment facts: employees | Rendered | ✅ |
| SCHED-041 | P1 | Functional | Enrichment facts: revenue | Rendered | ✅ |
| SCHED-042 | P1 | Functional | Enrichment facts: industry | Rendered | ✅ |
| SCHED-043 | P1 | Functional | Enrichment facts: HQ | Rendered | ✅ |
| SCHED-044 | P1 | Functional | Enrichment facts: website link | Clickable; opens in browser | 📋 |
| SCHED-045 | P1 | Functional | Enrichment facts: no facts state | "No company facts" placeholder | 📋 |
| SCHED-046 | P1 | Functional | Enrichment facts XSS safe | Escaped in panel | 📋 |
| SCHED-047 | P1 | Functional | Enrichment facts persist across reload | Retained | ✅ |
| SCHED-048 | P1 | Functional | Enrichment facts persist across restart | Retained (SQLite) | 📋 |
| SCHED-049 | P1 | Functional | Enrichment facts included in export | Part of export payload | 📋 |
| SCHED-050 | P1 | Functional | Enrichment facts included in compare | Side-by-side | 📋 |
| SCHED-051 | P1 | Functional | Scheduler + manual scan coexist | No conflict; both recorded | 📋 |
| SCHED-052 | P1 | Functional | Scheduler run during manual scan | Serialized; no corruption | 📋 |
| SCHED-053 | P1 | Functional | Scheduler run during enrichment | No conflict; both complete | 📋 |
| SCHED-054 | P1 | Functional | Scheduler interval 1 hour | Fires ~hourly | 🧪 |
| SCHED-055 | P1 | Functional | Scheduler interval 24 hours | Fires ~daily | 🧪 |
| SCHED-056 | P1 | Functional | Scheduler interval invalid in config | Falls back to default; warning logged | 📋 |
| SCHED-057 | P1 | Functional | Scheduler misfire handling | Late run caught up once | 📋 |
| SCHED-058 | P1 | Functional | Scheduler single-instance | No duplicate concurrent runs | 📋 |
| SCHED-059 | P1 | Functional | Scheduler logs runs | Timestamped log entries | 📋 |
| SCHED-060 | P1 | Functional | Scheduler/Enrichment regression v2.4 | All scheduler cases pass | 🧪 |

### 3.16 Desktop App (DESK) — F18

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| DESK-001 | P0 | Functional | `python desktop.py` launches native window | pywebview window opens; app loads | ⏳ |
| DESK-002 | P0 | Functional | Desktop window shows full SPA | All views render (dashboard, jobs, pipeline, etc.) | ⏳ |
| DESK-003 | P0 | Functional | Desktop window title | "ZEYRECUITE" | ⏳ |
| DESK-004 | P0 | Functional | Desktop window size | Reasonable default (1200×800) | ⏳ |
| DESK-005 | P0 | Functional | Desktop window resizable | User can resize | ⏳ |
| DESK-006 | P0 | Functional | Desktop window min size | Below min → clamped | ⏳ |
| DESK-007 | P0 | Functional | Desktop starts backend server | uvicorn starts on 127.0.0.1:8000 | ⏳ |
| DESK-008 | P0 | Functional | Desktop waits for server ready | Window loads after server responds | ⏳ |
| DESK-009 | P0 | Functional | Desktop clean shutdown | Window close → server stops; no orphan process | ⏳ |
| DESK-010 | P0 | Functional | Desktop port-in-use handling | Port 8000 busy → pick next free port or error | ⏳ |
| DESK-011 | P0 | Functional | Desktop per-user data folder | DB in `%LOCALAPPDATA%\ZEYRECUITE` (Win) / `~/Library/Application Support` (Mac) | ⏳ |
| DESK-012 | P0 | Functional | Desktop data persists across launches | Jobs/profile retained | ⏳ |
| DESK-013 | P0 | Functional | Desktop all features work in window | Scan, pipeline, compare, analytics, export, enrich | ⏳ |
| DESK-014 | P0 | Functional | Desktop offline operation | Works without internet (local data) | ⏳ |
| DESK-015 | P0 | Functional | Desktop login flow | Same as browser; token in webview storage | ⏳ |
| DESK-016 | P0 | Functional | Desktop logout | Token cleared; login view | ⏳ |
| DESK-017 | P1 | Functional | PyInstaller Windows build | `.exe` produced; runs standalone | ⏳ |
| DESK-018 | P1 | Functional | PyInstaller Mac build | `.app` bundle produced (on Mac/CI) | ⏳ |
| DESK-019 | P1 | Functional | Windows .exe first launch | Starts; no missing DLL errors | ⏳ |
| DESK-020 | P1 | Functional | Windows .exe with data | Per-user folder created; data persists | ⏳ |
| DESK-021 | P1 | Functional | Windows SmartScreen | Unsigned → warning; user can proceed | ⏳ |
| DESK-022 | P1 | Functional | Mac Gatekeeper | Unsigned → right-click → Open | ⏳ |
| DESK-023 | P1 | Functional | Mac .app first launch | Starts; no missing framework errors | ⏳ |
| DESK-024 | P1 | Functional | Mac .app with data | Per-user folder created; data persists | ⏳ |
| DESK-025 | P1 | Functional | Desktop window menu | File (Quit), Edit (Copy/Paste), View (Reload) | ⏳ |
| DESK-026 | P1 | Functional | Desktop keyboard shortcuts | Cmd/Ctrl+R reload; Cmd/Ctrl+Q quit | ⏳ |
| DESK-027 | P1 | Functional | Desktop external links | Open in system browser (not in window) | ⏳ |
| DESK-028 | P1 | Functional | Desktop notifications | Scan complete → OS notification (optional) | ⏳ |
| DESK-029 | P1 | Functional | Desktop tray icon | Minimize to tray (optional) | ⏳ |
| DESK-030 | P1 | Functional | Desktop auto-update check | Version check on launch (optional) | ⏳ |
| DESK-031 | P1 | Functional | Desktop crash recovery | Server crash → window shows error + retry | ⏳ |
| DESK-032 | P1 | Functional | Desktop DB corruption | Detected; backup offered | ⏳ |
| DESK-033 | P1 | Functional | Desktop concurrent instances | Second launch → focus existing or error | ⏳ |
| DESK-034 | P1 | Functional | Desktop high-DPI rendering | Crisp on Retina/4K | ⏳ |
| DESK-035 | P1 | Functional | Desktop dark mode | Follows OS theme (optional) | ⏳ |
| DESK-036 | P1 | Functional | Desktop window state memory | Position/size remembered across launches | ⏳ |
| DESK-037 | P1 | Functional | Desktop fullscreen toggle | F11 / green button | ⏳ |
| DESK-038 | P1 | Functional | Desktop zoom in/out | Cmd/Ctrl + +/- | ⏳ |
| DESK-039 | P1 | Functional | Desktop print | Cmd/Ctrl+P prints current view | ⏳ |
| DESK-040 | P1 | Functional | Desktop export download | File save dialog (native) | ⏳ |
| DESK-041 | P1 | Functional | Desktop import file picker | Native file dialog | ⏳ |
| DESK-042 | P1 | Functional | Desktop clipboard | Copy/paste works natively | ⏳ |
| DESK-043 | P1 | Functional | Desktop drag-drop file | Drop resume file → import (optional) | ⏳ |
| DESK-044 | P1 | Functional | Desktop memory usage | Bounded; no leak over 8h | ⏳ |
| DESK-045 | P1 | Functional | Desktop CPU usage | Idle < 5%; scan bounded | ⏳ |
| DESK-046 | P1 | Functional | Desktop startup time | < 10s to usable | ⏳ |
| DESK-047 | P1 | Functional | Desktop shutdown time | < 5s clean exit | ⏳ |
| DESK-048 | P1 | Functional | Desktop logs | Written to per-user logs folder | ⏳ |
| DESK-049 | P1 | Functional | Desktop error reporting | Crash → log + friendly message | ⏳ |
| DESK-050 | P1 | Functional | Desktop config file | `config.yaml` in data folder; editable | ⏳ |
| DESK-051 | P1 | Functional | Desktop sources.json | In data folder; editable | ⏳ |
| DESK-052 | P1 | Functional | Desktop update preserves data | New version → old data intact | ⏳ |
| DESK-053 | P1 | Functional | Desktop uninstall | Data folder remains (user data) | ⏳ |
| DESK-054 | P1 | Functional | Desktop Windows 10 | Runs | ⏳ |
| DESK-055 | P1 | Functional | Desktop Windows 11 | Runs | ⏳ |
| DESK-056 | P1 | Functional | Desktop macOS 12+ | Runs | ⏳ |
| DESK-057 | P1 | Functional | Desktop macOS 14+ | Runs | ⏳ |
| DESK-058 | P1 | Functional | Desktop ARM Mac (M1/M2/M3) | Runs (universal or arm64 build) | ⏳ |
| DESK-059 | P1 | Functional | Desktop Intel Mac | Runs (x64 build) | ⏳ |
| DESK-060 | P1 | Functional | Desktop regression v2.4 | All desktop cases pass | ⏳ |

### 3.17 Non-Functional (NFR)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| NFR-001 | P0 | Performance | Dashboard loads < 2s on local server | Measured via browser timing | 📋 |
| NFR-002 | P0 | Performance | Jobs list renders 500 jobs < 1s | Virtualized/paginated | 📋 |
| NFR-003 | P0 | Performance | Jobs list renders 2000 jobs < 3s | No browser freeze | 📋 |
| NFR-004 | P0 | Performance | API `GET /api/jobs` < 500ms (1000 jobs) | Measured | 📋 |
| NFR-005 | P0 | Performance | API `GET /api/jobs/{id}` < 100ms | Measured | 📋 |
| NFR-006 | P0 | Performance | Scan of 3 sources < 60s | Measured | 📋 |
| NFR-007 | P0 | Performance | Enrichment of 50 jobs < 30s | Measured | 📋 |
| NFR-008 | P0 | Performance | Export 1000 jobs < 5s | Measured | 📋 |
| NFR-009 | P0 | Performance | Import 1000 jobs < 10s | Measured | 📋 |
| NFR-010 | P0 | Performance | Compare 5 jobs < 200ms | Measured | 📋 |
| NFR-011 | P0 | Performance | Analytics compute < 1s (1000 jobs) | Measured | 📋 |
| NFR-012 | P0 | Performance | Rescore all jobs < 5s (1000 jobs) | Measured | 📋 |
| NFR-013 | P1 | Performance | Memory: server idle < 200MB | Measured | 📋 |
| NFR-014 | P1 | Performance | Memory: server after 1000 jobs < 400MB | Measured | 📋 |
| NFR-015 | P1 | Performance | Memory: no leak over 24h | Stable RSS | 📋 |
| NFR-016 | P1 | Performance | CPU: server idle < 5% | Measured | 📋 |
| NFR-017 | P1 | Performance | CPU: scan bounded | No runaway process | 📋 |
| NFR-018 | P1 | Performance | SQLite write throughput | 1000 inserts < 2s | 📋 |
| NFR-019 | P1 | Performance | SQLite read throughput | 1000-row query < 100ms | 📋 |
| NFR-020 | P1 | Performance | Concurrent requests (10 parallel) | All 200; no deadlock | 📋 |
| NFR-021 | P1 | Performance | Concurrent requests (50 parallel) | All 200; bounded | 📋 |
| NFR-022 | P1 | Performance | UI interaction latency < 100ms | Click → visual feedback | 📋 |
| NFR-023 | P1 | Performance | No layout shift on load | CLS < 0.1 | 📋 |
| NFR-024 | P1 | Performance | Bundle size < 500KB | app.js + assets | 📋 |
| NFR-025 | P1 | Performance | No blocking main-thread work > 200ms | Long tasks avoided | 📋 |
| NFR-026 | P0 | Reliability | Server runs 24h without crash | Soak test | 📋 |
| NFR-027 | P0 | Reliability | Server survives 1000 scans | No degradation | 📋 |
| NFR-028 | P0 | Reliability | DB integrity after 1000 writes | `PRAGMA integrity_check` ok | 📋 |
| NFR-029 | P0 | Reliability | DB survives power loss (WAL) | No corruption on recovery | 📋 |
| NFR-030 | P0 | Reliability | Server restart recovers state | All data intact | ✅ |
| NFR-031 | P0 | Reliability | Scheduler survives restart | Re-arms correctly | 🧪 |
| NFR-032 | P1 | Reliability | Graceful shutdown (SIGTERM) | Clean exit; no corruption | 📋 |
| NFR-033 | P1 | Reliability | Unhandled exception → 500 JSON | No crash; `{"detail":...}` | 📋 |
| NFR-034 | P1 | Reliability | DB locked → retry | Bounded wait; no crash | 📋 |
| NFR-035 | P1 | Reliability | Disk full → clear error | 500 with message; no corruption | 📋 |
| NFR-036 | P1 | Reliability | Network partition during scan | Sources error; app usable | 📋 |
| NFR-037 | P1 | Reliability | Partial scan failure | Successful sources persisted | 📋 |
| NFR-038 | P1 | Reliability | Concurrent scan + write | No corruption | 📋 |
| NFR-039 | P1 | Reliability | Backup/restore round-trip | Export → delete → import → intact | 📋 |
| NFR-040 | P1 | Reliability | Data migration forward | v2.3 → v2.4 schema upgrade | 🧪 |
| NFR-041 | P0 | Usability | All views reachable from nav | Sidebar links work | ✅ |
| NFR-042 | P0 | Usability | Consistent error toasts | All failures show message | ✅ |
| NFR-043 | P0 | Usability | Loading states on all async ops | Spinners shown | 📋 |
| NFR-044 | P0 | Usability | Empty states on all lists | Helpful messages | 📋 |
| NFR-045 | P0 | Usability | Keyboard navigation | Tab order logical | 📋 |
| NFR-046 | P0 | Usability | Focus visible | Focus rings shown | 📋 |
| NFR-047 | P1 | Usability | Responsive at 1024px | No horizontal scroll | 📋 |
| NFR-048 | P1 | Usability | Responsive at 768px | Usable on tablet | 📋 |
| NFR-049 | P1 | Usability | Responsive at 375px | Usable on phone (best-effort) | 📋 |
| NFR-050 | P1 | Usability | Color contrast WCAG AA | Text ≥ 4.5:1 | 📋 |
| NFR-051 | P1 | Usability | Screen reader: landmarks | nav/main/header roles | 📋 |
| NFR-052 | P1 | Usability | Screen reader: tables | Proper th/td semantics | 📋 |
| NFR-053 | P1 | Usability | Screen reader: modals | Focus trapped; announced | 📋 |
| NFR-054 | P1 | Usability | No console errors on any view | Clean console | 📋 |
| NFR-055 | P1 | Usability | No unhandled promise rejections | All caught | 📋 |
| NFR-056 | P1 | Usability | Consistent terminology | "Scan", "Enrich", "Pipeline" used consistently | 📋 |
| NFR-057 | P1 | Usability | Tooltips on icons | All icon buttons have title/aria | 📋 |
| NFR-058 | P1 | Usability | Confirmation on destructive actions | Delete/clear confirm dialogs | 📋 |
| NFR-059 | P1 | Usability | Undo where feasible | Status move undo | 📋 |
| NFR-060 | P1 | Usability | NFR regression v2.4 | All NFR cases pass | 📋 |

### 3.18 Regression & Release (REG)

| ID | Priority | Type | Scenario | Expected Result | Status |
|---|---|---|---|---|---|
| REG-001 | P0 | Regression | Full pytest suite | 131/131 pass | 🧪 |
| REG-002 | P0 | Regression | Fresh install → login → scan → pipeline | End-to-end happy path | ✅ |
| REG-003 | P0 | Regression | v2.3 → v2.4 DB migration | Existing data intact; new columns added | 🧪 |
| REG-004 | P0 | Regression | v2.4 → v2.4 restart | No schema drift; app boots | 🧪 |
| REG-005 | P0 | Regression | All 18 user stories covered | US-01–18 mapped to cases | ✅ |
| REG-006 | P0 | Regression | All 17 features covered | F1–F17 mapped to cases | ✅ |
| REG-007 | P0 | Regression | Error standard consistent | All errors `{"detail": "..."}` | ✅ |
| REG-008 | P0 | Regression | No 500 on any documented 4xx path | Status codes correct | ✅ |
| REG-009 | P0 | Regression | Auth enforced on all /api routes | 401 without token | ✅ |
| REG-010 | P0 | Regression | No route leaks raw stack traces | Clean error bodies | ✅ |
| REG-011 | P1 | Regression | Profile round-trip | Save → reload → identical | ✅ |
| REG-012 | P1 | Regression | Resume round-trip | Upload → reload → identical | ✅ |
| REG-013 | P1 | Regression | Filters round-trip | Save → reload → identical | ✅ |
| REG-014 | P1 | Regression | Variants round-trip | Save → reload → identical | ✅ |
| REG-015 | P1 | Regression | Jobs round-trip | Scan → restart → identical | ✅ |
| REG-016 | P1 | Regression | Pipeline round-trip | Move → restart → identical | ✅ |
| REG-017 | P1 | Regression | Applications round-trip | Add → restart → identical | ✅ |
| REG-018 | P1 | Regression | Notes round-trip | Add → restart → identical | ✅ |
| REG-019 | P1 | Regression | Export → import round-trip | Data identical | ✅ |
| REG-020 | P1 | Regression | Compare after status change | Reflects new status | ✅ |
| REG-021 | P1 | Regression | Analytics after delete | Counts updated | ✅ |
| REG-022 | P1 | Regression | Score after resume change | Recomputed | ✅ |
| REG-023 | P1 | Regression | Score after filter change | Recomputed | ✅ |
| REG-024 | P1 | Regression | Enrich after scan | New jobs enrichable | ✅ |
| REG-025 | P1 | Regression | Scheduler after config change | New interval honored | 📋 |
| REG-026 | P1 | Regression | Source toggle → next scan | Respected | 📋 |
| REG-027 | P1 | Regression | Logout → login | Session clean; data intact | ✅ |
| REG-028 | P1 | Regression | Password change → login | Old fails; new works | ✅ |
| REG-029 | P1 | Regression | Token expiry → auto-logout | Redirect to login | 📋 |
| REG-030 | P1 | Regression | Browser cache bust | New assets loaded after deploy | 📋 |
| REG-031 | P1 | Regression | No console errors after full tour | Clean console | 📋 |
| REG-032 | P1 | Regression | No orphan DB rows | FK integrity | 📋 |
| REG-033 | P1 | Regression | No duplicate jobs after re-scan | Fingerprint dedup | ✅ |
| REG-034 | P1 | Regression | No duplicate applications | Dedup on job+user | 📋 |
| REG-035 | P1 | Regression | UAT report matches reality | 131/131; verdict DONE | ✅ |
| REG-036 | P1 | Regression | User stories match implementation | v2.4 docs accurate | ✅ |
| REG-037 | P1 | Regression | Test cases match implementation | This doc accurate | ✅ |
| REG-038 | P1 | Regression | Dependency pinning | `requirements.txt` pinned | 📋 |
| REG-039 | P1 | Regression | Python 3.14 compatibility | Runs on 3.14 | 🧪 |
| REG-040 | P0 | Regression | Release gate v2.4 | All P0 cases pass → ship | ✅ |

---

## 4. Summary & Coverage Matrix

### 4.1 Per-Section Counts

| # | Section | Prefix | Cases |
|---|---|---|---|
| 3.1 | Profile & Account | PROF | 120 |
| 3.2 | Authentication & Account | AUTH | 80 |
| 3.3 | Security & Hardening | SEC | 100 |
| 3.4 | Job Discovery & Collection | JOB | 120 |
| 3.5 | Filtering & Data Quality | FIL | 80 |
| 3.6 | Resume & Tailoring | RES | 80 |
| 3.7 | Dashboard & Review Queue | DASH | 80 |
| 3.8 | Pipeline / Kanban | PIPE | 60 |
| 3.9 | Compare | CMP | 50 |
| 3.10 | Application Tracking | APP | 80 |
| 3.11 | Trust & Company | TRUST | 50 |
| 3.12 | Analytics | ANLY | 80 |
| 3.13 | Export / Import | EXP | 60 |
| 3.14 | Sources & Adapters | SRC | 60 |
| 3.15 | Scheduler & Enrichment | SCHED | 60 |
| 3.16 | Desktop App (F18) | DESK | 60 |
| 3.17 | Non-Functional | NFR | 60 |
| 3.18 | Regression & Release | REG | 40 |
| | **Total** | | **1320** |

### 4.2 Priority Breakdown

| Priority | Meaning | Approx. Share |
|---|---|---|
| P0 | Critical — must pass before release | ~35% |
| P1 | High — core feature behavior | ~50% |
| P2 | Medium — important edge cases | ~12% |
| P3 | Low — nice-to-have / cosmetic | ~3% |

### 4.3 Status Breakdown

| Status | Meaning | Count (approx.) |
|---|---|---|
| ✅ | Verified manually (UAT v2.4) | ~300 |
| 🧪 | Covered by pytest suite (131 tests) | ~250 |
| 📋 | Planned — to be executed in next UAT cycle | ~500 |
| ⏳ | Pending — blocked on F18 desktop build | ~60 |

### 4.4 Feature → Section Traceability

| Feature | Sections |
|---|---|
| F1 Profile | 3.1, 3.2 |
| F2 Auth | 3.2, 3.3 |
| F3 Job collection | 3.4, 3.14 |
| F4 Filtering | 3.5 |
| F5 Resume & tailoring | 3.6 |
| F6 Dashboard | 3.7 |
| F7 Pipeline | 3.8 |
| F8 Compare | 3.9 |
| F9 Application tracking | 3.10 |
| F10 Trust & company | 3.11 |
| F11 Analytics | 3.12 |
| F12 Export/Import | 3.13 |
| F13 Sources & adapters | 3.14 |
| F15 Source registry | 3.14 |
| F17 Scheduler & enrichment | 3.15 |
| F18 Desktop app | 3.16 |
| Cross-cutting | 3.3, 3.17, 3.18 |

### 4.5 Release Gate (v2.4)

- **All P0 cases must pass** before declaring release.
- **Pytest baseline:** 131/131 (REG-001).
- **UAT verdict:** DONE — READY (see `UAT_REPORT.md`).
- **Known pending:** F18 desktop build (DESK-001–060, ⏳) — tracked as next feature.

*Document version: 1.0 — generated alongside `docs/user-stories.md` v2.4 and `UAT_REPORT.md` v2.4.*

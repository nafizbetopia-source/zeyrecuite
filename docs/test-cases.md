# ZEYRECUITE — Test Cases (v2.4 — full catalog)

Companion to `PRD.md`, `SRS.md`, `user-stories.md`. Each case: **ID**,
**feature**, **precondition**, **steps**, **expected result**, **type**
(API / frontend-UAT). IDs are sequential and map to features (F#) and
user stories (US#).

**Scope note (v2.4):** F16 (Bangladesh boards) is **DROPPED** per product
decision — it conflicts with the app's South-Asia exclusion policy. All
F16 cases are removed. F15 and F17 now include frontend UAT cases for the
UI wired in v2.4 (Enrich button, Company facts panel, scheduler + registry
cards on Analytics).

**Test command:** `cd backend; & '..\.venv\Scripts\python.exe' -m pytest tests -q`

**Auth:** `POST /api/auth/login` with `admin` / `zeyrecuite` → Bearer token.

---

### F0 — Authentication & account

| TC-00001 | API | Authentication & account | Logged in | POST /api/auth/login | 200 + valid data |
| TC-00002 | API | Authentication & account | Logged in | POST /api/auth/login with invalid input | 400/422 + error message |
| TC-00003 | API | Authentication & account | Edge case | POST /api/auth/login at boundary value | Correct boundary handling |
| TC-00004 | API | Authentication & account | No auth token | POST /api/auth/login | 401 Unauthorized |
| TC-00005 | frontend-UAT | Authentication & account | Logged in | Open login in UI | UI renders correctly |
| TC-00006 | frontend-UAT | Authentication & account | No data | Open login with no data | No-data state shown |
| TC-00007 | API | Authentication & account | Expired token | POST /api/auth/login | 401 Unauthorized |
| TC-00008 | API | Authentication & account | Insufficient role | POST /api/auth/login | 403 Forbidden |
| TC-00009 | API | Authentication & account | Logged in | POST /api/auth/logout | 200 + valid data |
| TC-00010 | API | Authentication & account | Logged in | POST /api/auth/logout with invalid input | 400/422 + error message |
| TC-00011 | API | Authentication & account | Edge case | POST /api/auth/logout at boundary value | Correct boundary handling |
| TC-00012 | API | Authentication & account | No auth token | POST /api/auth/logout | 401 Unauthorized |
| TC-00013 | frontend-UAT | Authentication & account | Logged in | Open logout in UI | UI renders correctly |
| TC-00014 | frontend-UAT | Authentication & account | No data | Open logout with no data | No-data state shown |
| TC-00015 | API | Authentication & account | Expired token | POST /api/auth/logout | 401 Unauthorized |
| TC-00016 | API | Authentication & account | Insufficient role | POST /api/auth/logout | 403 Forbidden |
| TC-00017 | API | Authentication & account | Logged in | GET /api/auth/me | 200 + valid data |
| TC-00018 | API | Authentication & account | Logged in | GET /api/auth/me with invalid input | 400/422 + error message |
| TC-00019 | API | Authentication & account | Edge case | GET /api/auth/me at boundary value | Correct boundary handling |
| TC-00020 | API | Authentication & account | No auth token | GET /api/auth/me | 401 Unauthorized |
| TC-00021 | frontend-UAT | Authentication & account | Logged in | Open get current user in UI | UI renders correctly |
| TC-00022 | frontend-UAT | Authentication & account | No data | Open get current user with no data | No-data state shown |
| TC-00023 | API | Authentication & account | Expired token | GET /api/auth/me | 401 Unauthorized |
| TC-00024 | API | Authentication & account | Insufficient role | GET /api/auth/me | 403 Forbidden |
| TC-00025 | API | Authentication & account | Logged in | PUT /api/auth/password | 200 + valid data |
| TC-00026 | API | Authentication & account | Logged in | PUT /api/auth/password with invalid input | 400/422 + error message |
| TC-00027 | API | Authentication & account | Edge case | PUT /api/auth/password at boundary value | Correct boundary handling |
| TC-00028 | API | Authentication & account | No auth token | PUT /api/auth/password | 401 Unauthorized |
| TC-00029 | frontend-UAT | Authentication & account | Logged in | Open change password in UI | UI renders correctly |
| TC-00030 | frontend-UAT | Authentication & account | No data | Open change password with no data | No-data state shown |
| TC-00031 | API | Authentication & account | Expired token | PUT /api/auth/password | 401 Unauthorized |
| TC-00032 | API | Authentication & account | Insufficient role | PUT /api/auth/password | 403 Forbidden |
| TC-00033 | API | Authentication & account | Logged in | POST /api/auth/reset-password | 200 + valid data |
| TC-00034 | API | Authentication & account | Logged in | POST /api/auth/reset-password with invalid input | 400/422 + error message |
| TC-00035 | API | Authentication & account | Edge case | POST /api/auth/reset-password at boundary value | Correct boundary handling |
| TC-00036 | API | Authentication & account | No auth token | POST /api/auth/reset-password | 401 Unauthorized |
| TC-00037 | frontend-UAT | Authentication & account | Logged in | Open reset password in UI | UI renders correctly |
| TC-00038 | frontend-UAT | Authentication & account | No data | Open reset password with no data | No-data state shown |
| TC-00039 | API | Authentication & account | Expired token | POST /api/auth/reset-password | 401 Unauthorized |
| TC-00040 | API | Authentication & account | Insufficient role | POST /api/auth/reset-password | 403 Forbidden |
| TC-00041 | API | Authentication & account | Logged in | GET /api/auth/last-login | 200 + valid data |
| TC-00042 | API | Authentication & account | Logged in | GET /api/auth/last-login with invalid input | 400/422 + error message |
| TC-00043 | API | Authentication & account | Edge case | GET /api/auth/last-login at boundary value | Correct boundary handling |
| TC-00044 | API | Authentication & account | No auth token | GET /api/auth/last-login | 401 Unauthorized |
| TC-00045 | frontend-UAT | Authentication & account | Logged in | Open get last login in UI | UI renders correctly |
| TC-00046 | frontend-UAT | Authentication & account | No data | Open get last login with no data | No-data state shown |
| TC-00047 | API | Authentication & account | Expired token | GET /api/auth/last-login | 401 Unauthorized |
| TC-00048 | API | Authentication & account | Insufficient role | GET /api/auth/last-login | 403 Forbidden |
| TC-00049 | API | Authentication & account | Logged in | PUT /api/auth/email | 200 + valid data |
| TC-00050 | API | Authentication & account | Logged in | PUT /api/auth/email with invalid input | 400/422 + error message |
| TC-00051 | API | Authentication & account | Edge case | PUT /api/auth/email at boundary value | Correct boundary handling |
| TC-00052 | API | Authentication & account | No auth token | PUT /api/auth/email | 401 Unauthorized |
| TC-00053 | frontend-UAT | Authentication & account | Logged in | Open change email in UI | UI renders correctly |
| TC-00054 | frontend-UAT | Authentication & account | No data | Open change email with no data | No-data state shown |
| TC-00055 | API | Authentication & account | Expired token | PUT /api/auth/email | 401 Unauthorized |
| TC-00056 | API | Authentication & account | Insufficient role | PUT /api/auth/email | 403 Forbidden |
| TC-00057 | API | Authentication & account | Logged in | DELETE /api/auth/account | 200 + valid data |
| TC-00058 | API | Authentication & account | Logged in | DELETE /api/auth/account with invalid input | 400/422 + error message |
| TC-00059 | API | Authentication & account | Edge case | DELETE /api/auth/account at boundary value | Correct boundary handling |
| TC-00060 | API | Authentication & account | No auth token | DELETE /api/auth/account | 401 Unauthorized |
| TC-00061 | frontend-UAT | Authentication & account | Logged in | Open delete account in UI | UI renders correctly |
| TC-00062 | frontend-UAT | Authentication & account | No data | Open delete account with no data | No-data state shown |
| TC-00063 | API | Authentication & account | Expired token | DELETE /api/auth/account | 401 Unauthorized |
| TC-00064 | API | Authentication & account | Insufficient role | DELETE /api/auth/account | 403 Forbidden |
| TC-00065 | API | Authentication & account | Logged in | GET /api/auth/export | 200 + valid data |
| TC-00066 | API | Authentication & account | Logged in | GET /api/auth/export with invalid input | 400/422 + error message |
| TC-00067 | API | Authentication & account | Edge case | GET /api/auth/export at boundary value | Correct boundary handling |
| TC-00068 | API | Authentication & account | No auth token | GET /api/auth/export | 401 Unauthorized |
| TC-00069 | frontend-UAT | Authentication & account | Logged in | Open export account data in UI | UI renders correctly |
| TC-00070 | frontend-UAT | Authentication & account | No data | Open export account data with no data | No-data state shown |
| TC-00071 | API | Authentication & account | Expired token | GET /api/auth/export | 401 Unauthorized |
| TC-00072 | API | Authentication & account | Insufficient role | GET /api/auth/export | 403 Forbidden |
| TC-00073 | API | Authentication & account | Logged in | GET /api/auth/two-factor | 200 + valid data |
| TC-00074 | API | Authentication & account | Logged in | GET /api/auth/two-factor with invalid input | 400/422 + error message |
| TC-00075 | API | Authentication & account | Edge case | GET /api/auth/two-factor at boundary value | Correct boundary handling |
| TC-00076 | API | Authentication & account | No auth token | GET /api/auth/two-factor | 401 Unauthorized |
| TC-00077 | frontend-UAT | Authentication & account | Logged in | Open get 2FA status in UI | UI renders correctly |
| TC-00078 | frontend-UAT | Authentication & account | No data | Open get 2FA status with no data | No-data state shown |
| TC-00079 | API | Authentication & account | Expired token | GET /api/auth/two-factor | 401 Unauthorized |
| TC-00080 | API | Authentication & account | Insufficient role | GET /api/auth/two-factor | 403 Forbidden |
| TC-00081 | API | Authentication & account | Logged in | POST /api/auth/two-factor/enable | 200 + valid data |
| TC-00082 | API | Authentication & account | Logged in | POST /api/auth/two-factor/enable with invalid input | 400/422 + error message |
| TC-00083 | API | Authentication & account | Edge case | POST /api/auth/two-factor/enable at boundary value | Correct boundary handling |
| TC-00084 | API | Authentication & account | No auth token | POST /api/auth/two-factor/enable | 401 Unauthorized |
| TC-00085 | frontend-UAT | Authentication & account | Logged in | Open enable 2FA in UI | UI renders correctly |
| TC-00086 | frontend-UAT | Authentication & account | No data | Open enable 2FA with no data | No-data state shown |
| TC-00087 | API | Authentication & account | Expired token | POST /api/auth/two-factor/enable | 401 Unauthorized |
| TC-00088 | API | Authentication & account | Insufficient role | POST /api/auth/two-factor/enable | 403 Forbidden |
| TC-00089 | API | Authentication & account | Logged in | GET /api/auth/session | 200 + valid data |
| TC-00090 | API | Authentication & account | Logged in | GET /api/auth/session with invalid input | 400/422 + error message |
| TC-00091 | API | Authentication & account | Edge case | GET /api/auth/session at boundary value | Correct boundary handling |
| TC-00092 | API | Authentication & account | No auth token | GET /api/auth/session | 401 Unauthorized |
| TC-00093 | frontend-UAT | Authentication & account | Logged in | Open get session info in UI | UI renders correctly |
| TC-00094 | frontend-UAT | Authentication & account | No data | Open get session info with no data | No-data state shown |
| TC-00095 | API | Authentication & account | Expired token | GET /api/auth/session | 401 Unauthorized |
| TC-00096 | API | Authentication & account | Insufficient role | GET /api/auth/session | 403 Forbidden |
| TC-00097 | API | Authentication & account | Logged in | PUT /api/auth/lock | 200 + valid data |
| TC-00098 | API | Authentication & account | Logged in | PUT /api/auth/lock with invalid input | 400/422 + error message |
| TC-00099 | API | Authentication & account | Edge case | PUT /api/auth/lock at boundary value | Correct boundary handling |
| TC-00100 | API | Authentication & account | No auth token | PUT /api/auth/lock | 401 Unauthorized |
| TC-00101 | frontend-UAT | Authentication & account | Logged in | Open lock session in UI | UI renders correctly |
| TC-00102 | frontend-UAT | Authentication & account | No data | Open lock session with no data | No-data state shown |
| TC-00103 | API | Authentication & account | Expired token | PUT /api/auth/lock | 401 Unauthorized |
| TC-00104 | API | Authentication & account | Insufficient role | PUT /api/auth/lock | 403 Forbidden |
| TC-00105 | API | Authentication & account | Logged in | GET /api/auth/tips | 200 + valid data |
| TC-00106 | API | Authentication & account | Logged in | GET /api/auth/tips with invalid input | 400/422 + error message |
| TC-00107 | API | Authentication & account | Edge case | GET /api/auth/tips at boundary value | Correct boundary handling |
| TC-00108 | API | Authentication & account | No auth token | GET /api/auth/tips | 401 Unauthorized |
| TC-00109 | frontend-UAT | Authentication & account | Logged in | Open get usage tips in UI | UI renders correctly |
| TC-00110 | frontend-UAT | Authentication & account | No data | Open get usage tips with no data | No-data state shown |
| TC-00111 | API | Authentication & account | Expired token | GET /api/auth/tips | 401 Unauthorized |
| TC-00112 | API | Authentication & account | Insufficient role | GET /api/auth/tips | 403 Forbidden |
| TC-00113 | API | Authentication & account | Logged in | POST /api/auth/tour | 200 + valid data |
| TC-00114 | API | Authentication & account | Logged in | POST /api/auth/tour with invalid input | 400/422 + error message |
| TC-00115 | API | Authentication & account | Edge case | POST /api/auth/tour at boundary value | Correct boundary handling |
| TC-00116 | API | Authentication & account | No auth token | POST /api/auth/tour | 401 Unauthorized |
| TC-00117 | frontend-UAT | Authentication & account | Logged in | Open start welcome tour in UI | UI renders correctly |
| TC-00118 | frontend-UAT | Authentication & account | No data | Open start welcome tour with no data | No-data state shown |
| TC-00119 | API | Authentication & account | Expired token | POST /api/auth/tour | 401 Unauthorized |
| TC-00120 | API | Authentication & account | Insufficient role | POST /api/auth/tour | 403 Forbidden |
### F1 — Salary insights

| TC-00121 | API | Salary insights | Logged in | GET /api/analytics/salary | 200 + valid data |
| TC-00122 | API | Salary insights | Logged in | GET /api/analytics/salary with invalid input | 400/422 + error message |
| TC-00123 | API | Salary insights | Edge case | GET /api/analytics/salary at boundary value | Correct boundary handling |
| TC-00124 | API | Salary insights | No auth token | GET /api/analytics/salary | 401 Unauthorized |
| TC-00125 | frontend-UAT | Salary insights | Logged in | Open get salary analytics in UI | UI renders correctly |
| TC-00126 | frontend-UAT | Salary insights | No data | Open get salary analytics with no data | No-data state shown |
| TC-00127 | API | Salary insights | Expired token | GET /api/analytics/salary | 401 Unauthorized |
| TC-00128 | API | Salary insights | Insufficient role | GET /api/analytics/salary | 403 Forbidden |
| TC-00129 | API | Salary insights | Logged in | GET /api/analytics/salary?work_mode | 200 + valid data |
| TC-00130 | API | Salary insights | Logged in | GET /api/analytics/salary?work_mode with invalid input | 400/422 + error message |
| TC-00131 | API | Salary insights | Edge case | GET /api/analytics/salary?work_mode at boundary value | Correct boundary handling |
| TC-00132 | API | Salary insights | No auth token | GET /api/analytics/salary?work_mode | 401 Unauthorized |
| TC-00133 | frontend-UAT | Salary insights | Logged in | Open filter by work mode in UI | UI renders correctly |
| TC-00134 | frontend-UAT | Salary insights | No data | Open filter by work mode with no data | No-data state shown |
| TC-00135 | API | Salary insights | Expired token | GET /api/analytics/salary?work_mode | 401 Unauthorized |
| TC-00136 | API | Salary insights | Insufficient role | GET /api/analytics/salary?work_mode | 403 Forbidden |
| TC-00137 | API | Salary insights | Logged in | GET /api/analytics/salary?source | 200 + valid data |
| TC-00138 | API | Salary insights | Logged in | GET /api/analytics/salary?source with invalid input | 400/422 + error message |
| TC-00139 | API | Salary insights | Edge case | GET /api/analytics/salary?source at boundary value | Correct boundary handling |
| TC-00140 | API | Salary insights | No auth token | GET /api/analytics/salary?source | 401 Unauthorized |
| TC-00141 | frontend-UAT | Salary insights | Logged in | Open filter by source in UI | UI renders correctly |
| TC-00142 | frontend-UAT | Salary insights | No data | Open filter by source with no data | No-data state shown |
| TC-00143 | API | Salary insights | Expired token | GET /api/analytics/salary?source | 401 Unauthorized |
| TC-00144 | API | Salary insights | Insufficient role | GET /api/analytics/salary?source | 403 Forbidden |
| TC-00145 | API | Salary insights | Logged in | GET /api/analytics/salary?role | 200 + valid data |
| TC-00146 | API | Salary insights | Logged in | GET /api/analytics/salary?role with invalid input | 400/422 + error message |
| TC-00147 | API | Salary insights | Edge case | GET /api/analytics/salary?role at boundary value | Correct boundary handling |
| TC-00148 | API | Salary insights | No auth token | GET /api/analytics/salary?role | 401 Unauthorized |
| TC-00149 | frontend-UAT | Salary insights | Logged in | Open filter by role in UI | UI renders correctly |
| TC-00150 | frontend-UAT | Salary insights | No data | Open filter by role with no data | No-data state shown |
| TC-00151 | API | Salary insights | Expired token | GET /api/analytics/salary?role | 401 Unauthorized |
| TC-00152 | API | Salary insights | Insufficient role | GET /api/analytics/salary?role | 403 Forbidden |
| TC-00153 | API | Salary insights | Logged in | GET /api/analytics/salary?by_experience | 200 + valid data |
| TC-00154 | API | Salary insights | Logged in | GET /api/analytics/salary?by_experience with invalid input | 400/422 + error message |
| TC-00155 | API | Salary insights | Edge case | GET /api/analytics/salary?by_experience at boundary value | Correct boundary handling |
| TC-00156 | API | Salary insights | No auth token | GET /api/analytics/salary?by_experience | 401 Unauthorized |
| TC-00157 | frontend-UAT | Salary insights | Logged in | Open group by experience in UI | UI renders correctly |
| TC-00158 | frontend-UAT | Salary insights | No data | Open group by experience with no data | No-data state shown |
| TC-00159 | API | Salary insights | Expired token | GET /api/analytics/salary?by_experience | 401 Unauthorized |
| TC-00160 | API | Salary insights | Insufficient role | GET /api/analytics/salary?by_experience | 403 Forbidden |
| TC-00161 | API | Salary insights | Logged in | GET /api/analytics/salary?by_city | 200 + valid data |
| TC-00162 | API | Salary insights | Logged in | GET /api/analytics/salary?by_city with invalid input | 400/422 + error message |
| TC-00163 | API | Salary insights | Edge case | GET /api/analytics/salary?by_city at boundary value | Correct boundary handling |
| TC-00164 | API | Salary insights | No auth token | GET /api/analytics/salary?by_city | 401 Unauthorized |
| TC-00165 | frontend-UAT | Salary insights | Logged in | Open group by city in UI | UI renders correctly |
| TC-00166 | frontend-UAT | Salary insights | No data | Open group by city with no data | No-data state shown |
| TC-00167 | API | Salary insights | Expired token | GET /api/analytics/salary?by_city | 401 Unauthorized |
| TC-00168 | API | Salary insights | Insufficient role | GET /api/analytics/salary?by_city | 403 Forbidden |
| TC-00169 | API | Salary insights | Logged in | GET /api/analytics/salary?by_company_size | 200 + valid data |
| TC-00170 | API | Salary insights | Logged in | GET /api/analytics/salary?by_company_size with invalid input | 400/422 + error message |
| TC-00171 | API | Salary insights | Edge case | GET /api/analytics/salary?by_company_size at boundary value | Correct boundary handling |
| TC-00172 | API | Salary insights | No auth token | GET /api/analytics/salary?by_company_size | 401 Unauthorized |
| TC-00173 | frontend-UAT | Salary insights | Logged in | Open group by size in UI | UI renders correctly |
| TC-00174 | frontend-UAT | Salary insights | No data | Open group by size with no data | No-data state shown |
| TC-00175 | API | Salary insights | Expired token | GET /api/analytics/salary?by_company_size | 401 Unauthorized |
| TC-00176 | API | Salary insights | Insufficient role | GET /api/analytics/salary?by_company_size | 403 Forbidden |
| TC-00177 | API | Salary insights | Logged in | GET /api/analytics/salary?percentiles | 200 + valid data |
| TC-00178 | API | Salary insights | Logged in | GET /api/analytics/salary?percentiles with invalid input | 400/422 + error message |
| TC-00179 | API | Salary insights | Edge case | GET /api/analytics/salary?percentiles at boundary value | Correct boundary handling |
| TC-00180 | API | Salary insights | No auth token | GET /api/analytics/salary?percentiles | 401 Unauthorized |
| TC-00181 | frontend-UAT | Salary insights | Logged in | Open get percentiles in UI | UI renders correctly |
| TC-00182 | frontend-UAT | Salary insights | No data | Open get percentiles with no data | No-data state shown |
| TC-00183 | API | Salary insights | Expired token | GET /api/analytics/salary?percentiles | 401 Unauthorized |
| TC-00184 | API | Salary insights | Insufficient role | GET /api/analytics/salary?percentiles | 403 Forbidden |
| TC-00185 | API | Salary insights | Logged in | GET /api/analytics/salary?compare_current | 200 + valid data |
| TC-00186 | API | Salary insights | Logged in | GET /api/analytics/salary?compare_current with invalid input | 400/422 + error message |
| TC-00187 | API | Salary insights | Edge case | GET /api/analytics/salary?compare_current at boundary value | Correct boundary handling |
| TC-00188 | API | Salary insights | No auth token | GET /api/analytics/salary?compare_current | 401 Unauthorized |
| TC-00189 | frontend-UAT | Salary insights | Logged in | Open compare current in UI | UI renders correctly |
| TC-00190 | frontend-UAT | Salary insights | No data | Open compare current with no data | No-data state shown |
| TC-00191 | API | Salary insights | Expired token | GET /api/analytics/salary?compare_current | 401 Unauthorized |
| TC-00192 | API | Salary insights | Insufficient role | GET /api/analytics/salary?compare_current | 403 Forbidden |
| TC-00193 | API | Salary insights | Logged in | GET /api/analytics/salary?trend | 200 + valid data |
| TC-00194 | API | Salary insights | Logged in | GET /api/analytics/salary?trend with invalid input | 400/422 + error message |
| TC-00195 | API | Salary insights | Edge case | GET /api/analytics/salary?trend at boundary value | Correct boundary handling |
| TC-00196 | API | Salary insights | No auth token | GET /api/analytics/salary?trend | 401 Unauthorized |
| TC-00197 | frontend-UAT | Salary insights | Logged in | Open get trend in UI | UI renders correctly |
| TC-00198 | frontend-UAT | Salary insights | No data | Open get trend with no data | No-data state shown |
| TC-00199 | API | Salary insights | Expired token | GET /api/analytics/salary?trend | 401 Unauthorized |
| TC-00200 | API | Salary insights | Insufficient role | GET /api/analytics/salary?trend | 403 Forbidden |
| TC-00201 | API | Salary insights | Logged in | GET /api/analytics/salary?by_title | 200 + valid data |
| TC-00202 | API | Salary insights | Logged in | GET /api/analytics/salary?by_title with invalid input | 400/422 + error message |
| TC-00203 | API | Salary insights | Edge case | GET /api/analytics/salary?by_title at boundary value | Correct boundary handling |
| TC-00204 | API | Salary insights | No auth token | GET /api/analytics/salary?by_title | 401 Unauthorized |
| TC-00205 | frontend-UAT | Salary insights | Logged in | Open group by title in UI | UI renders correctly |
| TC-00206 | frontend-UAT | Salary insights | No data | Open group by title with no data | No-data state shown |
| TC-00207 | API | Salary insights | Expired token | GET /api/analytics/salary?by_title | 401 Unauthorized |
| TC-00208 | API | Salary insights | Insufficient role | GET /api/analytics/salary?by_title | 403 Forbidden |
| TC-00209 | API | Salary insights | Logged in | GET /api/analytics/salary?export | 200 + valid data |
| TC-00210 | API | Salary insights | Logged in | GET /api/analytics/salary?export with invalid input | 400/422 + error message |
| TC-00211 | API | Salary insights | Edge case | GET /api/analytics/salary?export at boundary value | Correct boundary handling |
| TC-00212 | API | Salary insights | No auth token | GET /api/analytics/salary?export | 401 Unauthorized |
| TC-00213 | frontend-UAT | Salary insights | Logged in | Open export salary data in UI | UI renders correctly |
| TC-00214 | frontend-UAT | Salary insights | No data | Open export salary data with no data | No-data state shown |
| TC-00215 | API | Salary insights | Expired token | GET /api/analytics/salary?export | 401 Unauthorized |
| TC-00216 | API | Salary insights | Insufficient role | GET /api/analytics/salary?export | 403 Forbidden |
| TC-00217 | API | Salary insights | Logged in | GET /api/analytics/salary?view=thousands | 200 + valid data |
| TC-00218 | API | Salary insights | Logged in | GET /api/analytics/salary?view=thousands with invalid input | 400/422 + error message |
| TC-00219 | API | Salary insights | Edge case | GET /api/analytics/salary?view=thousands at boundary value | Correct boundary handling |
| TC-00220 | API | Salary insights | No auth token | GET /api/analytics/salary?view=thousands | 401 Unauthorized |
| TC-00221 | frontend-UAT | Salary insights | Logged in | Open view in thousands in UI | UI renders correctly |
| TC-00222 | frontend-UAT | Salary insights | No data | Open view in thousands with no data | No-data state shown |
| TC-00223 | API | Salary insights | Expired token | GET /api/analytics/salary?view=thousands | 401 Unauthorized |
| TC-00224 | API | Salary insights | Insufficient role | GET /api/analytics/salary?view=thousands | 403 Forbidden |
| TC-00225 | API | Salary insights | Logged in | GET /api/analytics/salary?no_data | 200 + valid data |
| TC-00226 | API | Salary insights | Logged in | GET /api/analytics/salary?no_data with invalid input | 400/422 + error message |
| TC-00227 | API | Salary insights | Edge case | GET /api/analytics/salary?no_data at boundary value | Correct boundary handling |
| TC-00228 | API | Salary insights | No auth token | GET /api/analytics/salary?no_data | 401 Unauthorized |
| TC-00229 | frontend-UAT | Salary insights | Logged in | Open no-data state in UI | UI renders correctly |
| TC-00230 | frontend-UAT | Salary insights | No data | Open no-data state with no data | No-data state shown |
| TC-00231 | API | Salary insights | Expired token | GET /api/analytics/salary?no_data | 401 Unauthorized |
| TC-00232 | API | Salary insights | Insufficient role | GET /api/analytics/salary?no_data | 403 Forbidden |
| TC-00233 | API | Salary insights | Logged in | GET /api/analytics/salary?histogram | 200 + valid data |
| TC-00234 | API | Salary insights | Logged in | GET /api/analytics/salary?histogram with invalid input | 400/422 + error message |
| TC-00235 | API | Salary insights | Edge case | GET /api/analytics/salary?histogram at boundary value | Correct boundary handling |
| TC-00236 | API | Salary insights | No auth token | GET /api/analytics/salary?histogram | 401 Unauthorized |
| TC-00237 | frontend-UAT | Salary insights | Logged in | Open get histogram in UI | UI renders correctly |
| TC-00238 | frontend-UAT | Salary insights | No data | Open get histogram with no data | No-data state shown |
| TC-00239 | API | Salary insights | Expired token | GET /api/analytics/salary?histogram | 401 Unauthorized |
| TC-00240 | API | Salary insights | Insufficient role | GET /api/analytics/salary?histogram | 403 Forbidden |
### F2 — Resume scorecard

| TC-00241 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard | 200 + valid data |
| TC-00242 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard with invalid input | 400/422 + error message |
| TC-00243 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard at boundary value | Correct boundary handling |
| TC-00244 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard | 401 Unauthorized |
| TC-00245 | frontend-UAT | Resume scorecard | Logged in | Open get scorecard in UI | UI renders correctly |
| TC-00246 | frontend-UAT | Resume scorecard | No data | Open get scorecard with no data | No-data state shown |
| TC-00247 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard | 401 Unauthorized |
| TC-00248 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard | 403 Forbidden |
| TC-00249 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?category | 200 + valid data |
| TC-00250 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?category with invalid input | 400/422 + error message |
| TC-00251 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?category at boundary value | Correct boundary handling |
| TC-00252 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?category | 401 Unauthorized |
| TC-00253 | frontend-UAT | Resume scorecard | Logged in | Open breakdown by category in UI | UI renders correctly |
| TC-00254 | frontend-UAT | Resume scorecard | No data | Open breakdown by category with no data | No-data state shown |
| TC-00255 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?category | 401 Unauthorized |
| TC-00256 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?category | 403 Forbidden |
| TC-00257 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?variant | 200 + valid data |
| TC-00258 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?variant with invalid input | 400/422 + error message |
| TC-00259 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?variant at boundary value | Correct boundary handling |
| TC-00260 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?variant | 401 Unauthorized |
| TC-00261 | frontend-UAT | Resume scorecard | Logged in | Open scorecard per variant in UI | UI renders correctly |
| TC-00262 | frontend-UAT | Resume scorecard | No data | Open scorecard per variant with no data | No-data state shown |
| TC-00263 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?variant | 401 Unauthorized |
| TC-00264 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?variant | 403 Forbidden |
| TC-00265 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?export | 200 + valid data |
| TC-00266 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?export with invalid input | 400/422 + error message |
| TC-00267 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?export at boundary value | Correct boundary handling |
| TC-00268 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?export | 401 Unauthorized |
| TC-00269 | frontend-UAT | Resume scorecard | Logged in | Open export scorecard in UI | UI renders correctly |
| TC-00270 | frontend-UAT | Resume scorecard | No data | Open export scorecard with no data | No-data state shown |
| TC-00271 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?export | 401 Unauthorized |
| TC-00272 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?export | 403 Forbidden |
| TC-00273 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?radar | 200 + valid data |
| TC-00274 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?radar with invalid input | 400/422 + error message |
| TC-00275 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?radar at boundary value | Correct boundary handling |
| TC-00276 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?radar | 401 Unauthorized |
| TC-00277 | frontend-UAT | Resume scorecard | Logged in | Open radar chart data in UI | UI renders correctly |
| TC-00278 | frontend-UAT | Resume scorecard | No data | Open radar chart data with no data | No-data state shown |
| TC-00279 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?radar | 401 Unauthorized |
| TC-00280 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?radar | 403 Forbidden |
| TC-00281 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?core_only | 200 + valid data |
| TC-00282 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?core_only with invalid input | 400/422 + error message |
| TC-00283 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?core_only at boundary value | Correct boundary handling |
| TC-00284 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?core_only | 401 Unauthorized |
| TC-00285 | frontend-UAT | Resume scorecard | Logged in | Open core skills only in UI | UI renders correctly |
| TC-00286 | frontend-UAT | Resume scorecard | No data | Open core skills only with no data | No-data state shown |
| TC-00287 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?core_only | 401 Unauthorized |
| TC-00288 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?core_only | 403 Forbidden |
| TC-00289 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?refresh | 200 + valid data |
| TC-00290 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?refresh with invalid input | 400/422 + error message |
| TC-00291 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?refresh at boundary value | Correct boundary handling |
| TC-00292 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?refresh | 401 Unauthorized |
| TC-00293 | frontend-UAT | Resume scorecard | Logged in | Open refresh scorecard in UI | UI renders correctly |
| TC-00294 | frontend-UAT | Resume scorecard | No data | Open refresh scorecard with no data | No-data state shown |
| TC-00295 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?refresh | 401 Unauthorized |
| TC-00296 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?refresh | 403 Forbidden |
| TC-00297 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?mobile | 200 + valid data |
| TC-00298 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?mobile with invalid input | 400/422 + error message |
| TC-00299 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?mobile at boundary value | Correct boundary handling |
| TC-00300 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?mobile | 401 Unauthorized |
| TC-00301 | frontend-UAT | Resume scorecard | Logged in | Open mobile view in UI | UI renders correctly |
| TC-00302 | frontend-UAT | Resume scorecard | No data | Open mobile view with no data | No-data state shown |
| TC-00303 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?mobile | 401 Unauthorized |
| TC-00304 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?mobile | 403 Forbidden |
| TC-00305 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?hover | 200 + valid data |
| TC-00306 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?hover with invalid input | 400/422 + error message |
| TC-00307 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?hover at boundary value | Correct boundary handling |
| TC-00308 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?hover | 401 Unauthorized |
| TC-00309 | frontend-UAT | Resume scorecard | Logged in | Open hover tooltip data in UI | UI renders correctly |
| TC-00310 | frontend-UAT | Resume scorecard | No data | Open hover tooltip data with no data | No-data state shown |
| TC-00311 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?hover | 401 Unauthorized |
| TC-00312 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?hover | 403 Forbidden |
| TC-00313 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?zero | 200 + valid data |
| TC-00314 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?zero with invalid input | 400/422 + error message |
| TC-00315 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?zero at boundary value | Correct boundary handling |
| TC-00316 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?zero | 401 Unauthorized |
| TC-00317 | frontend-UAT | Resume scorecard | Logged in | Open zero coverage in UI | UI renders correctly |
| TC-00318 | frontend-UAT | Resume scorecard | No data | Open zero coverage with no data | No-data state shown |
| TC-00319 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?zero | 401 Unauthorized |
| TC-00320 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?zero | 403 Forbidden |
| TC-00321 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?full | 200 + valid data |
| TC-00322 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?full with invalid input | 400/422 + error message |
| TC-00323 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?full at boundary value | Correct boundary handling |
| TC-00324 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?full | 401 Unauthorized |
| TC-00325 | frontend-UAT | Resume scorecard | Logged in | Open full coverage in UI | UI renders correctly |
| TC-00326 | frontend-UAT | Resume scorecard | No data | Open full coverage with no data | No-data state shown |
| TC-00327 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?full | 401 Unauthorized |
| TC-00328 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?full | 403 Forbidden |
| TC-00329 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?gap | 200 + valid data |
| TC-00330 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?gap with invalid input | 400/422 + error message |
| TC-00331 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?gap at boundary value | Correct boundary handling |
| TC-00332 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?gap | 401 Unauthorized |
| TC-00333 | frontend-UAT | Resume scorecard | Logged in | Open gap list in UI | UI renders correctly |
| TC-00334 | frontend-UAT | Resume scorecard | No data | Open gap list with no data | No-data state shown |
| TC-00335 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?gap | 401 Unauthorized |
| TC-00336 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?gap | 403 Forbidden |
| TC-00337 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?matched | 200 + valid data |
| TC-00338 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?matched with invalid input | 400/422 + error message |
| TC-00339 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?matched at boundary value | Correct boundary handling |
| TC-00340 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?matched | 401 Unauthorized |
| TC-00341 | frontend-UAT | Resume scorecard | Logged in | Open matched skills in UI | UI renders correctly |
| TC-00342 | frontend-UAT | Resume scorecard | No data | Open matched skills with no data | No-data state shown |
| TC-00343 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?matched | 401 Unauthorized |
| TC-00344 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?matched | 403 Forbidden |
| TC-00345 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?ranked | 200 + valid data |
| TC-00346 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?ranked with invalid input | 400/422 + error message |
| TC-00347 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?ranked at boundary value | Correct boundary handling |
| TC-00348 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?ranked | 401 Unauthorized |
| TC-00349 | frontend-UAT | Resume scorecard | Logged in | Open ranked missing in UI | UI renders correctly |
| TC-00350 | frontend-UAT | Resume scorecard | No data | Open ranked missing with no data | No-data state shown |
| TC-00351 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?ranked | 401 Unauthorized |
| TC-00352 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?ranked | 403 Forbidden |
| TC-00353 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?saved | 200 + valid data |
| TC-00354 | API | Resume scorecard | Logged in | GET /api/jobs/{id}/scorecard?saved with invalid input | 400/422 + error message |
| TC-00355 | API | Resume scorecard | Edge case | GET /api/jobs/{id}/scorecard?saved at boundary value | Correct boundary handling |
| TC-00356 | API | Resume scorecard | No auth token | GET /api/jobs/{id}/scorecard?saved | 401 Unauthorized |
| TC-00357 | frontend-UAT | Resume scorecard | Logged in | Open saved job scorecard in UI | UI renders correctly |
| TC-00358 | frontend-UAT | Resume scorecard | No data | Open saved job scorecard with no data | No-data state shown |
| TC-00359 | API | Resume scorecard | Expired token | GET /api/jobs/{id}/scorecard?saved | 401 Unauthorized |
| TC-00360 | API | Resume scorecard | Insufficient role | GET /api/jobs/{id}/scorecard?saved | 403 Forbidden |
### F3 — Skill gap analysis

| TC-00361 | API | Skill gap analysis | Logged in | GET /api/analytics/skills | 200 + valid data |
| TC-00362 | API | Skill gap analysis | Logged in | GET /api/analytics/skills with invalid input | 400/422 + error message |
| TC-00363 | API | Skill gap analysis | Edge case | GET /api/analytics/skills at boundary value | Correct boundary handling |
| TC-00364 | API | Skill gap analysis | No auth token | GET /api/analytics/skills | 401 Unauthorized |
| TC-00365 | frontend-UAT | Skill gap analysis | Logged in | Open get most-requested skills in UI | UI renders correctly |
| TC-00366 | frontend-UAT | Skill gap analysis | No data | Open get most-requested skills with no data | No-data state shown |
| TC-00367 | API | Skill gap analysis | Expired token | GET /api/analytics/skills | 401 Unauthorized |
| TC-00368 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills | 403 Forbidden |
| TC-00369 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?missing | 200 + valid data |
| TC-00370 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?missing with invalid input | 400/422 + error message |
| TC-00371 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?missing at boundary value | Correct boundary handling |
| TC-00372 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?missing | 401 Unauthorized |
| TC-00373 | frontend-UAT | Skill gap analysis | Logged in | Open you're-missing list in UI | UI renders correctly |
| TC-00374 | frontend-UAT | Skill gap analysis | No data | Open you're-missing list with no data | No-data state shown |
| TC-00375 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?missing | 401 Unauthorized |
| TC-00376 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?missing | 403 Forbidden |
| TC-00377 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?mine | 200 + valid data |
| TC-00378 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?mine with invalid input | 400/422 + error message |
| TC-00379 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?mine at boundary value | Correct boundary handling |
| TC-00380 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?mine | 401 Unauthorized |
| TC-00381 | frontend-UAT | Skill gap analysis | Logged in | Open my skills ranked in UI | UI renders correctly |
| TC-00382 | frontend-UAT | Skill gap analysis | No data | Open my skills ranked with no data | No-data state shown |
| TC-00383 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?mine | 401 Unauthorized |
| TC-00384 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?mine | 403 Forbidden |
| TC-00385 | API | Skill gap analysis | Logged in | POST /api/profile/skills | 200 + valid data |
| TC-00386 | API | Skill gap analysis | Logged in | POST /api/profile/skills with invalid input | 400/422 + error message |
| TC-00387 | API | Skill gap analysis | Edge case | POST /api/profile/skills at boundary value | Correct boundary handling |
| TC-00388 | API | Skill gap analysis | No auth token | POST /api/profile/skills | 401 Unauthorized |
| TC-00389 | frontend-UAT | Skill gap analysis | Logged in | Open add skill in UI | UI renders correctly |
| TC-00390 | frontend-UAT | Skill gap analysis | No data | Open add skill with no data | No-data state shown |
| TC-00391 | API | Skill gap analysis | Expired token | POST /api/profile/skills | 401 Unauthorized |
| TC-00392 | API | Skill gap analysis | Insufficient role | POST /api/profile/skills | 403 Forbidden |
| TC-00393 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?work_mode | 200 + valid data |
| TC-00394 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?work_mode with invalid input | 400/422 + error message |
| TC-00395 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?work_mode at boundary value | Correct boundary handling |
| TC-00396 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?work_mode | 401 Unauthorized |
| TC-00397 | frontend-UAT | Skill gap analysis | Logged in | Open remote demand in UI | UI renders correctly |
| TC-00398 | frontend-UAT | Skill gap analysis | No data | Open remote demand with no data | No-data state shown |
| TC-00399 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?work_mode | 401 Unauthorized |
| TC-00400 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?work_mode | 403 Forbidden |
| TC-00401 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?source | 200 + valid data |
| TC-00402 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?source with invalid input | 400/422 + error message |
| TC-00403 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?source at boundary value | Correct boundary handling |
| TC-00404 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?source | 401 Unauthorized |
| TC-00405 | frontend-UAT | Skill gap analysis | Logged in | Open source demand in UI | UI renders correctly |
| TC-00406 | frontend-UAT | Skill gap analysis | No data | Open source demand with no data | No-data state shown |
| TC-00407 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?source | 401 Unauthorized |
| TC-00408 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?source | 403 Forbidden |
| TC-00409 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?top | 200 + valid data |
| TC-00410 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?top with invalid input | 400/422 + error message |
| TC-00411 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?top at boundary value | Correct boundary handling |
| TC-00412 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?top | 401 Unauthorized |
| TC-00413 | frontend-UAT | Skill gap analysis | Logged in | Open top N skills in UI | UI renders correctly |
| TC-00414 | frontend-UAT | Skill gap analysis | No data | Open top N skills with no data | No-data state shown |
| TC-00415 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?top | 401 Unauthorized |
| TC-00416 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?top | 403 Forbidden |
| TC-00417 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?by_city | 200 + valid data |
| TC-00418 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?by_city with invalid input | 400/422 + error message |
| TC-00419 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?by_city at boundary value | Correct boundary handling |
| TC-00420 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?by_city | 401 Unauthorized |
| TC-00421 | frontend-UAT | Skill gap analysis | Logged in | Open demand by city in UI | UI renders correctly |
| TC-00422 | frontend-UAT | Skill gap analysis | No data | Open demand by city with no data | No-data state shown |
| TC-00423 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?by_city | 401 Unauthorized |
| TC-00424 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?by_city | 403 Forbidden |
| TC-00425 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?by_salary | 200 + valid data |
| TC-00426 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?by_salary with invalid input | 400/422 + error message |
| TC-00427 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?by_salary at boundary value | Correct boundary handling |
| TC-00428 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?by_salary | 401 Unauthorized |
| TC-00429 | frontend-UAT | Skill gap analysis | Logged in | Open demand by salary in UI | UI renders correctly |
| TC-00430 | frontend-UAT | Skill gap analysis | No data | Open demand by salary with no data | No-data state shown |
| TC-00431 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?by_salary | 401 Unauthorized |
| TC-00432 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?by_salary | 403 Forbidden |
| TC-00433 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?roadmap | 200 + valid data |
| TC-00434 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?roadmap with invalid input | 400/422 + error message |
| TC-00435 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?roadmap at boundary value | Correct boundary handling |
| TC-00436 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?roadmap | 401 Unauthorized |
| TC-00437 | frontend-UAT | Skill gap analysis | Logged in | Open learning roadmap in UI | UI renders correctly |
| TC-00438 | frontend-UAT | Skill gap analysis | No data | Open learning roadmap with no data | No-data state shown |
| TC-00439 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?roadmap | 401 Unauthorized |
| TC-00440 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?roadmap | 403 Forbidden |
| TC-00441 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?trending | 200 + valid data |
| TC-00442 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?trending with invalid input | 400/422 + error message |
| TC-00443 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?trending at boundary value | Correct boundary handling |
| TC-00444 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?trending | 401 Unauthorized |
| TC-00445 | frontend-UAT | Skill gap analysis | Logged in | Open trending skills in UI | UI renders correctly |
| TC-00446 | frontend-UAT | Skill gap analysis | No data | Open trending skills with no data | No-data state shown |
| TC-00447 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?trending | 401 Unauthorized |
| TC-00448 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?trending | 403 Forbidden |
| TC-00449 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?coverage_by_job | 200 + valid data |
| TC-00450 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?coverage_by_job with invalid input | 400/422 + error message |
| TC-00451 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?coverage_by_job at boundary value | Correct boundary handling |
| TC-00452 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?coverage_by_job | 401 Unauthorized |
| TC-00453 | frontend-UAT | Skill gap analysis | Logged in | Open per-job coverage in UI | UI renders correctly |
| TC-00454 | frontend-UAT | Skill gap analysis | No data | Open per-job coverage with no data | No-data state shown |
| TC-00455 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?coverage_by_job | 401 Unauthorized |
| TC-00456 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?coverage_by_job | 403 Forbidden |
| TC-00457 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?by_proficiency | 200 + valid data |
| TC-00458 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?by_proficiency with invalid input | 400/422 + error message |
| TC-00459 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?by_proficiency at boundary value | Correct boundary handling |
| TC-00460 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?by_proficiency | 401 Unauthorized |
| TC-00461 | frontend-UAT | Skill gap analysis | Logged in | Open by proficiency in UI | UI renders correctly |
| TC-00462 | frontend-UAT | Skill gap analysis | No data | Open by proficiency with no data | No-data state shown |
| TC-00463 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?by_proficiency | 401 Unauthorized |
| TC-00464 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?by_proficiency | 403 Forbidden |
| TC-00465 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?export | 200 + valid data |
| TC-00466 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?export with invalid input | 400/422 + error message |
| TC-00467 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?export at boundary value | Correct boundary handling |
| TC-00468 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?export | 401 Unauthorized |
| TC-00469 | frontend-UAT | Skill gap analysis | Logged in | Open export skills in UI | UI renders correctly |
| TC-00470 | frontend-UAT | Skill gap analysis | No data | Open export skills with no data | No-data state shown |
| TC-00471 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?export | 401 Unauthorized |
| TC-00472 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?export | 403 Forbidden |
| TC-00473 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?empty | 200 + valid data |
| TC-00474 | API | Skill gap analysis | Logged in | GET /api/analytics/skills?empty with invalid input | 400/422 + error message |
| TC-00475 | API | Skill gap analysis | Edge case | GET /api/analytics/skills?empty at boundary value | Correct boundary handling |
| TC-00476 | API | Skill gap analysis | No auth token | GET /api/analytics/skills?empty | 401 Unauthorized |
| TC-00477 | frontend-UAT | Skill gap analysis | Logged in | Open no-data state in UI | UI renders correctly |
| TC-00478 | frontend-UAT | Skill gap analysis | No data | Open no-data state with no data | No-data state shown |
| TC-00479 | API | Skill gap analysis | Expired token | GET /api/analytics/skills?empty | 401 Unauthorized |
| TC-00480 | API | Skill gap analysis | Insufficient role | GET /api/analytics/skills?empty | 403 Forbidden |
### F4 — Source health

| TC-00481 | API | Source health | Logged in | GET /api/analytics/sources | 200 + valid data |
| TC-00482 | API | Source health | Logged in | GET /api/analytics/sources with invalid input | 400/422 + error message |
| TC-00483 | API | Source health | Edge case | GET /api/analytics/sources at boundary value | Correct boundary handling |
| TC-00484 | API | Source health | No auth token | GET /api/analytics/sources | 401 Unauthorized |
| TC-00485 | frontend-UAT | Source health | Logged in | Open get source health in UI | UI renders correctly |
| TC-00486 | frontend-UAT | Source health | No data | Open get source health with no data | No-data state shown |
| TC-00487 | API | Source health | Expired token | GET /api/analytics/sources | 401 Unauthorized |
| TC-00488 | API | Source health | Insufficient role | GET /api/analytics/sources | 403 Forbidden |
| TC-00489 | API | Source health | Logged in | GET /api/analytics/sources?success_rate | 200 + valid data |
| TC-00490 | API | Source health | Logged in | GET /api/analytics/sources?success_rate with invalid input | 400/422 + error message |
| TC-00491 | API | Source health | Edge case | GET /api/analytics/sources?success_rate at boundary value | Correct boundary handling |
| TC-00492 | API | Source health | No auth token | GET /api/analytics/sources?success_rate | 401 Unauthorized |
| TC-00493 | frontend-UAT | Source health | Logged in | Open success rate in UI | UI renders correctly |
| TC-00494 | frontend-UAT | Source health | No data | Open success rate with no data | No-data state shown |
| TC-00495 | API | Source health | Expired token | GET /api/analytics/sources?success_rate | 401 Unauthorized |
| TC-00496 | API | Source health | Insufficient role | GET /api/analytics/sources?success_rate | 403 Forbidden |
| TC-00497 | API | Source health | Logged in | GET /api/analytics/sources?sort | 200 + valid data |
| TC-00498 | API | Source health | Logged in | GET /api/analytics/sources?sort with invalid input | 400/422 + error message |
| TC-00499 | API | Source health | Edge case | GET /api/analytics/sources?sort at boundary value | Correct boundary handling |
| TC-00500 | API | Source health | No auth token | GET /api/analytics/sources?sort | 401 Unauthorized |
| TC-00501 | frontend-UAT | Source health | Logged in | Open sort by yield in UI | UI renders correctly |
| TC-00502 | frontend-UAT | Source health | No data | Open sort by yield with no data | No-data state shown |
| TC-00503 | API | Source health | Expired token | GET /api/analytics/sources?sort | 401 Unauthorized |
| TC-00504 | API | Source health | Insufficient role | GET /api/analytics/sources?sort | 403 Forbidden |
| TC-00505 | API | Source health | Logged in | GET /api/analytics/sources/{id} | 200 + valid data |
| TC-00506 | API | Source health | Logged in | GET /api/analytics/sources/{id} with invalid input | 400/422 + error message |
| TC-00507 | API | Source health | Edge case | GET /api/analytics/sources/{id} at boundary value | Correct boundary handling |
| TC-00508 | API | Source health | No auth token | GET /api/analytics/sources/{id} | 401 Unauthorized |
| TC-00509 | frontend-UAT | Source health | Logged in | Open drill into source in UI | UI renders correctly |
| TC-00510 | frontend-UAT | Source health | No data | Open drill into source with no data | No-data state shown |
| TC-00511 | API | Source health | Expired token | GET /api/analytics/sources/{id} | 401 Unauthorized |
| TC-00512 | API | Source health | Insufficient role | GET /api/analytics/sources/{id} | 403 Forbidden |
| TC-00513 | API | Source health | Logged in | PUT /api/analytics/sources/{id} | 200 + valid data |
| TC-00514 | API | Source health | Logged in | PUT /api/analytics/sources/{id} with invalid input | 400/422 + error message |
| TC-00515 | API | Source health | Edge case | PUT /api/analytics/sources/{id} at boundary value | Correct boundary handling |
| TC-00516 | API | Source health | No auth token | PUT /api/analytics/sources/{id} | 401 Unauthorized |
| TC-00517 | frontend-UAT | Source health | Logged in | Open hide source in UI | UI renders correctly |
| TC-00518 | frontend-UAT | Source health | No data | Open hide source with no data | No-data state shown |
| TC-00519 | API | Source health | Expired token | PUT /api/analytics/sources/{id} | 401 Unauthorized |
| TC-00520 | API | Source health | Insufficient role | PUT /api/analytics/sources/{id} | 403 Forbidden |
| TC-00521 | API | Source health | Logged in | GET /api/analytics/sources?coverage_over_time | 200 + valid data |
| TC-00522 | API | Source health | Logged in | GET /api/analytics/sources?coverage_over_time with invalid input | 400/422 + error message |
| TC-00523 | API | Source health | Edge case | GET /api/analytics/sources?coverage_over_time at boundary value | Correct boundary handling |
| TC-00524 | API | Source health | No auth token | GET /api/analytics/sources?coverage_over_time | 401 Unauthorized |
| TC-00525 | frontend-UAT | Source health | Logged in | Open coverage over time in UI | UI renders correctly |
| TC-00526 | frontend-UAT | Source health | No data | Open coverage over time with no data | No-data state shown |
| TC-00527 | API | Source health | Expired token | GET /api/analytics/sources?coverage_over_time | 401 Unauthorized |
| TC-00528 | API | Source health | Insufficient role | GET /api/analytics/sources?coverage_over_time | 403 Forbidden |
| TC-00529 | API | Source health | Logged in | GET /api/analytics/sources?freshness | 200 + valid data |
| TC-00530 | API | Source health | Logged in | GET /api/analytics/sources?freshness with invalid input | 400/422 + error message |
| TC-00531 | API | Source health | Edge case | GET /api/analytics/sources?freshness at boundary value | Correct boundary handling |
| TC-00532 | API | Source health | No auth token | GET /api/analytics/sources?freshness | 401 Unauthorized |
| TC-00533 | frontend-UAT | Source health | Logged in | Open newest job per source in UI | UI renders correctly |
| TC-00534 | frontend-UAT | Source health | No data | Open newest job per source with no data | No-data state shown |
| TC-00535 | API | Source health | Expired token | GET /api/analytics/sources?freshness | 401 Unauthorized |
| TC-00536 | API | Source health | Insufficient role | GET /api/analytics/sources?freshness | 403 Forbidden |
| TC-00537 | API | Source health | Logged in | POST /api/analytics/sources | 200 + valid data |
| TC-00538 | API | Source health | Logged in | POST /api/analytics/sources with invalid input | 400/422 + error message |
| TC-00539 | API | Source health | Edge case | POST /api/analytics/sources at boundary value | Correct boundary handling |
| TC-00540 | API | Source health | No auth token | POST /api/analytics/sources | 401 Unauthorized |
| TC-00541 | frontend-UAT | Source health | Logged in | Open add custom source in UI | UI renders correctly |
| TC-00542 | frontend-UAT | Source health | No data | Open add custom source with no data | No-data state shown |
| TC-00543 | API | Source health | Expired token | POST /api/analytics/sources | 401 Unauthorized |
| TC-00544 | API | Source health | Insufficient role | POST /api/analytics/sources | 403 Forbidden |
| TC-00545 | API | Source health | Logged in | GET /api/analytics/sources?response_time | 200 + valid data |
| TC-00546 | API | Source health | Logged in | GET /api/analytics/sources?response_time with invalid input | 400/422 + error message |
| TC-00547 | API | Source health | Edge case | GET /api/analytics/sources?response_time at boundary value | Correct boundary handling |
| TC-00548 | API | Source health | No auth token | GET /api/analytics/sources?response_time | 401 Unauthorized |
| TC-00549 | frontend-UAT | Source health | Logged in | Open response time in UI | UI renders correctly |
| TC-00550 | frontend-UAT | Source health | No data | Open response time with no data | No-data state shown |
| TC-00551 | API | Source health | Expired token | GET /api/analytics/sources?response_time | 401 Unauthorized |
| TC-00552 | API | Source health | Insufficient role | GET /api/analytics/sources?response_time | 403 Forbidden |
| TC-00553 | API | Source health | Logged in | GET /api/analytics/sources?quality | 200 + valid data |
| TC-00554 | API | Source health | Logged in | GET /api/analytics/sources?quality with invalid input | 400/422 + error message |
| TC-00555 | API | Source health | Edge case | GET /api/analytics/sources?quality at boundary value | Correct boundary handling |
| TC-00556 | API | Source health | No auth token | GET /api/analytics/sources?quality | 401 Unauthorized |
| TC-00557 | frontend-UAT | Source health | Logged in | Open quality score in UI | UI renders correctly |
| TC-00558 | frontend-UAT | Source health | No data | Open quality score with no data | No-data state shown |
| TC-00559 | API | Source health | Expired token | GET /api/analytics/sources?quality | 401 Unauthorized |
| TC-00560 | API | Source health | Insufficient role | GET /api/analytics/sources?quality | 403 Forbidden |
| TC-00561 | API | Source health | Logged in | GET /api/analytics/sources?duplicates | 200 + valid data |
| TC-00562 | API | Source health | Logged in | GET /api/analytics/sources?duplicates with invalid input | 400/422 + error message |
| TC-00563 | API | Source health | Edge case | GET /api/analytics/sources?duplicates at boundary value | Correct boundary handling |
| TC-00564 | API | Source health | No auth token | GET /api/analytics/sources?duplicates | 401 Unauthorized |
| TC-00565 | frontend-UAT | Source health | Logged in | Open duplicate rate in UI | UI renders correctly |
| TC-00566 | frontend-UAT | Source health | No data | Open duplicate rate with no data | No-data state shown |
| TC-00567 | API | Source health | Expired token | GET /api/analytics/sources?duplicates | 401 Unauthorized |
| TC-00568 | API | Source health | Insufficient role | GET /api/analytics/sources?duplicates | 403 Forbidden |
| TC-00569 | API | Source health | Logged in | GET /api/analytics/sources?categories | 200 + valid data |
| TC-00570 | API | Source health | Logged in | GET /api/analytics/sources?categories with invalid input | 400/422 + error message |
| TC-00571 | API | Source health | Edge case | GET /api/analytics/sources?categories at boundary value | Correct boundary handling |
| TC-00572 | API | Source health | No auth token | GET /api/analytics/sources?categories | 401 Unauthorized |
| TC-00573 | frontend-UAT | Source health | Logged in | Open category coverage in UI | UI renders correctly |
| TC-00574 | frontend-UAT | Source health | No data | Open category coverage with no data | No-data state shown |
| TC-00575 | API | Source health | Expired token | GET /api/analytics/sources?categories | 401 Unauthorized |
| TC-00576 | API | Source health | Insufficient role | GET /api/analytics/sources?categories | 403 Forbidden |
| TC-00577 | API | Source health | Logged in | GET /api/analytics/sources?historical | 200 + valid data |
| TC-00578 | API | Source health | Logged in | GET /api/analytics/sources?historical with invalid input | 400/422 + error message |
| TC-00579 | API | Source health | Edge case | GET /api/analytics/sources?historical at boundary value | Correct boundary handling |
| TC-00580 | API | Source health | No auth token | GET /api/analytics/sources?historical | 401 Unauthorized |
| TC-00581 | frontend-UAT | Source health | Logged in | Open historical yield in UI | UI renders correctly |
| TC-00582 | frontend-UAT | Source health | No data | Open historical yield with no data | No-data state shown |
| TC-00583 | API | Source health | Expired token | GET /api/analytics/sources?historical | 401 Unauthorized |
| TC-00584 | API | Source health | Insufficient role | GET /api/analytics/sources?historical | 403 Forbidden |
| TC-00585 | API | Source health | Logged in | GET /api/analytics/sources?empty | 200 + valid data |
| TC-00586 | API | Source health | Logged in | GET /api/analytics/sources?empty with invalid input | 400/422 + error message |
| TC-00587 | API | Source health | Edge case | GET /api/analytics/sources?empty at boundary value | Correct boundary handling |
| TC-00588 | API | Source health | No auth token | GET /api/analytics/sources?empty | 401 Unauthorized |
| TC-00589 | frontend-UAT | Source health | Logged in | Open no-data state in UI | UI renders correctly |
| TC-00590 | frontend-UAT | Source health | No data | Open no-data state with no data | No-data state shown |
| TC-00591 | API | Source health | Expired token | GET /api/analytics/sources?empty | 401 Unauthorized |
| TC-00592 | API | Source health | Insufficient role | GET /api/analytics/sources?empty | 403 Forbidden |
| TC-00593 | API | Source health | Logged in | GET /api/analytics/sources?export | 200 + valid data |
| TC-00594 | API | Source health | Logged in | GET /api/analytics/sources?export with invalid input | 400/422 + error message |
| TC-00595 | API | Source health | Edge case | GET /api/analytics/sources?export at boundary value | Correct boundary handling |
| TC-00596 | API | Source health | No auth token | GET /api/analytics/sources?export | 401 Unauthorized |
| TC-00597 | frontend-UAT | Source health | Logged in | Open export source health in UI | UI renders correctly |
| TC-00598 | frontend-UAT | Source health | No data | Open export source health with no data | No-data state shown |
| TC-00599 | API | Source health | Expired token | GET /api/analytics/sources?export | 401 Unauthorized |
| TC-00600 | API | Source health | Insufficient role | GET /api/analytics/sources?export | 403 Forbidden |
### F5 — Form completeness

| TC-00601 | API | Form completeness | Logged in | GET /api/form/completeness | 200 + valid data |
| TC-00602 | API | Form completeness | Logged in | GET /api/form/completeness with invalid input | 400/422 + error message |
| TC-00603 | API | Form completeness | Edge case | GET /api/form/completeness at boundary value | Correct boundary handling |
| TC-00604 | API | Form completeness | No auth token | GET /api/form/completeness | 401 Unauthorized |
| TC-00605 | frontend-UAT | Form completeness | Logged in | Open get completeness in UI | UI renders correctly |
| TC-00606 | frontend-UAT | Form completeness | No data | Open get completeness with no data | No-data state shown |
| TC-00607 | API | Form completeness | Expired token | GET /api/form/completeness | 401 Unauthorized |
| TC-00608 | API | Form completeness | Insufficient role | GET /api/form/completeness | 403 Forbidden |
| TC-00609 | API | Form completeness | Logged in | GET /api/form/empty-fields | 200 + valid data |
| TC-00610 | API | Form completeness | Logged in | GET /api/form/empty-fields with invalid input | 400/422 + error message |
| TC-00611 | API | Form completeness | Edge case | GET /api/form/empty-fields at boundary value | Correct boundary handling |
| TC-00612 | API | Form completeness | No auth token | GET /api/form/empty-fields | 401 Unauthorized |
| TC-00613 | frontend-UAT | Form completeness | Logged in | Open get empty fields in UI | UI renders correctly |
| TC-00614 | frontend-UAT | Form completeness | No data | Open get empty fields with no data | No-data state shown |
| TC-00615 | API | Form completeness | Expired token | GET /api/form/empty-fields | 401 Unauthorized |
| TC-00616 | API | Form completeness | Insufficient role | GET /api/form/empty-fields | 403 Forbidden |
| TC-00617 | API | Form completeness | Logged in | POST /api/form/submit | 200 + valid data |
| TC-00618 | API | Form completeness | Logged in | POST /api/form/submit with invalid input | 400/422 + error message |
| TC-00619 | API | Form completeness | Edge case | POST /api/form/submit at boundary value | Correct boundary handling |
| TC-00620 | API | Form completeness | No auth token | POST /api/form/submit | 401 Unauthorized |
| TC-00621 | frontend-UAT | Form completeness | Logged in | Open submit form in UI | UI renders correctly |
| TC-00622 | frontend-UAT | Form completeness | No data | Open submit form with no data | No-data state shown |
| TC-00623 | API | Form completeness | Expired token | POST /api/form/submit | 401 Unauthorized |
| TC-00624 | API | Form completeness | Insufficient role | POST /api/form/submit | 403 Forbidden |
| TC-00625 | API | Form completeness | Logged in | POST /api/form/draft | 200 + valid data |
| TC-00626 | API | Form completeness | Logged in | POST /api/form/draft with invalid input | 400/422 + error message |
| TC-00627 | API | Form completeness | Edge case | POST /api/form/draft at boundary value | Correct boundary handling |
| TC-00628 | API | Form completeness | No auth token | POST /api/form/draft | 401 Unauthorized |
| TC-00629 | frontend-UAT | Form completeness | Logged in | Open save draft in UI | UI renders correctly |
| TC-00630 | frontend-UAT | Form completeness | No data | Open save draft with no data | No-data state shown |
| TC-00631 | API | Form completeness | Expired token | POST /api/form/draft | 401 Unauthorized |
| TC-00632 | API | Form completeness | Insufficient role | POST /api/form/draft | 403 Forbidden |
| TC-00633 | API | Form completeness | Logged in | GET /api/form/checklist | 200 + valid data |
| TC-00634 | API | Form completeness | Logged in | GET /api/form/checklist with invalid input | 400/422 + error message |
| TC-00635 | API | Form completeness | Edge case | GET /api/form/checklist at boundary value | Correct boundary handling |
| TC-00636 | API | Form completeness | No auth token | GET /api/form/checklist | 401 Unauthorized |
| TC-00637 | frontend-UAT | Form completeness | Logged in | Open get checklist in UI | UI renders correctly |
| TC-00638 | frontend-UAT | Form completeness | No data | Open get checklist with no data | No-data state shown |
| TC-00639 | API | Form completeness | Expired token | GET /api/form/checklist | 401 Unauthorized |
| TC-00640 | API | Form completeness | Insufficient role | GET /api/form/checklist | 403 Forbidden |
| TC-00641 | API | Form completeness | Logged in | GET /api/form/hints | 200 + valid data |
| TC-00642 | API | Form completeness | Logged in | GET /api/form/hints with invalid input | 400/422 + error message |
| TC-00643 | API | Form completeness | Edge case | GET /api/form/hints at boundary value | Correct boundary handling |
| TC-00644 | API | Form completeness | No auth token | GET /api/form/hints | 401 Unauthorized |
| TC-00645 | frontend-UAT | Form completeness | Logged in | Open get field hints in UI | UI renders correctly |
| TC-00646 | frontend-UAT | Form completeness | No data | Open get field hints with no data | No-data state shown |
| TC-00647 | API | Form completeness | Expired token | GET /api/form/hints | 401 Unauthorized |
| TC-00648 | API | Form completeness | Insufficient role | GET /api/form/hints | 403 Forbidden |
| TC-00649 | API | Form completeness | Logged in | GET /api/form/by-type | 200 + valid data |
| TC-00650 | API | Form completeness | Logged in | GET /api/form/by-type with invalid input | 400/422 + error message |
| TC-00651 | API | Form completeness | Edge case | GET /api/form/by-type at boundary value | Correct boundary handling |
| TC-00652 | API | Form completeness | No auth token | GET /api/form/by-type | 401 Unauthorized |
| TC-00653 | frontend-UAT | Form completeness | Logged in | Open required vs optional in UI | UI renders correctly |
| TC-00654 | frontend-UAT | Form completeness | No data | Open required vs optional with no data | No-data state shown |
| TC-00655 | API | Form completeness | Expired token | GET /api/form/by-type | 401 Unauthorized |
| TC-00656 | API | Form completeness | Insufficient role | GET /api/form/by-type | 403 Forbidden |
| TC-00657 | API | Form completeness | Logged in | POST /api/form/validate | 200 + valid data |
| TC-00658 | API | Form completeness | Logged in | POST /api/form/validate with invalid input | 400/422 + error message |
| TC-00659 | API | Form completeness | Edge case | POST /api/form/validate at boundary value | Correct boundary handling |
| TC-00660 | API | Form completeness | No auth token | POST /api/form/validate | 401 Unauthorized |
| TC-00661 | frontend-UAT | Form completeness | Logged in | Open validate form in UI | UI renders correctly |
| TC-00662 | frontend-UAT | Form completeness | No data | Open validate form with no data | No-data state shown |
| TC-00663 | API | Form completeness | Expired token | POST /api/form/validate | 401 Unauthorized |
| TC-00664 | API | Form completeness | Insufficient role | POST /api/form/validate | 403 Forbidden |
| TC-00665 | API | Form completeness | Logged in | GET /api/form/fields | 200 + valid data |
| TC-00666 | API | Form completeness | Logged in | GET /api/form/fields with invalid input | 400/422 + error message |
| TC-00667 | API | Form completeness | Edge case | GET /api/form/fields at boundary value | Correct boundary handling |
| TC-00668 | API | Form completeness | No auth token | GET /api/form/fields | 401 Unauthorized |
| TC-00669 | frontend-UAT | Form completeness | Logged in | Open list form fields in UI | UI renders correctly |
| TC-00670 | frontend-UAT | Form completeness | No data | Open list form fields with no data | No-data state shown |
| TC-00671 | API | Form completeness | Expired token | GET /api/form/fields | 401 Unauthorized |
| TC-00672 | API | Form completeness | Insufficient role | GET /api/form/fields | 403 Forbidden |
| TC-00673 | API | Form completeness | Logged in | PUT /api/form/fields/{id} | 200 + valid data |
| TC-00674 | API | Form completeness | Logged in | PUT /api/form/fields/{id} with invalid input | 400/422 + error message |
| TC-00675 | API | Form completeness | Edge case | PUT /api/form/fields/{id} at boundary value | Correct boundary handling |
| TC-00676 | API | Form completeness | No auth token | PUT /api/form/fields/{id} | 401 Unauthorized |
| TC-00677 | frontend-UAT | Form completeness | Logged in | Open edit field in UI | UI renders correctly |
| TC-00678 | frontend-UAT | Form completeness | No data | Open edit field with no data | No-data state shown |
| TC-00679 | API | Form completeness | Expired token | PUT /api/form/fields/{id} | 401 Unauthorized |
| TC-00680 | API | Form completeness | Insufficient role | PUT /api/form/fields/{id} | 403 Forbidden |
| TC-00681 | API | Form completeness | Logged in | POST /api/form/fields | 200 + valid data |
| TC-00682 | API | Form completeness | Logged in | POST /api/form/fields with invalid input | 400/422 + error message |
| TC-00683 | API | Form completeness | Edge case | POST /api/form/fields at boundary value | Correct boundary handling |
| TC-00684 | API | Form completeness | No auth token | POST /api/form/fields | 401 Unauthorized |
| TC-00685 | frontend-UAT | Form completeness | Logged in | Open add field in UI | UI renders correctly |
| TC-00686 | frontend-UAT | Form completeness | No data | Open add field with no data | No-data state shown |
| TC-00687 | API | Form completeness | Expired token | POST /api/form/fields | 401 Unauthorized |
| TC-00688 | API | Form completeness | Insufficient role | POST /api/form/fields | 403 Forbidden |
| TC-00689 | API | Form completeness | Logged in | DELETE /api/form/fields/{id} | 200 + valid data |
| TC-00690 | API | Form completeness | Logged in | DELETE /api/form/fields/{id} with invalid input | 400/422 + error message |
| TC-00691 | API | Form completeness | Edge case | DELETE /api/form/fields/{id} at boundary value | Correct boundary handling |
| TC-00692 | API | Form completeness | No auth token | DELETE /api/form/fields/{id} | 401 Unauthorized |
| TC-00693 | frontend-UAT | Form completeness | Logged in | Open remove field in UI | UI renders correctly |
| TC-00694 | frontend-UAT | Form completeness | No data | Open remove field with no data | No-data state shown |
| TC-00695 | API | Form completeness | Expired token | DELETE /api/form/fields/{id} | 401 Unauthorized |
| TC-00696 | API | Form completeness | Insufficient role | DELETE /api/form/fields/{id} | 403 Forbidden |
| TC-00697 | API | Form completeness | Logged in | GET /api/form/preview | 200 + valid data |
| TC-00698 | API | Form completeness | Logged in | GET /api/form/preview with invalid input | 400/422 + error message |
| TC-00699 | API | Form completeness | Edge case | GET /api/form/preview at boundary value | Correct boundary handling |
| TC-00700 | API | Form completeness | No auth token | GET /api/form/preview | 401 Unauthorized |
| TC-00701 | frontend-UAT | Form completeness | Logged in | Open form preview in UI | UI renders correctly |
| TC-00702 | frontend-UAT | Form completeness | No data | Open form preview with no data | No-data state shown |
| TC-00703 | API | Form completeness | Expired token | GET /api/form/preview | 401 Unauthorized |
| TC-00704 | API | Form completeness | Insufficient role | GET /api/form/preview | 403 Forbidden |
| TC-00705 | API | Form completeness | Logged in | GET /api/form/empty | 200 + valid data |
| TC-00706 | API | Form completeness | Logged in | GET /api/form/empty with invalid input | 400/422 + error message |
| TC-00707 | API | Form completeness | Edge case | GET /api/form/empty at boundary value | Correct boundary handling |
| TC-00708 | API | Form completeness | No auth token | GET /api/form/empty | 401 Unauthorized |
| TC-00709 | frontend-UAT | Form completeness | Logged in | Open no-data state in UI | UI renders correctly |
| TC-00710 | frontend-UAT | Form completeness | No data | Open no-data state with no data | No-data state shown |
| TC-00711 | API | Form completeness | Expired token | GET /api/form/empty | 401 Unauthorized |
| TC-00712 | API | Form completeness | Insufficient role | GET /api/form/empty | 403 Forbidden |
| TC-00713 | API | Form completeness | Logged in | GET /api/form/export | 200 + valid data |
| TC-00714 | API | Form completeness | Logged in | GET /api/form/export with invalid input | 400/422 + error message |
| TC-00715 | API | Form completeness | Edge case | GET /api/form/export at boundary value | Correct boundary handling |
| TC-00716 | API | Form completeness | No auth token | GET /api/form/export | 401 Unauthorized |
| TC-00717 | frontend-UAT | Form completeness | Logged in | Open export form in UI | UI renders correctly |
| TC-00718 | frontend-UAT | Form completeness | No data | Open export form with no data | No-data state shown |
| TC-00719 | API | Form completeness | Expired token | GET /api/form/export | 401 Unauthorized |
| TC-00720 | API | Form completeness | Insufficient role | GET /api/form/export | 403 Forbidden |
### F6 — Kanban board

| TC-00721 | API | Kanban board | Logged in | GET /api/jobs?board=true | 200 + valid data |
| TC-00722 | API | Kanban board | Logged in | GET /api/jobs?board=true with invalid input | 400/422 + error message |
| TC-00723 | API | Kanban board | Edge case | GET /api/jobs?board=true at boundary value | Correct boundary handling |
| TC-00724 | API | Kanban board | No auth token | GET /api/jobs?board=true | 401 Unauthorized |
| TC-00725 | frontend-UAT | Kanban board | Logged in | Open get kanban board in UI | UI renders correctly |
| TC-00726 | frontend-UAT | Kanban board | No data | Open get kanban board with no data | No-data state shown |
| TC-00727 | API | Kanban board | Expired token | GET /api/jobs?board=true | 401 Unauthorized |
| TC-00728 | API | Kanban board | Insufficient role | GET /api/jobs?board=true | 403 Forbidden |
| TC-00729 | API | Kanban board | Logged in | PUT /api/jobs/{id}/status | 200 + valid data |
| TC-00730 | API | Kanban board | Logged in | PUT /api/jobs/{id}/status with invalid input | 400/422 + error message |
| TC-00731 | API | Kanban board | Edge case | PUT /api/jobs/{id}/status at boundary value | Correct boundary handling |
| TC-00732 | API | Kanban board | No auth token | PUT /api/jobs/{id}/status | 401 Unauthorized |
| TC-00733 | frontend-UAT | Kanban board | Logged in | Open update status in UI | UI renders correctly |
| TC-00734 | frontend-UAT | Kanban board | No data | Open update status with no data | No-data state shown |
| TC-00735 | API | Kanban board | Expired token | PUT /api/jobs/{id}/status | 401 Unauthorized |
| TC-00736 | API | Kanban board | Insufficient role | PUT /api/jobs/{id}/status | 403 Forbidden |
| TC-00737 | API | Kanban board | Logged in | GET /api/jobs/columns | 200 + valid data |
| TC-00738 | API | Kanban board | Logged in | GET /api/jobs/columns with invalid input | 400/422 + error message |
| TC-00739 | API | Kanban board | Edge case | GET /api/jobs/columns at boundary value | Correct boundary handling |
| TC-00740 | API | Kanban board | No auth token | GET /api/jobs/columns | 401 Unauthorized |
| TC-00741 | frontend-UAT | Kanban board | Logged in | Open get column counts in UI | UI renders correctly |
| TC-00742 | frontend-UAT | Kanban board | No data | Open get column counts with no data | No-data state shown |
| TC-00743 | API | Kanban board | Expired token | GET /api/jobs/columns | 401 Unauthorized |
| TC-00744 | API | Kanban board | Insufficient role | GET /api/jobs/columns | 403 Forbidden |
| TC-00745 | API | Kanban board | Logged in | GET /api/jobs/card/{id} | 200 + valid data |
| TC-00746 | API | Kanban board | Logged in | GET /api/jobs/card/{id} with invalid input | 400/422 + error message |
| TC-00747 | API | Kanban board | Edge case | GET /api/jobs/card/{id} at boundary value | Correct boundary handling |
| TC-00748 | API | Kanban board | No auth token | GET /api/jobs/card/{id} | 401 Unauthorized |
| TC-00749 | frontend-UAT | Kanban board | Logged in | Open get card details in UI | UI renders correctly |
| TC-00750 | frontend-UAT | Kanban board | No data | Open get card details with no data | No-data state shown |
| TC-00751 | API | Kanban board | Expired token | GET /api/jobs/card/{id} | 401 Unauthorized |
| TC-00752 | API | Kanban board | Insufficient role | GET /api/jobs/card/{id} | 403 Forbidden |
| TC-00753 | API | Kanban board | Logged in | GET /api/jobs?filter=source | 200 + valid data |
| TC-00754 | API | Kanban board | Logged in | GET /api/jobs?filter=source with invalid input | 400/422 + error message |
| TC-00755 | API | Kanban board | Edge case | GET /api/jobs?filter=source at boundary value | Correct boundary handling |
| TC-00756 | API | Kanban board | No auth token | GET /api/jobs?filter=source | 401 Unauthorized |
| TC-00757 | frontend-UAT | Kanban board | Logged in | Open filter by source in UI | UI renders correctly |
| TC-00758 | frontend-UAT | Kanban board | No data | Open filter by source with no data | No-data state shown |
| TC-00759 | API | Kanban board | Expired token | GET /api/jobs?filter=source | 401 Unauthorized |
| TC-00760 | API | Kanban board | Insufficient role | GET /api/jobs?filter=source | 403 Forbidden |
| TC-00761 | API | Kanban board | Logged in | GET /api/jobs/search | 200 + valid data |
| TC-00762 | API | Kanban board | Logged in | GET /api/jobs/search with invalid input | 400/422 + error message |
| TC-00763 | API | Kanban board | Edge case | GET /api/jobs/search at boundary value | Correct boundary handling |
| TC-00764 | API | Kanban board | No auth token | GET /api/jobs/search | 401 Unauthorized |
| TC-00765 | frontend-UAT | Kanban board | Logged in | Open search card in UI | UI renders correctly |
| TC-00766 | frontend-UAT | Kanban board | No data | Open search card with no data | No-data state shown |
| TC-00767 | API | Kanban board | Expired token | GET /api/jobs/search | 401 Unauthorized |
| TC-00768 | API | Kanban board | Insufficient role | GET /api/jobs/search | 403 Forbidden |
| TC-00769 | API | Kanban board | Logged in | GET /api/jobs?clear_filter | 200 + valid data |
| TC-00770 | API | Kanban board | Logged in | GET /api/jobs?clear_filter with invalid input | 400/422 + error message |
| TC-00771 | API | Kanban board | Edge case | GET /api/jobs?clear_filter at boundary value | Correct boundary handling |
| TC-00772 | API | Kanban board | No auth token | GET /api/jobs?clear_filter | 401 Unauthorized |
| TC-00773 | frontend-UAT | Kanban board | Logged in | Open clear filter in UI | UI renders correctly |
| TC-00774 | frontend-UAT | Kanban board | No data | Open clear filter with no data | No-data state shown |
| TC-00775 | API | Kanban board | Expired token | GET /api/jobs?clear_filter | 401 Unauthorized |
| TC-00776 | API | Kanban board | Insufficient role | GET /api/jobs?clear_filter | 403 Forbidden |
| TC-00777 | API | Kanban board | Logged in | GET /api/jobs?fit_score | 200 + valid data |
| TC-00778 | API | Kanban board | Logged in | GET /api/jobs?fit_score with invalid input | 400/422 + error message |
| TC-00779 | API | Kanban board | Edge case | GET /api/jobs?fit_score at boundary value | Correct boundary handling |
| TC-00780 | API | Kanban board | No auth token | GET /api/jobs?fit_score | 401 Unauthorized |
| TC-00781 | frontend-UAT | Kanban board | Logged in | Open fit score on card in UI | UI renders correctly |
| TC-00782 | frontend-UAT | Kanban board | No data | Open fit score on card with no data | No-data state shown |
| TC-00783 | API | Kanban board | Expired token | GET /api/jobs?fit_score | 401 Unauthorized |
| TC-00784 | API | Kanban board | Insufficient role | GET /api/jobs?fit_score | 403 Forbidden |
| TC-00785 | API | Kanban board | Logged in | GET /api/jobs?last_updated | 200 + valid data |
| TC-00786 | API | Kanban board | Logged in | GET /api/jobs?last_updated with invalid input | 400/422 + error message |
| TC-00787 | API | Kanban board | Edge case | GET /api/jobs?last_updated at boundary value | Correct boundary handling |
| TC-00788 | API | Kanban board | No auth token | GET /api/jobs?last_updated | 401 Unauthorized |
| TC-00789 | frontend-UAT | Kanban board | Logged in | Open last updated time in UI | UI renders correctly |
| TC-00790 | frontend-UAT | Kanban board | No data | Open last updated time with no data | No-data state shown |
| TC-00791 | API | Kanban board | Expired token | GET /api/jobs?last_updated | 401 Unauthorized |
| TC-00792 | API | Kanban board | Insufficient role | GET /api/jobs?last_updated | 403 Forbidden |
| TC-00793 | API | Kanban board | Logged in | GET /api/jobs?empty | 200 + valid data |
| TC-00794 | API | Kanban board | Logged in | GET /api/jobs?empty with invalid input | 400/422 + error message |
| TC-00795 | API | Kanban board | Edge case | GET /api/jobs?empty at boundary value | Correct boundary handling |
| TC-00796 | API | Kanban board | No auth token | GET /api/jobs?empty | 401 Unauthorized |
| TC-00797 | frontend-UAT | Kanban board | Logged in | Open no-data state in UI | UI renders correctly |
| TC-00798 | frontend-UAT | Kanban board | No data | Open no-data state with no data | No-data state shown |
| TC-00799 | API | Kanban board | Expired token | GET /api/jobs?empty | 401 Unauthorized |
| TC-00800 | API | Kanban board | Insufficient role | GET /api/jobs?empty | 403 Forbidden |
| TC-00801 | API | Kanban board | Logged in | GET /api/jobs?responsive | 200 + valid data |
| TC-00802 | API | Kanban board | Logged in | GET /api/jobs?responsive with invalid input | 400/422 + error message |
| TC-00803 | API | Kanban board | Edge case | GET /api/jobs?responsive at boundary value | Correct boundary handling |
| TC-00804 | API | Kanban board | No auth token | GET /api/jobs?responsive | 401 Unauthorized |
| TC-00805 | frontend-UAT | Kanban board | Logged in | Open responsive layout in UI | UI renders correctly |
| TC-00806 | frontend-UAT | Kanban board | No data | Open responsive layout with no data | No-data state shown |
| TC-00807 | API | Kanban board | Expired token | GET /api/jobs?responsive | 401 Unauthorized |
| TC-00808 | API | Kanban board | Insufficient role | GET /api/jobs?responsive | 403 Forbidden |
| TC-00809 | API | Kanban board | Logged in | POST /api/jobs/drag | 200 + valid data |
| TC-00810 | API | Kanban board | Logged in | POST /api/jobs/drag with invalid input | 400/422 + error message |
| TC-00811 | API | Kanban board | Edge case | POST /api/jobs/drag at boundary value | Correct boundary handling |
| TC-00812 | API | Kanban board | No auth token | POST /api/jobs/drag | 401 Unauthorized |
| TC-00813 | frontend-UAT | Kanban board | Logged in | Open drag job in UI | UI renders correctly |
| TC-00814 | frontend-UAT | Kanban board | No data | Open drag job with no data | No-data state shown |
| TC-00815 | API | Kanban board | Expired token | POST /api/jobs/drag | 401 Unauthorized |
| TC-00816 | API | Kanban board | Insufficient role | POST /api/jobs/drag | 403 Forbidden |
| TC-00817 | API | Kanban board | Logged in | GET /api/jobs?color | 200 + valid data |
| TC-00818 | API | Kanban board | Logged in | GET /api/jobs?color with invalid input | 400/422 + error message |
| TC-00819 | API | Kanban board | Edge case | GET /api/jobs?color at boundary value | Correct boundary handling |
| TC-00820 | API | Kanban board | No auth token | GET /api/jobs?color | 401 Unauthorized |
| TC-00821 | frontend-UAT | Kanban board | Logged in | Open color-coded columns in UI | UI renders correctly |
| TC-00822 | frontend-UAT | Kanban board | No data | Open color-coded columns with no data | No-data state shown |
| TC-00823 | API | Kanban board | Expired token | GET /api/jobs?color | 401 Unauthorized |
| TC-00824 | API | Kanban board | Insufficient role | GET /api/jobs?color | 403 Forbidden |
| TC-00825 | API | Kanban board | Logged in | GET /api/jobs?counts | 200 + valid data |
| TC-00826 | API | Kanban board | Logged in | GET /api/jobs?counts with invalid input | 400/422 + error message |
| TC-00827 | API | Kanban board | Edge case | GET /api/jobs?counts at boundary value | Correct boundary handling |
| TC-00828 | API | Kanban board | No auth token | GET /api/jobs?counts | 401 Unauthorized |
| TC-00829 | frontend-UAT | Kanban board | Logged in | Open column counts in UI | UI renders correctly |
| TC-00830 | frontend-UAT | Kanban board | No data | Open column counts with no data | No-data state shown |
| TC-00831 | API | Kanban board | Expired token | GET /api/jobs?counts | 401 Unauthorized |
| TC-00832 | API | Kanban board | Insufficient role | GET /api/jobs?counts | 403 Forbidden |
| TC-00833 | API | Kanban board | Logged in | GET /api/jobs?export | 200 + valid data |
| TC-00834 | API | Kanban board | Logged in | GET /api/jobs?export with invalid input | 400/422 + error message |
| TC-00835 | API | Kanban board | Edge case | GET /api/jobs?export at boundary value | Correct boundary handling |
| TC-00836 | API | Kanban board | No auth token | GET /api/jobs?export | 401 Unauthorized |
| TC-00837 | frontend-UAT | Kanban board | Logged in | Open export board in UI | UI renders correctly |
| TC-00838 | frontend-UAT | Kanban board | No data | Open export board with no data | No-data state shown |
| TC-00839 | API | Kanban board | Expired token | GET /api/jobs?export | 401 Unauthorized |
| TC-00840 | API | Kanban board | Insufficient role | GET /api/jobs?export | 403 Forbidden |
### F7 — Job comparison

| TC-00841 | API | Job comparison | Logged in | GET /api/jobs/compare | 200 + valid data |
| TC-00842 | API | Job comparison | Logged in | GET /api/jobs/compare with invalid input | 400/422 + error message |
| TC-00843 | API | Job comparison | Edge case | GET /api/jobs/compare at boundary value | Correct boundary handling |
| TC-00844 | API | Job comparison | No auth token | GET /api/jobs/compare | 401 Unauthorized |
| TC-00845 | frontend-UAT | Job comparison | Logged in | Open compare jobs in UI | UI renders correctly |
| TC-00846 | frontend-UAT | Job comparison | No data | Open compare jobs with no data | No-data state shown |
| TC-00847 | API | Job comparison | Expired token | GET /api/jobs/compare | 401 Unauthorized |
| TC-00848 | API | Job comparison | Insufficient role | GET /api/jobs/compare | 403 Forbidden |
| TC-00849 | API | Job comparison | Logged in | POST /api/jobs/compare/select | 200 + valid data |
| TC-00850 | API | Job comparison | Logged in | POST /api/jobs/compare/select with invalid input | 400/422 + error message |
| TC-00851 | API | Job comparison | Edge case | POST /api/jobs/compare/select at boundary value | Correct boundary handling |
| TC-00852 | API | Job comparison | No auth token | POST /api/jobs/compare/select | 401 Unauthorized |
| TC-00853 | frontend-UAT | Job comparison | Logged in | Open select jobs in UI | UI renders correctly |
| TC-00854 | frontend-UAT | Job comparison | No data | Open select jobs with no data | No-data state shown |
| TC-00855 | API | Job comparison | Expired token | POST /api/jobs/compare/select | 401 Unauthorized |
| TC-00856 | API | Job comparison | Insufficient role | POST /api/jobs/compare/select | 403 Forbidden |
| TC-00857 | API | Job comparison | Logged in | GET /api/jobs/compare/fit-diff | 200 + valid data |
| TC-00858 | API | Job comparison | Logged in | GET /api/jobs/compare/fit-diff with invalid input | 400/422 + error message |
| TC-00859 | API | Job comparison | Edge case | GET /api/jobs/compare/fit-diff at boundary value | Correct boundary handling |
| TC-00860 | API | Job comparison | No auth token | GET /api/jobs/compare/fit-diff | 401 Unauthorized |
| TC-00861 | frontend-UAT | Job comparison | Logged in | Open fit score difference in UI | UI renders correctly |
| TC-00862 | frontend-UAT | Job comparison | No data | Open fit score difference with no data | No-data state shown |
| TC-00863 | API | Job comparison | Expired token | GET /api/jobs/compare/fit-diff | 401 Unauthorized |
| TC-00864 | API | Job comparison | Insufficient role | GET /api/jobs/compare/fit-diff | 403 Forbidden |
| TC-00865 | API | Job comparison | Logged in | POST /api/jobs/compare/clear | 200 + valid data |
| TC-00866 | API | Job comparison | Logged in | POST /api/jobs/compare/clear with invalid input | 400/422 + error message |
| TC-00867 | API | Job comparison | Edge case | POST /api/jobs/compare/clear at boundary value | Correct boundary handling |
| TC-00868 | API | Job comparison | No auth token | POST /api/jobs/compare/clear | 401 Unauthorized |
| TC-00869 | frontend-UAT | Job comparison | Logged in | Open clear comparison in UI | UI renders correctly |
| TC-00870 | frontend-UAT | Job comparison | No data | Open clear comparison with no data | No-data state shown |
| TC-00871 | API | Job comparison | Expired token | POST /api/jobs/compare/clear | 401 Unauthorized |
| TC-00872 | API | Job comparison | Insufficient role | POST /api/jobs/compare/clear | 403 Forbidden |
| TC-00873 | API | Job comparison | Logged in | PUT /api/jobs/compare/sort | 200 + valid data |
| TC-00874 | API | Job comparison | Logged in | PUT /api/jobs/compare/sort with invalid input | 400/422 + error message |
| TC-00875 | API | Job comparison | Edge case | PUT /api/jobs/compare/sort at boundary value | Correct boundary handling |
| TC-00876 | API | Job comparison | No auth token | PUT /api/jobs/compare/sort | 401 Unauthorized |
| TC-00877 | frontend-UAT | Job comparison | Logged in | Open sort columns in UI | UI renders correctly |
| TC-00878 | frontend-UAT | Job comparison | No data | Open sort columns with no data | No-data state shown |
| TC-00879 | API | Job comparison | Expired token | PUT /api/jobs/compare/sort | 401 Unauthorized |
| TC-00880 | API | Job comparison | Insufficient role | PUT /api/jobs/compare/sort | 403 Forbidden |
| TC-00881 | API | Job comparison | Logged in | GET /api/jobs/compare/export | 200 + valid data |
| TC-00882 | API | Job comparison | Logged in | GET /api/jobs/compare/export with invalid input | 400/422 + error message |
| TC-00883 | API | Job comparison | Edge case | GET /api/jobs/compare/export at boundary value | Correct boundary handling |
| TC-00884 | API | Job comparison | No auth token | GET /api/jobs/compare/export | 401 Unauthorized |
| TC-00885 | frontend-UAT | Job comparison | Logged in | Open export comparison in UI | UI renders correctly |
| TC-00886 | frontend-UAT | Job comparison | No data | Open export comparison with no data | No-data state shown |
| TC-00887 | API | Job comparison | Expired token | GET /api/jobs/compare/export | 401 Unauthorized |
| TC-00888 | API | Job comparison | Insufficient role | GET /api/jobs/compare/export | 403 Forbidden |
| TC-00889 | API | Job comparison | Logged in | GET /api/jobs/compare/table | 200 + valid data |
| TC-00890 | API | Job comparison | Logged in | GET /api/jobs/compare/table with invalid input | 400/422 + error message |
| TC-00891 | API | Job comparison | Edge case | GET /api/jobs/compare/table at boundary value | Correct boundary handling |
| TC-00892 | API | Job comparison | No auth token | GET /api/jobs/compare/table | 401 Unauthorized |
| TC-00893 | frontend-UAT | Job comparison | Logged in | Open compare table in UI | UI renders correctly |
| TC-00894 | frontend-UAT | Job comparison | No data | Open compare table with no data | No-data state shown |
| TC-00895 | API | Job comparison | Expired token | GET /api/jobs/compare/table | 401 Unauthorized |
| TC-00896 | API | Job comparison | Insufficient role | GET /api/jobs/compare/table | 403 Forbidden |
| TC-00897 | API | Job comparison | Logged in | GET /api/jobs/compare/salary | 200 + valid data |
| TC-00898 | API | Job comparison | Logged in | GET /api/jobs/compare/salary with invalid input | 400/422 + error message |
| TC-00899 | API | Job comparison | Edge case | GET /api/jobs/compare/salary at boundary value | Correct boundary handling |
| TC-00900 | API | Job comparison | No auth token | GET /api/jobs/compare/salary | 401 Unauthorized |
| TC-00901 | frontend-UAT | Job comparison | Logged in | Open salary comparison in UI | UI renders correctly |
| TC-00902 | frontend-UAT | Job comparison | No data | Open salary comparison with no data | No-data state shown |
| TC-00903 | API | Job comparison | Expired token | GET /api/jobs/compare/salary | 401 Unauthorized |
| TC-00904 | API | Job comparison | Insufficient role | GET /api/jobs/compare/salary | 403 Forbidden |
| TC-00905 | API | Job comparison | Logged in | GET /api/jobs/compare?ids=1,2 | 200 + valid data |
| TC-00906 | API | Job comparison | Logged in | GET /api/jobs/compare?ids=1,2 with invalid input | 400/422 + error message |
| TC-00907 | API | Job comparison | Edge case | GET /api/jobs/compare?ids=1,2 at boundary value | Correct boundary handling |
| TC-00908 | API | Job comparison | No auth token | GET /api/jobs/compare?ids=1,2 | 401 Unauthorized |
| TC-00909 | frontend-UAT | Job comparison | Logged in | Open two jobs in UI | UI renders correctly |
| TC-00910 | frontend-UAT | Job comparison | No data | Open two jobs with no data | No-data state shown |
| TC-00911 | API | Job comparison | Expired token | GET /api/jobs/compare?ids=1,2 | 401 Unauthorized |
| TC-00912 | API | Job comparison | Insufficient role | GET /api/jobs/compare?ids=1,2 | 403 Forbidden |
| TC-00913 | API | Job comparison | Logged in | GET /api/jobs/compare?ids=1 | 200 + valid data |
| TC-00914 | API | Job comparison | Logged in | GET /api/jobs/compare?ids=1 with invalid input | 400/422 + error message |
| TC-00915 | API | Job comparison | Edge case | GET /api/jobs/compare?ids=1 at boundary value | Correct boundary handling |
| TC-00916 | API | Job comparison | No auth token | GET /api/jobs/compare?ids=1 | 401 Unauthorized |
| TC-00917 | frontend-UAT | Job comparison | Logged in | Open one job error in UI | UI renders correctly |
| TC-00918 | frontend-UAT | Job comparison | No data | Open one job error with no data | No-data state shown |
| TC-00919 | API | Job comparison | Expired token | GET /api/jobs/compare?ids=1 | 401 Unauthorized |
| TC-00920 | API | Job comparison | Insufficient role | GET /api/jobs/compare?ids=1 | 403 Forbidden |
| TC-00921 | API | Job comparison | Logged in | GET /api/jobs/compare?empty | 200 + valid data |
| TC-00922 | API | Job comparison | Logged in | GET /api/jobs/compare?empty with invalid input | 400/422 + error message |
| TC-00923 | API | Job comparison | Edge case | GET /api/jobs/compare?empty at boundary value | Correct boundary handling |
| TC-00924 | API | Job comparison | No auth token | GET /api/jobs/compare?empty | 401 Unauthorized |
| TC-00925 | frontend-UAT | Job comparison | Logged in | Open no-data state in UI | UI renders correctly |
| TC-00926 | frontend-UAT | Job comparison | No data | Open no-data state with no data | No-data state shown |
| TC-00927 | API | Job comparison | Expired token | GET /api/jobs/compare?empty | 401 Unauthorized |
| TC-00928 | API | Job comparison | Insufficient role | GET /api/jobs/compare?empty | 403 Forbidden |
| TC-00929 | API | Job comparison | Logged in | GET /api/jobs/compare?three | 200 + valid data |
| TC-00930 | API | Job comparison | Logged in | GET /api/jobs/compare?three with invalid input | 400/422 + error message |
| TC-00931 | API | Job comparison | Edge case | GET /api/jobs/compare?three at boundary value | Correct boundary handling |
| TC-00932 | API | Job comparison | No auth token | GET /api/jobs/compare?three | 401 Unauthorized |
| TC-00933 | frontend-UAT | Job comparison | Logged in | Open three jobs in UI | UI renders correctly |
| TC-00934 | frontend-UAT | Job comparison | No data | Open three jobs with no data | No-data state shown |
| TC-00935 | API | Job comparison | Expired token | GET /api/jobs/compare?three | 401 Unauthorized |
| TC-00936 | API | Job comparison | Insufficient role | GET /api/jobs/compare?three | 403 Forbidden |
| TC-00937 | API | Job comparison | Logged in | GET /api/jobs/compare?skills | 200 + valid data |
| TC-00938 | API | Job comparison | Logged in | GET /api/jobs/compare?skills with invalid input | 400/422 + error message |
| TC-00939 | API | Job comparison | Edge case | GET /api/jobs/compare?skills at boundary value | Correct boundary handling |
| TC-00940 | API | Job comparison | No auth token | GET /api/jobs/compare?skills | 401 Unauthorized |
| TC-00941 | frontend-UAT | Job comparison | Logged in | Open skills comparison in UI | UI renders correctly |
| TC-00942 | frontend-UAT | Job comparison | No data | Open skills comparison with no data | No-data state shown |
| TC-00943 | API | Job comparison | Expired token | GET /api/jobs/compare?skills | 401 Unauthorized |
| TC-00944 | API | Job comparison | Insufficient role | GET /api/jobs/compare?skills | 403 Forbidden |
| TC-00945 | API | Job comparison | Logged in | GET /api/jobs/compare?pay | 200 + valid data |
| TC-00946 | API | Job comparison | Logged in | GET /api/jobs/compare?pay with invalid input | 400/422 + error message |
| TC-00947 | API | Job comparison | Edge case | GET /api/jobs/compare?pay at boundary value | Correct boundary handling |
| TC-00948 | API | Job comparison | No auth token | GET /api/jobs/compare?pay | 401 Unauthorized |
| TC-00949 | frontend-UAT | Job comparison | Logged in | Open pay comparison in UI | UI renders correctly |
| TC-00950 | frontend-UAT | Job comparison | No data | Open pay comparison with no data | No-data state shown |
| TC-00951 | API | Job comparison | Expired token | GET /api/jobs/compare?pay | 401 Unauthorized |
| TC-00952 | API | Job comparison | Insufficient role | GET /api/jobs/compare?pay | 403 Forbidden |
| TC-00953 | API | Job comparison | Logged in | GET /api/jobs/compare?hover | 200 + valid data |
| TC-00954 | API | Job comparison | Logged in | GET /api/jobs/compare?hover with invalid input | 400/422 + error message |
| TC-00955 | API | Job comparison | Edge case | GET /api/jobs/compare?hover at boundary value | Correct boundary handling |
| TC-00956 | API | Job comparison | No auth token | GET /api/jobs/compare?hover | 401 Unauthorized |
| TC-00957 | frontend-UAT | Job comparison | Logged in | Open hover tooltip in UI | UI renders correctly |
| TC-00958 | frontend-UAT | Job comparison | No data | Open hover tooltip with no data | No-data state shown |
| TC-00959 | API | Job comparison | Expired token | GET /api/jobs/compare?hover | 401 Unauthorized |
| TC-00960 | API | Job comparison | Insufficient role | GET /api/jobs/compare?hover | 403 Forbidden |
### F8 — Application timeline

| TC-00961 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline | 200 + valid data |
| TC-00962 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline with invalid input | 400/422 + error message |
| TC-00963 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline at boundary value | Correct boundary handling |
| TC-00964 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline | 401 Unauthorized |
| TC-00965 | frontend-UAT | Application timeline | Logged in | Open get timeline in UI | UI renders correctly |
| TC-00966 | frontend-UAT | Application timeline | No data | Open get timeline with no data | No-data state shown |
| TC-00967 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline | 401 Unauthorized |
| TC-00968 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline | 403 Forbidden |
| TC-00969 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/stages | 200 + valid data |
| TC-00970 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/stages with invalid input | 400/422 + error message |
| TC-00971 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline/stages at boundary value | Correct boundary handling |
| TC-00972 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline/stages | 401 Unauthorized |
| TC-00973 | frontend-UAT | Application timeline | Logged in | Open stages with dates in UI | UI renders correctly |
| TC-00974 | frontend-UAT | Application timeline | No data | Open stages with dates with no data | No-data state shown |
| TC-00975 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline/stages | 401 Unauthorized |
| TC-00976 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline/stages | 403 Forbidden |
| TC-00977 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/stalled | 200 + valid data |
| TC-00978 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/stalled with invalid input | 400/422 + error message |
| TC-00979 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline/stalled at boundary value | Correct boundary handling |
| TC-00980 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline/stalled | 401 Unauthorized |
| TC-00981 | frontend-UAT | Application timeline | Logged in | Open stalled stage in UI | UI renders correctly |
| TC-00982 | frontend-UAT | Application timeline | No data | Open stalled stage with no data | No-data state shown |
| TC-00983 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline/stalled | 401 Unauthorized |
| TC-00984 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline/stalled | 403 Forbidden |
| TC-00985 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/next | 200 + valid data |
| TC-00986 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/next with invalid input | 400/422 + error message |
| TC-00987 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline/next at boundary value | Correct boundary handling |
| TC-00988 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline/next | 401 Unauthorized |
| TC-00989 | frontend-UAT | Application timeline | Logged in | Open next action in UI | UI renders correctly |
| TC-00990 | frontend-UAT | Application timeline | No data | Open next action with no data | No-data state shown |
| TC-00991 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline/next | 401 Unauthorized |
| TC-00992 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline/next | 403 Forbidden |
| TC-00993 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/rejection | 200 + valid data |
| TC-00994 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/rejection with invalid input | 400/422 + error message |
| TC-00995 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline/rejection at boundary value | Correct boundary handling |
| TC-00996 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline/rejection | 401 Unauthorized |
| TC-00997 | frontend-UAT | Application timeline | Logged in | Open rejection reasons in UI | UI renders correctly |
| TC-00998 | frontend-UAT | Application timeline | No data | Open rejection reasons with no data | No-data state shown |
| TC-00999 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline/rejection | 401 Unauthorized |
| TC-01000 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline/rejection | 403 Forbidden |
| TC-01001 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/focus | 200 + valid data |
| TC-01002 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/focus with invalid input | 400/422 + error message |
| TC-01003 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline/focus at boundary value | Correct boundary handling |
| TC-01004 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline/focus | 401 Unauthorized |
| TC-01005 | frontend-UAT | Application timeline | Logged in | Open specific job in UI | UI renders correctly |
| TC-01006 | frontend-UAT | Application timeline | No data | Open specific job with no data | No-data state shown |
| TC-01007 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline/focus | 401 Unauthorized |
| TC-01008 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline/focus | 403 Forbidden |
| TC-01009 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/durations | 200 + valid data |
| TC-01010 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline/durations with invalid input | 400/422 + error message |
| TC-01011 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline/durations at boundary value | Correct boundary handling |
| TC-01012 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline/durations | 401 Unauthorized |
| TC-01013 | frontend-UAT | Application timeline | Logged in | Open stage durations in UI | UI renders correctly |
| TC-01014 | frontend-UAT | Application timeline | No data | Open stage durations with no data | No-data state shown |
| TC-01015 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline/durations | 401 Unauthorized |
| TC-01016 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline/durations | 403 Forbidden |
| TC-01017 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?empty | 200 + valid data |
| TC-01018 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?empty with invalid input | 400/422 + error message |
| TC-01019 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?empty at boundary value | Correct boundary handling |
| TC-01020 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?empty | 401 Unauthorized |
| TC-01021 | frontend-UAT | Application timeline | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01022 | frontend-UAT | Application timeline | No data | Open no-data state with no data | No-data state shown |
| TC-01023 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?empty | 401 Unauthorized |
| TC-01024 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?empty | 403 Forbidden |
| TC-01025 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?responsive | 200 + valid data |
| TC-01026 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?responsive with invalid input | 400/422 + error message |
| TC-01027 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?responsive at boundary value | Correct boundary handling |
| TC-01028 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?responsive | 401 Unauthorized |
| TC-01029 | frontend-UAT | Application timeline | Logged in | Open responsive in UI | UI renders correctly |
| TC-01030 | frontend-UAT | Application timeline | No data | Open responsive with no data | No-data state shown |
| TC-01031 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?responsive | 401 Unauthorized |
| TC-01032 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?responsive | 403 Forbidden |
| TC-01033 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?export | 200 + valid data |
| TC-01034 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?export with invalid input | 400/422 + error message |
| TC-01035 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?export at boundary value | Correct boundary handling |
| TC-01036 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?export | 401 Unauthorized |
| TC-01037 | frontend-UAT | Application timeline | Logged in | Open export timeline in UI | UI renders correctly |
| TC-01038 | frontend-UAT | Application timeline | No data | Open export timeline with no data | No-data state shown |
| TC-01039 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?export | 401 Unauthorized |
| TC-01040 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?export | 403 Forbidden |
| TC-01041 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?color | 200 + valid data |
| TC-01042 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?color with invalid input | 400/422 + error message |
| TC-01043 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?color at boundary value | Correct boundary handling |
| TC-01044 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?color | 401 Unauthorized |
| TC-01045 | frontend-UAT | Application timeline | Logged in | Open color-coded in UI | UI renders correctly |
| TC-01046 | frontend-UAT | Application timeline | No data | Open color-coded with no data | No-data state shown |
| TC-01047 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?color | 401 Unauthorized |
| TC-01048 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?color | 403 Forbidden |
| TC-01049 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?dates | 200 + valid data |
| TC-01050 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?dates with invalid input | 400/422 + error message |
| TC-01051 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?dates at boundary value | Correct boundary handling |
| TC-01052 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?dates | 401 Unauthorized |
| TC-01053 | frontend-UAT | Application timeline | Logged in | Open date formatting in UI | UI renders correctly |
| TC-01054 | frontend-UAT | Application timeline | No data | Open date formatting with no data | No-data state shown |
| TC-01055 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?dates | 401 Unauthorized |
| TC-01056 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?dates | 403 Forbidden |
| TC-01057 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?hover | 200 + valid data |
| TC-01058 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?hover with invalid input | 400/422 + error message |
| TC-01059 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?hover at boundary value | Correct boundary handling |
| TC-01060 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?hover | 401 Unauthorized |
| TC-01061 | frontend-UAT | Application timeline | Logged in | Open hover tooltip in UI | UI renders correctly |
| TC-01062 | frontend-UAT | Application timeline | No data | Open hover tooltip with no data | No-data state shown |
| TC-01063 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?hover | 401 Unauthorized |
| TC-01064 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?hover | 403 Forbidden |
| TC-01065 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?mobile | 200 + valid data |
| TC-01066 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?mobile with invalid input | 400/422 + error message |
| TC-01067 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?mobile at boundary value | Correct boundary handling |
| TC-01068 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?mobile | 401 Unauthorized |
| TC-01069 | frontend-UAT | Application timeline | Logged in | Open mobile view in UI | UI renders correctly |
| TC-01070 | frontend-UAT | Application timeline | No data | Open mobile view with no data | No-data state shown |
| TC-01071 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?mobile | 401 Unauthorized |
| TC-01072 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?mobile | 403 Forbidden |
| TC-01073 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?print | 200 + valid data |
| TC-01074 | API | Application timeline | Logged in | GET /api/jobs/{id}/timeline?print with invalid input | 400/422 + error message |
| TC-01075 | API | Application timeline | Edge case | GET /api/jobs/{id}/timeline?print at boundary value | Correct boundary handling |
| TC-01076 | API | Application timeline | No auth token | GET /api/jobs/{id}/timeline?print | 401 Unauthorized |
| TC-01077 | frontend-UAT | Application timeline | Logged in | Open print view in UI | UI renders correctly |
| TC-01078 | frontend-UAT | Application timeline | No data | Open print view with no data | No-data state shown |
| TC-01079 | API | Application timeline | Expired token | GET /api/jobs/{id}/timeline?print | 401 Unauthorized |
| TC-01080 | API | Application timeline | Insufficient role | GET /api/jobs/{id}/timeline?print | 403 Forbidden |
### F9 — Follow-up email

| TC-01081 | API | Follow-up email | Logged in | POST /api/followup/generate | 200 + valid data |
| TC-01082 | API | Follow-up email | Logged in | POST /api/followup/generate with invalid input | 400/422 + error message |
| TC-01083 | API | Follow-up email | Edge case | POST /api/followup/generate at boundary value | Correct boundary handling |
| TC-01084 | API | Follow-up email | No auth token | POST /api/followup/generate | 401 Unauthorized |
| TC-01085 | frontend-UAT | Follow-up email | Logged in | Open generate follow-up in UI | UI renders correctly |
| TC-01086 | frontend-UAT | Follow-up email | No data | Open generate follow-up with no data | No-data state shown |
| TC-01087 | API | Follow-up email | Expired token | POST /api/followup/generate | 401 Unauthorized |
| TC-01088 | API | Follow-up email | Insufficient role | POST /api/followup/generate | 403 Forbidden |
| TC-01089 | API | Follow-up email | Logged in | PUT /api/followup/tone | 200 + valid data |
| TC-01090 | API | Follow-up email | Logged in | PUT /api/followup/tone with invalid input | 400/422 + error message |
| TC-01091 | API | Follow-up email | Edge case | PUT /api/followup/tone at boundary value | Correct boundary handling |
| TC-01092 | API | Follow-up email | No auth token | PUT /api/followup/tone | 401 Unauthorized |
| TC-01093 | frontend-UAT | Follow-up email | Logged in | Open set tone in UI | UI renders correctly |
| TC-01094 | frontend-UAT | Follow-up email | No data | Open set tone with no data | No-data state shown |
| TC-01095 | API | Follow-up email | Expired token | PUT /api/followup/tone | 401 Unauthorized |
| TC-01096 | API | Follow-up email | Insufficient role | PUT /api/followup/tone | 403 Forbidden |
| TC-01097 | API | Follow-up email | Logged in | POST /api/followup/schedule | 200 + valid data |
| TC-01098 | API | Follow-up email | Logged in | POST /api/followup/schedule with invalid input | 400/422 + error message |
| TC-01099 | API | Follow-up email | Edge case | POST /api/followup/schedule at boundary value | Correct boundary handling |
| TC-01100 | API | Follow-up email | No auth token | POST /api/followup/schedule | 401 Unauthorized |
| TC-01101 | frontend-UAT | Follow-up email | Logged in | Open schedule follow-up in UI | UI renders correctly |
| TC-01102 | frontend-UAT | Follow-up email | No data | Open schedule follow-up with no data | No-data state shown |
| TC-01103 | API | Follow-up email | Expired token | POST /api/followup/schedule | 401 Unauthorized |
| TC-01104 | API | Follow-up email | Insufficient role | POST /api/followup/schedule | 403 Forbidden |
| TC-01105 | API | Follow-up email | Logged in | GET /api/followup/sent | 200 + valid data |
| TC-01106 | API | Follow-up email | Logged in | GET /api/followup/sent with invalid input | 400/422 + error message |
| TC-01107 | API | Follow-up email | Edge case | GET /api/followup/sent at boundary value | Correct boundary handling |
| TC-01108 | API | Follow-up email | No auth token | GET /api/followup/sent | 401 Unauthorized |
| TC-01109 | frontend-UAT | Follow-up email | Logged in | Open list sent follow-ups in UI | UI renders correctly |
| TC-01110 | frontend-UAT | Follow-up email | No data | Open list sent follow-ups with no data | No-data state shown |
| TC-01111 | API | Follow-up email | Expired token | GET /api/followup/sent | 401 Unauthorized |
| TC-01112 | API | Follow-up email | Insufficient role | GET /api/followup/sent | 403 Forbidden |
| TC-01113 | API | Follow-up email | Logged in | GET /api/followup/reminder | 200 + valid data |
| TC-01114 | API | Follow-up email | Logged in | GET /api/followup/reminder with invalid input | 400/422 + error message |
| TC-01115 | API | Follow-up email | Edge case | GET /api/followup/reminder at boundary value | Correct boundary handling |
| TC-01116 | API | Follow-up email | No auth token | GET /api/followup/reminder | 401 Unauthorized |
| TC-01117 | frontend-UAT | Follow-up email | Logged in | Open get reminder in UI | UI renders correctly |
| TC-01118 | frontend-UAT | Follow-up email | No data | Open get reminder with no data | No-data state shown |
| TC-01119 | API | Follow-up email | Expired token | GET /api/followup/reminder | 401 Unauthorized |
| TC-01120 | API | Follow-up email | Insufficient role | GET /api/followup/reminder | 403 Forbidden |
| TC-01121 | API | Follow-up email | Logged in | GET /api/followup/preview | 200 + valid data |
| TC-01122 | API | Follow-up email | Logged in | GET /api/followup/preview with invalid input | 400/422 + error message |
| TC-01123 | API | Follow-up email | Edge case | GET /api/followup/preview at boundary value | Correct boundary handling |
| TC-01124 | API | Follow-up email | No auth token | GET /api/followup/preview | 401 Unauthorized |
| TC-01125 | frontend-UAT | Follow-up email | Logged in | Open preview follow-up in UI | UI renders correctly |
| TC-01126 | frontend-UAT | Follow-up email | No data | Open preview follow-up with no data | No-data state shown |
| TC-01127 | API | Follow-up email | Expired token | GET /api/followup/preview | 401 Unauthorized |
| TC-01128 | API | Follow-up email | Insufficient role | GET /api/followup/preview | 403 Forbidden |
| TC-01129 | API | Follow-up email | Logged in | POST /api/followup/feedback | 200 + valid data |
| TC-01130 | API | Follow-up email | Logged in | POST /api/followup/feedback with invalid input | 400/422 + error message |
| TC-01131 | API | Follow-up email | Edge case | POST /api/followup/feedback at boundary value | Correct boundary handling |
| TC-01132 | API | Follow-up email | No auth token | POST /api/followup/feedback | 401 Unauthorized |
| TC-01133 | frontend-UAT | Follow-up email | Logged in | Open feedback request in UI | UI renders correctly |
| TC-01134 | frontend-UAT | Follow-up email | No data | Open feedback request with no data | No-data state shown |
| TC-01135 | API | Follow-up email | Expired token | POST /api/followup/feedback | 401 Unauthorized |
| TC-01136 | API | Follow-up email | Insufficient role | POST /api/followup/feedback | 403 Forbidden |
| TC-01137 | API | Follow-up email | Logged in | POST /api/followup/attach-resume | 200 + valid data |
| TC-01138 | API | Follow-up email | Logged in | POST /api/followup/attach-resume with invalid input | 400/422 + error message |
| TC-01139 | API | Follow-up email | Edge case | POST /api/followup/attach-resume at boundary value | Correct boundary handling |
| TC-01140 | API | Follow-up email | No auth token | POST /api/followup/attach-resume | 401 Unauthorized |
| TC-01141 | frontend-UAT | Follow-up email | Logged in | Open attach resume in UI | UI renders correctly |
| TC-01142 | frontend-UAT | Follow-up email | No data | Open attach resume with no data | No-data state shown |
| TC-01143 | API | Follow-up email | Expired token | POST /api/followup/attach-resume | 401 Unauthorized |
| TC-01144 | API | Follow-up email | Insufficient role | POST /api/followup/attach-resume | 403 Forbidden |
| TC-01145 | API | Follow-up email | Logged in | GET /api/followup?empty | 200 + valid data |
| TC-01146 | API | Follow-up email | Logged in | GET /api/followup?empty with invalid input | 400/422 + error message |
| TC-01147 | API | Follow-up email | Edge case | GET /api/followup?empty at boundary value | Correct boundary handling |
| TC-01148 | API | Follow-up email | No auth token | GET /api/followup?empty | 401 Unauthorized |
| TC-01149 | frontend-UAT | Follow-up email | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01150 | frontend-UAT | Follow-up email | No data | Open no-data state with no data | No-data state shown |
| TC-01151 | API | Follow-up email | Expired token | GET /api/followup?empty | 401 Unauthorized |
| TC-01152 | API | Follow-up email | Insufficient role | GET /api/followup?empty | 403 Forbidden |
| TC-01153 | API | Follow-up email | Logged in | GET /api/followup?tone | 200 + valid data |
| TC-01154 | API | Follow-up email | Logged in | GET /api/followup?tone with invalid input | 400/422 + error message |
| TC-01155 | API | Follow-up email | Edge case | GET /api/followup?tone at boundary value | Correct boundary handling |
| TC-01156 | API | Follow-up email | No auth token | GET /api/followup?tone | 401 Unauthorized |
| TC-01157 | frontend-UAT | Follow-up email | Logged in | Open tone options in UI | UI renders correctly |
| TC-01158 | frontend-UAT | Follow-up email | No data | Open tone options with no data | No-data state shown |
| TC-01159 | API | Follow-up email | Expired token | GET /api/followup?tone | 401 Unauthorized |
| TC-01160 | API | Follow-up email | Insufficient role | GET /api/followup?tone | 403 Forbidden |
| TC-01161 | API | Follow-up email | Logged in | GET /api/followup?schedule | 200 + valid data |
| TC-01162 | API | Follow-up email | Logged in | GET /api/followup?schedule with invalid input | 400/422 + error message |
| TC-01163 | API | Follow-up email | Edge case | GET /api/followup?schedule at boundary value | Correct boundary handling |
| TC-01164 | API | Follow-up email | No auth token | GET /api/followup?schedule | 401 Unauthorized |
| TC-01165 | frontend-UAT | Follow-up email | Logged in | Open schedule options in UI | UI renders correctly |
| TC-01166 | frontend-UAT | Follow-up email | No data | Open schedule options with no data | No-data state shown |
| TC-01167 | API | Follow-up email | Expired token | GET /api/followup?schedule | 401 Unauthorized |
| TC-01168 | API | Follow-up email | Insufficient role | GET /api/followup?schedule | 403 Forbidden |
| TC-01169 | API | Follow-up email | Logged in | GET /api/followup?preview | 200 + valid data |
| TC-01170 | API | Follow-up email | Logged in | GET /api/followup?preview with invalid input | 400/422 + error message |
| TC-01171 | API | Follow-up email | Edge case | GET /api/followup?preview at boundary value | Correct boundary handling |
| TC-01172 | API | Follow-up email | No auth token | GET /api/followup?preview | 401 Unauthorized |
| TC-01173 | frontend-UAT | Follow-up email | Logged in | Open preview render in UI | UI renders correctly |
| TC-01174 | frontend-UAT | Follow-up email | No data | Open preview render with no data | No-data state shown |
| TC-01175 | API | Follow-up email | Expired token | GET /api/followup?preview | 401 Unauthorized |
| TC-01176 | API | Follow-up email | Insufficient role | GET /api/followup?preview | 403 Forbidden |
| TC-01177 | API | Follow-up email | Logged in | POST /api/followup/send | 200 + valid data |
| TC-01178 | API | Follow-up email | Logged in | POST /api/followup/send with invalid input | 400/422 + error message |
| TC-01179 | API | Follow-up email | Edge case | POST /api/followup/send at boundary value | Correct boundary handling |
| TC-01180 | API | Follow-up email | No auth token | POST /api/followup/send | 401 Unauthorized |
| TC-01181 | frontend-UAT | Follow-up email | Logged in | Open send follow-up in UI | UI renders correctly |
| TC-01182 | frontend-UAT | Follow-up email | No data | Open send follow-up with no data | No-data state shown |
| TC-01183 | API | Follow-up email | Expired token | POST /api/followup/send | 401 Unauthorized |
| TC-01184 | API | Follow-up email | Insufficient role | POST /api/followup/send | 403 Forbidden |
| TC-01185 | API | Follow-up email | Logged in | GET /api/followup?toast | 200 + valid data |
| TC-01186 | API | Follow-up email | Logged in | GET /api/followup?toast with invalid input | 400/422 + error message |
| TC-01187 | API | Follow-up email | Edge case | GET /api/followup?toast at boundary value | Correct boundary handling |
| TC-01188 | API | Follow-up email | No auth token | GET /api/followup?toast | 401 Unauthorized |
| TC-01189 | frontend-UAT | Follow-up email | Logged in | Open confirmation in UI | UI renders correctly |
| TC-01190 | frontend-UAT | Follow-up email | No data | Open confirmation with no data | No-data state shown |
| TC-01191 | API | Follow-up email | Expired token | GET /api/followup?toast | 401 Unauthorized |
| TC-01192 | API | Follow-up email | Insufficient role | GET /api/followup?toast | 403 Forbidden |
| TC-01193 | API | Follow-up email | Logged in | GET /api/followup?mobile | 200 + valid data |
| TC-01194 | API | Follow-up email | Logged in | GET /api/followup?mobile with invalid input | 400/422 + error message |
| TC-01195 | API | Follow-up email | Edge case | GET /api/followup?mobile at boundary value | Correct boundary handling |
| TC-01196 | API | Follow-up email | No auth token | GET /api/followup?mobile | 401 Unauthorized |
| TC-01197 | frontend-UAT | Follow-up email | Logged in | Open mobile view in UI | UI renders correctly |
| TC-01198 | frontend-UAT | Follow-up email | No data | Open mobile view with no data | No-data state shown |
| TC-01199 | API | Follow-up email | Expired token | GET /api/followup?mobile | 401 Unauthorized |
| TC-01200 | API | Follow-up email | Insufficient role | GET /api/followup?mobile | 403 Forbidden |
### F10 — Saved filters

| TC-01201 | API | Saved filters | Logged in | POST /api/filters/save | 200 + valid data |
| TC-01202 | API | Saved filters | Logged in | POST /api/filters/save with invalid input | 400/422 + error message |
| TC-01203 | API | Saved filters | Edge case | POST /api/filters/save at boundary value | Correct boundary handling |
| TC-01204 | API | Saved filters | No auth token | POST /api/filters/save | 401 Unauthorized |
| TC-01205 | frontend-UAT | Saved filters | Logged in | Open save filter in UI | UI renders correctly |
| TC-01206 | frontend-UAT | Saved filters | No data | Open save filter with no data | No-data state shown |
| TC-01207 | API | Saved filters | Expired token | POST /api/filters/save | 401 Unauthorized |
| TC-01208 | API | Saved filters | Insufficient role | POST /api/filters/save | 403 Forbidden |
| TC-01209 | API | Saved filters | Logged in | GET /api/filters/{id} | 200 + valid data |
| TC-01210 | API | Saved filters | Logged in | GET /api/filters/{id} with invalid input | 400/422 + error message |
| TC-01211 | API | Saved filters | Edge case | GET /api/filters/{id} at boundary value | Correct boundary handling |
| TC-01212 | API | Saved filters | No auth token | GET /api/filters/{id} | 401 Unauthorized |
| TC-01213 | frontend-UAT | Saved filters | Logged in | Open load preset in UI | UI renders correctly |
| TC-01214 | frontend-UAT | Saved filters | No data | Open load preset with no data | No-data state shown |
| TC-01215 | API | Saved filters | Expired token | GET /api/filters/{id} | 401 Unauthorized |
| TC-01216 | API | Saved filters | Insufficient role | GET /api/filters/{id} | 403 Forbidden |
| TC-01217 | API | Saved filters | Logged in | PUT /api/filters/{id}/name | 200 + valid data |
| TC-01218 | API | Saved filters | Logged in | PUT /api/filters/{id}/name with invalid input | 400/422 + error message |
| TC-01219 | API | Saved filters | Edge case | PUT /api/filters/{id}/name at boundary value | Correct boundary handling |
| TC-01220 | API | Saved filters | No auth token | PUT /api/filters/{id}/name | 401 Unauthorized |
| TC-01221 | frontend-UAT | Saved filters | Logged in | Open rename preset in UI | UI renders correctly |
| TC-01222 | frontend-UAT | Saved filters | No data | Open rename preset with no data | No-data state shown |
| TC-01223 | API | Saved filters | Expired token | PUT /api/filters/{id}/name | 401 Unauthorized |
| TC-01224 | API | Saved filters | Insufficient role | PUT /api/filters/{id}/name | 403 Forbidden |
| TC-01225 | API | Saved filters | Logged in | DELETE /api/filters/{id} | 200 + valid data |
| TC-01226 | API | Saved filters | Logged in | DELETE /api/filters/{id} with invalid input | 400/422 + error message |
| TC-01227 | API | Saved filters | Edge case | DELETE /api/filters/{id} at boundary value | Correct boundary handling |
| TC-01228 | API | Saved filters | No auth token | DELETE /api/filters/{id} | 401 Unauthorized |
| TC-01229 | frontend-UAT | Saved filters | Logged in | Open delete preset in UI | UI renders correctly |
| TC-01230 | frontend-UAT | Saved filters | No data | Open delete preset with no data | No-data state shown |
| TC-01231 | API | Saved filters | Expired token | DELETE /api/filters/{id} | 401 Unauthorized |
| TC-01232 | API | Saved filters | Insufficient role | DELETE /api/filters/{id} | 403 Forbidden |
| TC-01233 | API | Saved filters | Logged in | GET /api/filters | 200 + valid data |
| TC-01234 | API | Saved filters | Logged in | GET /api/filters with invalid input | 400/422 + error message |
| TC-01235 | API | Saved filters | Edge case | GET /api/filters at boundary value | Correct boundary handling |
| TC-01236 | API | Saved filters | No auth token | GET /api/filters | 401 Unauthorized |
| TC-01237 | frontend-UAT | Saved filters | Logged in | Open list saved filters in UI | UI renders correctly |
| TC-01238 | frontend-UAT | Saved filters | No data | Open list saved filters with no data | No-data state shown |
| TC-01239 | API | Saved filters | Expired token | GET /api/filters | 401 Unauthorized |
| TC-01240 | API | Saved filters | Insufficient role | GET /api/filters | 403 Forbidden |
| TC-01241 | API | Saved filters | Logged in | POST /api/filters/{id}/share | 200 + valid data |
| TC-01242 | API | Saved filters | Logged in | POST /api/filters/{id}/share with invalid input | 400/422 + error message |
| TC-01243 | API | Saved filters | Edge case | POST /api/filters/{id}/share at boundary value | Correct boundary handling |
| TC-01244 | API | Saved filters | No auth token | POST /api/filters/{id}/share | 401 Unauthorized |
| TC-01245 | frontend-UAT | Saved filters | Logged in | Open share filter in UI | UI renders correctly |
| TC-01246 | frontend-UAT | Saved filters | No data | Open share filter with no data | No-data state shown |
| TC-01247 | API | Saved filters | Expired token | POST /api/filters/{id}/share | 401 Unauthorized |
| TC-01248 | API | Saved filters | Insufficient role | POST /api/filters/{id}/share | 403 Forbidden |
| TC-01249 | API | Saved filters | Logged in | POST /api/filters/{id}/clone | 200 + valid data |
| TC-01250 | API | Saved filters | Logged in | POST /api/filters/{id}/clone with invalid input | 400/422 + error message |
| TC-01251 | API | Saved filters | Edge case | POST /api/filters/{id}/clone at boundary value | Correct boundary handling |
| TC-01252 | API | Saved filters | No auth token | POST /api/filters/{id}/clone | 401 Unauthorized |
| TC-01253 | frontend-UAT | Saved filters | Logged in | Open duplicate filter in UI | UI renders correctly |
| TC-01254 | frontend-UAT | Saved filters | No data | Open duplicate filter with no data | No-data state shown |
| TC-01255 | API | Saved filters | Expired token | POST /api/filters/{id}/clone | 401 Unauthorized |
| TC-01256 | API | Saved filters | Insufficient role | POST /api/filters/{id}/clone | 403 Forbidden |
| TC-01257 | API | Saved filters | Logged in | GET /api/jobs?autoapply | 200 + valid data |
| TC-01258 | API | Saved filters | Logged in | GET /api/jobs?autoapply with invalid input | 400/422 + error message |
| TC-01259 | API | Saved filters | Edge case | GET /api/jobs?autoapply at boundary value | Correct boundary handling |
| TC-01260 | API | Saved filters | No auth token | GET /api/jobs?autoapply | 401 Unauthorized |
| TC-01261 | frontend-UAT | Saved filters | Logged in | Open auto-apply preset in UI | UI renders correctly |
| TC-01262 | frontend-UAT | Saved filters | No data | Open auto-apply preset with no data | No-data state shown |
| TC-01263 | API | Saved filters | Expired token | GET /api/jobs?autoapply | 401 Unauthorized |
| TC-01264 | API | Saved filters | Insufficient role | GET /api/jobs?autoapply | 403 Forbidden |
| TC-01265 | API | Saved filters | Logged in | GET /api/filters?empty | 200 + valid data |
| TC-01266 | API | Saved filters | Logged in | GET /api/filters?empty with invalid input | 400/422 + error message |
| TC-01267 | API | Saved filters | Edge case | GET /api/filters?empty at boundary value | Correct boundary handling |
| TC-01268 | API | Saved filters | No auth token | GET /api/filters?empty | 401 Unauthorized |
| TC-01269 | frontend-UAT | Saved filters | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01270 | frontend-UAT | Saved filters | No data | Open no-data state with no data | No-data state shown |
| TC-01271 | API | Saved filters | Expired token | GET /api/filters?empty | 401 Unauthorized |
| TC-01272 | API | Saved filters | Insufficient role | GET /api/filters?empty | 403 Forbidden |
| TC-01273 | API | Saved filters | Logged in | GET /api/filters?sidebar | 200 + valid data |
| TC-01274 | API | Saved filters | Logged in | GET /api/filters?sidebar with invalid input | 400/422 + error message |
| TC-01275 | API | Saved filters | Edge case | GET /api/filters?sidebar at boundary value | Correct boundary handling |
| TC-01276 | API | Saved filters | No auth token | GET /api/filters?sidebar | 401 Unauthorized |
| TC-01277 | frontend-UAT | Saved filters | Logged in | Open sidebar render in UI | UI renders correctly |
| TC-01278 | frontend-UAT | Saved filters | No data | Open sidebar render with no data | No-data state shown |
| TC-01279 | API | Saved filters | Expired token | GET /api/filters?sidebar | 401 Unauthorized |
| TC-01280 | API | Saved filters | Insufficient role | GET /api/filters?sidebar | 403 Forbidden |
| TC-01281 | API | Saved filters | Logged in | GET /api/filters?rename | 200 + valid data |
| TC-01282 | API | Saved filters | Logged in | GET /api/filters?rename with invalid input | 400/422 + error message |
| TC-01283 | API | Saved filters | Edge case | GET /api/filters?rename at boundary value | Correct boundary handling |
| TC-01284 | API | Saved filters | No auth token | GET /api/filters?rename | 401 Unauthorized |
| TC-01285 | frontend-UAT | Saved filters | Logged in | Open rename render in UI | UI renders correctly |
| TC-01286 | frontend-UAT | Saved filters | No data | Open rename render with no data | No-data state shown |
| TC-01287 | API | Saved filters | Expired token | GET /api/filters?rename | 401 Unauthorized |
| TC-01288 | API | Saved filters | Insufficient role | GET /api/filters?rename | 403 Forbidden |
| TC-01289 | API | Saved filters | Logged in | GET /api/filters?delete | 200 + valid data |
| TC-01290 | API | Saved filters | Logged in | GET /api/filters?delete with invalid input | 400/422 + error message |
| TC-01291 | API | Saved filters | Edge case | GET /api/filters?delete at boundary value | Correct boundary handling |
| TC-01292 | API | Saved filters | No auth token | GET /api/filters?delete | 401 Unauthorized |
| TC-01293 | frontend-UAT | Saved filters | Logged in | Open delete render in UI | UI renders correctly |
| TC-01294 | frontend-UAT | Saved filters | No data | Open delete render with no data | No-data state shown |
| TC-01295 | API | Saved filters | Expired token | GET /api/filters?delete | 401 Unauthorized |
| TC-01296 | API | Saved filters | Insufficient role | GET /api/filters?delete | 403 Forbidden |
| TC-01297 | API | Saved filters | Logged in | GET /api/filters?share | 200 + valid data |
| TC-01298 | API | Saved filters | Logged in | GET /api/filters?share with invalid input | 400/422 + error message |
| TC-01299 | API | Saved filters | Edge case | GET /api/filters?share at boundary value | Correct boundary handling |
| TC-01300 | API | Saved filters | No auth token | GET /api/filters?share | 401 Unauthorized |
| TC-01301 | frontend-UAT | Saved filters | Logged in | Open share link in UI | UI renders correctly |
| TC-01302 | frontend-UAT | Saved filters | No data | Open share link with no data | No-data state shown |
| TC-01303 | API | Saved filters | Expired token | GET /api/filters?share | 401 Unauthorized |
| TC-01304 | API | Saved filters | Insufficient role | GET /api/filters?share | 403 Forbidden |
| TC-01305 | API | Saved filters | Logged in | GET /api/filters?clone | 200 + valid data |
| TC-01306 | API | Saved filters | Logged in | GET /api/filters?clone with invalid input | 400/422 + error message |
| TC-01307 | API | Saved filters | Edge case | GET /api/filters?clone at boundary value | Correct boundary handling |
| TC-01308 | API | Saved filters | No auth token | GET /api/filters?clone | 401 Unauthorized |
| TC-01309 | frontend-UAT | Saved filters | Logged in | Open clone render in UI | UI renders correctly |
| TC-01310 | frontend-UAT | Saved filters | No data | Open clone render with no data | No-data state shown |
| TC-01311 | API | Saved filters | Expired token | GET /api/filters?clone | 401 Unauthorized |
| TC-01312 | API | Saved filters | Insufficient role | GET /api/filters?clone | 403 Forbidden |
| TC-01313 | API | Saved filters | Logged in | GET /api/filters?export | 200 + valid data |
| TC-01314 | API | Saved filters | Logged in | GET /api/filters?export with invalid input | 400/422 + error message |
| TC-01315 | API | Saved filters | Edge case | GET /api/filters?export at boundary value | Correct boundary handling |
| TC-01316 | API | Saved filters | No auth token | GET /api/filters?export | 401 Unauthorized |
| TC-01317 | frontend-UAT | Saved filters | Logged in | Open export filters in UI | UI renders correctly |
| TC-01318 | frontend-UAT | Saved filters | No data | Open export filters with no data | No-data state shown |
| TC-01319 | API | Saved filters | Expired token | GET /api/filters?export | 401 Unauthorized |
| TC-01320 | API | Saved filters | Insufficient role | GET /api/filters?export | 403 Forbidden |
### F11 — Fit trend

| TC-01321 | API | Fit trend | Logged in | GET /api/analytics/fit-trend | 200 + valid data |
| TC-01322 | API | Fit trend | Logged in | GET /api/analytics/fit-trend with invalid input | 400/422 + error message |
| TC-01323 | API | Fit trend | Edge case | GET /api/analytics/fit-trend at boundary value | Correct boundary handling |
| TC-01324 | API | Fit trend | No auth token | GET /api/analytics/fit-trend | 401 Unauthorized |
| TC-01325 | frontend-UAT | Fit trend | Logged in | Open get fit trend in UI | UI renders correctly |
| TC-01326 | frontend-UAT | Fit trend | No data | Open get fit trend with no data | No-data state shown |
| TC-01327 | API | Fit trend | Expired token | GET /api/analytics/fit-trend | 401 Unauthorized |
| TC-01328 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend | 403 Forbidden |
| TC-01329 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?period | 200 + valid data |
| TC-01330 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?period with invalid input | 400/422 + error message |
| TC-01331 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?period at boundary value | Correct boundary handling |
| TC-01332 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?period | 401 Unauthorized |
| TC-01333 | frontend-UAT | Fit trend | Logged in | Open period filter in UI | UI renders correctly |
| TC-01334 | frontend-UAT | Fit trend | No data | Open period filter with no data | No-data state shown |
| TC-01335 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?period | 401 Unauthorized |
| TC-01336 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?period | 403 Forbidden |
| TC-01337 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?explain | 200 + valid data |
| TC-01338 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?explain with invalid input | 400/422 + error message |
| TC-01339 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?explain at boundary value | Correct boundary handling |
| TC-01340 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?explain | 401 Unauthorized |
| TC-01341 | frontend-UAT | Fit trend | Logged in | Open explain change in UI | UI renders correctly |
| TC-01342 | frontend-UAT | Fit trend | No data | Open explain change with no data | No-data state shown |
| TC-01343 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?explain | 401 Unauthorized |
| TC-01344 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?explain | 403 Forbidden |
| TC-01345 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?export | 200 + valid data |
| TC-01346 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?export with invalid input | 400/422 + error message |
| TC-01347 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?export at boundary value | Correct boundary handling |
| TC-01348 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?export | 401 Unauthorized |
| TC-01349 | frontend-UAT | Fit trend | Logged in | Open export trend in UI | UI renders correctly |
| TC-01350 | frontend-UAT | Fit trend | No data | Open export trend with no data | No-data state shown |
| TC-01351 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?export | 401 Unauthorized |
| TC-01352 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?export | 403 Forbidden |
| TC-01353 | API | Fit trend | Logged in | GET /api/analytics/fit | 200 + valid data |
| TC-01354 | API | Fit trend | Logged in | GET /api/analytics/fit with invalid input | 400/422 + error message |
| TC-01355 | API | Fit trend | Edge case | GET /api/analytics/fit at boundary value | Correct boundary handling |
| TC-01356 | API | Fit trend | No auth token | GET /api/analytics/fit | 401 Unauthorized |
| TC-01357 | frontend-UAT | Fit trend | Logged in | Open current fit score in UI | UI renders correctly |
| TC-01358 | frontend-UAT | Fit trend | No data | Open current fit score with no data | No-data state shown |
| TC-01359 | API | Fit trend | Expired token | GET /api/analytics/fit | 401 Unauthorized |
| TC-01360 | API | Fit trend | Insufficient role | GET /api/analytics/fit | 403 Forbidden |
| TC-01361 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?by_category | 200 + valid data |
| TC-01362 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?by_category with invalid input | 400/422 + error message |
| TC-01363 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?by_category at boundary value | Correct boundary handling |
| TC-01364 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?by_category | 401 Unauthorized |
| TC-01365 | frontend-UAT | Fit trend | Logged in | Open by category in UI | UI renders correctly |
| TC-01366 | frontend-UAT | Fit trend | No data | Open by category with no data | No-data state shown |
| TC-01367 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?by_category | 401 Unauthorized |
| TC-01368 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?by_category | 403 Forbidden |
| TC-01369 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?empty | 200 + valid data |
| TC-01370 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?empty with invalid input | 400/422 + error message |
| TC-01371 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?empty at boundary value | Correct boundary handling |
| TC-01372 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?empty | 401 Unauthorized |
| TC-01373 | frontend-UAT | Fit trend | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01374 | frontend-UAT | Fit trend | No data | Open no-data state with no data | No-data state shown |
| TC-01375 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?empty | 401 Unauthorized |
| TC-01376 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?empty | 403 Forbidden |
| TC-01377 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?week | 200 + valid data |
| TC-01378 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?week with invalid input | 400/422 + error message |
| TC-01379 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?week at boundary value | Correct boundary handling |
| TC-01380 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?week | 401 Unauthorized |
| TC-01381 | frontend-UAT | Fit trend | Logged in | Open weekly fit in UI | UI renders correctly |
| TC-01382 | frontend-UAT | Fit trend | No data | Open weekly fit with no data | No-data state shown |
| TC-01383 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?week | 401 Unauthorized |
| TC-01384 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?week | 403 Forbidden |
| TC-01385 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?month | 200 + valid data |
| TC-01386 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?month with invalid input | 400/422 + error message |
| TC-01387 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?month at boundary value | Correct boundary handling |
| TC-01388 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?month | 401 Unauthorized |
| TC-01389 | frontend-UAT | Fit trend | Logged in | Open monthly fit in UI | UI renders correctly |
| TC-01390 | frontend-UAT | Fit trend | No data | Open monthly fit with no data | No-data state shown |
| TC-01391 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?month | 401 Unauthorized |
| TC-01392 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?month | 403 Forbidden |
| TC-01393 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?line | 200 + valid data |
| TC-01394 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?line with invalid input | 400/422 + error message |
| TC-01395 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?line at boundary value | Correct boundary handling |
| TC-01396 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?line | 401 Unauthorized |
| TC-01397 | frontend-UAT | Fit trend | Logged in | Open line chart data in UI | UI renders correctly |
| TC-01398 | frontend-UAT | Fit trend | No data | Open line chart data with no data | No-data state shown |
| TC-01399 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?line | 401 Unauthorized |
| TC-01400 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?line | 403 Forbidden |
| TC-01401 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?hover | 200 + valid data |
| TC-01402 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?hover with invalid input | 400/422 + error message |
| TC-01403 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?hover at boundary value | Correct boundary handling |
| TC-01404 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?hover | 401 Unauthorized |
| TC-01405 | frontend-UAT | Fit trend | Logged in | Open hover tooltip in UI | UI renders correctly |
| TC-01406 | frontend-UAT | Fit trend | No data | Open hover tooltip with no data | No-data state shown |
| TC-01407 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?hover | 401 Unauthorized |
| TC-01408 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?hover | 403 Forbidden |
| TC-01409 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?mobile | 200 + valid data |
| TC-01410 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?mobile with invalid input | 400/422 + error message |
| TC-01411 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?mobile at boundary value | Correct boundary handling |
| TC-01412 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?mobile | 401 Unauthorized |
| TC-01413 | frontend-UAT | Fit trend | Logged in | Open mobile view in UI | UI renders correctly |
| TC-01414 | frontend-UAT | Fit trend | No data | Open mobile view with no data | No-data state shown |
| TC-01415 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?mobile | 401 Unauthorized |
| TC-01416 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?mobile | 403 Forbidden |
| TC-01417 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?print | 200 + valid data |
| TC-01418 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?print with invalid input | 400/422 + error message |
| TC-01419 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?print at boundary value | Correct boundary handling |
| TC-01420 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?print | 401 Unauthorized |
| TC-01421 | frontend-UAT | Fit trend | Logged in | Open print view in UI | UI renders correctly |
| TC-01422 | frontend-UAT | Fit trend | No data | Open print view with no data | No-data state shown |
| TC-01423 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?print | 401 Unauthorized |
| TC-01424 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?print | 403 Forbidden |
| TC-01425 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?compare | 200 + valid data |
| TC-01426 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?compare with invalid input | 400/422 + error message |
| TC-01427 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?compare at boundary value | Correct boundary handling |
| TC-01428 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?compare | 401 Unauthorized |
| TC-01429 | frontend-UAT | Fit trend | Logged in | Open compare periods in UI | UI renders correctly |
| TC-01430 | frontend-UAT | Fit trend | No data | Open compare periods with no data | No-data state shown |
| TC-01431 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?compare | 401 Unauthorized |
| TC-01432 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?compare | 403 Forbidden |
| TC-01433 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?max | 200 + valid data |
| TC-01434 | API | Fit trend | Logged in | GET /api/analytics/fit-trend?max with invalid input | 400/422 + error message |
| TC-01435 | API | Fit trend | Edge case | GET /api/analytics/fit-trend?max at boundary value | Correct boundary handling |
| TC-01436 | API | Fit trend | No auth token | GET /api/analytics/fit-trend?max | 401 Unauthorized |
| TC-01437 | frontend-UAT | Fit trend | Logged in | Open max fit in UI | UI renders correctly |
| TC-01438 | frontend-UAT | Fit trend | No data | Open max fit with no data | No-data state shown |
| TC-01439 | API | Fit trend | Expired token | GET /api/analytics/fit-trend?max | 401 Unauthorized |
| TC-01440 | API | Fit trend | Insufficient role | GET /api/analytics/fit-trend?max | 403 Forbidden |
### F12 — Resume variants

| TC-01441 | API | Resume variants | Logged in | POST /api/resume/variants | 200 + valid data |
| TC-01442 | API | Resume variants | Logged in | POST /api/resume/variants with invalid input | 400/422 + error message |
| TC-01443 | API | Resume variants | Edge case | POST /api/resume/variants at boundary value | Correct boundary handling |
| TC-01444 | API | Resume variants | No auth token | POST /api/resume/variants | 401 Unauthorized |
| TC-01445 | frontend-UAT | Resume variants | Logged in | Open create variant in UI | UI renders correctly |
| TC-01446 | frontend-UAT | Resume variants | No data | Open create variant with no data | No-data state shown |
| TC-01447 | API | Resume variants | Expired token | POST /api/resume/variants | 401 Unauthorized |
| TC-01448 | API | Resume variants | Insufficient role | POST /api/resume/variants | 403 Forbidden |
| TC-01449 | API | Resume variants | Logged in | PUT /api/resume/variants/{id}/name | 200 + valid data |
| TC-01450 | API | Resume variants | Logged in | PUT /api/resume/variants/{id}/name with invalid input | 400/422 + error message |
| TC-01451 | API | Resume variants | Edge case | PUT /api/resume/variants/{id}/name at boundary value | Correct boundary handling |
| TC-01452 | API | Resume variants | No auth token | PUT /api/resume/variants/{id}/name | 401 Unauthorized |
| TC-01453 | frontend-UAT | Resume variants | Logged in | Open rename variant in UI | UI renders correctly |
| TC-01454 | frontend-UAT | Resume variants | No data | Open rename variant with no data | No-data state shown |
| TC-01455 | API | Resume variants | Expired token | PUT /api/resume/variants/{id}/name | 401 Unauthorized |
| TC-01456 | API | Resume variants | Insufficient role | PUT /api/resume/variants/{id}/name | 403 Forbidden |
| TC-01457 | API | Resume variants | Logged in | GET /api/resume/variants/compare | 200 + valid data |
| TC-01458 | API | Resume variants | Logged in | GET /api/resume/variants/compare with invalid input | 400/422 + error message |
| TC-01459 | API | Resume variants | Edge case | GET /api/resume/variants/compare at boundary value | Correct boundary handling |
| TC-01460 | API | Resume variants | No auth token | GET /api/resume/variants/compare | 401 Unauthorized |
| TC-01461 | frontend-UAT | Resume variants | Logged in | Open compare variants in UI | UI renders correctly |
| TC-01462 | frontend-UAT | Resume variants | No data | Open compare variants with no data | No-data state shown |
| TC-01463 | API | Resume variants | Expired token | GET /api/resume/variants/compare | 401 Unauthorized |
| TC-01464 | API | Resume variants | Insufficient role | GET /api/resume/variants/compare | 403 Forbidden |
| TC-01465 | API | Resume variants | Logged in | PUT /api/resume/variants/{id}/default | 200 + valid data |
| TC-01466 | API | Resume variants | Logged in | PUT /api/resume/variants/{id}/default with invalid input | 400/422 + error message |
| TC-01467 | API | Resume variants | Edge case | PUT /api/resume/variants/{id}/default at boundary value | Correct boundary handling |
| TC-01468 | API | Resume variants | No auth token | PUT /api/resume/variants/{id}/default | 401 Unauthorized |
| TC-01469 | frontend-UAT | Resume variants | Logged in | Open set default in UI | UI renders correctly |
| TC-01470 | frontend-UAT | Resume variants | No data | Open set default with no data | No-data state shown |
| TC-01471 | API | Resume variants | Expired token | PUT /api/resume/variants/{id}/default | 401 Unauthorized |
| TC-01472 | API | Resume variants | Insufficient role | PUT /api/resume/variants/{id}/default | 403 Forbidden |
| TC-01473 | API | Resume variants | Logged in | DELETE /api/resume/variants/{id} | 200 + valid data |
| TC-01474 | API | Resume variants | Logged in | DELETE /api/resume/variants/{id} with invalid input | 400/422 + error message |
| TC-01475 | API | Resume variants | Edge case | DELETE /api/resume/variants/{id} at boundary value | Correct boundary handling |
| TC-01476 | API | Resume variants | No auth token | DELETE /api/resume/variants/{id} | 401 Unauthorized |
| TC-01477 | frontend-UAT | Resume variants | Logged in | Open delete variant in UI | UI renders correctly |
| TC-01478 | frontend-UAT | Resume variants | No data | Open delete variant with no data | No-data state shown |
| TC-01479 | API | Resume variants | Expired token | DELETE /api/resume/variants/{id} | 401 Unauthorized |
| TC-01480 | API | Resume variants | Insufficient role | DELETE /api/resume/variants/{id} | 403 Forbidden |
| TC-01481 | API | Resume variants | Logged in | POST /api/resume/variants/{id}/clone | 200 + valid data |
| TC-01482 | API | Resume variants | Logged in | POST /api/resume/variants/{id}/clone with invalid input | 400/422 + error message |
| TC-01483 | API | Resume variants | Edge case | POST /api/resume/variants/{id}/clone at boundary value | Correct boundary handling |
| TC-01484 | API | Resume variants | No auth token | POST /api/resume/variants/{id}/clone | 401 Unauthorized |
| TC-01485 | frontend-UAT | Resume variants | Logged in | Open clone variant in UI | UI renders correctly |
| TC-01486 | frontend-UAT | Resume variants | No data | Open clone variant with no data | No-data state shown |
| TC-01487 | API | Resume variants | Expired token | POST /api/resume/variants/{id}/clone | 401 Unauthorized |
| TC-01488 | API | Resume variants | Insufficient role | POST /api/resume/variants/{id}/clone | 403 Forbidden |
| TC-01489 | API | Resume variants | Logged in | GET /api/resume/variants?best | 200 + valid data |
| TC-01490 | API | Resume variants | Logged in | GET /api/resume/variants?best with invalid input | 400/422 + error message |
| TC-01491 | API | Resume variants | Edge case | GET /api/resume/variants?best at boundary value | Correct boundary handling |
| TC-01492 | API | Resume variants | No auth token | GET /api/resume/variants?best | 401 Unauthorized |
| TC-01493 | frontend-UAT | Resume variants | Logged in | Open highest scoring in UI | UI renders correctly |
| TC-01494 | frontend-UAT | Resume variants | No data | Open highest scoring with no data | No-data state shown |
| TC-01495 | API | Resume variants | Expired token | GET /api/resume/variants?best | 401 Unauthorized |
| TC-01496 | API | Resume variants | Insufficient role | GET /api/resume/variants?best | 403 Forbidden |
| TC-01497 | API | Resume variants | Logged in | GET /api/resume/variants?empty | 200 + valid data |
| TC-01498 | API | Resume variants | Logged in | GET /api/resume/variants?empty with invalid input | 400/422 + error message |
| TC-01499 | API | Resume variants | Edge case | GET /api/resume/variants?empty at boundary value | Correct boundary handling |
| TC-01500 | API | Resume variants | No auth token | GET /api/resume/variants?empty | 401 Unauthorized |
| TC-01501 | frontend-UAT | Resume variants | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01502 | frontend-UAT | Resume variants | No data | Open no-data state with no data | No-data state shown |
| TC-01503 | API | Resume variants | Expired token | GET /api/resume/variants?empty | 401 Unauthorized |
| TC-01504 | API | Resume variants | Insufficient role | GET /api/resume/variants?empty | 403 Forbidden |
| TC-01505 | API | Resume variants | Logged in | GET /api/resume/variants?editor | 200 + valid data |
| TC-01506 | API | Resume variants | Logged in | GET /api/resume/variants?editor with invalid input | 400/422 + error message |
| TC-01507 | API | Resume variants | Edge case | GET /api/resume/variants?editor at boundary value | Correct boundary handling |
| TC-01508 | API | Resume variants | No auth token | GET /api/resume/variants?editor | 401 Unauthorized |
| TC-01509 | frontend-UAT | Resume variants | Logged in | Open editor render in UI | UI renders correctly |
| TC-01510 | frontend-UAT | Resume variants | No data | Open editor render with no data | No-data state shown |
| TC-01511 | API | Resume variants | Expired token | GET /api/resume/variants?editor | 401 Unauthorized |
| TC-01512 | API | Resume variants | Insufficient role | GET /api/resume/variants?editor | 403 Forbidden |
| TC-01513 | API | Resume variants | Logged in | GET /api/resume/variants?default | 200 + valid data |
| TC-01514 | API | Resume variants | Logged in | GET /api/resume/variants?default with invalid input | 400/422 + error message |
| TC-01515 | API | Resume variants | Edge case | GET /api/resume/variants?default at boundary value | Correct boundary handling |
| TC-01516 | API | Resume variants | No auth token | GET /api/resume/variants?default | 401 Unauthorized |
| TC-01517 | frontend-UAT | Resume variants | Logged in | Open default flag in UI | UI renders correctly |
| TC-01518 | frontend-UAT | Resume variants | No data | Open default flag with no data | No-data state shown |
| TC-01519 | API | Resume variants | Expired token | GET /api/resume/variants?default | 401 Unauthorized |
| TC-01520 | API | Resume variants | Insufficient role | GET /api/resume/variants?default | 403 Forbidden |
| TC-01521 | API | Resume variants | Logged in | GET /api/resume/variants?delete | 200 + valid data |
| TC-01522 | API | Resume variants | Logged in | GET /api/resume/variants?delete with invalid input | 400/422 + error message |
| TC-01523 | API | Resume variants | Edge case | GET /api/resume/variants?delete at boundary value | Correct boundary handling |
| TC-01524 | API | Resume variants | No auth token | GET /api/resume/variants?delete | 401 Unauthorized |
| TC-01525 | frontend-UAT | Resume variants | Logged in | Open delete render in UI | UI renders correctly |
| TC-01526 | frontend-UAT | Resume variants | No data | Open delete render with no data | No-data state shown |
| TC-01527 | API | Resume variants | Expired token | GET /api/resume/variants?delete | 401 Unauthorized |
| TC-01528 | API | Resume variants | Insufficient role | GET /api/resume/variants?delete | 403 Forbidden |
| TC-01529 | API | Resume variants | Logged in | GET /api/resume/variants?clone | 200 + valid data |
| TC-01530 | API | Resume variants | Logged in | GET /api/resume/variants?clone with invalid input | 400/422 + error message |
| TC-01531 | API | Resume variants | Edge case | GET /api/resume/variants?clone at boundary value | Correct boundary handling |
| TC-01532 | API | Resume variants | No auth token | GET /api/resume/variants?clone | 401 Unauthorized |
| TC-01533 | frontend-UAT | Resume variants | Logged in | Open clone render in UI | UI renders correctly |
| TC-01534 | frontend-UAT | Resume variants | No data | Open clone render with no data | No-data state shown |
| TC-01535 | API | Resume variants | Expired token | GET /api/resume/variants?clone | 401 Unauthorized |
| TC-01536 | API | Resume variants | Insufficient role | GET /api/resume/variants?clone | 403 Forbidden |
| TC-01537 | API | Resume variants | Logged in | GET /api/resume/variants?export | 200 + valid data |
| TC-01538 | API | Resume variants | Logged in | GET /api/resume/variants?export with invalid input | 400/422 + error message |
| TC-01539 | API | Resume variants | Edge case | GET /api/resume/variants?export at boundary value | Correct boundary handling |
| TC-01540 | API | Resume variants | No auth token | GET /api/resume/variants?export | 401 Unauthorized |
| TC-01541 | frontend-UAT | Resume variants | Logged in | Open export variants in UI | UI renders correctly |
| TC-01542 | frontend-UAT | Resume variants | No data | Open export variants with no data | No-data state shown |
| TC-01543 | API | Resume variants | Expired token | GET /api/resume/variants?export | 401 Unauthorized |
| TC-01544 | API | Resume variants | Insufficient role | GET /api/resume/variants?export | 403 Forbidden |
| TC-01545 | API | Resume variants | Logged in | GET /api/resume/variants?mobile | 200 + valid data |
| TC-01546 | API | Resume variants | Logged in | GET /api/resume/variants?mobile with invalid input | 400/422 + error message |
| TC-01547 | API | Resume variants | Edge case | GET /api/resume/variants?mobile at boundary value | Correct boundary handling |
| TC-01548 | API | Resume variants | No auth token | GET /api/resume/variants?mobile | 401 Unauthorized |
| TC-01549 | frontend-UAT | Resume variants | Logged in | Open mobile view in UI | UI renders correctly |
| TC-01550 | frontend-UAT | Resume variants | No data | Open mobile view with no data | No-data state shown |
| TC-01551 | API | Resume variants | Expired token | GET /api/resume/variants?mobile | 401 Unauthorized |
| TC-01552 | API | Resume variants | Insufficient role | GET /api/resume/variants?mobile | 403 Forbidden |
| TC-01553 | API | Resume variants | Logged in | GET /api/resume/variants?hover | 200 + valid data |
| TC-01554 | API | Resume variants | Logged in | GET /api/resume/variants?hover with invalid input | 400/422 + error message |
| TC-01555 | API | Resume variants | Edge case | GET /api/resume/variants?hover at boundary value | Correct boundary handling |
| TC-01556 | API | Resume variants | No auth token | GET /api/resume/variants?hover | 401 Unauthorized |
| TC-01557 | frontend-UAT | Resume variants | Logged in | Open hover tooltip in UI | UI renders correctly |
| TC-01558 | frontend-UAT | Resume variants | No data | Open hover tooltip with no data | No-data state shown |
| TC-01559 | API | Resume variants | Expired token | GET /api/resume/variants?hover | 401 Unauthorized |
| TC-01560 | API | Resume variants | Insufficient role | GET /api/resume/variants?hover | 403 Forbidden |
### F13 — Cover-letter personalization

| TC-01561 | API | Cover-letter personalization | Logged in | POST /api/coverletter/generate | 200 + valid data |
| TC-01562 | API | Cover-letter personalization | Logged in | POST /api/coverletter/generate with invalid input | 400/422 + error message |
| TC-01563 | API | Cover-letter personalization | Edge case | POST /api/coverletter/generate at boundary value | Correct boundary handling |
| TC-01564 | API | Cover-letter personalization | No auth token | POST /api/coverletter/generate | 401 Unauthorized |
| TC-01565 | frontend-UAT | Cover-letter personalization | Logged in | Open generate cover letter in UI | UI renders correctly |
| TC-01566 | frontend-UAT | Cover-letter personalization | No data | Open generate cover letter with no data | No-data state shown |
| TC-01567 | API | Cover-letter personalization | Expired token | POST /api/coverletter/generate | 401 Unauthorized |
| TC-01568 | API | Cover-letter personalization | Insufficient role | POST /api/coverletter/generate | 403 Forbidden |
| TC-01569 | API | Cover-letter personalization | Logged in | POST /api/coverletter/regenerate | 200 + valid data |
| TC-01570 | API | Cover-letter personalization | Logged in | POST /api/coverletter/regenerate with invalid input | 400/422 + error message |
| TC-01571 | API | Cover-letter personalization | Edge case | POST /api/coverletter/regenerate at boundary value | Correct boundary handling |
| TC-01572 | API | Cover-letter personalization | No auth token | POST /api/coverletter/regenerate | 401 Unauthorized |
| TC-01573 | frontend-UAT | Cover-letter personalization | Logged in | Open regenerate in UI | UI renders correctly |
| TC-01574 | frontend-UAT | Cover-letter personalization | No data | Open regenerate with no data | No-data state shown |
| TC-01575 | API | Cover-letter personalization | Expired token | POST /api/coverletter/regenerate | 401 Unauthorized |
| TC-01576 | API | Cover-letter personalization | Insufficient role | POST /api/coverletter/regenerate | 403 Forbidden |
| TC-01577 | API | Cover-letter personalization | Logged in | PUT /api/coverletter/edit | 200 + valid data |
| TC-01578 | API | Cover-letter personalization | Logged in | PUT /api/coverletter/edit with invalid input | 400/422 + error message |
| TC-01579 | API | Cover-letter personalization | Edge case | PUT /api/coverletter/edit at boundary value | Correct boundary handling |
| TC-01580 | API | Cover-letter personalization | No auth token | PUT /api/coverletter/edit | 401 Unauthorized |
| TC-01581 | frontend-UAT | Cover-letter personalization | Logged in | Open edit letter in UI | UI renders correctly |
| TC-01582 | frontend-UAT | Cover-letter personalization | No data | Open edit letter with no data | No-data state shown |
| TC-01583 | API | Cover-letter personalization | Expired token | PUT /api/coverletter/edit | 401 Unauthorized |
| TC-01584 | API | Cover-letter personalization | Insufficient role | PUT /api/coverletter/edit | 403 Forbidden |
| TC-01585 | API | Cover-letter personalization | Logged in | GET /api/coverletter?job | 200 + valid data |
| TC-01586 | API | Cover-letter personalization | Logged in | GET /api/coverletter?job with invalid input | 400/422 + error message |
| TC-01587 | API | Cover-letter personalization | Edge case | GET /api/coverletter?job at boundary value | Correct boundary handling |
| TC-01588 | API | Cover-letter personalization | No auth token | GET /api/coverletter?job | 401 Unauthorized |
| TC-01589 | frontend-UAT | Cover-letter personalization | Logged in | Open tailored letter in UI | UI renders correctly |
| TC-01590 | frontend-UAT | Cover-letter personalization | No data | Open tailored letter with no data | No-data state shown |
| TC-01591 | API | Cover-letter personalization | Expired token | GET /api/coverletter?job | 401 Unauthorized |
| TC-01592 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?job | 403 Forbidden |
| TC-01593 | API | Cover-letter personalization | Logged in | GET /api/coverletter/export | 200 + valid data |
| TC-01594 | API | Cover-letter personalization | Logged in | GET /api/coverletter/export with invalid input | 400/422 + error message |
| TC-01595 | API | Cover-letter personalization | Edge case | GET /api/coverletter/export at boundary value | Correct boundary handling |
| TC-01596 | API | Cover-letter personalization | No auth token | GET /api/coverletter/export | 401 Unauthorized |
| TC-01597 | frontend-UAT | Cover-letter personalization | Logged in | Open export PDF in UI | UI renders correctly |
| TC-01598 | frontend-UAT | Cover-letter personalization | No data | Open export PDF with no data | No-data state shown |
| TC-01599 | API | Cover-letter personalization | Expired token | GET /api/coverletter/export | 401 Unauthorized |
| TC-01600 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter/export | 403 Forbidden |
| TC-01601 | API | Cover-letter personalization | Logged in | POST /api/coverletter/validate | 200 + valid data |
| TC-01602 | API | Cover-letter personalization | Logged in | POST /api/coverletter/validate with invalid input | 400/422 + error message |
| TC-01603 | API | Cover-letter personalization | Edge case | POST /api/coverletter/validate at boundary value | Correct boundary handling |
| TC-01604 | API | Cover-letter personalization | No auth token | POST /api/coverletter/validate | 401 Unauthorized |
| TC-01605 | frontend-UAT | Cover-letter personalization | Logged in | Open validate length in UI | UI renders correctly |
| TC-01606 | frontend-UAT | Cover-letter personalization | No data | Open validate length with no data | No-data state shown |
| TC-01607 | API | Cover-letter personalization | Expired token | POST /api/coverletter/validate | 401 Unauthorized |
| TC-01608 | API | Cover-letter personalization | Insufficient role | POST /api/coverletter/validate | 403 Forbidden |
| TC-01609 | API | Cover-letter personalization | Logged in | GET /api/coverletter?empty | 200 + valid data |
| TC-01610 | API | Cover-letter personalization | Logged in | GET /api/coverletter?empty with invalid input | 400/422 + error message |
| TC-01611 | API | Cover-letter personalization | Edge case | GET /api/coverletter?empty at boundary value | Correct boundary handling |
| TC-01612 | API | Cover-letter personalization | No auth token | GET /api/coverletter?empty | 401 Unauthorized |
| TC-01613 | frontend-UAT | Cover-letter personalization | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01614 | frontend-UAT | Cover-letter personalization | No data | Open no-data state with no data | No-data state shown |
| TC-01615 | API | Cover-letter personalization | Expired token | GET /api/coverletter?empty | 401 Unauthorized |
| TC-01616 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?empty | 403 Forbidden |
| TC-01617 | API | Cover-letter personalization | Logged in | GET /api/coverletter?editor | 200 + valid data |
| TC-01618 | API | Cover-letter personalization | Logged in | GET /api/coverletter?editor with invalid input | 400/422 + error message |
| TC-01619 | API | Cover-letter personalization | Edge case | GET /api/coverletter?editor at boundary value | Correct boundary handling |
| TC-01620 | API | Cover-letter personalization | No auth token | GET /api/coverletter?editor | 401 Unauthorized |
| TC-01621 | frontend-UAT | Cover-letter personalization | Logged in | Open editor render in UI | UI renders correctly |
| TC-01622 | frontend-UAT | Cover-letter personalization | No data | Open editor render with no data | No-data state shown |
| TC-01623 | API | Cover-letter personalization | Expired token | GET /api/coverletter?editor | 401 Unauthorized |
| TC-01624 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?editor | 403 Forbidden |
| TC-01625 | API | Cover-letter personalization | Logged in | GET /api/coverletter?preview | 200 + valid data |
| TC-01626 | API | Cover-letter personalization | Logged in | GET /api/coverletter?preview with invalid input | 400/422 + error message |
| TC-01627 | API | Cover-letter personalization | Edge case | GET /api/coverletter?preview at boundary value | Correct boundary handling |
| TC-01628 | API | Cover-letter personalization | No auth token | GET /api/coverletter?preview | 401 Unauthorized |
| TC-01629 | frontend-UAT | Cover-letter personalization | Logged in | Open preview render in UI | UI renders correctly |
| TC-01630 | frontend-UAT | Cover-letter personalization | No data | Open preview render with no data | No-data state shown |
| TC-01631 | API | Cover-letter personalization | Expired token | GET /api/coverletter?preview | 401 Unauthorized |
| TC-01632 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?preview | 403 Forbidden |
| TC-01633 | API | Cover-letter personalization | Logged in | GET /api/coverletter?export | 200 + valid data |
| TC-01634 | API | Cover-letter personalization | Logged in | GET /api/coverletter?export with invalid input | 400/422 + error message |
| TC-01635 | API | Cover-letter personalization | Edge case | GET /api/coverletter?export at boundary value | Correct boundary handling |
| TC-01636 | API | Cover-letter personalization | No auth token | GET /api/coverletter?export | 401 Unauthorized |
| TC-01637 | frontend-UAT | Cover-letter personalization | Logged in | Open export render in UI | UI renders correctly |
| TC-01638 | frontend-UAT | Cover-letter personalization | No data | Open export render with no data | No-data state shown |
| TC-01639 | API | Cover-letter personalization | Expired token | GET /api/coverletter?export | 401 Unauthorized |
| TC-01640 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?export | 403 Forbidden |
| TC-01641 | API | Cover-letter personalization | Logged in | GET /api/coverletter?length | 200 + valid data |
| TC-01642 | API | Cover-letter personalization | Logged in | GET /api/coverletter?length with invalid input | 400/422 + error message |
| TC-01643 | API | Cover-letter personalization | Edge case | GET /api/coverletter?length at boundary value | Correct boundary handling |
| TC-01644 | API | Cover-letter personalization | No auth token | GET /api/coverletter?length | 401 Unauthorized |
| TC-01645 | frontend-UAT | Cover-letter personalization | Logged in | Open length warning in UI | UI renders correctly |
| TC-01646 | frontend-UAT | Cover-letter personalization | No data | Open length warning with no data | No-data state shown |
| TC-01647 | API | Cover-letter personalization | Expired token | GET /api/coverletter?length | 401 Unauthorized |
| TC-01648 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?length | 403 Forbidden |
| TC-01649 | API | Cover-letter personalization | Logged in | GET /api/coverletter?mobile | 200 + valid data |
| TC-01650 | API | Cover-letter personalization | Logged in | GET /api/coverletter?mobile with invalid input | 400/422 + error message |
| TC-01651 | API | Cover-letter personalization | Edge case | GET /api/coverletter?mobile at boundary value | Correct boundary handling |
| TC-01652 | API | Cover-letter personalization | No auth token | GET /api/coverletter?mobile | 401 Unauthorized |
| TC-01653 | frontend-UAT | Cover-letter personalization | Logged in | Open mobile view in UI | UI renders correctly |
| TC-01654 | frontend-UAT | Cover-letter personalization | No data | Open mobile view with no data | No-data state shown |
| TC-01655 | API | Cover-letter personalization | Expired token | GET /api/coverletter?mobile | 401 Unauthorized |
| TC-01656 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?mobile | 403 Forbidden |
| TC-01657 | API | Cover-letter personalization | Logged in | GET /api/coverletter?print | 200 + valid data |
| TC-01658 | API | Cover-letter personalization | Logged in | GET /api/coverletter?print with invalid input | 400/422 + error message |
| TC-01659 | API | Cover-letter personalization | Edge case | GET /api/coverletter?print at boundary value | Correct boundary handling |
| TC-01660 | API | Cover-letter personalization | No auth token | GET /api/coverletter?print | 401 Unauthorized |
| TC-01661 | frontend-UAT | Cover-letter personalization | Logged in | Open print view in UI | UI renders correctly |
| TC-01662 | frontend-UAT | Cover-letter personalization | No data | Open print view with no data | No-data state shown |
| TC-01663 | API | Cover-letter personalization | Expired token | GET /api/coverletter?print | 401 Unauthorized |
| TC-01664 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?print | 403 Forbidden |
| TC-01665 | API | Cover-letter personalization | Logged in | GET /api/coverletter?hover | 200 + valid data |
| TC-01666 | API | Cover-letter personalization | Logged in | GET /api/coverletter?hover with invalid input | 400/422 + error message |
| TC-01667 | API | Cover-letter personalization | Edge case | GET /api/coverletter?hover at boundary value | Correct boundary handling |
| TC-01668 | API | Cover-letter personalization | No auth token | GET /api/coverletter?hover | 401 Unauthorized |
| TC-01669 | frontend-UAT | Cover-letter personalization | Logged in | Open hover tooltip in UI | UI renders correctly |
| TC-01670 | frontend-UAT | Cover-letter personalization | No data | Open hover tooltip with no data | No-data state shown |
| TC-01671 | API | Cover-letter personalization | Expired token | GET /api/coverletter?hover | 401 Unauthorized |
| TC-01672 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?hover | 403 Forbidden |
| TC-01673 | API | Cover-letter personalization | Logged in | GET /api/coverletter?tone | 200 + valid data |
| TC-01674 | API | Cover-letter personalization | Logged in | GET /api/coverletter?tone with invalid input | 400/422 + error message |
| TC-01675 | API | Cover-letter personalization | Edge case | GET /api/coverletter?tone at boundary value | Correct boundary handling |
| TC-01676 | API | Cover-letter personalization | No auth token | GET /api/coverletter?tone | 401 Unauthorized |
| TC-01677 | frontend-UAT | Cover-letter personalization | Logged in | Open tone options in UI | UI renders correctly |
| TC-01678 | frontend-UAT | Cover-letter personalization | No data | Open tone options with no data | No-data state shown |
| TC-01679 | API | Cover-letter personalization | Expired token | GET /api/coverletter?tone | 401 Unauthorized |
| TC-01680 | API | Cover-letter personalization | Insufficient role | GET /api/coverletter?tone | 403 Forbidden |
### F14 — Export / import

| TC-01681 | API | Export / import | Logged in | GET /api/export?format=csv | 200 + valid data |
| TC-01682 | API | Export / import | Logged in | GET /api/export?format=csv with invalid input | 400/422 + error message |
| TC-01683 | API | Export / import | Edge case | GET /api/export?format=csv at boundary value | Correct boundary handling |
| TC-01684 | API | Export / import | No auth token | GET /api/export?format=csv | 401 Unauthorized |
| TC-01685 | frontend-UAT | Export / import | Logged in | Open export CSV in UI | UI renders correctly |
| TC-01686 | frontend-UAT | Export / import | No data | Open export CSV with no data | No-data state shown |
| TC-01687 | API | Export / import | Expired token | GET /api/export?format=csv | 401 Unauthorized |
| TC-01688 | API | Export / import | Insufficient role | GET /api/export?format=csv | 403 Forbidden |
| TC-01689 | API | Export / import | Logged in | GET /api/export?format=json | 200 + valid data |
| TC-01690 | API | Export / import | Logged in | GET /api/export?format=json with invalid input | 400/422 + error message |
| TC-01691 | API | Export / import | Edge case | GET /api/export?format=json at boundary value | Correct boundary handling |
| TC-01692 | API | Export / import | No auth token | GET /api/export?format=json | 401 Unauthorized |
| TC-01693 | frontend-UAT | Export / import | Logged in | Open export JSON in UI | UI renders correctly |
| TC-01694 | frontend-UAT | Export / import | No data | Open export JSON with no data | No-data state shown |
| TC-01695 | API | Export / import | Expired token | GET /api/export?format=json | 401 Unauthorized |
| TC-01696 | API | Export / import | Insufficient role | GET /api/export?format=json | 403 Forbidden |
| TC-01697 | API | Export / import | Logged in | GET /api/export?assets | 200 + valid data |
| TC-01698 | API | Export / import | Logged in | GET /api/export?assets with invalid input | 400/422 + error message |
| TC-01699 | API | Export / import | Edge case | GET /api/export?assets at boundary value | Correct boundary handling |
| TC-01700 | API | Export / import | No auth token | GET /api/export?assets | 401 Unauthorized |
| TC-01701 | frontend-UAT | Export / import | Logged in | Open export assets in UI | UI renders correctly |
| TC-01702 | frontend-UAT | Export / import | No data | Open export assets with no data | No-data state shown |
| TC-01703 | API | Export / import | Expired token | GET /api/export?assets | 401 Unauthorized |
| TC-01704 | API | Export / import | Insufficient role | GET /api/export?assets | 403 Forbidden |
| TC-01705 | API | Export / import | Logged in | POST /api/import?file | 200 + valid data |
| TC-01706 | API | Export / import | Logged in | POST /api/import?file with invalid input | 400/422 + error message |
| TC-01707 | API | Export / import | Edge case | POST /api/import?file at boundary value | Correct boundary handling |
| TC-01708 | API | Export / import | No auth token | POST /api/import?file | 401 Unauthorized |
| TC-01709 | frontend-UAT | Export / import | Logged in | Open import file in UI | UI renders correctly |
| TC-01710 | frontend-UAT | Export / import | No data | Open import file with no data | No-data state shown |
| TC-01711 | API | Export / import | Expired token | POST /api/import?file | 401 Unauthorized |
| TC-01712 | API | Export / import | Insufficient role | POST /api/import?file | 403 Forbidden |
| TC-01713 | API | Export / import | Logged in | POST /api/import?bad | 200 + valid data |
| TC-01714 | API | Export / import | Logged in | POST /api/import?bad with invalid input | 400/422 + error message |
| TC-01715 | API | Export / import | Edge case | POST /api/import?bad at boundary value | Correct boundary handling |
| TC-01716 | API | Export / import | No auth token | POST /api/import?bad | 401 Unauthorized |
| TC-01717 | frontend-UAT | Export / import | Logged in | Open import bad file in UI | UI renders correctly |
| TC-01718 | frontend-UAT | Export / import | No data | Open import bad file with no data | No-data state shown |
| TC-01719 | API | Export / import | Expired token | POST /api/import?bad | 401 Unauthorized |
| TC-01720 | API | Export / import | Insufficient role | POST /api/import?bad | 403 Forbidden |
| TC-01721 | API | Export / import | Logged in | POST /api/import?filters | 200 + valid data |
| TC-01722 | API | Export / import | Logged in | POST /api/import?filters with invalid input | 400/422 + error message |
| TC-01723 | API | Export / import | Edge case | POST /api/import?filters at boundary value | Correct boundary handling |
| TC-01724 | API | Export / import | No auth token | POST /api/import?filters | 401 Unauthorized |
| TC-01725 | frontend-UAT | Export / import | Logged in | Open import filters in UI | UI renders correctly |
| TC-01726 | frontend-UAT | Export / import | No data | Open import filters with no data | No-data state shown |
| TC-01727 | API | Export / import | Expired token | POST /api/import?filters | 401 Unauthorized |
| TC-01728 | API | Export / import | Insufficient role | POST /api/import?filters | 403 Forbidden |
| TC-01729 | API | Export / import | Logged in | GET /api/jobs/{id}/export | 200 + valid data |
| TC-01730 | API | Export / import | Logged in | GET /api/jobs/{id}/export with invalid input | 400/422 + error message |
| TC-01731 | API | Export / import | Edge case | GET /api/jobs/{id}/export at boundary value | Correct boundary handling |
| TC-01732 | API | Export / import | No auth token | GET /api/jobs/{id}/export | 401 Unauthorized |
| TC-01733 | frontend-UAT | Export / import | Logged in | Open export single job in UI | UI renders correctly |
| TC-01734 | frontend-UAT | Export / import | No data | Open export single job with no data | No-data state shown |
| TC-01735 | API | Export / import | Expired token | GET /api/jobs/{id}/export | 401 Unauthorized |
| TC-01736 | API | Export / import | Insufficient role | GET /api/jobs/{id}/export | 403 Forbidden |
| TC-01737 | API | Export / import | Logged in | POST /api/import?dedupe | 200 + valid data |
| TC-01738 | API | Export / import | Logged in | POST /api/import?dedupe with invalid input | 400/422 + error message |
| TC-01739 | API | Export / import | Edge case | POST /api/import?dedupe at boundary value | Correct boundary handling |
| TC-01740 | API | Export / import | No auth token | POST /api/import?dedupe | 401 Unauthorized |
| TC-01741 | frontend-UAT | Export / import | Logged in | Open import dedupe in UI | UI renders correctly |
| TC-01742 | frontend-UAT | Export / import | No data | Open import dedupe with no data | No-data state shown |
| TC-01743 | API | Export / import | Expired token | POST /api/import?dedupe | 401 Unauthorized |
| TC-01744 | API | Export / import | Insufficient role | POST /api/import?dedupe | 403 Forbidden |
| TC-01745 | API | Export / import | Logged in | GET /api/export?empty | 200 + valid data |
| TC-01746 | API | Export / import | Logged in | GET /api/export?empty with invalid input | 400/422 + error message |
| TC-01747 | API | Export / import | Edge case | GET /api/export?empty at boundary value | Correct boundary handling |
| TC-01748 | API | Export / import | No auth token | GET /api/export?empty | 401 Unauthorized |
| TC-01749 | frontend-UAT | Export / import | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01750 | frontend-UAT | Export / import | No data | Open no-data state with no data | No-data state shown |
| TC-01751 | API | Export / import | Expired token | GET /api/export?empty | 401 Unauthorized |
| TC-01752 | API | Export / import | Insufficient role | GET /api/export?empty | 403 Forbidden |
| TC-01753 | API | Export / import | Logged in | GET /api/export?csv | 200 + valid data |
| TC-01754 | API | Export / import | Logged in | GET /api/export?csv with invalid input | 400/422 + error message |
| TC-01755 | API | Export / import | Edge case | GET /api/export?csv at boundary value | Correct boundary handling |
| TC-01756 | API | Export / import | No auth token | GET /api/export?csv | 401 Unauthorized |
| TC-01757 | frontend-UAT | Export / import | Logged in | Open CSV render in UI | UI renders correctly |
| TC-01758 | frontend-UAT | Export / import | No data | Open CSV render with no data | No-data state shown |
| TC-01759 | API | Export / import | Expired token | GET /api/export?csv | 401 Unauthorized |
| TC-01760 | API | Export / import | Insufficient role | GET /api/export?csv | 403 Forbidden |
| TC-01761 | API | Export / import | Logged in | GET /api/export?json | 200 + valid data |
| TC-01762 | API | Export / import | Logged in | GET /api/export?json with invalid input | 400/422 + error message |
| TC-01763 | API | Export / import | Edge case | GET /api/export?json at boundary value | Correct boundary handling |
| TC-01764 | API | Export / import | No auth token | GET /api/export?json | 401 Unauthorized |
| TC-01765 | frontend-UAT | Export / import | Logged in | Open JSON render in UI | UI renders correctly |
| TC-01766 | frontend-UAT | Export / import | No data | Open JSON render with no data | No-data state shown |
| TC-01767 | API | Export / import | Expired token | GET /api/export?json | 401 Unauthorized |
| TC-01768 | API | Export / import | Insufficient role | GET /api/export?json | 403 Forbidden |
| TC-01769 | API | Export / import | Logged in | GET /api/import?preview | 200 + valid data |
| TC-01770 | API | Export / import | Logged in | GET /api/import?preview with invalid input | 400/422 + error message |
| TC-01771 | API | Export / import | Edge case | GET /api/import?preview at boundary value | Correct boundary handling |
| TC-01772 | API | Export / import | No auth token | GET /api/import?preview | 401 Unauthorized |
| TC-01773 | frontend-UAT | Export / import | Logged in | Open preview render in UI | UI renders correctly |
| TC-01774 | frontend-UAT | Export / import | No data | Open preview render with no data | No-data state shown |
| TC-01775 | API | Export / import | Expired token | GET /api/import?preview | 401 Unauthorized |
| TC-01776 | API | Export / import | Insufficient role | GET /api/import?preview | 403 Forbidden |
| TC-01777 | API | Export / import | Logged in | GET /api/import?error | 200 + valid data |
| TC-01778 | API | Export / import | Logged in | GET /api/import?error with invalid input | 400/422 + error message |
| TC-01779 | API | Export / import | Edge case | GET /api/import?error at boundary value | Correct boundary handling |
| TC-01780 | API | Export / import | No auth token | GET /api/import?error | 401 Unauthorized |
| TC-01781 | frontend-UAT | Export / import | Logged in | Open error highlight in UI | UI renders correctly |
| TC-01782 | frontend-UAT | Export / import | No data | Open error highlight with no data | No-data state shown |
| TC-01783 | API | Export / import | Expired token | GET /api/import?error | 401 Unauthorized |
| TC-01784 | API | Export / import | Insufficient role | GET /api/import?error | 403 Forbidden |
| TC-01785 | API | Export / import | Logged in | GET /api/export?resume | 200 + valid data |
| TC-01786 | API | Export / import | Logged in | GET /api/export?resume with invalid input | 400/422 + error message |
| TC-01787 | API | Export / import | Edge case | GET /api/export?resume at boundary value | Correct boundary handling |
| TC-01788 | API | Export / import | No auth token | GET /api/export?resume | 401 Unauthorized |
| TC-01789 | frontend-UAT | Export / import | Logged in | Open resume export in UI | UI renders correctly |
| TC-01790 | frontend-UAT | Export / import | No data | Open resume export with no data | No-data state shown |
| TC-01791 | API | Export / import | Expired token | GET /api/export?resume | 401 Unauthorized |
| TC-01792 | API | Export / import | Insufficient role | GET /api/export?resume | 403 Forbidden |
| TC-01793 | API | Export / import | Logged in | GET /api/export?mobile | 200 + valid data |
| TC-01794 | API | Export / import | Logged in | GET /api/export?mobile with invalid input | 400/422 + error message |
| TC-01795 | API | Export / import | Edge case | GET /api/export?mobile at boundary value | Correct boundary handling |
| TC-01796 | API | Export / import | No auth token | GET /api/export?mobile | 401 Unauthorized |
| TC-01797 | frontend-UAT | Export / import | Logged in | Open mobile view in UI | UI renders correctly |
| TC-01798 | frontend-UAT | Export / import | No data | Open mobile view with no data | No-data state shown |
| TC-01799 | API | Export / import | Expired token | GET /api/export?mobile | 401 Unauthorized |
| TC-01800 | API | Export / import | Insufficient role | GET /api/export?mobile | 403 Forbidden |
### F15 — More job sources

| TC-01801 | API | More job sources | Logged in | POST /api/sources/connect | 200 + valid data |
| TC-01802 | API | More job sources | Logged in | POST /api/sources/connect with invalid input | 400/422 + error message |
| TC-01803 | API | More job sources | Edge case | POST /api/sources/connect at boundary value | Correct boundary handling |
| TC-01804 | API | More job sources | No auth token | POST /api/sources/connect | 401 Unauthorized |
| TC-01805 | frontend-UAT | More job sources | Logged in | Open connect source in UI | UI renders correctly |
| TC-01806 | frontend-UAT | More job sources | No data | Open connect source with no data | No-data state shown |
| TC-01807 | API | More job sources | Expired token | POST /api/sources/connect | 401 Unauthorized |
| TC-01808 | API | More job sources | Insufficient role | POST /api/sources/connect | 403 Forbidden |
| TC-01809 | API | More job sources | Logged in | GET /api/sources | 200 + valid data |
| TC-01810 | API | More job sources | Logged in | GET /api/sources with invalid input | 400/422 + error message |
| TC-01811 | API | More job sources | Edge case | GET /api/sources at boundary value | Correct boundary handling |
| TC-01812 | API | More job sources | No auth token | GET /api/sources | 401 Unauthorized |
| TC-01813 | frontend-UAT | More job sources | Logged in | Open jobs from all sources in UI | UI renders correctly |
| TC-01814 | frontend-UAT | More job sources | No data | Open jobs from all sources with no data | No-data state shown |
| TC-01815 | API | More job sources | Expired token | GET /api/sources | 401 Unauthorized |
| TC-01816 | API | More job sources | Insufficient role | GET /api/sources | 403 Forbidden |
| TC-01817 | API | More job sources | Logged in | GET /api/sources/list | 200 + valid data |
| TC-01818 | API | More job sources | Logged in | GET /api/sources/list with invalid input | 400/422 + error message |
| TC-01819 | API | More job sources | Edge case | GET /api/sources/list at boundary value | Correct boundary handling |
| TC-01820 | API | More job sources | No auth token | GET /api/sources/list | 401 Unauthorized |
| TC-01821 | frontend-UAT | More job sources | Logged in | Open connected sources in UI | UI renders correctly |
| TC-01822 | frontend-UAT | More job sources | No data | Open connected sources with no data | No-data state shown |
| TC-01823 | API | More job sources | Expired token | GET /api/sources/list | 401 Unauthorized |
| TC-01824 | API | More job sources | Insufficient role | GET /api/sources/list | 403 Forbidden |
| TC-01825 | API | More job sources | Logged in | DELETE /api/sources/{id} | 200 + valid data |
| TC-01826 | API | More job sources | Logged in | DELETE /api/sources/{id} with invalid input | 400/422 + error message |
| TC-01827 | API | More job sources | Edge case | DELETE /api/sources/{id} at boundary value | Correct boundary handling |
| TC-01828 | API | More job sources | No auth token | DELETE /api/sources/{id} | 401 Unauthorized |
| TC-01829 | frontend-UAT | More job sources | Logged in | Open disconnect source in UI | UI renders correctly |
| TC-01830 | frontend-UAT | More job sources | No data | Open disconnect source with no data | No-data state shown |
| TC-01831 | API | More job sources | Expired token | DELETE /api/sources/{id} | 401 Unauthorized |
| TC-01832 | API | More job sources | Insufficient role | DELETE /api/sources/{id} | 403 Forbidden |
| TC-01833 | API | More job sources | Logged in | GET /api/sources/sync-status | 200 + valid data |
| TC-01834 | API | More job sources | Logged in | GET /api/sources/sync-status with invalid input | 400/422 + error message |
| TC-01835 | API | More job sources | Edge case | GET /api/sources/sync-status at boundary value | Correct boundary handling |
| TC-01836 | API | More job sources | No auth token | GET /api/sources/sync-status | 401 Unauthorized |
| TC-01837 | frontend-UAT | More job sources | Logged in | Open sync status in UI | UI renders correctly |
| TC-01838 | frontend-UAT | More job sources | No data | Open sync status with no data | No-data state shown |
| TC-01839 | API | More job sources | Expired token | GET /api/sources/sync-status | 401 Unauthorized |
| TC-01840 | API | More job sources | Insufficient role | GET /api/sources/sync-status | 403 Forbidden |
| TC-01841 | API | More job sources | Logged in | POST /api/sources/merge | 200 + valid data |
| TC-01842 | API | More job sources | Logged in | POST /api/sources/merge with invalid input | 400/422 + error message |
| TC-01843 | API | More job sources | Edge case | POST /api/sources/merge at boundary value | Correct boundary handling |
| TC-01844 | API | More job sources | No auth token | POST /api/sources/merge | 401 Unauthorized |
| TC-01845 | frontend-UAT | More job sources | Logged in | Open merge duplicates in UI | UI renders correctly |
| TC-01846 | frontend-UAT | More job sources | No data | Open merge duplicates with no data | No-data state shown |
| TC-01847 | API | More job sources | Expired token | POST /api/sources/merge | 401 Unauthorized |
| TC-01848 | API | More job sources | Insufficient role | POST /api/sources/merge | 403 Forbidden |
| TC-01849 | API | More job sources | Logged in | GET /api/sources/recent-count | 200 + valid data |
| TC-01850 | API | More job sources | Logged in | GET /api/sources/recent-count with invalid input | 400/422 + error message |
| TC-01851 | API | More job sources | Edge case | GET /api/sources/recent-count at boundary value | Correct boundary handling |
| TC-01852 | API | More job sources | No auth token | GET /api/sources/recent-count | 401 Unauthorized |
| TC-01853 | frontend-UAT | More job sources | Logged in | Open recent count in UI | UI renders correctly |
| TC-01854 | frontend-UAT | More job sources | No data | Open recent count with no data | No-data state shown |
| TC-01855 | API | More job sources | Expired token | GET /api/sources/recent-count | 401 Unauthorized |
| TC-01856 | API | More job sources | Insufficient role | GET /api/sources/recent-count | 403 Forbidden |
| TC-01857 | API | More job sources | Logged in | POST /api/sources/custom | 200 + valid data |
| TC-01858 | API | More job sources | Logged in | POST /api/sources/custom with invalid input | 400/422 + error message |
| TC-01859 | API | More job sources | Edge case | POST /api/sources/custom at boundary value | Correct boundary handling |
| TC-01860 | API | More job sources | No auth token | POST /api/sources/custom | 401 Unauthorized |
| TC-01861 | frontend-UAT | More job sources | Logged in | Open custom URL in UI | UI renders correctly |
| TC-01862 | frontend-UAT | More job sources | No data | Open custom URL with no data | No-data state shown |
| TC-01863 | API | More job sources | Expired token | POST /api/sources/custom | 401 Unauthorized |
| TC-01864 | API | More job sources | Insufficient role | POST /api/sources/custom | 403 Forbidden |
| TC-01865 | API | More job sources | Logged in | GET /api/sources?empty | 200 + valid data |
| TC-01866 | API | More job sources | Logged in | GET /api/sources?empty with invalid input | 400/422 + error message |
| TC-01867 | API | More job sources | Edge case | GET /api/sources?empty at boundary value | Correct boundary handling |
| TC-01868 | API | More job sources | No auth token | GET /api/sources?empty | 401 Unauthorized |
| TC-01869 | frontend-UAT | More job sources | Logged in | Open no-data state in UI | UI renders correctly |
| TC-01870 | frontend-UAT | More job sources | No data | Open no-data state with no data | No-data state shown |
| TC-01871 | API | More job sources | Expired token | GET /api/sources?empty | 401 Unauthorized |
| TC-01872 | API | More job sources | Insufficient role | GET /api/sources?empty | 403 Forbidden |
| TC-01873 | API | More job sources | Logged in | GET /api/sources?connect | 200 + valid data |
| TC-01874 | API | More job sources | Logged in | GET /api/sources?connect with invalid input | 400/422 + error message |
| TC-01875 | API | More job sources | Edge case | GET /api/sources?connect at boundary value | Correct boundary handling |
| TC-01876 | API | More job sources | No auth token | GET /api/sources?connect | 401 Unauthorized |
| TC-01877 | frontend-UAT | More job sources | Logged in | Open connect form in UI | UI renders correctly |
| TC-01878 | frontend-UAT | More job sources | No data | Open connect form with no data | No-data state shown |
| TC-01879 | API | More job sources | Expired token | GET /api/sources?connect | 401 Unauthorized |
| TC-01880 | API | More job sources | Insufficient role | GET /api/sources?connect | 403 Forbidden |
| TC-01881 | API | More job sources | Logged in | GET /api/sources?disconnect | 200 + valid data |
| TC-01882 | API | More job sources | Logged in | GET /api/sources?disconnect with invalid input | 400/422 + error message |
| TC-01883 | API | More job sources | Edge case | GET /api/sources?disconnect at boundary value | Correct boundary handling |
| TC-01884 | API | More job sources | No auth token | GET /api/sources?disconnect | 401 Unauthorized |
| TC-01885 | frontend-UAT | More job sources | Logged in | Open disconnect render in UI | UI renders correctly |
| TC-01886 | frontend-UAT | More job sources | No data | Open disconnect render with no data | No-data state shown |
| TC-01887 | API | More job sources | Expired token | GET /api/sources?disconnect | 401 Unauthorized |
| TC-01888 | API | More job sources | Insufficient role | GET /api/sources?disconnect | 403 Forbidden |
| TC-01889 | API | More job sources | Logged in | GET /api/sources?sync | 200 + valid data |
| TC-01890 | API | More job sources | Logged in | GET /api/sources?sync with invalid input | 400/422 + error message |
| TC-01891 | API | More job sources | Edge case | GET /api/sources?sync at boundary value | Correct boundary handling |
| TC-01892 | API | More job sources | No auth token | GET /api/sources?sync | 401 Unauthorized |
| TC-01893 | frontend-UAT | More job sources | Logged in | Open sync render in UI | UI renders correctly |
| TC-01894 | frontend-UAT | More job sources | No data | Open sync render with no data | No-data state shown |
| TC-01895 | API | More job sources | Expired token | GET /api/sources?sync | 401 Unauthorized |
| TC-01896 | API | More job sources | Insufficient role | GET /api/sources?sync | 403 Forbidden |
| TC-01897 | API | More job sources | Logged in | GET /api/sources?merge | 200 + valid data |
| TC-01898 | API | More job sources | Logged in | GET /api/sources?merge with invalid input | 400/422 + error message |
| TC-01899 | API | More job sources | Edge case | GET /api/sources?merge at boundary value | Correct boundary handling |
| TC-01900 | API | More job sources | No auth token | GET /api/sources?merge | 401 Unauthorized |
| TC-01901 | frontend-UAT | More job sources | Logged in | Open merge render in UI | UI renders correctly |
| TC-01902 | frontend-UAT | More job sources | No data | Open merge render with no data | No-data state shown |
| TC-01903 | API | More job sources | Expired token | GET /api/sources?merge | 401 Unauthorized |
| TC-01904 | API | More job sources | Insufficient role | GET /api/sources?merge | 403 Forbidden |
| TC-01905 | API | More job sources | Logged in | GET /api/sources?custom | 200 + valid data |
| TC-01906 | API | More job sources | Logged in | GET /api/sources?custom with invalid input | 400/422 + error message |
| TC-01907 | API | More job sources | Edge case | GET /api/sources?custom at boundary value | Correct boundary handling |
| TC-01908 | API | More job sources | No auth token | GET /api/sources?custom | 401 Unauthorized |
| TC-01909 | frontend-UAT | More job sources | Logged in | Open custom render in UI | UI renders correctly |
| TC-01910 | frontend-UAT | More job sources | No data | Open custom render with no data | No-data state shown |
| TC-01911 | API | More job sources | Expired token | GET /api/sources?custom | 401 Unauthorized |
| TC-01912 | API | More job sources | Insufficient role | GET /api/sources?custom | 403 Forbidden |
| TC-01913 | API | More job sources | Logged in | GET /api/sources?export | 200 + valid data |
| TC-01914 | API | More job sources | Logged in | GET /api/sources?export with invalid input | 400/422 + error message |
| TC-01915 | API | More job sources | Edge case | GET /api/sources?export at boundary value | Correct boundary handling |
| TC-01916 | API | More job sources | No auth token | GET /api/sources?export | 401 Unauthorized |
| TC-01917 | frontend-UAT | More job sources | Logged in | Open export sources in UI | UI renders correctly |
| TC-01918 | frontend-UAT | More job sources | No data | Open export sources with no data | No-data state shown |
| TC-01919 | API | More job sources | Expired token | GET /api/sources?export | 401 Unauthorized |
| TC-01920 | API | More job sources | Insufficient role | GET /api/sources?export | 403 Forbidden |
### F17 — Scheduler + enrichment

| TC-01921 | API | Scheduler + enrichment | Logged in | POST /api/schedule | 200 + valid data |
| TC-01922 | API | Scheduler + enrichment | Logged in | POST /api/schedule with invalid input | 400/422 + error message |
| TC-01923 | API | Scheduler + enrichment | Edge case | POST /api/schedule at boundary value | Correct boundary handling |
| TC-01924 | API | Scheduler + enrichment | No auth token | POST /api/schedule | 401 Unauthorized |
| TC-01925 | frontend-UAT | Scheduler + enrichment | Logged in | Open schedule scrape in UI | UI renders correctly |
| TC-01926 | frontend-UAT | Scheduler + enrichment | No data | Open schedule scrape with no data | No-data state shown |
| TC-01927 | API | Scheduler + enrichment | Expired token | POST /api/schedule | 401 Unauthorized |
| TC-01928 | API | Scheduler + enrichment | Insufficient role | POST /api/schedule | 403 Forbidden |
| TC-01929 | API | Scheduler + enrichment | Logged in | GET /api/schedule/next | 200 + valid data |
| TC-01930 | API | Scheduler + enrichment | Logged in | GET /api/schedule/next with invalid input | 400/422 + error message |
| TC-01931 | API | Scheduler + enrichment | Edge case | GET /api/schedule/next at boundary value | Correct boundary handling |
| TC-01932 | API | Scheduler + enrichment | No auth token | GET /api/schedule/next | 401 Unauthorized |
| TC-01933 | frontend-UAT | Scheduler + enrichment | Logged in | Open next run in UI | UI renders correctly |
| TC-01934 | frontend-UAT | Scheduler + enrichment | No data | Open next run with no data | No-data state shown |
| TC-01935 | API | Scheduler + enrichment | Expired token | GET /api/schedule/next | 401 Unauthorized |
| TC-01936 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule/next | 403 Forbidden |
| TC-01937 | API | Scheduler + enrichment | Logged in | PUT /api/schedule/{id}/pause | 200 + valid data |
| TC-01938 | API | Scheduler + enrichment | Logged in | PUT /api/schedule/{id}/pause with invalid input | 400/422 + error message |
| TC-01939 | API | Scheduler + enrichment | Edge case | PUT /api/schedule/{id}/pause at boundary value | Correct boundary handling |
| TC-01940 | API | Scheduler + enrichment | No auth token | PUT /api/schedule/{id}/pause | 401 Unauthorized |
| TC-01941 | frontend-UAT | Scheduler + enrichment | Logged in | Open pause schedule in UI | UI renders correctly |
| TC-01942 | frontend-UAT | Scheduler + enrichment | No data | Open pause schedule with no data | No-data state shown |
| TC-01943 | API | Scheduler + enrichment | Expired token | PUT /api/schedule/{id}/pause | 401 Unauthorized |
| TC-01944 | API | Scheduler + enrichment | Insufficient role | PUT /api/schedule/{id}/pause | 403 Forbidden |
| TC-01945 | API | Scheduler + enrichment | Logged in | POST /api/enrich/{job_id} | 200 + valid data |
| TC-01946 | API | Scheduler + enrichment | Logged in | POST /api/enrich/{job_id} with invalid input | 400/422 + error message |
| TC-01947 | API | Scheduler + enrichment | Edge case | POST /api/enrich/{job_id} at boundary value | Correct boundary handling |
| TC-01948 | API | Scheduler + enrichment | No auth token | POST /api/enrich/{job_id} | 401 Unauthorized |
| TC-01949 | frontend-UAT | Scheduler + enrichment | Logged in | Open enrich job in UI | UI renders correctly |
| TC-01950 | frontend-UAT | Scheduler + enrichment | No data | Open enrich job with no data | No-data state shown |
| TC-01951 | API | Scheduler + enrichment | Expired token | POST /api/enrich/{job_id} | 401 Unauthorized |
| TC-01952 | API | Scheduler + enrichment | Insufficient role | POST /api/enrich/{job_id} | 403 Forbidden |
| TC-01953 | API | Scheduler + enrichment | Logged in | GET /api/enrich/{job_id}/status | 200 + valid data |
| TC-01954 | API | Scheduler + enrichment | Logged in | GET /api/enrich/{job_id}/status with invalid input | 400/422 + error message |
| TC-01955 | API | Scheduler + enrichment | Edge case | GET /api/enrich/{job_id}/status at boundary value | Correct boundary handling |
| TC-01956 | API | Scheduler + enrichment | No auth token | GET /api/enrich/{job_id}/status | 401 Unauthorized |
| TC-01957 | frontend-UAT | Scheduler + enrichment | Logged in | Open enrichment status in UI | UI renders correctly |
| TC-01958 | frontend-UAT | Scheduler + enrichment | No data | Open enrichment status with no data | No-data state shown |
| TC-01959 | API | Scheduler + enrichment | Expired token | GET /api/enrich/{job_id}/status | 401 Unauthorized |
| TC-01960 | API | Scheduler + enrichment | Insufficient role | GET /api/enrich/{job_id}/status | 403 Forbidden |
| TC-01961 | API | Scheduler + enrichment | Logged in | GET /api/schedule/logs | 200 + valid data |
| TC-01962 | API | Scheduler + enrichment | Logged in | GET /api/schedule/logs with invalid input | 400/422 + error message |
| TC-01963 | API | Scheduler + enrichment | Edge case | GET /api/schedule/logs at boundary value | Correct boundary handling |
| TC-01964 | API | Scheduler + enrichment | No auth token | GET /api/schedule/logs | 401 Unauthorized |
| TC-01965 | frontend-UAT | Scheduler + enrichment | Logged in | Open scrape log in UI | UI renders correctly |
| TC-01966 | frontend-UAT | Scheduler + enrichment | No data | Open scrape log with no data | No-data state shown |
| TC-01967 | API | Scheduler + enrichment | Expired token | GET /api/schedule/logs | 401 Unauthorized |
| TC-01968 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule/logs | 403 Forbidden |
| TC-01969 | API | Scheduler + enrichment | Logged in | PUT /api/schedule/{id}/freq | 200 + valid data |
| TC-01970 | API | Scheduler + enrichment | Logged in | PUT /api/schedule/{id}/freq with invalid input | 400/422 + error message |
| TC-01971 | API | Scheduler + enrichment | Edge case | PUT /api/schedule/{id}/freq at boundary value | Correct boundary handling |
| TC-01972 | API | Scheduler + enrichment | No auth token | PUT /api/schedule/{id}/freq | 401 Unauthorized |
| TC-01973 | frontend-UAT | Scheduler + enrichment | Logged in | Open change frequency in UI | UI renders correctly |
| TC-01974 | frontend-UAT | Scheduler + enrichment | No data | Open change frequency with no data | No-data state shown |
| TC-01975 | API | Scheduler + enrichment | Expired token | PUT /api/schedule/{id}/freq | 401 Unauthorized |
| TC-01976 | API | Scheduler + enrichment | Insufficient role | PUT /api/schedule/{id}/freq | 403 Forbidden |
| TC-01977 | API | Scheduler + enrichment | Logged in | GET /api/schedule/last | 200 + valid data |
| TC-01978 | API | Scheduler + enrichment | Logged in | GET /api/schedule/last with invalid input | 400/422 + error message |
| TC-01979 | API | Scheduler + enrichment | Edge case | GET /api/schedule/last at boundary value | Correct boundary handling |
| TC-01980 | API | Scheduler + enrichment | No auth token | GET /api/schedule/last | 401 Unauthorized |
| TC-01981 | frontend-UAT | Scheduler + enrichment | Logged in | Open last result in UI | UI renders correctly |
| TC-01982 | frontend-UAT | Scheduler + enrichment | No data | Open last result with no data | No-data state shown |
| TC-01983 | API | Scheduler + enrichment | Expired token | GET /api/schedule/last | 401 Unauthorized |
| TC-01984 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule/last | 403 Forbidden |
| TC-01985 | API | Scheduler + enrichment | Logged in | GET /api/schedule/logs?error | 200 + valid data |
| TC-01986 | API | Scheduler + enrichment | Logged in | GET /api/schedule/logs?error with invalid input | 400/422 + error message |
| TC-01987 | API | Scheduler + enrichment | Edge case | GET /api/schedule/logs?error at boundary value | Correct boundary handling |
| TC-01988 | API | Scheduler + enrichment | No auth token | GET /api/schedule/logs?error | 401 Unauthorized |
| TC-01989 | frontend-UAT | Scheduler + enrichment | Logged in | Open error alerts in UI | UI renders correctly |
| TC-01990 | frontend-UAT | Scheduler + enrichment | No data | Open error alerts with no data | No-data state shown |
| TC-01991 | API | Scheduler + enrichment | Expired token | GET /api/schedule/logs?error | 401 Unauthorized |
| TC-01992 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule/logs?error | 403 Forbidden |
| TC-01993 | API | Scheduler + enrichment | Logged in | GET /api/schedule/summary | 200 + valid data |
| TC-01994 | API | Scheduler + enrichment | Logged in | GET /api/schedule/summary with invalid input | 400/422 + error message |
| TC-01995 | API | Scheduler + enrichment | Edge case | GET /api/schedule/summary at boundary value | Correct boundary handling |
| TC-01996 | API | Scheduler + enrichment | No auth token | GET /api/schedule/summary | 401 Unauthorized |
| TC-01997 | frontend-UAT | Scheduler + enrichment | Logged in | Open scrape summary in UI | UI renders correctly |
| TC-01998 | frontend-UAT | Scheduler + enrichment | No data | Open scrape summary with no data | No-data state shown |
| TC-01999 | API | Scheduler + enrichment | Expired token | GET /api/schedule/summary | 401 Unauthorized |
| TC-02000 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule/summary | 403 Forbidden |
| TC-02001 | API | Scheduler + enrichment | Logged in | POST /api/schedule/one-time | 200 + valid data |
| TC-02002 | API | Scheduler + enrichment | Logged in | POST /api/schedule/one-time with invalid input | 400/422 + error message |
| TC-02003 | API | Scheduler + enrichment | Edge case | POST /api/schedule/one-time at boundary value | Correct boundary handling |
| TC-02004 | API | Scheduler + enrichment | No auth token | POST /api/schedule/one-time | 401 Unauthorized |
| TC-02005 | frontend-UAT | Scheduler + enrichment | Logged in | Open one-time scrape in UI | UI renders correctly |
| TC-02006 | frontend-UAT | Scheduler + enrichment | No data | Open one-time scrape with no data | No-data state shown |
| TC-02007 | API | Scheduler + enrichment | Expired token | POST /api/schedule/one-time | 401 Unauthorized |
| TC-02008 | API | Scheduler + enrichment | Insufficient role | POST /api/schedule/one-time | 403 Forbidden |
| TC-02009 | API | Scheduler + enrichment | Logged in | POST /api/enrich/bulk | 200 + valid data |
| TC-02010 | API | Scheduler + enrichment | Logged in | POST /api/enrich/bulk with invalid input | 400/422 + error message |
| TC-02011 | API | Scheduler + enrichment | Edge case | POST /api/enrich/bulk at boundary value | Correct boundary handling |
| TC-02012 | API | Scheduler + enrichment | No auth token | POST /api/enrich/bulk | 401 Unauthorized |
| TC-02013 | frontend-UAT | Scheduler + enrichment | Logged in | Open bulk enrich in UI | UI renders correctly |
| TC-02014 | frontend-UAT | Scheduler + enrichment | No data | Open bulk enrich with no data | No-data state shown |
| TC-02015 | API | Scheduler + enrichment | Expired token | POST /api/enrich/bulk | 401 Unauthorized |
| TC-02016 | API | Scheduler + enrichment | Insufficient role | POST /api/enrich/bulk | 403 Forbidden |
| TC-02017 | API | Scheduler + enrichment | Logged in | GET /api/schedule?empty | 200 + valid data |
| TC-02018 | API | Scheduler + enrichment | Logged in | GET /api/schedule?empty with invalid input | 400/422 + error message |
| TC-02019 | API | Scheduler + enrichment | Edge case | GET /api/schedule?empty at boundary value | Correct boundary handling |
| TC-02020 | API | Scheduler + enrichment | No auth token | GET /api/schedule?empty | 401 Unauthorized |
| TC-02021 | frontend-UAT | Scheduler + enrichment | Logged in | Open no-data state in UI | UI renders correctly |
| TC-02022 | frontend-UAT | Scheduler + enrichment | No data | Open no-data state with no data | No-data state shown |
| TC-02023 | API | Scheduler + enrichment | Expired token | GET /api/schedule?empty | 401 Unauthorized |
| TC-02024 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule?empty | 403 Forbidden |
| TC-02025 | API | Scheduler + enrichment | Logged in | GET /api/schedule?cards | 200 + valid data |
| TC-02026 | API | Scheduler + enrichment | Logged in | GET /api/schedule?cards with invalid input | 400/422 + error message |
| TC-02027 | API | Scheduler + enrichment | Edge case | GET /api/schedule?cards at boundary value | Correct boundary handling |
| TC-02028 | API | Scheduler + enrichment | No auth token | GET /api/schedule?cards | 401 Unauthorized |
| TC-02029 | frontend-UAT | Scheduler + enrichment | Logged in | Open cards render in UI | UI renders correctly |
| TC-02030 | frontend-UAT | Scheduler + enrichment | No data | Open cards render with no data | No-data state shown |
| TC-02031 | API | Scheduler + enrichment | Expired token | GET /api/schedule?cards | 401 Unauthorized |
| TC-02032 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule?cards | 403 Forbidden |
| TC-02033 | API | Scheduler + enrichment | Logged in | GET /api/schedule?pause | 200 + valid data |
| TC-02034 | API | Scheduler + enrichment | Logged in | GET /api/schedule?pause with invalid input | 400/422 + error message |
| TC-02035 | API | Scheduler + enrichment | Edge case | GET /api/schedule?pause at boundary value | Correct boundary handling |
| TC-02036 | API | Scheduler + enrichment | No auth token | GET /api/schedule?pause | 401 Unauthorized |
| TC-02037 | frontend-UAT | Scheduler + enrichment | Logged in | Open pause render in UI | UI renders correctly |
| TC-02038 | frontend-UAT | Scheduler + enrichment | No data | Open pause render with no data | No-data state shown |
| TC-02039 | API | Scheduler + enrichment | Expired token | GET /api/schedule?pause | 401 Unauthorized |
| TC-02040 | API | Scheduler + enrichment | Insufficient role | GET /api/schedule?pause | 403 Forbidden |
### F18 — Desktop app

| TC-02041 | API | Desktop app | Logged in | GET /api/desktop/install | 200 + valid data |
| TC-02042 | API | Desktop app | Logged in | GET /api/desktop/install with invalid input | 400/422 + error message |
| TC-02043 | API | Desktop app | Edge case | GET /api/desktop/install at boundary value | Correct boundary handling |
| TC-02044 | API | Desktop app | No auth token | GET /api/desktop/install | 401 Unauthorized |
| TC-02045 | frontend-UAT | Desktop app | Logged in | Open install app in UI | UI renders correctly |
| TC-02046 | frontend-UAT | Desktop app | No data | Open install app with no data | No-data state shown |
| TC-02047 | API | Desktop app | Expired token | GET /api/desktop/install | 401 Unauthorized |
| TC-02048 | API | Desktop app | Insufficient role | GET /api/desktop/install | 403 Forbidden |
| TC-02049 | API | Desktop app | Logged in | GET /api/desktop/launch | 200 + valid data |
| TC-02050 | API | Desktop app | Logged in | GET /api/desktop/launch with invalid input | 400/422 + error message |
| TC-02051 | API | Desktop app | Edge case | GET /api/desktop/launch at boundary value | Correct boundary handling |
| TC-02052 | API | Desktop app | No auth token | GET /api/desktop/launch | 401 Unauthorized |
| TC-02053 | frontend-UAT | Desktop app | Logged in | Open launch app in UI | UI renders correctly |
| TC-02054 | frontend-UAT | Desktop app | No data | Open launch app with no data | No-data state shown |
| TC-02055 | API | Desktop app | Expired token | GET /api/desktop/launch | 401 Unauthorized |
| TC-02056 | API | Desktop app | Insufficient role | GET /api/desktop/launch | 403 Forbidden |
| TC-02057 | API | Desktop app | Logged in | GET /api/desktop/notifications | 200 + valid data |
| TC-02058 | API | Desktop app | Logged in | GET /api/desktop/notifications with invalid input | 400/422 + error message |
| TC-02059 | API | Desktop app | Edge case | GET /api/desktop/notifications at boundary value | Correct boundary handling |
| TC-02060 | API | Desktop app | No auth token | GET /api/desktop/notifications | 401 Unauthorized |
| TC-02061 | frontend-UAT | Desktop app | Logged in | Open notifications in UI | UI renders correctly |
| TC-02062 | frontend-UAT | Desktop app | No data | Open notifications with no data | No-data state shown |
| TC-02063 | API | Desktop app | Expired token | GET /api/desktop/notifications | 401 Unauthorized |
| TC-02064 | API | Desktop app | Insufficient role | GET /api/desktop/notifications | 403 Forbidden |
| TC-02065 | API | Desktop app | Logged in | GET /api/desktop/sync | 200 + valid data |
| TC-02066 | API | Desktop app | Logged in | GET /api/desktop/sync with invalid input | 400/422 + error message |
| TC-02067 | API | Desktop app | Edge case | GET /api/desktop/sync at boundary value | Correct boundary handling |
| TC-02068 | API | Desktop app | No auth token | GET /api/desktop/sync | 401 Unauthorized |
| TC-02069 | frontend-UAT | Desktop app | Logged in | Open sync data in UI | UI renders correctly |
| TC-02070 | frontend-UAT | Desktop app | No data | Open sync data with no data | No-data state shown |
| TC-02071 | API | Desktop app | Expired token | GET /api/desktop/sync | 401 Unauthorized |
| TC-02072 | API | Desktop app | Insufficient role | GET /api/desktop/sync | 403 Forbidden |
| TC-02073 | API | Desktop app | Logged in | GET /api/desktop/macos | 200 + valid data |
| TC-02074 | API | Desktop app | Logged in | GET /api/desktop/macos with invalid input | 400/422 + error message |
| TC-02075 | API | Desktop app | Edge case | GET /api/desktop/macos at boundary value | Correct boundary handling |
| TC-02076 | API | Desktop app | No auth token | GET /api/desktop/macos | 401 Unauthorized |
| TC-02077 | frontend-UAT | Desktop app | Logged in | Open macOS support in UI | UI renders correctly |
| TC-02078 | frontend-UAT | Desktop app | No data | Open macOS support with no data | No-data state shown |
| TC-02079 | API | Desktop app | Expired token | GET /api/desktop/macos | 401 Unauthorized |
| TC-02080 | API | Desktop app | Insufficient role | GET /api/desktop/macos | 403 Forbidden |
| TC-02081 | API | Desktop app | Logged in | GET /api/desktop/offline | 200 + valid data |
| TC-02082 | API | Desktop app | Logged in | GET /api/desktop/offline with invalid input | 400/422 + error message |
| TC-02083 | API | Desktop app | Edge case | GET /api/desktop/offline at boundary value | Correct boundary handling |
| TC-02084 | API | Desktop app | No auth token | GET /api/desktop/offline | 401 Unauthorized |
| TC-02085 | frontend-UAT | Desktop app | Logged in | Open offline indicator in UI | UI renders correctly |
| TC-02086 | frontend-UAT | Desktop app | No data | Open offline indicator with no data | No-data state shown |
| TC-02087 | API | Desktop app | Expired token | GET /api/desktop/offline | 401 Unauthorized |
| TC-02088 | API | Desktop app | Insufficient role | GET /api/desktop/offline | 403 Forbidden |
| TC-02089 | API | Desktop app | Logged in | GET /api/desktop/minimize | 200 + valid data |
| TC-02090 | API | Desktop app | Logged in | GET /api/desktop/minimize with invalid input | 400/422 + error message |
| TC-02091 | API | Desktop app | Edge case | GET /api/desktop/minimize at boundary value | Correct boundary handling |
| TC-02092 | API | Desktop app | No auth token | GET /api/desktop/minimize | 401 Unauthorized |
| TC-02093 | frontend-UAT | Desktop app | Logged in | Open minimize to tray in UI | UI renders correctly |
| TC-02094 | frontend-UAT | Desktop app | No data | Open minimize to tray with no data | No-data state shown |
| TC-02095 | API | Desktop app | Expired token | GET /api/desktop/minimize | 401 Unauthorized |
| TC-02096 | API | Desktop app | Insufficient role | GET /api/desktop/minimize | 403 Forbidden |
| TC-02097 | API | Desktop app | Logged in | GET /api/desktop/auto-start | 200 + valid data |
| TC-02098 | API | Desktop app | Logged in | GET /api/desktop/auto-start with invalid input | 400/422 + error message |
| TC-02099 | API | Desktop app | Edge case | GET /api/desktop/auto-start at boundary value | Correct boundary handling |
| TC-02100 | API | Desktop app | No auth token | GET /api/desktop/auto-start | 401 Unauthorized |
| TC-02101 | frontend-UAT | Desktop app | Logged in | Open auto start in UI | UI renders correctly |
| TC-02102 | frontend-UAT | Desktop app | No data | Open auto start with no data | No-data state shown |
| TC-02103 | API | Desktop app | Expired token | GET /api/desktop/auto-start | 401 Unauthorized |
| TC-02104 | API | Desktop app | Insufficient role | GET /api/desktop/auto-start | 403 Forbidden |
| TC-02105 | API | Desktop app | Logged in | GET /api/desktop/badge | 200 + valid data |
| TC-02106 | API | Desktop app | Logged in | GET /api/desktop/badge with invalid input | 400/422 + error message |
| TC-02107 | API | Desktop app | Edge case | GET /api/desktop/badge at boundary value | Correct boundary handling |
| TC-02108 | API | Desktop app | No auth token | GET /api/desktop/badge | 401 Unauthorized |
| TC-02109 | frontend-UAT | Desktop app | Logged in | Open badge count in UI | UI renders correctly |
| TC-02110 | frontend-UAT | Desktop app | No data | Open badge count with no data | No-data state shown |
| TC-02111 | API | Desktop app | Expired token | GET /api/desktop/badge | 401 Unauthorized |
| TC-02112 | API | Desktop app | Insufficient role | GET /api/desktop/badge | 403 Forbidden |
| TC-02113 | API | Desktop app | Logged in | GET /api/desktop/sounds | 200 + valid data |
| TC-02114 | API | Desktop app | Logged in | GET /api/desktop/sounds with invalid input | 400/422 + error message |
| TC-02115 | API | Desktop app | Edge case | GET /api/desktop/sounds at boundary value | Correct boundary handling |
| TC-02116 | API | Desktop app | No auth token | GET /api/desktop/sounds | 401 Unauthorized |
| TC-02117 | frontend-UAT | Desktop app | Logged in | Open notification sounds in UI | UI renders correctly |
| TC-02118 | frontend-UAT | Desktop app | No data | Open notification sounds with no data | No-data state shown |
| TC-02119 | API | Desktop app | Expired token | GET /api/desktop/sounds | 401 Unauthorized |
| TC-02120 | API | Desktop app | Insufficient role | GET /api/desktop/sounds | 403 Forbidden |
| TC-02121 | API | Desktop app | Logged in | GET /api/desktop/version | 200 + valid data |
| TC-02122 | API | Desktop app | Logged in | GET /api/desktop/version with invalid input | 400/422 + error message |
| TC-02123 | API | Desktop app | Edge case | GET /api/desktop/version at boundary value | Correct boundary handling |
| TC-02124 | API | Desktop app | No auth token | GET /api/desktop/version | 401 Unauthorized |
| TC-02125 | frontend-UAT | Desktop app | Logged in | Open version info in UI | UI renders correctly |
| TC-02126 | frontend-UAT | Desktop app | No data | Open version info with no data | No-data state shown |
| TC-02127 | API | Desktop app | Expired token | GET /api/desktop/version | 401 Unauthorized |
| TC-02128 | API | Desktop app | Insufficient role | GET /api/desktop/version | 403 Forbidden |
| TC-02129 | API | Desktop app | Logged in | GET /api/desktop/updates | 200 + valid data |
| TC-02130 | API | Desktop app | Logged in | GET /api/desktop/updates with invalid input | 400/422 + error message |
| TC-02131 | API | Desktop app | Edge case | GET /api/desktop/updates at boundary value | Correct boundary handling |
| TC-02132 | API | Desktop app | No auth token | GET /api/desktop/updates | 401 Unauthorized |
| TC-02133 | frontend-UAT | Desktop app | Logged in | Open check updates in UI | UI renders correctly |
| TC-02134 | frontend-UAT | Desktop app | No data | Open check updates with no data | No-data state shown |
| TC-02135 | API | Desktop app | Expired token | GET /api/desktop/updates | 401 Unauthorized |
| TC-02136 | API | Desktop app | Insufficient role | GET /api/desktop/updates | 403 Forbidden |
| TC-02137 | API | Desktop app | Logged in | GET /api/desktop/storage | 200 + valid data |
| TC-02138 | API | Desktop app | Logged in | GET /api/desktop/storage with invalid input | 400/422 + error message |
| TC-02139 | API | Desktop app | Edge case | GET /api/desktop/storage at boundary value | Correct boundary handling |
| TC-02140 | API | Desktop app | No auth token | GET /api/desktop/storage | 401 Unauthorized |
| TC-02141 | frontend-UAT | Desktop app | Logged in | Open storage usage in UI | UI renders correctly |
| TC-02142 | frontend-UAT | Desktop app | No data | Open storage usage with no data | No-data state shown |
| TC-02143 | API | Desktop app | Expired token | GET /api/desktop/storage | 401 Unauthorized |
| TC-02144 | API | Desktop app | Insufficient role | GET /api/desktop/storage | 403 Forbidden |
| TC-02145 | API | Desktop app | Logged in | GET /api/desktop/reset | 200 + valid data |
| TC-02146 | API | Desktop app | Logged in | GET /api/desktop/reset with invalid input | 400/422 + error message |
| TC-02147 | API | Desktop app | Edge case | GET /api/desktop/reset at boundary value | Correct boundary handling |
| TC-02148 | API | Desktop app | No auth token | GET /api/desktop/reset | 401 Unauthorized |
| TC-02149 | frontend-UAT | Desktop app | Logged in | Open reset defaults in UI | UI renders correctly |
| TC-02150 | frontend-UAT | Desktop app | No data | Open reset defaults with no data | No-data state shown |
| TC-02151 | API | Desktop app | Expired token | GET /api/desktop/reset | 401 Unauthorized |
| TC-02152 | API | Desktop app | Insufficient role | GET /api/desktop/reset | 403 Forbidden |
| TC-02153 | API | Desktop app | Logged in | GET /api/desktop?empty | 200 + valid data |
| TC-02154 | API | Desktop app | Logged in | GET /api/desktop?empty with invalid input | 400/422 + error message |
| TC-02155 | API | Desktop app | Edge case | GET /api/desktop?empty at boundary value | Correct boundary handling |
| TC-02156 | API | Desktop app | No auth token | GET /api/desktop?empty | 401 Unauthorized |
| TC-02157 | frontend-UAT | Desktop app | Logged in | Open no-data state in UI | UI renders correctly |
| TC-02158 | frontend-UAT | Desktop app | No data | Open no-data state with no data | No-data state shown |
| TC-02159 | API | Desktop app | Expired token | GET /api/desktop?empty | 401 Unauthorized |
| TC-02160 | API | Desktop app | Insufficient role | GET /api/desktop?empty | 403 Forbidden |
### F19 — Application submission pipeline

| TC-02161 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/generate | 200 + valid data |
| TC-02162 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/generate with invalid input | 400/422 + error message |
| TC-02163 | API | Application submission pipeline | Edge case | POST /api/jobs/{job_id}/generate at boundary value | Correct boundary handling |
| TC-02164 | API | Application submission pipeline | No auth token | POST /api/jobs/{job_id}/generate | 401 Unauthorized |
| TC-02165 | frontend-UAT | Application submission pipeline | Logged in | Open generate application package in UI | UI renders correctly |
| TC-02166 | frontend-UAT | Application submission pipeline | No data | Open generate application package with no data | No-data state shown |
| TC-02167 | API | Application submission pipeline | Expired token | POST /api/jobs/{job_id}/generate | 401 Unauthorized |
| TC-02168 | API | Application submission pipeline | Insufficient role | POST /api/jobs/{job_id}/generate | 403 Forbidden |
| TC-02169 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/approve | 200 + valid data |
| TC-02170 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/approve with invalid input | 400/422 + error message |
| TC-02171 | API | Application submission pipeline | Edge case | POST /api/jobs/{job_id}/approve at boundary value | Correct boundary handling |
| TC-02172 | API | Application submission pipeline | No auth token | POST /api/jobs/{job_id}/approve | 401 Unauthorized |
| TC-02173 | frontend-UAT | Application submission pipeline | Logged in | Open approve + start submission in UI | UI renders correctly |
| TC-02174 | frontend-UAT | Application submission pipeline | No data | Open approve + start submission with no data | No-data state shown |
| TC-02175 | API | Application submission pipeline | Expired token | POST /api/jobs/{job_id}/approve | 401 Unauthorized |
| TC-02176 | API | Application submission pipeline | Insufficient role | POST /api/jobs/{job_id}/approve | 403 Forbidden |
| TC-02177 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/submit | 200 + valid data |
| TC-02178 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/submit with invalid input | 400/422 + error message |
| TC-02179 | API | Application submission pipeline | Edge case | POST /api/jobs/{job_id}/submit at boundary value | Correct boundary handling |
| TC-02180 | API | Application submission pipeline | No auth token | POST /api/jobs/{job_id}/submit | 401 Unauthorized |
| TC-02181 | frontend-UAT | Application submission pipeline | Logged in | Open submit application in UI | UI renders correctly |
| TC-02182 | frontend-UAT | Application submission pipeline | No data | Open submit application with no data | No-data state shown |
| TC-02183 | API | Application submission pipeline | Expired token | POST /api/jobs/{job_id}/submit | 401 Unauthorized |
| TC-02184 | API | Application submission pipeline | Insufficient role | POST /api/jobs/{job_id}/submit | 403 Forbidden |
| TC-02185 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/resubmit | 200 + valid data |
| TC-02186 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/resubmit with invalid input | 400/422 + error message |
| TC-02187 | API | Application submission pipeline | Edge case | POST /api/jobs/{job_id}/resubmit at boundary value | Correct boundary handling |
| TC-02188 | API | Application submission pipeline | No auth token | POST /api/jobs/{job_id}/resubmit | 401 Unauthorized |
| TC-02189 | frontend-UAT | Application submission pipeline | Logged in | Open resubmit application in UI | UI renders correctly |
| TC-02190 | frontend-UAT | Application submission pipeline | No data | Open resubmit application with no data | No-data state shown |
| TC-02191 | API | Application submission pipeline | Expired token | POST /api/jobs/{job_id}/resubmit | 401 Unauthorized |
| TC-02192 | API | Application submission pipeline | Insufficient role | POST /api/jobs/{job_id}/resubmit | 403 Forbidden |
| TC-02193 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id} | 200 + valid data |
| TC-02194 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id} with invalid input | 400/422 + error message |
| TC-02195 | API | Application submission pipeline | Edge case | GET /api/jobs/{job_id} at boundary value | Correct boundary handling |
| TC-02196 | API | Application submission pipeline | No auth token | GET /api/jobs/{job_id} | 401 Unauthorized |
| TC-02197 | frontend-UAT | Application submission pipeline | Logged in | Open submission + application state in UI | UI renders correctly |
| TC-02198 | frontend-UAT | Application submission pipeline | No data | Open submission + application state with no data | No-data state shown |
| TC-02199 | API | Application submission pipeline | Expired token | GET /api/jobs/{job_id} | 401 Unauthorized |
| TC-02200 | API | Application submission pipeline | Insufficient role | GET /api/jobs/{job_id} | 403 Forbidden |
| TC-02201 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/timeline | 200 + valid data |
| TC-02202 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/timeline with invalid input | 400/422 + error message |
| TC-02203 | API | Application submission pipeline | Edge case | GET /api/jobs/{job_id}/timeline at boundary value | Correct boundary handling |
| TC-02204 | API | Application submission pipeline | No auth token | GET /api/jobs/{job_id}/timeline | 401 Unauthorized |
| TC-02205 | frontend-UAT | Application submission pipeline | Logged in | Open submission timeline in UI | UI renders correctly |
| TC-02206 | frontend-UAT | Application submission pipeline | No data | Open submission timeline with no data | No-data state shown |
| TC-02207 | API | Application submission pipeline | Expired token | GET /api/jobs/{job_id}/timeline | 401 Unauthorized |
| TC-02208 | API | Application submission pipeline | Insufficient role | GET /api/jobs/{job_id}/timeline | 403 Forbidden |
| TC-02209 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/application-form | 200 + valid data |
| TC-02210 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/application-form with invalid input | 400/422 + error message |
| TC-02211 | API | Application submission pipeline | Edge case | GET /api/jobs/{job_id}/application-form at boundary value | Correct boundary handling |
| TC-02212 | API | Application submission pipeline | No auth token | GET /api/jobs/{job_id}/application-form | 401 Unauthorized |
| TC-02213 | frontend-UAT | Application submission pipeline | Logged in | Open prefilled form in UI | UI renders correctly |
| TC-02214 | frontend-UAT | Application submission pipeline | No data | Open prefilled form with no data | No-data state shown |
| TC-02215 | API | Application submission pipeline | Expired token | GET /api/jobs/{job_id}/application-form | 401 Unauthorized |
| TC-02216 | API | Application submission pipeline | Insufficient role | GET /api/jobs/{job_id}/application-form | 403 Forbidden |
| TC-02217 | API | Application submission pipeline | Logged in | PUT /api/jobs/{job_id}/application-form | 200 + valid data |
| TC-02218 | API | Application submission pipeline | Logged in | PUT /api/jobs/{job_id}/application-form with invalid input | 400/422 + error message |
| TC-02219 | API | Application submission pipeline | Edge case | PUT /api/jobs/{job_id}/application-form at boundary value | Correct boundary handling |
| TC-02220 | API | Application submission pipeline | No auth token | PUT /api/jobs/{job_id}/application-form | 401 Unauthorized |
| TC-02221 | frontend-UAT | Application submission pipeline | Logged in | Open save edited form in UI | UI renders correctly |
| TC-02222 | frontend-UAT | Application submission pipeline | No data | Open save edited form with no data | No-data state shown |
| TC-02223 | API | Application submission pipeline | Expired token | PUT /api/jobs/{job_id}/application-form | 401 Unauthorized |
| TC-02224 | API | Application submission pipeline | Insufficient role | PUT /api/jobs/{job_id}/application-form | 403 Forbidden |
| TC-02225 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/resume.pdf | 200 + valid data |
| TC-02226 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/resume.pdf with invalid input | 400/422 + error message |
| TC-02227 | API | Application submission pipeline | Edge case | GET /api/jobs/{job_id}/resume.pdf at boundary value | Correct boundary handling |
| TC-02228 | API | Application submission pipeline | No auth token | GET /api/jobs/{job_id}/resume.pdf | 401 Unauthorized |
| TC-02229 | frontend-UAT | Application submission pipeline | Logged in | Open tailored resume PDF in UI | UI renders correctly |
| TC-02230 | frontend-UAT | Application submission pipeline | No data | Open tailored resume PDF with no data | No-data state shown |
| TC-02231 | API | Application submission pipeline | Expired token | GET /api/jobs/{job_id}/resume.pdf | 401 Unauthorized |
| TC-02232 | API | Application submission pipeline | Insufficient role | GET /api/jobs/{job_id}/resume.pdf | 403 Forbidden |
| TC-02233 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/application-status | 200 + valid data |
| TC-02234 | API | Application submission pipeline | Logged in | POST /api/jobs/{job_id}/application-status with invalid input | 400/422 + error message |
| TC-02235 | API | Application submission pipeline | Edge case | POST /api/jobs/{job_id}/application-status at boundary value | Correct boundary handling |
| TC-02236 | API | Application submission pipeline | No auth token | POST /api/jobs/{job_id}/application-status | 401 Unauthorized |
| TC-02237 | frontend-UAT | Application submission pipeline | Logged in | Open manual stage move in UI | UI renders correctly |
| TC-02238 | frontend-UAT | Application submission pipeline | No data | Open manual stage move with no data | No-data state shown |
| TC-02239 | API | Application submission pipeline | Expired token | POST /api/jobs/{job_id}/application-status | 401 Unauthorized |
| TC-02240 | API | Application submission pipeline | Insufficient role | POST /api/jobs/{job_id}/application-status | 403 Forbidden |
| TC-02241 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/followup | 200 + valid data |
| TC-02242 | API | Application submission pipeline | Logged in | GET /api/jobs/{job_id}/followup with invalid input | 400/422 + error message |
| TC-02243 | API | Application submission pipeline | Edge case | GET /api/jobs/{job_id}/followup at boundary value | Correct boundary handling |
| TC-02244 | API | Application submission pipeline | No auth token | GET /api/jobs/{job_id}/followup | 401 Unauthorized |
| TC-02245 | frontend-UAT | Application submission pipeline | Logged in | Open follow-up email draft in UI | UI renders correctly |
| TC-02246 | frontend-UAT | Application submission pipeline | No data | Open follow-up email draft with no data | No-data state shown |
| TC-02247 | API | Application submission pipeline | Expired token | GET /api/jobs/{job_id}/followup | 401 Unauthorized |
| TC-02248 | API | Application submission pipeline | Insufficient role | GET /api/jobs/{job_id}/followup | 403 Forbidden |
| TC-02249 | API | Application submission pipeline | Logged in | GET /api/jobs?status | 200 + valid data |
| TC-02250 | API | Application submission pipeline | Logged in | GET /api/jobs?status with invalid input | 400/422 + error message |
| TC-02251 | API | Application submission pipeline | Edge case | GET /api/jobs?status at boundary value | Correct boundary handling |
| TC-02252 | API | Application submission pipeline | No auth token | GET /api/jobs?status | 401 Unauthorized |
| TC-02253 | frontend-UAT | Application submission pipeline | Logged in | Open submission queue by status in UI | UI renders correctly |
| TC-02254 | frontend-UAT | Application submission pipeline | No data | Open submission queue by status with no data | No-data state shown |
| TC-02255 | API | Application submission pipeline | Expired token | GET /api/jobs?status | 401 Unauthorized |
| TC-02256 | API | Application submission pipeline | Insufficient role | GET /api/jobs?status | 403 Forbidden |
### F20 — Application status tracking

| TC-02257 | API | Application status tracking | Logged in | GET /api/applications/{id}/status | 200 + valid data |
| TC-02258 | API | Application status tracking | Logged in | GET /api/applications/{id}/status with invalid input | 400/422 + error message |
| TC-02259 | API | Application status tracking | Edge case | GET /api/applications/{id}/status at boundary value | Correct boundary handling |
| TC-02260 | API | Application status tracking | No auth token | GET /api/applications/{id}/status | 401 Unauthorized |
| TC-02261 | frontend-UAT | Application status tracking | Logged in | Open current status in UI | UI renders correctly |
| TC-02262 | frontend-UAT | Application status tracking | No data | Open current status with no data | No-data state shown |
| TC-02263 | API | Application status tracking | Expired token | GET /api/applications/{id}/status | 401 Unauthorized |
| TC-02264 | API | Application status tracking | Insufficient role | GET /api/applications/{id}/status | 403 Forbidden |
| TC-02265 | API | Application status tracking | Logged in | GET /api/applications/{id}/status-history | 200 + valid data |
| TC-02266 | API | Application status tracking | Logged in | GET /api/applications/{id}/status-history with invalid input | 400/422 + error message |
| TC-02267 | API | Application status tracking | Edge case | GET /api/applications/{id}/status-history at boundary value | Correct boundary handling |
| TC-02268 | API | Application status tracking | No auth token | GET /api/applications/{id}/status-history | 401 Unauthorized |
| TC-02269 | frontend-UAT | Application status tracking | Logged in | Open status history in UI | UI renders correctly |
| TC-02270 | frontend-UAT | Application status tracking | No data | Open status history with no data | No-data state shown |
| TC-02271 | API | Application status tracking | Expired token | GET /api/applications/{id}/status-history | 401 Unauthorized |
| TC-02272 | API | Application status tracking | Insufficient role | GET /api/applications/{id}/status-history | 403 Forbidden |
| TC-02273 | API | Application status tracking | Logged in | GET /api/applications?status | 200 + valid data |
| TC-02274 | API | Application status tracking | Logged in | GET /api/applications?status with invalid input | 400/422 + error message |
| TC-02275 | API | Application status tracking | Edge case | GET /api/applications?status at boundary value | Correct boundary handling |
| TC-02276 | API | Application status tracking | No auth token | GET /api/applications?status | 401 Unauthorized |
| TC-02277 | frontend-UAT | Application status tracking | Logged in | Open filter by status in UI | UI renders correctly |
| TC-02278 | frontend-UAT | Application status tracking | No data | Open filter by status with no data | No-data state shown |
| TC-02279 | API | Application status tracking | Expired token | GET /api/applications?status | 401 Unauthorized |
| TC-02280 | API | Application status tracking | Insufficient role | GET /api/applications?status | 403 Forbidden |
| TC-02281 | API | Application status tracking | Logged in | GET /api/applications/{id}/status?empty | 200 + valid data |
| TC-02282 | API | Application status tracking | Logged in | GET /api/applications/{id}/status?empty with invalid input | 400/422 + error message |
| TC-02283 | API | Application status tracking | Edge case | GET /api/applications/{id}/status?empty at boundary value | Correct boundary handling |
| TC-02284 | API | Application status tracking | No auth token | GET /api/applications/{id}/status?empty | 401 Unauthorized |
| TC-02285 | frontend-UAT | Application status tracking | Logged in | Open no-status state in UI | UI renders correctly |
| TC-02286 | frontend-UAT | Application status tracking | No data | Open no-status state with no data | No-data state shown |
| TC-02287 | API | Application status tracking | Expired token | GET /api/applications/{id}/status?empty | 401 Unauthorized |
| TC-02288 | API | Application status tracking | Insufficient role | GET /api/applications/{id}/status?empty | 403 Forbidden |
| TC-02289 | API | Application status tracking | Logged in | GET /api/applications/{id}/method | 200 + valid data |
| TC-02290 | API | Application status tracking | Logged in | GET /api/applications/{id}/method with invalid input | 400/422 + error message |
| TC-02291 | API | Application status tracking | Edge case | GET /api/applications/{id}/method at boundary value | Correct boundary handling |
| TC-02292 | API | Application status tracking | No auth token | GET /api/applications/{id}/method | 401 Unauthorized |
| TC-02293 | frontend-UAT | Application status tracking | Logged in | Open submission method in UI | UI renders correctly |
| TC-02294 | frontend-UAT | Application status tracking | No data | Open submission method with no data | No-data state shown |
| TC-02295 | API | Application status tracking | Expired token | GET /api/applications/{id}/method | 401 Unauthorized |
| TC-02296 | API | Application status tracking | Insufficient role | GET /api/applications/{id}/method | 403 Forbidden |
| TC-02297 | API | Application status tracking | Logged in | GET /api/applications/{id}/message | 200 + valid data |
| TC-02298 | API | Application status tracking | Logged in | GET /api/applications/{id}/message with invalid input | 400/422 + error message |
| TC-02299 | API | Application status tracking | Edge case | GET /api/applications/{id}/message at boundary value | Correct boundary handling |
| TC-02300 | API | Application status tracking | No auth token | GET /api/applications/{id}/message | 401 Unauthorized |
| TC-02301 | frontend-UAT | Application status tracking | Logged in | Open submission message in UI | UI renders correctly |
| TC-02302 | frontend-UAT | Application status tracking | No data | Open submission message with no data | No-data state shown |
| TC-02303 | API | Application status tracking | Expired token | GET /api/applications/{id}/message | 401 Unauthorized |
| TC-02304 | API | Application status tracking | Insufficient role | GET /api/applications/{id}/message | 403 Forbidden |
| TC-02305 | API | Application status tracking | Logged in | GET /api/applications/summary | 200 + valid data |
| TC-02306 | API | Application status tracking | Logged in | GET /api/applications/summary with invalid input | 400/422 + error message |
| TC-02307 | API | Application status tracking | Edge case | GET /api/applications/summary at boundary value | Correct boundary handling |
| TC-02308 | API | Application status tracking | No auth token | GET /api/applications/summary | 401 Unauthorized |
| TC-02309 | frontend-UAT | Application status tracking | Logged in | Open status summary in UI | UI renders correctly |
| TC-02310 | frontend-UAT | Application status tracking | No data | Open status summary with no data | No-data state shown |
| TC-02311 | API | Application status tracking | Expired token | GET /api/applications/summary | 401 Unauthorized |
| TC-02312 | API | Application status tracking | Insufficient role | GET /api/applications/summary | 403 Forbidden |
| TC-02313 | API | Application status tracking | Logged in | GET /api/applications?color | 200 + valid data |
| TC-02314 | API | Application status tracking | Logged in | GET /api/applications?color with invalid input | 400/422 + error message |
| TC-02315 | API | Application status tracking | Edge case | GET /api/applications?color at boundary value | Correct boundary handling |
| TC-02316 | API | Application status tracking | No auth token | GET /api/applications?color | 401 Unauthorized |
| TC-02317 | frontend-UAT | Application status tracking | Logged in | Open color-coded statuses in UI | UI renders correctly |
| TC-02318 | frontend-UAT | Application status tracking | No data | Open color-coded statuses with no data | No-data state shown |
| TC-02319 | API | Application status tracking | Expired token | GET /api/applications?color | 401 Unauthorized |
| TC-02320 | API | Application status tracking | Insufficient role | GET /api/applications?color | 403 Forbidden |
| TC-02321 | API | Application status tracking | Logged in | GET /api/applications/funnel | 200 + valid data |
| TC-02322 | API | Application status tracking | Logged in | GET /api/applications/funnel with invalid input | 400/422 + error message |
| TC-02323 | API | Application status tracking | Edge case | GET /api/applications/funnel at boundary value | Correct boundary handling |
| TC-02324 | API | Application status tracking | No auth token | GET /api/applications/funnel | 401 Unauthorized |
| TC-02325 | frontend-UAT | Application status tracking | Logged in | Open status funnel in UI | UI renders correctly |
| TC-02326 | frontend-UAT | Application status tracking | No data | Open status funnel with no data | No-data state shown |
| TC-02327 | API | Application status tracking | Expired token | GET /api/applications/funnel | 401 Unauthorized |
| TC-02328 | API | Application status tracking | Insufficient role | GET /api/applications/funnel | 403 Forbidden |
| TC-02329 | API | Application status tracking | Logged in | GET /api/applications?by_source | 200 + valid data |
| TC-02330 | API | Application status tracking | Logged in | GET /api/applications?by_source with invalid input | 400/422 + error message |
| TC-02331 | API | Application status tracking | Edge case | GET /api/applications?by_source at boundary value | Correct boundary handling |
| TC-02332 | API | Application status tracking | No auth token | GET /api/applications?by_source | 401 Unauthorized |
| TC-02333 | frontend-UAT | Application status tracking | Logged in | Open status by source in UI | UI renders correctly |
| TC-02334 | frontend-UAT | Application status tracking | No data | Open status by source with no data | No-data state shown |
| TC-02335 | API | Application status tracking | Expired token | GET /api/applications?by_source | 401 Unauthorized |
| TC-02336 | API | Application status tracking | Insufficient role | GET /api/applications?by_source | 403 Forbidden |
| TC-02337 | API | Application status tracking | Logged in | GET /api/applications?by_week | 200 + valid data |
| TC-02338 | API | Application status tracking | Logged in | GET /api/applications?by_week with invalid input | 400/422 + error message |
| TC-02339 | API | Application status tracking | Edge case | GET /api/applications?by_week at boundary value | Correct boundary handling |
| TC-02340 | API | Application status tracking | No auth token | GET /api/applications?by_week | 401 Unauthorized |
| TC-02341 | frontend-UAT | Application status tracking | Logged in | Open status by week in UI | UI renders correctly |
| TC-02342 | frontend-UAT | Application status tracking | No data | Open status by week with no data | No-data state shown |
| TC-02343 | API | Application status tracking | Expired token | GET /api/applications?by_week | 401 Unauthorized |
| TC-02344 | API | Application status tracking | Insufficient role | GET /api/applications?by_week | 403 Forbidden |
| TC-02345 | API | Application status tracking | Logged in | GET /api/applications?by_salary | 200 + valid data |
| TC-02346 | API | Application status tracking | Logged in | GET /api/applications?by_salary with invalid input | 400/422 + error message |
| TC-02347 | API | Application status tracking | Edge case | GET /api/applications?by_salary at boundary value | Correct boundary handling |
| TC-02348 | API | Application status tracking | No auth token | GET /api/applications?by_salary | 401 Unauthorized |
| TC-02349 | frontend-UAT | Application status tracking | Logged in | Open status by salary in UI | UI renders correctly |
| TC-02350 | frontend-UAT | Application status tracking | No data | Open status by salary with no data | No-data state shown |
| TC-02351 | API | Application status tracking | Expired token | GET /api/applications?by_salary | 401 Unauthorized |
| TC-02352 | API | Application status tracking | Insufficient role | GET /api/applications?by_salary | 403 Forbidden |
| TC-02353 | API | Application status tracking | Logged in | GET /api/applications?by_role | 200 + valid data |
| TC-02354 | API | Application status tracking | Logged in | GET /api/applications?by_role with invalid input | 400/422 + error message |
| TC-02355 | API | Application status tracking | Edge case | GET /api/applications?by_role at boundary value | Correct boundary handling |
| TC-02356 | API | Application status tracking | No auth token | GET /api/applications?by_role | 401 Unauthorized |
| TC-02357 | frontend-UAT | Application status tracking | Logged in | Open status by role in UI | UI renders correctly |
| TC-02358 | frontend-UAT | Application status tracking | No data | Open status by role with no data | No-data state shown |
| TC-02359 | API | Application status tracking | Expired token | GET /api/applications?by_role | 401 Unauthorized |
| TC-02360 | API | Application status tracking | Insufficient role | GET /api/applications?by_role | 403 Forbidden |
| TC-02361 | API | Application status tracking | Logged in | GET /api/applications?empty | 200 + valid data |
| TC-02362 | API | Application status tracking | Logged in | GET /api/applications?empty with invalid input | 400/422 + error message |
| TC-02363 | API | Application status tracking | Edge case | GET /api/applications?empty at boundary value | Correct boundary handling |
| TC-02364 | API | Application status tracking | No auth token | GET /api/applications?empty | 401 Unauthorized |
| TC-02365 | frontend-UAT | Application status tracking | Logged in | Open no-data state in UI | UI renders correctly |
| TC-02366 | frontend-UAT | Application status tracking | No data | Open no-data state with no data | No-data state shown |
| TC-02367 | API | Application status tracking | Expired token | GET /api/applications?empty | 401 Unauthorized |
| TC-02368 | API | Application status tracking | Insufficient role | GET /api/applications?empty | 403 Forbidden |
| TC-02369 | API | Application status tracking | Logged in | GET /api/applications?export | 200 + valid data |
| TC-02370 | API | Application status tracking | Logged in | GET /api/applications?export with invalid input | 400/422 + error message |
| TC-02371 | API | Application status tracking | Edge case | GET /api/applications?export at boundary value | Correct boundary handling |
| TC-02372 | API | Application status tracking | No auth token | GET /api/applications?export | 401 Unauthorized |
| TC-02373 | frontend-UAT | Application status tracking | Logged in | Open export statuses in UI | UI renders correctly |
| TC-02374 | frontend-UAT | Application status tracking | No data | Open export statuses with no data | No-data state shown |
| TC-02375 | API | Application status tracking | Expired token | GET /api/applications?export | 401 Unauthorized |
| TC-02376 | API | Application status tracking | Insufficient role | GET /api/applications?export | 403 Forbidden |
### F21 — Application form editor

| TC-02377 | API | Application form editor | Logged in | PUT /api/form/fields/{id} | 200 + valid data |
| TC-02378 | API | Application form editor | Logged in | PUT /api/form/fields/{id} with invalid input | 400/422 + error message |
| TC-02379 | API | Application form editor | Edge case | PUT /api/form/fields/{id} at boundary value | Correct boundary handling |
| TC-02380 | API | Application form editor | No auth token | PUT /api/form/fields/{id} | 401 Unauthorized |
| TC-02381 | frontend-UAT | Application form editor | Logged in | Open edit field in UI | UI renders correctly |
| TC-02382 | frontend-UAT | Application form editor | No data | Open edit field with no data | No-data state shown |
| TC-02383 | API | Application form editor | Expired token | PUT /api/form/fields/{id} | 401 Unauthorized |
| TC-02384 | API | Application form editor | Insufficient role | PUT /api/form/fields/{id} | 403 Forbidden |
| TC-02385 | API | Application form editor | Logged in | POST /api/form/fields | 200 + valid data |
| TC-02386 | API | Application form editor | Logged in | POST /api/form/fields with invalid input | 400/422 + error message |
| TC-02387 | API | Application form editor | Edge case | POST /api/form/fields at boundary value | Correct boundary handling |
| TC-02388 | API | Application form editor | No auth token | POST /api/form/fields | 401 Unauthorized |
| TC-02389 | frontend-UAT | Application form editor | Logged in | Open add field in UI | UI renders correctly |
| TC-02390 | frontend-UAT | Application form editor | No data | Open add field with no data | No-data state shown |
| TC-02391 | API | Application form editor | Expired token | POST /api/form/fields | 401 Unauthorized |
| TC-02392 | API | Application form editor | Insufficient role | POST /api/form/fields | 403 Forbidden |
| TC-02393 | API | Application form editor | Logged in | PUT /api/form/fields/{id}/hidden | 200 + valid data |
| TC-02394 | API | Application form editor | Logged in | PUT /api/form/fields/{id}/hidden with invalid input | 400/422 + error message |
| TC-02395 | API | Application form editor | Edge case | PUT /api/form/fields/{id}/hidden at boundary value | Correct boundary handling |
| TC-02396 | API | Application form editor | No auth token | PUT /api/form/fields/{id}/hidden | 401 Unauthorized |
| TC-02397 | frontend-UAT | Application form editor | Logged in | Open hide field in UI | UI renders correctly |
| TC-02398 | frontend-UAT | Application form editor | No data | Open hide field with no data | No-data state shown |
| TC-02399 | API | Application form editor | Expired token | PUT /api/form/fields/{id}/hidden | 401 Unauthorized |
| TC-02400 | API | Application form editor | Insufficient role | PUT /api/form/fields/{id}/hidden | 403 Forbidden |
| TC-02401 | API | Application form editor | Logged in | GET /api/form/preview | 200 + valid data |
| TC-02402 | API | Application form editor | Logged in | GET /api/form/preview with invalid input | 400/422 + error message |
| TC-02403 | API | Application form editor | Edge case | GET /api/form/preview at boundary value | Correct boundary handling |
| TC-02404 | API | Application form editor | No auth token | GET /api/form/preview | 401 Unauthorized |
| TC-02405 | frontend-UAT | Application form editor | Logged in | Open form preview in UI | UI renders correctly |
| TC-02406 | frontend-UAT | Application form editor | No data | Open form preview with no data | No-data state shown |
| TC-02407 | API | Application form editor | Expired token | GET /api/form/preview | 401 Unauthorized |
| TC-02408 | API | Application form editor | Insufficient role | GET /api/form/preview | 403 Forbidden |
| TC-02409 | API | Application form editor | Logged in | PUT /api/form/fields/{id}/reset | 200 + valid data |
| TC-02410 | API | Application form editor | Logged in | PUT /api/form/fields/{id}/reset with invalid input | 400/422 + error message |
| TC-02411 | API | Application form editor | Edge case | PUT /api/form/fields/{id}/reset at boundary value | Correct boundary handling |
| TC-02412 | API | Application form editor | No auth token | PUT /api/form/fields/{id}/reset | 401 Unauthorized |
| TC-02413 | frontend-UAT | Application form editor | Logged in | Open reset field in UI | UI renders correctly |
| TC-02414 | frontend-UAT | Application form editor | No data | Open reset field with no data | No-data state shown |
| TC-02415 | API | Application form editor | Expired token | PUT /api/form/fields/{id}/reset | 401 Unauthorized |
| TC-02416 | API | Application form editor | Insufficient role | PUT /api/form/fields/{id}/reset | 403 Forbidden |
| TC-02417 | API | Application form editor | Logged in | POST /api/form/fields?invalid | 200 + valid data |
| TC-02418 | API | Application form editor | Logged in | POST /api/form/fields?invalid with invalid input | 400/422 + error message |
| TC-02419 | API | Application form editor | Edge case | POST /api/form/fields?invalid at boundary value | Correct boundary handling |
| TC-02420 | API | Application form editor | No auth token | POST /api/form/fields?invalid | 401 Unauthorized |
| TC-02421 | frontend-UAT | Application form editor | Logged in | Open invalid field in UI | UI renders correctly |
| TC-02422 | frontend-UAT | Application form editor | No data | Open invalid field with no data | No-data state shown |
| TC-02423 | API | Application form editor | Expired token | POST /api/form/fields?invalid | 401 Unauthorized |
| TC-02424 | API | Application form editor | Insufficient role | POST /api/form/fields?invalid | 403 Forbidden |
| TC-02425 | API | Application form editor | Logged in | PUT /api/form/order | 200 + valid data |
| TC-02426 | API | Application form editor | Logged in | PUT /api/form/order with invalid input | 400/422 + error message |
| TC-02427 | API | Application form editor | Edge case | PUT /api/form/order at boundary value | Correct boundary handling |
| TC-02428 | API | Application form editor | No auth token | PUT /api/form/order | 401 Unauthorized |
| TC-02429 | frontend-UAT | Application form editor | Logged in | Open reorder fields in UI | UI renders correctly |
| TC-02430 | frontend-UAT | Application form editor | No data | Open reorder fields with no data | No-data state shown |
| TC-02431 | API | Application form editor | Expired token | PUT /api/form/order | 401 Unauthorized |
| TC-02432 | API | Application form editor | Insufficient role | PUT /api/form/order | 403 Forbidden |
| TC-02433 | API | Application form editor | Logged in | GET /api/form/usage | 200 + valid data |
| TC-02434 | API | Application form editor | Logged in | GET /api/form/usage with invalid input | 400/422 + error message |
| TC-02435 | API | Application form editor | Edge case | GET /api/form/usage at boundary value | Correct boundary handling |
| TC-02436 | API | Application form editor | No auth token | GET /api/form/usage | 401 Unauthorized |
| TC-02437 | frontend-UAT | Application form editor | Logged in | Open field usage in UI | UI renders correctly |
| TC-02438 | frontend-UAT | Application form editor | No data | Open field usage with no data | No-data state shown |
| TC-02439 | API | Application form editor | Expired token | GET /api/form/usage | 401 Unauthorized |
| TC-02440 | API | Application form editor | Insufficient role | GET /api/form/usage | 403 Forbidden |
| TC-02441 | API | Application form editor | Logged in | PUT /api/form/fields/{id}?invalid | 200 + valid data |
| TC-02442 | API | Application form editor | Logged in | PUT /api/form/fields/{id}?invalid with invalid input | 400/422 + error message |
| TC-02443 | API | Application form editor | Edge case | PUT /api/form/fields/{id}?invalid at boundary value | Correct boundary handling |
| TC-02444 | API | Application form editor | No auth token | PUT /api/form/fields/{id}?invalid | 401 Unauthorized |
| TC-02445 | frontend-UAT | Application form editor | Logged in | Open validation error in UI | UI renders correctly |
| TC-02446 | frontend-UAT | Application form editor | No data | Open validation error with no data | No-data state shown |
| TC-02447 | API | Application form editor | Expired token | PUT /api/form/fields/{id}?invalid | 401 Unauthorized |
| TC-02448 | API | Application form editor | Insufficient role | PUT /api/form/fields/{id}?invalid | 403 Forbidden |
| TC-02449 | API | Application form editor | Logged in | GET /api/form/fields/{id}/default | 200 + valid data |
| TC-02450 | API | Application form editor | Logged in | GET /api/form/fields/{id}/default with invalid input | 400/422 + error message |
| TC-02451 | API | Application form editor | Edge case | GET /api/form/fields/{id}/default at boundary value | Correct boundary handling |
| TC-02452 | API | Application form editor | No auth token | GET /api/form/fields/{id}/default | 401 Unauthorized |
| TC-02453 | frontend-UAT | Application form editor | Logged in | Open default value in UI | UI renders correctly |
| TC-02454 | frontend-UAT | Application form editor | No data | Open default value with no data | No-data state shown |
| TC-02455 | API | Application form editor | Expired token | GET /api/form/fields/{id}/default | 401 Unauthorized |
| TC-02456 | API | Application form editor | Insufficient role | GET /api/form/fields/{id}/default | 403 Forbidden |
| TC-02457 | API | Application form editor | Logged in | GET /api/form/fields/{id}/help | 200 + valid data |
| TC-02458 | API | Application form editor | Logged in | GET /api/form/fields/{id}/help with invalid input | 400/422 + error message |
| TC-02459 | API | Application form editor | Edge case | GET /api/form/fields/{id}/help at boundary value | Correct boundary handling |
| TC-02460 | API | Application form editor | No auth token | GET /api/form/fields/{id}/help | 401 Unauthorized |
| TC-02461 | frontend-UAT | Application form editor | Logged in | Open help text in UI | UI renders correctly |
| TC-02462 | frontend-UAT | Application form editor | No data | Open help text with no data | No-data state shown |
| TC-02463 | API | Application form editor | Expired token | GET /api/form/fields/{id}/help | 401 Unauthorized |
| TC-02464 | API | Application form editor | Insufficient role | GET /api/form/fields/{id}/help | 403 Forbidden |
| TC-02465 | API | Application form editor | Logged in | GET /api/form/fields/{id}/history | 200 + valid data |
| TC-02466 | API | Application form editor | Logged in | GET /api/form/fields/{id}/history with invalid input | 400/422 + error message |
| TC-02467 | API | Application form editor | Edge case | GET /api/form/fields/{id}/history at boundary value | Correct boundary handling |
| TC-02468 | API | Application form editor | No auth token | GET /api/form/fields/{id}/history | 401 Unauthorized |
| TC-02469 | frontend-UAT | Application form editor | Logged in | Open value history in UI | UI renders correctly |
| TC-02470 | frontend-UAT | Application form editor | No data | Open value history with no data | No-data state shown |
| TC-02471 | API | Application form editor | Expired token | GET /api/form/fields/{id}/history | 401 Unauthorized |
| TC-02472 | API | Application form editor | Insufficient role | GET /api/form/fields/{id}/history | 403 Forbidden |
| TC-02473 | API | Application form editor | Logged in | GET /api/form/fields?empty | 200 + valid data |
| TC-02474 | API | Application form editor | Logged in | GET /api/form/fields?empty with invalid input | 400/422 + error message |
| TC-02475 | API | Application form editor | Edge case | GET /api/form/fields?empty at boundary value | Correct boundary handling |
| TC-02476 | API | Application form editor | No auth token | GET /api/form/fields?empty | 401 Unauthorized |
| TC-02477 | frontend-UAT | Application form editor | Logged in | Open no-data state in UI | UI renders correctly |
| TC-02478 | frontend-UAT | Application form editor | No data | Open no-data state with no data | No-data state shown |
| TC-02479 | API | Application form editor | Expired token | GET /api/form/fields?empty | 401 Unauthorized |
| TC-02480 | API | Application form editor | Insufficient role | GET /api/form/fields?empty | 403 Forbidden |
| TC-02481 | API | Application form editor | Logged in | GET /api/form/fields?editor | 200 + valid data |
| TC-02482 | API | Application form editor | Logged in | GET /api/form/fields?editor with invalid input | 400/422 + error message |
| TC-02483 | API | Application form editor | Edge case | GET /api/form/fields?editor at boundary value | Correct boundary handling |
| TC-02484 | API | Application form editor | No auth token | GET /api/form/fields?editor | 401 Unauthorized |
| TC-02485 | frontend-UAT | Application form editor | Logged in | Open editor render in UI | UI renders correctly |
| TC-02486 | frontend-UAT | Application form editor | No data | Open editor render with no data | No-data state shown |
| TC-02487 | API | Application form editor | Expired token | GET /api/form/fields?editor | 401 Unauthorized |
| TC-02488 | API | Application form editor | Insufficient role | GET /api/form/fields?editor | 403 Forbidden |
| TC-02489 | API | Application form editor | Logged in | GET /api/form/fields?export | 200 + valid data |
| TC-02490 | API | Application form editor | Logged in | GET /api/form/fields?export with invalid input | 400/422 + error message |
| TC-02491 | API | Application form editor | Edge case | GET /api/form/fields?export at boundary value | Correct boundary handling |
| TC-02492 | API | Application form editor | No auth token | GET /api/form/fields?export | 401 Unauthorized |
| TC-02493 | frontend-UAT | Application form editor | Logged in | Open export fields in UI | UI renders correctly |
| TC-02494 | frontend-UAT | Application form editor | No data | Open export fields with no data | No-data state shown |
| TC-02495 | API | Application form editor | Expired token | GET /api/form/fields?export | 401 Unauthorized |
| TC-02496 | API | Application form editor | Insufficient role | GET /api/form/fields?export | 403 Forbidden |
### F22 — Resume PDF generation

| TC-02497 | API | Resume PDF generation | Logged in | GET /api/resume/pdf | 200 + valid data |
| TC-02498 | API | Resume PDF generation | Logged in | GET /api/resume/pdf with invalid input | 400/422 + error message |
| TC-02499 | API | Resume PDF generation | Edge case | GET /api/resume/pdf at boundary value | Correct boundary handling |
| TC-02500 | API | Resume PDF generation | No auth token | GET /api/resume/pdf | 401 Unauthorized |
| TC-02501 | frontend-UAT | Resume PDF generation | Logged in | Open generate PDF in UI | UI renders correctly |
| TC-02502 | frontend-UAT | Resume PDF generation | No data | Open generate PDF with no data | No-data state shown |
| TC-02503 | API | Resume PDF generation | Expired token | GET /api/resume/pdf | 401 Unauthorized |
| TC-02504 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf | 403 Forbidden |
| TC-02505 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/preview | 200 + valid data |
| TC-02506 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/preview with invalid input | 400/422 + error message |
| TC-02507 | API | Resume PDF generation | Edge case | GET /api/resume/pdf/preview at boundary value | Correct boundary handling |
| TC-02508 | API | Resume PDF generation | No auth token | GET /api/resume/pdf/preview | 401 Unauthorized |
| TC-02509 | frontend-UAT | Resume PDF generation | Logged in | Open preview PDF in UI | UI renders correctly |
| TC-02510 | frontend-UAT | Resume PDF generation | No data | Open preview PDF with no data | No-data state shown |
| TC-02511 | API | Resume PDF generation | Expired token | GET /api/resume/pdf/preview | 401 Unauthorized |
| TC-02512 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf/preview | 403 Forbidden |
| TC-02513 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?variant | 200 + valid data |
| TC-02514 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?variant with invalid input | 400/422 + error message |
| TC-02515 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?variant at boundary value | Correct boundary handling |
| TC-02516 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?variant | 401 Unauthorized |
| TC-02517 | frontend-UAT | Resume PDF generation | Logged in | Open variant PDF in UI | UI renders correctly |
| TC-02518 | frontend-UAT | Resume PDF generation | No data | Open variant PDF with no data | No-data state shown |
| TC-02519 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?variant | 401 Unauthorized |
| TC-02520 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?variant | 403 Forbidden |
| TC-02521 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/pages | 200 + valid data |
| TC-02522 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/pages with invalid input | 400/422 + error message |
| TC-02523 | API | Resume PDF generation | Edge case | GET /api/resume/pdf/pages at boundary value | Correct boundary handling |
| TC-02524 | API | Resume PDF generation | No auth token | GET /api/resume/pdf/pages | 401 Unauthorized |
| TC-02525 | frontend-UAT | Resume PDF generation | Logged in | Open page count in UI | UI renders correctly |
| TC-02526 | frontend-UAT | Resume PDF generation | No data | Open page count with no data | No-data state shown |
| TC-02527 | API | Resume PDF generation | Expired token | GET /api/resume/pdf/pages | 401 Unauthorized |
| TC-02528 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf/pages | 403 Forbidden |
| TC-02529 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/export | 200 + valid data |
| TC-02530 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/export with invalid input | 400/422 + error message |
| TC-02531 | API | Resume PDF generation | Edge case | GET /api/resume/pdf/export at boundary value | Correct boundary handling |
| TC-02532 | API | Resume PDF generation | No auth token | GET /api/resume/pdf/export | 401 Unauthorized |
| TC-02533 | frontend-UAT | Resume PDF generation | Logged in | Open export PDF in UI | UI renders correctly |
| TC-02534 | frontend-UAT | Resume PDF generation | No data | Open export PDF with no data | No-data state shown |
| TC-02535 | API | Resume PDF generation | Expired token | GET /api/resume/pdf/export | 401 Unauthorized |
| TC-02536 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf/export | 403 Forbidden |
| TC-02537 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/view | 200 + valid data |
| TC-02538 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/view with invalid input | 400/422 + error message |
| TC-02539 | API | Resume PDF generation | Edge case | GET /api/resume/pdf/view at boundary value | Correct boundary handling |
| TC-02540 | API | Resume PDF generation | No auth token | GET /api/resume/pdf/view | 401 Unauthorized |
| TC-02541 | frontend-UAT | Resume PDF generation | Logged in | Open viewer in UI | UI renders correctly |
| TC-02542 | frontend-UAT | Resume PDF generation | No data | Open viewer with no data | No-data state shown |
| TC-02543 | API | Resume PDF generation | Expired token | GET /api/resume/pdf/view | 401 Unauthorized |
| TC-02544 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf/view | 403 Forbidden |
| TC-02545 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?font | 200 + valid data |
| TC-02546 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?font with invalid input | 400/422 + error message |
| TC-02547 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?font at boundary value | Correct boundary handling |
| TC-02548 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?font | 401 Unauthorized |
| TC-02549 | frontend-UAT | Resume PDF generation | Logged in | Open font size in UI | UI renders correctly |
| TC-02550 | frontend-UAT | Resume PDF generation | No data | Open font size with no data | No-data state shown |
| TC-02551 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?font | 401 Unauthorized |
| TC-02552 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?font | 403 Forbidden |
| TC-02553 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/log | 200 + valid data |
| TC-02554 | API | Resume PDF generation | Logged in | GET /api/resume/pdf/log with invalid input | 400/422 + error message |
| TC-02555 | API | Resume PDF generation | Edge case | GET /api/resume/pdf/log at boundary value | Correct boundary handling |
| TC-02556 | API | Resume PDF generation | No auth token | GET /api/resume/pdf/log | 401 Unauthorized |
| TC-02557 | frontend-UAT | Resume PDF generation | Logged in | Open export log in UI | UI renders correctly |
| TC-02558 | frontend-UAT | Resume PDF generation | No data | Open export log with no data | No-data state shown |
| TC-02559 | API | Resume PDF generation | Expired token | GET /api/resume/pdf/log | 401 Unauthorized |
| TC-02560 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf/log | 403 Forbidden |
| TC-02561 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?empty | 200 + valid data |
| TC-02562 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?empty with invalid input | 400/422 + error message |
| TC-02563 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?empty at boundary value | Correct boundary handling |
| TC-02564 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?empty | 401 Unauthorized |
| TC-02565 | frontend-UAT | Resume PDF generation | Logged in | Open no-data state in UI | UI renders correctly |
| TC-02566 | frontend-UAT | Resume PDF generation | No data | Open no-data state with no data | No-data state shown |
| TC-02567 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?empty | 401 Unauthorized |
| TC-02568 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?empty | 403 Forbidden |
| TC-02569 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?download | 200 + valid data |
| TC-02570 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?download with invalid input | 400/422 + error message |
| TC-02571 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?download at boundary value | Correct boundary handling |
| TC-02572 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?download | 401 Unauthorized |
| TC-02573 | frontend-UAT | Resume PDF generation | Logged in | Open download render in UI | UI renders correctly |
| TC-02574 | frontend-UAT | Resume PDF generation | No data | Open download render with no data | No-data state shown |
| TC-02575 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?download | 401 Unauthorized |
| TC-02576 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?download | 403 Forbidden |
| TC-02577 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?preview | 200 + valid data |
| TC-02578 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?preview with invalid input | 400/422 + error message |
| TC-02579 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?preview at boundary value | Correct boundary handling |
| TC-02580 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?preview | 401 Unauthorized |
| TC-02581 | frontend-UAT | Resume PDF generation | Logged in | Open preview render in UI | UI renders correctly |
| TC-02582 | frontend-UAT | Resume PDF generation | No data | Open preview render with no data | No-data state shown |
| TC-02583 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?preview | 401 Unauthorized |
| TC-02584 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?preview | 403 Forbidden |
| TC-02585 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?variant | 200 + valid data |
| TC-02586 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?variant with invalid input | 400/422 + error message |
| TC-02587 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?variant at boundary value | Correct boundary handling |
| TC-02588 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?variant | 401 Unauthorized |
| TC-02589 | frontend-UAT | Resume PDF generation | Logged in | Open variant render in UI | UI renders correctly |
| TC-02590 | frontend-UAT | Resume PDF generation | No data | Open variant render with no data | No-data state shown |
| TC-02591 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?variant | 401 Unauthorized |
| TC-02592 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?variant | 403 Forbidden |
| TC-02593 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?mobile | 200 + valid data |
| TC-02594 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?mobile with invalid input | 400/422 + error message |
| TC-02595 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?mobile at boundary value | Correct boundary handling |
| TC-02596 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?mobile | 401 Unauthorized |
| TC-02597 | frontend-UAT | Resume PDF generation | Logged in | Open mobile view in UI | UI renders correctly |
| TC-02598 | frontend-UAT | Resume PDF generation | No data | Open mobile view with no data | No-data state shown |
| TC-02599 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?mobile | 401 Unauthorized |
| TC-02600 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?mobile | 403 Forbidden |
| TC-02601 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?print | 200 + valid data |
| TC-02602 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?print with invalid input | 400/422 + error message |
| TC-02603 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?print at boundary value | Correct boundary handling |
| TC-02604 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?print | 401 Unauthorized |
| TC-02605 | frontend-UAT | Resume PDF generation | Logged in | Open print view in UI | UI renders correctly |
| TC-02606 | frontend-UAT | Resume PDF generation | No data | Open print view with no data | No-data state shown |
| TC-02607 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?print | 401 Unauthorized |
| TC-02608 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?print | 403 Forbidden |
| TC-02609 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?hover | 200 + valid data |
| TC-02610 | API | Resume PDF generation | Logged in | GET /api/resume/pdf?hover with invalid input | 400/422 + error message |
| TC-02611 | API | Resume PDF generation | Edge case | GET /api/resume/pdf?hover at boundary value | Correct boundary handling |
| TC-02612 | API | Resume PDF generation | No auth token | GET /api/resume/pdf?hover | 401 Unauthorized |
| TC-02613 | frontend-UAT | Resume PDF generation | Logged in | Open hover tooltip in UI | UI renders correctly |
| TC-02614 | frontend-UAT | Resume PDF generation | No data | Open hover tooltip with no data | No-data state shown |
| TC-02615 | API | Resume PDF generation | Expired token | GET /api/resume/pdf?hover | 401 Unauthorized |
| TC-02616 | API | Resume PDF generation | Insufficient role | GET /api/resume/pdf?hover | 403 Forbidden |
### F23 — Company intel & facts

| TC-02617 | API | Company intel & facts | Logged in | GET /api/company/{name} | 200 + valid data |
| TC-02618 | API | Company intel & facts | Logged in | GET /api/company/{name} with invalid input | 400/422 + error message |
| TC-02619 | API | Company intel & facts | Edge case | GET /api/company/{name} at boundary value | Correct boundary handling |
| TC-02620 | API | Company intel & facts | No auth token | GET /api/company/{name} | 401 Unauthorized |
| TC-02621 | frontend-UAT | Company intel & facts | Logged in | Open company facts in UI | UI renders correctly |
| TC-02622 | frontend-UAT | Company intel & facts | No data | Open company facts with no data | No-data state shown |
| TC-02623 | API | Company intel & facts | Expired token | GET /api/company/{name} | 401 Unauthorized |
| TC-02624 | API | Company intel & facts | Insufficient role | GET /api/company/{name} | 403 Forbidden |
| TC-02625 | API | Company intel & facts | Logged in | GET /api/company/{name}?size | 200 + valid data |
| TC-02626 | API | Company intel & facts | Logged in | GET /api/company/{name}?size with invalid input | 400/422 + error message |
| TC-02627 | API | Company intel & facts | Edge case | GET /api/company/{name}?size at boundary value | Correct boundary handling |
| TC-02628 | API | Company intel & facts | No auth token | GET /api/company/{name}?size | 401 Unauthorized |
| TC-02629 | frontend-UAT | Company intel & facts | Logged in | Open company size in UI | UI renders correctly |
| TC-02630 | frontend-UAT | Company intel & facts | No data | Open company size with no data | No-data state shown |
| TC-02631 | API | Company intel & facts | Expired token | GET /api/company/{name}?size | 401 Unauthorized |
| TC-02632 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?size | 403 Forbidden |
| TC-02633 | API | Company intel & facts | Logged in | GET /api/company/{name}?industry | 200 + valid data |
| TC-02634 | API | Company intel & facts | Logged in | GET /api/company/{name}?industry with invalid input | 400/422 + error message |
| TC-02635 | API | Company intel & facts | Edge case | GET /api/company/{name}?industry at boundary value | Correct boundary handling |
| TC-02636 | API | Company intel & facts | No auth token | GET /api/company/{name}?industry | 401 Unauthorized |
| TC-02637 | frontend-UAT | Company intel & facts | Logged in | Open industry in UI | UI renders correctly |
| TC-02638 | frontend-UAT | Company intel & facts | No data | Open industry with no data | No-data state shown |
| TC-02639 | API | Company intel & facts | Expired token | GET /api/company/{name}?industry | 401 Unauthorized |
| TC-02640 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?industry | 403 Forbidden |
| TC-02641 | API | Company intel & facts | Logged in | GET /api/company/{name}?location | 200 + valid data |
| TC-02642 | API | Company intel & facts | Logged in | GET /api/company/{name}?location with invalid input | 400/422 + error message |
| TC-02643 | API | Company intel & facts | Edge case | GET /api/company/{name}?location at boundary value | Correct boundary handling |
| TC-02644 | API | Company intel & facts | No auth token | GET /api/company/{name}?location | 401 Unauthorized |
| TC-02645 | frontend-UAT | Company intel & facts | Logged in | Open location in UI | UI renders correctly |
| TC-02646 | frontend-UAT | Company intel & facts | No data | Open location with no data | No-data state shown |
| TC-02647 | API | Company intel & facts | Expired token | GET /api/company/{name}?location | 401 Unauthorized |
| TC-02648 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?location | 403 Forbidden |
| TC-02649 | API | Company intel & facts | Logged in | GET /api/company/{name}?empty | 200 + valid data |
| TC-02650 | API | Company intel & facts | Logged in | GET /api/company/{name}?empty with invalid input | 400/422 + error message |
| TC-02651 | API | Company intel & facts | Edge case | GET /api/company/{name}?empty at boundary value | Correct boundary handling |
| TC-02652 | API | Company intel & facts | No auth token | GET /api/company/{name}?empty | 401 Unauthorized |
| TC-02653 | frontend-UAT | Company intel & facts | Logged in | Open no-intel state in UI | UI renders correctly |
| TC-02654 | frontend-UAT | Company intel & facts | No data | Open no-intel state with no data | No-data state shown |
| TC-02655 | API | Company intel & facts | Expired token | GET /api/company/{name}?empty | 401 Unauthorized |
| TC-02656 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?empty | 403 Forbidden |
| TC-02657 | API | Company intel & facts | Logged in | GET /api/company/{name}?refresh | 200 + valid data |
| TC-02658 | API | Company intel & facts | Logged in | GET /api/company/{name}?refresh with invalid input | 400/422 + error message |
| TC-02659 | API | Company intel & facts | Edge case | GET /api/company/{name}?refresh at boundary value | Correct boundary handling |
| TC-02660 | API | Company intel & facts | No auth token | GET /api/company/{name}?refresh | 401 Unauthorized |
| TC-02661 | frontend-UAT | Company intel & facts | Logged in | Open refresh intel in UI | UI renders correctly |
| TC-02662 | frontend-UAT | Company intel & facts | No data | Open refresh intel with no data | No-data state shown |
| TC-02663 | API | Company intel & facts | Expired token | GET /api/company/{name}?refresh | 401 Unauthorized |
| TC-02664 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?refresh | 403 Forbidden |
| TC-02665 | API | Company intel & facts | Logged in | GET /api/company/{name}?funding | 200 + valid data |
| TC-02666 | API | Company intel & facts | Logged in | GET /api/company/{name}?funding with invalid input | 400/422 + error message |
| TC-02667 | API | Company intel & facts | Edge case | GET /api/company/{name}?funding at boundary value | Correct boundary handling |
| TC-02668 | API | Company intel & facts | No auth token | GET /api/company/{name}?funding | 401 Unauthorized |
| TC-02669 | frontend-UAT | Company intel & facts | Logged in | Open funding stage in UI | UI renders correctly |
| TC-02670 | frontend-UAT | Company intel & facts | No data | Open funding stage with no data | No-data state shown |
| TC-02671 | API | Company intel & facts | Expired token | GET /api/company/{name}?funding | 401 Unauthorized |
| TC-02672 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?funding | 403 Forbidden |
| TC-02673 | API | Company intel & facts | Logged in | GET /api/company/{name}?website | 200 + valid data |
| TC-02674 | API | Company intel & facts | Logged in | GET /api/company/{name}?website with invalid input | 400/422 + error message |
| TC-02675 | API | Company intel & facts | Edge case | GET /api/company/{name}?website at boundary value | Correct boundary handling |
| TC-02676 | API | Company intel & facts | No auth token | GET /api/company/{name}?website | 401 Unauthorized |
| TC-02677 | frontend-UAT | Company intel & facts | Logged in | Open website in UI | UI renders correctly |
| TC-02678 | frontend-UAT | Company intel & facts | No data | Open website with no data | No-data state shown |
| TC-02679 | API | Company intel & facts | Expired token | GET /api/company/{name}?website | 401 Unauthorized |
| TC-02680 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?website | 403 Forbidden |
| TC-02681 | API | Company intel & facts | Logged in | GET /api/company/{name}?revenue | 200 + valid data |
| TC-02682 | API | Company intel & facts | Logged in | GET /api/company/{name}?revenue with invalid input | 400/422 + error message |
| TC-02683 | API | Company intel & facts | Edge case | GET /api/company/{name}?revenue at boundary value | Correct boundary handling |
| TC-02684 | API | Company intel & facts | No auth token | GET /api/company/{name}?revenue | 401 Unauthorized |
| TC-02685 | frontend-UAT | Company intel & facts | Logged in | Open revenue in UI | UI renders correctly |
| TC-02686 | frontend-UAT | Company intel & facts | No data | Open revenue with no data | No-data state shown |
| TC-02687 | API | Company intel & facts | Expired token | GET /api/company/{name}?revenue | 401 Unauthorized |
| TC-02688 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?revenue | 403 Forbidden |
| TC-02689 | API | Company intel & facts | Logged in | GET /api/company/{name}?founded | 200 + valid data |
| TC-02690 | API | Company intel & facts | Logged in | GET /api/company/{name}?founded with invalid input | 400/422 + error message |
| TC-02691 | API | Company intel & facts | Edge case | GET /api/company/{name}?founded at boundary value | Correct boundary handling |
| TC-02692 | API | Company intel & facts | No auth token | GET /api/company/{name}?founded | 401 Unauthorized |
| TC-02693 | frontend-UAT | Company intel & facts | Logged in | Open founding year in UI | UI renders correctly |
| TC-02694 | frontend-UAT | Company intel & facts | No data | Open founding year with no data | No-data state shown |
| TC-02695 | API | Company intel & facts | Expired token | GET /api/company/{name}?founded | 401 Unauthorized |
| TC-02696 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?founded | 403 Forbidden |
| TC-02697 | API | Company intel & facts | Logged in | GET /api/company/{name}?tech | 200 + valid data |
| TC-02698 | API | Company intel & facts | Logged in | GET /api/company/{name}?tech with invalid input | 400/422 + error message |
| TC-02699 | API | Company intel & facts | Edge case | GET /api/company/{name}?tech at boundary value | Correct boundary handling |
| TC-02700 | API | Company intel & facts | No auth token | GET /api/company/{name}?tech | 401 Unauthorized |
| TC-02701 | frontend-UAT | Company intel & facts | Logged in | Open tech stack in UI | UI renders correctly |
| TC-02702 | frontend-UAT | Company intel & facts | No data | Open tech stack with no data | No-data state shown |
| TC-02703 | API | Company intel & facts | Expired token | GET /api/company/{name}?tech | 401 Unauthorized |
| TC-02704 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?tech | 403 Forbidden |
| TC-02705 | API | Company intel & facts | Logged in | GET /api/company/{name}?competitors | 200 + valid data |
| TC-02706 | API | Company intel & facts | Logged in | GET /api/company/{name}?competitors with invalid input | 400/422 + error message |
| TC-02707 | API | Company intel & facts | Edge case | GET /api/company/{name}?competitors at boundary value | Correct boundary handling |
| TC-02708 | API | Company intel & facts | No auth token | GET /api/company/{name}?competitors | 401 Unauthorized |
| TC-02709 | frontend-UAT | Company intel & facts | Logged in | Open competitors in UI | UI renders correctly |
| TC-02710 | frontend-UAT | Company intel & facts | No data | Open competitors with no data | No-data state shown |
| TC-02711 | API | Company intel & facts | Expired token | GET /api/company/{name}?competitors | 401 Unauthorized |
| TC-02712 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?competitors | 403 Forbidden |
| TC-02713 | API | Company intel & facts | Logged in | GET /api/company/{name}?news | 200 + valid data |
| TC-02714 | API | Company intel & facts | Logged in | GET /api/company/{name}?news with invalid input | 400/422 + error message |
| TC-02715 | API | Company intel & facts | Edge case | GET /api/company/{name}?news at boundary value | Correct boundary handling |
| TC-02716 | API | Company intel & facts | No auth token | GET /api/company/{name}?news | 401 Unauthorized |
| TC-02717 | frontend-UAT | Company intel & facts | Logged in | Open news in UI | UI renders correctly |
| TC-02718 | frontend-UAT | Company intel & facts | No data | Open news with no data | No-data state shown |
| TC-02719 | API | Company intel & facts | Expired token | GET /api/company/{name}?news | 401 Unauthorized |
| TC-02720 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?news | 403 Forbidden |
| TC-02721 | API | Company intel & facts | Logged in | GET /api/company/{name}?reviews | 200 + valid data |
| TC-02722 | API | Company intel & facts | Logged in | GET /api/company/{name}?reviews with invalid input | 400/422 + error message |
| TC-02723 | API | Company intel & facts | Edge case | GET /api/company/{name}?reviews at boundary value | Correct boundary handling |
| TC-02724 | API | Company intel & facts | No auth token | GET /api/company/{name}?reviews | 401 Unauthorized |
| TC-02725 | frontend-UAT | Company intel & facts | Logged in | Open reviews in UI | UI renders correctly |
| TC-02726 | frontend-UAT | Company intel & facts | No data | Open reviews with no data | No-data state shown |
| TC-02727 | API | Company intel & facts | Expired token | GET /api/company/{name}?reviews | 401 Unauthorized |
| TC-02728 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?reviews | 403 Forbidden |
| TC-02729 | API | Company intel & facts | Logged in | GET /api/company/{name}?panel | 200 + valid data |
| TC-02730 | API | Company intel & facts | Logged in | GET /api/company/{name}?panel with invalid input | 400/422 + error message |
| TC-02731 | API | Company intel & facts | Edge case | GET /api/company/{name}?panel at boundary value | Correct boundary handling |
| TC-02732 | API | Company intel & facts | No auth token | GET /api/company/{name}?panel | 401 Unauthorized |
| TC-02733 | frontend-UAT | Company intel & facts | Logged in | Open panel render in UI | UI renders correctly |
| TC-02734 | frontend-UAT | Company intel & facts | No data | Open panel render with no data | No-data state shown |
| TC-02735 | API | Company intel & facts | Expired token | GET /api/company/{name}?panel | 401 Unauthorized |
| TC-02736 | API | Company intel & facts | Insufficient role | GET /api/company/{name}?panel | 403 Forbidden |
### F24 — Salary negotiation assistant

| TC-02737 | API | Salary negotiation assistant | Logged in | PUT /api/negotiation?offer | 200 + valid data |
| TC-02738 | API | Salary negotiation assistant | Logged in | PUT /api/negotiation?offer with invalid input | 400/422 + error message |
| TC-02739 | API | Salary negotiation assistant | Edge case | PUT /api/negotiation?offer at boundary value | Correct boundary handling |
| TC-02740 | API | Salary negotiation assistant | No auth token | PUT /api/negotiation?offer | 401 Unauthorized |
| TC-02741 | frontend-UAT | Salary negotiation assistant | Logged in | Open get recommendation in UI | UI renders correctly |
| TC-02742 | frontend-UAT | Salary negotiation assistant | No data | Open get recommendation with no data | No-data state shown |
| TC-02743 | API | Salary negotiation assistant | Expired token | PUT /api/negotiation?offer | 401 Unauthorized |
| TC-02744 | API | Salary negotiation assistant | Insufficient role | PUT /api/negotiation?offer | 403 Forbidden |
| TC-02745 | API | Salary negotiation assistant | Logged in | GET /api/negotiation | 200 + valid data |
| TC-02746 | API | Salary negotiation assistant | Logged in | GET /api/negotiation with invalid input | 400/422 + error message |
| TC-02747 | API | Salary negotiation assistant | Edge case | GET /api/negotiation at boundary value | Correct boundary handling |
| TC-02748 | API | Salary negotiation assistant | No auth token | GET /api/negotiation | 401 Unauthorized |
| TC-02749 | frontend-UAT | Salary negotiation assistant | Logged in | Open market range in UI | UI renders correctly |
| TC-02750 | frontend-UAT | Salary negotiation assistant | No data | Open market range with no data | No-data state shown |
| TC-02751 | API | Salary negotiation assistant | Expired token | GET /api/negotiation | 401 Unauthorized |
| TC-02752 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation | 403 Forbidden |
| TC-02753 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?percentiles | 200 + valid data |
| TC-02754 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?percentiles with invalid input | 400/422 + error message |
| TC-02755 | API | Salary negotiation assistant | Edge case | GET /api/negotiation?percentiles at boundary value | Correct boundary handling |
| TC-02756 | API | Salary negotiation assistant | No auth token | GET /api/negotiation?percentiles | 401 Unauthorized |
| TC-02757 | frontend-UAT | Salary negotiation assistant | Logged in | Open percentiles in UI | UI renders correctly |
| TC-02758 | frontend-UAT | Salary negotiation assistant | No data | Open percentiles with no data | No-data state shown |
| TC-02759 | API | Salary negotiation assistant | Expired token | GET /api/negotiation?percentiles | 401 Unauthorized |
| TC-02760 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation?percentiles | 403 Forbidden |
| TC-02761 | API | Salary negotiation assistant | Logged in | PUT /api/negotiation?target | 200 + valid data |
| TC-02762 | API | Salary negotiation assistant | Logged in | PUT /api/negotiation?target with invalid input | 400/422 + error message |
| TC-02763 | API | Salary negotiation assistant | Edge case | PUT /api/negotiation?target at boundary value | Correct boundary handling |
| TC-02764 | API | Salary negotiation assistant | No auth token | PUT /api/negotiation?target | 401 Unauthorized |
| TC-02765 | frontend-UAT | Salary negotiation assistant | Logged in | Open tailored advice in UI | UI renders correctly |
| TC-02766 | frontend-UAT | Salary negotiation assistant | No data | Open tailored advice with no data | No-data state shown |
| TC-02767 | API | Salary negotiation assistant | Expired token | PUT /api/negotiation?target | 401 Unauthorized |
| TC-02768 | API | Salary negotiation assistant | Insufficient role | PUT /api/negotiation?target | 403 Forbidden |
| TC-02769 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/script | 200 + valid data |
| TC-02770 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/script with invalid input | 400/422 + error message |
| TC-02771 | API | Salary negotiation assistant | Edge case | GET /api/negotiation/script at boundary value | Correct boundary handling |
| TC-02772 | API | Salary negotiation assistant | No auth token | GET /api/negotiation/script | 401 Unauthorized |
| TC-02773 | frontend-UAT | Salary negotiation assistant | Logged in | Open negotiation script in UI | UI renders correctly |
| TC-02774 | frontend-UAT | Salary negotiation assistant | No data | Open negotiation script with no data | No-data state shown |
| TC-02775 | API | Salary negotiation assistant | Expired token | GET /api/negotiation/script | 401 Unauthorized |
| TC-02776 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation/script | 403 Forbidden |
| TC-02777 | API | Salary negotiation assistant | Logged in | PUT /api/negotiation/reset | 200 + valid data |
| TC-02778 | API | Salary negotiation assistant | Logged in | PUT /api/negotiation/reset with invalid input | 400/422 + error message |
| TC-02779 | API | Salary negotiation assistant | Edge case | PUT /api/negotiation/reset at boundary value | Correct boundary handling |
| TC-02780 | API | Salary negotiation assistant | No auth token | PUT /api/negotiation/reset | 401 Unauthorized |
| TC-02781 | frontend-UAT | Salary negotiation assistant | Logged in | Open reset inputs in UI | UI renders correctly |
| TC-02782 | frontend-UAT | Salary negotiation assistant | No data | Open reset inputs with no data | No-data state shown |
| TC-02783 | API | Salary negotiation assistant | Expired token | PUT /api/negotiation/reset | 401 Unauthorized |
| TC-02784 | API | Salary negotiation assistant | Insufficient role | PUT /api/negotiation/reset | 403 Forbidden |
| TC-02785 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/risk | 200 + valid data |
| TC-02786 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/risk with invalid input | 400/422 + error message |
| TC-02787 | API | Salary negotiation assistant | Edge case | GET /api/negotiation/risk at boundary value | Correct boundary handling |
| TC-02788 | API | Salary negotiation assistant | No auth token | GET /api/negotiation/risk | 401 Unauthorized |
| TC-02789 | frontend-UAT | Salary negotiation assistant | Logged in | Open downside risk in UI | UI renders correctly |
| TC-02790 | frontend-UAT | Salary negotiation assistant | No data | Open downside risk with no data | No-data state shown |
| TC-02791 | API | Salary negotiation assistant | Expired token | GET /api/negotiation/risk | 401 Unauthorized |
| TC-02792 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation/risk | 403 Forbidden |
| TC-02793 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/upside | 200 + valid data |
| TC-02794 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/upside with invalid input | 400/422 + error message |
| TC-02795 | API | Salary negotiation assistant | Edge case | GET /api/negotiation/upside at boundary value | Correct boundary handling |
| TC-02796 | API | Salary negotiation assistant | No auth token | GET /api/negotiation/upside | 401 Unauthorized |
| TC-02797 | frontend-UAT | Salary negotiation assistant | Logged in | Open upside in UI | UI renders correctly |
| TC-02798 | frontend-UAT | Salary negotiation assistant | No data | Open upside with no data | No-data state shown |
| TC-02799 | API | Salary negotiation assistant | Expired token | GET /api/negotiation/upside | 401 Unauthorized |
| TC-02800 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation/upside | 403 Forbidden |
| TC-02801 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/range | 200 + valid data |
| TC-02802 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/range with invalid input | 400/422 + error message |
| TC-02803 | API | Salary negotiation assistant | Edge case | GET /api/negotiation/range at boundary value | Correct boundary handling |
| TC-02804 | API | Salary negotiation assistant | No auth token | GET /api/negotiation/range | 401 Unauthorized |
| TC-02805 | frontend-UAT | Salary negotiation assistant | Logged in | Open negotiation range in UI | UI renders correctly |
| TC-02806 | frontend-UAT | Salary negotiation assistant | No data | Open negotiation range with no data | No-data state shown |
| TC-02807 | API | Salary negotiation assistant | Expired token | GET /api/negotiation/range | 401 Unauthorized |
| TC-02808 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation/range | 403 Forbidden |
| TC-02809 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/email-template | 200 + valid data |
| TC-02810 | API | Salary negotiation assistant | Logged in | GET /api/negotiation/email-template with invalid input | 400/422 + error message |
| TC-02811 | API | Salary negotiation assistant | Edge case | GET /api/negotiation/email-template at boundary value | Correct boundary handling |
| TC-02812 | API | Salary negotiation assistant | No auth token | GET /api/negotiation/email-template | 401 Unauthorized |
| TC-02813 | frontend-UAT | Salary negotiation assistant | Logged in | Open email template in UI | UI renders correctly |
| TC-02814 | frontend-UAT | Salary negotiation assistant | No data | Open email template with no data | No-data state shown |
| TC-02815 | API | Salary negotiation assistant | Expired token | GET /api/negotiation/email-template | 401 Unauthorized |
| TC-02816 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation/email-template | 403 Forbidden |
| TC-02817 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?type | 200 + valid data |
| TC-02818 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?type with invalid input | 400/422 + error message |
| TC-02819 | API | Salary negotiation assistant | Edge case | GET /api/negotiation?type at boundary value | Correct boundary handling |
| TC-02820 | API | Salary negotiation assistant | No auth token | GET /api/negotiation?type | 401 Unauthorized |
| TC-02821 | frontend-UAT | Salary negotiation assistant | Logged in | Open offer type in UI | UI renders correctly |
| TC-02822 | frontend-UAT | Salary negotiation assistant | No data | Open offer type with no data | No-data state shown |
| TC-02823 | API | Salary negotiation assistant | Expired token | GET /api/negotiation?type | 401 Unauthorized |
| TC-02824 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation?type | 403 Forbidden |
| TC-02825 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?role | 200 + valid data |
| TC-02826 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?role with invalid input | 400/422 + error message |
| TC-02827 | API | Salary negotiation assistant | Edge case | GET /api/negotiation?role at boundary value | Correct boundary handling |
| TC-02828 | API | Salary negotiation assistant | No auth token | GET /api/negotiation?role | 401 Unauthorized |
| TC-02829 | frontend-UAT | Salary negotiation assistant | Logged in | Open role-specific in UI | UI renders correctly |
| TC-02830 | frontend-UAT | Salary negotiation assistant | No data | Open role-specific with no data | No-data state shown |
| TC-02831 | API | Salary negotiation assistant | Expired token | GET /api/negotiation?role | 401 Unauthorized |
| TC-02832 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation?role | 403 Forbidden |
| TC-02833 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?experience | 200 + valid data |
| TC-02834 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?experience with invalid input | 400/422 + error message |
| TC-02835 | API | Salary negotiation assistant | Edge case | GET /api/negotiation?experience at boundary value | Correct boundary handling |
| TC-02836 | API | Salary negotiation assistant | No auth token | GET /api/negotiation?experience | 401 Unauthorized |
| TC-02837 | frontend-UAT | Salary negotiation assistant | Logged in | Open experience-specific in UI | UI renders correctly |
| TC-02838 | frontend-UAT | Salary negotiation assistant | No data | Open experience-specific with no data | No-data state shown |
| TC-02839 | API | Salary negotiation assistant | Expired token | GET /api/negotiation?experience | 401 Unauthorized |
| TC-02840 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation?experience | 403 Forbidden |
| TC-02841 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?location | 200 + valid data |
| TC-02842 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?location with invalid input | 400/422 + error message |
| TC-02843 | API | Salary negotiation assistant | Edge case | GET /api/negotiation?location at boundary value | Correct boundary handling |
| TC-02844 | API | Salary negotiation assistant | No auth token | GET /api/negotiation?location | 401 Unauthorized |
| TC-02845 | frontend-UAT | Salary negotiation assistant | Logged in | Open location-specific in UI | UI renders correctly |
| TC-02846 | frontend-UAT | Salary negotiation assistant | No data | Open location-specific with no data | No-data state shown |
| TC-02847 | API | Salary negotiation assistant | Expired token | GET /api/negotiation?location | 401 Unauthorized |
| TC-02848 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation?location | 403 Forbidden |
| TC-02849 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?empty | 200 + valid data |
| TC-02850 | API | Salary negotiation assistant | Logged in | GET /api/negotiation?empty with invalid input | 400/422 + error message |
| TC-02851 | API | Salary negotiation assistant | Edge case | GET /api/negotiation?empty at boundary value | Correct boundary handling |
| TC-02852 | API | Salary negotiation assistant | No auth token | GET /api/negotiation?empty | 401 Unauthorized |
| TC-02853 | frontend-UAT | Salary negotiation assistant | Logged in | Open no-data state in UI | UI renders correctly |
| TC-02854 | frontend-UAT | Salary negotiation assistant | No data | Open no-data state with no data | No-data state shown |
| TC-02855 | API | Salary negotiation assistant | Expired token | GET /api/negotiation?empty | 401 Unauthorized |
| TC-02856 | API | Salary negotiation assistant | Insufficient role | GET /api/negotiation?empty | 403 Forbidden |
### F25 — Rescoring

| TC-02857 | API | Rescoring | Logged in | POST /api/rescore/all | 200 + valid data |
| TC-02858 | API | Rescoring | Logged in | POST /api/rescore/all with invalid input | 400/422 + error message |
| TC-02859 | API | Rescoring | Edge case | POST /api/rescore/all at boundary value | Correct boundary handling |
| TC-02860 | API | Rescoring | No auth token | POST /api/rescore/all | 401 Unauthorized |
| TC-02861 | frontend-UAT | Rescoring | Logged in | Open rescore all in UI | UI renders correctly |
| TC-02862 | frontend-UAT | Rescoring | No data | Open rescore all with no data | No-data state shown |
| TC-02863 | API | Rescoring | Expired token | POST /api/rescore/all | 401 Unauthorized |
| TC-02864 | API | Rescoring | Insufficient role | POST /api/rescore/all | 403 Forbidden |
| TC-02865 | API | Rescoring | Logged in | GET /api/rescore/changed | 200 + valid data |
| TC-02866 | API | Rescoring | Logged in | GET /api/rescore/changed with invalid input | 400/422 + error message |
| TC-02867 | API | Rescoring | Edge case | GET /api/rescore/changed at boundary value | Correct boundary handling |
| TC-02868 | API | Rescoring | No auth token | GET /api/rescore/changed | 401 Unauthorized |
| TC-02869 | frontend-UAT | Rescoring | Logged in | Open changed jobs in UI | UI renders correctly |
| TC-02870 | frontend-UAT | Rescoring | No data | Open changed jobs with no data | No-data state shown |
| TC-02871 | API | Rescoring | Expired token | GET /api/rescore/changed | 401 Unauthorized |
| TC-02872 | API | Rescoring | Insufficient role | GET /api/rescore/changed | 403 Forbidden |
| TC-02873 | API | Rescoring | Logged in | POST /api/rescore/{job_id} | 200 + valid data |
| TC-02874 | API | Rescoring | Logged in | POST /api/rescore/{job_id} with invalid input | 400/422 + error message |
| TC-02875 | API | Rescoring | Edge case | POST /api/rescore/{job_id} at boundary value | Correct boundary handling |
| TC-02876 | API | Rescoring | No auth token | POST /api/rescore/{job_id} | 401 Unauthorized |
| TC-02877 | frontend-UAT | Rescoring | Logged in | Open rescore single in UI | UI renders correctly |
| TC-02878 | frontend-UAT | Rescoring | No data | Open rescore single with no data | No-data state shown |
| TC-02879 | API | Rescoring | Expired token | POST /api/rescore/{job_id} | 401 Unauthorized |
| TC-02880 | API | Rescoring | Insufficient role | POST /api/rescore/{job_id} | 403 Forbidden |
| TC-02881 | API | Rescoring | Logged in | GET /api/rescore/timestamp | 200 + valid data |
| TC-02882 | API | Rescoring | Logged in | GET /api/rescore/timestamp with invalid input | 400/422 + error message |
| TC-02883 | API | Rescoring | Edge case | GET /api/rescore/timestamp at boundary value | Correct boundary handling |
| TC-02884 | API | Rescoring | No auth token | GET /api/rescore/timestamp | 401 Unauthorized |
| TC-02885 | frontend-UAT | Rescoring | Logged in | Open timestamp in UI | UI renders correctly |
| TC-02886 | frontend-UAT | Rescoring | No data | Open timestamp with no data | No-data state shown |
| TC-02887 | API | Rescoring | Expired token | GET /api/rescore/timestamp | 401 Unauthorized |
| TC-02888 | API | Rescoring | Insufficient role | GET /api/rescore/timestamp | 403 Forbidden |
| TC-02889 | API | Rescoring | Logged in | GET /api/rescore/summary | 200 + valid data |
| TC-02890 | API | Rescoring | Logged in | GET /api/rescore/summary with invalid input | 400/422 + error message |
| TC-02891 | API | Rescoring | Edge case | GET /api/rescore/summary at boundary value | Correct boundary handling |
| TC-02892 | API | Rescoring | No auth token | GET /api/rescore/summary | 401 Unauthorized |
| TC-02893 | frontend-UAT | Rescoring | Logged in | Open summary in UI | UI renders correctly |
| TC-02894 | frontend-UAT | Rescoring | No data | Open summary with no data | No-data state shown |
| TC-02895 | API | Rescoring | Expired token | GET /api/rescore/summary | 401 Unauthorized |
| TC-02896 | API | Rescoring | Insufficient role | GET /api/rescore/summary | 403 Forbidden |
| TC-02897 | API | Rescoring | Logged in | POST /api/rescore?after_feedback | 200 + valid data |
| TC-02898 | API | Rescoring | Logged in | POST /api/rescore?after_feedback with invalid input | 400/422 + error message |
| TC-02899 | API | Rescoring | Edge case | POST /api/rescore?after_feedback at boundary value | Correct boundary handling |
| TC-02900 | API | Rescoring | No auth token | POST /api/rescore?after_feedback | 401 Unauthorized |
| TC-02901 | frontend-UAT | Rescoring | Logged in | Open rescore with feedback in UI | UI renders correctly |
| TC-02902 | frontend-UAT | Rescoring | No data | Open rescore with feedback with no data | No-data state shown |
| TC-02903 | API | Rescoring | Expired token | POST /api/rescore?after_feedback | 401 Unauthorized |
| TC-02904 | API | Rescoring | Insufficient role | POST /api/rescore?after_feedback | 403 Forbidden |
| TC-02905 | API | Rescoring | Logged in | GET /api/rescore?by_job | 200 + valid data |
| TC-02906 | API | Rescoring | Logged in | GET /api/rescore?by_job with invalid input | 400/422 + error message |
| TC-02907 | API | Rescoring | Edge case | GET /api/rescore?by_job at boundary value | Correct boundary handling |
| TC-02908 | API | Rescoring | No auth token | GET /api/rescore?by_job | 401 Unauthorized |
| TC-02909 | frontend-UAT | Rescoring | Logged in | Open rescore by job in UI | UI renders correctly |
| TC-02910 | frontend-UAT | Rescoring | No data | Open rescore by job with no data | No-data state shown |
| TC-02911 | API | Rescoring | Expired token | GET /api/rescore?by_job | 401 Unauthorized |
| TC-02912 | API | Rescoring | Insufficient role | GET /api/rescore?by_job | 403 Forbidden |
| TC-02913 | API | Rescoring | Logged in | GET /api/rescore?by_change | 200 + valid data |
| TC-02914 | API | Rescoring | Logged in | GET /api/rescore?by_change with invalid input | 400/422 + error message |
| TC-02915 | API | Rescoring | Edge case | GET /api/rescore?by_change at boundary value | Correct boundary handling |
| TC-02916 | API | Rescoring | No auth token | GET /api/rescore?by_change | 401 Unauthorized |
| TC-02917 | frontend-UAT | Rescoring | Logged in | Open rescore by change in UI | UI renders correctly |
| TC-02918 | frontend-UAT | Rescoring | No data | Open rescore by change with no data | No-data state shown |
| TC-02919 | API | Rescoring | Expired token | GET /api/rescore?by_change | 401 Unauthorized |
| TC-02920 | API | Rescoring | Insufficient role | GET /api/rescore?by_change | 403 Forbidden |
| TC-02921 | API | Rescoring | Logged in | GET /api/rescore?by_source | 200 + valid data |
| TC-02922 | API | Rescoring | Logged in | GET /api/rescore?by_source with invalid input | 400/422 + error message |
| TC-02923 | API | Rescoring | Edge case | GET /api/rescore?by_source at boundary value | Correct boundary handling |
| TC-02924 | API | Rescoring | No auth token | GET /api/rescore?by_source | 401 Unauthorized |
| TC-02925 | frontend-UAT | Rescoring | Logged in | Open rescore by source in UI | UI renders correctly |
| TC-02926 | frontend-UAT | Rescoring | No data | Open rescore by source with no data | No-data state shown |
| TC-02927 | API | Rescoring | Expired token | GET /api/rescore?by_source | 401 Unauthorized |
| TC-02928 | API | Rescoring | Insufficient role | GET /api/rescore?by_source | 403 Forbidden |
| TC-02929 | API | Rescoring | Logged in | GET /api/rescore?by_role | 200 + valid data |
| TC-02930 | API | Rescoring | Logged in | GET /api/rescore?by_role with invalid input | 400/422 + error message |
| TC-02931 | API | Rescoring | Edge case | GET /api/rescore?by_role at boundary value | Correct boundary handling |
| TC-02932 | API | Rescoring | No auth token | GET /api/rescore?by_role | 401 Unauthorized |
| TC-02933 | frontend-UAT | Rescoring | Logged in | Open rescore by role in UI | UI renders correctly |
| TC-02934 | frontend-UAT | Rescoring | No data | Open rescore by role with no data | No-data state shown |
| TC-02935 | API | Rescoring | Expired token | GET /api/rescore?by_role | 401 Unauthorized |
| TC-02936 | API | Rescoring | Insufficient role | GET /api/rescore?by_role | 403 Forbidden |
| TC-02937 | API | Rescoring | Logged in | GET /api/rescore?by_salary | 200 + valid data |
| TC-02938 | API | Rescoring | Logged in | GET /api/rescore?by_salary with invalid input | 400/422 + error message |
| TC-02939 | API | Rescoring | Edge case | GET /api/rescore?by_salary at boundary value | Correct boundary handling |
| TC-02940 | API | Rescoring | No auth token | GET /api/rescore?by_salary | 401 Unauthorized |
| TC-02941 | frontend-UAT | Rescoring | Logged in | Open rescore by salary in UI | UI renders correctly |
| TC-02942 | frontend-UAT | Rescoring | No data | Open rescore by salary with no data | No-data state shown |
| TC-02943 | API | Rescoring | Expired token | GET /api/rescore?by_salary | 401 Unauthorized |
| TC-02944 | API | Rescoring | Insufficient role | GET /api/rescore?by_salary | 403 Forbidden |
| TC-02945 | API | Rescoring | Logged in | GET /api/rescore?by_week | 200 + valid data |
| TC-02946 | API | Rescoring | Logged in | GET /api/rescore?by_week with invalid input | 400/422 + error message |
| TC-02947 | API | Rescoring | Edge case | GET /api/rescore?by_week at boundary value | Correct boundary handling |
| TC-02948 | API | Rescoring | No auth token | GET /api/rescore?by_week | 401 Unauthorized |
| TC-02949 | frontend-UAT | Rescoring | Logged in | Open rescore by week in UI | UI renders correctly |
| TC-02950 | frontend-UAT | Rescoring | No data | Open rescore by week with no data | No-data state shown |
| TC-02951 | API | Rescoring | Expired token | GET /api/rescore?by_week | 401 Unauthorized |
| TC-02952 | API | Rescoring | Insufficient role | GET /api/rescore?by_week | 403 Forbidden |
| TC-02953 | API | Rescoring | Logged in | GET /api/rescore?empty | 200 + valid data |
| TC-02954 | API | Rescoring | Logged in | GET /api/rescore?empty with invalid input | 400/422 + error message |
| TC-02955 | API | Rescoring | Edge case | GET /api/rescore?empty at boundary value | Correct boundary handling |
| TC-02956 | API | Rescoring | No auth token | GET /api/rescore?empty | 401 Unauthorized |
| TC-02957 | frontend-UAT | Rescoring | Logged in | Open no-data state in UI | UI renders correctly |
| TC-02958 | frontend-UAT | Rescoring | No data | Open no-data state with no data | No-data state shown |
| TC-02959 | API | Rescoring | Expired token | GET /api/rescore?empty | 401 Unauthorized |
| TC-02960 | API | Rescoring | Insufficient role | GET /api/rescore?empty | 403 Forbidden |
| TC-02961 | API | Rescoring | Logged in | GET /api/rescore?export | 200 + valid data |
| TC-02962 | API | Rescoring | Logged in | GET /api/rescore?export with invalid input | 400/422 + error message |
| TC-02963 | API | Rescoring | Edge case | GET /api/rescore?export at boundary value | Correct boundary handling |
| TC-02964 | API | Rescoring | No auth token | GET /api/rescore?export | 401 Unauthorized |
| TC-02965 | frontend-UAT | Rescoring | Logged in | Open export rescore in UI | UI renders correctly |
| TC-02966 | frontend-UAT | Rescoring | No data | Open export rescore with no data | No-data state shown |
| TC-02967 | API | Rescoring | Expired token | GET /api/rescore?export | 401 Unauthorized |
| TC-02968 | API | Rescoring | Insufficient role | GET /api/rescore?export | 403 Forbidden |
| TC-02969 | API | Rescoring | Logged in | GET /api/rescore?mobile | 200 + valid data |
| TC-02970 | API | Rescoring | Logged in | GET /api/rescore?mobile with invalid input | 400/422 + error message |
| TC-02971 | API | Rescoring | Edge case | GET /api/rescore?mobile at boundary value | Correct boundary handling |
| TC-02972 | API | Rescoring | No auth token | GET /api/rescore?mobile | 401 Unauthorized |
| TC-02973 | frontend-UAT | Rescoring | Logged in | Open mobile view in UI | UI renders correctly |
| TC-02974 | frontend-UAT | Rescoring | No data | Open mobile view with no data | No-data state shown |
| TC-02975 | API | Rescoring | Expired token | GET /api/rescore?mobile | 401 Unauthorized |
| TC-02976 | API | Rescoring | Insufficient role | GET /api/rescore?mobile | 403 Forbidden |
### F26 — Learning insights

| TC-02977 | API | Learning insights | Logged in | GET /api/learning/matched | 200 + valid data |
| TC-02978 | API | Learning insights | Logged in | GET /api/learning/matched with invalid input | 400/422 + error message |
| TC-02979 | API | Learning insights | Edge case | GET /api/learning/matched at boundary value | Correct boundary handling |
| TC-02980 | API | Learning insights | No auth token | GET /api/learning/matched | 401 Unauthorized |
| TC-02981 | frontend-UAT | Learning insights | Logged in | Open matched jobs in UI | UI renders correctly |
| TC-02982 | frontend-UAT | Learning insights | No data | Open matched jobs with no data | No-data state shown |
| TC-02983 | API | Learning insights | Expired token | GET /api/learning/matched | 401 Unauthorized |
| TC-02984 | API | Learning insights | Insufficient role | GET /api/learning/matched | 403 Forbidden |
| TC-02985 | API | Learning insights | Logged in | GET /api/learning/top-skills | 200 + valid data |
| TC-02986 | API | Learning insights | Logged in | GET /api/learning/top-skills with invalid input | 400/422 + error message |
| TC-02987 | API | Learning insights | Edge case | GET /api/learning/top-skills at boundary value | Correct boundary handling |
| TC-02988 | API | Learning insights | No auth token | GET /api/learning/top-skills | 401 Unauthorized |
| TC-02989 | frontend-UAT | Learning insights | Logged in | Open top skills in UI | UI renders correctly |
| TC-02990 | frontend-UAT | Learning insights | No data | Open top skills with no data | No-data state shown |
| TC-02991 | API | Learning insights | Expired token | GET /api/learning/top-skills | 401 Unauthorized |
| TC-02992 | API | Learning insights | Insufficient role | GET /api/learning/top-skills | 403 Forbidden |
| TC-02993 | API | Learning insights | Logged in | GET /api/learning/patterns | 200 + valid data |
| TC-02994 | API | Learning insights | Logged in | GET /api/learning/patterns with invalid input | 400/422 + error message |
| TC-02995 | API | Learning insights | Edge case | GET /api/learning/patterns at boundary value | Correct boundary handling |
| TC-02996 | API | Learning insights | No auth token | GET /api/learning/patterns | 401 Unauthorized |
| TC-02997 | frontend-UAT | Learning insights | Logged in | Open rejected patterns in UI | UI renders correctly |
| TC-02998 | frontend-UAT | Learning insights | No data | Open rejected patterns with no data | No-data state shown |
| TC-02999 | API | Learning insights | Expired token | GET /api/learning/patterns | 401 Unauthorized |
| TC-03000 | API | Learning insights | Insufficient role | GET /api/learning/patterns | 403 Forbidden |
| TC-03001 | API | Learning insights | Logged in | GET /api/learning/tip | 200 + valid data |
| TC-03002 | API | Learning insights | Logged in | GET /api/learning/tip with invalid input | 400/422 + error message |
| TC-03003 | API | Learning insights | Edge case | GET /api/learning/tip at boundary value | Correct boundary handling |
| TC-03004 | API | Learning insights | No auth token | GET /api/learning/tip | 401 Unauthorized |
| TC-03005 | frontend-UAT | Learning insights | Logged in | Open learning tip in UI | UI renders correctly |
| TC-03006 | frontend-UAT | Learning insights | No data | Open learning tip with no data | No-data state shown |
| TC-03007 | API | Learning insights | Expired token | GET /api/learning/tip | 401 Unauthorized |
| TC-03008 | API | Learning insights | Insufficient role | GET /api/learning/tip | 403 Forbidden |
| TC-03009 | API | Learning insights | Logged in | GET /api/learning/effect | 200 + valid data |
| TC-03010 | API | Learning insights | Logged in | GET /api/learning/effect with invalid input | 400/422 + error message |
| TC-03011 | API | Learning insights | Edge case | GET /api/learning/effect at boundary value | Correct boundary handling |
| TC-03012 | API | Learning insights | No auth token | GET /api/learning/effect | 401 Unauthorized |
| TC-03013 | frontend-UAT | Learning insights | Logged in | Open feedback effect in UI | UI renders correctly |
| TC-03014 | frontend-UAT | Learning insights | No data | Open feedback effect with no data | No-data state shown |
| TC-03015 | API | Learning insights | Expired token | GET /api/learning/effect | 401 Unauthorized |
| TC-03016 | API | Learning insights | Insufficient role | GET /api/learning/effect | 403 Forbidden |
| TC-03017 | API | Learning insights | Logged in | GET /api/learning/next-skill | 200 + valid data |
| TC-03018 | API | Learning insights | Logged in | GET /api/learning/next-skill with invalid input | 400/422 + error message |
| TC-03019 | API | Learning insights | Edge case | GET /api/learning/next-skill at boundary value | Correct boundary handling |
| TC-03020 | API | Learning insights | No auth token | GET /api/learning/next-skill | 401 Unauthorized |
| TC-03021 | frontend-UAT | Learning insights | Logged in | Open next skill in UI | UI renders correctly |
| TC-03022 | frontend-UAT | Learning insights | No data | Open next skill with no data | No-data state shown |
| TC-03023 | API | Learning insights | Expired token | GET /api/learning/next-skill | 401 Unauthorized |
| TC-03024 | API | Learning insights | Insufficient role | GET /api/learning/next-skill | 403 Forbidden |
| TC-03025 | API | Learning insights | Logged in | GET /api/learning/tip?skill | 200 + valid data |
| TC-03026 | API | Learning insights | Logged in | GET /api/learning/tip?skill with invalid input | 400/422 + error message |
| TC-03027 | API | Learning insights | Edge case | GET /api/learning/tip?skill at boundary value | Correct boundary handling |
| TC-03028 | API | Learning insights | No auth token | GET /api/learning/tip?skill | 401 Unauthorized |
| TC-03029 | frontend-UAT | Learning insights | Logged in | Open skill-specific tip in UI | UI renders correctly |
| TC-03030 | frontend-UAT | Learning insights | No data | Open skill-specific tip with no data | No-data state shown |
| TC-03031 | API | Learning insights | Expired token | GET /api/learning/tip?skill | 401 Unauthorized |
| TC-03032 | API | Learning insights | Insufficient role | GET /api/learning/tip?skill | 403 Forbidden |
| TC-03033 | API | Learning insights | Logged in | GET /api/learning/tip?job | 200 + valid data |
| TC-03034 | API | Learning insights | Logged in | GET /api/learning/tip?job with invalid input | 400/422 + error message |
| TC-03035 | API | Learning insights | Edge case | GET /api/learning/tip?job at boundary value | Correct boundary handling |
| TC-03036 | API | Learning insights | No auth token | GET /api/learning/tip?job | 401 Unauthorized |
| TC-03037 | frontend-UAT | Learning insights | Logged in | Open job-specific tip in UI | UI renders correctly |
| TC-03038 | frontend-UAT | Learning insights | No data | Open job-specific tip with no data | No-data state shown |
| TC-03039 | API | Learning insights | Expired token | GET /api/learning/tip?job | 401 Unauthorized |
| TC-03040 | API | Learning insights | Insufficient role | GET /api/learning/tip?job | 403 Forbidden |
| TC-03041 | API | Learning insights | Logged in | GET /api/learning/tip?source | 200 + valid data |
| TC-03042 | API | Learning insights | Logged in | GET /api/learning/tip?source with invalid input | 400/422 + error message |
| TC-03043 | API | Learning insights | Edge case | GET /api/learning/tip?source at boundary value | Correct boundary handling |
| TC-03044 | API | Learning insights | No auth token | GET /api/learning/tip?source | 401 Unauthorized |
| TC-03045 | frontend-UAT | Learning insights | Logged in | Open source-specific tip in UI | UI renders correctly |
| TC-03046 | frontend-UAT | Learning insights | No data | Open source-specific tip with no data | No-data state shown |
| TC-03047 | API | Learning insights | Expired token | GET /api/learning/tip?source | 401 Unauthorized |
| TC-03048 | API | Learning insights | Insufficient role | GET /api/learning/tip?source | 403 Forbidden |
| TC-03049 | API | Learning insights | Logged in | GET /api/learning/tip?week | 200 + valid data |
| TC-03050 | API | Learning insights | Logged in | GET /api/learning/tip?week with invalid input | 400/422 + error message |
| TC-03051 | API | Learning insights | Edge case | GET /api/learning/tip?week at boundary value | Correct boundary handling |
| TC-03052 | API | Learning insights | No auth token | GET /api/learning/tip?week | 401 Unauthorized |
| TC-03053 | frontend-UAT | Learning insights | Logged in | Open week-specific tip in UI | UI renders correctly |
| TC-03054 | frontend-UAT | Learning insights | No data | Open week-specific tip with no data | No-data state shown |
| TC-03055 | API | Learning insights | Expired token | GET /api/learning/tip?week | 401 Unauthorized |
| TC-03056 | API | Learning insights | Insufficient role | GET /api/learning/tip?week | 403 Forbidden |
| TC-03057 | API | Learning insights | Logged in | GET /api/learning/tip?role | 200 + valid data |
| TC-03058 | API | Learning insights | Logged in | GET /api/learning/tip?role with invalid input | 400/422 + error message |
| TC-03059 | API | Learning insights | Edge case | GET /api/learning/tip?role at boundary value | Correct boundary handling |
| TC-03060 | API | Learning insights | No auth token | GET /api/learning/tip?role | 401 Unauthorized |
| TC-03061 | frontend-UAT | Learning insights | Logged in | Open role-specific tip in UI | UI renders correctly |
| TC-03062 | frontend-UAT | Learning insights | No data | Open role-specific tip with no data | No-data state shown |
| TC-03063 | API | Learning insights | Expired token | GET /api/learning/tip?role | 401 Unauthorized |
| TC-03064 | API | Learning insights | Insufficient role | GET /api/learning/tip?role | 403 Forbidden |
| TC-03065 | API | Learning insights | Logged in | GET /api/learning/tip?salary | 200 + valid data |
| TC-03066 | API | Learning insights | Logged in | GET /api/learning/tip?salary with invalid input | 400/422 + error message |
| TC-03067 | API | Learning insights | Edge case | GET /api/learning/tip?salary at boundary value | Correct boundary handling |
| TC-03068 | API | Learning insights | No auth token | GET /api/learning/tip?salary | 401 Unauthorized |
| TC-03069 | frontend-UAT | Learning insights | Logged in | Open salary-specific tip in UI | UI renders correctly |
| TC-03070 | frontend-UAT | Learning insights | No data | Open salary-specific tip with no data | No-data state shown |
| TC-03071 | API | Learning insights | Expired token | GET /api/learning/tip?salary | 401 Unauthorized |
| TC-03072 | API | Learning insights | Insufficient role | GET /api/learning/tip?salary | 403 Forbidden |
| TC-03073 | API | Learning insights | Logged in | GET /api/learning?empty | 200 + valid data |
| TC-03074 | API | Learning insights | Logged in | GET /api/learning?empty with invalid input | 400/422 + error message |
| TC-03075 | API | Learning insights | Edge case | GET /api/learning?empty at boundary value | Correct boundary handling |
| TC-03076 | API | Learning insights | No auth token | GET /api/learning?empty | 401 Unauthorized |
| TC-03077 | frontend-UAT | Learning insights | Logged in | Open no-data state in UI | UI renders correctly |
| TC-03078 | frontend-UAT | Learning insights | No data | Open no-data state with no data | No-data state shown |
| TC-03079 | API | Learning insights | Expired token | GET /api/learning?empty | 401 Unauthorized |
| TC-03080 | API | Learning insights | Insufficient role | GET /api/learning?empty | 403 Forbidden |
| TC-03081 | API | Learning insights | Logged in | GET /api/learning?panel | 200 + valid data |
| TC-03082 | API | Learning insights | Logged in | GET /api/learning?panel with invalid input | 400/422 + error message |
| TC-03083 | API | Learning insights | Edge case | GET /api/learning?panel at boundary value | Correct boundary handling |
| TC-03084 | API | Learning insights | No auth token | GET /api/learning?panel | 401 Unauthorized |
| TC-03085 | frontend-UAT | Learning insights | Logged in | Open panel render in UI | UI renders correctly |
| TC-03086 | frontend-UAT | Learning insights | No data | Open panel render with no data | No-data state shown |
| TC-03087 | API | Learning insights | Expired token | GET /api/learning?panel | 401 Unauthorized |
| TC-03088 | API | Learning insights | Insufficient role | GET /api/learning?panel | 403 Forbidden |
| TC-03089 | API | Learning insights | Logged in | GET /api/learning?export | 200 + valid data |
| TC-03090 | API | Learning insights | Logged in | GET /api/learning?export with invalid input | 400/422 + error message |
| TC-03091 | API | Learning insights | Edge case | GET /api/learning?export at boundary value | Correct boundary handling |
| TC-03092 | API | Learning insights | No auth token | GET /api/learning?export | 401 Unauthorized |
| TC-03093 | frontend-UAT | Learning insights | Logged in | Open export learning in UI | UI renders correctly |
| TC-03094 | frontend-UAT | Learning insights | No data | Open export learning with no data | No-data state shown |
| TC-03095 | API | Learning insights | Expired token | GET /api/learning?export | 401 Unauthorized |
| TC-03096 | API | Learning insights | Insufficient role | GET /api/learning?export | 403 Forbidden |
### F27 — Analytics salary/skills/sources/trend

| TC-03097 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/salary | 200 + valid data |
| TC-03098 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/salary with invalid input | 400/422 + error message |
| TC-03099 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics/salary at boundary value | Correct boundary handling |
| TC-03100 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics/salary | 401 Unauthorized |
| TC-03101 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open salary analytics in UI | UI renders correctly |
| TC-03102 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open salary analytics with no data | No-data state shown |
| TC-03103 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics/salary | 401 Unauthorized |
| TC-03104 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics/salary | 403 Forbidden |
| TC-03105 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/skills | 200 + valid data |
| TC-03106 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/skills with invalid input | 400/422 + error message |
| TC-03107 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics/skills at boundary value | Correct boundary handling |
| TC-03108 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics/skills | 401 Unauthorized |
| TC-03109 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open skills analytics in UI | UI renders correctly |
| TC-03110 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open skills analytics with no data | No-data state shown |
| TC-03111 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics/skills | 401 Unauthorized |
| TC-03112 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics/skills | 403 Forbidden |
| TC-03113 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/sources | 200 + valid data |
| TC-03114 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/sources with invalid input | 400/422 + error message |
| TC-03115 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics/sources at boundary value | Correct boundary handling |
| TC-03116 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics/sources | 401 Unauthorized |
| TC-03117 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open source analytics in UI | UI renders correctly |
| TC-03118 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open source analytics with no data | No-data state shown |
| TC-03119 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics/sources | 401 Unauthorized |
| TC-03120 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics/sources | 403 Forbidden |
| TC-03121 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/trend | 200 + valid data |
| TC-03122 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/trend with invalid input | 400/422 + error message |
| TC-03123 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics/trend at boundary value | Correct boundary handling |
| TC-03124 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics/trend | 401 Unauthorized |
| TC-03125 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open trend analytics in UI | UI renders correctly |
| TC-03126 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open trend analytics with no data | No-data state shown |
| TC-03127 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics/trend | 401 Unauthorized |
| TC-03128 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics/trend | 403 Forbidden |
| TC-03129 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/export | 200 + valid data |
| TC-03130 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/export with invalid input | 400/422 + error message |
| TC-03131 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics/export at boundary value | Correct boundary handling |
| TC-03132 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics/export | 401 Unauthorized |
| TC-03133 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open export analytics in UI | UI renders correctly |
| TC-03134 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open export analytics with no data | No-data state shown |
| TC-03135 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics/export | 401 Unauthorized |
| TC-03136 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics/export | 403 Forbidden |
| TC-03137 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?from | 200 + valid data |
| TC-03138 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?from with invalid input | 400/422 + error message |
| TC-03139 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?from at boundary value | Correct boundary handling |
| TC-03140 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?from | 401 Unauthorized |
| TC-03141 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open filter by date in UI | UI renders correctly |
| TC-03142 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open filter by date with no data | No-data state shown |
| TC-03143 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?from | 401 Unauthorized |
| TC-03144 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?from | 403 Forbidden |
| TC-03145 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/dashboard | 200 + valid data |
| TC-03146 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics/dashboard with invalid input | 400/422 + error message |
| TC-03147 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics/dashboard at boundary value | Correct boundary handling |
| TC-03148 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics/dashboard | 401 Unauthorized |
| TC-03149 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open combined dashboard in UI | UI renders correctly |
| TC-03150 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open combined dashboard with no data | No-data state shown |
| TC-03151 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics/dashboard | 401 Unauthorized |
| TC-03152 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics/dashboard | 403 Forbidden |
| TC-03153 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?compare | 200 + valid data |
| TC-03154 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?compare with invalid input | 400/422 + error message |
| TC-03155 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?compare at boundary value | Correct boundary handling |
| TC-03156 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?compare | 401 Unauthorized |
| TC-03157 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open compare ranges in UI | UI renders correctly |
| TC-03158 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open compare ranges with no data | No-data state shown |
| TC-03159 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?compare | 401 Unauthorized |
| TC-03160 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?compare | 403 Forbidden |
| TC-03161 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?empty | 200 + valid data |
| TC-03162 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?empty with invalid input | 400/422 + error message |
| TC-03163 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?empty at boundary value | Correct boundary handling |
| TC-03164 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?empty | 401 Unauthorized |
| TC-03165 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open no-data state in UI | UI renders correctly |
| TC-03166 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open no-data state with no data | No-data state shown |
| TC-03167 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?empty | 401 Unauthorized |
| TC-03168 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?empty | 403 Forbidden |
| TC-03169 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?salary | 200 + valid data |
| TC-03170 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?salary with invalid input | 400/422 + error message |
| TC-03171 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?salary at boundary value | Correct boundary handling |
| TC-03172 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?salary | 401 Unauthorized |
| TC-03173 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open salary render in UI | UI renders correctly |
| TC-03174 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open salary render with no data | No-data state shown |
| TC-03175 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?salary | 401 Unauthorized |
| TC-03176 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?salary | 403 Forbidden |
| TC-03177 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?skills | 200 + valid data |
| TC-03178 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?skills with invalid input | 400/422 + error message |
| TC-03179 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?skills at boundary value | Correct boundary handling |
| TC-03180 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?skills | 401 Unauthorized |
| TC-03181 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open skills render in UI | UI renders correctly |
| TC-03182 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open skills render with no data | No-data state shown |
| TC-03183 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?skills | 401 Unauthorized |
| TC-03184 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?skills | 403 Forbidden |
| TC-03185 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?sources | 200 + valid data |
| TC-03186 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?sources with invalid input | 400/422 + error message |
| TC-03187 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?sources at boundary value | Correct boundary handling |
| TC-03188 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?sources | 401 Unauthorized |
| TC-03189 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open source render in UI | UI renders correctly |
| TC-03190 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open source render with no data | No-data state shown |
| TC-03191 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?sources | 401 Unauthorized |
| TC-03192 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?sources | 403 Forbidden |
| TC-03193 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?trend | 200 + valid data |
| TC-03194 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?trend with invalid input | 400/422 + error message |
| TC-03195 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?trend at boundary value | Correct boundary handling |
| TC-03196 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?trend | 401 Unauthorized |
| TC-03197 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open trend render in UI | UI renders correctly |
| TC-03198 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open trend render with no data | No-data state shown |
| TC-03199 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?trend | 401 Unauthorized |
| TC-03200 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?trend | 403 Forbidden |
| TC-03201 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?mobile | 200 + valid data |
| TC-03202 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?mobile with invalid input | 400/422 + error message |
| TC-03203 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?mobile at boundary value | Correct boundary handling |
| TC-03204 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?mobile | 401 Unauthorized |
| TC-03205 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open mobile view in UI | UI renders correctly |
| TC-03206 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open mobile view with no data | No-data state shown |
| TC-03207 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?mobile | 401 Unauthorized |
| TC-03208 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?mobile | 403 Forbidden |
| TC-03209 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?print | 200 + valid data |
| TC-03210 | API | Analytics salary/skills/sources/trend | Logged in | GET /api/analytics?print with invalid input | 400/422 + error message |
| TC-03211 | API | Analytics salary/skills/sources/trend | Edge case | GET /api/analytics?print at boundary value | Correct boundary handling |
| TC-03212 | API | Analytics salary/skills/sources/trend | No auth token | GET /api/analytics?print | 401 Unauthorized |
| TC-03213 | frontend-UAT | Analytics salary/skills/sources/trend | Logged in | Open print view in UI | UI renders correctly |
| TC-03214 | frontend-UAT | Analytics salary/skills/sources/trend | No data | Open print view with no data | No-data state shown |
| TC-03215 | API | Analytics salary/skills/sources/trend | Expired token | GET /api/analytics?print | 401 Unauthorized |
| TC-03216 | API | Analytics salary/skills/sources/trend | Insufficient role | GET /api/analytics?print | 403 Forbidden |
### F28 — KPI goals & streak

| TC-03217 | API | KPI goals & streak | Logged in | PUT /api/kpi/goal | 200 + valid data |
| TC-03218 | API | KPI goals & streak | Logged in | PUT /api/kpi/goal with invalid input | 400/422 + error message |
| TC-03219 | API | KPI goals & streak | Edge case | PUT /api/kpi/goal at boundary value | Correct boundary handling |
| TC-03220 | API | KPI goals & streak | No auth token | PUT /api/kpi/goal | 401 Unauthorized |
| TC-03221 | frontend-UAT | KPI goals & streak | Logged in | Open set goal in UI | UI renders correctly |
| TC-03222 | frontend-UAT | KPI goals & streak | No data | Open set goal with no data | No-data state shown |
| TC-03223 | API | KPI goals & streak | Expired token | PUT /api/kpi/goal | 401 Unauthorized |
| TC-03224 | API | KPI goals & streak | Insufficient role | PUT /api/kpi/goal | 403 Forbidden |
| TC-03225 | API | KPI goals & streak | Logged in | GET /api/kpi/goal/progress | 200 + valid data |
| TC-03226 | API | KPI goals & streak | Logged in | GET /api/kpi/goal/progress with invalid input | 400/422 + error message |
| TC-03227 | API | KPI goals & streak | Edge case | GET /api/kpi/goal/progress at boundary value | Correct boundary handling |
| TC-03228 | API | KPI goals & streak | No auth token | GET /api/kpi/goal/progress | 401 Unauthorized |
| TC-03229 | frontend-UAT | KPI goals & streak | Logged in | Open goal progress in UI | UI renders correctly |
| TC-03230 | frontend-UAT | KPI goals & streak | No data | Open goal progress with no data | No-data state shown |
| TC-03231 | API | KPI goals & streak | Expired token | GET /api/kpi/goal/progress | 401 Unauthorized |
| TC-03232 | API | KPI goals & streak | Insufficient role | GET /api/kpi/goal/progress | 403 Forbidden |
| TC-03233 | API | KPI goals & streak | Logged in | GET /api/kpi/submitted?week | 200 + valid data |
| TC-03234 | API | KPI goals & streak | Logged in | GET /api/kpi/submitted?week with invalid input | 400/422 + error message |
| TC-03235 | API | KPI goals & streak | Edge case | GET /api/kpi/submitted?week at boundary value | Correct boundary handling |
| TC-03236 | API | KPI goals & streak | No auth token | GET /api/kpi/submitted?week | 401 Unauthorized |
| TC-03237 | frontend-UAT | KPI goals & streak | Logged in | Open this-week count in UI | UI renders correctly |
| TC-03238 | frontend-UAT | KPI goals & streak | No data | Open this-week count with no data | No-data state shown |
| TC-03239 | API | KPI goals & streak | Expired token | GET /api/kpi/submitted?week | 401 Unauthorized |
| TC-03240 | API | KPI goals & streak | Insufficient role | GET /api/kpi/submitted?week | 403 Forbidden |
| TC-03241 | API | KPI goals & streak | Logged in | GET /api/kpi/submitted?all | 200 + valid data |
| TC-03242 | API | KPI goals & streak | Logged in | GET /api/kpi/submitted?all with invalid input | 400/422 + error message |
| TC-03243 | API | KPI goals & streak | Edge case | GET /api/kpi/submitted?all at boundary value | Correct boundary handling |
| TC-03244 | API | KPI goals & streak | No auth token | GET /api/kpi/submitted?all | 401 Unauthorized |
| TC-03245 | frontend-UAT | KPI goals & streak | Logged in | Open all-time count in UI | UI renders correctly |
| TC-03246 | frontend-UAT | KPI goals & streak | No data | Open all-time count with no data | No-data state shown |
| TC-03247 | API | KPI goals & streak | Expired token | GET /api/kpi/submitted?all | 401 Unauthorized |
| TC-03248 | API | KPI goals & streak | Insufficient role | GET /api/kpi/submitted?all | 403 Forbidden |
| TC-03249 | API | KPI goals & streak | Logged in | GET /api/kpi/streak | 200 + valid data |
| TC-03250 | API | KPI goals & streak | Logged in | GET /api/kpi/streak with invalid input | 400/422 + error message |
| TC-03251 | API | KPI goals & streak | Edge case | GET /api/kpi/streak at boundary value | Correct boundary handling |
| TC-03252 | API | KPI goals & streak | No auth token | GET /api/kpi/streak | 401 Unauthorized |
| TC-03253 | frontend-UAT | KPI goals & streak | Logged in | Open streak counter in UI | UI renders correctly |
| TC-03254 | frontend-UAT | KPI goals & streak | No data | Open streak counter with no data | No-data state shown |
| TC-03255 | API | KPI goals & streak | Expired token | GET /api/kpi/streak | 401 Unauthorized |
| TC-03256 | API | KPI goals & streak | Insufficient role | GET /api/kpi/streak | 403 Forbidden |
| TC-03257 | API | KPI goals & streak | Logged in | GET /api/kpi/streak-dots | 200 + valid data |
| TC-03258 | API | KPI goals & streak | Logged in | GET /api/kpi/streak-dots with invalid input | 400/422 + error message |
| TC-03259 | API | KPI goals & streak | Edge case | GET /api/kpi/streak-dots at boundary value | Correct boundary handling |
| TC-03260 | API | KPI goals & streak | No auth token | GET /api/kpi/streak-dots | 401 Unauthorized |
| TC-03261 | frontend-UAT | KPI goals & streak | Logged in | Open streak dots in UI | UI renders correctly |
| TC-03262 | frontend-UAT | KPI goals & streak | No data | Open streak dots with no data | No-data state shown |
| TC-03263 | API | KPI goals & streak | Expired token | GET /api/kpi/streak-dots | 401 Unauthorized |
| TC-03264 | API | KPI goals & streak | Insufficient role | GET /api/kpi/streak-dots | 403 Forbidden |
| TC-03265 | API | KPI goals & streak | Logged in | PUT /api/kpi/streak/reset | 200 + valid data |
| TC-03266 | API | KPI goals & streak | Logged in | PUT /api/kpi/streak/reset with invalid input | 400/422 + error message |
| TC-03267 | API | KPI goals & streak | Edge case | PUT /api/kpi/streak/reset at boundary value | Correct boundary handling |
| TC-03268 | API | KPI goals & streak | No auth token | PUT /api/kpi/streak/reset | 401 Unauthorized |
| TC-03269 | frontend-UAT | KPI goals & streak | Logged in | Open reset streak in UI | UI renders correctly |
| TC-03270 | frontend-UAT | KPI goals & streak | No data | Open reset streak with no data | No-data state shown |
| TC-03271 | API | KPI goals & streak | Expired token | PUT /api/kpi/streak/reset | 401 Unauthorized |
| TC-03272 | API | KPI goals & streak | Insufficient role | PUT /api/kpi/streak/reset | 403 Forbidden |
| TC-03273 | API | KPI goals & streak | Logged in | PUT /api/kpi/goal/save | 200 + valid data |
| TC-03274 | API | KPI goals & streak | Logged in | PUT /api/kpi/goal/save with invalid input | 400/422 + error message |
| TC-03275 | API | KPI goals & streak | Edge case | PUT /api/kpi/goal/save at boundary value | Correct boundary handling |
| TC-03276 | API | KPI goals & streak | No auth token | PUT /api/kpi/goal/save | 401 Unauthorized |
| TC-03277 | frontend-UAT | KPI goals & streak | Logged in | Open save goal in UI | UI renders correctly |
| TC-03278 | frontend-UAT | KPI goals & streak | No data | Open save goal with no data | No-data state shown |
| TC-03279 | API | KPI goals & streak | Expired token | PUT /api/kpi/goal/save | 401 Unauthorized |
| TC-03280 | API | KPI goals & streak | Insufficient role | PUT /api/kpi/goal/save | 403 Forbidden |
| TC-03281 | API | KPI goals & streak | Logged in | GET /api/kpi/how-it-works | 200 + valid data |
| TC-03282 | API | KPI goals & streak | Logged in | GET /api/kpi/how-it-works with invalid input | 400/422 + error message |
| TC-03283 | API | KPI goals & streak | Edge case | GET /api/kpi/how-it-works at boundary value | Correct boundary handling |
| TC-03284 | API | KPI goals & streak | No auth token | GET /api/kpi/how-it-works | 401 Unauthorized |
| TC-03285 | frontend-UAT | KPI goals & streak | Logged in | Open how it works in UI | UI renders correctly |
| TC-03286 | frontend-UAT | KPI goals & streak | No data | Open how it works with no data | No-data state shown |
| TC-03287 | API | KPI goals & streak | Expired token | GET /api/kpi/how-it-works | 401 Unauthorized |
| TC-03288 | API | KPI goals & streak | Insufficient role | GET /api/kpi/how-it-works | 403 Forbidden |
| TC-03289 | API | KPI goals & streak | Logged in | PUT /api/kpi/goal/increase | 200 + valid data |
| TC-03290 | API | KPI goals & streak | Logged in | PUT /api/kpi/goal/increase with invalid input | 400/422 + error message |
| TC-03291 | API | KPI goals & streak | Edge case | PUT /api/kpi/goal/increase at boundary value | Correct boundary handling |
| TC-03292 | API | KPI goals & streak | No auth token | PUT /api/kpi/goal/increase | 401 Unauthorized |
| TC-03293 | frontend-UAT | KPI goals & streak | Logged in | Open increase goal in UI | UI renders correctly |
| TC-03294 | frontend-UAT | KPI goals & streak | No data | Open increase goal with no data | No-data state shown |
| TC-03295 | API | KPI goals & streak | Expired token | PUT /api/kpi/goal/increase | 401 Unauthorized |
| TC-03296 | API | KPI goals & streak | Insufficient role | PUT /api/kpi/goal/increase | 403 Forbidden |
| TC-03297 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_week | 200 + valid data |
| TC-03298 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_week with invalid input | 400/422 + error message |
| TC-03299 | API | KPI goals & streak | Edge case | GET /api/kpi/goal?by_week at boundary value | Correct boundary handling |
| TC-03300 | API | KPI goals & streak | No auth token | GET /api/kpi/goal?by_week | 401 Unauthorized |
| TC-03301 | frontend-UAT | KPI goals & streak | Logged in | Open goal by week in UI | UI renders correctly |
| TC-03302 | frontend-UAT | KPI goals & streak | No data | Open goal by week with no data | No-data state shown |
| TC-03303 | API | KPI goals & streak | Expired token | GET /api/kpi/goal?by_week | 401 Unauthorized |
| TC-03304 | API | KPI goals & streak | Insufficient role | GET /api/kpi/goal?by_week | 403 Forbidden |
| TC-03305 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_source | 200 + valid data |
| TC-03306 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_source with invalid input | 400/422 + error message |
| TC-03307 | API | KPI goals & streak | Edge case | GET /api/kpi/goal?by_source at boundary value | Correct boundary handling |
| TC-03308 | API | KPI goals & streak | No auth token | GET /api/kpi/goal?by_source | 401 Unauthorized |
| TC-03309 | frontend-UAT | KPI goals & streak | Logged in | Open goal by source in UI | UI renders correctly |
| TC-03310 | frontend-UAT | KPI goals & streak | No data | Open goal by source with no data | No-data state shown |
| TC-03311 | API | KPI goals & streak | Expired token | GET /api/kpi/goal?by_source | 401 Unauthorized |
| TC-03312 | API | KPI goals & streak | Insufficient role | GET /api/kpi/goal?by_source | 403 Forbidden |
| TC-03313 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_role | 200 + valid data |
| TC-03314 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_role with invalid input | 400/422 + error message |
| TC-03315 | API | KPI goals & streak | Edge case | GET /api/kpi/goal?by_role at boundary value | Correct boundary handling |
| TC-03316 | API | KPI goals & streak | No auth token | GET /api/kpi/goal?by_role | 401 Unauthorized |
| TC-03317 | frontend-UAT | KPI goals & streak | Logged in | Open goal by role in UI | UI renders correctly |
| TC-03318 | frontend-UAT | KPI goals & streak | No data | Open goal by role with no data | No-data state shown |
| TC-03319 | API | KPI goals & streak | Expired token | GET /api/kpi/goal?by_role | 401 Unauthorized |
| TC-03320 | API | KPI goals & streak | Insufficient role | GET /api/kpi/goal?by_role | 403 Forbidden |
| TC-03321 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_salary | 200 + valid data |
| TC-03322 | API | KPI goals & streak | Logged in | GET /api/kpi/goal?by_salary with invalid input | 400/422 + error message |
| TC-03323 | API | KPI goals & streak | Edge case | GET /api/kpi/goal?by_salary at boundary value | Correct boundary handling |
| TC-03324 | API | KPI goals & streak | No auth token | GET /api/kpi/goal?by_salary | 401 Unauthorized |
| TC-03325 | frontend-UAT | KPI goals & streak | Logged in | Open goal by salary in UI | UI renders correctly |
| TC-03326 | frontend-UAT | KPI goals & streak | No data | Open goal by salary with no data | No-data state shown |
| TC-03327 | API | KPI goals & streak | Expired token | GET /api/kpi/goal?by_salary | 401 Unauthorized |
| TC-03328 | API | KPI goals & streak | Insufficient role | GET /api/kpi/goal?by_salary | 403 Forbidden |
| TC-03329 | API | KPI goals & streak | Logged in | GET /api/kpi?empty | 200 + valid data |
| TC-03330 | API | KPI goals & streak | Logged in | GET /api/kpi?empty with invalid input | 400/422 + error message |
| TC-03331 | API | KPI goals & streak | Edge case | GET /api/kpi?empty at boundary value | Correct boundary handling |
| TC-03332 | API | KPI goals & streak | No auth token | GET /api/kpi?empty | 401 Unauthorized |
| TC-03333 | frontend-UAT | KPI goals & streak | Logged in | Open no-data state in UI | UI renders correctly |
| TC-03334 | frontend-UAT | KPI goals & streak | No data | Open no-data state with no data | No-data state shown |
| TC-03335 | API | KPI goals & streak | Expired token | GET /api/kpi?empty | 401 Unauthorized |
| TC-03336 | API | KPI goals & streak | Insufficient role | GET /api/kpi?empty | 403 Forbidden |
### F29 — Stats & top jobs

| TC-03337 | API | Stats & top jobs | Logged in | GET /api/stats/overall | 200 + valid data |
| TC-03338 | API | Stats & top jobs | Logged in | GET /api/stats/overall with invalid input | 400/422 + error message |
| TC-03339 | API | Stats & top jobs | Edge case | GET /api/stats/overall at boundary value | Correct boundary handling |
| TC-03340 | API | Stats & top jobs | No auth token | GET /api/stats/overall | 401 Unauthorized |
| TC-03341 | frontend-UAT | Stats & top jobs | Logged in | Open overall stats in UI | UI renders correctly |
| TC-03342 | frontend-UAT | Stats & top jobs | No data | Open overall stats with no data | No-data state shown |
| TC-03343 | API | Stats & top jobs | Expired token | GET /api/stats/overall | 401 Unauthorized |
| TC-03344 | API | Stats & top jobs | Insufficient role | GET /api/stats/overall | 403 Forbidden |
| TC-03345 | API | Stats & top jobs | Logged in | GET /api/stats/top-jobs | 200 + valid data |
| TC-03346 | API | Stats & top jobs | Logged in | GET /api/stats/top-jobs with invalid input | 400/422 + error message |
| TC-03347 | API | Stats & top jobs | Edge case | GET /api/stats/top-jobs at boundary value | Correct boundary handling |
| TC-03348 | API | Stats & top jobs | No auth token | GET /api/stats/top-jobs | 401 Unauthorized |
| TC-03349 | frontend-UAT | Stats & top jobs | Logged in | Open top jobs in UI | UI renders correctly |
| TC-03350 | frontend-UAT | Stats & top jobs | No data | Open top jobs with no data | No-data state shown |
| TC-03351 | API | Stats & top jobs | Expired token | GET /api/stats/top-jobs | 401 Unauthorized |
| TC-03352 | API | Stats & top jobs | Insufficient role | GET /api/stats/top-jobs | 403 Forbidden |
| TC-03353 | API | Stats & top jobs | Logged in | GET /api/stats/summary | 200 + valid data |
| TC-03354 | API | Stats & top jobs | Logged in | GET /api/stats/summary with invalid input | 400/422 + error message |
| TC-03355 | API | Stats & top jobs | Edge case | GET /api/stats/summary at boundary value | Correct boundary handling |
| TC-03356 | API | Stats & top jobs | No auth token | GET /api/stats/summary | 401 Unauthorized |
| TC-03357 | frontend-UAT | Stats & top jobs | Logged in | Open stats summary in UI | UI renders correctly |
| TC-03358 | frontend-UAT | Stats & top jobs | No data | Open stats summary with no data | No-data state shown |
| TC-03359 | API | Stats & top jobs | Expired token | GET /api/stats/summary | 401 Unauthorized |
| TC-03360 | API | Stats & top jobs | Insufficient role | GET /api/stats/summary | 403 Forbidden |
| TC-03361 | API | Stats & top jobs | Logged in | GET /api/stats/top-jobs?detailed | 200 + valid data |
| TC-03362 | API | Stats & top jobs | Logged in | GET /api/stats/top-jobs?detailed with invalid input | 400/422 + error message |
| TC-03363 | API | Stats & top jobs | Edge case | GET /api/stats/top-jobs?detailed at boundary value | Correct boundary handling |
| TC-03364 | API | Stats & top jobs | No auth token | GET /api/stats/top-jobs?detailed | 401 Unauthorized |
| TC-03365 | frontend-UAT | Stats & top jobs | Logged in | Open detailed top jobs in UI | UI renders correctly |
| TC-03366 | frontend-UAT | Stats & top jobs | No data | Open detailed top jobs with no data | No-data state shown |
| TC-03367 | API | Stats & top jobs | Expired token | GET /api/stats/top-jobs?detailed | 401 Unauthorized |
| TC-03368 | API | Stats & top jobs | Insufficient role | GET /api/stats/top-jobs?detailed | 403 Forbidden |
| TC-03369 | API | Stats & top jobs | Logged in | GET /api/stats/approval-rate | 200 + valid data |
| TC-03370 | API | Stats & top jobs | Logged in | GET /api/stats/approval-rate with invalid input | 400/422 + error message |
| TC-03371 | API | Stats & top jobs | Edge case | GET /api/stats/approval-rate at boundary value | Correct boundary handling |
| TC-03372 | API | Stats & top jobs | No auth token | GET /api/stats/approval-rate | 401 Unauthorized |
| TC-03373 | frontend-UAT | Stats & top jobs | Logged in | Open approval rate in UI | UI renders correctly |
| TC-03374 | frontend-UAT | Stats & top jobs | No data | Open approval rate with no data | No-data state shown |
| TC-03375 | API | Stats & top jobs | Expired token | GET /api/stats/approval-rate | 401 Unauthorized |
| TC-03376 | API | Stats & top jobs | Insufficient role | GET /api/stats/approval-rate | 403 Forbidden |
| TC-03377 | API | Stats & top jobs | Logged in | GET /api/stats?by_source | 200 + valid data |
| TC-03378 | API | Stats & top jobs | Logged in | GET /api/stats?by_source with invalid input | 400/422 + error message |
| TC-03379 | API | Stats & top jobs | Edge case | GET /api/stats?by_source at boundary value | Correct boundary handling |
| TC-03380 | API | Stats & top jobs | No auth token | GET /api/stats?by_source | 401 Unauthorized |
| TC-03381 | frontend-UAT | Stats & top jobs | Logged in | Open stats by source in UI | UI renders correctly |
| TC-03382 | frontend-UAT | Stats & top jobs | No data | Open stats by source with no data | No-data state shown |
| TC-03383 | API | Stats & top jobs | Expired token | GET /api/stats?by_source | 401 Unauthorized |
| TC-03384 | API | Stats & top jobs | Insufficient role | GET /api/stats?by_source | 403 Forbidden |
| TC-03385 | API | Stats & top jobs | Logged in | GET /api/stats?by_role | 200 + valid data |
| TC-03386 | API | Stats & top jobs | Logged in | GET /api/stats?by_role with invalid input | 400/422 + error message |
| TC-03387 | API | Stats & top jobs | Edge case | GET /api/stats?by_role at boundary value | Correct boundary handling |
| TC-03388 | API | Stats & top jobs | No auth token | GET /api/stats?by_role | 401 Unauthorized |
| TC-03389 | frontend-UAT | Stats & top jobs | Logged in | Open stats by role in UI | UI renders correctly |
| TC-03390 | frontend-UAT | Stats & top jobs | No data | Open stats by role with no data | No-data state shown |
| TC-03391 | API | Stats & top jobs | Expired token | GET /api/stats?by_role | 401 Unauthorized |
| TC-03392 | API | Stats & top jobs | Insufficient role | GET /api/stats?by_role | 403 Forbidden |
| TC-03393 | API | Stats & top jobs | Logged in | GET /api/stats?by_salary | 200 + valid data |
| TC-03394 | API | Stats & top jobs | Logged in | GET /api/stats?by_salary with invalid input | 400/422 + error message |
| TC-03395 | API | Stats & top jobs | Edge case | GET /api/stats?by_salary at boundary value | Correct boundary handling |
| TC-03396 | API | Stats & top jobs | No auth token | GET /api/stats?by_salary | 401 Unauthorized |
| TC-03397 | frontend-UAT | Stats & top jobs | Logged in | Open stats by salary in UI | UI renders correctly |
| TC-03398 | frontend-UAT | Stats & top jobs | No data | Open stats by salary with no data | No-data state shown |
| TC-03399 | API | Stats & top jobs | Expired token | GET /api/stats?by_salary | 401 Unauthorized |
| TC-03400 | API | Stats & top jobs | Insufficient role | GET /api/stats?by_salary | 403 Forbidden |
| TC-03401 | API | Stats & top jobs | Logged in | GET /api/stats?by_week | 200 + valid data |
| TC-03402 | API | Stats & top jobs | Logged in | GET /api/stats?by_week with invalid input | 400/422 + error message |
| TC-03403 | API | Stats & top jobs | Edge case | GET /api/stats?by_week at boundary value | Correct boundary handling |
| TC-03404 | API | Stats & top jobs | No auth token | GET /api/stats?by_week | 401 Unauthorized |
| TC-03405 | frontend-UAT | Stats & top jobs | Logged in | Open stats by week in UI | UI renders correctly |
| TC-03406 | frontend-UAT | Stats & top jobs | No data | Open stats by week with no data | No-data state shown |
| TC-03407 | API | Stats & top jobs | Expired token | GET /api/stats?by_week | 401 Unauthorized |
| TC-03408 | API | Stats & top jobs | Insufficient role | GET /api/stats?by_week | 403 Forbidden |
| TC-03409 | API | Stats & top jobs | Logged in | GET /api/stats?empty | 200 + valid data |
| TC-03410 | API | Stats & top jobs | Logged in | GET /api/stats?empty with invalid input | 400/422 + error message |
| TC-03411 | API | Stats & top jobs | Edge case | GET /api/stats?empty at boundary value | Correct boundary handling |
| TC-03412 | API | Stats & top jobs | No auth token | GET /api/stats?empty | 401 Unauthorized |
| TC-03413 | frontend-UAT | Stats & top jobs | Logged in | Open no-data state in UI | UI renders correctly |
| TC-03414 | frontend-UAT | Stats & top jobs | No data | Open no-data state with no data | No-data state shown |
| TC-03415 | API | Stats & top jobs | Expired token | GET /api/stats?empty | 401 Unauthorized |
| TC-03416 | API | Stats & top jobs | Insufficient role | GET /api/stats?empty | 403 Forbidden |
| TC-03417 | API | Stats & top jobs | Logged in | GET /api/stats?summary | 200 + valid data |
| TC-03418 | API | Stats & top jobs | Logged in | GET /api/stats?summary with invalid input | 400/422 + error message |
| TC-03419 | API | Stats & top jobs | Edge case | GET /api/stats?summary at boundary value | Correct boundary handling |
| TC-03420 | API | Stats & top jobs | No auth token | GET /api/stats?summary | 401 Unauthorized |
| TC-03421 | frontend-UAT | Stats & top jobs | Logged in | Open summary render in UI | UI renders correctly |
| TC-03422 | frontend-UAT | Stats & top jobs | No data | Open summary render with no data | No-data state shown |
| TC-03423 | API | Stats & top jobs | Expired token | GET /api/stats?summary | 401 Unauthorized |
| TC-03424 | API | Stats & top jobs | Insufficient role | GET /api/stats?summary | 403 Forbidden |
| TC-03425 | API | Stats & top jobs | Logged in | GET /api/stats?top | 200 + valid data |
| TC-03426 | API | Stats & top jobs | Logged in | GET /api/stats?top with invalid input | 400/422 + error message |
| TC-03427 | API | Stats & top jobs | Edge case | GET /api/stats?top at boundary value | Correct boundary handling |
| TC-03428 | API | Stats & top jobs | No auth token | GET /api/stats?top | 401 Unauthorized |
| TC-03429 | frontend-UAT | Stats & top jobs | Logged in | Open top jobs render in UI | UI renders correctly |
| TC-03430 | frontend-UAT | Stats & top jobs | No data | Open top jobs render with no data | No-data state shown |
| TC-03431 | API | Stats & top jobs | Expired token | GET /api/stats?top | 401 Unauthorized |
| TC-03432 | API | Stats & top jobs | Insufficient role | GET /api/stats?top | 403 Forbidden |
| TC-03433 | API | Stats & top jobs | Logged in | GET /api/stats?mobile | 200 + valid data |
| TC-03434 | API | Stats & top jobs | Logged in | GET /api/stats?mobile with invalid input | 400/422 + error message |
| TC-03435 | API | Stats & top jobs | Edge case | GET /api/stats?mobile at boundary value | Correct boundary handling |
| TC-03436 | API | Stats & top jobs | No auth token | GET /api/stats?mobile | 401 Unauthorized |
| TC-03437 | frontend-UAT | Stats & top jobs | Logged in | Open mobile view in UI | UI renders correctly |
| TC-03438 | frontend-UAT | Stats & top jobs | No data | Open mobile view with no data | No-data state shown |
| TC-03439 | API | Stats & top jobs | Expired token | GET /api/stats?mobile | 401 Unauthorized |
| TC-03440 | API | Stats & top jobs | Insufficient role | GET /api/stats?mobile | 403 Forbidden |
| TC-03441 | API | Stats & top jobs | Logged in | GET /api/stats?print | 200 + valid data |
| TC-03442 | API | Stats & top jobs | Logged in | GET /api/stats?print with invalid input | 400/422 + error message |
| TC-03443 | API | Stats & top jobs | Edge case | GET /api/stats?print at boundary value | Correct boundary handling |
| TC-03444 | API | Stats & top jobs | No auth token | GET /api/stats?print | 401 Unauthorized |
| TC-03445 | frontend-UAT | Stats & top jobs | Logged in | Open print view in UI | UI renders correctly |
| TC-03446 | frontend-UAT | Stats & top jobs | No data | Open print view with no data | No-data state shown |
| TC-03447 | API | Stats & top jobs | Expired token | GET /api/stats?print | 401 Unauthorized |
| TC-03448 | API | Stats & top jobs | Insufficient role | GET /api/stats?print | 403 Forbidden |
| TC-03449 | API | Stats & top jobs | Logged in | GET /api/stats?export | 200 + valid data |
| TC-03450 | API | Stats & top jobs | Logged in | GET /api/stats?export with invalid input | 400/422 + error message |
| TC-03451 | API | Stats & top jobs | Edge case | GET /api/stats?export at boundary value | Correct boundary handling |
| TC-03452 | API | Stats & top jobs | No auth token | GET /api/stats?export | 401 Unauthorized |
| TC-03453 | frontend-UAT | Stats & top jobs | Logged in | Open export stats in UI | UI renders correctly |
| TC-03454 | frontend-UAT | Stats & top jobs | No data | Open export stats with no data | No-data state shown |
| TC-03455 | API | Stats & top jobs | Expired token | GET /api/stats?export | 401 Unauthorized |
| TC-03456 | API | Stats & top jobs | Insufficient role | GET /api/stats?export | 403 Forbidden |
### F30 — Feedback & continuous learning

| TC-03457 | API | Feedback & continuous learning | Logged in | POST /api/feedback/{job_id} | 200 + valid data |
| TC-03458 | API | Feedback & continuous learning | Logged in | POST /api/feedback/{job_id} with invalid input | 400/422 + error message |
| TC-03459 | API | Feedback & continuous learning | Edge case | POST /api/feedback/{job_id} at boundary value | Correct boundary handling |
| TC-03460 | API | Feedback & continuous learning | No auth token | POST /api/feedback/{job_id} | 401 Unauthorized |
| TC-03461 | frontend-UAT | Feedback & continuous learning | Logged in | Open submit feedback in UI | UI renders correctly |
| TC-03462 | frontend-UAT | Feedback & continuous learning | No data | Open submit feedback with no data | No-data state shown |
| TC-03463 | API | Feedback & continuous learning | Expired token | POST /api/feedback/{job_id} | 401 Unauthorized |
| TC-03464 | API | Feedback & continuous learning | Insufficient role | POST /api/feedback/{job_id} | 403 Forbidden |
| TC-03465 | API | Feedback & continuous learning | Logged in | GET /api/feedback/{job_id} | 200 + valid data |
| TC-03466 | API | Feedback & continuous learning | Logged in | GET /api/feedback/{job_id} with invalid input | 400/422 + error message |
| TC-03467 | API | Feedback & continuous learning | Edge case | GET /api/feedback/{job_id} at boundary value | Correct boundary handling |
| TC-03468 | API | Feedback & continuous learning | No auth token | GET /api/feedback/{job_id} | 401 Unauthorized |
| TC-03469 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback recorded in UI | UI renders correctly |
| TC-03470 | frontend-UAT | Feedback & continuous learning | No data | Open feedback recorded with no data | No-data state shown |
| TC-03471 | API | Feedback & continuous learning | Expired token | GET /api/feedback/{job_id} | 401 Unauthorized |
| TC-03472 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback/{job_id} | 403 Forbidden |
| TC-03473 | API | Feedback & continuous learning | Logged in | GET /api/learning/effect | 200 + valid data |
| TC-03474 | API | Feedback & continuous learning | Logged in | GET /api/learning/effect with invalid input | 400/422 + error message |
| TC-03475 | API | Feedback & continuous learning | Edge case | GET /api/learning/effect at boundary value | Correct boundary handling |
| TC-03476 | API | Feedback & continuous learning | No auth token | GET /api/learning/effect | 401 Unauthorized |
| TC-03477 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback effect in UI | UI renders correctly |
| TC-03478 | frontend-UAT | Feedback & continuous learning | No data | Open feedback effect with no data | No-data state shown |
| TC-03479 | API | Feedback & continuous learning | Expired token | GET /api/learning/effect | 401 Unauthorized |
| TC-03480 | API | Feedback & continuous learning | Insufficient role | GET /api/learning/effect | 403 Forbidden |
| TC-03481 | API | Feedback & continuous learning | Logged in | GET /api/feedback/{job_id}/toast | 200 + valid data |
| TC-03482 | API | Feedback & continuous learning | Logged in | GET /api/feedback/{job_id}/toast with invalid input | 400/422 + error message |
| TC-03483 | API | Feedback & continuous learning | Edge case | GET /api/feedback/{job_id}/toast at boundary value | Correct boundary handling |
| TC-03484 | API | Feedback & continuous learning | No auth token | GET /api/feedback/{job_id}/toast | 401 Unauthorized |
| TC-03485 | frontend-UAT | Feedback & continuous learning | Logged in | Open confirmation in UI | UI renders correctly |
| TC-03486 | frontend-UAT | Feedback & continuous learning | No data | Open confirmation with no data | No-data state shown |
| TC-03487 | API | Feedback & continuous learning | Expired token | GET /api/feedback/{job_id}/toast | 401 Unauthorized |
| TC-03488 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback/{job_id}/toast | 403 Forbidden |
| TC-03489 | API | Feedback & continuous learning | Logged in | PUT /api/feedback/{job_id} | 200 + valid data |
| TC-03490 | API | Feedback & continuous learning | Logged in | PUT /api/feedback/{job_id} with invalid input | 400/422 + error message |
| TC-03491 | API | Feedback & continuous learning | Edge case | PUT /api/feedback/{job_id} at boundary value | Correct boundary handling |
| TC-03492 | API | Feedback & continuous learning | No auth token | PUT /api/feedback/{job_id} | 401 Unauthorized |
| TC-03493 | frontend-UAT | Feedback & continuous learning | Logged in | Open edit feedback in UI | UI renders correctly |
| TC-03494 | frontend-UAT | Feedback & continuous learning | No data | Open edit feedback with no data | No-data state shown |
| TC-03495 | API | Feedback & continuous learning | Expired token | PUT /api/feedback/{job_id} | 401 Unauthorized |
| TC-03496 | API | Feedback & continuous learning | Insufficient role | PUT /api/feedback/{job_id} | 403 Forbidden |
| TC-03497 | API | Feedback & continuous learning | Logged in | GET /api/feedback/history | 200 + valid data |
| TC-03498 | API | Feedback & continuous learning | Logged in | GET /api/feedback/history with invalid input | 400/422 + error message |
| TC-03499 | API | Feedback & continuous learning | Edge case | GET /api/feedback/history at boundary value | Correct boundary handling |
| TC-03500 | API | Feedback & continuous learning | No auth token | GET /api/feedback/history | 401 Unauthorized |
| TC-03501 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback history in UI | UI renders correctly |
| TC-03502 | frontend-UAT | Feedback & continuous learning | No data | Open feedback history with no data | No-data state shown |
| TC-03503 | API | Feedback & continuous learning | Expired token | GET /api/feedback/history | 401 Unauthorized |
| TC-03504 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback/history | 403 Forbidden |
| TC-03505 | API | Feedback & continuous learning | Logged in | GET /api/feedback?job | 200 + valid data |
| TC-03506 | API | Feedback & continuous learning | Logged in | GET /api/feedback?job with invalid input | 400/422 + error message |
| TC-03507 | API | Feedback & continuous learning | Edge case | GET /api/feedback?job at boundary value | Correct boundary handling |
| TC-03508 | API | Feedback & continuous learning | No auth token | GET /api/feedback?job | 401 Unauthorized |
| TC-03509 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback by job in UI | UI renders correctly |
| TC-03510 | frontend-UAT | Feedback & continuous learning | No data | Open feedback by job with no data | No-data state shown |
| TC-03511 | API | Feedback & continuous learning | Expired token | GET /api/feedback?job | 401 Unauthorized |
| TC-03512 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?job | 403 Forbidden |
| TC-03513 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_source | 200 + valid data |
| TC-03514 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_source with invalid input | 400/422 + error message |
| TC-03515 | API | Feedback & continuous learning | Edge case | GET /api/feedback?by_source at boundary value | Correct boundary handling |
| TC-03516 | API | Feedback & continuous learning | No auth token | GET /api/feedback?by_source | 401 Unauthorized |
| TC-03517 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback by source in UI | UI renders correctly |
| TC-03518 | frontend-UAT | Feedback & continuous learning | No data | Open feedback by source with no data | No-data state shown |
| TC-03519 | API | Feedback & continuous learning | Expired token | GET /api/feedback?by_source | 401 Unauthorized |
| TC-03520 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?by_source | 403 Forbidden |
| TC-03521 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_role | 200 + valid data |
| TC-03522 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_role with invalid input | 400/422 + error message |
| TC-03523 | API | Feedback & continuous learning | Edge case | GET /api/feedback?by_role at boundary value | Correct boundary handling |
| TC-03524 | API | Feedback & continuous learning | No auth token | GET /api/feedback?by_role | 401 Unauthorized |
| TC-03525 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback by role in UI | UI renders correctly |
| TC-03526 | frontend-UAT | Feedback & continuous learning | No data | Open feedback by role with no data | No-data state shown |
| TC-03527 | API | Feedback & continuous learning | Expired token | GET /api/feedback?by_role | 401 Unauthorized |
| TC-03528 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?by_role | 403 Forbidden |
| TC-03529 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_salary | 200 + valid data |
| TC-03530 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_salary with invalid input | 400/422 + error message |
| TC-03531 | API | Feedback & continuous learning | Edge case | GET /api/feedback?by_salary at boundary value | Correct boundary handling |
| TC-03532 | API | Feedback & continuous learning | No auth token | GET /api/feedback?by_salary | 401 Unauthorized |
| TC-03533 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback by salary in UI | UI renders correctly |
| TC-03534 | frontend-UAT | Feedback & continuous learning | No data | Open feedback by salary with no data | No-data state shown |
| TC-03535 | API | Feedback & continuous learning | Expired token | GET /api/feedback?by_salary | 401 Unauthorized |
| TC-03536 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?by_salary | 403 Forbidden |
| TC-03537 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_week | 200 + valid data |
| TC-03538 | API | Feedback & continuous learning | Logged in | GET /api/feedback?by_week with invalid input | 400/422 + error message |
| TC-03539 | API | Feedback & continuous learning | Edge case | GET /api/feedback?by_week at boundary value | Correct boundary handling |
| TC-03540 | API | Feedback & continuous learning | No auth token | GET /api/feedback?by_week | 401 Unauthorized |
| TC-03541 | frontend-UAT | Feedback & continuous learning | Logged in | Open feedback by week in UI | UI renders correctly |
| TC-03542 | frontend-UAT | Feedback & continuous learning | No data | Open feedback by week with no data | No-data state shown |
| TC-03543 | API | Feedback & continuous learning | Expired token | GET /api/feedback?by_week | 401 Unauthorized |
| TC-03544 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?by_week | 403 Forbidden |
| TC-03545 | API | Feedback & continuous learning | Logged in | GET /api/feedback?empty | 200 + valid data |
| TC-03546 | API | Feedback & continuous learning | Logged in | GET /api/feedback?empty with invalid input | 400/422 + error message |
| TC-03547 | API | Feedback & continuous learning | Edge case | GET /api/feedback?empty at boundary value | Correct boundary handling |
| TC-03548 | API | Feedback & continuous learning | No auth token | GET /api/feedback?empty | 401 Unauthorized |
| TC-03549 | frontend-UAT | Feedback & continuous learning | Logged in | Open no-data state in UI | UI renders correctly |
| TC-03550 | frontend-UAT | Feedback & continuous learning | No data | Open no-data state with no data | No-data state shown |
| TC-03551 | API | Feedback & continuous learning | Expired token | GET /api/feedback?empty | 401 Unauthorized |
| TC-03552 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?empty | 403 Forbidden |
| TC-03553 | API | Feedback & continuous learning | Logged in | GET /api/feedback?toast | 200 + valid data |
| TC-03554 | API | Feedback & continuous learning | Logged in | GET /api/feedback?toast with invalid input | 400/422 + error message |
| TC-03555 | API | Feedback & continuous learning | Edge case | GET /api/feedback?toast at boundary value | Correct boundary handling |
| TC-03556 | API | Feedback & continuous learning | No auth token | GET /api/feedback?toast | 401 Unauthorized |
| TC-03557 | frontend-UAT | Feedback & continuous learning | Logged in | Open toast render in UI | UI renders correctly |
| TC-03558 | frontend-UAT | Feedback & continuous learning | No data | Open toast render with no data | No-data state shown |
| TC-03559 | API | Feedback & continuous learning | Expired token | GET /api/feedback?toast | 401 Unauthorized |
| TC-03560 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?toast | 403 Forbidden |
| TC-03561 | API | Feedback & continuous learning | Logged in | GET /api/feedback?edit | 200 + valid data |
| TC-03562 | API | Feedback & continuous learning | Logged in | GET /api/feedback?edit with invalid input | 400/422 + error message |
| TC-03563 | API | Feedback & continuous learning | Edge case | GET /api/feedback?edit at boundary value | Correct boundary handling |
| TC-03564 | API | Feedback & continuous learning | No auth token | GET /api/feedback?edit | 401 Unauthorized |
| TC-03565 | frontend-UAT | Feedback & continuous learning | Logged in | Open edit render in UI | UI renders correctly |
| TC-03566 | frontend-UAT | Feedback & continuous learning | No data | Open edit render with no data | No-data state shown |
| TC-03567 | API | Feedback & continuous learning | Expired token | GET /api/feedback?edit | 401 Unauthorized |
| TC-03568 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?edit | 403 Forbidden |
| TC-03569 | API | Feedback & continuous learning | Logged in | GET /api/feedback?export | 200 + valid data |
| TC-03570 | API | Feedback & continuous learning | Logged in | GET /api/feedback?export with invalid input | 400/422 + error message |
| TC-03571 | API | Feedback & continuous learning | Edge case | GET /api/feedback?export at boundary value | Correct boundary handling |
| TC-03572 | API | Feedback & continuous learning | No auth token | GET /api/feedback?export | 401 Unauthorized |
| TC-03573 | frontend-UAT | Feedback & continuous learning | Logged in | Open export feedback in UI | UI renders correctly |
| TC-03574 | frontend-UAT | Feedback & continuous learning | No data | Open export feedback with no data | No-data state shown |
| TC-03575 | API | Feedback & continuous learning | Expired token | GET /api/feedback?export | 401 Unauthorized |
| TC-03576 | API | Feedback & continuous learning | Insufficient role | GET /api/feedback?export | 403 Forbidden |

---

**Total test cases:** 3576

/* ZEYRECUITE dashboard — SPA logic */
(function () {
  "use strict";

  const TOKEN_KEY = "zr_token";
  const state = {
    token: localStorage.getItem(TOKEN_KEY) || null,
    user: null,
    view: "dashboard",
    jobs: [],
    top: [],
    stats: null,
    runs: [],
    analytics: null,
    filter: "all",
    search: "",
    sort: "confidence",
    compare: [],
    savedFilters: [],
    activeFilter: null,
    resumeVariants: [],
  };

  // ---------- API helper ----------
  async function api(path, opts = {}) {
    const headers = Object.assign({}, opts.headers || {});
    if (state.token) headers["Authorization"] = "Bearer " + state.token;
    if (opts.body && typeof opts.body === "object") {
      headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(opts.body);
    }
    const res = await fetch(path, Object.assign({}, opts, { headers }));
    if (res.status === 401 && !opts.allow401) {
      showLogin();
      throw new Error("unauthorized");
    }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || data.message || "Request failed");
    return data;
  }

  // ---------- Utilities ----------
  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  // Only allow http(s) URLs (including same-origin relative paths once
  // resolved); blocks javascript:, data:, etc. anywhere a URL is rendered.
  function safeUrl(u) {
    if (!u) return null;
    try {
      const url = new URL(u, window.location.href);
      if (url.protocol === "http:" || url.protocol === "https:") return url.href;
    } catch (e) { /* invalid URL */ }
    return null;
  }
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg;
    t.classList.remove("hidden");
    clearTimeout(t._t);
    t._t = setTimeout(() => t.classList.add("hidden"), 2600);
  }
  function stars(v) {
    if (v == null) return "";
    const full = Math.max(0, Math.min(5, Math.round(v)));
    return "★".repeat(full) + "☆".repeat(5 - full);
  }
  function confClass(label) {
    return (label || "").toLowerCase().replace(/\s+/g, "");
  }
  function confColor(v) {
    if (v >= 80) return "var(--green)";
    if (v >= 65) return "var(--primary)";
    if (v >= 50) return "var(--amber)";
    return "var(--red)";
  }
  function timeAgo(iso) {
    if (!iso) return "";
    const d = new Date(iso);
    const mins = Math.round((Date.now() - d.getTime()) / 60000);
    if (mins < 1) return "just now";
    if (mins < 60) return mins + "m ago";
    const hrs = Math.round(mins / 60);
    if (hrs < 24) return hrs + "h ago";
    return Math.round(hrs / 24) + "d ago";
  }

  // ---------- Auth ----------
  function showLogin() {
    state.token = null;
    localStorage.removeItem(TOKEN_KEY);
    $("#appView").classList.add("hidden");
    $("#loginView").classList.remove("hidden");
  }
  function showApp() {
    $("#loginView").classList.add("hidden");
    $("#appView").classList.remove("hidden");
  }

  async function doLogin(e) {
    e.preventDefault();
    const btn = $("#loginBtn");
    const err = $("#loginError");
    err.classList.add("hidden");
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Signing in…';
    try {
      const data = await api("/api/auth/login", {
        method: "POST",
        allow401: true,
        body: { username: e.target.username.value, password: e.target.password.value },
      });
      state.token = data.token;
      state.user = data.user;
      localStorage.setItem(TOKEN_KEY, data.token);
      showApp();
      setView("dashboard");
      loadAll();
    } catch (ex) {
      const msg = String((ex && ex.message) || "");
      err.textContent = /fetch|network/i.test(msg)
        ? "Could not reach the server. Please try again."
        : (msg && msg !== "unauthorized" ? msg : "Invalid username or password.");
      err.classList.remove("hidden");
    } finally {
      btn.disabled = false;
      btn.textContent = "Sign in";
    }
  }

  async function doLogout() {
    try { await api("/api/auth/logout", { method: "POST" }); } catch (e) {}
    showLogin();
  }

  // ---------- Data loading ----------
  async function loadAll() {
    try {
      const [stats, jobs, runs, top, filters, variants, learning, profile] = await Promise.all([
        api("/api/stats"),
        api("/api/jobs"),
        api("/api/runs?limit=8"),
        api("/api/top?limit=10"),
        api("/api/profile/filters").catch(() => ({ filters: [] })),
        api("/api/profile/resume-variants").catch(() => ({ variants: [] })),
        api("/api/learning/insights").catch(() => ({ has_data: false })),
        api("/api/profile").catch(() => null),
      ]);
      state.stats = stats;
      state.jobs = jobs;
      state.runs = runs;
      state.top = top;
      state.savedFilters = filters.filters || [];
      state.resumeVariants = variants.variants || [];
      state.learning = learning;
      state.profile = profile;
      renderSidebar();
      renderCurrent();
    } catch (err) {
      // A transient failure (server hiccup, offline) must never log the user
      // out — api() already calls showLogin() itself on a real 401.
      console.error("loadAll failed:", err);
      if (String(err && err.message) !== "unauthorized") {
        toast("Some dashboard data failed to load.");
      }
    }
  }

  function renderSidebar() {
    const s = state.stats || {};
    $("#sideTotal").textContent = s.total || 0;
    $("#sideEligible").textContent = s.eligible || 0;
    $("#sideApproved").textContent = s.approved || 0;
    $("#sideSubmitted").textContent = s.submitted || 0;
    $("#sideReview").textContent = s.review || 0;
    $("#sideRejected").textContent = s.rejected || 0;
    $("#navJobCount").textContent = s.total || 0;
    if (state.user) {
      $("#userName").textContent = state.user.display_name || state.user.username;
      $("#userAvatar").textContent = (state.user.display_name || state.user.username || "U").charAt(0).toUpperCase();
      $("#userRole").textContent = (state.profile && state.profile.role) || "Member";
    }
  }

  // ---------- View routing ----------
  const TITLES = {
    dashboard: ["Dashboard", "Your morning review at a glance"],
    jobs: ["Jobs", "Review, score, and act on every posting"],
    pipeline: ["Pipeline", "Drag jobs through your review stages"],
    applications: ["Applications", "Tailored resumes, cover letters, and prep"],
    search: ["Search & Submit", "Find jobs and send your tailored applications"],
    analytics: ["Analytics", "Submission tracking and performance insights"],
    goals: ["Goals", "Weekly application targets, progress & streak"],
    profile: ["Profile", "Your details power the tailoring"],
  };

  function setView(view) {
    state.view = view;
    document.querySelectorAll(".nav-item").forEach((n) => n.classList.toggle("active", n.dataset.view === view));
    document.querySelectorAll(".view").forEach((v) => v.classList.add("hidden"));
    $("#view-" + view).classList.remove("hidden");
    $("#pageTitle").textContent = TITLES[view][0];
    $("#pageSubtitle").textContent = TITLES[view][1];
    renderCurrent();
  }

  function renderCurrent() {
    if (state.view === "dashboard") renderDashboard();
    else if (state.view === "jobs") renderJobs();
    else if (state.view === "pipeline") renderPipeline();
    else if (state.view === "applications") renderApplications();
    else if (state.view === "search") renderSearch();
    else if (state.view === "analytics") renderAnalytics();
    else if (state.view === "goals") renderGoals();
    else if (state.view === "profile") renderProfile();
  }

  // ---------- Dashboard ----------
  function renderDashboard() {
    const s = state.stats || {};
    const top = state.top || [];
    const el = $("#view-dashboard");
    el.innerHTML = `
      <div class="grid cols-4" style="margin-bottom:18px">
        ${statCard("Total jobs", s.total, "blue", "across all sources")}
        ${statCard("Eligible", s.eligible, "green", "ready to review")}
        ${statCard("Approved", s.approved, "violet", "materials prepared")}
        ${statCard("Submitted", s.submitted, "teal", "applications sent")}
      </div>
      <div class="grid cols-2">
        <div class="card card-pad">
          <div class="section-title">Top 10 matches <span class="muted">highest confidence</span></div>
          ${top.length ? `<div class="job-list">${top.map(jobRow).join("")}</div>` : emptyBox("No matches yet", "Click “Scan now” to fetch from Remotive & Greenhouse.")}
        </div>
        <div class="card card-pad">
          <div class="section-title">Recent scans <span class="muted">last ${state.runs.length}</span></div>
          ${state.runs.length ? `<div class="job-list">${state.runs.map(runRow).join("")}</div>` : emptyBox("No scans yet", "Run a scan to start collecting jobs.")}
        </div>
      </div>
      <div class="card card-pad" style="margin-top:18px">
        <div class="section-title">Your data <span class="muted">export or import</span></div>
        <div class="data-actions">
          <button class="btn sm" data-export="jobs">⬇ Jobs (CSV)</button>
          <button class="btn sm" data-export="jobs-json">⬇ Jobs (JSON)</button>
          <button class="btn sm" data-export="applications">⬇ Applications (CSV)</button>
          <button class="btn sm" data-export="analytics">⬇ Analytics (CSV)</button>
          <label class="btn sm" style="cursor:pointer">⬆ Import jobs (JSON)
            <input type="file" id="importFile" accept="application/json,.json" hidden />
          </label>
        </div>
        <p class="muted" style="font-size:12px;margin-top:10px">Exports download your real data. Import accepts a jobs JSON export and skips duplicates.</p>
      </div>`;
    bindJobRows(el);
    el.querySelectorAll("[data-export]").forEach((b) => b.addEventListener("click", () => doExport(b.dataset.export)));
    const imp = $("#importFile");
    if (imp) imp.addEventListener("change", () => doImport(imp));
  }

  // ---------- Export / Import (F14) ----------
  async function doExport(kind) {
    const map = {
      jobs: { url: "/api/export/jobs?format=csv", name: "jobs.csv" },
      "jobs-json": { url: "/api/export/jobs?format=json", name: "jobs.json" },
      applications: { url: "/api/export/applications?format=csv", name: "applications.csv" },
      analytics: { url: "/api/export/analytics?format=csv", name: "analytics.csv" },
    };
    const cfg = map[kind];
    if (!cfg) return;
    try {
      const res = await fetch(cfg.url, { headers: { Authorization: "Bearer " + state.token } });
      if (res.status === 401) {
        showLogin();
        throw new Error("Session expired — please sign in again.");
      }
      if (!res.ok) throw new Error("Export failed (" + res.status + ")");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = cfg.name;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      toast("Export downloaded");
    } catch (e) { toast(e.message); }
  }

  async function doImport(input) {
    const file = input.files && input.files[0];
    if (!file) return;
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      const res = await api("/api/import/jobs", { method: "POST", body: { jobs: data.jobs || data } });
      toast(`Imported ${res.imported}, skipped ${res.skipped}`);
      await loadAll();
    } catch (e) { toast("Import failed: " + e.message); }
    finally { input.value = ""; }
  }

  function statCard(label, value, color, sub) {
    return `<div class="card stat-card">
      <div class="label"><span class="dot ${color}"></span> ${esc(label)}</div>
      <div class="value">${value == null ? 0 : value}</div>
      <div class="sub">${esc(sub)}</div>
    </div>`;
  }

  function runRow(r) {
    return `<div class="card" style="padding:13px 15px">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <b style="font-size:13.5px;text-transform:capitalize">${esc(r.source)}</b>
        <span class="muted" style="font-size:12px">${timeAgo(r.started_at)}</span>
      </div>
      <div style="font-size:12.5px;color:var(--text-2);margin-top:6px">
        ${r.fetched} fetched · <span style="color:var(--green);font-weight:600">${r.eligible} eligible</span> · ${r.review} review · ${r.rejected} rejected${r.skipped ? ` · ${r.skipped} skipped (no apply link)` : ""}
      </div>
    </div>`;
  }

  // ---------- Jobs ----------
  function renderJobs() {
    const el = $("#view-jobs");
    el.innerHTML = `
      <div class="toolbar">
        <input class="search" id="jobSearch" placeholder="Search title, company, or skill…" value="${esc(state.search)}" />
        <select class="select" id="jobSort">
          <option value="confidence" ${state.sort === "confidence" ? "selected" : ""}>Sort: Confidence</option>
          <option value="score" ${state.sort === "score" ? "selected" : ""}>Sort: Fit score</option>
          <option value="company" ${state.sort === "company" ? "selected" : ""}>Sort: Company rating</option>
          <option value="date" ${state.sort === "date" ? "selected" : ""}>Sort: Newest first</option>
        </select>
        <button class="btn" id="saveFilterBtn" title="Save the current search + filter as a reusable chip">＋ Save filter</button>
      </div>
      <div class="chips" style="margin-bottom:16px">
        ${chip("all", "All", state.stats ? state.stats.total : 0)}
        ${chip("new", "Eligible", state.stats ? state.stats.eligible : 0)}
        ${chip("review", "Needs review", state.stats ? state.stats.review : 0)}
        ${chip("approved", "Approved", state.stats ? state.stats.approved : 0)}
        ${chip("rejected", "Rejected", state.stats ? state.stats.rejected : 0)}
      </div>
      ${savedFilterChips()}
      <div class="job-list" id="jobList"></div>`;

    $("#jobSearch").addEventListener("input", (e) => { state.search = e.target.value; renderJobList(); });
    $("#jobSort").addEventListener("change", (e) => { state.sort = e.target.value; renderJobList(); });
    $("#saveFilterBtn").addEventListener("click", saveCurrentFilter);
    el.querySelectorAll(".chip[data-status]").forEach((c) => c.addEventListener("click", () => { state.filter = c.dataset.status; state.search = ""; renderJobList(); }));
    el.querySelectorAll(".filter-chip[data-apply]").forEach((c) => c.addEventListener("click", () => applySavedFilter(c.dataset.apply)));
    el.querySelectorAll(".filter-chip[data-rmfilter]").forEach((c) => c.addEventListener("click", (e) => { e.stopPropagation(); removeSavedFilter(c.dataset.rmfilter); }));
    renderJobList();
  }

  // ---------- Saved filters (F10) ----------
  function savedFilterChips() {
    const filters = state.savedFilters || [];
    if (!filters.length) return "";
    return `<div class="filter-chips" style="margin-bottom:16px">
      ${filters.map((f) => `
        <span class="filter-chip ${state.activeFilter === f.id ? "active" : ""}" data-apply="${f.id}">
          ${esc(f.label)}
          <button class="filter-chip-x" data-rmfilter="${f.id}" title="Remove saved filter">×</button>
        </span>`).join("")}
    </div>`;
  }

  async function saveCurrentFilter() {
    const search = state.search.trim();
    const status = state.filter;
    if (!search && status === "all") { toast("Set a search or filter first"); return; }
    const label = search ? `“${search}”` : statusLabel(status);
    const filter = { id: Date.now(), label, search, status };
    const next = [...(state.savedFilters || []), filter];
    try {
      await api("/api/profile/filters", { method: "PUT", body: { filters: next } });
      state.savedFilters = next;
      state.activeFilter = filter.id;
      toast("Filter saved");
      renderJobs();
    } catch (e) { toast(e.message); }
  }

  function applySavedFilter(id) {
    const f = (state.savedFilters || []).find((x) => String(x.id) === String(id));
    if (!f) return;
    state.search = f.search || "";
    state.filter = f.status || "all";
    state.activeFilter = f.id;
    renderJobs();
  }

  async function removeSavedFilter(id) {
    const next = (state.savedFilters || []).filter((x) => String(x.id) !== String(id));
    try {
      await api("/api/profile/filters", { method: "PUT", body: { filters: next } });
      state.savedFilters = next;
      if (state.activeFilter === id) state.activeFilter = null;
      renderJobs();
    } catch (e) { toast(e.message); }
  }

  function chip(status, label, count) {
    return `<div class="chip ${state.filter === status ? "active" : ""}" data-status="${status}">${esc(label)} · ${count}</div>`;
  }

  function filteredJobs() {
    let list = state.jobs.slice();
    if (state.filter !== "all") list = list.filter((j) => j.status === state.filter);
    if (state.search) {
      const q = state.search.toLowerCase();
      list = list.filter((j) => {
        const skills = Array.isArray(j.skills) ? j.skills : String(j.skills || "").split(",").map((s) => s.trim()).filter(Boolean);
        return (
          (j.title || "").toLowerCase().includes(q) ||
          (j.company || "").toLowerCase().includes(q) ||
          skills.some((s) => String(s).toLowerCase().includes(q))
        );
      });
    }
    list.sort((a, b) => {
      if (state.sort === "company") return (b.company_overall || 0) - (a.company_overall || 0);
      if (state.sort === "score") return (b.score || 0) - (a.score || 0);
      if (state.sort === "date") {
        const da = a.posted_date || a.created_at || "";
        const db = b.posted_date || b.created_at || "";
        return db.localeCompare(da);
      }
      return (b.confidence || 0) - (a.confidence || 0);
    });
    return list;
  }

  function renderJobList() {
    const list = filteredJobs();
    const box = $("#jobList");
    if (!box) return;
    box.innerHTML = list.length ? list.map(jobRow).join("") : emptyBox("No jobs match", "Try a different filter or search term.");
    bindJobRows(box);
  }

  function jobRow(j) {
    const flags = (j.company_flags || []).map((f) => `<span class="tag flag">${esc(f)}</span>`).join("");
    const matched = (j.confidence_breakdown && j.confidence_breakdown.matched_skills || []).slice(0, 4)
      .map((s) => `<span class="tag skill match">${esc(s)}</span>`).join("");
    const rating = j.company_has_data
      ? `<span class="rating-mini"><span class="stars">${stars(j.company_overall)}</span> ${j.company_overall.toFixed(1)}</span>`
      : `<span class="rating-mini muted">No rating</span>`;
    const elig = j.eligibility != null ? Math.round(j.eligibility) : null;
    return `<div class="card job-card" data-id="${j.id}">
      <div class="job-main">
        <div class="job-title-row">
          <span class="job-title">${esc(j.title)}</span>
          <span class="badge ${j.status}">${statusLabel(j.status)}</span>
        </div>
        <div class="job-company">
          <b>${esc(j.company)}</b><span class="sep">·</span>${esc(j.location || "Remote")}
          <span class="sep">·</span><span class="muted">${esc(j.source)}</span>
          ${rating}
        </div>
        <div class="job-tags">${flags}${matched}</div>
      </div>
      <div class="job-side">
        <div class="confidence">
          <span class="num" style="color:${confColor(j.confidence)}">${Math.round(j.confidence)}</span>
          <span class="lbl ${confClass(j.confidence_label)}">${esc(j.confidence_label)}</span>
          <div class="conf-bar"><span style="width:${j.confidence}%;background:${confColor(j.confidence)}"></span></div>
        </div>
        ${elig != null ? `<div class="elig-mini">Eligible <b style="color:${confColor(elig)}">${elig}%</b></div>` : ""}
        ${j.materials_ready ? `<div class="materials-mini">📄 Resume + letter ready</div>` : ""}
        <label class="compare-pick" title="Select to compare">
          <input type="checkbox" data-compare="${j.id}" ${state.compare.includes(j.id) ? "checked" : ""} /> Compare
        </label>
      </div>
    </div>`;
  }


  function emptyBox(title, sub) {
    return `<div class="empty"><div class="big">📋</div><h3>${esc(title)}</h3><p>${esc(sub)}</p></div>`;
  }

  function bindJobRows(scope) {
    scope.querySelectorAll(".job-card").forEach((c) => {
      c.addEventListener("click", (e) => {
        if (e.target.closest("[data-compare]")) return; // let the checkbox handle itself
        openJob(Number(c.dataset.id));
      });
      const cb = c.querySelector("[data-compare]");
      if (cb) cb.addEventListener("change", () => {
        const id = Number(cb.dataset.compare);
        if (cb.checked) {
          if (state.compare.length >= 5) { cb.checked = false; toast("Compare up to 5 jobs"); return; }
          state.compare.push(id);
        } else {
          state.compare = state.compare.filter((x) => x !== id);
        }
        updateCompareFab();
      });
    });
  }

  // ---------- Comparison (F7) ----------
  function updateCompareFab() {
    let fab = $("#compareFab");
    if (state.compare.length >= 2) {
      if (!fab) {
        fab = document.createElement("button");
        fab.id = "compareFab";
        fab.className = "btn primary compare-fab";
        document.body.appendChild(fab);
        fab.addEventListener("click", openCompare);
      }
      fab.textContent = `Compare (${state.compare.length})`;
      fab.classList.remove("hidden");
    } else if (fab) {
      fab.remove();
    }
  }

  async function openCompare() {
    const box = $("#compareDetail");
    box.innerHTML = `<div class="loading"><span class="spinner"></span> Comparing…</div>`;
    $("#compareModal").classList.remove("hidden");
    let data;
    try { data = await api("/api/jobs/compare?ids=" + state.compare.join(",")); }
    catch (e) { box.innerHTML = emptyBox("Comparison unavailable", e.message); return; }
    const jobs = data.jobs;
    const best = data.best || {};
    const cols = jobs.map((j) => `<th>${esc(j.title)}<br><span class="muted" style="font-weight:400;font-size:11px">${esc(j.company)}</span>
      <button class="compare-remove" data-rm="${j.id}" title="Remove">×</button></th>`).join("");
    // Build rows with explicit best highlighting.
    const bestId = (key) => best[key];
    const cellCls = (j, key) => (bestId(key) === j.id ? "best" : "");
    const rows = [
      `<tr><td class="metric-name">Confidence</td>${jobs.map((j) => `<td class="${cellCls(j, "confidence")}">${Math.round(j.confidence)}</td>`).join("")}</tr>`,
      `<tr><td class="metric-name">Eligibility</td>${jobs.map((j) => `<td class="${cellCls(j, "eligibility")}">${j.eligibility != null ? Math.round(j.eligibility) + "%" : "—"}</td>`).join("")}</tr>`,
      `<tr><td class="metric-name">Salary</td>${jobs.map((j) => `<td class="${cellCls(j, "salary")}">${esc(j.salary || "—")}</td>`).join("")}</tr>`,
      `<tr><td class="metric-name">Company rating</td>${jobs.map((j) => `<td class="${cellCls(j, "company")}">${j.company_overall != null ? j.company_overall.toFixed(1) : "—"}</td>`).join("")}</tr>`,
      `<tr><td class="metric-name">Work mode</td>${jobs.map((j) => `<td>${esc(j.work_mode || "—")}</td>`).join("")}</tr>`,
      `<tr><td class="metric-name">Application</td>${jobs.map((j) => `<td>${esc(j.application_method || "—")}</td>`).join("")}</tr>`,
      `<tr><td class="metric-name">Matched skills</td>${jobs.map((j) => `<td>${(j.matched_skills || []).slice(0, 6).map((s) => `<span class="tag skill match">${esc(s)}</span>`).join(" ") || "—"}</td>`).join("")}</tr>`,
      `<tr><td class="metric-name">Missing skills</td>${jobs.map((j) => `<td class="${cellCls(j, "skills")}">${(j.missing_skills || []).slice(0, 6).map((s) => `<span class="tag skill miss">${esc(s)}</span>`).join(" ") || "—"}</td>`).join("")}</tr>`,
    ].join("");
    box.innerHTML = `
      <div class="detail-head"><div><h3>Compare jobs</h3>
        <div class="meta"><span class="muted">Green = best in column · ${jobs.length} jobs</span></div></div></div>
      <div style="overflow-x:auto">
      <table class="compare-table">
        <thead><tr><th class="metric-name"></th>${cols}</tr></thead>
        <tbody>${rows}</tbody>
      </table></div>`;
    box.querySelectorAll("[data-rm]").forEach((b) => b.addEventListener("click", () => {
      state.compare = state.compare.filter((x) => x !== Number(b.dataset.rm));
      updateCompareFab();
      if (state.compare.length >= 2) openCompare(); else closeCompare();
    }));
  }
  function closeCompare() { $("#compareModal").classList.add("hidden"); }

  // ---------- Pipeline (Kanban, F6) ----------
  const PIPELINE_LANES = [
    { key: "new", label: "Eligible" },
    { key: "review", label: "Review" },
    { key: "approved", label: "Approved" },
    { key: "rejected", label: "Rejected" },
  ];

  function renderPipeline() {
    const el = $("#view-pipeline");
    const cols = PIPELINE_LANES.map((lane) => {
      const items = state.jobs.filter((j) => j.status === lane.key)
        .sort((a, b) => (b.confidence || 0) - (a.confidence || 0));
      const cards = items.map((j) => `
        <div class="kanban-card" draggable="true" data-id="${j.id}">
          <div class="kc-title">${esc(j.title)}</div>
          <div class="kc-meta"><span>${esc(j.company)}</span><span style="color:${confColor(j.confidence)};font-weight:700">${Math.round(j.confidence)}</span></div>
          ${j.salary ? `<div class="kc-salary">${esc(j.salary)}</div>` : ""}
        </div>`).join("");
      return `<div class="kanban-col" data-lane="${lane.key}">
        <div class="kanban-col-head"><span class="dot ${lane.key === "approved" ? "green" : lane.key === "rejected" ? "red" : lane.key === "review" ? "amber" : "blue"}"></span>
          ${lane.label}<span class="count">${items.length}</span></div>
        <div class="kanban-cards" data-lane="${lane.key}">${cards || '<p class="muted" style="font-size:12px;text-align:center;padding:14px 0">Drop jobs here</p>'}</div>
      </div>`;
    }).join("");
    el.innerHTML = `<div class="kanban">${cols}</div>`;
    bindKanban(el);
  }

  function bindKanban(scope) {
    let draggedId = null;
    scope.querySelectorAll(".kanban-card").forEach((card) => {
      card.addEventListener("dragstart", () => { draggedId = Number(card.dataset.id); card.style.opacity = ".5"; });
      card.addEventListener("dragend", () => { card.style.opacity = "1"; });
      card.addEventListener("click", () => openJob(Number(card.dataset.id)));
    });
    scope.querySelectorAll(".kanban-col").forEach((col) => {
      col.addEventListener("dragover", (e) => { e.preventDefault(); col.classList.add("drag-over"); });
      col.addEventListener("dragleave", () => col.classList.remove("drag-over"));
      col.addEventListener("drop", async (e) => {
        e.preventDefault();
        col.classList.remove("drag-over");
        const lane = col.dataset.lane;
        if (draggedId == null) return;
        const job = state.jobs.find((j) => j.id === draggedId);
        if (!job || job.status === lane) { draggedId = null; return; }
        // Optimistic update.
        job.status = lane;
        renderPipeline();
        try {
          await api(`/api/jobs/${draggedId}/status`, { method: "POST", body: { status: lane } });
          toast(`Moved to ${PIPELINE_LANES.find((l) => l.key === lane).label}`);
          await loadAll();
        } catch (err) {
          toast(err.message);
          await loadAll();
        }
        draggedId = null;
      });
    });
  }

  // ---------- Job detail ----------
  async function openJob(id) {
    const detail = await api("/api/jobs/" + id);
    // Load the prefilled, editable application form for this job.
    try {
      const form = await api(`/api/jobs/${id}/application-form`);
      detail.application_form = form;
    } catch (e) { /* form is optional */ }
    // Load the resume scorecard and timeline (v2.3).
    try { detail.scorecard = await api(`/api/jobs/${id}/scorecard`); } catch (e) { /* optional */ }
    try { detail.timeline = await api(`/api/jobs/${id}/timeline`); } catch (e) { /* optional */ }
    // v2.4 — company intel (keyword gap is provided by the scorecard panel above).
    if (detail.company) {
      try { detail.companyIntel = await api(`/api/company/${encodeURIComponent(detail.company)}`); } catch (e) { /* optional */ }
    }
    $("#jobDetail").innerHTML = jobDetailHTML(detail);
    $("#jobModal").classList.remove("hidden");
    bindDetail(detail);
  }

  function jobDetailHTML(j) {
    const c = j.company_info || {};
    const cb = j.confidence_breakdown || {};
    const factors = cb.factors || [];
    const factorRows = factors.map((f) => `
      <div class="factor-row">
        <div class="factor-head"><span>${esc(f.label)}</span><span class="muted">${Math.round(f.value)}</span></div>
        <div class="bar"><span style="width:${f.value}%;background:${confColor(f.value)}"></span></div>
        <div class="factor-detail">${esc(f.detail)}</div>
      </div>`).join("");
    const reasons = (cb.reasons || []).map((r) => `<li>${esc(r)}</li>`).join("");
    const matched = (cb.matched_skills || []).map((s) => `<span class="tag skill match">✓ ${esc(s)}</span>`).join("");
    const missing = (cb.missing_skills || []).slice(0, 8).map((s) => `<span class="tag skill miss">✕ ${esc(s)}</span>`).join("");
    const mustHave = (cb.must_have_present || []).map((s) => `<span class="tag skill match">✓ ${esc(s)}</span>`).join("")
      + (cb.must_have_missing || []).map((s) => `<span class="tag skill miss">✕ ${esc(s)}</span>`).join("");

    const ratingRows = Object.entries(c.ratings || {}).map(([k, v]) => {
      const label = ({ work_life_balance: "Work-life balance", culture: "Culture", management: "Management", compensation: "Compensation", career_growth: "Career growth", environment: "Work environment" }[k]) || k;
      return `<div class="rating-row"><span class="name">${esc(label)}</span><div class="bar"><span style="width:${(v / 5) * 100}%"></span></div><span class="val">${v.toFixed(1)}</span></div>`;
    }).join("");
    const flags = (c.flags || []).map((f) => `<span class="tag flag">${esc(f)}</span>`).join("");
    const warns = (c.warnings || []).map((w) => `<span class="tag warn">⚠ ${esc(w)}</span>`).join("");
    const questions = (j.questions || []).map((q) => `<li>${esc(q)}</li>`).join("");

    const app = j.application || null;
    const clScore = app && app.personalization_score != null
      ? `<span class="cl-score ${app.personalization_score >= 80 ? "good" : app.personalization_score >= 60 ? "mid" : "low"}" title="How tailored this letter is to the job">${app.personalization_score}% tailored</span>`
      : "";
    const letter = app && app.cover_letter
      ? `<div class="panel"><h4>Cover letter ${clScore}</h4><div class="letter-box">${esc(app.cover_letter)}</div></div>`
      : "";
    const resumePdf = app && app.resume_pdf ? safeUrl(app.resume_pdf) : null;
    const resumeLink = resumePdf
      ? `<a class="btn sm" href="${esc(resumePdf)}" target="_blank" rel="noopener">⬇ Download resume PDF</a>`
      : "";
    const subPanel = submissionPanel(app, j);

    return `
      <div class="detail-head">
        <div>
          <h3>${esc(j.title)}</h3>
          <div class="meta">
            <b>${esc(j.company)}</b><span>·</span>${esc(j.location || "Remote")}
            <span>·</span><span class="muted">${esc(j.source)}</span>
            <span class="badge ${j.status}">${statusLabel(j.status)}</span>
          </div>
        </div>
        <a class="btn sm" href="${esc(safeUrl(j.url) || "#")}" target="_blank" rel="noopener">Open listing ↗</a>
      </div>
      <div class="detail-grid">
        <div class="detail-col">
          <div class="panel">
            <div class="conf-hero">
              <div class="conf-ring" style="background:${confColor(j.confidence)}22;color:${confColor(j.confidence)}">${Math.round(j.confidence)}</div>
              <div class="txt">
                <div class="lbl">${esc(j.confidence_label)}</div>
                <div class="sub">Multi-factor confidence: role fit, skill coverage, your eligibility, company quality, freshness & data completeness.</div>
              </div>
            </div>
            <div class="factor-list">${factorRows}</div>
          </div>
          <div class="panel">
            <h4>Why this score</h4>
            <ul class="reason-list">${reasons || "<li>No explanation available.</li>"}</ul>
          </div>
          <div class="panel">
            <h4>Job description</h4>
            <div class="desc-box">${esc(j.description || "No description available.")}</div>
          </div>
          ${letter}
        </div>
        <div class="detail-col">
          <div class="panel">
            <h4>Your eligibility</h4>
            <div class="elig-hero">
              <div class="conf-ring" style="background:${confColor(j.eligibility)}22;color:${confColor(j.eligibility)}">${Math.round(j.eligibility)}</div>
              <div class="txt"><div class="lbl">${esc(j.eligibility_label)}</div>
              <div class="sub">How well this role fits your location, work-mode and salary preferences.</div></div>
            </div>
          </div>
          <div class="panel">
            <h4>Skills match</h4>
            <div class="skill-group"><div class="skill-group-label">Matched</div><div class="job-tags">${matched || '<span class="muted">None</span>'}</div></div>
            <div class="skill-group"><div class="skill-group-label">Core (must-have)</div><div class="job-tags">${mustHave || '<span class="muted">None</span>'}</div></div>
            ${missing ? `<div class="skill-group"><div class="skill-group-label">Not in your profile</div><div class="job-tags">${missing}</div></div>` : ""}
          </div>
          ${scorecardPanel(j)}
          <div class="panel">
            <h4>Company rating ${c.has_data ? "" : "· no data"}</h4>
            ${c.has_data ? `
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
                <span style="font-size:24px;font-weight:800">${c.overall.toFixed(1)}</span>
                <span class="stars" style="color:var(--amber)">${stars(c.overall)}</span>
                <span class="muted" style="font-size:12px">${esc(c.remote_policy || "")} · ${esc(c.size || "")}</span>
              </div>
              ${ratingRows}
              <div class="flag-list" style="margin-top:12px">${flags}${warns}</div>
            ` : `<p class="muted" style="font-size:13px">No rating data for this company yet. Ratings are curated benchmarks for known remote employers.</p>`}
          </div>
          ${companyFactsPanel(j)}
          ${companyIntelPanel(j)}
          <div class="panel">
            <h4>Interview prep · ${(j.questions || []).length} questions</h4>
            <ol class="q-list">${questions}</ol>
          </div>
          ${timelinePanel(j)}
        </div>
      </div>
      ${formPanel(j)}
      ${subPanel}
      <div class="detail-actions">
        <button class="btn primary" id="dGen">✎ Generate resume + letter</button>
        ${resumeLink}
        <button class="btn ok" id="dApprove">✓ Approve &amp; submit</button>
        <button class="btn danger" id="dReject">✕ Reject</button>
        ${j.application && j.application.submitted_at ? `<button class="btn" id="dFollowup">✉ Follow up</button>` : ""}
      </div>
      <div class="feedback-bar" data-feedback-job="${j.id}">
        <span class="muted feedback-label">Help the app learn</span>
        <button class="btn sm ok fb-btn" data-signal="approve" title="I like this kind of job — score similar jobs higher">👍 Like</button>
        <button class="btn sm fb-btn" data-signal="select" title="Selected — strong signal, weight it heavily">⭐ Selected</button>
        <button class="btn sm danger fb-btn" data-signal="reject" title="I don't like this kind — score similar jobs lower">👎 Dislike</button>
        <span class="fb-status muted"></span>
      </div>`;
  }

  // ---------- Resume scorecard panel (F2) ----------
  function companyFactsPanel(j) {
    const f = j.company_facts;
    if (!f || !Object.keys(f).length) return "";
    const rows = [
      f.hq ? `<div class="rating-row"><span class="name">HQ</span><span class="val">${esc(f.hq)}</span></div>` : "",
      f.founded ? `<div class="rating-row"><span class="name">Founded</span><span class="val">${esc(f.founded)}</span></div>` : "",
      f.employees ? `<div class="rating-row"><span class="name">Employees</span><span class="val">${Number(f.employees).toLocaleString()}</span></div>` : "",
      f.industry ? `<div class="rating-row"><span class="name">Industry</span><span class="val">${esc(f.industry)}</span></div>` : "",
    ].filter(Boolean).join("");
    return `
      <div class="panel">
        <h4>Company facts <span class="muted">Wikidata</span></h4>
        ${rows || '<p class="muted" style="font-size:13px">No facts found.</p>'}
      </div>`;
  }

  // ---------- Company intel panel (v2.4) ----------
  function companyIntelPanel(j) {
    const ci = j.companyIntel;
    if (!ci || !ci.job_count) return "";
    const info = ci.company_info || {};
    const ratingRows = Object.entries(info.ratings || {}).map(([k, v]) => {
      const label = ({ work_life_balance: "Work-life balance", culture: "Culture", management: "Management", compensation: "Compensation", career_growth: "Career growth", environment: "Work environment" }[k]) || k;
      return `<div class="rating-row"><span class="name">${esc(label)}</span><div class="bar"><span style="width:${(v / 5) * 100}%"></span></div><span class="val">${v.toFixed(1)}</span></div>`;
    }).join("");
    const srcRows = Object.entries(ci.sources || {}).map(([name, n]) =>
      `<div class="rating-row"><span class="name">${esc(name)}</span><span class="val">${n}</span></div>`).join("");
    const stageRows = Object.entries(ci.application_stages || {}).map(([stage, n]) =>
      `<div class="rating-row"><span class="name">${esc(statusLabel(stage))}</span><span class="val">${n}</span></div>`).join("");
    const sal = ci.salary_range;
    const salRow = sal
      ? `<div class="rating-row"><span class="name">Salary range</span><span class="val">${sal.min}–${sal.max}k</span></div>`
      : "";
    const jobs = (ci.jobs || []).slice(0, 5).map((jj) =>
      `<div class="rating-row"><span class="name" style="width:auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(jj.title)}</span><span class="muted" style="font-size:11px">${esc(jj.source || "")}</span></div>`).join("");
    return `
      <div class="panel">
        <div style="display:flex;align-items:center;justify-content:space-between">
          <h4 style="margin:0">Company intel</h4>
          <span class="muted" style="font-size:11px">${ci.job_count} job${ci.job_count === 1 ? "" : "s"}</span>
        </div>
        ${info.overall != null ? `<div style="display:flex;align-items:center;gap:8px;margin:12px 0">
          <span style="font-size:26px;font-weight:800">${info.overall.toFixed(1)}</span>
          <span class="stars" style="color:var(--amber)">${stars(info.overall)}</span>
          <span class="muted" style="font-size:12px">${esc(info.remote_policy || "")} · ${esc(info.size || "")}</span>
        </div>` : ""}
        ${salRow}
        ${ratingRows}
        ${srcRows ? `<div class="skill-group" style="margin-top:12px"><div class="skill-group-label">Jobs by source</div>${srcRows}</div>` : ""}
        ${stageRows ? `<div class="skill-group" style="margin-top:12px"><div class="skill-group-label">Application stages</div>${stageRows}</div>` : ""}
        ${jobs ? `<div class="skill-group" style="margin-top:12px"><div class="skill-group-label">Your jobs</div>${jobs}</div>` : ""}
      </div>`;
  }

  function scorecardPanel(j) {
    const sc = j.scorecard;
    if (!sc) return "";
    const matched = (sc.matched_skills || []).map((s) =>
      `<span class="tag skill ${s.core ? "match" : ""}">${s.core ? "★ " : ""}${esc(s.skill)}</span>`).join("");
    const gap = (sc.resume_gap || []).map((s) => `<span class="tag skill miss">${esc(s)}</span>`).join("");
    const sugg = (sc.suggestions || []).map((s) => `<li>${esc(s)}</li>`).join("");
    return `
      <div class="panel">
        <h4>Resume scorecard</h4>
        <div class="scorecard-coverage">
          <div class="conf-ring" style="background:${confColor(sc.coverage_pct)}22;color:${confColor(sc.coverage_pct)}">${Math.round(sc.coverage_pct)}</div>
          <div class="txt"><div class="lbl">Skill coverage</div>
          <div class="sub">How much of this job's skill set your profile + resume cover.</div></div>
        </div>
        <div class="skill-group"><div class="skill-group-label">Matched</div><div class="job-tags">${matched || '<span class="muted">None</span>'}</div></div>
        ${gap ? `<div class="skill-group"><div class="skill-group-label">Resume gap — add these</div><div class="job-tags">${gap}</div></div>` : ""}
        ${sugg ? `<div class="skill-group"><div class="skill-group-label">Suggestions</div><ul class="suggestion-list">${sugg}</ul></div>` : ""}
      </div>`;
  }

  // ---------- Timeline panel (F8) ----------
  function timelinePanel(j) {
    const tl = j.timeline;
    if (!tl || !tl.events || !tl.events.length) return "";
    const items = tl.events.map((e) => `
      <div class="tl-item">
        <div class="tl-label">${esc(e.label)}</div>
        <div class="tl-time">${timeAgo(e.at)}</div>
      </div>`).join("");
    return `<div class="panel"><h4>Application timeline</h4><div class="timeline">${items}</div></div>`;
  }

  function submissionPanel(app, j) {
    if (!app) return "";
    const status = app.application_status || app.submission_status || app.status;
    const icon = { submitted: "✅", ready: "📦", failed: "⚠️", submitting: "⏳" }[status] || "📄";
    const cls = { submitted: "ok", ready: "info", failed: "warn", submitting: "info" }[status] || "info";
    const applyUrl = app.submission_url ? safeUrl(app.submission_url) : null;
    const link = applyUrl
      ? `<a class="btn sm" href="${esc(applyUrl)}" target="_blank" rel="noopener">Open apply link ↗</a>`
      : "";
    const shot = app.screenshot
      ? `<a class="btn sm" href="${esc(app.screenshot)}" target="_blank" rel="noopener">Proof screenshot 📸</a>`
      : "";
    const when = app.submitted_at ? ` · ${timeAgo(app.submitted_at)}` : "";
    return `<div class="panel sub-panel ${cls}">
      <div class="sub-head"><span class="sub-icon">${icon}</span>
        <div><b>Application status: ${esc(statusLabel(status))}</b>${when}
        <div class="sub-msg">${esc(app.submission_message || "")}</div></div>
      </div>
      ${link}
      ${shot}
    </div>`;
  }

  function statusLabel(s) {
    return { new: "Eligible", review: "Review", approved: "Approved", rejected: "Rejected",
             submitted: "Submitted", ready: "Ready to submit", failed: "Failed", submitting: "Submitting" }[s] || s;
  }

  // ---------- Application form (prefilled, editable) ----------
  function formField(label, key, value, opts = {}) {
    const val = esc(value == null ? "" : value);
    const ph = opts.placeholder ? ` placeholder="${esc(opts.placeholder)}"` : "";
    const type = opts.type || "text";
    return `<label class="field">${label}<input data-af="${key}" type="${type}" value="${val}"${ph} /></label>`;
  }
  function formPanel(j) {
    const f = j.application_form || {};
    const saved = f.saved ? `<span class="tag ok">Your edits saved</span>` : `<span class="tag info">Prefilled from your profile</span>`;
    const comp = f.completeness;
    const compBar = comp ? `
      <div class="completeness">
        <div class="completeness-bar"><span style="width:${comp.pct}%;background:${comp.pct >= 100 ? "var(--green)" : comp.pct >= 50 ? "var(--amber)" : "var(--red)"}"></span></div>
        <div class="completeness-hint ${comp.pct < 100 ? "warn" : ""}">
          ${comp.pct >= 100 ? "All required fields filled — ready to submit." : `Required fields: ${comp.filled}/${comp.total} · missing ${comp.missing_required.map(esc).join(", ")}`}
        </div>
      </div>` : "";
    return `
      <div class="panel form-panel">
        <div class="form-head">
          <h4>Application form · ${esc(j.title)} at ${esc(j.company)}</h4>
          ${saved}
        </div>
        ${compBar}
        <p class="muted form-note">These fields are prefilled from your profile. Edit anything, then save — your tailored resume and cover letter stay in sync.</p>
        <div class="profile-grid">
          ${formField("Full name", "name", f.name, { placeholder: "Your name" })}
          ${formField("Email", "email", f.email, { type: "email" })}
          ${formField("Phone", "phone", f.phone)}
          ${formField("LinkedIn", "linkedin", f.linkedin)}
          ${formField("Website / portfolio", "website", f.website)}
          ${formField("GitHub", "github", f.github)}
          ${formField("Current location", "current_location", f.current_location)}
          ${formField("Timezone", "timezone", f.timezone)}
          ${formField("Notice period", "notice_period", f.notice_period)}
          ${formField("Expected salary", "expected_salary", f.expected_salary)}
          ${formField("Work authorization", "work_authorization", f.work_authorization)}
          ${formField("Visa status", "visa_status", f.visa_status)}
          ${formField("Availability", "availability", f.availability)}
          ${formField("Preferred work mode", "preferred_work_mode", f.preferred_work_mode)}
          ${formField("Years of experience", "years_experience", f.years_experience, { type: "number" })}
          ${formField("Languages", "languages", f.languages)}
          ${formField("Certifications", "certifications", f.certifications)}
        </div>
        <label class="field full">Cover letter<textarea id="af_cover" rows="7">${esc(f.cover_letter || "")}</textarea></label>
        ${variantSelectHTML()}
        <div class="save-row">
          <button class="btn primary" id="afSave">💾 Save application form</button>
          <span class="save-msg hidden" id="afMsg">Saved ✓</span>
        </div>
      </div>`;
  }

  // ---------- Resume variants (F12) ----------
  function variantSelectHTML() {
    const variants = state.resumeVariants || [];
    if (!variants.length) return "";
    const opts = variants.map((v) =>
      `<option value="${esc(v.id)}">${esc(v.label || "Variant")}</option>`).join("");
    return `<label class="field full">Resume variant <span class="muted">— used when generating the resume</span>
      <select id="af_variant"><option value="">Default (full profile)</option>${opts}</select></label>`;
  }

  function bindDetail(j) {
    const afSave = $("#afSave");
    if (afSave) {
      afSave.addEventListener("click", async () => {
        const body = {};
        document.querySelectorAll("[data-af]").forEach((inp) => {
          let v = inp.value;
          if (inp.dataset.af === "years_experience") v = v === "" ? null : Number(v);
          body[inp.dataset.af] = v;
        });
        body.cover_letter = $("#af_cover").value;
        afSave.disabled = true; afSave.innerHTML = '<span class="spinner"></span> Saving…';
        try {
          await api(`/api/jobs/${j.id}/application-form`, { method: "PUT", body });
          const m = $("#afMsg"); m.classList.remove("hidden"); setTimeout(() => m.classList.add("hidden"), 2000);
          toast("Application form saved");
        } catch (e) { toast(e.message); }
        finally { afSave.disabled = false; afSave.textContent = "💾 Save application form"; }
      });
    }
    $("#dGen").addEventListener("click", async () => {
      const btn = $("#dGen");
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Generating…';
      const vSel = $("#af_variant");
      const variant = vSel && vSel.value ? `?variant=${encodeURIComponent(vSel.value)}` : "";
      try {
        await api(`/api/jobs/${j.id}/generate${variant}`, { method: "POST" });
        toast("Resume + cover letter generated");
        openJob(j.id);
      } catch (e) { toast(e.message); btn.disabled = false; btn.textContent = "✎ Generate resume + letter"; }
    });
    $("#dApprove").addEventListener("click", async () => {
      const btn = $("#dApprove");
      btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Submitting…';
      try {
        const res = await api(`/api/jobs/${j.id}/approve`, { method: "POST" });
        const sub = res.submission || {};
        toast(sub.submission_status === "submitted" ? "Approved & submitted" : "Approved — package ready");
        closeJob(); await loadAll();
      } catch (e) { toast(e.message); btn.disabled = false; btn.textContent = "✓ Approve & submit"; }
    });
    $("#dReject").addEventListener("click", async () => {
      await api(`/api/jobs/${j.id}/reject`, { method: "POST" });
      toast("Rejected");
      closeJob(); await loadAll();
    });
    const fu = $("#dFollowup");
    if (fu) fu.addEventListener("click", () => openFollowup(j.id));

    // Learning loop feedback buttons.
    const fbBar = document.querySelector(`.feedback-bar[data-feedback-job="${j.id}"]`);
    if (fbBar) {
      const statusEl = fbBar.querySelector(".fb-status");
      fbBar.querySelectorAll(".fb-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          const signal = btn.dataset.signal;
          const original = btn.textContent;
          btn.disabled = true;
          btn.innerHTML = '<span class="spinner"></span>';
          try {
            const res = await api(`/api/jobs/${j.id}/feedback`, {
              method: "POST",
              body: { signal, source: "manual" },
            });
            // Reflect the learning contribution on the hero confidence.
            const ring = fbBar.closest(".modal-card").querySelector(".conf-ring .num, .conf-ring");
            toast(`Learned from “${signal}” — ${res.learning.approved} liked · ${res.learning.rejected} disliked`);
            // Reopen to reflect updated score.
            await openJob(j.id);
            await loadAll();
          } catch (e) {
            toast(e.message);
            btn.disabled = false; btn.textContent = original;
          }
        });
      });
    }
  }

  function closeJob() { $("#jobModal").classList.add("hidden"); }

  // ---------- Follow-up email (F9) ----------
  async function openFollowup(jobId) {
    const box = $("#followupDetail");
    box.innerHTML = `<div class="loading"><span class="spinner"></span> Drafting…</div>`;
    $("#followupModal").classList.remove("hidden");
    let f;
    try { f = await api(`/api/jobs/${jobId}/followup`); }
    catch (e) { box.innerHTML = emptyBox("Unavailable", e.message); return; }
    box.innerHTML = `
      <div class="detail-head"><div><h3>Follow-up email</h3>
        <div class="meta"><span class="muted">Sent ${f.days_since} day${f.days_since === 1 ? "" : "s"} ago · ready to copy</span></div></div></div>
      <label class="field">Subject<input id="fuSubject" value="${esc(f.subject)}" /></label>
      <label class="field">Message<textarea id="fuBody" rows="12">${esc(f.body)}</textarea></label>
      <div class="save-row">
        <button class="btn primary" id="fuCopy">⧉ Copy to clipboard</button>
        <span class="save-msg hidden" id="fuMsg">Copied ✓</span>
      </div>`;
    $("#fuCopy").addEventListener("click", async () => {
      const text = `Subject: ${$("#fuSubject").value}\n\n${$("#fuBody").value}`;
      try { await navigator.clipboard.writeText(text); }
      catch (e) {
        const ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        document.execCommand("copy"); ta.remove();
      }
      const m = $("#fuMsg"); m.classList.remove("hidden"); setTimeout(() => m.classList.add("hidden"), 2000);
    });
  }
  function closeFollowup() { $("#followupModal").classList.add("hidden"); }

  // ---------- Applications ----------
  function renderApplications() {
    const el = $("#view-applications");
    let apps = state.jobs.filter((j) => j.status === "approved" || j.status === "new" || j.status === "review");
    // Sort by submission date (newest first), then last activity, then start date.
    apps.sort((a, b) => {
      const da = a.app_submitted || a.app_last || a.app_start || "";
      const db = b.app_submitted || b.app_last || b.app_start || "";
      return db.localeCompare(da);
    });
    el.innerHTML = `
      <div class="card">
        ${apps.length ? apps.map((j) => {
          const app = j.application || {};
          const stage = app.application_status || app.submission_status || "draft";
          const posted = j.posted_date ? new Date(j.posted_date).toLocaleDateString() : "—";
          const last = j.app_last ? new Date(j.app_last).toLocaleDateString() : "—";
          const submitted = j.app_submitted ? new Date(j.app_submitted).toLocaleDateString() : "—";
          return `
          <div class="app-row" data-id="${j.id}">
            <div>
              <div class="title">${esc(j.title)}</div>
              <div class="sub">${esc(j.company)} · ${esc(j.location || "Remote")}</div>
              <div class="app-dates">
                <span class="app-date" title="When this job was posted">🗂️ Posted ${esc(posted)}</span>
                <span class="app-date updated" title="Last time anything changed on this application">🕐 Updated ${esc(last)}</span>
                <span class="app-date ${j.app_submitted ? 'submitted' : ''}" title="When you submitted this application">✅ Submitted ${esc(submitted)}</span>
              </div>
            </div>
            <div class="confidence" style="align-items:center">
              <span class="num" style="color:${confColor(j.confidence)}">${Math.round(j.confidence)}</span>
              <span class="lbl ${confClass(j.confidence_label)}">${esc(j.confidence_label)}</span>
            </div>
            <div class="app-stage">
              <select class="select stage-select" data-stage="${j.id}">
                ${stageOptions(stage)}
              </select>
            </div>
            <div style="display:flex;gap:8px">
              <button class="btn sm" data-act="open">Open</button>
              <button class="btn sm primary" data-act="gen">Generate</button>
            </div>
          </div>`;
        }).join("") : emptyBox("No applications yet", "Approve a job or generate materials to see them here.")}
      </div>`;
    el.querySelectorAll(".app-row").forEach((row) => {
      const id = Number(row.dataset.id);
      row.querySelector('[data-act="open"]').addEventListener("click", () => openJob(id));
      row.querySelector('[data-act="gen"]').addEventListener("click", async (e) => {
        e.stopPropagation();
        const btn = e.currentTarget; btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
        try { await api(`/api/jobs/${id}/generate`, { method: "POST" }); toast("Generated"); await loadAll(); }
        catch (ex) { toast(ex.message); btn.disabled = false; btn.textContent = "Generate"; }
      });
      const sel = row.querySelector(".stage-select");
      if (sel) {
        sel.addEventListener("change", async () => {
          const original = sel.innerHTML;
          sel.disabled = true;
          try {
            await api(`/api/jobs/${id}/application-status`, { method: "POST", body: { status: sel.value } });
            toast(`Application moved to "${statusLabel(sel.value)}"`);
            await loadAll();
          } catch (ex) {
            toast(ex.message);
            sel.innerHTML = original;
          } finally {
            sel.disabled = false;
          }
        });
      }
    });
  }

  // Options for the manual application-stage selector.
  function stageOptions(current) {
    const stages = ["draft", "ready", "submitting", "submitted", "failed"];
    return stages.map((s) => `<option value="${s}" ${s === current ? "selected" : ""}>${statusLabel(s)}</option>`).join("");
  }

  // ---------- Search & Submit (F19) ----------
  async function renderSearch() {
    const el = $("#view-search");
    const insights = state.learning || {};
    el.innerHTML = `
      <div class="card card-pad">
        <div class="section-title">Search &amp; submit applications</div>
        <p class="muted" style="font-size:13px;margin-bottom:14px">
          Search every job you've collected, pick the ones you want, and submit your
          tailored application package. Each job with a direct apply link opens the
          employer's application page; others are marked ready to submit.
        </p>
        <div class="toolbar">
          <input class="search" id="searchBox" placeholder="Search title, company, or skill…" value="${esc(state.search)}" />
          <select class="select" id="searchStatus">
            <option value="all" ${state.filter === "all" ? "selected" : ""}>All statuses</option>
            <option value="new" ${state.filter === "new" ? "selected" : ""}>Eligible</option>
            <option value="review" ${state.filter === "review" ? "selected" : ""}>Needs review</option>
            <option value="approved" ${state.filter === "approved" ? "selected" : ""}>Approved</option>
            <option value="rejected" ${state.filter === "rejected" ? "selected" : ""}>Rejected</option>
          </select>
          <select class="select" id="searchSort">
            <option value="confidence" ${state.sort === "confidence" ? "selected" : ""}>Confidence</option>
            <option value="score" ${state.sort === "score" ? "selected" : ""}>Fit score</option>
            <option value="company" ${state.sort === "company" ? "selected" : ""}>Company rating</option>
          </select>
        </div>
        <div class="job-list" id="searchList"></div>
      </div>
      <div class="card card-pad" style="margin-top:18px">
        <div class="section-title">What the app has learned <span class="muted">from your feedback</span></div>
        ${learningInsightsHTML(insights)}
      </div>`;

    const box = $("#searchBox");
    if (box) box.addEventListener("input", (e) => { state.search = e.target.value; renderSearchList(); });
    const st = $("#searchStatus");
    if (st) st.addEventListener("change", (e) => { state.filter = e.target.value; renderSearchList(); });
    const so = $("#searchSort");
    if (so) so.addEventListener("change", (e) => { state.sort = e.target.value; renderSearchList(); });
    renderSearchList();
  }

  function renderSearchList() {
    const list = filteredJobs();
    const box = $("#searchList");
    if (!box) return;
    box.innerHTML = list.length ? list.map(searchJobRow).join("") : emptyBox("No jobs match", "Run a scan to collect jobs, then search and submit here.");
    bindSearchRows(box);
  }

  function searchJobRow(j) {
    const elig = j.eligibility != null ? Math.round(j.eligibility) : null;
    const applyable = !!j.application_url;
    return `<div class="card job-card" data-id="${j.id}">
      <div class="job-main">
        <div class="job-title-row">
          <span class="job-title">${esc(j.title)}</span>
          <span class="badge ${j.status}">${statusLabel(j.status)}</span>
        </div>
        <div class="job-company"><b>${esc(j.company)}</b><span class="sep">·</span>${esc(j.location || "Remote")}
          <span class="sep">·</span><span class="muted">${esc(j.source)}</span></div>
        <div class="job-tags">${(j.confidence_breakdown && j.confidence_breakdown.matched_skills || []).slice(0, 4).map((s) => `<span class="tag skill match">${esc(s)}</span>`).join("")}</div>
      </div>
      <div class="job-side">
        <div class="confidence">
          <span class="num" style="color:${confColor(j.confidence)}">${Math.round(j.confidence)}</span>
          <span class="lbl ${confClass(j.confidence_label)}">${esc(j.confidence_label)}</span>
        </div>
        ${elig != null ? `<div class="elig-mini">Eligible <b style="color:${confColor(elig)}">${elig}%</b></div>` : ""}
        <div class="submit-actions">
          <button class="btn sm primary" data-submit="${j.id}">Submit application</button>
          <span class="muted submit-hint">${applyable ? "Direct apply link" : "Ready to submit"}</span>
        </div>
      </div>
    </div>`;
  }

  function bindSearchRows(scope) {
    scope.querySelectorAll(".job-card").forEach((c) => {
      c.addEventListener("click", (e) => {
        const submitBtn = e.target.closest("[data-submit]");
        if (submitBtn) { e.stopPropagation(); submitApplication(Number(submitBtn.dataset.submit)); }
        else openJob(Number(c.dataset.id));
      });
    });
  }

  async function submitApplication(jobId) {
    const btn = document.querySelector(`[data-submit="${jobId}"]`);
    if (!btn) return;
    const original = btn.textContent;
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
    try {
      const res = await api(`/api/jobs/${jobId}/submit`, { method: "POST" });
      const sub = res.submission || {};
      const applyUrl = sub.submission_url ? safeUrl(sub.submission_url) : null;
      if (applyUrl) {
        window.open(applyUrl, "_blank", "noopener");
      }
      toast(sub.submission_status === "submitted" ? "Application submitted — link opened" : "Marked ready to submit");
      await loadAll();
      renderSearch();
    } catch (e) {
      toast(e.message);
      btn.disabled = false; btn.textContent = original;
    }
  }

  function learningInsightsHTML(l) {
    if (!l.has_data) {
      return `<p class="muted" style="font-size:13px">No feedback yet. Tap 👍 / ⭐ / 👎 on any job to teach the app what you like — scores adapt automatically on your next scan.</p>`;
    }
    const rows = [
      ["Approved", l.approved, "var(--green)"],
      ["Selected", l.selected, "var(--violet)"],
      ["Disliked", l.rejected, "var(--red)"],
    ];
    const rowsHtml = rows.map(([label, val, color]) =>
      `<div class="rating-row"><span class="name">${esc(label)}</span><span class="val" style="color:${color};font-weight:700">${val}</span></div>`).join("");
    const skills = (l.top_skills || []).length ? `<div class="skill-group" style="margin-top:10px"><div class="skill-group-label">Skills you like</div><div class="job-tags">${l.top_skills.map((s) => `<span class="tag skill match">${esc(s)}</span>`).join("")}</div></div>` : "";
    const companies = (l.top_companies || []).length ? `<div class="skill-group" style="margin-top:10px"><div class="skill-group-label">Companies you like</div><div class="job-tags">${l.top_companies.map((c) => `<span class="tag skill match">${esc(c)}</span>`).join("")}</div></div>` : "";
    const sources = (l.top_sources || []).length ? `<div class="skill-group" style="margin-top:10px"><div class="skill-group-label">Sources you like</div><div class="job-tags">${l.top_sources.map((s) => `<span class="tag skill match">${esc(s)}</span>`).join("")}</div></div>` : "";
    const modes = (l.top_work_modes || []).length ? `<div class="skill-group" style="margin-top:10px"><div class="skill-group-label">Work modes you like</div><div class="job-tags">${l.top_work_modes.map((m) => `<span class="tag skill match">${esc(m)}</span>`).join("")}</div></div>` : "";
    return `<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
        <span class="badge approved" style="font-size:12px">Learning active</span>
        <span class="muted" style="font-size:12.5px">fit ×${l.fit_mult} · confidence ×${l.confidence_mult}</span>
      </div>
      ${rowsHtml}${skills}${companies}${sources}${modes}`;
  }

  // ---------- Analytics ----------
  async function renderAnalytics() {
    const el = $("#view-analytics");
    el.innerHTML = `<div class="loading"><span class="spinner"></span> Loading analytics…</div>`;
    let a;
    try { a = await api("/api/analytics"); } catch (e) { el.innerHTML = emptyBox("Analytics unavailable", e.message); return; }
    state.analytics = a;

    const app = a.applications || {};
    const submitted = app.submitted || 0, ready = app.ready || 0, draft = app.draft || 0;
    // Manual stages (submitting/failed) may add keys beyond the big three.
    const other = Math.max(0, Object.values(app).reduce((s, v) => s + (Number(v) || 0), 0) - (submitted + ready + draft));
    const totalApps = submitted + ready + draft + other;
    const conv = totalApps ? Math.round((submitted / totalApps) * 100) : 0;

    el.innerHTML = `
      <div class="grid cols-4" style="margin-bottom:18px">
        ${statCard("Total jobs", a.total, "blue", "in your pipeline")}
        ${statCard("Submitted", submitted, "teal", "applications sent")}
        ${statCard("Ready to submit", ready, "violet", "package prepared")}
        ${statCard("Avg confidence", a.avg_confidence, "green", "across all jobs")}
      </div>
      <div class="grid cols-2">
        <div class="card card-pad">
          <div class="section-title">Application pipeline</div>
          ${donutChart([
                        { label: "Submitted", value: submitted, color: "var(--teal)" },
                        { label: "Ready", value: ready, color: "var(--violet)" },
                        { label: "Draft", value: draft, color: "var(--border)" },
                        ...(other ? [{ label: "In progress", value: other, color: "var(--amber)" }] : []),
                      ])}
          <div class="legend">
            <span><i style="background:var(--teal)"></i>Submitted ${submitted}</span>
            <span><i style="background:var(--violet)"></i>Ready ${ready}</span>
            <span><i style="background:var(--border)"></i>Draft ${draft}</span>
            ${other ? `<span><i style="background:var(--amber)"></i>In progress ${other}</span>` : ""}
            <span class="muted">Conversion ${conv}%</span>
          </div>
        </div>
        <div class="card card-pad">
          <div class="section-title">Submissions · last 14 days</div>
          ${barChart(a.submissions_by_day || {}, { label: (k) => k.slice(5), labelEvery: 2 })}
        </div>
      </div>
      <div class="grid cols-2" style="margin-top:18px">
        <div class="card card-pad">
          <div class="section-title">Confidence distribution</div>
          ${barChart(a.confidence_buckets || {}, { max: Math.max(1, ...Object.values(a.confidence_buckets || {})) })}
        </div>
        <div class="card card-pad">
          <div class="section-title">Jobs by source</div>
          ${hbarChart(a.by_source || {})}
        </div>
      </div>
      <div class="grid cols-2" style="margin-top:18px">
        <div class="card card-pad">
          <div class="section-title">Jobs by work mode</div>
          ${hbarChart(a.by_work_mode || {})}
        </div>
        <div class="card card-pad">
          <div class="section-title">Top companies</div>
          ${hbarChart((a.top_companies || []).reduce((o, c) => (o[c.company] = c.count, o), {}))}
        </div>
      </div>
      <div class="grid cols-2" style="margin-top:18px">
        <div class="card card-pad" id="salaryCard">
          <div class="section-title">Salary insights <span class="muted">market vs. you</span></div>
          <div class="loading"><span class="spinner"></span> Loading…</div>
        </div>
        <div class="card card-pad" id="skillsCard">
          <div class="section-title">Skill demand <span class="muted">what the market wants</span></div>
          <div class="loading"><span class="spinner"></span> Loading…</div>
        </div>
      </div>
      <div class="card card-pad" id="sourcesCard" style="margin-top:18px">
        <div class="section-title">Source health <span class="muted">scan reliability</span></div>
        <div class="loading"><span class="spinner"></span> Loading…</div>
      </div>
      <div class="card card-pad" id="trendCard" style="margin-top:18px">
        <div class="section-title">Fit trend <span class="muted">how your match quality is moving</span></div>
        <div class="loading"><span class="spinner"></span> Loading…</div>
      </div>
      <div class="card card-pad" id="negotiationCard" style="margin-top:18px">
        <div class="section-title">Salary negotiation assistant <span class="muted">market data → your offer</span></div>
        <div class="loading"><span class="spinner"></span> Loading…</div>
      </div>
      <div class="grid cols-2" style="margin-top:18px">
        <div class="card card-pad" id="schedulerCard">
          <div class="section-title">Auto-scan scheduler <span class="muted">background</span></div>
          <div class="loading"><span class="spinner"></span> Loading…</div>
        </div>
        <div class="card card-pad" id="registryCard">
          <div class="section-title">Source registry <span class="muted">enabled feeds</span></div>
          <div class="loading"><span class="spinner"></span> Loading…</div>
        </div>
      </div>`;

    await Promise.all([renderSalary(), renderSkills(), renderSources(), renderTrend(), renderScheduler(), renderRegistry(), renderNegotiation()]);
  }

  // ---------- Salary negotiation assistant (v2.4) ----------
  async function renderNegotiation() {
    const card = $("#negotiationCard");
    let n;
    try { n = await api("/api/negotiation"); } catch (e) { card.innerHTML = `<div class="section-title">Salary negotiation assistant</div>` + emptyBox("Unavailable", e.message); return; }
    const rec = n.recommendation || {};
    const floor = rec.floor ?? 0, target = rec.target ?? 0, stretch = rec.stretch ?? 0;
    const market = n.market || {};
    const p25 = market.p25 ?? 0, p50 = market.p50 ?? 0, p75 = market.p75 ?? 0;
    const offer = n.offer ?? 0;

    // Build a visual range bar: floor..stretch, with offer + market markers.
    const lo = Math.max(0, Math.min(floor, target, stretch, p25, p50, p75, offer));
    const hi = Math.max(floor, target, stretch, p25, p50, p75, offer) || 1;
    const span = (hi - lo) || 1;
    const pos = (v) => Math.max(0, Math.min(100, ((v - lo) / span) * 100));
    const fmt = (v) => v ? `$${v}k` : "—";

    const markers = [
      { at: pos(floor), label: "Floor", color: "var(--primary)" },
      { at: pos(target), label: "Target", color: "var(--teal)" },
      { at: pos(stretch), label: "Stretch", color: "var(--violet)" },
      { at: pos(offer), label: "Your offer", color: "var(--amber)" },
    ].map((m) => `<div class="neg-marker" style="left:${m.at}%;border-color:${m.color}"><span class="neg-dot" style="background:${m.color}"></span><span class="neg-lbl" style="color:${m.color}">${esc(m.label)}</span></div>`).join("");

    const points = (n.talking_points || []).map((p) => `<li>${esc(p)}</li>`).join("");

    card.innerHTML = `
      <div class="section-title">Salary negotiation assistant <span class="muted">market data → your offer</span></div>
      <div class="neg-grid">
        <div class="neg-input">
          <label class="neg-lbl-inline">Your offer (k)</label>
          <input id="negOffer" type="number" min="0" value="${offer}" style="flex:1" />
          <button class="btn primary sm" id="negRecalc">Recalculate</button>
        </div>
        <div class="neg-range">
          <div class="neg-bar">
            <div class="neg-track"><span class="neg-fill" style="background:linear-gradient(90deg,var(--primary),var(--teal),var(--violet))"></span></div>
            ${markers}
          </div>
          <div class="neg-values">
            <div><span class="neg-lbl-inline">Floor</span> <b>${fmt(floor)}</b></div>
            <div><span class="neg-lbl-inline">Target</span> <b>${fmt(target)}</b></div>
            <div><span class="neg-lbl-inline">Stretch</span> <b>${fmt(stretch)}</b></div>
          </div>
        </div>
      </div>
      <div class="neg-market">
        <div class="neg-mkt-item"><span class="neg-lbl-inline">Market p25</span> <b>${fmt(p25)}</b></div>
        <div class="neg-mkt-item"><span class="neg-lbl-inline">Market p50</span> <b>${fmt(p50)}</b></div>
        <div class="neg-mkt-item"><span class="neg-lbl-inline">Market p75</span> <b>${fmt(p75)}</b></div>
      </div>
      ${n.talking_points && n.talking_points.length ? `
        <div class="skill-group" style="margin-top:14px"><div class="skill-group-label">Talking points</div><ul class="suggestion-list">${points}</ul></div>` : ""}
      <p class="muted" style="font-size:12px;margin-top:12px">Recommendation is derived from market data across your scanned jobs, your expected salary, and your experience. Adjust your offer above to recalculate.</p>`;

    const rc = $("#negRecalc");
    if (rc) rc.addEventListener("click", async () => {
      const val = Number($("#negOffer").value) || 0;
      try { await api("/api/negotiation", { method: "PUT", body: { offer: val } }); renderNegotiation(); } catch (e) { toast(e.message); }
    });
  }

  // ---------- Analytics: scheduler + registry (F17/F15) ----------
  async function renderScheduler() {
    const card = $("#schedulerCard");
    let s;
    try { s = await api("/api/scheduler"); } catch (e) { card.innerHTML = `<div class="section-title">Auto-scan scheduler</div>` + emptyBox("Unavailable", e.message); return; }
    const on = s.running;
    card.innerHTML = `
      <div class="section-title">Auto-scan scheduler <span class="muted">background</span></div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
        <span class="badge ${on ? "approved" : "rejected"}" style="font-size:12px">${on ? "Running" : "Off"}</span>
        <span class="muted" style="font-size:13px">every ${s.interval_hours}h</span>
      </div>
      <div class="rating-row"><span class="name">Enabled in config</span><span class="val">${s.enabled ? "yes" : "no"}</span></div>
      <div class="rating-row"><span class="name">Next run</span><span class="val">${s.next_run ? new Date(s.next_run).toLocaleString() : "—"}</span></div>
      <p class="muted" style="font-size:12px;margin-top:10px">Set <code>scheduler.enabled: true</code> in <code>config.yaml</code> to run scans automatically while the app is open.</p>`;
  }

  async function renderRegistry() {
    const card = $("#registryCard");
    let r;
    try { r = await api("/api/sources"); } catch (e) { card.innerHTML = `<div class="section-title">Source registry</div>` + emptyBox("Unavailable", e.message); return; }
    const entries = Object.entries(r.sources || {}).filter(([k]) => k !== "_comment");
    const rows = entries.map(([name, cfg]) => {
      const on = cfg && cfg.enabled;
      const detail = cfg && (cfg.companies || cfg.orgs || cfg.accounts || cfg.tenants || cfg.query)
        ? (cfg.companies || cfg.orgs || cfg.accounts || cfg.tenants || [cfg.query]).join(", ")
        : "";
      return `<div class="rating-row"><span class="name">${esc(name)} ${detail ? `<span class="muted" style="font-size:11px">· ${esc(detail)}</span>` : ""}</span>
        <span class="badge ${on ? "approved" : "rejected"}" style="font-size:11px">${on ? "on" : "off"}</span></div>`;
    }).join("");
    card.innerHTML = `
      <div class="section-title">Source registry <span class="muted">enabled feeds</span></div>
      ${rows || '<p class="muted" style="font-size:13px">No sources configured.</p>'}
      <p class="muted" style="font-size:12px;margin-top:10px">Edit <code>backend/sources.json</code> to enable a source and add its slugs/keys.</p>`;
  }

  // ---------- Analytics: fit trend (F11) ----------
  async function renderTrend() {
    const card = $("#trendCard");
    let t;
    try { t = await api("/api/analytics/trend"); } catch (e) { card.innerHTML = `<div class="section-title">Fit trend</div>` + emptyBox("Unavailable", e.message); return; }
    const pts = t.points || [];
    if (!pts.length) {
      card.innerHTML = `<div class="section-title">Fit trend <span class="muted">how your match quality is moving</span></div>` +
        emptyBox("No trend yet", "Run a couple of scans to start tracking how your average fit changes over time.");
      return;
    }
    card.innerHTML = `
      <div class="section-title">Fit trend <span class="muted">how your match quality is moving</span></div>
      ${trendChart(pts)}
      <div class="trend-legend">
        <span><i style="background:var(--primary)"></i>Avg confidence</span>
        <span><i style="background:var(--green)"></i>Avg eligibility</span>
        <span class="muted">${pts.length} scans</span>
      </div>`;
  }

  function trendChart(pts) {
    const W = 560, H = 180, pad = 30;
    const n = pts.length;
    const x = (i) => pad + (n > 1 ? (i / (n - 1)) * (W - pad * 2) : (W - pad * 2) / 2);
    const y = (v) => H - pad - (v / 100) * (H - pad * 2);
    const line = (key, color) => {
      const segs = pts.map((p, i) => (p[key] != null ? `${x(i)},${y(p[key])}` : null)).filter(Boolean);
      if (segs.length < 2) return "";
      return `<polyline points="${segs.join(" ")}" fill="none" stroke="${color}" stroke-width="2"/>`;
    };
    const dots = (key, color) => pts.map((p, i) =>
      p[key] != null ? `<circle cx="${x(i)}" cy="${y(p[key])}" r="3" fill="${color}"/>` : "").join("");
    const grid = [0, 25, 50, 75, 100].map((v) =>
      `<line x1="${pad}" y1="${y(v)}" x2="${W - pad}" y2="${y(v)}" stroke="var(--border)" stroke-width="1"/>
       <text x="${pad - 6}" y="${y(v) + 3}" text-anchor="end" class="axis">${v}</text>`).join("");
    const labels = pts.map((p, i) => (i % Math.ceil(n / 6) === 0 ?
      `<text x="${x(i)}" y="${H - pad + 14}" text-anchor="middle" class="axis">${esc((p.at || "").slice(5, 10))}</text>` : "")).join("");
    return `<svg viewBox="0 0 ${W} ${H}" class="trend-chart">${grid}
      ${line("avg_confidence", "var(--primary)")}${dots("avg_confidence", "var(--primary)")}
      ${line("avg_eligibility", "var(--green)")}${dots("avg_eligibility", "var(--green)")}
      ${labels}</svg>`;
  }

  // ---------- Analytics: salary insights (F1) ----------
  async function renderSalary() {
    const card = $("#salaryCard");
    let s;
    try { s = await api("/api/analytics/salary"); } catch (e) { card.innerHTML = `<div class="section-title">Salary insights</div>` + emptyBox("Unavailable", e.message); return; }
    if (!s.count) {
      card.innerHTML = `<div class="section-title">Salary insights <span class="muted">market vs. you</span></div>` +
        emptyBox("No salary data", "None of the collected jobs list a parseable salary yet.");
      return;
    }
    const hist = (s.histogram || []).reduce((o, b) => (o[b.label] = b.count, o), {});
    const gauge = (s.user_percentile != null)
      ? `<div class="gauge">
           <div class="gauge-track"><span style="width:${s.user_percentile}%"></span>
             <i class="gauge-marker" style="left:${s.user_percentile}%"></i></div>
           <div class="gauge-lbl"><span>Your ask · ${s.user_value}k</span><span>${s.user_percentile}th percentile of ${s.count} jobs</span></div>
         </div>`
      : `<p class="muted" style="font-size:12.5px">Set your expected salary in Profile to see where you fall.</p>`;
    card.innerHTML = `
      <div class="section-title">Salary insights <span class="muted">market vs. you</span></div>
      <div class="grid cols-4" style="margin-bottom:12px">
        ${statCard("Median", s.median + "k", "blue", `${s.count} jobs`)}
        ${statCard("P25", s.p25 + "k", "teal", "lower quartile")}
        ${statCard("P75", s.p75 + "k", "violet", "upper quartile")}
        ${statCard("Range", `${s.min}–${s.max}k`, "green", "min to max")}
      </div>
      ${barChart(hist, { label: (k) => k.replace("k", "") })}
      ${gauge}`;
  }

  // ---------- Analytics: skill gap (F3) ----------
  async function renderSkills() {
    const card = $("#skillsCard");
    let s;
    try { s = await api("/api/analytics/skills"); } catch (e) { card.innerHTML = `<div class="section-title">Skill demand</div>` + emptyBox("Unavailable", e.message); return; }
    const top = (s.top_requested || []).reduce((o, x) => (o[x.skill] = x.count, o), {});
    const mine = (s.your_skills_by_demand || []).reduce((o, x) => (o[x.skill] = x.count, o), {});
    const missing = (s.you_are_missing || []).map((x) => `
      <div class="gap-row">
        <span class="tag skill miss">${esc(x.skill)}</span>
        <span class="muted" style="font-size:12px">${x.count} jobs</span>
        <button class="btn sm ghost" data-addskill="${esc(x.skill)}">+ Add to my skills</button>
      </div>`).join("");
    card.innerHTML = `
      <div class="section-title">Skill demand <span class="muted">what the market wants</span></div>
      <div class="grid cols-2">
        <div><div class="skill-group-label">Most requested</div>${hbarChart(top)}</div>
        <div><div class="skill-group-label">Your skills by demand</div>${hbarChart(mine)}</div>
      </div>
      <div class="skill-group" style="margin-top:12px">
        <div class="skill-group-label">You're missing (in demand) · coverage ${s.coverage_pct}%</div>
        ${missing || '<span class="muted">You cover the in-demand skills. 🎉</span>'}
      </div>`;
    card.querySelectorAll("[data-addskill]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const skill = btn.dataset.addskill;
        try {
          const p = await api("/api/profile");
          const skills = Array.from(new Set([...(p.skills || []), skill]));
          await api("/api/profile", { method: "PUT", body: Object.assign({}, p, { skills }) });
          toast(`Added "${skill}" to your skills`);
          await doRescore();
          renderSkills();
        } catch (e) { toast(e.message); }
      });
    });
  }

  // ---------- Analytics: source health (F4) ----------
  async function renderSources() {
    const card = $("#sourcesCard");
    let s;
    try { s = await api("/api/analytics/sources"); } catch (e) { card.innerHTML = `<div class="section-title">Source health</div>` + emptyBox("Unavailable", e.message); return; }
    if (!s.sources.length) {
      card.innerHTML = `<div class="section-title">Source health <span class="muted">scan reliability</span></div>` +
        emptyBox("No scans yet", "Run a scan to start tracking source reliability.");
      return;
    }
    const cards = s.sources.map((src) => `
      <div class="src-card">
        <div class="src-head">
          <span class="dot ${src.health}"></span>
          <b style="text-transform:capitalize">${esc(src.source)}</b>
          <span class="muted" style="font-size:11.5px;margin-left:auto">${timeAgo(src.last_scan)}</span>
        </div>
        <div class="src-meta">
          <span>${src.success_rate}% success</span>
          <span>avg ${src.avg_fetched} fetched</span>
          <span>${src.error_count} errors</span>
        </div>
        ${sparkline(src.sparkline || [])}
      </div>`).join("");
    card.innerHTML = `<div class="section-title">Source health <span class="muted">scan reliability</span></div>
      <div class="src-grid">${cards}</div>`;
  }

  function sparkline(values) {
    if (!values.length) return "";
    const W = 120, H = 28, pad = 2;
    const max = Math.max(1, ...values);
    const step = values.length > 1 ? (W - pad * 2) / (values.length - 1) : 0;
    const pts = values.map((v, i) => `${(pad + i * step).toFixed(1)},${(H - pad - (v / max) * (H - pad * 2)).toFixed(1)}`).join(" ");
    return `<svg viewBox="0 0 ${W} ${H}" class="sparkline"><polyline points="${pts}" fill="none" stroke="var(--primary)" stroke-width="1.5"/></svg>`;
  }

  // ---------- SVG chart helpers ----------
  function donutChart(segments) {
    const total = segments.reduce((s, x) => s + (x.value || 0), 0);
    const R = 60, C = 2 * Math.PI * R;
    let offset = 0;
    const arcs = total ? segments.map((s) => {
      const frac = (s.value || 0) / total;
      const dash = frac * C;
      const el = `<circle r="${R}" cx="80" cy="80" fill="none" stroke="${s.color}" stroke-width="26"
        stroke-dasharray="${dash} ${C - dash}" stroke-dashoffset="${-offset}" transform="rotate(-90 80 80)"/>`;
      offset += dash;
      return el;
    }).join("") : `<circle r="${R}" cx="80" cy="80" fill="none" stroke="var(--border)" stroke-width="26"/>`;
    return `<svg viewBox="0 0 160 160" class="chart donut">${arcs}
      <text x="80" y="76" text-anchor="middle" class="donut-num">${total}</text>
      <text x="80" y="96" text-anchor="middle" class="donut-lbl">applications</text></svg>`;
  }

  function barChart(data, opts = {}) {
    const entries = Object.entries(data);
    if (!entries.length) return emptyBox("No data", "Nothing to chart yet.");
    const W = 320, H = 150, pad = 24;
    const max = opts.max || Math.max(1, ...entries.map(([, v]) => v));
    const bw = (W - pad * 2) / entries.length;
    const fmt = opts.label || ((k) => k);
    const every = opts.labelEvery || 1;
    const bars = entries.map(([k, v], i) => {
      const h = (v / max) * (H - pad * 2);
      const x = pad + i * bw + bw * 0.15;
      const y = H - pad - h;
      const showLabel = i % every === 0;
      return `<rect x="${x}" y="${y}" width="${bw * 0.7}" height="${h}" rx="3" fill="var(--primary)"/>
        ${showLabel ? `<text x="${x + bw * 0.35}" y="${H - pad + 14}" text-anchor="middle" class="axis">${esc(fmt(k))}</text>` : ""}
        ${v > 0 ? `<text x="${x + bw * 0.35}" y="${y - 4}" text-anchor="middle" class="axis val">${v}</text>` : ""}`;
    }).join("");
    return `<svg viewBox="0 0 ${W} ${H}" class="chart bars">${bars}</svg>`;
  }

  function hbarChart(data) {
    const entries = Object.entries(data).sort((a, b) => b[1] - a[1]).slice(0, 8);
    if (!entries.length) return emptyBox("No data", "Nothing to chart yet.");
    const max = Math.max(1, ...entries.map(([, v]) => v));
    const rows = entries.map(([k, v]) => `
      <div class="hbar-row">
        <span class="hbar-label">${esc(k)}</span>
        <div class="hbar-track"><span style="width:${(v / max) * 100}%;background:var(--primary)"></span></div>
        <span class="hbar-val">${v}</span>
      </div>`).join("");
    return `<div class="hbar-list">${rows}</div>`;
  }

  // ---------- Goals / KPI (v2.4) ----------
  async function renderGoals() {
    const el = $("#view-goals");
    el.innerHTML = `<div class="loading"><span class="spinner"></span> Loading goals…</div>`;
    let k;
    try { k = await api("/api/kpi"); } catch (e) { el.innerHTML = emptyBox("Goals unavailable", e.message); return; }

    const goal = k.weekly_goal || 0;
    const done = k.submitted_this_week || 0;
    const pct = Math.min(100, Math.round((done / goal) * 100));
    const goalPct = goal ? pct : 0;
    const ringBg = goalPct >= 100 ? "var(--green)" : goalPct >= 50 ? "var(--amber)" : "var(--primary)";
    const circumference = 2 * Math.PI * 54;
    const dash = goal ? (goalPct / 100) * circumference : 0;

    const stageRows = Object.entries(k.stages || {}).map(([stage, n]) =>
      `<div class="rating-row"><span class="name">${esc(statusLabel(stage))}</span><span class="val">${n}</span></div>`).join("");

    const goalInput = goal
      ? `<div class="card card-pad" style="margin-top:18px">
           <div class="section-title">Weekly application target</div>
           <div style="display:flex;align-items:center;gap:12px;max-width:320px">
             <input id="goalInput" type="number" min="0" value="${goal}" style="flex:1" />
             <button class="btn primary" id="goalSave">Save</button>
           </div>
           <p class="muted" style="font-size:12px;margin-top:8px">Applications submitted this week count toward this target.</p>
         </div>`
      : `<div class="card card-pad" style="margin-top:18px">
           <div class="section-title">Set your weekly target</div>
           <div style="display:flex;align-items:center;gap:12px;max-width:320px">
             <input id="goalInput" type="number" min="0" value="5" style="flex:1" />
             <button class="btn primary" id="goalSave">Set target</button>
           </div>
         </div>`;

    el.innerHTML = `
      <div class="grid cols-3" style="margin-bottom:18px">
        <div class="card card-pad" style="align-items:center;display:flex;flex-direction:column;gap:4px;text-align:center">
          <div class="label" style="font-size:12.5px;color:var(--text-2);font-weight:600;margin-bottom:6px">Weekly progress</div>
          <div style="position:relative;width:120px;height:120px">
            <svg viewBox="0 0 120 120" style="width:120px;height:120px;transform:rotate(-90deg)">
              <circle cx="60" cy="60" r="54" fill="none" stroke="var(--border)" stroke-width="10"/>
              <circle cx="60" cy="60" r="54" fill="none" stroke="${ringBg}" stroke-width="10"
                stroke-dasharray="${dash} ${circumference}" stroke-linecap="round"
                style="transition:stroke-dasharray .5s ease"/>
            </svg>
            <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
              <span style="font-size:28px;font-weight:800;color:${ringBg}">${done}<span style="font-size:14px;color:var(--muted)">/${goal}</span></span>
              <span style="font-size:11px;color:var(--muted)">this week</span>
            </div>
          </div>
        </div>
        <div class="card card-pad">
          <div class="label" style="font-size:12.5px;color:var(--text-2);font-weight:600">Applications submitted</div>
          <div class="value" style="font-size:40px;font-weight:800;margin-top:6px">${k.submitted_total || 0}</div>
          <div class="sub" style="color:var(--muted);font-size:12.5px;margin-top:4px">all time</div>
          <div style="margin-top:14px">${stageRows || '<p class="muted" style="font-size:12.5px">No applications yet</p>'}</div>
        </div>
        <div class="card card-pad">
          <div class="label" style="font-size:12.5px;color:var(--text-2);font-weight:600">Streak</div>
          <div class="value" style="font-size:40px;font-weight:800;margin-top:6px">${k.streak || 0}<span style="font-size:16px;color:var(--muted)">🔥</span></div>
          <div class="sub" style="color:var(--muted);font-size:12.5px;margin-top:4px">consecutive days with submissions</div>
          <div style="margin-top:16px">
            ${[0,1,2,3,4,5,6].map((i) =>
              `<span class="dot" style="width:22px;height:22px;border-radius:6px;display:inline-block;margin:2px;background:${(k.streak && i < k.streak) ? "var(--amber)" : "var(--surface-2)"}"></span>`
            ).join("")}
          </div>
        </div>
      </div>

      <div class="card card-pad">
        <div class="section-title">How it works</div>
        <p class="muted" style="font-size:13px;line-height:1.6;margin:0">
          Set a weekly application target. Every application you mark <b>submitted</b> counts toward this week's goal.
          Keep a submission on <b>consecutive days</b> to build your streak. Progress resets each week — aim for 100% and don't break the chain.
        </p>
      </div>
      ${goalInput}`;

    const gs = $("#goalSave");
    if (gs) gs.addEventListener("click", async () => {
      const val = Number($("#goalInput").value) || 0;
      try {
        await api("/api/kpi", { method: "PUT", body: { weekly_goal: val } });
        toast("Goal saved");
        renderGoals();
      } catch (e) { toast(e.message); }
    });
  }

  // ---------- Profile ----------
  // ---------- Profile (comprehensive) ----------
  const csv = (arr) => (arr || []).join(", ");
  const parseCsv = (s) => String(s || "").split(",").map((x) => x.trim()).filter(Boolean);

  function field(label, id, value, opts = {}) {
    const val = esc(value == null ? "" : value);
    const type = opts.type || "text";
    const ph = opts.placeholder ? ` placeholder="${esc(opts.placeholder)}"` : "";
    const full = opts.full ? " full" : "";
    return `<label class="field${full}">${label}<input id="${id}" type="${type}" value="${val}"${ph} /></label>`;
  }
  function area(label, id, value, rows = 3, full = true) {
    return `<label class="field${full ? " full" : ""}">${label}<textarea id="${id}" rows="${rows}">${esc(value == null ? "" : value)}</textarea></label>`;
  }
  function sectionTitle(t, hint) {
    return `<div class="profile-section"><span>${esc(t)}</span>${hint ? `<span class="muted">${esc(hint)}</span>` : ""}</div>`;
  }

  function certCard(c, i) {
    return `<div class="dyn-card" data-kind="cert" data-idx="${i}">
      <div class="dyn-grid">
        <label class="field">Certification<input data-f="name" value="${esc(c.name || "")}" placeholder="e.g. PMP" /></label>
        <label class="field">Issuer<input data-f="issuer" value="${esc(c.issuer || "")}" placeholder="e.g. PMI" /></label>
        <label class="field">Year<input data-f="year" value="${esc(c.year || "")}" placeholder="2024" /></label>
      </div>
      <button class="btn sm danger dyn-remove" type="button">Remove</button>
    </div>`;
  }
  function projectCard(p, i) {
    return `<div class="dyn-card" data-kind="project" data-idx="${i}">
      <div class="dyn-grid">
        <label class="field">Project name<input data-f="name" value="${esc(p.name || "")}" /></label>
        <label class="field">Tech / tools<input data-f="tech" value="${esc(p.tech || "")}" /></label>
      </div>
      <label class="field full">Description<textarea data-f="description" rows="2">${esc(p.description || "")}</textarea></label>
      <button class="btn sm danger dyn-remove" type="button">Remove</button>
    </div>`;
  }
  function expCard(e, i) {
    return `<div class="dyn-card" data-kind="exp" data-idx="${i}">
      <div class="dyn-grid">
        <label class="field">Role / title<input data-f="role" value="${esc(e.role || "")}" /></label>
        <label class="field">Company<input data-f="company" value="${esc(e.company || "")}" /></label>
        <label class="field">Period<input data-f="period" value="${esc(e.period || "")}" placeholder="2022 - Present" /></label>
      </div>
      <label class="field full">Achievements (one per line)<textarea data-f="bullets" rows="3">${esc((e.bullets || []).join("\n"))}</textarea></label>
      <button class="btn sm danger dyn-remove" type="button">Remove</button>
    </div>`;
  }
  function eduCard(e, i) {
    return `<div class="dyn-card" data-kind="edu" data-idx="${i}">
      <div class="dyn-grid">
        <label class="field">Degree / qualification<input data-f="degree" value="${esc(e.degree || "")}" /></label>
        <label class="field">School / institution<input data-f="school" value="${esc(e.school || "")}" /></label>
        <label class="field">Period<input data-f="period" value="${esc(e.period || "")}" placeholder="2018 - 2022" /></label>
      </div>
      <button class="btn sm danger dyn-remove" type="button">Remove</button>
    </div>`;
  }
  function dynSection(title, hint, kind, items, addLabel, emptyMsg) {
    const cards = (items || []).map((it, i) =>
      kind === "cert" ? certCard(it, i) : kind === "project" ? projectCard(it, i) : kind === "exp" ? expCard(it, i) : eduCard(it, i)
    ).join("");
    return `<div class="profile-block">
      ${sectionTitle(title, hint)}
      <div class="dyn-list" data-kind="${kind}">${cards || `<p class="muted dyn-empty">${esc(emptyMsg)}</p>`}</div>
      <button class="btn sm dyn-add" type="button" data-kind="${kind}">+ ${esc(addLabel)}</button>
    </div>`;
  }

  // ---------- Resume variants (F12) ----------
  function variantManagerHTML(p) {
    const variants = state.resumeVariants || [];
    const cards = variants.map((v) => `
      <div class="dyn-card variant-card" data-vid="${esc(v.id)}">
        <div class="variant-head">
          <b>${esc(v.label || "Variant")}</b>
          <button class="btn sm danger dyn-remove-variant" type="button" data-vid="${esc(v.id)}">Remove</button>
        </div>
        <div class="profile-grid">
          <label class="field">Label<input data-vf="label" value="${esc(v.label || "")}" /></label>
          <label class="field">Skills (comma separated)<input data-vf="skills" value="${esc(csv(v.skills))}" /></label>
        </div>
        <label class="field full">Summary<textarea data-vf="summary" rows="2">${esc(v.summary || "")}</textarea></label>
      </div>`).join("");
    return `<div class="profile-block">
      ${sectionTitle("Resume variants", "tailored summaries + skill sets for different roles")}
      <div class="dyn-list" id="variantList">${cards || `<p class="muted dyn-empty">No variants yet. Add one to generate a resume tuned for a specific role.</p>`}</div>
      <button class="btn sm" id="variantAdd" type="button">+ Add variant</button>
    </div>`;
  }

  async function renderProfile() {
    const el = $("#view-profile");
    const p = await api("/api/profile");
    el.innerHTML = `
      <div class="card card-pad profile-wide">
        <div class="profile-banner">
          <div class="pb-title">Your profile</div>
          <div class="pb-sub">This is the single source of truth. Everything — resume, cover letter, and the prefilled application form — is built from these real details. Fill it in once; update it anytime.</div>
        </div>

        <div class="profile-block">
          ${sectionTitle("Identity & contact")}
          <div class="profile-grid">
            ${field("Full name", "p_name", p.name, { placeholder: "Your real name" })}
            ${field("Email", "p_email", p.email, { type: "email", placeholder: "you@email.com" })}
            ${field("Phone", "p_phone", p.phone, { placeholder: "+880…" })}
            ${field("LinkedIn", "p_linkedin", p.linkedin, { placeholder: "linkedin.com/in/you" })}
            ${field("Website / portfolio", "p_website", p.website, { placeholder: "yourportfolio.com" })}
            ${field("GitHub", "p_github", p.github, { placeholder: "github.com/you" })}
          </div>
        </div>

        <div class="profile-block">
          ${sectionTitle("Location & availability")}
          <div class="profile-grid">
            ${field("Current country", "p_country", p.current_country, { placeholder: "Bangladesh" })}
            ${field("City", "p_city", p.city, { placeholder: "Dhaka" })}
            ${field("Timezone", "p_timezone", p.timezone, { placeholder: "UTC+6 (Dhaka)" })}
            ${field("Availability", "p_availability", p.availability, { placeholder: "Immediate / 2 weeks" })}
            ${field("Notice period", "p_notice", p.notice_period, { placeholder: "Immediate" })}
          </div>
        </div>

        <div class="profile-block">
          ${sectionTitle("Role & positioning")}
          <div class="profile-grid">
            ${field("Target role", "p_role", p.role, { placeholder: "Business Analyst" })}
            ${field("Years of experience", "p_years", p.years_experience, { type: "number", placeholder: "4" })}
          </div>
          ${area("Professional summary", "p_summary", p.summary, 3)}
        </div>

        <div class="profile-block">
          ${sectionTitle("Skills & knowledge", "comma separated")}
          <div class="profile-grid">
            ${field("Core skills", "p_skills", csv(p.skills), { placeholder: "SQL, Excel, Power BI" })}
            ${field("Keywords", "p_keywords", csv(p.keywords), { placeholder: "stakeholder, reporting, agile" })}
            ${field("Languages", "p_languages", csv(p.languages), { placeholder: "English, Bengali" })}
            ${field("Interests", "p_interests", csv(p.interests), { placeholder: "data viz, mentoring" })}
          </div>
        </div>

        ${dynSection("Certifications", "name · issuer · year", "cert", p.certifications, "Add certification", "No certifications yet.")}
        ${dynSection("Projects", "name · tech · description", "project", p.projects, "Add project", "No projects yet.")}
        ${dynSection("Work experience", "role · company · period · achievements", "exp", p.experiences, "Add experience", "No experience added yet.")}
        ${dynSection("Education", "degree · school · period", "edu", p.education, "Add education", "No education added yet.")}

        <div class="profile-block">
          ${sectionTitle("Compensation & logistics")}
          <div class="profile-grid">
            ${field("Expected salary", "p_expected", p.expected_salary, { placeholder: "$80k / year" })}
            ${field("Minimum salary", "p_min", p.min_salary, { placeholder: "$60k / year" })}
            ${field("Work authorization", "p_auth", p.work_authorization, { placeholder: "Bangladesh citizen" })}
            ${field("Visa status", "p_visa", p.visa_status, { placeholder: "N/A" })}
            ${field("Preferred work mode", "p_mode", p.preferred_work_mode, { placeholder: "Remote / Hybrid" })}
          </div>
        </div>

        <div class="profile-block">
          ${sectionTitle("Preferences", "comma separated")}
          <div class="profile-grid">
            ${field("Target companies", "p_targets", csv(p.target_companies), { placeholder: "Company A, Company B" })}
            ${field("Deal breakers", "p_deals", csv(p.deal_breakers), { placeholder: "no on-site, no US hours" })}
          </div>
        </div>

        ${variantManagerHTML(p)}

        <div class="save-row">
          <button class="btn primary" id="pSave">Save profile</button>
          <span class="save-msg hidden" id="pMsg">Saved ✓</span>
        </div>

        <hr style="border:none;border-top:1px solid var(--border);margin:22px 0" />
        <div class="profile-block">
          ${sectionTitle("Change password")}
          <div class="profile-grid">
            <label class="field">Current password<input id="p_cur" type="password" /></label>
            <label class="field">New password<input id="p_new" type="password" /></label>
          </div>
          <div class="save-row"><button class="btn" id="pPass">Update password</button></div>
        </div>
      </div>`;

    // Dynamic list add/remove.
    el.querySelectorAll(".dyn-add").forEach((btn) => btn.addEventListener("click", () => {
      const kind = btn.dataset.kind;
      const list = el.querySelector(`.dyn-list[data-kind="${kind}"]`);
      const empty = list.querySelector(".dyn-empty");
      if (empty) empty.remove();
      const idx = list.querySelectorAll(".dyn-card").length;
      const blank = kind === "cert" ? {} : kind === "project" ? {} : kind === "exp" ? { bullets: [] } : {};
      list.insertAdjacentHTML("beforeend", kind === "cert" ? certCard(blank, idx) : kind === "project" ? projectCard(blank, idx) : kind === "exp" ? expCard(blank, idx) : eduCard(blank, idx));
    }));
    el.querySelectorAll(".dyn-remove").forEach((btn) => btn.addEventListener("click", () => {
      const card = btn.closest(".dyn-card");
      const list = card.parentElement;
      card.remove();
      if (!list.querySelector(".dyn-card")) {
        const msg = { cert: "No certifications yet.", project: "No projects yet.", exp: "No experience added yet.", edu: "No education added yet." }[list.dataset.kind];
        list.innerHTML = `<p class="muted dyn-empty">${msg}</p>`;
      }
    }));

    function collectList(kind) {
      const list = el.querySelector(`.dyn-list[data-kind="${kind}"]`);
      const out = [];
      list.querySelectorAll(".dyn-card").forEach((card) => {
        const get = (f) => (card.querySelector(`[data-f="${f}"]`) || {}).value || "";
        if (kind === "cert") out.push({ name: get("name"), issuer: get("issuer"), year: get("year") });
        else if (kind === "project") out.push({ name: get("name"), tech: get("tech"), description: get("description") });
        else if (kind === "exp") out.push({ role: get("role"), company: get("company"), period: get("period"), bullets: get("bullets").split("\n").map((x) => x.trim()).filter(Boolean) });
        else out.push({ degree: get("degree"), school: get("school"), period: get("period") });
      });
      return out;
    }

    $("#pSave").addEventListener("click", async () => {
      const body = {
        name: $("#p_name").value, email: $("#p_email").value, phone: $("#p_phone").value,
        linkedin: $("#p_linkedin").value, website: $("#p_website").value, github: $("#p_github").value,
        current_country: $("#p_country").value, city: $("#p_city").value, timezone: $("#p_timezone").value,
        availability: $("#p_availability").value, notice_period: $("#p_notice").value,
        role: $("#p_role").value, years_experience: $("#p_years").value ? Number($("#p_years").value) : null,
        summary: $("#p_summary").value,
        skills: parseCsv($("#p_skills").value), keywords: parseCsv($("#p_keywords").value),
        languages: parseCsv($("#p_languages").value), interests: parseCsv($("#p_interests").value),
        certifications: collectList("cert"), projects: collectList("project"),
        experiences: collectList("exp"), education: collectList("edu"),
        expected_salary: $("#p_expected").value, min_salary: $("#p_min").value,
        work_authorization: $("#p_auth").value, visa_status: $("#p_visa").value,
        preferred_work_mode: $("#p_mode").value,
        target_companies: parseCsv($("#p_targets").value), deal_breakers: parseCsv($("#p_deals").value),
      };
      await api("/api/profile", { method: "PUT", body });
      const m = $("#pMsg"); m.classList.remove("hidden"); setTimeout(() => m.classList.add("hidden"), 2000);
      toast("Profile saved — re-scoring…");
      await doRescore();
    });
    $("#pPass").addEventListener("click", async () => {
      try {
        await api("/api/profile/password", { method: "POST", body: { current_password: $("#p_cur").value, new_password: $("#p_new").value } });
        toast("Password updated"); $("#p_cur").value = ""; $("#p_new").value = "";
      } catch (e) { toast(e.message); }
    });

    // Resume variants (F12).
    const vList = $("#variantList");
    const vAdd = $("#variantAdd");
    if (vAdd) vAdd.addEventListener("click", async () => {
      const id = "v" + Date.now();
      const next = [...(state.resumeVariants || []), { id, label: "", skills: [], summary: "" }];
      try {
        await api("/api/profile/resume-variants", { method: "PUT", body: { variants: next } });
        state.resumeVariants = next;
        renderProfile();
      } catch (e) { toast(e.message); }
    });
    el.querySelectorAll(".dyn-remove-variant").forEach((btn) => btn.addEventListener("click", async () => {
      const next = (state.resumeVariants || []).filter((v) => String(v.id) !== String(btn.dataset.vid));
      try {
        await api("/api/profile/resume-variants", { method: "PUT", body: { variants: next } });
        state.resumeVariants = next;
        renderProfile();
      } catch (e) { toast(e.message); }
    }));
    // Persist variant edits on blur.
    el.querySelectorAll("[data-vf]").forEach((inp) => inp.addEventListener("change", async () => {
      const card = inp.closest(".variant-card");
      const get = (f) => (card.querySelector(`[data-vf="${f}"]`) || {}).value || "";
      const next = (state.resumeVariants || []).map((v) => {
        if (String(v.id) !== String(card.dataset.vid)) return v;
        return { ...v, label: get("label"), skills: parseCsv(get("skills")), summary: get("summary") };
      });
      try {
        await api("/api/profile/resume-variants", { method: "PUT", body: { variants: next } });
        state.resumeVariants = next;
        toast("Variant saved");
      } catch (e) { toast(e.message); }
    }));
  }

  // ---------- Scan / refresh ----------
  async function doScan() {
    const btn = $("#scanBtn");
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Scanning…';
    try {
      await api("/api/scan", { method: "POST" });
      toast("Scan complete");
      await loadAll();
    } catch (e) { toast(e.message); }
    finally { btn.disabled = false; btn.textContent = "Scan now"; }
  }

  async function doRescore() {
    const btn = $("#rescoreBtn");
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Re-scoring…';
    try {
      const r = await api("/api/rescore", { method: "POST" });
      toast(`Re-scored ${r.rescored} jobs`);
      await loadAll();
    } catch (e) { toast(e.message); }
    finally { btn.disabled = false; btn.textContent = "⟳ Re-score"; }
  }

  async function doEnrich() {
    const btn = $("#enrichBtn");
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Enriching…';
    try {
      const r = await api("/api/enrich", { method: "POST" });
      toast(r.enriched ? `Enriched ${r.enriched} job(s)` : "Nothing to enrich");
      await loadAll();
    } catch (e) { toast(e.message); }
    finally { btn.disabled = false; btn.textContent = "✦ Enrich"; }
  }

  // ---------- Init ----------
  function init() {
    $("#loginForm").addEventListener("submit", doLogin);
    $("#logoutBtn").addEventListener("click", doLogout);
    $("#scanBtn").addEventListener("click", doScan);
    $("#rescoreBtn").addEventListener("click", doRescore);
    $("#enrichBtn").addEventListener("click", doEnrich);
    $("#refreshBtn").addEventListener("click", loadAll);
    $("#closeJob").addEventListener("click", closeJob);
    $("#jobModal").addEventListener("click", (e) => { if (e.target.id === "jobModal") closeJob(); });
    $("#closeCompare").addEventListener("click", closeCompare);
    $("#compareModal").addEventListener("click", (e) => { if (e.target.id === "compareModal") closeCompare(); });
    $("#closeFollowup").addEventListener("click", closeFollowup);
    $("#followupModal").addEventListener("click", (e) => { if (e.target.id === "followupModal") closeFollowup(); });
    document.querySelectorAll(".nav-item").forEach((n) => n.addEventListener("click", () => { setView(n.dataset.view); closeSidebar(); }));
    // Mobile sidebar toggle.
    const hamburger = $("#hamburgerBtn");
    const overlay = $("#sidebarOverlay");
    const closeSidebar = () => {
      document.body.classList.remove("sidebar-open");
      overlay.classList.add("hidden");
    };
    if (hamburger) hamburger.addEventListener("click", () => {
      const open = document.body.classList.toggle("sidebar-open");
      overlay.classList.toggle("hidden", !open);
    });
    if (overlay) overlay.addEventListener("click", closeSidebar);

    if (state.token) {
      api("/api/auth/me")
        .then((d) => { state.user = d.user; showApp(); setView("dashboard"); return loadAll(); })
        .catch(() => showLogin());
    } else {
      showLogin();
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();

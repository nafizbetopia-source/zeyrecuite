"""Browser-based submission on the employer's own application page (Phase 4).

Opens the job's application URL in headless Chromium (Playwright), fills the
form from the user's profile + prepared materials, uploads the tailored resume
PDF, submits, and saves a full-page screenshot as proof.

Design rules (deliberately conservative):
- **Never raises.** Failures return ``{"ok": False, "status": "failed", ...}``
  so the caller falls back to the existing honest manual ("ready") flow —
  nothing is ever marked submitted unless the browser confirms a receipt page.
- **Never wrong data.** Fields are matched by label/name/placeholder/type;
  unknown or already-filled fields are left untouched rather than guessed.
- **Offline-safe.** ``browser_available()`` is False under pytest (tests stay
  offline; opt in with ``ZEYRECUITE_BROWSER_SUBMIT=1``) and when Playwright or
  its Chromium build is missing. The pure helpers (``plan_fills``,
  ``detect_submit_target``, ``is_success_page``) are unit tested with plain
  data — no browser needed.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Pure helpers (no browser): field matching, submit button, receipt detection
# ---------------------------------------------------------------------------

# A page (or final URL) that clearly confirms a receipt. Deliberately strict:
# claiming a submission that didn't happen is far worse than missing one.
_SUCCESS_RE = re.compile(
    r"thank[-\s]?you|thanks for (applying|your|submi)|"
    r"application (was |has been |is )?(received|submitted)|"
    r"successfully (submitted|received|applied)|"
    r"we\s+received|we(’|')ve received|confirmation number|"
    r"your application (is|was)|"
    r"/thank[-_]?you|/confirmation|/success",
    re.I,
)

# Submit-like buttons, most specific first: the first pattern that matches any
# button wins, so "Submit application" beats a sibling "Apply now".
_SUBMIT_RES = (
    re.compile(r"^submit(\s+(my\s+)?application)?$", re.I),
    re.compile(r"^(send|complete|finish)(\s+(my\s+)?application)?$", re.I),
    re.compile(r"^(submit|send|apply)(\s+now|\s+online)?$", re.I),
    re.compile(r"^apply(\s+now)?$", re.I),
)

# Person-name fields must look like a person name — never "company name",
# "user name", "job title", "email", ...
_NAME_OK = re.compile(r"\b(full name|your name|applicant name|first name|name)\b", re.I)
_NAME_BLOCK = re.compile(
    r"company|employer|hiring|team|manager|email|password|user[\s_-]?name|job[\s_-]?title|file",
    re.I,
)


def _haystack(field: dict) -> str:
    """All identifying text of one form-field descriptor, lowercased."""
    parts = [
        field.get("label"), field.get("name"), field.get("placeholder"),
        field.get("id"), field.get("aria"), field.get("type"), field.get("text"),
    ]
    return " ".join(str(p) for p in parts if p).strip().lower()


def _match_profile(hay: str, profile: dict) -> str | None:
    """Map a field's text to a profile value (most specific rule first).

    Returns ``None`` when the field isn't recognized; returns the profile value
    (possibly empty) when it is — an empty value simply leaves the field alone.
    """
    if re.search(r"e-?mail", hay):
        return profile.get("email")
    if re.search(r"phone|mobile|telephone|contact number", hay):
        return profile.get("phone")
    if "linkedin" in hay:
        return profile.get("linkedin")
    if "github" in hay:
        return profile.get("github")
    if re.search(r"website|portfolio|personal site", hay):
        return profile.get("website")
    if re.search(r"\bcity\b|current location", hay):
        return profile.get("city") or profile.get("current_country")
    if _NAME_OK.search(hay) and not _NAME_BLOCK.search(hay):
        return profile.get("name")
    return None


def plan_fills(
    fields: list[dict],
    *,
    profile: dict,
    cover_letter: str = "",
    answers: dict | None = None,
) -> list[tuple[int, str]]:
    """Decide which form field (by index) gets which value. Pure & testable.

    ``fields`` are descriptors ``{label, name, placeholder, id, aria, type,
    value, text}``. Returns ``[(index, value), ...]``; each field is filled at
    most once and only when it is currently empty.
    """
    plan: list[tuple[int, str]] = []
    used: set[int] = set()
    answers = answers or {}

    def take(idx: int, value: str) -> None:
        value = (value or "").strip()
        if idx in used or not value:
            return
        used.add(idx)
        plan.append((idx, value))

    for idx, field in enumerate(fields):
        if str(field.get("value") or "").strip():
            continue  # never overwrite what the form already has
        hay = _haystack(field)
        ftype = str(field.get("type") or "").lower()

        # 1. Saved application answers, matched by their question text.
        hit = None
        for question, answer in answers.items():
            q = str(question or "").strip().lower()
            a = str(answer or "")
            if len(q) >= 6 and q in hay and a.strip():
                hit = a
                break
        if hit:
            take(idx, hit)
            continue

        # 2. Cover letter → a textarea that mentions it.
        if ftype == "textarea" and re.search(
            r"cover[\s-]*letter|letter of motivation|message to the hiring", hay
        ):
            take(idx, cover_letter)
            continue

        # 3. Profile heuristics (specific → general, person-name last).
        val = _match_profile(hay, profile)
        if val is not None:
            take(idx, val)
    return plan


def detect_submit_target(buttons: list[dict]) -> int | None:
    """Index of the button that submits the form, or None. Skips disabled."""
    for pattern in _SUBMIT_RES:
        for idx, btn in enumerate(buttons):
            text = str(btn.get("text") or "").strip()
            if not text or btn.get("disabled"):
                continue
            if pattern.match(text):
                return idx
    return None


def is_success_page(text: str, url: str = "") -> bool:
    """True only when the page (or final URL) clearly confirms a receipt."""
    return bool(_SUCCESS_RE.search(f"{text or ''} {url or ''}"))


def browser_available() -> bool:
    """Can an actual headless-Chromium submission be attempted right now?"""
    if os.environ.get("ZEYRECUITE_BROWSER_SUBMIT") == "0":
        return False
    if "pytest" in sys.modules and os.environ.get("ZEYRECUITE_BROWSER_SUBMIT") != "1":
        return False  # keep the unit-test suite offline & fast; opt in with =1
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return False
    try:
        with sync_playwright() as pw:
            return Path(pw.chromium.executable_path).exists()
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Browser layer (Playwright). Everything below degrades gracefully — see the
# module docstring; failures surface as data, never exceptions.
# ---------------------------------------------------------------------------

_FIELD_SELECTOR = (
    "input:not([type=hidden]):not([type=file]):not([type=submit]):not([type=button]),"
    " textarea, select"
)
_BUTTON_SELECTOR = "button, input[type=submit], [role=button]"
# Multi-step forms: buttons that move to the next section (clicked only while
# no real submit button is present yet).
_NEXT_RE = re.compile(r"^(next|continue|proceed)(\s+(step|section|page|question))?$", re.I)

def _collect_fields(page) -> list[dict]:
    """Describe the page's fillable fields (DOM order) for ``plan_fills``."""
    try:
        return page.evaluate(
            """(sel) => {
              const out = [];
              let i = 0;
              for (const el of document.querySelectorAll(sel)) {
                const label = (el.labels && el.labels[0]) ? el.labels[0].innerText : '';
                out.push({
                  index: i++,
                  label: (el.getAttribute('aria-label') || label || '').trim(),
                  name: el.name || '', placeholder: el.placeholder || '',
                  id: el.id || '', aria: el.getAttribute('aria-labelledby') || '',
                  type: (el.type || el.tagName.toLowerCase()),
                  value: el.value || '',
                });
              }
              return out;
            }""",
            _FIELD_SELECTOR,
        )
    except Exception:
        return []


def _fill_fields(page, plan: list[tuple[int, str]], selector: str) -> int:
    """Fill planned fields by DOM index; skips anything that won't take a value."""
    filled = 0
    if not plan:
        return 0
    loc = page.locator(selector)
    for idx, value in plan:
        try:
            el = loc.nth(idx)
            tag = el.evaluate("(e) => e.tagName.toLowerCase()")
            if tag == "select":
                opts = el.locator("option")
                vals = [
                    opts.nth(k).get_attribute("value") or opts.nth(k).inner_text()
                    for k in range(opts.count())
                ]
                if value in vals:
                    el.select_option(value=value)
                    filled += 1
                # can't map the value onto an option list → leave it alone
            else:
                el.fill(value, timeout=2000)
                filled += 1
        except Exception:
            continue  # hidden/blocked field — best effort, never abort
    return filled


def _upload_resume(page, resume_path: str | None) -> str | None:
    """Attach the tailored resume PDF to the first file input that accepts it.

    Returns a short human-readable note (``"ok"`` / why not) for the audit
    trail; ``None`` when there is nothing to upload.
    """
    if not resume_path or not Path(resume_path).exists():
        return None
    try:
        inputs = page.locator('input[type="file"]')
        for i in range(inputs.count()):
            inp = inputs.nth(i)
            try:
                accept = (inp.get_attribute("accept") or "").lower()
            except Exception:
                accept = ""
            if accept and "pdf" not in accept and "*/*" not in accept and "*" not in accept:
                continue
            inp.set_input_files(str(resume_path), timeout=3000)
            return "ok"
        return "no resume file input found"
    except Exception as exc:  # noqa: BLE001
        return f"file input failed ({type(exc).__name__})"

def _collect_buttons(page) -> list[dict]:
    """Describe clickable submit-ish controls (DOM order)."""
    out: list[dict] = []
    try:
        loc = page.locator(_BUTTON_SELECTOR)
        for i in range(min(loc.count(), 40)):
            h = loc.nth(i)
            try:
                text = (h.inner_text() or h.get_attribute("value") or "").strip()
                out.append({"text": text, "disabled": bool(h.is_disabled())})
            except Exception:
                out.append({"text": "", "disabled": True})
    except Exception:
        pass
    return out


def _click_submit(page) -> tuple[bool, str]:
    """Click the submit button (Enter as a last resort). Returns (did, note)."""
    buttons = _collect_buttons(page)
    idx = detect_submit_target(buttons)
    if idx is None:
        try:
            page.keyboard.press("Enter")
            return True, "pressed Enter (no labeled submit button found)"
        except Exception as exc:
            return False, f"no submit control found ({type(exc).__name__})"
    try:
        target = page.locator(_BUTTON_SELECTOR).nth(idx)
        target.scroll_into_view_if_needed(timeout=1500)
        target.click(timeout=3000)
        return True, f"clicked “{buttons[idx]['text']}”"
    except Exception as exc:
        return False, f"could not click submit ({type(exc).__name__})"


def submit_on_company_site(
    url: str,
    *,
    profile: dict,
    cover_letter: str = "",
    answers: dict | None = None,
    resume_path: str | Path | None = None,
    screenshot_path: str | Path | None = None,
    timeout_ms: int = 45_000,
) -> dict[str, Any]:
    """Fill + submit the application form on the company's own page.

    Returns ``{"ok", "status", "message", "screenshot", "final_url", "filled",
    "submitted", "error"}``. Never raises — see the module docstring.
    """
    result: dict[str, Any] = {
        "ok": False, "status": "failed", "message": "", "screenshot": None,
        "final_url": None, "filled": 0, "submitted": False, "error": None,
    }
    if not browser_available():
        result["message"] = (
            "browser automation unavailable (Playwright/Chromium missing or disabled)"
        )
        return result
    from playwright.sync_api import sync_playwright

    shot = Path(screenshot_path) if screenshot_path else None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.set_default_timeout(timeout_ms)
                page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                try:
                    page.wait_for_load_state("networkidle", timeout=8_000)
                except Exception:
                    pass  # busy pages never go idle — the DOM is enough

                fields = _collect_fields(page)
                plan = plan_fills(
                    fields, profile=profile, cover_letter=cover_letter, answers=answers
                )
                result["filled"] = _fill_fields(page, plan, _FIELD_SELECTOR)
                upload_note = _upload_resume(
                    page, str(resume_path) if resume_path else None
                )

                # Walk "Next/Continue" steps until a real submit button appears.
                for _ in range(3):
                    if detect_submit_target(_collect_buttons(page)) is not None:
                        break
                    advanced = False
                    for i, b in enumerate(_collect_buttons(page)):
                        text = str(b.get("text") or "").strip()
                        if not b.get("disabled") and _NEXT_RE.match(text):
                            try:
                                page.locator(_BUTTON_SELECTOR).nth(i).click(timeout=2500)
                                page.wait_for_timeout(800)
                                advanced = True
                            except Exception:
                                pass
                            break
                    if not advanced:
                        break

                ok_click, click_msg = _click_submit(page)
                result["submitted"] = ok_click
                if ok_click:
                    try:
                        page.wait_for_load_state("networkidle", timeout=15_000)
                    except Exception:
                        pass
                    page.wait_for_timeout(1_500)
                    try:
                        body = page.inner_text("body", timeout=3_000)
                    except Exception:
                        body = ""
                    final_url = page.url
                    result["final_url"] = final_url
                    if is_success_page(body, final_url):
                        result["ok"] = True
                        result["status"] = "submitted"
                        result["message"] = f"{click_msg}; receipt confirmed at {final_url}"
                    else:
                        result["message"] = (
                            f"{click_msg}, but no receipt could be verified — NOT marked "
                            f"submitted. Check the page manually ({final_url})."
                        )
                        if upload_note and upload_note != "ok":
                            result["message"] += f" Resume upload: {upload_note}."
                else:
                    result["message"] = click_msg

                if shot:
                    try:
                        shot.parent.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=str(shot), full_page=True)
                        result["screenshot"] = str(shot)
                    except Exception:
                        pass
            finally:
                try:
                    browser.close()
                except Exception:
                    pass
    except Exception as exc:  # noqa: BLE001 — never raise into the submit flow
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["message"] = result["message"] or (
            f"browser submission failed ({type(exc).__name__})"
        )
    return result

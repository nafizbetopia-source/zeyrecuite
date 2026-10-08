"""Discord webhook notifications (opt-in, local-first).

Posts a plain-text message to ``discord_webhook_url`` (config.yaml). Used by
the daily auto-submit runner to report what it did — submitted, degraded, or
found nothing — and by ``POST /api/notifications/discord/test`` for setup
verification.

Design rules, matching the rest of the backend:
- never raises: a notification problem must never interrupt a submission run;
- injectable ``poster`` so tests run fully offline;
- content is sanitized (no @everyone/@here pings) and capped at Discord's
  2000-character message limit.
"""
from __future__ import annotations

import logging
from typing import Callable

import httpx

logger = logging.getLogger("zeyrecuite.notify")

#: Discord rejects messages longer than 2000 characters.
MAX_CONTENT_LENGTH = 2000

# poster(url, content) — injected in tests; defaults to an httpx POST.
Poster = Callable[[str, str], None]


def _default_poster(url: str, content: str) -> None:
    response = httpx.post(url, json={"content": content}, timeout=10.0)
    response.raise_for_status()


def sanitize(content: str) -> str:
    """Neutralize @everyone/@here pings and cap the message length."""
    text = str(content or "")
    # A zero-width space keeps the text readable for humans but stops the ping.
    text = text.replace("@everyone", "@​everyone").replace("@here", "@​here")
    if len(text) > MAX_CONTENT_LENGTH:
        text = text[: MAX_CONTENT_LENGTH - 1] + "…"
    return text


def send(webhook_url: str | None, content: str, *, poster: Poster | None = None) -> bool:
    """POST ``content`` to the Discord webhook. True when Discord accepted it.

    A missing URL, network error, or non-2xx response returns False and logs —
    callers keep their own record either way and never see an exception.
    """
    if not webhook_url:
        return False
    payload = sanitize(content)
    post = poster or _default_poster
    try:
        post(webhook_url, payload)
    except Exception as exc:  # noqa: BLE001 - notifications never interrupt work
        logger.warning("discord notification failed: %s", exc)
        return False
    logger.info("discord notification sent (%d chars)", len(payload))
    return True

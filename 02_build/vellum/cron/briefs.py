"""Brief generation helpers — morning and evening.

Morning brief target time: 06:30 UTC.
Evening brief target time: 18:00 UTC.

Morning brief now auto-ingests via httpx.post to the Ledger endpoint,
closing the automation loop. No human ferries data to the endpoint.
The machine feeds itself.

Devon-b5dc | 2026-05-14
Devon-58ca | 2026-05-18 — wired httpx.post for Daily Brief automation
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone

import httpx

from vellum.models.entry import SheetEntry
from vellum.models.sheet import SheetMeta
from vellum.storage import get_store

log = logging.getLogger("vellum.cron")

# Ledger endpoint — defaults to self (localhost) but configurable
# via VELLUM_LEDGER_URL for production (e.g. Beast deployment).
LEDGER_BASE_URL = os.environ.get("VELLUM_LEDGER_URL", "http://localhost:8000")

# Timeout for outbound POST calls (seconds)
_POST_TIMEOUT = float(os.environ.get("VELLUM_POST_TIMEOUT", "10"))


async def _post_to_ledger(path: str, payload: dict) -> dict | None:
    """POST JSON to the Ledger endpoint. Returns response dict or None on failure.

    Failures are logged but do not break the brief generation — the brief
    sheet is created regardless so the system degrades gracefully.
    """
    url = f"{LEDGER_BASE_URL}{path}"
    try:
        async with httpx.AsyncClient(timeout=_POST_TIMEOUT) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            log.info("POST %s → %s", url, resp.status_code)
            return data
    except httpx.HTTPStatusError as exc:
        log.warning("POST %s failed: %s %s", url, exc.response.status_code, exc.response.text[:200])
        return None
    except httpx.RequestError as exc:
        log.warning("POST %s connection error: %s", url, exc)
        return None


async def generate_morning_brief(tenant_id: str = "ewan") -> str:
    """Generate the morning brief sheet and POST to the Ledger.

    Two things happen:
    1. A brief sheet is created in the local store (always succeeds).
    2. An httpx.post fires the brief payload to /api/v1/sheets/generate
       on the Ledger endpoint, closing the automation loop.
    """
    store = get_store()
    now = datetime.now(timezone.utc)
    title = f"Morning Brief — {now.strftime('%A %d %B')}"

    meta = SheetMeta(
        tenant_id=tenant_id,
        title=title,
        mode="brief",
        created_by="vellum-cron",
    )
    await store.create_sheet(meta)

    brief_content = (
        f"Good morning. Brief for {now.strftime('%A %d %B %Y')}.\n\n"
        "Awaiting agent reports. Agents will write their updates below."
    )

    entry = SheetEntry(
        sheet_id=meta.id,
        author="vellum-cron",
        content=brief_content,
        entry_type="brief_summary",
    )
    await store.append_entry(meta.id, entry)

    log.info("Morning brief created: %s", meta.id)

    # --- Automation: POST to Ledger endpoint ---
    await _post_to_ledger(
        "/api/v1/sheets/generate",
        {
            "tenant_id": tenant_id,
            "title": title,
            "content": brief_content,
            "author": "vellum-cron",
        },
    )

    return meta.id


async def generate_evening_brief(tenant_id: str = "ewan") -> str:
    """Generate the evening wrap-up sheet and POST to the Ledger.

    Same pattern as morning brief — local store creation + httpx.post
    to the Ledger endpoint for automation.
    """
    store = get_store()
    now = datetime.now(timezone.utc)
    title = f"Evening Wrap — {now.strftime('%A %d %B')}"

    meta = SheetMeta(
        tenant_id=tenant_id,
        title=title,
        mode="brief",
        created_by="vellum-cron",
    )
    await store.create_sheet(meta)

    wrap_content = (
        f"End of day. Wrap-up for {now.strftime('%A %d %B %Y')}.\n\n"
        "Awaiting agent reports. Agents will summarise today's work below."
    )

    entry = SheetEntry(
        sheet_id=meta.id,
        author="vellum-cron",
        content=wrap_content,
        entry_type="brief_summary",
    )
    await store.append_entry(meta.id, entry)

    log.info("Evening brief created: %s", meta.id)

    # --- Automation: POST to Ledger endpoint ---
    await _post_to_ledger(
        "/api/v1/sheets/generate",
        {
            "tenant_id": tenant_id,
            "title": title,
            "content": wrap_content,
            "author": "vellum-cron",
        },
    )

    return meta.id

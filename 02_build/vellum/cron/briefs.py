"""Brief generation helpers — morning and evening.

Morning brief target time: 06:30 UTC.
Evening brief target time: 18:00 UTC.

In production, agents populate the brief content via the
/api/v1/sheets/generate endpoint. This module defines async
placeholder generators for creating the morning and evening
brief sheets; any scheduling is handled elsewhere.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from vellum.models.entry import SheetEntry
from vellum.models.sheet import SheetMeta
from vellum.storage import get_store

log = logging.getLogger("vellum.cron")


async def generate_morning_brief(tenant_id: str = "ewan") -> str:
    """Generate the morning brief sheet."""
    store = get_store()
    now = datetime.now(timezone.utc)

    meta = SheetMeta(
        tenant_id=tenant_id,
        title=f"Morning Brief — {now.strftime('%A %d %B')}",
        mode="brief",
        created_by="vellum-cron",
    )
    sheet = await store.create_sheet(meta)

    entry = SheetEntry(
        sheet_id=meta.id,
        author="vellum-cron",
        content=(
            f"Good morning. Brief for {now.strftime('%A %d %B %Y')}.\n\n"
            "Awaiting agent reports. Agents will write their updates below."
        ),
        entry_type="brief_summary",
    )
    await store.append_entry(meta.id, entry)

    log.info("Morning brief created: %s", meta.id)
    return meta.id


async def generate_evening_brief(tenant_id: str = "ewan") -> str:
    """Generate the evening wrap-up sheet."""
    store = get_store()
    now = datetime.now(timezone.utc)

    meta = SheetMeta(
        tenant_id=tenant_id,
        title=f"Evening Wrap — {now.strftime('%A %d %B')}",
        mode="brief",
        created_by="vellum-cron",
    )
    sheet = await store.create_sheet(meta)

    entry = SheetEntry(
        sheet_id=meta.id,
        author="vellum-cron",
        content=(
            f"End of day. Wrap-up for {now.strftime('%A %d %B %Y')}.\n\n"
            "Awaiting agent reports. Agents will summarise today's work below."
        ),
        entry_type="brief_summary",
    )
    await store.append_entry(meta.id, entry)

    log.info("Evening brief created: %s", meta.id)
    return meta.id

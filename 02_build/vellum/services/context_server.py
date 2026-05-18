"""Context server — assemble the full context packet for an agent.

GET /api/v1/brain/context?agent_id=...&tenant_id=...

Returns: portable spine + latest baton + recent entries + active
decisions + unread items. This is the packet the next agent wakes
up with — everything it needs to start a bounded sprint.

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import logging

from vellum.models.spine import PortableSpine
from vellum.services.spine_server import get_spine
from vellum.storage import get_store

log = logging.getLogger("vellum.context")


async def assemble_context_packet(
    agent_id: str,
    tenant_id: str = "ewan",
    max_recent_entries: int = 20,
) -> dict:
    """Assemble the full context packet for an agent.

    The packet contains everything the agent needs on wakeup:
    - spine: the agent's portable spine (if registered)
    - latest_baton: the most recent baton pass
    - recent_entries: last N entries across all sheets
    - decisions: active pinned decisions
    - unread: entries the agent hasn't read yet
    """
    store = get_store()

    # 1. Portable spine
    spine = get_spine(agent_id, tenant_id)
    spine_dict = spine.model_dump(mode="json") if spine else None

    # 2. Latest baton pass (across all sheets)
    latest_baton = None
    sheets = await store.list_sheets(tenant_id)
    for sheet in reversed(sheets):
        for entry in reversed(sheet.entries):
            if entry.entry_type == "baton_pass":
                latest_baton = {
                    "entry_id": entry.id,
                    "sheet_id": sheet.meta.id,
                    "author": entry.author,
                    "content": entry.content,
                    "timestamp": entry.timestamp.isoformat(),
                    "metadata": entry.metadata,
                }
                break
        if latest_baton:
            break

    # 3. Recent entries (most recent first, across all sheets)
    all_entries = []
    for sheet in sheets:
        for entry in sheet.entries:
            all_entries.append({
                "entry_id": entry.id,
                "sheet_id": sheet.meta.id,
                "sheet_title": sheet.meta.title,
                "author": entry.author,
                "content": entry.content,
                "entry_type": entry.entry_type,
                "epistemic_tier": entry.epistemic_tier,
                "timestamp": entry.timestamp.isoformat(),
            })
    all_entries.sort(key=lambda e: e["timestamp"], reverse=True)
    recent_entries = all_entries[:max_recent_entries]

    # 4. Decisions
    decisions = await store.get_decisions(tenant_id)
    decisions_list = [
        {
            "id": d.id,
            "sheet_id": d.sheet_id,
            "author": d.author,
            "content": d.content,
            "timestamp": d.timestamp.isoformat(),
            "epistemic_tier": d.epistemic_tier,
        }
        for d in decisions
    ]

    # 5. Unread entries
    unread = await store.get_unread(tenant_id, reader_id=agent_id)
    unread_list = [
        {
            "entry_id": u.id,
            "sheet_id": u.sheet_id,
            "author": u.author,
            "content": u.content,
            "entry_type": u.entry_type,
            "timestamp": u.timestamp.isoformat(),
        }
        for u in unread
    ]

    packet = {
        "agent_id": agent_id,
        "tenant_id": tenant_id,
        "spine": spine_dict,
        "latest_baton": latest_baton,
        "recent_entries": recent_entries,
        "decisions": decisions_list,
        "unread": unread_list,
        "counts": {
            "recent_entries": len(recent_entries),
            "decisions": len(decisions_list),
            "unread": len(unread_list),
            "total_sheets": len(sheets),
        },
    }

    log.info(
        "Context packet assembled: agent=%s entries=%d decisions=%d unread=%d",
        agent_id,
        len(recent_entries),
        len(decisions_list),
        len(unread_list),
    )
    return packet

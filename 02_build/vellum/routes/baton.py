"""Baton pass route — receives session handover payloads from agents.

POST /api/v1/baton
  - Receives a BatonPass payload when a session finishes
  - Creates a baton_pass entry on the agent's active brief sheet
  - Stores the baton for the next agent to read
  - Returns confirmation + entry ID

This closes the MCP Context Pipe loop:
  Agent works → baton pass to Ledger → Ledger evaluates → next agent wakes.

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from vellum.models.baton import BatonPass
from vellum.models.entry import SheetEntry
from vellum.storage import get_store

log = logging.getLogger("vellum.baton")
router = APIRouter(prefix="/api/v1", tags=["baton"])


class BatonPassRequest(BaseModel):
    """Inbound baton pass from an agent session."""

    session_id: str = ""
    agent_id: str = ""
    tenant_id: str = "ewan"
    what_happened: str = ""
    implications: str = ""
    actions_required: list[str] = Field(default_factory=list)
    work_refs: list[dict] = Field(default_factory=list)
    context_saturation_pct: float = 0.0
    next_agent: str = ""
    epistemic_tier: str = "INTUITED"
    metadata: dict = Field(default_factory=dict)


@router.post("/baton")
async def receive_baton(body: BatonPassRequest) -> dict:
    """Receive a baton pass from a finishing agent session.

    Creates a baton_pass entry on the most recent brief sheet for the
    tenant, or creates a new sheet if none exists.
    """
    store = get_store()
    baton = BatonPass(
        session_id=body.session_id,
        agent_id=body.agent_id,
        tenant_id=body.tenant_id,
        what_happened=body.what_happened,
        implications=body.implications,
        actions_required=body.actions_required,
        context_saturation_pct=body.context_saturation_pct,
        next_agent=body.next_agent,
        epistemic_tier=body.epistemic_tier,
        metadata=body.metadata,
    )

    # Find the most recent brief sheet for this tenant
    sheets = await store.list_sheets(body.tenant_id)
    brief_sheets = [s for s in sheets if s.meta.mode == "brief"]

    if brief_sheets:
        target_sheet = brief_sheets[-1]
        sheet_id = target_sheet.meta.id
        prev_hash = target_sheet.latest_hash
    else:
        # No brief sheet exists — create one to hold the baton
        from vellum.models.sheet import SheetMeta

        meta = SheetMeta(
            tenant_id=body.tenant_id,
            title=f"Baton pass from {body.agent_id or 'unknown'}",
            mode="brief",
            created_by="vellum-baton",
        )
        target_sheet = await store.create_sheet(meta)
        sheet_id = meta.id
        prev_hash = ""

    # Build the baton content as structured text
    content_parts = [
        f"## Baton Pass — {body.agent_id or 'unknown'}",
        "",
        f"**Session:** {body.session_id or 'not provided'}",
        "",
        "### What Happened",
        body.what_happened or "(not provided)",
        "",
        "### Implications",
        body.implications or "(not provided)",
        "",
        "### Actions Required",
    ]
    if body.actions_required:
        for action in body.actions_required:
            content_parts.append(f"- {action}")
    else:
        content_parts.append("(none)")

    if body.next_agent:
        content_parts.extend(["", f"**Next agent:** {body.next_agent}"])

    content = "\n".join(content_parts)

    entry = SheetEntry(
        sheet_id=sheet_id,
        author=body.agent_id or "unknown-agent",
        content=content,
        prev_hash=prev_hash,
        entry_type="baton_pass",
        epistemic_tier=body.epistemic_tier,
        metadata={
            "baton_id": baton.id,
            "session_id": body.session_id,
            "context_saturation_pct": body.context_saturation_pct,
            "next_agent": body.next_agent,
            "work_refs": body.work_refs,
            "actions_required": body.actions_required,
        },
    )
    await store.append_entry(sheet_id, entry)

    log.info(
        "Baton received: agent=%s session=%s sheet=%s",
        body.agent_id,
        body.session_id,
        sheet_id,
    )

    return {
        "status": "ok",
        "baton_id": baton.id,
        "entry_id": entry.id,
        "sheet_id": sheet_id,
        "next_agent": body.next_agent,
    }


@router.get("/baton/latest")
async def get_latest_baton(tenant_id: str = "ewan") -> dict:
    """Get the most recent baton pass for a tenant.

    Used by the next agent to read what the previous session left behind.
    """
    store = get_store()
    sheets = await store.list_sheets(tenant_id)

    for sheet in reversed(sheets):
        for entry in reversed(sheet.entries):
            if entry.entry_type == "baton_pass":
                return {
                    "status": "ok",
                    "entry_id": entry.id,
                    "sheet_id": sheet.meta.id,
                    "author": entry.author,
                    "content": entry.content,
                    "timestamp": entry.timestamp.isoformat(),
                    "metadata": entry.metadata,
                }

    raise HTTPException(status_code=404, detail="No baton pass found")

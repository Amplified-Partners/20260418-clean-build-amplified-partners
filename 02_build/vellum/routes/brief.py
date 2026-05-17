"""Brief mode routes — sheet CRUD, entry listing, brief generation.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from vellum.models.entry import SheetEntry
from vellum.models.sheet import SheetMeta
from vellum.models.token import ShareToken
from vellum.storage import get_store

router = APIRouter(prefix="/api/v1", tags=["brief"])


class GenerateRequest(BaseModel):
    tenant_id: str = "ewan"
    title: str = ""
    content: str = ""
    author: str = "vellum-generator"


class AgentWriteRequest(BaseModel):
    sheet_id: str
    content: str
    author: str
    entry_type: str = "agent_write"
    metadata: dict = {}


@router.post("/sheets/generate")
async def generate_brief(body: GenerateRequest) -> dict:
    """Generate a new brief sheet with initial content."""
    store = get_store()
    now = datetime.now(timezone.utc)

    title = body.title or f"Brief — {now.strftime('%A %d %B %Y, %H:%M')}"
    meta = SheetMeta(
        tenant_id=body.tenant_id,
        title=title,
        mode="brief",
        created_by=body.author,
    )
    sheet = await store.create_sheet(meta)

    if body.content:
        entry = SheetEntry(
            sheet_id=meta.id,
            author=body.author,
            content=body.content,
            entry_type="brief_summary",
        )
        await store.append_entry(meta.id, entry)

    token = ShareToken(
        sheet_id=meta.id,
        role="write",
        expires_at=now + timedelta(hours=72),
    )
    await store.store_token(token)

    return {
        "status": "ok",
        "sheet_id": meta.id,
        "token_id": token.token_id,
        "title": title,
    }


@router.get("/sheets")
async def list_sheets(tenant_id: str = "ewan") -> dict:
    """List all sheets for a tenant.

    19/3 principle: returns only the 3 human-facing fields (title, mode,
    created_by) plus metadata (epistemic_tier, entry_count, timestamps).
    Internal fields (hash chain, tenant_id) stay behind the pipe.
    """
    store = get_store()
    sheets = await store.list_sheets(tenant_id)
    return {
        "sheets": [
            {
                "id": s.meta.id,
                # --- 3 human-facing fields ---
                "title": s.meta.title,
                "mode": s.meta.mode,
                "created_by": s.meta.created_by,
                # --- metadata ---
                "epistemic_tier": s.meta.epistemic_tier,
                "created_at": s.meta.created_at.isoformat(),
                "entry_count": len(s.entries),
            }
            for s in sheets
        ],
        "count": len(sheets),
    }


@router.get("/sheets/{sheet_id}")
async def get_sheet(sheet_id: str) -> dict:
    """Get a sheet with all entries.

    19/3 principle applied per entry: human sees (author, content, entry_type)
    plus metadata (epistemic_tier, timestamp, entry_hash for provenance).
    Raw internal metadata dict stays behind the pipe.
    """
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "sheet_id": sheet.meta.id,
        "title": sheet.meta.title,
        "mode": sheet.meta.mode,
        "epistemic_tier": sheet.meta.epistemic_tier,
        "created_at": sheet.meta.created_at.isoformat(),
        "created_by": sheet.meta.created_by,
        "entries": [
            {
                "id": e.id,
                # --- 3 human-facing fields ---
                "author": e.author,
                "content": e.content,
                "entry_type": e.entry_type,
                # --- metadata ---
                "epistemic_tier": e.epistemic_tier,
                "timestamp": e.timestamp.isoformat(),
                "entry_hash": e.entry_hash,
            }
            for e in sheet.entries
        ],
        "entry_count": len(sheet.entries),
    }


@router.post("/sheets/{sheet_id}/entries")
async def add_entry(sheet_id: str, body: AgentWriteRequest) -> dict:
    """Add an entry to a sheet (agent or system)."""
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")

    prev_hash = sheet.latest_hash
    entry = SheetEntry(
        sheet_id=sheet_id,
        author=body.author,
        content=body.content,
        prev_hash=prev_hash,
        entry_type=body.entry_type,
        metadata=body.metadata,
    )
    await store.append_entry(sheet_id, entry)

    return {
        "status": "ok",
        "entry_id": entry.id,
        "entry_hash": entry.entry_hash,
    }


# Context saturation tracking — tokens used per agent session
# In production this reads from the agent runtime. For now, simulated.
_CONTEXT_SATURATION: dict[str, float] = {}


def set_context_saturation(agent_id: str, pct: float) -> None:
    """Set context saturation % for an agent. Called by agent runtime."""
    _CONTEXT_SATURATION[agent_id] = max(0.0, min(100.0, pct))


def get_context_saturation(agent_id: str = "active") -> float:
    """Get context saturation % for an agent. 0.0 if unknown."""
    return _CONTEXT_SATURATION.get(agent_id, 0.0)


@router.get("/decisions")
async def list_decisions(tenant_id: str = "ewan") -> dict:
    """List all pinned decisions across sheets.

    19/3 principle: human sees (author, content, timestamp) plus metadata
    (epistemic_tier, context_saturation). Internal fields stay behind.
    """
    store = get_store()
    decisions = await store.get_decisions(tenant_id)
    saturation = get_context_saturation()
    return {
        "decisions": [
            {
                "id": d.id,
                "sheet_id": d.sheet_id,
                # --- 3 human-facing fields ---
                "author": d.author,
                "content": d.content,
                "timestamp": d.timestamp.isoformat(),
                # --- metadata ---
                "epistemic_tier": d.epistemic_tier,
                "entry_hash": d.entry_hash,
            }
            for d in decisions
        ],
        "count": len(decisions),
        "context_saturation_pct": saturation,
        "context_saturation_state": (
            "GREEN" if saturation < 40.0
            else "AMBER" if saturation < 80.0
            else "RED"
        ),
    }


class ContextSaturationUpdate(BaseModel):
    agent_id: str = "active"
    pct: float


@router.post("/context-saturation")
async def update_context_saturation(body: ContextSaturationUpdate) -> dict:
    """Agent reports its context window saturation. Surfaces on decisions."""
    set_context_saturation(body.agent_id, body.pct)
    return {
        "status": "ok",
        "agent_id": body.agent_id,
        "pct": body.pct,
        "state": (
            "GREEN" if body.pct < 40.0
            else "AMBER" if body.pct < 80.0
            else "RED"
        ),
    }

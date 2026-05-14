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
    """List all sheets for a tenant."""
    store = get_store()
    sheets = await store.list_sheets(tenant_id)
    return {
        "sheets": [
            {
                "id": s.meta.id,
                "title": s.meta.title,
                "mode": s.meta.mode,
                "created_at": s.meta.created_at.isoformat(),
                "created_by": s.meta.created_by,
                "entry_count": len(s.entries),
                "latest_hash": s.latest_hash,
            }
            for s in sheets
        ],
        "count": len(sheets),
    }


@router.get("/sheets/{sheet_id}")
async def get_sheet(sheet_id: str) -> dict:
    """Get a sheet with all entries."""
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "sheet_id": sheet.meta.id,
        "title": sheet.meta.title,
        "mode": sheet.meta.mode,
        "created_at": sheet.meta.created_at.isoformat(),
        "created_by": sheet.meta.created_by,
        "entries": [
            {
                "id": e.id,
                "author": e.author,
                "content": e.content,
                "timestamp": e.timestamp.isoformat(),
                "entry_type": e.entry_type,
                "entry_hash": e.entry_hash,
                "metadata": e.metadata,
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


@router.get("/decisions")
async def list_decisions(tenant_id: str = "ewan") -> dict:
    """List all pinned decisions across sheets."""
    store = get_store()
    decisions = await store.get_decisions(tenant_id)
    return {
        "decisions": [
            {
                "id": d.id,
                "sheet_id": d.sheet_id,
                "author": d.author,
                "content": d.content,
                "timestamp": d.timestamp.isoformat(),
                "metadata": d.metadata,
            }
            for d in decisions
        ],
        "count": len(decisions),
    }

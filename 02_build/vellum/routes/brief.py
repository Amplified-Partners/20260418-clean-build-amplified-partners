"""Brief mode routes — sheet read, reply, and entry listing.

All routes validate the share token. Invalid/expired token = 404 (no info leak).

Devon-598da8fc | 2026-05-11
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from vellum.models.entry import SheetEntry
from vellum.webhooks.reply_to_loop import (
    SheetNotFoundError,
    TokenValidationError,
    get_sheet,
    process_reply,
    validate_token,
)

router = APIRouter(prefix="/api/v1/sheets", tags=["brief"])


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------

class ReplyRequest(BaseModel):
    """Body for POST /reply."""

    content: str
    entry_type: Literal["emoji_reaction", "human_comment"]
    token: str


class EntryResponse(BaseModel):
    """Serialised sheet entry for JSON responses."""

    id: str
    sheet_id: str
    author: str
    content: str
    timestamp: str
    prev_hash: str
    entry_hash: str
    entry_type: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/{sheet_id}")
async def render_brief(sheet_id: str, token: str = Query(...)) -> dict:
    """Render the brief sheet.

    Validates token from query param. Returns a minimal HTML-compatible
    payload (in production this would return Jinja-rendered HTML).
    """
    try:
        validate_token(sheet_id, token, min_role="read")
    except TokenValidationError:
        raise HTTPException(status_code=404, detail="Not found")

    sheet = get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")

    entries = [
        EntryResponse(
            id=e.id,
            sheet_id=e.sheet_id,
            author=e.author,
            content=e.content,
            timestamp=e.timestamp.isoformat(),
            prev_hash=e.prev_hash,
            entry_hash=e.entry_hash,
            entry_type=e.entry_type,
        )
        for e in sheet.entries
    ]

    return {
        "sheet_id": sheet.meta.id,
        "title": sheet.meta.title,
        "tenant_id": sheet.meta.tenant_id,
        "entries": [e.model_dump() for e in entries],
    }


@router.post("/{sheet_id}/reply")
async def accept_reply(sheet_id: str, body: ReplyRequest) -> dict:
    """Accept a reply (emoji or comment) from the reader."""
    try:
        entry = await process_reply(
            sheet_id=sheet_id,
            token=body.token,
            content=body.content,
            entry_type=body.entry_type,
        )
    except (SheetNotFoundError, TokenValidationError):
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "status": "ok",
        "entry_id": entry.id,
        "entry_hash": entry.entry_hash,
    }


@router.get("/{sheet_id}/entries")
async def list_entries(sheet_id: str, token: str = Query(...)) -> dict:
    """JSON list of entries for polling/refresh."""
    try:
        validate_token(sheet_id, token, min_role="read")
    except TokenValidationError:
        raise HTTPException(status_code=404, detail="Not found")

    sheet = get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")

    entries = [
        EntryResponse(
            id=e.id,
            sheet_id=e.sheet_id,
            author=e.author,
            content=e.content,
            timestamp=e.timestamp.isoformat(),
            prev_hash=e.prev_hash,
            entry_hash=e.entry_hash,
            entry_type=e.entry_type,
        )
        for e in sheet.entries
    ]

    return {
        "sheet_id": sheet.meta.id,
        "entries": [e.model_dump() for e in entries],
        "count": len(entries),
    }

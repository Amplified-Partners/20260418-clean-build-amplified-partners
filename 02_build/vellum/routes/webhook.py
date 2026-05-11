"""Internal webhook route — brief generation trigger.

POST /api/v1/internal/brief/generate
Used by cron or manual trigger to kick off brief generation for a tenant.

Devon-598da8fc | 2026-05-11
"""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from vellum.models.entry import SheetEntry
from vellum.models.sheet import Sheet, SheetMeta

from vellum.webhooks.reply_to_loop import register_sheet

router = APIRouter(prefix="/api/v1/internal/brief", tags=["internal"])


class GenerateRequest(BaseModel):
    """Body for POST /generate."""

    tenant_id: str


class GenerateResponse(BaseModel):
    """Response for brief generation."""

    status: str
    sheet_id: str
    tenant_id: str
    entry_count: int


@router.post("/generate")
async def generate_brief(body: GenerateRequest) -> GenerateResponse:
    """Trigger brief generation for a tenant.

    In production this orchestrates researchers → synthesiser → sheet.
    For now, creates a stub sheet with a placeholder entry.
    """
    meta = SheetMeta(
        tenant_id=body.tenant_id,
        title=f"Daily Brief — {body.tenant_id}",
        mode="brief",
        created_by="vellum-generator",
    )

    entry = SheetEntry(
        sheet_id=meta.id,
        author="vellum-generator",
        content="Good morning! Here is your daily brief.",
        entry_type="agent_write",
    )

    sheet = Sheet(
        meta=meta,
        entries=[entry],
        latest_hash=entry.entry_hash,
    )

    register_sheet(sheet)

    return GenerateResponse(
        status="ok",
        sheet_id=meta.id,
        tenant_id=body.tenant_id,
        entry_count=1,
    )

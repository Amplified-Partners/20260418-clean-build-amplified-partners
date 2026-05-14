"""UI routes — serves the simple dashboard for Ewan.

HTMX-powered single-page interface. No build step.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from vellum.storage import get_store

router = APIRouter(tags=["ui"])

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATE_DIR))


def _time_ago(dt_val: datetime) -> str:
    """Human-readable relative time."""
    now = datetime.now(timezone.utc)
    if dt_val.tzinfo is None:
        dt_val = dt_val.replace(tzinfo=timezone.utc)
    diff = now - dt_val
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        m = seconds // 60
        return f"{m}m ago"
    if seconds < 86400:
        h = seconds // 3600
        return f"{h}h ago"
    d = seconds // 86400
    return f"{d}d ago"


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, tenant_id: str = "ewan") -> HTMLResponse:
    """Main dashboard — Ewan's contact surface."""
    store = get_store()
    sheets = await store.list_sheets(tenant_id)
    decisions = await store.get_decisions(tenant_id)

    sheets_sorted = sorted(sheets, key=lambda s: s.meta.created_at, reverse=True)

    sheet_data = []
    for s in sheets_sorted:
        last_entry = s.entries[-1] if s.entries else None
        agent_entries = [e for e in s.entries if e.entry_type == "agent_write" or e.entry_type == "brief_summary"]
        human_entries = [e for e in s.entries if e.entry_type in ("human_comment", "emoji_reaction", "decision")]
        unread_count = 0
        read_authors = {e.author for e in s.entries if e.entry_type == "read_receipt"}
        for e in s.entries:
            if e.entry_type in ("agent_write", "brief_summary") and e.author not in read_authors:
                unread_count += 1

        sheet_data.append({
            "id": s.meta.id,
            "title": s.meta.title,
            "mode": s.meta.mode,
            "created_at": s.meta.created_at,
            "time_ago": _time_ago(s.meta.created_at),
            "entry_count": len(s.entries),
            "agent_count": len(agent_entries),
            "human_count": len(human_entries),
            "unread_count": unread_count,
            "last_author": last_entry.author if last_entry else "",
            "last_content": (last_entry.content[:80] + "...") if last_entry and len(last_entry.content) > 80 else (last_entry.content if last_entry else ""),
            "last_time": _time_ago(last_entry.timestamp) if last_entry else "",
        })

    decision_data = [
        {
            "id": d.id,
            "content": d.content,
            "author": d.author,
            "timestamp": d.timestamp,
            "time_ago": _time_ago(d.timestamp),
            "sheet_id": d.sheet_id,
        }
        for d in decisions[:10]
    ]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "sheets": sheet_data,
            "decisions": decision_data,
            "tenant_id": tenant_id,
            "now": datetime.now(timezone.utc),
        },
    )


@router.get("/sheet/{sheet_id}", response_class=HTMLResponse)
async def sheet_detail(request: Request, sheet_id: str) -> HTMLResponse:
    """Detail view of a single sheet — entries + reply interface."""
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        return HTMLResponse("<h1>Not found</h1>", status_code=404)

    entries = [
        {
            "id": e.id,
            "author": e.author,
            "content": e.content,
            "timestamp": e.timestamp,
            "time_ago": _time_ago(e.timestamp),
            "entry_type": e.entry_type,
            "entry_hash": e.entry_hash[:12],
            "metadata": e.metadata,
        }
        for e in sheet.entries
    ]

    return templates.TemplateResponse(
        request=request,
        name="sheet_detail.html",
        context={
            "sheet": {
                "id": sheet.meta.id,
                "title": sheet.meta.title,
                "mode": sheet.meta.mode,
                "created_at": sheet.meta.created_at,
                "created_by": sheet.meta.created_by,
            },
            "entries": entries,
        },
    )


@router.get("/partials/sheets", response_class=HTMLResponse)
async def sheets_partial(request: Request, tenant_id: str = "ewan") -> HTMLResponse:
    """HTMX partial — refreshes the sheets list."""
    store = get_store()
    sheets = await store.list_sheets(tenant_id)
    sheets_sorted = sorted(sheets, key=lambda s: s.meta.created_at, reverse=True)

    sheet_data = []
    for s in sheets_sorted:
        last_entry = s.entries[-1] if s.entries else None
        sheet_data.append({
            "id": s.meta.id,
            "title": s.meta.title,
            "mode": s.meta.mode,
            "time_ago": _time_ago(s.meta.created_at),
            "entry_count": len(s.entries),
            "last_content": (last_entry.content[:60] + "...") if last_entry and len(last_entry.content) > 60 else (last_entry.content if last_entry else ""),
            "last_time": _time_ago(last_entry.timestamp) if last_entry else "",
        })

    return templates.TemplateResponse(
        request=request,
        name="components/sheet_list.html",
        context={"sheets": sheet_data},
    )


@router.get("/partials/entries/{sheet_id}", response_class=HTMLResponse)
async def entries_partial(request: Request, sheet_id: str) -> HTMLResponse:
    """HTMX partial — refreshes entries for a sheet."""
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        return HTMLResponse("")

    entries = [
        {
            "id": e.id,
            "author": e.author,
            "content": e.content,
            "timestamp": e.timestamp,
            "time_ago": _time_ago(e.timestamp),
            "entry_type": e.entry_type,
            "entry_hash": e.entry_hash[:12],
            "metadata": e.metadata,
        }
        for e in sheet.entries
    ]

    return templates.TemplateResponse(
        request=request,
        name="components/entry_list.html",
        context={"entries": entries, "sheet_id": sheet_id},
    )

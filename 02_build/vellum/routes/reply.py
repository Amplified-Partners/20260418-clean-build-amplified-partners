"""Reply handling — bidirectional communication with intent routing.

Ewan's replies (emoji or text) are classified into intents and routed:
- acknowledge → log only
- escalate → create urgent task entry
- clarify → request clarification entry
- decision → pin as decision entry
- create_task → create task entry
- calendar_action → create calendar task
- park_task → create park entry
- general_reply → log as comment

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from vellum.intent.router import classify_reply
from vellum.models.entry import SheetEntry
from vellum.storage import get_store

router = APIRouter(prefix="/api/v1", tags=["reply"])


class ReplyRequest(BaseModel):
    content: str
    author: str = "Ewan"


INTENT_TO_ENTRY_TYPE = {
    "acknowledge": "emoji_reaction",
    "escalate": "task_created",
    "clarify": "human_comment",
    "calendar_action": "task_created",
    "park_task": "task_created",
    "create_task": "task_created",
    "decision": "decision",
    "general_reply": "human_comment",
}


@router.post("/sheets/{sheet_id}/reply")
async def handle_reply(sheet_id: str, body: ReplyRequest) -> dict:
    """Accept a reply from Ewan, classify intent, route accordingly."""
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")

    intent = classify_reply(body.content)
    entry_type = INTENT_TO_ENTRY_TYPE.get(intent.kind, "human_comment")

    prev_hash = sheet.latest_hash
    entry = SheetEntry(
        sheet_id=sheet_id,
        author=body.author,
        content=body.content,
        prev_hash=prev_hash,
        entry_type=entry_type,
        metadata={
            "intent": intent.kind,
            "confidence": intent.confidence,
            "extracted_action": intent.extracted_action,
        },
    )
    await store.append_entry(sheet_id, entry)

    return {
        "status": "ok",
        "entry_id": entry.id,
        "entry_hash": entry.entry_hash,
        "intent": intent.kind,
        "confidence": intent.confidence,
        "entry_type": entry_type,
    }


@router.post("/sheets/{sheet_id}/read-receipt")
async def post_read_receipt(sheet_id: str, author: str = "unknown-agent") -> dict:
    """Agent posts a read receipt to acknowledge it has read the sheet."""
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")

    prev_hash = sheet.latest_hash
    entry = SheetEntry(
        sheet_id=sheet_id,
        author=author,
        content=f"{author} read this sheet",
        prev_hash=prev_hash,
        entry_type="read_receipt",
    )
    await store.append_entry(sheet_id, entry)

    return {
        "status": "ok",
        "entry_id": entry.id,
        "author": author,
    }

"""Reply handling — bidirectional communication with intent routing.

Dual-layer replies:
  1. Verbatim entry — Ewan's raw words, untouched (radical attribution)
  2. Cleaned prompt entry — structured, agent-ready rewrite (chained after)

Ewan's replies (emoji or text) are classified into intents and routed:
- acknowledge → log only (no rewrite for emoji)
- escalate → create urgent task entry + structured prompt
- clarify → request clarification entry + structured prompt
- decision → pin as decision entry + structured prompt
- create_task → create task entry + structured prompt
- calendar_action → create calendar task + structured prompt
- park_task → create park entry + structured prompt
- general_reply → log as comment + structured prompt

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from vellum.intent.router import classify_reply
from vellum.intent.rewriter import rewrite_to_prompt
from vellum.models.entry import SheetEntry
from vellum.storage import get_store

router = APIRouter(prefix="/api/v1", tags=["reply"])

# Minimum content length to trigger rewrite — short emoji/acks don't need it
_REWRITE_MIN_LENGTH = 5


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

# Intents that are too short/simple to benefit from a rewrite
_SKIP_REWRITE_INTENTS = {"acknowledge"}


@router.post("/sheets/{sheet_id}/reply")
async def handle_reply(sheet_id: str, body: ReplyRequest) -> dict:
    """Accept a reply from Ewan, classify intent, route accordingly.

    Dual-layer: stores verbatim first, then generates a cleaned structured
    prompt as a second entry on the same hash chain. Agents read the clean
    version; humans and audit see both.
    """
    store = get_store()
    sheet = await store.get_sheet(sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Not found")

    intent = classify_reply(body.content)
    entry_type = INTENT_TO_ENTRY_TYPE.get(intent.kind, "human_comment")

    # --- Entry 1: verbatim (radical attribution, untouched) ---
    prev_hash = sheet.latest_hash
    verbatim_entry = SheetEntry(
        sheet_id=sheet_id,
        author=body.author,
        content=body.content,
        prev_hash=prev_hash,
        entry_type=entry_type,
        metadata={
            "intent": intent.kind,
            "confidence": intent.confidence,
            "extracted_action": intent.extracted_action,
            "layer": "verbatim",
        },
    )
    await store.append_entry(sheet_id, verbatim_entry)

    # --- Entry 2: cleaned prompt (structured, agent-ready) ---
    cleaned_entry_id = None
    cleaned_text = None
    should_rewrite = (
        intent.kind not in _SKIP_REWRITE_INTENTS
        and len(body.content.strip()) >= _REWRITE_MIN_LENGTH
    )

    if should_rewrite:
        prompt = rewrite_to_prompt(body.content)
        cleaned_text = prompt.clean_text

        # Re-read sheet to get updated latest_hash after verbatim entry
        sheet = await store.get_sheet(sheet_id)
        cleaned_entry = SheetEntry(
            sheet_id=sheet_id,
            author="vellum-rewriter",
            content=cleaned_text,
            prev_hash=sheet.latest_hash if sheet else verbatim_entry.entry_hash,
            entry_type="cleaned_prompt",
            metadata={
                "layer": "cleaned",
                "source_entry_id": verbatim_entry.id,
                "action": prompt.action,
                "subject": prompt.subject,
                "context": prompt.context,
                "urgency": prompt.urgency,
                "constraints": prompt.constraints,
                "raw_length": prompt.raw_length,
            },
        )
        await store.append_entry(sheet_id, cleaned_entry)
        cleaned_entry_id = cleaned_entry.id

    return {
        "status": "ok",
        "entry_id": verbatim_entry.id,
        "entry_hash": verbatim_entry.entry_hash,
        "intent": intent.kind,
        "confidence": intent.confidence,
        "entry_type": entry_type,
        "cleaned_entry_id": cleaned_entry_id,
        "cleaned_text": cleaned_text,
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

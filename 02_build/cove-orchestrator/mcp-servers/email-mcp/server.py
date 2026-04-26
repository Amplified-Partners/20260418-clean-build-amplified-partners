"""Email Agent MCP Server — inbox status, search, draft management."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

import asyncpg
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

SERVICE_NAME = "email"

mcp = FastMCP(
    SERVICE_NAME,
    instructions=(
        "Email Agent MCP server for Amplified Partners. "
        "Provides inbox status, email search, draft management, "
        "and pipeline control."
    ),
)

POSTGRES_DSN = os.environ.get(
    "POSTGRES_DSN",
    "postgresql://cove:cove_dev_2026@localhost:5432/cove",
)

_pool: asyncpg.Pool | None = None


async def _get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(POSTGRES_DSN, min_size=1, max_size=3)
    return _pool


# ─── Tool: Inbox Status ─────────────────────────────────────────────


@mcp.tool(
    name=f"{SERVICE_NAME}_inbox_status",
    description="Get current inbox status: unhandled emails by priority, pending drafts, last sync time.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def inbox_status() -> str:
    pool = await _get_pool()

    priority_rows = await pool.fetch(
        """SELECT priority, count(*) as cnt
           FROM emails_inbound WHERE NOT handled
           GROUP BY priority"""
    )
    draft_count = await pool.fetchval(
        "SELECT count(*) FROM email_drafts WHERE status = 'pending_review'"
    )
    last_sync = await pool.fetchval(
        "SELECT last_sync_at FROM email_accounts ORDER BY last_sync_at DESC NULLS LAST LIMIT 1"
    )

    result = {
        "unhandled_by_priority": {r["priority"]: r["cnt"] for r in priority_rows},
        "total_unhandled": sum(r["cnt"] for r in priority_rows),
        "drafts_pending_review": draft_count,
        "last_sync": last_sync.isoformat() if last_sync else None,
    }
    return json.dumps(result, indent=2)


# ─── Tool: Search Emails ────────────────────────────────────────────


class SearchEmailInput(BaseModel):
    query: str = Field(description="Search term (matches subject, from_address, body_text)")
    priority: str | None = Field(None, description="Filter by priority: critical, urgent, normal, low")
    action: str | None = Field(None, description="Filter by action: respond, delegate, archive, defer, escalate")
    unhandled_only: bool = Field(True, description="Only return unhandled emails")
    limit: int = Field(20, ge=1, le=100, description="Max results")


@mcp.tool(
    name=f"{SERVICE_NAME}_search",
    description="Search emails by keyword, priority, or action. Returns email details. PRIVACY RULE: Do not output any client PII or email bodies in your final report.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def search_emails(input: SearchEmailInput) -> str:
    pool = await _get_pool()

    conditions = ["(subject ILIKE $1 OR from_address ILIKE $1 OR body_text ILIKE $1)"]
    params: list[Any] = [f"%{input.query}%"]
    idx = 2

    if input.unhandled_only:
        conditions.append("NOT handled")

    if input.priority:
        conditions.append(f"priority = ${idx}")
        params.append(input.priority)
        idx += 1

    if input.action:
        conditions.append(f"action = ${idx}")
        params.append(input.action)
        idx += 1

    where = " AND ".join(conditions)

    rows = await pool.fetch(
        f"""SELECT id, from_address, from_name, subject, received_at,
                   priority, action, confidence, triage_reasoning, handled
            FROM emails_inbound
            WHERE {where}
            ORDER BY received_at DESC
            LIMIT ${idx}""",
        *params,
        input.limit,
    )

    results = []
    for r in rows:
        results.append({
            "id": str(r["id"]),
            "from": f"{r['from_name'] or ''} <{r['from_address']}>".strip(),
            "subject": r["subject"],
            "received_at": r["received_at"].isoformat(),
            "priority": r["priority"],
            "action": r["action"],
            "confidence": float(r["confidence"]) if r["confidence"] else None,
            "reasoning": r["triage_reasoning"],
            "handled": r["handled"],
        })

    return json.dumps({"count": len(results), "emails": results}, indent=2)


# ─── Tool: Get Pending Drafts ───────────────────────────────────────


class GetDraftsInput(BaseModel):
    limit: int = Field(10, ge=1, le=50, description="Max drafts to return")


@mcp.tool(
    name=f"{SERVICE_NAME}_get_drafts",
    description="Get pending draft responses. LAYER 0 RULE: Apply Radical Transparency by detailing why a draft was prioritized. PRIVACY RULE: Do not leak recipient PII.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def get_drafts(input: GetDraftsInput) -> str:
    pool = await _get_pool()

    rows = await pool.fetch(
        """SELECT d.id, d.to_addresses, d.subject, d.body_text, d.tone,
                  d.draft_model, d.created_at,
                  e.from_address, e.from_name, e.subject as original_subject,
                  e.priority, e.triage_reasoning
           FROM email_drafts d
           JOIN emails_inbound e ON d.inbound_id = e.id
           WHERE d.status = 'pending_review'
           ORDER BY e.priority DESC, d.created_at ASC
           LIMIT $1""",
        input.limit,
    )

    drafts = []
    for r in rows:
        drafts.append({
            "draft_id": str(r["id"]),
            "to": r["to_addresses"],
            "subject": r["subject"],
            "body": r["body_text"],
            "tone": r["tone"],
            "model": r["draft_model"],
            "created_at": r["created_at"].isoformat(),
            "original_from": f"{r['from_name'] or ''} <{r['from_address']}>".strip(),
            "original_subject": r["original_subject"],
            "priority": r["priority"],
            "triage_reasoning": r["triage_reasoning"],
        })

    return json.dumps({"count": len(drafts), "drafts": drafts}, indent=2)


# ─── Tool: Approve/Reject Draft ─────────────────────────────────────


class ReviewDraftInput(BaseModel):
    draft_id: str = Field(description="UUID of the draft to review")
    action: str = Field(description="'approve' or 'reject'")
    notes: str | None = Field(None, description="Optional review notes or edits")


@mcp.tool(
    name=f"{SERVICE_NAME}_review_draft",
    description="Approve or reject a pending draft response. PRIVACY RULE: If a draft contains unprotected client data, it must be rejected.",
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
async def review_draft(input: ReviewDraftInput) -> str:
    pool = await _get_pool()

    if input.action not in ("approve", "reject"):
        return json.dumps({"error": "Action must be 'approve' or 'reject'"})

    new_status = "approved" if input.action == "approve" else "rejected"

    result = await pool.execute(
        """UPDATE email_drafts
           SET status = $2, review_notes = $3, reviewed_at = now()
           WHERE id = $1::uuid AND status = 'pending_review'""",
        input.draft_id,
        new_status,
        input.notes,
    )

    if result == "UPDATE 0":
        return json.dumps({"error": "Draft not found or already reviewed"})

    return json.dumps({
        "draft_id": input.draft_id,
        "new_status": new_status,
        "notes": input.notes,
    })


# ─── Tool: Run Pipeline ─────────────────────────────────────────────


@mcp.tool(
    name=f"{SERVICE_NAME}_run_pipeline",
    description="Trigger the email pipeline: fetch → triage → draft → notify. Returns run statistics.",
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def run_pipeline_tool() -> str:
    from email_agent.pipeline import run_pipeline

    stats = await run_pipeline()
    return json.dumps(stats, indent=2, default=str)


# ─── Entry Point ─────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")

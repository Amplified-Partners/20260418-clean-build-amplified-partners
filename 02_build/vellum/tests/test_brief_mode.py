"""End-to-end test for Brief mode.

Full flow: generate brief -> check entries on sheet -> simulate reply
-> verify reply in chain -> verify OpenClaw webhook fired.

Devon-598da8fc | 2026-05-11
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from vellum.webhooks.reply_to_loop import (
    clear_stores,
    get_sheet,
    register_token,
)
from vellum.models.token import ShareToken

from datetime import datetime, timedelta, timezone


pytestmark = pytest.mark.asyncio


async def test_full_brief_flow(client: AsyncClient) -> None:
    """Generate a brief, read it, reply with emoji, verify the chain and webhook."""

    # Step 1: Generate brief via internal webhook
    resp = await client.post(
        "/api/v1/internal/brief/generate",
        json={"tenant_id": "tenant-jesmond"},
    )
    assert resp.status_code == 200
    gen_data = resp.json()
    assert gen_data["status"] == "ok"
    sheet_id = gen_data["sheet_id"]
    assert gen_data["entry_count"] == 1

    # Step 2: Create a comment token for the generated sheet
    token = ShareToken(
        token_id="tok-e2e-comment",
        sheet_id=sheet_id,
        role="comment",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
    register_token(token)

    # Also register a read token for GET routes
    read_tok = ShareToken(
        token_id="tok-e2e-read",
        sheet_id=sheet_id,
        role="read",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
    register_token(read_tok)

    # Step 3: Check entries on the sheet
    resp = await client.get(
        f"/api/v1/sheets/{sheet_id}/entries",
        params={"token": read_tok.token_id},
    )
    assert resp.status_code == 200
    entries_data = resp.json()
    assert entries_data["count"] == 1
    assert entries_data["entries"][0]["entry_type"] == "agent_write"

    # Step 4: Simulate emoji reply — mock OpenClaw webhook
    with patch(
        "vellum.webhooks.reply_to_loop._fire_openclaw_webhook",
        new_callable=AsyncMock,
    ) as mock_webhook:
        resp = await client.post(
            f"/api/v1/sheets/{sheet_id}/reply",
            json={
                "content": "thumbsup",
                "entry_type": "emoji_reaction",
                "token": token.token_id,
            },
        )
        assert resp.status_code == 200
        reply_data = resp.json()
        assert reply_data["status"] == "ok"
        assert reply_data["entry_hash"] != ""

        mock_webhook.assert_awaited_once()

    # Step 5: Verify the reply appears in the chain
    resp = await client.get(
        f"/api/v1/sheets/{sheet_id}/entries",
        params={"token": read_tok.token_id},
    )
    assert resp.status_code == 200
    entries_data = resp.json()
    assert entries_data["count"] == 2

    entries = entries_data["entries"]
    agent_entry = entries[0]
    reply_entry = entries[1]

    assert agent_entry["entry_type"] == "agent_write"
    assert reply_entry["entry_type"] == "emoji_reaction"
    assert reply_entry["content"] == "thumbsup"

    # Step 6: Verify hash chain integrity
    assert reply_entry["prev_hash"] == agent_entry["entry_hash"]
    assert reply_entry["entry_hash"] != ""
    assert reply_entry["entry_hash"] != reply_entry["prev_hash"]


async def test_generate_then_text_reply(client: AsyncClient) -> None:
    """Generate brief, reply with a text comment, verify chain."""

    resp = await client.post(
        "/api/v1/internal/brief/generate",
        json={"tenant_id": "tenant-heaton"},
    )
    assert resp.status_code == 200
    sheet_id = resp.json()["sheet_id"]

    token = ShareToken(
        token_id="tok-e2e-text",
        sheet_id=sheet_id,
        role="comment",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
    register_token(token)

    with patch(
        "vellum.webhooks.reply_to_loop._fire_openclaw_webhook",
        new_callable=AsyncMock,
    ):
        resp = await client.post(
            f"/api/v1/sheets/{sheet_id}/reply",
            json={
                "content": "Can you reschedule the 2pm?",
                "entry_type": "human_comment",
                "token": token.token_id,
            },
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    sheet = get_sheet(sheet_id)
    assert sheet is not None
    assert len(sheet.entries) == 2
    assert sheet.entries[1].entry_type == "human_comment"
    assert sheet.entries[1].content == "Can you reschedule the 2pm?"


async def test_render_brief_returns_entries(client: AsyncClient) -> None:
    """GET /sheets/{id} returns the sheet with entries."""

    resp = await client.post(
        "/api/v1/internal/brief/generate",
        json={"tenant_id": "tenant-jesmond"},
    )
    sheet_id = resp.json()["sheet_id"]

    token = ShareToken(
        token_id="tok-e2e-render",
        sheet_id=sheet_id,
        role="read",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
    register_token(token)

    resp = await client.get(
        f"/api/v1/sheets/{sheet_id}",
        params={"token": token.token_id},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["sheet_id"] == sheet_id
    assert data["title"].startswith("Daily Brief")
    assert len(data["entries"]) == 1

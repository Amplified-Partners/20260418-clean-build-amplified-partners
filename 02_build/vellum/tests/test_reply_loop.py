"""Tests for reply-to-loop webhook.

Covers:
- Valid token + emoji -> appended to sheet
- Valid token + comment -> appended to sheet
- Invalid token -> 404
- Expired token -> 404

Devon-598da8fc | 2026-05-11
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


class TestReplyEmoji:
    """Valid token + emoji reaction -> appended to sheet."""

    async def test_emoji_reply_appended(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        with patch(
            "vellum.webhooks.reply_to_loop._fire_openclaw_webhook",
            new_callable=AsyncMock,
        ):
            resp = await client.post(
                "/api/v1/sheets/sheet-001/reply",
                json={
                    "content": "\U0001F44D",
                    "entry_type": "emoji_reaction",
                    "token": "tok-comment-valid",
                },
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["entry_hash"] != ""

    async def test_emoji_reply_appears_in_entries(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        with patch(
            "vellum.webhooks.reply_to_loop._fire_openclaw_webhook",
            new_callable=AsyncMock,
        ):
            await client.post(
                "/api/v1/sheets/sheet-001/reply",
                json={
                    "content": "\u26A0\uFE0F",
                    "entry_type": "emoji_reaction",
                    "token": "tok-comment-valid",
                },
            )

        resp = await client.get(
            "/api/v1/sheets/sheet-001/entries",
            params={"token": "tok-read-valid"},
        )
        assert resp.status_code == 200
        entries = resp.json()["entries"]
        assert len(entries) == 2
        assert entries[1]["entry_type"] == "emoji_reaction"
        assert entries[1]["content"] == "\u26A0\uFE0F"

    async def test_emoji_reply_fires_openclaw_webhook(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        with patch(
            "vellum.webhooks.reply_to_loop._fire_openclaw_webhook",
            new_callable=AsyncMock,
        ) as mock_webhook:
            await client.post(
                "/api/v1/sheets/sheet-001/reply",
                json={
                    "content": "\u2753",
                    "entry_type": "emoji_reaction",
                    "token": "tok-comment-valid",
                },
            )
            mock_webhook.assert_awaited_once()


class TestReplyComment:
    """Valid token + text comment -> appended to sheet."""

    async def test_comment_reply_appended(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        with patch(
            "vellum.webhooks.reply_to_loop._fire_openclaw_webhook",
            new_callable=AsyncMock,
        ):
            resp = await client.post(
                "/api/v1/sheets/sheet-001/reply",
                json={
                    "content": "Looks good, thanks!",
                    "entry_type": "human_comment",
                    "token": "tok-comment-valid",
                },
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    async def test_comment_updates_hash_chain(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        with patch(
            "vellum.webhooks.reply_to_loop._fire_openclaw_webhook",
            new_callable=AsyncMock,
        ):
            await client.post(
                "/api/v1/sheets/sheet-001/reply",
                json={
                    "content": "Can you move the 2pm?",
                    "entry_type": "human_comment",
                    "token": "tok-comment-valid",
                },
            )

        resp = await client.get(
            "/api/v1/sheets/sheet-001/entries",
            params={"token": "tok-read-valid"},
        )
        entries = resp.json()["entries"]
        assert len(entries) == 2
        assert entries[1]["prev_hash"] == entries[0]["entry_hash"]


class TestInvalidToken:
    """Invalid token -> 404 (no information leak)."""

    async def test_nonexistent_token_returns_404(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.post(
            "/api/v1/sheets/sheet-001/reply",
            json={
                "content": "thumbsup",
                "entry_type": "emoji_reaction",
                "token": "tok-does-not-exist",
            },
        )
        assert resp.status_code == 404

    async def test_wrong_sheet_token_returns_404(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.post(
            "/api/v1/sheets/sheet-wrong/reply",
            json={
                "content": "thumbsup",
                "entry_type": "emoji_reaction",
                "token": "tok-comment-valid",
            },
        )
        assert resp.status_code == 404

    async def test_read_only_token_cannot_reply(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.post(
            "/api/v1/sheets/sheet-001/reply",
            json={
                "content": "thumbsup",
                "entry_type": "emoji_reaction",
                "token": "tok-read-valid",
            },
        )
        assert resp.status_code == 404

    async def test_invalid_token_on_get_entries(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.get(
            "/api/v1/sheets/sheet-001/entries",
            params={"token": "tok-bogus"},
        )
        assert resp.status_code == 404

    async def test_invalid_token_on_render_brief(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.get(
            "/api/v1/sheets/sheet-001",
            params={"token": "tok-bogus"},
        )
        assert resp.status_code == 404


class TestExpiredToken:
    """Expired token -> 404."""

    async def test_expired_token_reply_returns_404(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.post(
            "/api/v1/sheets/sheet-001/reply",
            json={
                "content": "thumbsup",
                "entry_type": "emoji_reaction",
                "token": "tok-expired",
            },
        )
        assert resp.status_code == 404

    async def test_expired_token_entries_returns_404(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.get(
            "/api/v1/sheets/sheet-001/entries",
            params={"token": "tok-expired"},
        )
        assert resp.status_code == 404

    async def test_expired_token_render_returns_404(
        self, client: AsyncClient, populated_stores: None
    ) -> None:
        resp = await client.get(
            "/api/v1/sheets/sheet-001",
            params={"token": "tok-expired"},
        )
        assert resp.status_code == 404

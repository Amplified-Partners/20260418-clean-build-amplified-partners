"""Shared pytest fixtures for Vellum Brief mode tests.

Mocks all external services: Stripe, Google Calendar, SearXNG, LiteLLM, OpenClaw.
Provides test tenant, sheet, token, and FastAPI async client fixtures.

Devon-598da8fc | 2026-05-11
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI

from vellum.models.entry import SheetEntry
from vellum.models.sheet import Sheet, SheetMeta, Tenant
from vellum.models.token import ShareToken
from vellum.routes import router
from vellum.webhooks.reply_to_loop import (
    clear_stores,
    register_sheet,
    register_token,
)


# ---------------------------------------------------------------------------
# FastAPI app for testing
# ---------------------------------------------------------------------------

def create_test_app() -> FastAPI:
    """Create a FastAPI app wired with Vellum routes."""
    app = FastAPI(title="Vellum Test")
    app.include_router(router)
    return app


# ---------------------------------------------------------------------------
# Tenant + sheet + token fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def test_tenant() -> Tenant:
    return Tenant(id="tenant-jesmond", name="jesmond")


@pytest.fixture()
def test_sheet_meta(test_tenant: Tenant) -> SheetMeta:
    return SheetMeta(
        id="sheet-001",
        tenant_id=test_tenant.id,
        title="Daily Brief — Jesmond",
        mode="brief",
        created_by="vellum-generator",
    )


@pytest.fixture()
def seed_entry(test_sheet_meta: SheetMeta) -> SheetEntry:
    """An initial agent-written entry to seed the sheet."""
    return SheetEntry(
        sheet_id=test_sheet_meta.id,
        author="vellum-generator",
        content="Good morning! Here is your daily brief.",
        entry_type="agent_write",
    )


@pytest.fixture()
def test_sheet(test_sheet_meta: SheetMeta, seed_entry: SheetEntry) -> Sheet:
    sheet = Sheet(
        meta=test_sheet_meta,
        entries=[seed_entry],
        latest_hash=seed_entry.entry_hash,
    )
    return sheet


@pytest.fixture()
def comment_token(test_sheet_meta: SheetMeta) -> ShareToken:
    """A valid comment-role token."""
    return ShareToken(
        token_id="tok-comment-valid",
        sheet_id=test_sheet_meta.id,
        role="comment",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )


@pytest.fixture()
def read_token(test_sheet_meta: SheetMeta) -> ShareToken:
    """A valid read-only token."""
    return ShareToken(
        token_id="tok-read-valid",
        sheet_id=test_sheet_meta.id,
        role="read",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )


@pytest.fixture()
def expired_token(test_sheet_meta: SheetMeta) -> ShareToken:
    """An expired token."""
    return ShareToken(
        token_id="tok-expired",
        sheet_id=test_sheet_meta.id,
        role="comment",
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )


@pytest.fixture(autouse=True)
def _reset_stores() -> None:
    """Clear in-memory stores before every test."""
    clear_stores()


@pytest.fixture()
def populated_stores(
    test_sheet: Sheet,
    comment_token: ShareToken,
    read_token: ShareToken,
    expired_token: ShareToken,
) -> None:
    """Register the standard test sheet and tokens in the in-memory store."""
    register_sheet(test_sheet)
    register_token(comment_token)
    register_token(read_token)
    register_token(expired_token)


# ---------------------------------------------------------------------------
# FastAPI async client
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    app = create_test_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ---------------------------------------------------------------------------
# External service mocks
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_stripe() -> AsyncMock:
    """Mock Stripe API responses — returns stub transaction data."""
    mock = AsyncMock()
    mock.return_value = {
        "transactions": [
            {"id": "txn_001", "amount": 15000, "currency": "gbp", "description": "Job payment"},
            {"id": "txn_002", "amount": -2500, "currency": "gbp", "description": "Fuel purchase"},
        ],
        "balance": 42500,
    }
    return mock


@pytest.fixture()
def mock_calendar() -> AsyncMock:
    """Mock Google Calendar API responses — returns stub job schedule."""
    mock = AsyncMock()
    mock.return_value = {
        "events": [
            {"id": "evt_001", "summary": "Boiler install - 14 Acacia Ave", "start": "09:00", "end": "12:00"},
            {"id": "evt_002", "summary": "Quote visit - 7 Park Rd", "start": "14:00", "end": "15:00"},
        ],
    }
    return mock


@pytest.fixture()
def mock_searxng() -> AsyncMock:
    """Mock SearXNG responses — returns stub weather and demand signals."""
    mock = AsyncMock()
    mock.return_value = {
        "weather": {"temp_c": 14, "condition": "Partly cloudy", "wind_mph": 8},
        "demand_signals": ["Boiler servicing demand up 15% this week"],
    }
    return mock


@pytest.fixture()
def mock_litellm() -> AsyncMock:
    """Mock LiteLLM synthesiser responses — returns a pre-composed brief."""
    mock = AsyncMock()
    mock.return_value = (
        "Good morning! You have 2 jobs today. "
        "Yesterday you took in \u00a3150 and spent \u00a325 on fuel. "
        "Weather: 14\u00b0C, partly cloudy."
    )
    return mock


@pytest.fixture()
def mock_openclaw_webhook() -> AsyncMock:
    """Mock the OpenClaw webhook POST to capture calls without network."""
    return AsyncMock()

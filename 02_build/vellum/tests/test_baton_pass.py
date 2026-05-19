"""Tests for baton pass — API route + cron automation wiring.

Covers:
- BatonPass model creation and field defaults
- POST /api/v1/baton endpoint
- GET /api/v1/baton/latest endpoint
- baton_pass entry type on sheets
- httpx.post wiring in morning/evening briefs (mocked)

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ["VELLUM_DEV_MODE"] = "1"

from vellum.app import app
from vellum.cron.briefs import generate_evening_brief, generate_morning_brief
from vellum.models.baton import BatonPass, WorkReference
from vellum.storage import init_store


# ── Model tests ──


class TestBatonPassModel:
    def test_defaults(self) -> None:
        baton = BatonPass()
        assert baton.id
        assert baton.tenant_id == "ewan"
        assert baton.what_happened == ""
        assert baton.implications == ""
        assert baton.actions_required == []
        assert baton.work_refs == []
        assert baton.context_saturation_pct == 0.0
        assert baton.epistemic_tier == "INTUITED"

    def test_full_payload(self) -> None:
        baton = BatonPass(
            session_id="devin-abc123",
            agent_id="Devon-58ca",
            tenant_id="ewan",
            what_happened="Wired httpx.post into morning briefs",
            implications="Daily Brief automation is now closed-loop",
            actions_required=["Deploy to Beast", "Verify cron schedule"],
            work_refs=[
                WorkReference(kind="pr", ref="#139", url="https://github.com/Amplified-Partners/clean-build/pull/139"),
            ],
            context_saturation_pct=42.5,
            next_agent="Devon-next",
            epistemic_tier="STRUCTURED",
        )
        assert baton.session_id == "devin-abc123"
        assert baton.agent_id == "Devon-58ca"
        assert len(baton.work_refs) == 1
        assert baton.work_refs[0].kind == "pr"
        assert baton.epistemic_tier == "STRUCTURED"

    def test_work_reference_defaults(self) -> None:
        ref = WorkReference()
        assert ref.kind == "other"
        assert ref.ref == ""
        assert ref.url == ""


# ── API route tests ──


@pytest_asyncio.fixture
async def client():
    await init_store()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c


class TestBatonPassAPI:
    @pytest.mark.asyncio
    async def test_receive_baton_creates_entry(self, client) -> None:
        # First create a brief sheet so the baton has somewhere to land
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Test brief", "title": "Test Brief"},
        )
        assert gen.status_code == 200

        resp = await client.post(
            "/api/v1/baton",
            json={
                "session_id": "devin-test-session",
                "agent_id": "Devon-test",
                "tenant_id": "ewan",
                "what_happened": "Ran the test suite",
                "implications": "All tests pass",
                "actions_required": ["Review PR", "Merge"],
                "context_saturation_pct": 35.0,
                "next_agent": "Devon-next",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "baton_id" in data
        assert "entry_id" in data
        assert "sheet_id" in data
        assert data["next_agent"] == "Devon-next"

    @pytest.mark.asyncio
    async def test_receive_baton_creates_sheet_if_none(self, client) -> None:
        resp = await client.post(
            "/api/v1/baton",
            json={
                "session_id": "devin-orphan",
                "agent_id": "Devon-orphan",
                "tenant_id": "orphan-tenant",
                "what_happened": "Baton with no existing sheet",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["sheet_id"]

    @pytest.mark.asyncio
    async def test_get_latest_baton(self, client) -> None:
        # Create a brief + baton
        await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Brief", "title": "T"},
        )
        await client.post(
            "/api/v1/baton",
            json={
                "session_id": "devin-latest",
                "agent_id": "Devon-latest",
                "what_happened": "Latest baton test",
            },
        )

        resp = await client.get("/api/v1/baton/latest?tenant_id=ewan")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["author"] == "Devon-latest"
        assert "Latest baton test" in data["content"]

    @pytest.mark.asyncio
    async def test_get_latest_baton_404_when_none(self, client) -> None:
        resp = await client.get("/api/v1/baton/latest?tenant_id=no-batons-here")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_baton_content_has_three_sections(self, client) -> None:
        await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Brief", "title": "T"},
        )
        resp = await client.post(
            "/api/v1/baton",
            json={
                "session_id": "devin-sections",
                "agent_id": "Devon-sections",
                "what_happened": "Built the automation",
                "implications": "Loop is closed",
                "actions_required": ["Deploy", "Monitor"],
            },
        )
        data = resp.json()

        # Fetch the sheet to verify entry content
        sheet_resp = await client.get(f"/api/v1/sheets/{data['sheet_id']}")
        sheet_data = sheet_resp.json()
        baton_entries = [e for e in sheet_data["entries"] if e["entry_type"] == "baton_pass"]
        assert len(baton_entries) >= 1

        content = baton_entries[-1]["content"]
        assert "What Happened" in content
        assert "Built the automation" in content
        assert "Implications" in content
        assert "Loop is closed" in content
        assert "Actions Required" in content
        assert "Deploy" in content


# ── Cron automation wiring tests ──


class TestCronAutomation:
    @pytest.mark.asyncio
    async def test_morning_brief_posts_to_ledger(self) -> None:
        """Morning brief fires httpx.post to the Ledger endpoint."""
        await init_store()

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok", "sheet_id": "test-123"}
        mock_response.raise_for_status = AsyncMock()

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("vellum.cron.briefs.httpx.AsyncClient", return_value=mock_client):
            sheet_id = await generate_morning_brief()

        assert sheet_id
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert "/api/v1/sheets/generate" in call_args[0][0]
        payload = call_args[1]["json"]
        assert payload["author"] == "vellum-cron"
        assert "Morning Brief" in payload["title"]

    @pytest.mark.asyncio
    async def test_evening_brief_posts_to_ledger(self) -> None:
        """Evening brief fires httpx.post to the Ledger endpoint."""
        await init_store()

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok", "sheet_id": "test-456"}
        mock_response.raise_for_status = AsyncMock()

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("vellum.cron.briefs.httpx.AsyncClient", return_value=mock_client):
            sheet_id = await generate_evening_brief()

        assert sheet_id
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert "/api/v1/sheets/generate" in call_args[0][0]
        payload = call_args[1]["json"]
        assert "Evening Wrap" in payload["title"]

    @pytest.mark.asyncio
    async def test_brief_survives_ledger_connection_failure(self) -> None:
        """Brief sheet is created even if Ledger POST fails (graceful degradation)."""
        await init_store()

        with patch("vellum.cron.briefs._post_to_ledger", new_callable=AsyncMock, return_value=None):
            sheet_id = await generate_morning_brief()

        # Sheet still created despite POST failure
        assert sheet_id

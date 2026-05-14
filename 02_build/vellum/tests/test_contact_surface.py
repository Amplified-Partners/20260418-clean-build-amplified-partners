"""Tests for the Vellum contact surface.

Covers: hash chain, additive guard, intent routing, storage, API routes.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ["VELLUM_DEV_MODE"] = "1"

from vellum.app import app
from vellum.canvas.additive import AdditiveGuard
from vellum.canvas.hash_chain import HashChain
from vellum.intent.router import classify_reply
from vellum.models.entry import SheetEntry
from vellum.models.sheet import SheetMeta
from vellum.storage import get_store, init_store
from vellum.storage.memory import MemorySheetStore


# ── Hash chain ──


class TestHashChain:
    def test_compute_next_hash(self) -> None:
        h = HashChain.compute_next_hash("", "hello")
        assert len(h) == 64
        assert h == HashChain.compute_next_hash("", "hello")

    def test_different_content_different_hash(self) -> None:
        h1 = HashChain.compute_next_hash("", "hello")
        h2 = HashChain.compute_next_hash("", "world")
        assert h1 != h2

    def test_verify_entry(self) -> None:
        entry = SheetEntry(sheet_id="s1", author="test", content="hello")
        assert HashChain.verify_entry(entry)

    def test_validate_chain(self) -> None:
        e1 = SheetEntry(sheet_id="s1", author="a", content="first", prev_hash="")
        e2 = SheetEntry(
            sheet_id="s1", author="b", content="second", prev_hash=e1.entry_hash
        )
        assert HashChain.validate_chain([e1, e2])

    def test_tampered_chain_fails(self) -> None:
        e1 = SheetEntry(sheet_id="s1", author="a", content="first", prev_hash="")
        e2 = SheetEntry(
            sheet_id="s1", author="b", content="second", prev_hash="wrong"
        )
        assert not HashChain.validate_chain([e1, e2])


# ── Additive guard ──


class TestAdditiveGuard:
    def test_first_write_allowed(self) -> None:
        entry = SheetEntry(sheet_id="s1", author="a", content="hello")
        assert AdditiveGuard.validate_write(entry, [])

    def test_duplicate_id_rejected(self) -> None:
        entry = SheetEntry(id="dup", sheet_id="s1", author="a", content="hello")
        assert not AdditiveGuard.validate_write(entry, [entry])

    def test_wrong_sheet_rejected(self) -> None:
        e1 = SheetEntry(sheet_id="s1", author="a", content="hello")
        e2 = SheetEntry(sheet_id="s2", author="a", content="world")
        assert not AdditiveGuard.validate_write(e2, [e1])


# ── Intent router ──


class TestIntentRouter:
    def test_thumbsup_acknowledge(self) -> None:
        intent = classify_reply("\U0001f44d")
        assert intent.kind == "acknowledge"
        assert intent.confidence >= 0.9

    def test_warning_escalate(self) -> None:
        intent = classify_reply("\u26a0\ufe0f")
        assert intent.kind == "escalate"

    def test_question_clarify(self) -> None:
        intent = classify_reply("\u2753")
        assert intent.kind == "clarify"

    def test_fix_creates_task(self) -> None:
        intent = classify_reply("fix the CI on clean-build")
        assert intent.kind == "create_task"

    def test_cancel_calendar(self) -> None:
        intent = classify_reply("cancel the 2pm")
        assert intent.kind == "calendar_action"

    def test_park_task(self) -> None:
        intent = classify_reply("park this for now")
        assert intent.kind == "park_task"

    def test_decision(self) -> None:
        intent = classify_reply("approved, go ahead")
        assert intent.kind == "decision"

    def test_general_fallback(self) -> None:
        intent = classify_reply("sounds good mate")
        assert intent.kind == "general_reply"
        assert intent.confidence <= 0.6


# ── Storage ──


@pytest_asyncio.fixture
async def store():
    s = await init_store()
    yield s
    if isinstance(s, MemorySheetStore):
        s.clear()


class TestStorage:
    @pytest.mark.asyncio
    async def test_create_and_get_sheet(self, store) -> None:
        meta = SheetMeta(title="Test", tenant_id="ewan", created_by="test")
        sheet = await store.create_sheet(meta)
        assert sheet.meta.id == meta.id

        fetched = await store.get_sheet(meta.id)
        assert fetched is not None
        assert fetched.meta.title == "Test"

    @pytest.mark.asyncio
    async def test_append_entry(self, store) -> None:
        meta = SheetMeta(title="Test", tenant_id="ewan", created_by="test")
        await store.create_sheet(meta)

        entry = SheetEntry(sheet_id=meta.id, author="agent-1", content="hello")
        await store.append_entry(meta.id, entry)

        sheet = await store.get_sheet(meta.id)
        assert len(sheet.entries) == 1
        assert sheet.latest_hash == entry.entry_hash

    @pytest.mark.asyncio
    async def test_decisions_query(self, store) -> None:
        meta = SheetMeta(title="Test", tenant_id="ewan", created_by="test")
        await store.create_sheet(meta)

        entry = SheetEntry(
            sheet_id=meta.id,
            author="Ewan",
            content="approved — go with option A",
            entry_type="decision",
        )
        await store.append_entry(meta.id, entry)

        decisions = await store.get_decisions("ewan")
        assert len(decisions) == 1
        assert decisions[0].content == "approved — go with option A"

    @pytest.mark.asyncio
    async def test_list_sheets(self, store) -> None:
        m1 = SheetMeta(title="A", tenant_id="ewan", created_by="t")
        m2 = SheetMeta(title="B", tenant_id="ewan", created_by="t")
        await store.create_sheet(m1)
        await store.create_sheet(m2)

        sheets = await store.list_sheets("ewan")
        assert len(sheets) == 2


# ── API routes ──


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as c:
        yield c


class TestAPI:
    @pytest.mark.asyncio
    async def test_generate_brief(self, client) -> None:
        resp = await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Test brief content", "title": "Test Brief"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "sheet_id" in data

    @pytest.mark.asyncio
    async def test_list_sheets(self, client) -> None:
        resp = await client.get("/api/v1/sheets")
        assert resp.status_code == 200
        data = resp.json()
        assert "sheets" in data

    @pytest.mark.asyncio
    async def test_reply_with_intent(self, client) -> None:
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Brief", "title": "T"},
        )
        sheet_id = gen.json()["sheet_id"]

        resp = await client.post(
            f"/api/v1/sheets/{sheet_id}/reply",
            json={"content": "fix the deployment", "author": "Ewan"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["intent"] == "create_task"
        assert data["entry_type"] == "task_created"

    @pytest.mark.asyncio
    async def test_emoji_reply(self, client) -> None:
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Brief", "title": "T"},
        )
        sheet_id = gen.json()["sheet_id"]

        resp = await client.post(
            f"/api/v1/sheets/{sheet_id}/reply",
            json={"content": "\U0001f44d", "author": "Ewan"},
        )
        data = resp.json()
        assert data["intent"] == "acknowledge"

    @pytest.mark.asyncio
    async def test_read_receipt(self, client) -> None:
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Brief", "title": "T"},
        )
        sheet_id = gen.json()["sheet_id"]

        resp = await client.post(
            f"/api/v1/sheets/{sheet_id}/read-receipt?author=Devon-54b0",
        )
        data = resp.json()
        assert data["status"] == "ok"
        assert data["author"] == "Devon-54b0"

    @pytest.mark.asyncio
    async def test_decisions_endpoint(self, client) -> None:
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Brief", "title": "T"},
        )
        sheet_id = gen.json()["sheet_id"]

        await client.post(
            f"/api/v1/sheets/{sheet_id}/reply",
            json={"content": "approved, go ahead", "author": "Ewan"},
        )

        resp = await client.get("/api/v1/decisions")
        data = resp.json()
        assert data["count"] >= 1

    @pytest.mark.asyncio
    async def test_dashboard_renders(self, client) -> None:
        resp = await client.get("/")
        assert resp.status_code == 200
        assert "Vellum" in resp.text

    @pytest.mark.asyncio
    async def test_sheet_detail_renders(self, client) -> None:
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"content": "Test", "title": "Detail Test"},
        )
        sheet_id = gen.json()["sheet_id"]

        resp = await client.get(f"/sheet/{sheet_id}")
        assert resp.status_code == 200
        assert "Detail Test" in resp.text

    @pytest.mark.asyncio
    async def test_sheet_not_found(self, client) -> None:
        resp = await client.get("/api/v1/sheets/nonexistent")
        assert resp.status_code == 404

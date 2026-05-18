"""Tests for the Brain measured loop — all four pieces.

1. Spine server (register, read, update from baton)
2. Context server (assemble full packet)
3. Memory extractor (extract candidates from entries)
4. Ingestion gate (admit/reject/quarantine)
5. Integration: full measured loop cycle

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import os

os.environ["VELLUM_DEV_MODE"] = "1"

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from vellum.app import app
from vellum.models.entry import SheetEntry
from vellum.models.memory import MemoryCandidate
from vellum.services.ingestion_gate import evaluate_candidate, run_gate
from vellum.services.memory_extractor import extract_candidates
from vellum.services.spine_server import clear_spines


@pytest_asyncio.fixture
async def client():
    from vellum.storage import init_store, get_store
    store = await init_store()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    await store.close()


@pytest.fixture(autouse=True)
def _reset_spines():
    """Clear spine store between tests."""
    clear_spines()
    yield
    clear_spines()


# -----------------------------------------------------------------------
# 1. Spine server
# -----------------------------------------------------------------------


class TestSpineServer:
    """Test portable spine registration, reading, and baton updates."""

    @pytest.mark.asyncio
    @pytest.mark.asyncio
    async def test_register_and_read_spine(self, client: AsyncClient):
        resp = await client.put(
            "/api/v1/brain/spine",
            json={
                "agent_id": "devon-58ca",
                "agent_name": "Devon",
                "lens": "infrastructure",
                "role": "systems coordinator",
                "procedural_constraints": ["no force push to main"],
                "experience_line": "built vellum plumbing",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["agent_id"] == "devon-58ca"

        resp2 = await client.get(
            "/api/v1/brain/spine", params={"agent_id": "devon-58ca"}
        )
        assert resp2.status_code == 200
        spine = resp2.json()["spine"]
        assert spine["agent_id"] == "devon-58ca"
        assert spine["lens"] == "infrastructure"
        assert spine["role"] == "systems coordinator"
        assert "no force push to main" in spine["procedural_constraints"]

    @pytest.mark.asyncio
    async def test_spine_not_found(self, client: AsyncClient):
        resp = await client.get(
            "/api/v1/brain/spine", params={"agent_id": "nonexistent"}
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_list_spines(self, client: AsyncClient):
        await client.put(
            "/api/v1/brain/spine",
            json={"agent_id": "agent-a", "agent_name": "Alpha"},
        )
        await client.put(
            "/api/v1/brain/spine",
            json={"agent_id": "agent-b", "agent_name": "Bravo"},
        )
        resp = await client.get("/api/v1/brain/spines")
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] == 2

    @pytest.mark.asyncio
    async def test_patch_spine_from_baton(self, client: AsyncClient):
        await client.put(
            "/api/v1/brain/spine",
            json={"agent_id": "devon-test", "agent_name": "Devon"},
        )
        resp = await client.patch(
            "/api/v1/brain/spine",
            json={
                "agent_id": "devon-test",
                "failed_paths": ["tried rsync, permission denied"],
                "if_then_lessons": [
                    "IF Beast SSH fails THEN check tailscale first"
                ],
                "experience_line": "wired cron + baton pass",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["failure_patterns_count"] == 1
        assert data["if_then_lessons_count"] == 1

        resp2 = await client.get(
            "/api/v1/brain/spine", params={"agent_id": "devon-test"}
        )
        spine = resp2.json()["spine"]
        assert spine["experience_line"] == "wired cron + baton pass"
        assert len(spine["failure_patterns"]) == 1
        assert spine["failure_patterns"][0]["description"] == "tried rsync, permission denied"

    @pytest.mark.asyncio
    async def test_patch_increments_failure_count(self, client: AsyncClient):
        await client.put(
            "/api/v1/brain/spine",
            json={"agent_id": "devon-inc"},
        )
        await client.patch(
            "/api/v1/brain/spine",
            json={
                "agent_id": "devon-inc",
                "failed_paths": ["SSH timeout"],
            },
        )
        await client.patch(
            "/api/v1/brain/spine",
            json={
                "agent_id": "devon-inc",
                "failed_paths": ["SSH timeout"],
            },
        )
        resp = await client.get(
            "/api/v1/brain/spine", params={"agent_id": "devon-inc"}
        )
        spine = resp.json()["spine"]
        assert spine["failure_patterns"][0]["times_observed"] == 2

    @pytest.mark.asyncio
    async def test_patch_nonexistent_spine_404(self, client: AsyncClient):
        resp = await client.patch(
            "/api/v1/brain/spine",
            json={"agent_id": "ghost", "failed_paths": ["x"]},
        )
        assert resp.status_code == 404


# -----------------------------------------------------------------------
# 2. Context server
# -----------------------------------------------------------------------


class TestContextServer:
    """Test context packet assembly."""

    @pytest.mark.asyncio
    async def test_context_packet_empty(self, client: AsyncClient):
        await client.put(
            "/api/v1/brain/spine",
            json={"agent_id": "devon-ctx", "lens": "testing"},
        )
        resp = await client.get(
            "/api/v1/brain/context", params={"agent_id": "devon-ctx"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["agent_id"] == "devon-ctx"
        assert data["spine"] is not None
        assert data["spine"]["lens"] == "testing"
        assert isinstance(data["recent_entries"], list)
        assert isinstance(data["decisions"], list)
        assert isinstance(data["unread"], list)

    @pytest.mark.asyncio
    async def test_context_packet_no_spine(self, client: AsyncClient):
        resp = await client.get(
            "/api/v1/brain/context", params={"agent_id": "unknown-agent"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["spine"] is None

    @pytest.mark.asyncio
    async def test_context_includes_entries(self, client: AsyncClient):
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"title": "Test Brief", "content": "Initial content"},
        )
        sheet_id = gen.json()["sheet_id"]

        await client.post(
            f"/api/v1/sheets/{sheet_id}/entries",
            json={
                "sheet_id": sheet_id,
                "content": "Agent wrote something useful",
                "author": "devon-ctx2",
            },
        )

        resp = await client.get(
            "/api/v1/brain/context", params={"agent_id": "devon-ctx2"}
        )
        data = resp.json()
        assert data["counts"]["recent_entries"] >= 1


# -----------------------------------------------------------------------
# 3. Memory extractor
# -----------------------------------------------------------------------


class TestMemoryExtractor:
    """Test memory candidate extraction from entries."""

    def test_extract_failure(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="devon",
            content="Tried rsync to Beast but it failed with permission denied error",
            entry_type="agent_write",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "failed_approach" in kinds

    def test_extract_correction(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="ewan",
            content="That was wrong — corrected the endpoint to use POST not GET",
            entry_type="human_comment",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "correction" in kinds

    def test_extract_lesson(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="devon",
            content="Lesson learned: if the CI fails on Linear ticket then skip it next time",
            entry_type="agent_write",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "if_then_lesson" in kinds

    def test_extract_explicit_remember(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="ewan",
            content="Remember this: Bob always wants the report on Monday morning",
            entry_type="human_comment",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "explicit_remember" in kinds

    def test_extract_preference(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="ewan",
            content="I prefer using httpx instead of requests for async work",
            entry_type="human_comment",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "preference" in kinds

    def test_extract_procedure_improvement(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="devon",
            content="Found a better way to handle the deployment — streamlined the Docker build",
            entry_type="agent_write",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "procedure_improvement" in kinds

    def test_extract_tool_quirk(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="devon",
            content="Watch out for this gotcha: the Linear API returns 200 even on partial failure",
            entry_type="agent_write",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "tool_quirk" in kinds

    def test_extract_baton_pass_outcome(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="devon",
            content="PR merged and deployed successfully, tests passed, CI green",
            entry_type="baton_pass",
        )
        candidates = extract_candidates(entry)
        kinds = [c.kind for c in candidates]
        assert "task_outcome" in kinds

    def test_skip_non_scannable(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="system",
            content="Read receipt for entry xyz",
            entry_type="read_receipt",
        )
        candidates = extract_candidates(entry)
        assert len(candidates) == 0

    def test_skip_empty_content(self):
        entry = SheetEntry(
            sheet_id="s1",
            author="devon",
            content="   ",
            entry_type="agent_write",
        )
        candidates = extract_candidates(entry)
        assert len(candidates) == 0

    @pytest.mark.asyncio
    async def test_extract_via_api(self, client: AsyncClient):
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={"title": "Memory Test Brief", "content": "Everything failed and broke"},
        )
        sheet_id = gen.json()["sheet_id"]

        resp = await client.post(
            "/api/v1/brain/extract",
            json={"sheet_id": sheet_id},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] >= 1
        assert any(c["kind"] == "failed_approach" for c in data["candidates"])

    @pytest.mark.asyncio
    async def test_extract_sheet_not_found(self, client: AsyncClient):
        resp = await client.post(
            "/api/v1/brain/extract",
            json={"sheet_id": "nonexistent"},
        )
        assert resp.status_code == 404


# -----------------------------------------------------------------------
# 4. Ingestion gate
# -----------------------------------------------------------------------


class TestIngestionGate:
    """Test the ingestion gate — admit/reject/quarantine decisions."""

    def test_admit_correction(self):
        candidate = MemoryCandidate(
            source_entry_id="e1",
            source_sheet_id="s1",
            kind="correction",
            content="The endpoint was wrong — corrected to POST",
            confidence=0.8,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "ADMIT"
        assert decision.changes_future_behaviour is True

    def test_admit_failed_approach(self):
        candidate = MemoryCandidate(
            source_entry_id="e2",
            source_sheet_id="s1",
            kind="failed_approach",
            content="Tried rsync but permission denied on Beast",
            confidence=0.7,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "ADMIT"

    def test_admit_if_then_lesson(self):
        candidate = MemoryCandidate(
            source_entry_id="e3",
            source_sheet_id="s1",
            kind="if_then_lesson",
            content="IF Beast SSH fails THEN check tailscale first",
            confidence=0.85,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "ADMIT"

    def test_reject_low_confidence(self):
        candidate = MemoryCandidate(
            source_entry_id="e4",
            source_sheet_id="s1",
            kind="preference",
            content="Maybe use a different approach next time",
            confidence=0.3,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "REJECT"
        assert "confidence_below_floor" in decision.reason_codes

    def test_reject_trivia(self):
        candidate = MemoryCandidate(
            source_entry_id="e5",
            source_sheet_id="s1",
            kind="preference",
            content="ok fine",
            confidence=0.9,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "REJECT"
        assert "content_too_short_trivia" in decision.reason_codes

    def test_reject_pleasantry(self):
        candidate = MemoryCandidate(
            source_entry_id="e6",
            source_sheet_id="s1",
            kind="preference",
            content="thank you very much for that",
            confidence=0.9,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "REJECT"
        assert "social_pleasantry_noise" in decision.reason_codes

    def test_quarantine_raw_dump(self):
        candidate = MemoryCandidate(
            source_entry_id="e7",
            source_sheet_id="s1",
            kind="correction",
            content="x" * 6000,
            confidence=0.8,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "QUARANTINE"
        assert "raw_dump_needs_summarisation" in decision.reason_codes

    def test_reject_low_signal_insufficient_confidence(self):
        candidate = MemoryCandidate(
            source_entry_id="e8",
            source_sheet_id="s1",
            kind="preference",
            content="I think maybe we could try something different next time",
            confidence=0.55,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "REJECT"
        assert "low_signal_kind_insufficient_confidence" in decision.reason_codes

    def test_admit_low_signal_high_confidence(self):
        candidate = MemoryCandidate(
            source_entry_id="e9",
            source_sheet_id="s1",
            kind="preference",
            content="Always use httpx instead of requests for async — confirmed faster",
            confidence=0.85,
        )
        decision = evaluate_candidate(candidate)
        assert decision.verdict == "ADMIT"

    def test_batch_gate(self):
        candidates = [
            MemoryCandidate(
                source_entry_id="b1",
                source_sheet_id="s1",
                kind="correction",
                content="Fixed the wrong endpoint path",
                confidence=0.8,
            ),
            MemoryCandidate(
                source_entry_id="b2",
                source_sheet_id="s1",
                kind="preference",
                content="thanks",
                confidence=0.9,
            ),
            MemoryCandidate(
                source_entry_id="b3",
                source_sheet_id="s1",
                kind="if_then_lesson",
                content="IF deploy fails THEN check Docker logs first",
                confidence=0.9,
            ),
        ]
        decisions = run_gate(candidates)
        assert len(decisions) == 3
        verdicts = [d.verdict for d in decisions]
        assert verdicts.count("ADMIT") == 2
        assert verdicts.count("REJECT") == 1

    @pytest.mark.asyncio
    async def test_ingest_via_api(self, client: AsyncClient):
        candidates = [
            {
                "source_entry_id": "api1",
                "source_sheet_id": "s1",
                "kind": "correction",
                "content": "Fixed the deployment script to handle timeouts",
                "confidence": 0.8,
            },
            {
                "source_entry_id": "api2",
                "source_sheet_id": "s1",
                "kind": "preference",
                "content": "ok",
                "confidence": 0.9,
            },
        ]
        resp = await client.post(
            "/api/v1/brain/ingest",
            json={"candidates": candidates},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"]["admitted"] == 1
        assert data["summary"]["rejected"] == 1


# -----------------------------------------------------------------------
# 5. Integration: full measured loop cycle
# -----------------------------------------------------------------------


class TestMeasuredLoopIntegration:
    """Test the full measured loop: spine → context → extract → ingest."""

    @pytest.mark.asyncio
    async def test_full_cycle(self, client: AsyncClient):
        # Step 1: Register a spine
        await client.put(
            "/api/v1/brain/spine",
            json={
                "agent_id": "devon-loop",
                "agent_name": "Devon Loop Test",
                "lens": "integration testing",
                "role": "test agent",
            },
        )

        # Step 2: Create a brief with memory-worthy content
        gen = await client.post(
            "/api/v1/sheets/generate",
            json={
                "title": "Loop Test Brief",
                "content": "Tried to deploy but it failed with timeout error. Lesson learned: always check Docker first",
            },
        )
        sheet_id = gen.json()["sheet_id"]

        # Step 3: Get the context packet
        ctx = await client.get(
            "/api/v1/brain/context", params={"agent_id": "devon-loop"}
        )
        assert ctx.status_code == 200
        ctx_data = ctx.json()
        assert ctx_data["spine"] is not None
        assert ctx_data["counts"]["recent_entries"] >= 1

        # Step 4: Extract memory candidates
        extract = await client.post(
            "/api/v1/brain/extract",
            json={"sheet_id": sheet_id},
        )
        assert extract.status_code == 200
        candidates = extract.json()["candidates"]
        assert len(candidates) >= 1

        # Step 5: Run the ingestion gate
        ingest = await client.post(
            "/api/v1/brain/ingest",
            json={"candidates": candidates},
        )
        assert ingest.status_code == 200
        ingest_data = ingest.json()
        assert ingest_data["summary"]["total"] >= 1
        assert ingest_data["summary"]["admitted"] >= 1

        # Step 6: Update spine from the learnings
        patch = await client.patch(
            "/api/v1/brain/spine",
            json={
                "agent_id": "devon-loop",
                "failed_paths": ["deploy timeout"],
                "if_then_lessons": ["IF deploy fails THEN check Docker first"],
            },
        )
        assert patch.status_code == 200

        # Step 7: Verify spine has the learnings
        spine_resp = await client.get(
            "/api/v1/brain/spine", params={"agent_id": "devon-loop"}
        )
        spine = spine_resp.json()["spine"]
        assert len(spine["failure_patterns"]) == 1
        assert len(spine["if_then_lessons"]) == 1
        assert spine["failure_patterns"][0]["description"] == "deploy timeout"

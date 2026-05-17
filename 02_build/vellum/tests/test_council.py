"""Council of Three — unit tests.

Tests the council engine, context builder, and route without
hitting actual LLM endpoints (mocked via httpx responder).

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from vellum.council.context import CouncilContext, build_council_prompt
from vellum.council.engine import (
    CouncilMember,
    MemberResponse,
    Verdict,
    _classify_agreement,
    run_council,
)


# --- Context builder tests ---


class TestContextBuilder:

    def test_builds_minimal_prompt(self):
        ctx = CouncilContext(decision_statement="Should we deploy today?")
        prompt = build_council_prompt(ctx)
        assert "## Decision" in prompt
        assert "Should we deploy today?" in prompt
        assert "plan before answering" in prompt.lower() or "Plan before answering" in prompt

    def test_includes_options_with_do_nothing(self):
        ctx = CouncilContext(
            decision_statement="Which database?",
            options=["PostgreSQL", "MongoDB"],
        )
        prompt = build_council_prompt(ctx)
        assert "PostgreSQL" in prompt
        assert "MongoDB" in prompt
        assert "Do nothing" in prompt
        assert "Defer" in prompt

    def test_includes_constraints(self):
        ctx = CouncilContext(
            decision_statement="Pick a stack",
            constraints=["Budget under £500/mo", "Must run on Beast"],
        )
        prompt = build_council_prompt(ctx)
        assert "Budget under £500/mo" in prompt
        assert "Must run on Beast" in prompt
        assert "Binding Constraints" in prompt

    def test_includes_failure_modes(self):
        ctx = CouncilContext(
            decision_statement="Deploy?",
            failure_modes=["Data loss", "Downtime > 1hr"],
        )
        prompt = build_council_prompt(ctx)
        assert "Data loss" in prompt
        assert "Downtime > 1hr" in prompt

    def test_includes_reasoning_instructions(self):
        ctx = CouncilContext(decision_statement="Any question")
        prompt = build_council_prompt(ctx)
        assert "Steelman" in prompt
        assert "uncertainty" in prompt.lower()
        assert "Do NOT ask the questioner what they prefer" in prompt

    def test_no_stated_preference(self):
        ctx = CouncilContext(decision_statement="Which option is better?")
        prompt = build_council_prompt(ctx)
        assert "prefer" not in prompt.split("Instructions")[0].lower()


# --- Agreement classifier tests ---


class TestAgreementClassifier:

    def test_all_similar_responses_unanimous(self):
        responses = [
            MemberResponse(label="A", model_id="gpt", recommendation="Deploy today because it is ready and tested", raw_response=""),
            MemberResponse(label="B", model_id="claude", recommendation="Deploy today because the tests pass and it is ready", raw_response=""),
            MemberResponse(label="C", model_id="gemini", recommendation="Deploy today because it is stable and ready", raw_response=""),
        ]
        verdict, score = _classify_agreement(responses)
        assert verdict == Verdict.UNANIMOUS
        assert score == 1.0

    def test_one_dissents_majority(self):
        responses = [
            MemberResponse(label="A", model_id="gpt", recommendation="Deploy today it is ready", raw_response=""),
            MemberResponse(label="B", model_id="claude", recommendation="Deploy today it is tested and ready", raw_response=""),
            MemberResponse(label="C", model_id="gemini", recommendation="Wait until next week for more testing coverage", raw_response=""),
        ]
        verdict, score = _classify_agreement(responses)
        assert verdict == Verdict.MAJORITY
        assert score == 0.67

    def test_all_different_split(self):
        responses = [
            MemberResponse(label="A", model_id="gpt", recommendation="Absolutely proceed immediately", raw_response=""),
            MemberResponse(label="B", model_id="claude", recommendation="Wait for quarterly review cycle", raw_response=""),
            MemberResponse(label="C", model_id="gemini", recommendation="Gather customer feedback first", raw_response=""),
        ]
        verdict, score = _classify_agreement(responses)
        assert verdict == Verdict.SPLIT
        assert score == 0.33

    def test_one_error_still_classifies(self):
        responses = [
            MemberResponse(label="A", model_id="gpt", recommendation="Deploy now it is ready", raw_response=""),
            MemberResponse(label="B", model_id="claude", recommendation="Deploy now it is ready", raw_response=""),
            MemberResponse(label="C", model_id="gemini", recommendation="", raw_response="", error="timeout"),
        ]
        verdict, score = _classify_agreement(responses)
        assert verdict in (Verdict.UNANIMOUS, Verdict.MAJORITY)

    def test_all_errors_returns_split(self):
        responses = [
            MemberResponse(label="A", model_id="gpt", recommendation="", raw_response="", error="fail"),
            MemberResponse(label="B", model_id="claude", recommendation="", raw_response="", error="fail"),
        ]
        verdict, score = _classify_agreement(responses)
        assert verdict == Verdict.SPLIT
        assert score == 0.0


# --- Engine tests (mocked LLM calls) ---


class TestCouncilEngine:

    @pytest.mark.asyncio
    async def test_run_council_all_agree(self):
        mock_response = MemberResponse(
            label="X",
            model_id="mock",
            recommendation="Deploy to production. The tests pass and the architecture is sound.",
            raw_response="Deploy to production. The tests pass and the architecture is sound.",
            latency_ms=100.0,
        )

        async def mock_call(member, prompt, system_prompt=""):
            return MemberResponse(
                label=member.label,
                model_id=member.model_id,
                recommendation="Deploy to production. The tests pass and the architecture is sound.",
                raw_response="Deploy to production. The tests pass and the architecture is sound.",
                latency_ms=100.0,
            )

        with patch("vellum.council.engine._call_model", side_effect=mock_call):
            ctx = CouncilContext(decision_statement="Should we deploy?")
            result = await run_council("Should we deploy?", ctx)

            assert result.verdict == Verdict.UNANIMOUS
            assert len(result.responses) == 3
            assert not result.escalate

    @pytest.mark.asyncio
    async def test_run_council_escalates_on_failure(self):
        async def mock_call_fail(member, prompt, system_prompt=""):
            return MemberResponse(
                label=member.label,
                model_id=member.model_id,
                recommendation="",
                raw_response="",
                latency_ms=50.0,
                error="connection refused",
            )

        with patch("vellum.council.engine._call_model", side_effect=mock_call_fail):
            ctx = CouncilContext(decision_statement="Should we deploy?")
            result = await run_council("Should we deploy?", ctx)

            assert result.escalate
            assert "responded" in result.escalation_reason


# --- Route tests (integration with store) ---


class TestCouncilRoute:

    @pytest.mark.asyncio
    async def test_council_route_stores_entries(self):
        from vellum.models.sheet import SheetMeta
        from vellum.storage import init_store, get_store

        store = await init_store()
        meta = SheetMeta(id="council-test-sheet", title="Council Test", mode="council")
        await store.create_sheet(meta)

        async def mock_call(member, prompt, system_prompt=""):
            return MemberResponse(
                label=member.label,
                model_id=member.model_id,
                recommendation=f"Model {member.label} recommends: go ahead with deployment.",
                raw_response=f"Model {member.label} recommends: go ahead with deployment.",
                latency_ms=80.0,
            )

        with patch("vellum.council.engine._call_model", side_effect=mock_call):
            from vellum.routes.council import submit_council_question, CouncilRequest

            req = CouncilRequest(
                question="Should we deploy Vellum to Beast today?",
                author="ewan",
                options=["Deploy now", "Wait until Monday"],
                constraints=["Must not break existing services"],
            )
            resp = await submit_council_question("council-test-sheet", req)

            assert resp.verdict in ("unanimous", "majority", "split")
            assert resp.question_entry_id
            assert len(resp.answer_entry_ids) == 3

            # Verify entries on sheet
            sheet = await store.get_sheet("council-test-sheet")
            assert sheet is not None
            # question + 3 answers + verdict = 5 entries
            assert len(sheet.entries) == 5
            assert sheet.entries[0].entry_type == "council_question"
            assert sheet.entries[1].entry_type == "council_answer"
            assert sheet.entries[4].entry_type == "council_answer"  # verdict
            assert "council_verdict" in sheet.entries[4].metadata.get("layer", "")

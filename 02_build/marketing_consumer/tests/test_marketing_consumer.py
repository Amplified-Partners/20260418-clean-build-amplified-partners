"""Tests for marketing_consumer — models, guardrails, state machine, dry-run, Vellum.

Covers the four required invariants from IMPLEMENTATION_PLAN.md § PR 7:
  1. Marketing publish/send remains dry-run without approval
  2. Marketing artifacts reference brain_packet_id (no forked schema)
  3. Guardrail checks block unsourced claims
  4. Vellum events emitted for each state transition

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow imports from 02_build/
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from marketing_consumer.models import (  # noqa: E402
    MarketingArtifact,
    TERMINAL_STATES,
)
from marketing_consumer.guardrails import (  # noqa: E402
    check_no_fake_persona,
    run_guardrails,
)
from marketing_consumer.state_machine import (  # noqa: E402
    InvalidTransition,
    MissingApproval,
    VALID_TRANSITIONS,
    transition,
)
from marketing_consumer.dry_run import (  # noqa: E402
    execute_send,
)
from marketing_consumer.vellum_integration import (  # noqa: E402
    STATE_EVENT_MAP,
    emit_state_event,
)
from epistemic_core.vellum_emitter import (  # noqa: E402
    MemoryVellumStore,
    VellumEmitter,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _artifact(**kw: object) -> MarketingArtifact:
    defaults: dict = {
        "title": "Test Marketing Post",
        "content": "Great insights from our analysis.",
        "brain_packet_id": "pkt-abc-123",
        "channel": "linkedin",
    }
    defaults.update(kw)
    return MarketingArtifact(**defaults)


def _emitter() -> tuple[VellumEmitter, MemoryVellumStore]:
    store = MemoryVellumStore()
    emitter = VellumEmitter(store=store)
    return emitter, store


# ===================================================================
# 1. Models
# ===================================================================


class TestModels:
    def test_artifact_defaults(self) -> None:
        a = _artifact()
        assert a.state == "draft"
        assert a.brain_packet_id == "pkt-abc-123"
        assert a.approval_signal == ""

    def test_artifact_requires_brain_packet_id(self) -> None:
        a = _artifact()
        assert a.brain_packet_id
        assert a.context_packet_id == ""

    def test_terminal_states(self) -> None:
        assert "sent" in TERMINAL_STATES
        assert "blocked" in TERMINAL_STATES
        assert len(TERMINAL_STATES) == 2


# ===================================================================
# 2. Guardrails — Radical Honesty checks
# ===================================================================


class TestGuardrails:
    def test_clean_artifact_passes(self) -> None:
        result = run_guardrails(_artifact())
        assert result.passed
        assert result.violations == []

    def test_missing_brain_packet_id_fails(self) -> None:
        a = _artifact(brain_packet_id="")
        result = run_guardrails(a)
        assert not result.passed
        assert any("brain_packet_id" in v for v in result.violations)

    def test_fake_persona_ceo_blocked(self) -> None:
        a = _artifact(persona="CEO John Smith")
        violations = check_no_fake_persona(a)
        assert len(violations) > 0
        assert any("ceo" in v.lower() for v in violations)

    def test_fake_persona_founder_blocked(self) -> None:
        a = _artifact(persona="Founder & Director")
        violations = check_no_fake_persona(a)
        assert len(violations) > 0

    def test_fake_persona_dr_blocked(self) -> None:
        a = _artifact(persona="Dr. Expert Opinion")
        violations = check_no_fake_persona(a)
        assert len(violations) > 0

    def test_normal_persona_allowed(self) -> None:
        a = _artifact(persona="Amplified Partners")
        violations = check_no_fake_persona(a)
        assert violations == []

    def test_unsourced_percentage_claim_blocked(self) -> None:
        a = _artifact(
            content="Our clients see 85% improvement in efficiency.",
            evidence_refs=[],
        )
        result = run_guardrails(a)
        assert not result.passed
        assert any("claim" in v.lower() or "evidence" in v.lower() for v in result.violations)

    def test_unsourced_study_claim_blocked(self) -> None:
        a = _artifact(
            content="Studies show that AI reduces friction by half.",
            evidence_refs=[],
        )
        result = run_guardrails(a)
        assert not result.passed

    def test_sourced_claim_passes(self) -> None:
        a = _artifact(
            content="Research shows 40% improvement in workflow speed.",
            evidence_refs=["ev-study-2026"],
        )
        result = run_guardrails(a)
        assert result.passed

    def test_no_claims_no_evidence_passes(self) -> None:
        a = _artifact(
            content="We help small businesses work smarter.",
            evidence_refs=[],
        )
        result = run_guardrails(a)
        assert result.passed


# ===================================================================
# 3. State machine — valid transitions + approval gate
# ===================================================================


class TestStateMachine:
    def test_happy_path_draft_to_reviewed(self) -> None:
        a = _artifact()
        a = transition(a, "reviewed")
        assert a.state == "reviewed"

    def test_happy_path_reviewed_to_approved(self) -> None:
        a = _artifact()
        a = transition(a, "reviewed")
        a = transition(a, "approved")
        assert a.state == "approved"

    def test_happy_path_approved_to_dry_run(self) -> None:
        a = _artifact()
        a = transition(a, "reviewed")
        a = transition(a, "approved")
        a = transition(a, "dry_run")
        assert a.state == "dry_run"

    def test_dry_run_to_sent_requires_approval(self) -> None:
        a = _artifact()
        a = transition(a, "reviewed")
        a = transition(a, "approved")
        a = transition(a, "dry_run")
        try:
            transition(a, "sent")
            assert False, "Should have raised MissingApproval"
        except MissingApproval:
            pass

    def test_dry_run_to_sent_with_approval(self) -> None:
        a = _artifact()
        a = transition(a, "reviewed")
        a = transition(a, "approved")
        a = transition(a, "dry_run")
        a = a.model_copy(update={"approval_signal": "explicit_approval"})
        a = transition(a, "sent")
        assert a.state == "sent"

    def test_cannot_skip_states(self) -> None:
        a = _artifact()
        try:
            transition(a, "approved")
            assert False, "Should have raised InvalidTransition"
        except InvalidTransition:
            pass

    def test_cannot_go_backwards(self) -> None:
        a = _artifact()
        a = transition(a, "reviewed")
        try:
            transition(a, "draft")
            assert False, "Should have raised InvalidTransition"
        except InvalidTransition:
            pass

    def test_terminal_states_have_no_transitions(self) -> None:
        for state in TERMINAL_STATES:
            assert VALID_TRANSITIONS[state] == frozenset()

    def test_reviewed_can_be_blocked(self) -> None:
        a = _artifact()
        a = transition(a, "reviewed")
        a = transition(a, "blocked")
        assert a.state == "blocked"


# ===================================================================
# 4. Dry-run — defaults to dry-run without approval
# ===================================================================


class TestDryRun:
    def test_default_is_dry_run(self) -> None:
        a = _artifact(state="approved")
        updated, result = execute_send(a)
        assert result.dry_run
        assert not result.sent
        assert not result.blocked
        assert updated.state == "dry_run"

    def test_force_approve_sends(self) -> None:
        a = _artifact(state="approved")
        updated, result = execute_send(a, force_approve=True)
        assert result.sent
        assert not result.dry_run
        assert updated.state == "sent"

    def test_guardrail_failure_blocks(self) -> None:
        a = _artifact(
            state="approved",
            brain_packet_id="",
        )
        updated, result = execute_send(a)
        assert result.blocked
        assert not result.sent
        assert updated.state == "blocked"

    def test_unsourced_claim_blocks_send(self) -> None:
        a = _artifact(
            state="approved",
            content="Studies show 90% of businesses fail.",
            evidence_refs=[],
        )
        updated, result = execute_send(a)
        assert result.blocked
        assert not result.sent

    def test_wrong_state_blocks(self) -> None:
        a = _artifact(state="draft")
        updated, result = execute_send(a)
        assert result.blocked


# ===================================================================
# 5. Vellum events — emitted for each state transition
# ===================================================================


class TestVellumEvents:
    def test_draft_event_emitted(self) -> None:
        emitter, store = _emitter()
        a = _artifact()
        result = emit_state_event(emitter, a)
        assert result is True
        events = store.all_events()
        assert len(events) == 1
        assert events[0].event_type == "marketing.draft_created"
        assert events[0].subject_id == a.artifact_id

    def test_all_states_have_events(self) -> None:
        for state in STATE_EVENT_MAP:
            assert state in STATE_EVENT_MAP

    def test_full_lifecycle_events(self) -> None:
        emitter, store = _emitter()
        a = _artifact()
        emit_state_event(emitter, a, previous_state="")

        a = transition(a, "reviewed")
        emit_state_event(emitter, a, previous_state="draft")

        a = transition(a, "approved")
        emit_state_event(emitter, a, previous_state="reviewed")

        a = transition(a, "dry_run")
        emit_state_event(emitter, a, previous_state="approved")

        a = a.model_copy(update={"approval_signal": "explicit_approval"})
        a = transition(a, "sent")
        emit_state_event(emitter, a, previous_state="dry_run")

        events = store.all_events()
        assert len(events) == 5
        types = [e.event_type for e in events]
        assert types == [
            "marketing.draft_created",
            "marketing.reviewed",
            "marketing.approved",
            "marketing.dry_run_executed",
            "marketing.sent",
        ]

    def test_event_carries_brain_packet_id(self) -> None:
        emitter, store = _emitter()
        a = _artifact(brain_packet_id="pkt-ref-456")
        emit_state_event(emitter, a)
        events = store.all_events()
        assert events[0].provenance_refs == ["pkt-ref-456"]

    def test_event_carries_evidence_refs(self) -> None:
        emitter, store = _emitter()
        a = _artifact(evidence_refs=["ev-1", "ev-2"])
        emit_state_event(emitter, a)
        events = store.all_events()
        assert events[0].evidence_refs == ["ev-1", "ev-2"]

    def test_blocked_event(self) -> None:
        emitter, store = _emitter()
        a = _artifact(state="blocked")
        emit_state_event(emitter, a, previous_state="dry_run", detail="guardrail violation")
        events = store.all_events()
        assert events[0].event_type == "marketing.blocked"
        assert events[0].metadata["detail"] == "guardrail violation"

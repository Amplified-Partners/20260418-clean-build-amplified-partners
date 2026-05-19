"""Tests for sidecar — models, lifecycle, cleanup, receipts.

Covers the four required invariants from IMPLEMENTATION_PLAN.md § PR 8:
  1. Sidecar cleanup works on: normal completion, exception path, expired TTL, startup scavenger
  2. No raw SaaS context persists after expiry
  3. Deletion receipts created in Vellum
  4. Sidecar never becomes source of record for customer/contact data

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Allow imports from 02_build/
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sidecar.models import (  # noqa: E402
    DEFAULT_TTL_HOURS,
    TERMINAL_STATES,
    EphemeralSession,
    StablePreference,
)
from sidecar.lifecycle import (  # noqa: E402
    InvalidTransition,
    SessionExpired,
    VALID_TRANSITIONS,
    check_ttl,
    close_session,
    error_session,
    expire_session,
    transition,
    use_session,
)
from sidecar.cleanup import (  # noqa: E402
    cleanup_exception,
    cleanup_expired,
    cleanup_normal,
    startup_scavenger,
)
from sidecar.receipts import (  # noqa: E402
    emit_deletion_receipt,
    emit_session_event,
)
from epistemic_core.vellum_emitter import (  # noqa: E402
    MemoryVellumStore,
    VellumEmitter,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _session(**kw: object) -> EphemeralSession:
    defaults: dict = {
        "owner": "test-agent",
        "purpose": "test session",
    }
    defaults.update(kw)
    return EphemeralSession(**defaults)


def _expired_session(**kw: object) -> EphemeralSession:
    past = datetime.now(timezone.utc) - timedelta(hours=2)
    defaults: dict = {
        "owner": "test-agent",
        "purpose": "expired session",
        "created_at": past,
        "expires_at": past + timedelta(hours=1),
    }
    defaults.update(kw)
    return EphemeralSession(**defaults)


def _active_session(**kw: object) -> EphemeralSession:
    s = _session(**kw)
    return use_session(s, {"key": "value"})


def _emitter() -> tuple[VellumEmitter, MemoryVellumStore]:
    store = MemoryVellumStore()
    emitter = VellumEmitter(store=store)
    return emitter, store


# ===================================================================
# 1. Models
# ===================================================================


class TestModels:
    def test_session_defaults(self) -> None:
        s = _session()
        assert s.state == "open"
        assert s.ttl_hours == DEFAULT_TTL_HOURS
        assert s.expires_at is not None
        assert not s.is_expired
        assert not s.is_terminal

    def test_session_expiry_calculated(self) -> None:
        s = _session(ttl_hours=2)
        assert s.expires_at is not None
        expected = s.created_at + timedelta(hours=2)
        assert abs((s.expires_at - expected).total_seconds()) < 1

    def test_expired_session_detected(self) -> None:
        s = _expired_session()
        assert s.is_expired

    def test_terminal_states(self) -> None:
        assert "closed" in TERMINAL_STATES
        assert "expired" in TERMINAL_STATES
        assert "error" in TERMINAL_STATES
        assert len(TERMINAL_STATES) == 3

    def test_stable_preference_separate(self) -> None:
        p = StablePreference(key="theme", value="dark", owner="user-1")
        assert p.key == "theme"
        assert p.value == "dark"

    def test_context_is_dict(self) -> None:
        s = _session()
        assert s.context == {}
        assert s.saas_refs == []


# ===================================================================
# 2. Lifecycle — state transitions + TTL
# ===================================================================


class TestLifecycle:
    def test_open_to_active(self) -> None:
        s = _session()
        s = transition(s, "active")
        assert s.state == "active"

    def test_active_to_closing(self) -> None:
        s = _active_session()
        s = transition(s, "closing")
        assert s.state == "closing"

    def test_closing_to_closed(self) -> None:
        s = _active_session()
        s = transition(s, "closing")
        s = transition(s, "closed")
        assert s.state == "closed"

    def test_use_session_activates(self) -> None:
        s = _session()
        s = use_session(s, {"task": "lookup"})
        assert s.state == "active"
        assert s.context["task"] == "lookup"

    def test_use_session_adds_context(self) -> None:
        s = _active_session()
        s = use_session(s, {"extra": "data"})
        assert "extra" in s.context

    def test_use_expired_session_raises(self) -> None:
        s = _expired_session()
        try:
            use_session(s, {"key": "val"})
            assert False, "Should have raised SessionExpired"
        except SessionExpired:
            pass

    def test_use_terminal_session_raises(self) -> None:
        s = _session()
        s = close_session(s)
        try:
            use_session(s, {"key": "val"})
            assert False, "Should have raised InvalidTransition"
        except InvalidTransition:
            pass

    def test_close_session(self) -> None:
        s = _active_session()
        s = close_session(s)
        assert s.state == "closed"

    def test_expire_session(self) -> None:
        s = _active_session()
        s = expire_session(s)
        assert s.state == "expired"

    def test_error_session(self) -> None:
        s = _active_session()
        s = error_session(s)
        assert s.state == "error"

    def test_check_ttl_expires(self) -> None:
        s = _expired_session()
        s = check_ttl(s)
        assert s.state == "expired"

    def test_check_ttl_noop_if_valid(self) -> None:
        s = _session()
        s = check_ttl(s)
        assert s.state == "open"

    def test_cannot_transition_from_terminal(self) -> None:
        for state in TERMINAL_STATES:
            assert VALID_TRANSITIONS[state] == frozenset()

    def test_cannot_skip_to_closed(self) -> None:
        s = _session()
        try:
            transition(s, "closed")
            assert False, "Should have raised InvalidTransition"
        except InvalidTransition:
            pass


# ===================================================================
# 3. Cleanup — four paths
# ===================================================================


class TestCleanup:
    def test_normal_completion_wipes_context(self) -> None:
        s = _active_session()
        s = use_session(s, {"secret": "data", "saas_id": "crm-123"})
        s = s.model_copy(update={"saas_refs": ["ref-1"]})
        wiped, result = cleanup_normal(s)
        assert wiped.state == "closed"
        assert wiped.context == {}
        assert wiped.saas_refs == []
        assert wiped.candidate_signals == []
        assert result.context_wiped
        assert result.saas_refs_wiped
        assert result.reason == "normal_completion"

    def test_exception_path_wipes_context(self) -> None:
        s = _active_session()
        s = use_session(s, {"data": "sensitive"})
        wiped, result = cleanup_exception(s)
        assert wiped.state == "error"
        assert wiped.context == {}
        assert result.reason == "exception_path"

    def test_expired_ttl_wipes_context(self) -> None:
        s = _expired_session()
        s = s.model_copy(update={
            "context": {"saas_data": "leaked"},
            "saas_refs": ["crm-ref"],
        })
        wiped, result = cleanup_expired(s)
        assert wiped.is_terminal
        assert wiped.context == {}
        assert wiped.saas_refs == []
        assert result.reason == "expired_ttl"

    def test_startup_scavenger_cleans_all(self) -> None:
        sessions = [
            _active_session(),
            _expired_session(),
            _session(),
            close_session(_active_session()),  # already terminal
        ]
        sessions[0] = use_session(sessions[0], {"data": "stale"})
        cleaned, report = startup_scavenger(sessions)
        assert len(report.cleaned) == 3  # 3 non-terminal cleaned
        assert report.skipped == 1  # 1 already terminal
        for s in cleaned:
            assert s.is_terminal
        # Non-terminal sessions had context wiped
        for r in report.cleaned:
            assert r.context_wiped
            assert r.saas_refs_wiped

    def test_startup_scavenger_empty_list(self) -> None:
        cleaned, report = startup_scavenger([])
        assert len(cleaned) == 0
        assert report.skipped == 0
        assert report.cleaned == []


# ===================================================================
# 4. No SaaS context persists after cleanup
# ===================================================================


class TestNoPersistence:
    def test_no_context_after_normal_close(self) -> None:
        s = _active_session()
        s = use_session(s, {"customer_name": "Bob", "crm_id": "C-001"})
        s = s.model_copy(update={"saas_refs": ["xero-inv-123"]})
        wiped, _ = cleanup_normal(s)
        assert "customer_name" not in wiped.context
        assert "crm_id" not in wiped.context
        assert wiped.saas_refs == []

    def test_no_context_after_expiry(self) -> None:
        s = _expired_session()
        s = s.model_copy(update={
            "context": {"phone": "07700900000"},
            "saas_refs": ["stripe-cus-xyz"],
        })
        wiped, _ = cleanup_expired(s)
        assert wiped.context == {}
        assert wiped.saas_refs == []

    def test_candidate_signals_wiped(self) -> None:
        s = _active_session()
        s = s.model_copy(update={
            "candidate_signals": ["signal-1", "signal-2"],
        })
        wiped, _ = cleanup_normal(s)
        assert wiped.candidate_signals == []


# ===================================================================
# 5. Vellum deletion receipts
# ===================================================================


class TestVellumReceipts:
    def test_deletion_receipt_emitted(self) -> None:
        emitter, store = _emitter()
        s = _active_session()
        wiped, result = cleanup_normal(s)
        emitted = emit_deletion_receipt(emitter, wiped, result)
        assert emitted
        events = store.all_events()
        assert len(events) == 1
        assert events[0].event_type == "sidecar.cleanup.normal_completion"
        assert events[0].subject_id == wiped.session_id
        assert events[0].metadata["context_wiped"] is True

    def test_exception_receipt(self) -> None:
        emitter, store = _emitter()
        s = _active_session()
        wiped, result = cleanup_exception(s)
        emit_deletion_receipt(emitter, wiped, result)
        events = store.all_events()
        assert events[0].event_type == "sidecar.cleanup.exception_path"

    def test_expired_receipt(self) -> None:
        emitter, store = _emitter()
        s = _expired_session()
        wiped, result = cleanup_expired(s)
        emit_deletion_receipt(emitter, wiped, result)
        events = store.all_events()
        assert events[0].event_type == "sidecar.cleanup.expired_ttl"

    def test_scavenger_receipts(self) -> None:
        emitter, store = _emitter()
        sessions = [_active_session(), _expired_session()]
        cleaned, report = startup_scavenger(sessions)
        for s, r in zip(cleaned, report.cleaned):
            emit_deletion_receipt(emitter, s, r)
        events = store.all_events()
        assert len(events) == 2

    def test_session_event_emitted(self) -> None:
        emitter, store = _emitter()
        s = _session()
        emit_session_event(emitter, s, "opened", detail="test")
        events = store.all_events()
        assert len(events) == 1
        assert events[0].event_type == "sidecar.opened"

    def test_receipt_carries_metadata(self) -> None:
        emitter, store = _emitter()
        s = _session(owner="agent-x", purpose="lookup")
        wiped, result = cleanup_normal(s)
        emit_deletion_receipt(emitter, wiped, result)
        events = store.all_events()
        assert events[0].metadata["owner"] == "agent-x"
        assert events[0].metadata["purpose"] == "lookup"


# ===================================================================
# 6. Never source of record
# ===================================================================


class TestNeverSourceOfRecord:
    def test_session_has_no_customer_fields(self) -> None:
        fields = set(EphemeralSession.model_fields.keys())
        forbidden = {"customer_id", "contact_id", "email", "phone", "address"}
        assert fields.isdisjoint(forbidden), (
            f"Session model must not have customer/contact fields. "
            f"Found: {fields & forbidden}"
        )

    def test_preference_has_no_customer_fields(self) -> None:
        fields = set(StablePreference.model_fields.keys())
        forbidden = {"customer_id", "contact_id", "email", "phone", "address"}
        assert fields.isdisjoint(forbidden)

"""Tests for Vellum event model, emitter, buffer, and reconciler — PR 5.

Covers the five required invariants from IMPLEMENTATION_PLAN.md:
  1. Vellum idempotency prevents duplicate receipts
  2. Events carry all required fields
  3. Events are persisted to Vellum permanently
  4. Fallback JSONL buffer replays correctly on reconnect
  5. Reconciler detects pending-too-long events

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from epistemic_core.tiers import EpistemicTier
from epistemic_core.vellum_event import VellumEvent
from epistemic_core.vellum_emitter import (
    JSONLBuffer,
    MemoryVellumStore,
    VellumEmitter,
    reconcile,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _event(**kw: object) -> VellumEvent:
    defaults: dict = {
        "event_type": "test_event",
        "actor": "test_actor",
        "component": "test_component",
    }
    defaults.update(kw)
    return VellumEvent(**defaults)


# ===================================================================
# 1. VellumEvent model
# ===================================================================


class TestVellumEvent:
    def test_required_fields(self) -> None:
        ev = _event(
            subject_id="sub-1",
            new_state="created",
            epistemic_tier=EpistemicTier.STRUCTURED,
            provenance_refs=["ref-1"],
            evidence_refs=["ev-1"],
            correlation_id="corr-1",
            workflow_id="wf-1",
            permission_scope="agent_retrieval",
            expected_next_state="processed",
        )
        assert ev.event_type == "test_event"
        assert ev.actor == "test_actor"
        assert ev.component == "test_component"
        assert ev.subject_id == "sub-1"
        assert ev.previous_state == ""
        assert ev.new_state == "created"
        assert ev.epistemic_tier == EpistemicTier.STRUCTURED
        assert ev.provenance_refs == ["ref-1"]
        assert ev.evidence_refs == ["ev-1"]
        assert ev.correlation_id == "corr-1"
        assert ev.workflow_id == "wf-1"
        assert ev.permission_scope == "agent_retrieval"
        assert ev.expected_next_state == "processed"
        assert ev.idempotency_key  # auto-generated
        assert ev.event_id  # auto-generated
        assert ev.timestamp  # auto-generated

    def test_idempotency_key_auto_generated(self) -> None:
        ev = _event()
        assert len(ev.idempotency_key) == 16

    def test_same_inputs_same_timestamp_same_key(self) -> None:
        ts = datetime(2026, 5, 19, tzinfo=timezone.utc)
        ev1 = _event(timestamp=ts, subject_id="s1", new_state="done")
        ev2 = _event(timestamp=ts, subject_id="s1", new_state="done")
        assert ev1.idempotency_key == ev2.idempotency_key

    def test_different_inputs_different_key(self) -> None:
        ts = datetime(2026, 5, 19, tzinfo=timezone.utc)
        ev1 = _event(timestamp=ts, subject_id="s1", new_state="done")
        ev2 = _event(timestamp=ts, subject_id="s2", new_state="done")
        assert ev1.idempotency_key != ev2.idempotency_key

    def test_explicit_idempotency_key_preserved(self) -> None:
        ev = _event(idempotency_key="my-custom-key")
        assert ev.idempotency_key == "my-custom-key"

    def test_to_jsonl_dict(self) -> None:
        ev = _event(subject_id="sub-1")
        d = ev.to_jsonl_dict()
        assert d["event_type"] == "test_event"
        assert d["subject_id"] == "sub-1"
        assert isinstance(d["timestamp"], str)

    def test_default_tier_is_intuited(self) -> None:
        ev = _event()
        assert ev.epistemic_tier == EpistemicTier.INTUITED

    def test_metadata_freeform(self) -> None:
        ev = _event(metadata={"key": "value", "count": 42})
        assert ev.metadata["key"] == "value"
        assert ev.metadata["count"] == 42


# ===================================================================
# 2. MemoryVellumStore
# ===================================================================


class TestMemoryStore:
    def test_write_and_read(self) -> None:
        store = MemoryVellumStore()
        ev = _event()
        store.write_event(ev)
        assert store.has_event(ev.idempotency_key)
        assert len(store.all_events()) == 1

    def test_has_event_false_for_unknown(self) -> None:
        store = MemoryVellumStore()
        assert not store.has_event("nonexistent")

    def test_clear(self) -> None:
        store = MemoryVellumStore()
        store.write_event(_event())
        store.clear()
        assert len(store.all_events()) == 0


# ===================================================================
# 3. VellumEmitter — idempotency and persistence
# ===================================================================


class TestEmitter:
    def test_emit_persists_event(self) -> None:
        store = MemoryVellumStore()
        emitter = VellumEmitter(store=store)
        ev = _event()
        result = emitter.emit(ev)
        assert result is True
        assert len(store.all_events()) == 1

    def test_duplicate_is_noop(self) -> None:
        store = MemoryVellumStore()
        emitter = VellumEmitter(store=store)
        ev = _event()
        emitter.emit(ev)
        result = emitter.emit(ev)
        assert result is False
        assert len(store.all_events()) == 1

    def test_subscriber_called(self) -> None:
        store = MemoryVellumStore()
        emitter = VellumEmitter(store=store)
        received: list[VellumEvent] = []
        emitter.subscribe(lambda e: received.append(e))
        emitter.emit(_event())
        assert len(received) == 1

    def test_subscriber_not_called_on_duplicate(self) -> None:
        store = MemoryVellumStore()
        emitter = VellumEmitter(store=store)
        received: list[VellumEvent] = []
        emitter.subscribe(lambda e: received.append(e))
        ev = _event()
        emitter.emit(ev)
        emitter.emit(ev)
        assert len(received) == 1

    def test_multiple_different_events(self) -> None:
        store = MemoryVellumStore()
        emitter = VellumEmitter(store=store)
        for i in range(5):
            emitter.emit(_event(subject_id=f"sub-{i}"))
        assert len(store.all_events()) == 5


# ===================================================================
# 4. JSONL buffer — fallback and replay
# ===================================================================


class TestJSONLBuffer:
    def test_append_and_drain(self, tmp_path: Path) -> None:
        buf = JSONLBuffer(tmp_path / "buffer.jsonl")
        ev1 = _event(subject_id="s1")
        ev2 = _event(subject_id="s2")
        buf.append(ev1)
        buf.append(ev2)
        assert buf.pending_count == 2
        drained = buf.drain()
        assert len(drained) == 2
        assert drained[0].subject_id == "s1"
        assert drained[1].subject_id == "s2"

    def test_drain_clears_file(self, tmp_path: Path) -> None:
        buf = JSONLBuffer(tmp_path / "buffer.jsonl")
        buf.append(_event())
        buf.drain()
        assert buf.pending_count == 0

    def test_drain_empty_buffer(self, tmp_path: Path) -> None:
        buf = JSONLBuffer(tmp_path / "buffer.jsonl")
        assert buf.drain() == []

    def test_emitter_buffers_on_store_failure(self, tmp_path: Path) -> None:
        class FailingStore:
            def write_event(self, event: VellumEvent) -> None:
                raise ConnectionError("store down")
            def has_event(self, key: str) -> bool:
                return False
            def all_events(self) -> list[VellumEvent]:
                return []

        buf_path = tmp_path / "fallback.jsonl"
        emitter = VellumEmitter(store=FailingStore(), buffer_path=buf_path)  # type: ignore[arg-type]
        ev = _event()
        result = emitter.emit(ev)
        assert result is True
        buf = JSONLBuffer(buf_path)
        assert buf.pending_count == 1

    def test_replay_buffer_to_store(self, tmp_path: Path) -> None:
        buf_path = tmp_path / "replay.jsonl"
        buf = JSONLBuffer(buf_path)
        ev1 = _event(subject_id="r1")
        ev2 = _event(subject_id="r2")
        buf.append(ev1)
        buf.append(ev2)

        store = MemoryVellumStore()
        emitter = VellumEmitter(store=store, buffer_path=buf_path)
        replayed = emitter.replay_buffer()
        assert replayed == 2
        assert len(store.all_events()) == 2

    def test_replay_skips_duplicates(self, tmp_path: Path) -> None:
        buf_path = tmp_path / "dedup.jsonl"
        store = MemoryVellumStore()
        ev = _event(subject_id="dup")
        store.write_event(ev)

        buf = JSONLBuffer(buf_path)
        buf.append(ev)

        emitter = VellumEmitter(store=store, buffer_path=buf_path)
        replayed = emitter.replay_buffer()
        assert replayed == 0
        assert len(store.all_events()) == 1


# ===================================================================
# 5. Reconciler — pending-too-long and missing witness
# ===================================================================


class TestReconciler:
    def test_clean_result(self) -> None:
        store = MemoryVellumStore()
        store.write_event(_event(subject_id="s1", new_state="done"))
        result = reconcile(store)
        assert result.clean

    def test_pending_too_long_flagged(self) -> None:
        store = MemoryVellumStore()
        old_time = datetime.now(timezone.utc) - timedelta(hours=2)
        store.write_event(_event(
            subject_id="s1",
            new_state="started",
            expected_next_state="completed",
            timestamp=old_time,
        ))
        result = reconcile(store, max_pending_age=timedelta(hours=1))
        assert not result.clean
        assert len(result.pending_too_long) == 1
        assert result.pending_too_long[0].subject_id == "s1"

    def test_pending_resolved_not_flagged(self) -> None:
        store = MemoryVellumStore()
        old_time = datetime.now(timezone.utc) - timedelta(hours=2)
        store.write_event(_event(
            subject_id="s1",
            new_state="started",
            expected_next_state="completed",
            timestamp=old_time,
        ))
        store.write_event(_event(
            subject_id="s1",
            new_state="completed",
        ))
        result = reconcile(store, max_pending_age=timedelta(hours=1))
        assert result.clean

    def test_missing_witness_flagged(self) -> None:
        store = MemoryVellumStore()
        store.write_event(_event(subject_id="s1"))
        result = reconcile(
            store,
            expected_subjects=["s1", "s2", "s3"],
        )
        assert not result.clean
        assert set(result.missing_witness) == {"s2", "s3"}

    def test_no_expected_subjects_no_missing(self) -> None:
        store = MemoryVellumStore()
        result = reconcile(store)
        assert result.clean

    def test_custom_now(self) -> None:
        store = MemoryVellumStore()
        event_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
        store.write_event(_event(
            subject_id="s1",
            new_state="started",
            expected_next_state="done",
            timestamp=event_time,
        ))
        check_time = datetime(2026, 1, 1, 0, 30, tzinfo=timezone.utc)
        result = reconcile(
            store,
            max_pending_age=timedelta(hours=1),
            now=check_time,
        )
        assert result.clean

        check_time_later = datetime(2026, 1, 1, 2, 0, tzinfo=timezone.utc)
        result = reconcile(
            store,
            max_pending_age=timedelta(hours=1),
            now=check_time_later,
        )
        assert not result.clean

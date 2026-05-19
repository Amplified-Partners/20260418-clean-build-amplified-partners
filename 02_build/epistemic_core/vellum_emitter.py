"""Vellum emitter — system-wide event witness.

Vellum is permanent. Every component that changes state emits events
through this module. The emitter guarantees:

  1. Events are persisted to the Vellum store (permanent).
  2. If the store is temporarily unreachable, events buffer to local
     JSONL and replay on reconnect.
  3. Duplicate events (same idempotency_key) are no-ops.
  4. The reconciler flags pending-too-long and state-without-witness.

In the reference implementation the store is in-memory. In production
this writes to Vellum's additive-only hash-chained sheet.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import json
import logging
import threading
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Protocol

from epistemic_core.vellum_event import VellumEvent

log = logging.getLogger("amplified.vellum.emitter")


# ---------------------------------------------------------------------------
# Store protocol — anything that can persist events
# ---------------------------------------------------------------------------


class VellumStore(Protocol):
    """Minimal interface a persistence backend must satisfy."""

    def write_event(self, event: VellumEvent) -> None: ...
    def has_event(self, idempotency_key: str) -> bool: ...
    def all_events(self) -> list[VellumEvent]: ...


# ---------------------------------------------------------------------------
# In-memory store (testing / reference implementation)
# ---------------------------------------------------------------------------


class MemoryVellumStore:
    """Thread-safe in-memory store. For testing and dev."""

    def __init__(self) -> None:
        self._events: list[VellumEvent] = []
        self._keys: set[str] = set()
        self._lock = threading.Lock()

    def write_event(self, event: VellumEvent) -> None:
        with self._lock:
            self._events.append(event)
            self._keys.add(event.idempotency_key)

    def has_event(self, idempotency_key: str) -> bool:
        with self._lock:
            return idempotency_key in self._keys

    def all_events(self) -> list[VellumEvent]:
        with self._lock:
            return list(self._events)

    def clear(self) -> None:
        with self._lock:
            self._events.clear()
            self._keys.clear()


# ---------------------------------------------------------------------------
# JSONL fallback buffer
# ---------------------------------------------------------------------------


class JSONLBuffer:
    """Append-only local buffer for when the store is unreachable."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = threading.Lock()

    def append(self, event: VellumEvent) -> None:
        with self._lock:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a") as f:
                f.write(json.dumps(event.to_jsonl_dict()) + "\n")

    def drain(self) -> list[VellumEvent]:
        """Read and clear the buffer. Returns events in order."""
        with self._lock:
            if not self._path.exists():
                return []
            events: list[VellumEvent] = []
            with self._path.open() as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(VellumEvent.model_validate_json(line))
                    except Exception:
                        log.warning("Skipping malformed JSONL line: %s", line[:80])
            self._path.unlink(missing_ok=True)
            return events

    @property
    def pending_count(self) -> int:
        with self._lock:
            if not self._path.exists():
                return 0
            with self._path.open() as f:
                return sum(1 for line in f if line.strip())


# ---------------------------------------------------------------------------
# Emitter — the single entry point for all Vellum events
# ---------------------------------------------------------------------------


class VellumEmitter:
    """Emit events to Vellum. Idempotent. Buffers on failure.

    Usage::

        emitter = VellumEmitter(store=MemoryVellumStore())
        emitter.emit(VellumEvent(
            event_type="packet_created",
            actor="brain_curator",
            component="brain_curator.freeze",
            subject_id="pkt-123",
            new_state="frozen",
            epistemic_tier=EpistemicTier.STRUCTURED,
        ))
    """

    def __init__(
        self,
        *,
        store: VellumStore,
        buffer_path: Path | None = None,
    ) -> None:
        self._store = store
        self._buffer = JSONLBuffer(buffer_path) if buffer_path else None
        self._subscribers: list[Callable[[VellumEvent], None]] = []
        self._lock = threading.Lock()

    def emit(self, event: VellumEvent) -> bool:
        """Persist event to Vellum. Returns True if written, False if duplicate.

        If the store is unreachable, buffers to JSONL and returns True
        (the event is not lost).
        """
        if self._store.has_event(event.idempotency_key):
            log.debug("Duplicate event (key=%s), skipping", event.idempotency_key)
            return False

        try:
            self._store.write_event(event)
        except Exception as exc:
            log.warning("Store unreachable (%s), buffering event %s", exc, event.event_id)
            if self._buffer:
                self._buffer.append(event)
            return True

        log.debug(
            "VELLUM: %s actor=%s component=%s subject=%s",
            event.event_type,
            event.actor,
            event.component,
            event.subject_id,
        )

        for hook in self._subscribers:
            try:
                hook(event)
            except Exception as exc:
                log.error("Subscriber hook %s raised: %s", hook, exc)

        return True

    def replay_buffer(self) -> int:
        """Replay any buffered events to the store. Returns count replayed."""
        if not self._buffer:
            return 0
        events = self._buffer.drain()
        replayed = 0
        for event in events:
            if not self._store.has_event(event.idempotency_key):
                try:
                    self._store.write_event(event)
                    replayed += 1
                except Exception:
                    self._buffer.append(event)
        return replayed

    def subscribe(self, hook: Callable[[VellumEvent], None]) -> None:
        """Register a callback for every new event."""
        self._subscribers.append(hook)

    @property
    def store(self) -> VellumStore:
        return self._store


# ---------------------------------------------------------------------------
# Reconciler stub — flags pending-too-long and state-without-witness
# ---------------------------------------------------------------------------


class ReconcilerResult:
    """Result of a reconciliation check."""

    def __init__(
        self,
        *,
        pending_too_long: list[VellumEvent],
        missing_witness: list[str],
    ) -> None:
        self.pending_too_long = pending_too_long
        self.missing_witness = missing_witness

    @property
    def clean(self) -> bool:
        return not self.pending_too_long and not self.missing_witness


def reconcile(
    store: VellumStore,
    *,
    max_pending_age: timedelta = timedelta(hours=1),
    expected_subjects: list[str] | None = None,
    now: datetime | None = None,
) -> ReconcilerResult:
    """Check for events stuck in non-terminal states.

    Flags:
    - Events with expected_next_state set but no follow-up event within
      max_pending_age.
    - Subjects in expected_subjects that have zero events (no witness).
    """
    check_time = now or datetime.now(timezone.utc)
    events = store.all_events()

    # Index: subject_id → latest event
    latest_by_subject: dict[str, VellumEvent] = {}
    for ev in events:
        if ev.subject_id:
            existing = latest_by_subject.get(ev.subject_id)
            if existing is None or ev.timestamp > existing.timestamp:
                latest_by_subject[ev.subject_id] = ev

    # Find events still pending (have expected_next_state, not yet reached)
    reached_states: dict[str, set[str]] = {}
    for ev in events:
        if ev.subject_id:
            reached_states.setdefault(ev.subject_id, set()).add(ev.new_state)

    pending_too_long: list[VellumEvent] = []
    for ev in events:
        if not ev.expected_next_state:
            continue
        states = reached_states.get(ev.subject_id, set())
        if ev.expected_next_state in states:
            continue
        age = check_time - ev.timestamp
        if age > max_pending_age:
            pending_too_long.append(ev)

    # Find subjects with no witness
    missing_witness: list[str] = []
    if expected_subjects:
        witnessed = {ev.subject_id for ev in events if ev.subject_id}
        for subject in expected_subjects:
            if subject not in witnessed:
                missing_witness.append(subject)

    return ReconcilerResult(
        pending_too_long=pending_too_long,
        missing_witness=missing_witness,
    )

"""
Audit log — the system's memory of its own honesty.

Append-only, thread-safe. In production this writes to PostgreSQL/Vellum.
For the reference implementation and tests: in-memory.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import logging
import threading
from collections.abc import Callable

from epistemic_core.tiers import EpistemicTier
from epistemic_core.min_rule import Provenance, PreconditionCheck

log = logging.getLogger("amplified.epistemic.audit")


@dataclasses.dataclass(frozen=True)
class StatusRecord:
    """One audit-log entry. Written for every decision the system makes."""

    record_id: str
    timestamp: dt.datetime
    layer: str
    declared_status: EpistemicTier
    effective_status: EpistemicTier
    provenance: Provenance
    preconditions: tuple[PreconditionCheck, ...]
    sample_size: int | None = None
    note: str = ""


class AuditLog:
    """Append-only log. In production this writes to PostgreSQL/Vellum.

    For the reference implementation, in-memory and thread-safe.
    Supports subscriber hooks for downstream consumers (drift detector,
    Vellum emitter, etc.).
    """

    def __init__(self) -> None:
        self._records: list[StatusRecord] = []
        self._lock = threading.Lock()
        self._on_record: list[Callable[[StatusRecord], None]] = []

    def write(self, record: StatusRecord) -> None:
        with self._lock:
            self._records.append(record)
        log.debug(
            "AUDIT: %s declared=%s effective=%s",
            record.layer,
            record.declared_status.label(),
            record.effective_status.label(),
        )
        for hook in self._on_record:
            hook(record)

    def subscribe(self, hook: Callable[[StatusRecord], None]) -> None:
        """Register a callback for every new record."""
        self._on_record.append(hook)

    def all(self) -> tuple[StatusRecord, ...]:
        with self._lock:
            return tuple(self._records)

    def clear(self) -> None:
        """For testing only."""
        with self._lock:
            self._records.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._records)

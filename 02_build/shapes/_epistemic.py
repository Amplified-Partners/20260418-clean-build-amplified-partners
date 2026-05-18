"""
Epistemic bridge for the Huf Haus shape system.

Connects the shapes system to the Layer 0 epistemic invariant
(02_build/routing/epistemic_status.py) without tight coupling.

This module is intentionally small. It provides:
1. StatusedOutput — a shape's output wrapped with epistemic metadata
2. ShapeAuditRecord — one audit entry per boundary crossing
3. ShapeAuditLog — append-only, thread-safe, inspectable in tests
4. EpistemicTier — re-export of the four tiers for shapes to use
5. Helper functions for the min-rule and demotion

Authored by Devon-b5dc | 2026-05-17 | session devin-b5dc68e1aefa4982b9c083714ac968c6
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import enum
import logging
import threading
import uuid
from typing import Any, Sequence

log = logging.getLogger("amplified.shapes.epistemic")


# ---------------------------------------------------------------------------
# 1. The four tiers (self-contained to avoid circular import with routing)
# ---------------------------------------------------------------------------


class EpistemicTier(enum.IntEnum):
    """Four tiers of honest knowledge claim. Order matters: min() works."""

    INTUITED = 1
    STRUCTURED = 2
    MEASURED = 3
    PROVEN = 4

    def label(self) -> str:
        return {1: "intuited", 2: "structured", 3: "measured", 4: "proven"}[self]

    @classmethod
    def from_string(cls, s: str) -> EpistemicTier:
        mapping = {
            "intuited": cls.INTUITED,
            "structured": cls.STRUCTURED,
            "measured": cls.MEASURED,
            "proven": cls.PROVEN,
        }
        return mapping[s.lower()]


def _demote(tier: EpistemicTier) -> EpistemicTier:
    """One-tier demotion. PROVEN→MEASURED→STRUCTURED→INTUITED."""
    return EpistemicTier(max(EpistemicTier.INTUITED.value, tier.value - 1))


# ---------------------------------------------------------------------------
# 2. Precondition check (local definition, same semantics as reference)
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class PreconditionCheck:
    """A precondition with its verification state."""

    name: str
    holds: bool
    verified_at: dt.datetime = dataclasses.field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)
    )
    evidence: str = ""


# ---------------------------------------------------------------------------
# 3. StatusedOutput — a shape's output with epistemic provenance
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ShapeProvenance:
    """How was this output produced?"""

    shape_name: str
    method: str
    input_ids: tuple[str, ...] = ()


@dataclasses.dataclass(frozen=True)
class StatusedOutput:
    """A value that knows what it is.

    Wraps any shape output with epistemic metadata. Bare values at
    protected boundaries are the laundering trap — this type prevents that.
    """

    value: Any
    status: EpistemicTier
    provenance: ShapeProvenance
    preconditions: tuple[PreconditionCheck, ...] = ()
    valid_until: dt.datetime | None = None
    output_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))

    def is_stale(self, now: dt.datetime | None = None) -> bool:
        if self.valid_until is None:
            return False
        return (now or dt.datetime.now(dt.timezone.utc)) > self.valid_until

    def effective_status(
        self, input_statuses: Sequence[EpistemicTier] = ()
    ) -> EpistemicTier:
        """The min-rule. Cannot be overridden."""
        own_claim = self.status
        input_floor = min(input_statuses, default=EpistemicTier.PROVEN)
        precondition_floor = (
            own_claim
            if all(p.holds for p in self.preconditions)
            else _demote(own_claim)
        )
        staleness_floor = _demote(own_claim) if self.is_stale() else own_claim
        return min(own_claim, input_floor, precondition_floor, staleness_floor)


# ---------------------------------------------------------------------------
# 4. ShapeAuditRecord and ShapeAuditLog
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ShapeAuditRecord:
    """One audit entry per epistemic boundary crossing."""

    record_id: str
    timestamp: dt.datetime
    shape_name: str
    method: str
    declared_status: EpistemicTier
    effective_status: EpistemicTier
    input_statuses: tuple[EpistemicTier, ...]
    preconditions: tuple[PreconditionCheck, ...]
    reason: str = ""


class ShapeAuditLog:
    """Append-only, thread-safe audit log for epistemic boundary crossings.

    In production this sinks to Vellum/PostgreSQL. For testing: in-memory.
    """

    def __init__(self) -> None:
        self._records: list[ShapeAuditRecord] = []
        self._lock = threading.Lock()

    def write(self, record: ShapeAuditRecord) -> None:
        with self._lock:
            self._records.append(record)
        log.debug(
            "EPISTEMIC AUDIT: %s.%s declared=%s effective=%s",
            record.shape_name,
            record.method,
            record.declared_status.label(),
            record.effective_status.label(),
        )

    def all(self) -> tuple[ShapeAuditRecord, ...]:
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


# Module-level singleton
SHAPE_AUDIT_LOG = ShapeAuditLog()

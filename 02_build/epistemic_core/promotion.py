"""
Promotion gates — the only legal way to move status up.

One step at a time. Tier skipping is forbidden (P0).
Each promotion creates an immutable PromotionRecord.

Sample size floor for MEASURED = 30 (Brain Architecture v8, confirmed by Ewan).

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import uuid
from collections.abc import Sequence

from epistemic_core.tiers import EpistemicTier
from epistemic_core.min_rule import StatusedValue, PreconditionCheck
from epistemic_core.p0_policy import P0Incident


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MEASURED_SAMPLE_SIZE_FLOOR = 30  # Brain Architecture v8, confirmed by Ewan


# ---------------------------------------------------------------------------
# PromotionRecord — immutable evidence that a promotion happened
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class PromotionRecord:
    """An immutable record that a value was promoted up one tier."""

    promotion_id: str
    from_status: EpistemicTier
    to_status: EpistemicTier
    method: str
    artefacts: tuple[str, ...]
    timestamp: dt.datetime
    approver: str


# ---------------------------------------------------------------------------
# Persistence adapter interface
# ---------------------------------------------------------------------------


class PromotionStore:
    """Interface for persisting promotion records.

    Default implementation: in-memory list. Production: PostgreSQL/Vellum.
    Subclass and override save() for production use.
    """

    def __init__(self) -> None:
        self._records: list[PromotionRecord] = []

    def save(self, record: PromotionRecord) -> None:
        self._records.append(record)

    def all(self) -> tuple[PromotionRecord, ...]:
        return tuple(self._records)

    @property
    def size(self) -> int:
        return len(self._records)


# Module-level default store
_PROMOTION_STORE = PromotionStore()


def get_promotion_store() -> PromotionStore:
    return _PROMOTION_STORE


def set_promotion_store(store: PromotionStore) -> None:
    global _PROMOTION_STORE
    _PROMOTION_STORE = store


# ---------------------------------------------------------------------------
# Promotion gates — one step at a time
# ---------------------------------------------------------------------------


def promote_to_structured(
    value: StatusedValue,
    *,
    rubric_path: str,
    approver: str,
    store: PromotionStore | None = None,
) -> StatusedValue:
    """1 -> 2: rubric codification.

    The intuited value is now expressed as a deterministic rule with explicit
    inputs, outputs, and weights. The weights are still arbitrary.
    """
    if value.status != EpistemicTier.INTUITED:
        raise P0Incident(
            f"promote_to_structured: input is {value.status.label()}, expected intuited. "
            "Skipping tiers is forbidden."
        )

    record = PromotionRecord(
        promotion_id=str(uuid.uuid4()),
        from_status=EpistemicTier.INTUITED,
        to_status=EpistemicTier.STRUCTURED,
        method="rubric_codification",
        artefacts=(rubric_path,),
        timestamp=dt.datetime.now(dt.timezone.utc),
        approver=approver,
    )
    (store or _PROMOTION_STORE).save(record)

    return dataclasses.replace(
        value,
        status=EpistemicTier.STRUCTURED,
        provenance=dataclasses.replace(
            value.provenance, promotion_record_id=record.promotion_id
        ),
    )


def promote_to_measured(
    value: StatusedValue,
    *,
    sample_size: int,
    confidence_interval: tuple[float, float],
    held_out_validation: float,
    drift_monitor_id: str,
    approver: str,
    store: PromotionStore | None = None,
) -> StatusedValue:
    """2 -> 3: empirical calibration.

    The structured rule's parameters are fitted from data with declared CI,
    sample size, held-out validation, and an active drift monitor.
    """
    if value.status != EpistemicTier.STRUCTURED:
        raise P0Incident(
            f"promote_to_measured: input is {value.status.label()}, expected structured."
        )
    if sample_size < MEASURED_SAMPLE_SIZE_FLOOR:
        raise P0Incident(
            f"promote_to_measured: sample_size={sample_size} < {MEASURED_SAMPLE_SIZE_FLOOR}. "
            "MEASURED requires meaningful sample size."
        )

    record = PromotionRecord(
        promotion_id=str(uuid.uuid4()),
        from_status=EpistemicTier.STRUCTURED,
        to_status=EpistemicTier.MEASURED,
        method="empirical_calibration",
        artefacts=(
            f"sample_size={sample_size}",
            f"ci={confidence_interval}",
            f"held_out={held_out_validation}",
            f"drift_monitor={drift_monitor_id}",
        ),
        timestamp=dt.datetime.now(dt.timezone.utc),
        approver=approver,
    )
    (store or _PROMOTION_STORE).save(record)

    return dataclasses.replace(
        value,
        status=EpistemicTier.MEASURED,
        sample_size=sample_size,
        provenance=dataclasses.replace(
            value.provenance, promotion_record_id=record.promotion_id
        ),
    )


def promote_to_proven(
    value: StatusedValue,
    *,
    theorem: str,
    preconditions: Sequence[PreconditionCheck],
    approver: str,
    store: PromotionStore | None = None,
) -> StatusedValue:
    """3 -> 4: formal proof.

    The measured relationship is shown to follow from a closed-form theorem
    whose preconditions are independently verified.
    """
    if value.status != EpistemicTier.MEASURED:
        raise P0Incident(
            f"promote_to_proven: input is {value.status.label()}, expected measured."
        )
    failing = [p for p in preconditions if not p.holds]
    if failing:
        raise P0Incident(
            f"promote_to_proven: {len(failing)} precondition(s) failing: "
            f"{[p.name for p in failing]}. PROVEN requires verified preconditions."
        )

    record = PromotionRecord(
        promotion_id=str(uuid.uuid4()),
        from_status=EpistemicTier.MEASURED,
        to_status=EpistemicTier.PROVEN,
        method="formal_proof",
        artefacts=(theorem,) + tuple(p.name for p in preconditions),
        timestamp=dt.datetime.now(dt.timezone.utc),
        approver=approver,
    )
    (store or _PROMOTION_STORE).save(record)

    return dataclasses.replace(
        value,
        status=EpistemicTier.PROVEN,
        preconditions=tuple(preconditions),
        provenance=dataclasses.replace(
            value.provenance, promotion_record_id=record.promotion_id
        ),
    )

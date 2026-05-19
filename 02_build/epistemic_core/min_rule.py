"""
The min-rule — effective_tier = min(own_claim, all_input_tiers,
precondition_tiers, staleness_tier).

This is the meet operation of a bounded semilattice on the four tiers.
It is associative, commutative, idempotent, and can never promote.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import uuid
from collections.abc import Sequence
from typing import Any

from epistemic_core.tiers import EpistemicTier


# ---------------------------------------------------------------------------
# Provenance — how was this value produced?
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class Provenance:
    """How was this value produced?"""

    layer: str                              # which layer of the stack
    method: str                             # name of the procedure
    inputs: tuple[str, ...] = ()            # ids of input StatusedValues
    promotion_record_id: str | None = None  # id of the promotion gate, if any


# ---------------------------------------------------------------------------
# PreconditionCheck — a precondition with its verification state
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
# StatusedValue — every value in the system carries its tier
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class StatusedValue:
    """A value that knows what it is.

    All values flowing between layers MUST be StatusedValues. A bare float
    or string crossing a layer boundary is a P0 incident.

    Carries a `valid_until` timestamp. A value consumed after its expiry
    auto-demotes by one tier. This is the temporal-staleness fix.
    """

    value: Any
    status: EpistemicTier
    provenance: Provenance
    preconditions: tuple[PreconditionCheck, ...] = ()
    sample_size: int | None = None
    valid_until: dt.datetime | None = None
    lens: str | None = None
    value_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))

    def is_stale(self, now: dt.datetime | None = None) -> bool:
        if self.valid_until is None:
            return False
        return (now or dt.datetime.now(dt.timezone.utc)) > self.valid_until

    def effective_status(
        self, input_statuses: Sequence[EpistemicTier] = ()
    ) -> EpistemicTier:
        """The min-rule. Cannot be overridden."""
        return effective_status(
            own_claim=self.status,
            input_statuses=input_statuses,
            preconditions=self.preconditions,
            is_stale=self.is_stale(),
        )


# ---------------------------------------------------------------------------
# Standalone functions
# ---------------------------------------------------------------------------


def demote(tier: EpistemicTier) -> EpistemicTier:
    """One-tier demotion. PROVEN -> MEASURED -> STRUCTURED -> INTUITED.

    INTUITED is the floor — cannot demote further.
    """
    return EpistemicTier(max(EpistemicTier.INTUITED.value, tier.value - 1))


def effective_status(
    own_claim: EpistemicTier,
    input_statuses: Sequence[EpistemicTier] = (),
    preconditions: Sequence[PreconditionCheck] = (),
    is_stale: bool = False,
) -> EpistemicTier:
    """Compute effective tier via min-rule.

    effective_tier = min(own_claim, all_input_tiers,
                         precondition_tier, staleness_tier)

    This operation forms a meet-semilattice: associative, commutative,
    idempotent. It can NEVER promote — only demote or hold.
    """
    input_floor = min(input_statuses, default=EpistemicTier.PROVEN)
    precondition_floor = (
        own_claim
        if all(p.holds for p in preconditions)
        else demote(own_claim)
    )
    staleness_floor = demote(own_claim) if is_stale else own_claim
    return min(own_claim, input_floor, precondition_floor, staleness_floor)


def tier_min(a: EpistemicTier, b: EpistemicTier) -> EpistemicTier:
    """Return the lower of two tiers. The meet operation."""
    return min(a, b)


def tier_min_many(tiers: Sequence[EpistemicTier]) -> EpistemicTier:
    """Return the minimum tier from a sequence."""
    if not tiers:
        return EpistemicTier.PROVEN
    return min(tiers)


# String-based backward compat for brain_curator
def tier_min_str(a: str, b: str) -> str:
    """Return the lower of two tier strings (brain_curator compat)."""
    from epistemic_core.tiers import TIER_RANK
    return a if TIER_RANK.get(a, 1) <= TIER_RANK.get(b, 1) else b


def tier_min_many_str(tiers: list[str]) -> str:
    """Return the minimum tier string from a list (brain_curator compat)."""
    if not tiers:
        return "PROVEN"
    result = tiers[0]
    for t in tiers[1:]:
        result = tier_min_str(result, t)
    return result

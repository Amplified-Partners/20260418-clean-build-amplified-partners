"""
Epistemic Status Invariant — routing engine facade.

Layer 0 law for the Amplified substrate routing engine.

Canonical definitions now live in epistemic_core/. This module
re-exports them for backward compatibility and adds routing-specific
types: Layer (the base class for routing stack components) and
FederationUpdate/aggregate_federation_updates.

Authored by Devon-32cc | 2026-05-10 | session devin-32cc0fc89ad04baba570382e2c3eb2f4
Refactored by Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
  — canonical types moved to epistemic_core (consolidation PR 1)
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import logging
from collections.abc import Callable, Sequence
from typing import Any

# ---------------------------------------------------------------------------
# Re-exports from epistemic_core (single source of truth)
# ---------------------------------------------------------------------------

from epistemic_core.tiers import EpistemicTier

# Backward compat: this module historically exported EpistemicStatus
EpistemicStatus = EpistemicTier

from epistemic_core.min_rule import (  # noqa: E402
    Provenance,
    PreconditionCheck,
    StatusedValue,
    demote as _demote,
    effective_status,  # noqa: F401 — re-export
)
from epistemic_core.p0_policy import P0Incident, P0Policy  # noqa: E402, F401
from epistemic_core.audit import AuditLog, StatusRecord  # noqa: E402
from epistemic_core.drift import DriftDetector, DriftSignal  # noqa: E402, F401
from epistemic_core.promotion import (  # noqa: E402
    PromotionRecord,  # noqa: F401 — re-export
    promote_to_structured,  # noqa: F401 — re-export
    promote_to_measured,  # noqa: F401 — re-export
    promote_to_proven,  # noqa: F401 — re-export
)

log = logging.getLogger("amplified.epistemic")

# Module-level audit log singleton for the routing engine
AUDIT_LOG = AuditLog()


# ---------------------------------------------------------------------------
# 6. The Layer base class — every component declares its status
# ---------------------------------------------------------------------------


class Layer:
    """Base class for any component in the substrate routing stack.

    Subclasses MUST implement the four operations. The base class enforces
    the invariant on every call.
    """

    name: str = "unnamed"
    declared_max_status: EpistemicTier = EpistemicTier.INTUITED

    def declare_status(self) -> EpistemicTier:
        """The status this layer claims to produce, before applying min-rule."""
        raise NotImplementedError

    def declare_provenance(self, inputs: Sequence[StatusedValue]) -> Provenance:
        """Where did this layer's output come from?"""
        raise NotImplementedError

    def verify_preconditions(self) -> tuple[PreconditionCheck, ...]:
        """Check all preconditions for this layer's claimed status. Always fresh."""
        raise NotImplementedError

    def compute(self, inputs: Sequence[StatusedValue]) -> Any:
        """The actual work. Subclass implements."""
        raise NotImplementedError

    # ---- enforced wrapper. Subclasses do not override this. ----

    requires_lens: bool = False  # set True for layers that consume lens-dependent params

    def __call__(self, *inputs: StatusedValue) -> StatusedValue:
        # 1. Enforce that all inputs are StatusedValues.
        for i, inp in enumerate(inputs):
            if not isinstance(inp, StatusedValue):
                raise P0Incident(
                    f"{self.name}: input {i} is a bare value (type={type(inp).__name__}). "
                    "All inter-layer values must be StatusedValues. This is the laundering trap."
                )

        # 1b. Lens requirement: layers that consume lens-dependent parameters must
        #     receive inputs whose lens is declared.
        if self.requires_lens:
            missing = [i for i, inp in enumerate(inputs) if inp.lens is None]
            if missing:
                raise P0Incident(
                    f"{self.name}: requires_lens=True but inputs {missing} have lens=None. "
                    "Federated GLM consumers must declare their lens to avoid "
                    "the identifiability confounding documented in Section 11."
                )

        # 2. Run the computation.
        raw_value = self.compute(inputs)

        # 3. Verify preconditions FRESH. We never trust cached precondition state.
        preconditions = self.verify_preconditions()

        # 4. Apply the min-rule.
        own_claim = self.declare_status()
        if own_claim > self.declared_max_status:
            raise P0Incident(
                f"{self.name}: claims status {own_claim.label()} but declared_max_status "
                f"is {self.declared_max_status.label()}. The layer is over-claiming."
            )

        input_floor = min(
            (inp.status for inp in inputs), default=EpistemicTier.PROVEN
        )
        precondition_floor = (
            own_claim
            if all(p.holds for p in preconditions)
            else _demote(own_claim)
        )
        effective = min(own_claim, input_floor, precondition_floor)

        # 5. Build the output StatusedValue.
        provenance = self.declare_provenance(inputs)
        out = StatusedValue(
            value=raw_value,
            status=effective,
            provenance=provenance,
            preconditions=preconditions,
            sample_size=getattr(self, "sample_size", None),
        )

        # 6. Emit telemetry. NEVER skip this.
        AUDIT_LOG.write(
            StatusRecord(
                record_id=out.value_id,
                timestamp=dt.datetime.now(dt.timezone.utc),
                layer=self.name,
                declared_status=own_claim,
                effective_status=effective,
                provenance=provenance,
                preconditions=preconditions,
                sample_size=out.sample_size,
                note=f"effective_status = min({own_claim.label()}, "
                     f"input_floor={input_floor.label()}, "
                     f"precondition_floor={precondition_floor.label()})",
            )
        )

        return out


# ---------------------------------------------------------------------------
# 10. Federation rule
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class FederationUpdate:
    """A client's contribution to the federated parameter pool."""

    client_id: str
    parameter_name: str
    parameter_update: Any
    parameter_status_at_emission: EpistemicTier
    sample_size: int
    drift_signal: DriftSignal
    preconditions_verified: tuple[str, ...]


def aggregate_federation_updates(
    updates: Sequence[FederationUpdate],
    *,
    aggregator: Callable[[Sequence[Any]], Any],
) -> StatusedValue:
    """Aggregate client updates into a global parameter.

    Quarantine RED/BLACK clients. The aggregated status is the MINIMUM of
    contributing statuses. Aggregation cannot promote.
    """
    valid = [u for u in updates if u.drift_signal in (DriftSignal.GREEN, DriftSignal.AMBER)]
    if not valid:
        raise P0Incident("aggregate_federation_updates: no valid client updates after quarantine.")

    aggregated_value = aggregator([u.parameter_update for u in valid])
    aggregated_status = min(u.parameter_status_at_emission for u in valid)
    aggregated_n = sum(u.sample_size for u in valid)

    return StatusedValue(
        value=aggregated_value,
        status=aggregated_status,   # cannot exceed the minimum input status
        provenance=Provenance(
            layer="federation_aggregator",
            method="weighted_mean",
            inputs=tuple(u.client_id for u in valid),
        ),
        sample_size=aggregated_n,
    )

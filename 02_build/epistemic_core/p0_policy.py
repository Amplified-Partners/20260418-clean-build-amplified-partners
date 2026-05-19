"""
P0 policy — how the system reacts to Layer 0 violations.

Any silent promotion across a boundary is P0, even one tier.
Gap size is severity metadata, not the P0 trigger.

Production default: HALT. The system stops making decisions until
a human has signed off.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import enum
import logging

from epistemic_core.tiers import EpistemicTier

log = logging.getLogger("amplified.epistemic.p0")


class P0Incident(Exception):
    """Raised when the system catches itself laundering status.

    ANY silent promotion across a boundary is P0 — even one tier.
    Gap size is severity metadata only.

    The system MUST halt. A deterministic fallback may be returned to the
    caller, but the apparatus does not continue making decisions until a
    human has signed off.
    """

    def __init__(self, message: str, *, gap: int = 0) -> None:
        self.gap = gap
        super().__init__(message)


class P0Policy(enum.Enum):
    """Response to epistemic invariant violations.

    HALT is the production default. DEGRADE and TELEMETRY_ONLY exist
    for explicitly labelled experimental/backfill modes only.
    """

    HALT = "halt"
    DEGRADE = "degrade"
    TELEMETRY_ONLY = "telemetry_only"


# Active policy — override only in test fixtures or explicit backfill modes
ACTIVE_P0_POLICY: P0Policy = P0Policy.HALT


def enforce_p0(
    *,
    declared: EpistemicTier,
    effective: EpistemicTier,
    context: str,
    policy: P0Policy | None = None,
) -> None:
    """Check for silent promotion and enforce P0 policy.

    Any silent promotion across a boundary is P0, even one tier.
    Gap size is severity metadata only, not the P0 trigger.

    Raises P0Incident if policy is HALT and promotion detected.
    Logs the violation regardless of policy.
    """
    active = policy or ACTIVE_P0_POLICY

    if effective > declared:
        # This should never happen — the min-rule prevents upward movement.
        # If we get here, something bypassed the min-rule.
        gap = effective.value - declared.value
        msg = (
            f"Silent promotion detected: effective={effective.label()} > "
            f"declared={declared.label()} (gap={gap} tier(s)). "
            f"Context: {context}"
        )
        log.error("P0 INCIDENT: %s", msg)

        if active == P0Policy.HALT:
            raise P0Incident(msg, gap=gap)

    if effective < declared:
        # Legal demotion — the min-rule correctly reduced the tier.
        # Not a P0, but worth logging for drift detection.
        gap = declared.value - effective.value
        log.info(
            "Legal demotion: declared=%s effective=%s gap=%d context=%s",
            declared.label(),
            effective.label(),
            gap,
            context,
        )

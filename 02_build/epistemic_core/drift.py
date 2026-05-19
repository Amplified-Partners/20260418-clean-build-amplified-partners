"""
Drift detector — watches the audit log for the lying condition.

CRITICAL RULE (DeepSeek V4 review, confirmed by Ewan):
  Any silent promotion across a boundary is P0, even one tier.
  Gap size is severity metadata, not the P0 trigger.

The DriftDetector subscribes to the audit log and emits a signal
on every record. BLACK = P0Incident raised. The routing engine halts.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import enum
import logging

from epistemic_core.audit import AuditLog, StatusRecord
from epistemic_core.p0_policy import P0Incident

log = logging.getLogger("amplified.epistemic.drift")


class DriftSignal(enum.Enum):
    GREEN = "green"     # all declared statuses match observed behaviour
    AMBER = "amber"     # a precondition is within threshold of failure
    RED = "red"         # operating below declared status (legal demotion, but watch it)
    BLACK = "black"     # status laundering detected (P0)


class DriftDetector:
    """Subscribes to the audit log. Emits a signal on every record.

    BLACK signal = P0Incident raised. The routing engine halts.

    Any silent promotion across a boundary is P0, even one tier.
    Gap size is severity metadata (attached to the P0Incident), not the
    trigger condition.
    """

    def __init__(self, audit_log: AuditLog) -> None:
        self.audit_log = audit_log
        self.signal: DriftSignal = DriftSignal.GREEN
        self._incidents: list[str] = []
        audit_log.subscribe(self._on_record)

    def _on_record(self, record: StatusRecord) -> None:
        # BLACK: effective status is ABOVE declared status.
        # Any silent promotion = P0, even one tier.
        if record.effective_status > record.declared_status:
            gap = record.effective_status.value - record.declared_status.value
            self.signal = DriftSignal.BLACK
            msg = (
                f"DRIFT BLACK: layer {record.layer} declared "
                f"{record.declared_status.label()}, effective "
                f"{record.effective_status.label()}. "
                f"Silent promotion detected (gap={gap} tier(s))."
            )
            log.error(msg)
            self._incidents.append(msg)
            raise P0Incident(msg, gap=gap)

        # RED: effective status is below declared by any amount.
        # This is a legal demotion (min-rule working correctly), but
        # it means the layer is operating below its claim.
        if record.effective_status < record.declared_status:
            gap = record.declared_status.value - record.effective_status.value
            self.signal = DriftSignal.RED
            log.warning(
                "DRIFT RED: layer %s declared %s, effective %s. "
                "Legal demotion, gap=%d tier(s).",
                record.layer,
                record.declared_status.label(),
                record.effective_status.label(),
                gap,
            )
            return

        # AMBER: any precondition holds=False. The layer auto-demoted itself,
        # which is honest, but we want a human to know.
        failing = [p for p in record.preconditions if not p.holds]
        if failing:
            self.signal = DriftSignal.AMBER
            log.warning(
                "DRIFT AMBER: layer %s has %d failing precondition(s): %s",
                record.layer,
                len(failing),
                ", ".join(p.name for p in failing),
            )
            return

        self.signal = DriftSignal.GREEN

    @property
    def incidents(self) -> tuple[str, ...]:
        return tuple(self._incidents)

"""Vellum deletion receipts for sidecar cleanup.

Every cleanup operation emits a Vellum deletion receipt. This ensures:
  - We have proof that ephemeral context was destroyed
  - No silent data retention
  - Auditable cleanup trail

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from epistemic_core.tiers import EpistemicTier
from epistemic_core.vellum_emitter import VellumEmitter
from epistemic_core.vellum_event import VellumEvent
from sidecar.cleanup import CleanupResult
from sidecar.models import EphemeralSession


def emit_deletion_receipt(
    emitter: VellumEmitter,
    session: EphemeralSession,
    result: CleanupResult,
    *,
    actor: str = "sidecar",
) -> bool:
    """Emit a Vellum deletion receipt for a cleanup operation.

    Returns True if the event was written (or buffered), False if duplicate.
    """
    event = VellumEvent(
        event_type=f"sidecar.cleanup.{result.reason}",
        actor=actor,
        component="sidecar.cleanup",
        subject_id=session.session_id,
        previous_state=result.previous_state,
        new_state=result.new_state,
        epistemic_tier=EpistemicTier.STRUCTURED,
        metadata={
            "context_wiped": result.context_wiped,
            "saas_refs_wiped": result.saas_refs_wiped,
            "reason": result.reason,
            "owner": session.owner,
            "purpose": session.purpose,
        },
    )

    return emitter.emit(event)


def emit_session_event(
    emitter: VellumEmitter,
    session: EphemeralSession,
    event_type: str,
    *,
    actor: str = "sidecar",
    previous_state: str = "",
    detail: str = "",
) -> bool:
    """Emit a generic sidecar session event."""
    event = VellumEvent(
        event_type=f"sidecar.{event_type}",
        actor=actor,
        component="sidecar",
        subject_id=session.session_id,
        previous_state=previous_state,
        new_state=session.state,
        epistemic_tier=EpistemicTier.INTUITED,
        metadata={
            "owner": session.owner,
            "purpose": session.purpose,
            "detail": detail,
        },
    )

    return emitter.emit(event)

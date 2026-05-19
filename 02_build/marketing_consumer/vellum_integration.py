"""Vellum event emission for marketing consumer state transitions.

Every state transition emits a VellumEvent. Vellum is the witness.

Events emitted:
  - marketing.draft_created
  - marketing.reviewed
  - marketing.approved
  - marketing.dry_run_executed
  - marketing.sent
  - marketing.blocked

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from epistemic_core.tiers import EpistemicTier
from epistemic_core.vellum_emitter import VellumEmitter
from epistemic_core.vellum_event import VellumEvent
from marketing_consumer.models import MarketingArtifact, PublicationState


# Map from state to event type
STATE_EVENT_MAP: dict[PublicationState, str] = {
    "draft": "marketing.draft_created",
    "reviewed": "marketing.reviewed",
    "approved": "marketing.approved",
    "dry_run": "marketing.dry_run_executed",
    "sent": "marketing.sent",
    "blocked": "marketing.blocked",
}


def emit_state_event(
    emitter: VellumEmitter,
    artifact: MarketingArtifact,
    *,
    actor: str = "marketing_consumer",
    previous_state: str = "",
    detail: str = "",
) -> bool:
    """Emit a Vellum event for the current state of a marketing artifact.

    Returns True if the event was written (or buffered), False if duplicate.
    """
    event_type = STATE_EVENT_MAP.get(artifact.state, f"marketing.{artifact.state}")

    expected_next = ""
    if artifact.state == "draft":
        expected_next = "reviewed"
    elif artifact.state == "reviewed":
        expected_next = "approved"
    elif artifact.state == "approved":
        expected_next = "dry_run"
    elif artifact.state == "dry_run":
        expected_next = "sent"

    event = VellumEvent(
        event_type=event_type,
        actor=actor,
        component="marketing_consumer",
        subject_id=artifact.artifact_id,
        previous_state=previous_state,
        new_state=artifact.state,
        epistemic_tier=EpistemicTier.INTUITED,
        provenance_refs=[artifact.brain_packet_id] if artifact.brain_packet_id else [],
        evidence_refs=artifact.evidence_refs,
        permission_scope=artifact.channel or "unknown",
        expected_next_state=expected_next,
        metadata={
            "title": artifact.title,
            "channel": artifact.channel,
            "detail": detail,
        },
    )

    return emitter.emit(event)

"""Marketing publication state machine.

States: draft → reviewed → approved → dry_run → sent
                                              ↘ blocked

The approval gate between approved and sent is enforced:
  - approved → dry_run is automatic (dry-run always runs first)
  - dry_run → sent requires an explicit approval signal
  - dry_run → blocked if guardrails fail or approval is denied

Marketing-Kaizen emits candidates, never canonical truth.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from marketing_consumer.models import (
    MarketingArtifact,
    PublicationState,
)


class InvalidTransition(Exception):
    """Raised when a state transition is not allowed."""


class MissingApproval(Exception):
    """Raised when trying to send without explicit approval."""


# Valid transitions: from_state → set of allowed to_states
VALID_TRANSITIONS: dict[PublicationState, frozenset[PublicationState]] = {
    "draft": frozenset({"reviewed"}),
    "reviewed": frozenset({"approved", "blocked"}),
    "approved": frozenset({"dry_run"}),
    "dry_run": frozenset({"sent", "blocked"}),
    "sent": frozenset(),
    "blocked": frozenset(),
}


def transition(
    artifact: MarketingArtifact,
    to_state: PublicationState,
) -> MarketingArtifact:
    """Move an artifact to a new state. Validates the transition.

    The dry_run → sent transition requires an approval_signal on the artifact.
    Returns a new MarketingArtifact (immutable-style).
    """
    allowed = VALID_TRANSITIONS.get(artifact.state, frozenset())
    if to_state not in allowed:
        raise InvalidTransition(
            f"Cannot transition from '{artifact.state}' to '{to_state}'. "
            f"Allowed: {sorted(allowed) if allowed else 'none (terminal state)'}."
        )

    if to_state == "sent" and not artifact.approval_signal.strip():
        raise MissingApproval(
            "Cannot send artifact without explicit approval_signal. "
            "Marketing defaults to dry-run. Real send requires approval."
        )

    return artifact.model_copy(update={"state": to_state})

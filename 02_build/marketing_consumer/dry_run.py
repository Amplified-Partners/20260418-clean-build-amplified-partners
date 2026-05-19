"""Brevo adapter — defaults to dry-run.

Real send requires an explicit approval signal. Without it, the
adapter simulates the send and records the result.

Marketing-Kaizen emits candidates, never canonical truth.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from marketing_consumer.guardrails import run_guardrails
from marketing_consumer.models import MarketingArtifact
from marketing_consumer.state_machine import (
    InvalidTransition,
    MissingApproval,
    transition,
)


@dataclass
class DryRunResult:
    """Result of a dry-run or real send attempt."""

    sent: bool
    dry_run: bool
    blocked: bool
    reason: str
    timestamp: datetime


def execute_send(
    artifact: MarketingArtifact,
    *,
    force_approve: bool = False,
) -> tuple[MarketingArtifact, DryRunResult]:
    """Attempt to send a marketing artifact through the pipeline.

    The pipeline enforces:
      1. Guardrails must pass
      2. State must be in 'approved' or 'dry_run'
      3. Without explicit approval_signal, remains dry-run

    If force_approve is True and guardrails pass, sets the approval
    signal and transitions to sent. This is the explicit approval path.

    Returns (updated_artifact, result).
    """
    now = datetime.now(timezone.utc)

    # Run guardrails first
    guardrail_result = run_guardrails(artifact)
    if not guardrail_result.passed:
        blocked_artifact = artifact.model_copy(update={
            "state": "blocked",
            "dry_run_result": "; ".join(guardrail_result.violations),
        })
        return blocked_artifact, DryRunResult(
            sent=False,
            dry_run=False,
            blocked=True,
            reason=f"Guardrail violations: {'; '.join(guardrail_result.violations)}",
            timestamp=now,
        )

    # Transition to dry_run if in approved state
    if artifact.state == "approved":
        artifact = transition(artifact, "dry_run")

    # If not in dry_run state, cannot proceed
    if artifact.state != "dry_run":
        return artifact, DryRunResult(
            sent=False,
            dry_run=False,
            blocked=True,
            reason=f"Cannot send from state '{artifact.state}'. Must be in 'dry_run'.",
            timestamp=now,
        )

    # Dry-run simulation
    dry_run_artifact = artifact.model_copy(update={
        "dry_run_result": "dry_run_success",
    })

    if not force_approve:
        return dry_run_artifact, DryRunResult(
            sent=False,
            dry_run=True,
            blocked=False,
            reason="Dry-run completed successfully. Real send requires explicit approval.",
            timestamp=now,
        )

    # Explicit approval path
    approved_artifact = dry_run_artifact.model_copy(update={
        "approval_signal": "explicit_approval",
        "approved_by": "system",
    })
    try:
        sent_artifact = transition(approved_artifact, "sent")
    except (InvalidTransition, MissingApproval) as e:
        return approved_artifact, DryRunResult(
            sent=False,
            dry_run=True,
            blocked=True,
            reason=str(e),
            timestamp=now,
        )

    return sent_artifact, DryRunResult(
        sent=True,
        dry_run=False,
        blocked=False,
        reason="Sent with explicit approval.",
        timestamp=now,
    )

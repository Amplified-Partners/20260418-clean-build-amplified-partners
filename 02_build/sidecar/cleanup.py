"""Sidecar cleanup — deterministic context destruction.

Four cleanup paths:
  1. Normal completion: session closed, context wiped
  2. Exception path: session errored, context wiped
  3. Expired TTL: session expired, context wiped
  4. Startup scavenger: finds non-terminal sessions and cleans them

After cleanup, no raw SaaS context persists.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sidecar.lifecycle import (
    check_ttl,
    close_session,
    error_session,
)
from sidecar.models import EphemeralSession


@dataclass
class CleanupResult:
    """Result of a cleanup operation."""

    session_id: str
    previous_state: str
    new_state: str
    context_wiped: bool
    saas_refs_wiped: bool
    reason: str


def _wipe_context(session: EphemeralSession) -> EphemeralSession:
    """Remove all ephemeral context and SaaS refs from a session."""
    return session.model_copy(update={
        "context": {},
        "saas_refs": [],
        "candidate_signals": [],
    })


def cleanup_normal(session: EphemeralSession) -> tuple[EphemeralSession, CleanupResult]:
    """Cleanup path 1: normal completion."""
    previous = session.state
    closed = close_session(session)
    wiped = _wipe_context(closed)
    return wiped, CleanupResult(
        session_id=session.session_id,
        previous_state=previous,
        new_state=wiped.state,
        context_wiped=True,
        saas_refs_wiped=True,
        reason="normal_completion",
    )


def cleanup_exception(session: EphemeralSession) -> tuple[EphemeralSession, CleanupResult]:
    """Cleanup path 2: exception path."""
    previous = session.state
    errored = error_session(session)
    wiped = _wipe_context(errored)
    return wiped, CleanupResult(
        session_id=session.session_id,
        previous_state=previous,
        new_state=wiped.state,
        context_wiped=True,
        saas_refs_wiped=True,
        reason="exception_path",
    )


def cleanup_expired(session: EphemeralSession) -> tuple[EphemeralSession, CleanupResult]:
    """Cleanup path 3: expired TTL."""
    previous = session.state
    checked = check_ttl(session)
    if not checked.is_terminal:
        checked = close_session(checked)
    wiped = _wipe_context(checked)
    return wiped, CleanupResult(
        session_id=session.session_id,
        previous_state=previous,
        new_state=wiped.state,
        context_wiped=True,
        saas_refs_wiped=True,
        reason="expired_ttl",
    )


@dataclass
class ScavengerReport:
    """Report from the startup scavenger."""

    cleaned: list[CleanupResult] = field(default_factory=list)
    skipped: int = 0


def startup_scavenger(
    sessions: list[EphemeralSession],
) -> tuple[list[EphemeralSession], ScavengerReport]:
    """Cleanup path 4: startup scavenger.

    Finds all non-terminal sessions and cleans them up.
    Used on system startup to clear any leaked sessions from prior runs.
    """
    report = ScavengerReport()
    cleaned_sessions: list[EphemeralSession] = []

    for session in sessions:
        if session.is_terminal:
            report.skipped += 1
            cleaned_sessions.append(session)
            continue

        if session.is_expired:
            wiped, result = cleanup_expired(session)
        else:
            wiped, result = cleanup_exception(session)
            result.reason = "startup_scavenger"

        report.cleaned.append(result)
        cleaned_sessions.append(wiped)

    return cleaned_sessions, report

"""Sidecar session lifecycle — open/use/close with TTL enforcement.

States: open → active → closing → closed
                                 ↘ expired (TTL hit)
                                 ↘ error (exception path)

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from typing import Any

from sidecar.models import EphemeralSession, SessionState


class InvalidTransition(Exception):
    """Raised when a session state transition is not allowed."""


class SessionExpired(Exception):
    """Raised when operating on an expired session."""


VALID_TRANSITIONS: dict[SessionState, frozenset[SessionState]] = {
    "open": frozenset({"active", "closing", "expired", "error"}),
    "active": frozenset({"closing", "expired", "error"}),
    "closing": frozenset({"closed", "error"}),
    "closed": frozenset(),
    "expired": frozenset(),
    "error": frozenset(),
}


def transition(
    session: EphemeralSession,
    to_state: SessionState,
) -> EphemeralSession:
    """Move a session to a new state. Validates the transition."""
    allowed = VALID_TRANSITIONS.get(session.state, frozenset())
    if to_state not in allowed:
        raise InvalidTransition(
            f"Cannot transition from '{session.state}' to '{to_state}'. "
            f"Allowed: {sorted(allowed) if allowed else 'none (terminal)'}."
        )
    return session.model_copy(update={"state": to_state})


def use_session(
    session: EphemeralSession,
    context_update: dict[str, Any] | None = None,
) -> EphemeralSession:
    """Use a session: activate if open, add context, enforce TTL.

    Raises SessionExpired if the TTL has been exceeded.
    """
    if session.is_expired:
        raise SessionExpired(
            f"Session '{session.session_id}' expired at "
            f"{session.expires_at}."
        )

    if session.is_terminal:
        raise InvalidTransition(
            f"Cannot use session in terminal state '{session.state}'."
        )

    updated = session
    if updated.state == "open":
        updated = transition(updated, "active")

    if context_update:
        new_context = {**updated.context, **context_update}
        updated = updated.model_copy(update={"context": new_context})

    return updated


def close_session(session: EphemeralSession) -> EphemeralSession:
    """Close a session normally. Transitions through closing → closed."""
    if session.is_terminal:
        return session
    updated = session
    if updated.state in ("open", "active"):
        updated = transition(updated, "closing")
    return transition(updated, "closed")


def expire_session(session: EphemeralSession) -> EphemeralSession:
    """Expire a session due to TTL. Callable from cleanup scavenger."""
    if session.is_terminal:
        return session
    return transition(session, "expired")


def error_session(session: EphemeralSession) -> EphemeralSession:
    """Move a session to error state (exception path)."""
    if session.is_terminal:
        return session
    return transition(session, "error")


def check_ttl(session: EphemeralSession) -> EphemeralSession:
    """Check TTL and expire if needed. Idempotent."""
    if session.is_expired and not session.is_terminal:
        return expire_session(session)
    return session

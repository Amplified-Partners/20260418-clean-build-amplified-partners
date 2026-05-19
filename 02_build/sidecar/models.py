"""Sidecar ephemeral context models.

Two context types, kept strictly separate:
  - EphemeralSession: short-lived, TTL-enforced, cleaned up deterministically
  - StablePreference: long-lived user preferences (separate from SaaS context)

Sidecar never becomes a source of record for customer/contact data.
Signals extracted from sessions are candidate-only and permission-scoped.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Session states
# ---------------------------------------------------------------------------

SessionState = Literal[
    "open",
    "active",
    "closing",
    "closed",
    "expired",
    "error",
]

TERMINAL_STATES: frozenset[str] = frozenset({"closed", "expired", "error"})

DEFAULT_TTL_HOURS: int = 1


# ---------------------------------------------------------------------------
# Ephemeral session
# ---------------------------------------------------------------------------


class EphemeralSession(BaseModel):
    """A short-lived sidecar session with TTL enforcement.

    Context stored here is destroyed on completion, exception, or expiry.
    Never a source of record for customer/contact data.
    """

    session_id: str = Field(default_factory=lambda: str(uuid4()))
    state: SessionState = "open"
    owner: str = ""
    purpose: str = ""

    # TTL enforcement
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    ttl_hours: int = DEFAULT_TTL_HOURS
    expires_at: datetime | None = None

    # Ephemeral context (destroyed on cleanup)
    context: dict[str, Any] = Field(default_factory=dict)
    saas_refs: list[str] = Field(default_factory=list)

    # Permission scoping
    permission_scope: str = "session_only"
    candidate_signals: list[str] = Field(default_factory=list)

    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: object) -> None:
        if self.expires_at is None:
            self.expires_at = self.created_at + timedelta(hours=self.ttl_hours)

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_terminal(self) -> bool:
        return self.state in TERMINAL_STATES


# ---------------------------------------------------------------------------
# Stable preference context (separate from SaaS context)
# ---------------------------------------------------------------------------


class StablePreference(BaseModel):
    """Long-lived user preference, separate from SaaS context.

    Preferences are NOT ephemeral — they persist across sessions.
    They do NOT contain customer/contact data from SaaS systems.
    """

    preference_id: str = Field(default_factory=lambda: str(uuid4()))
    key: str
    value: str
    category: str = "general"
    owner: str = ""
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

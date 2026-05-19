"""Marketing consumer domain models.

Every marketing artifact carries references back to the shared substrate:
  - context_packet_id: runtime envelope from Brain MCP
  - brain_packet_id: governed packet from brain_curator
  - evidence_refs: list of evidence chunk IDs supporting claims

Marketing-Kaizen emits candidates, never canonical truth.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Publication states
# ---------------------------------------------------------------------------

PublicationState = Literal[
    "draft",
    "reviewed",
    "approved",
    "dry_run",
    "sent",
    "blocked",
]

TERMINAL_STATES: frozenset[str] = frozenset({"sent", "blocked"})


# ---------------------------------------------------------------------------
# Marketing artifact
# ---------------------------------------------------------------------------


class MarketingArtifact(BaseModel):
    """A marketing artifact that references the shared substrate.

    Never forks the schema — always links back to brain_packet_id.
    """

    artifact_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    content: str
    state: PublicationState = "draft"

    # Substrate references (no forked schema)
    context_packet_id: str = ""
    brain_packet_id: str
    evidence_refs: list[str] = Field(default_factory=list)

    # Attribution
    author: str = ""
    channel: str = ""  # e.g. "linkedin", "email", "twitter"
    persona: str = ""  # must not be fake

    # Metadata
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Approval tracking
    approval_signal: str = ""
    approved_by: str = ""
    dry_run_result: str = ""

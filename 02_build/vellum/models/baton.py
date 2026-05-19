"""BatonPass — the API payload sent to the Ledger when a session finishes.

Closes the MCP Context Pipe loop:
  Agent works (MCP context) → Agent finishes (baton pass to Ledger)
  → Ledger evaluates → Next agent wakes up.

Payload mirrors the three enforcer-checked sections:
  1. what_happened  — "What Happened This Session"
  2. implications    — "What This Means"
  3. actions_required — "Ewan Needs To Do" / next-agent actions

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

EpistemicTier = Literal["INTUITED", "STRUCTURED", "MEASURED", "PROVEN"]


class WorkReference(BaseModel):
    """A pointer to work output — PR, commit, file, Linear ticket, etc."""

    kind: Literal["pr", "commit", "file", "linear_ticket", "other"] = "other"
    ref: str = ""
    url: str = ""
    description: str = ""


class BatonPass(BaseModel):
    """The baton pass payload — sent to the Ledger when a session finishes.

    This is an API payload, not a text file. It is the atomic unit of
    session handover in the MCP Context Pipe.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    agent_id: str = ""
    tenant_id: str = "ewan"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # --- The three enforcer-checked sections ---
    what_happened: str = ""
    implications: str = ""
    actions_required: list[str] = Field(default_factory=list)

    # --- Work references ---
    work_refs: list[WorkReference] = Field(default_factory=list)

    # --- Context pipe metadata ---
    context_saturation_pct: float = 0.0
    next_agent: str = ""
    epistemic_tier: EpistemicTier = "INTUITED"
    metadata: dict = Field(default_factory=dict)

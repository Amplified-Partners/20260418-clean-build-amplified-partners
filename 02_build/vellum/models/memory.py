"""Memory candidate models — extracted from session entries.

A memory candidate is something worth remembering. The ingestion gate
decides whether it actually enters the Brain's long-term memory.

Rule: "Save it only if it changes future behaviour." — Ewan Bramley

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

EpistemicTier = Literal["INTUITED", "STRUCTURED", "MEASURED", "PROVEN"]

CandidateKind = Literal[
    "preference",
    "correction",
    "task_outcome",
    "new_entity",
    "repeated_pattern",
    "failed_approach",
    "tool_quirk",
    "procedure_improvement",
    "if_then_lesson",
    "explicit_remember",
]

GateVerdict = Literal["ADMIT", "REJECT", "QUARANTINE"]


class MemoryCandidate(BaseModel):
    """A memory-worthy item extracted from a session entry."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    source_entry_id: str
    source_sheet_id: str
    agent_id: str = ""
    tenant_id: str = "ewan"
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    kind: CandidateKind
    content: str
    reasoning: str = ""
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    epistemic_tier: EpistemicTier = "INTUITED"
    metadata: dict = Field(default_factory=dict)


class GateDecision(BaseModel):
    """The ingestion gate's verdict on a memory candidate."""

    candidate_id: str
    verdict: GateVerdict
    reason_codes: list[str] = Field(default_factory=list)
    changes_future_behaviour: bool = False
    epistemic_tier: EpistemicTier = "INTUITED"
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

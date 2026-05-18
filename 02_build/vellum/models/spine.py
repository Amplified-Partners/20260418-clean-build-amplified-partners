"""Portable Spine model — the operational continuity layer for each agent.

Not metaphysical. Operational. Contains: who the agent is, what lens it
uses, behavioural priors, known failure patterns, procedural constraints,
personal experience line, current job context.

Served by the Brain on agent wakeup. Updated by the Brain when sessions
produce learnings that change future behaviour.

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

EpistemicTier = Literal["INTUITED", "STRUCTURED", "MEASURED", "PROVEN"]


class BehaviouralPrior(BaseModel):
    """A known pattern the agent should carry forward."""

    description: str
    source_session: str = ""
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    epistemic_tier: EpistemicTier = "INTUITED"


class FailurePattern(BaseModel):
    """A known failure mode — so the agent doesn't repeat it."""

    description: str
    source_session: str = ""
    times_observed: int = 1
    mitigation: str = ""


class PortableSpine(BaseModel):
    """The portable spine for one agent.

    On wake: read this. Before stop: update via baton pass.
    Hierarchy: Spine > Project > Session.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    agent_name: str = ""
    tenant_id: str = "ewan"
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    lens: str = ""
    role: str = ""
    behavioural_priors: list[BehaviouralPrior] = Field(default_factory=list)
    failure_patterns: list[FailurePattern] = Field(default_factory=list)
    procedural_constraints: list[str] = Field(default_factory=list)
    experience_line: str = ""
    current_job_context: str = ""

    if_then_lessons: list[str] = Field(default_factory=list)
    decision_log_refs: list[str] = Field(default_factory=list)

    epistemic_tier: EpistemicTier = "INTUITED"
    metadata: dict = Field(default_factory=dict)

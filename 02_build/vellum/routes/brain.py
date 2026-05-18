"""Brain routes — the four measured loop endpoints.

1. GET  /api/v1/brain/spine      — portable spine per-agent
2. PUT  /api/v1/brain/spine      — register/update a spine
3. GET  /api/v1/brain/context    — full context packet for agent wakeup
4. POST /api/v1/brain/extract    — extract memory candidates from entries
5. POST /api/v1/brain/ingest     — run ingestion gate on candidates

These four pieces close the minimum measured loop:
  Vellum senses → pre-filled baton → agent adds thoughts →
  next agent wakes with spine → Brain supplies packet →
  agent works → Vellum records → memory candidates generated →
  ingestion gate decides

Devon-58ca | 2026-05-18
"""

from __future__ import annotations

import logging
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from vellum.models.entry import SheetEntry
from vellum.models.memory import CandidateKind, GateDecision, MemoryCandidate
from vellum.models.spine import (
    BehaviouralPrior,
    FailurePattern,
    PortableSpine,
)
from vellum.services.context_server import assemble_context_packet
from vellum.services.ingestion_gate import evaluate_candidate, run_gate
from vellum.services.memory_extractor import (
    extract_candidates,
    extract_from_sheet_entries,
)
from vellum.services.spine_server import (
    clear_spines,
    get_spine,
    list_spines,
    register_spine,
    update_spine_from_baton,
)
from vellum.storage import get_store

log = logging.getLogger("vellum.brain")
router = APIRouter(prefix="/api/v1/brain", tags=["brain"])


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------


class SpineRegistration(BaseModel):
    """Register a new portable spine for an agent."""

    agent_id: str
    agent_name: str = ""
    tenant_id: str = "ewan"
    lens: str = ""
    role: str = ""
    behavioural_priors: list[dict] = Field(default_factory=list)
    failure_patterns: list[dict] = Field(default_factory=list)
    procedural_constraints: list[str] = Field(default_factory=list)
    experience_line: str = ""
    current_job_context: str = ""
    if_then_lessons: list[str] = Field(default_factory=list)


class SpineUpdateFromBaton(BaseModel):
    """Update a spine with learnings from a baton pass."""

    agent_id: str
    tenant_id: str = "ewan"
    failed_paths: list[str] = Field(default_factory=list)
    if_then_lessons: list[str] = Field(default_factory=list)
    decision_log_refs: list[str] = Field(default_factory=list)
    experience_line: str = ""
    job_context: str = ""


class ExtractRequest(BaseModel):
    """Request to extract memory candidates from a sheet."""

    sheet_id: str
    tenant_id: str = "ewan"


class IngestRequest(BaseModel):
    """Request to run the ingestion gate on memory candidates."""

    candidates: list[dict] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# 1. Spine endpoints
# ---------------------------------------------------------------------------


@router.get("/spine")
async def read_spine(agent_id: str, tenant_id: str = "ewan") -> dict:
    """Read the portable spine for an agent.

    Served on agent wakeup. Contains: identity, lens, behavioural
    priors, known failure patterns, procedural constraints, experience
    line, current job context, IF-THEN lessons.
    """
    spine = get_spine(agent_id, tenant_id)
    if spine is None:
        raise HTTPException(status_code=404, detail=f"No spine for agent '{agent_id}'")
    return {
        "status": "ok",
        "spine": spine.model_dump(mode="json"),
    }


@router.get("/spines")
async def read_all_spines(tenant_id: str = "ewan") -> dict:
    """List all registered spines for a tenant."""
    spines = list_spines(tenant_id)
    return {
        "status": "ok",
        "spines": [s.model_dump(mode="json") for s in spines],
        "count": len(spines),
    }


@router.put("/spine")
async def upsert_spine(body: SpineRegistration) -> dict:
    """Register or replace a portable spine for an agent."""
    priors = [BehaviouralPrior(**p) for p in body.behavioural_priors]
    patterns = [FailurePattern(**f) for f in body.failure_patterns]

    spine = PortableSpine(
        agent_id=body.agent_id,
        agent_name=body.agent_name,
        tenant_id=body.tenant_id,
        lens=body.lens,
        role=body.role,
        behavioural_priors=priors,
        failure_patterns=patterns,
        procedural_constraints=body.procedural_constraints,
        experience_line=body.experience_line,
        current_job_context=body.current_job_context,
        if_then_lessons=body.if_then_lessons,
    )
    registered = register_spine(spine)
    return {
        "status": "ok",
        "spine_id": registered.id,
        "agent_id": registered.agent_id,
    }


@router.patch("/spine")
async def patch_spine_from_baton(body: SpineUpdateFromBaton) -> dict:
    """Update a spine with learnings from a baton pass.

    Appends failed paths, IF-THEN lessons, decision log refs.
    Updates experience line and job context if provided.
    """
    updated = update_spine_from_baton(
        body.agent_id,
        body.tenant_id,
        failed_paths=body.failed_paths or None,
        if_then_lessons=body.if_then_lessons or None,
        decision_log_refs=body.decision_log_refs or None,
        experience_line=body.experience_line or None,
        job_context=body.job_context or None,
    )
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"No spine for agent '{body.agent_id}' — register first",
        )
    return {
        "status": "ok",
        "spine_id": updated.id,
        "agent_id": updated.agent_id,
        "failure_patterns_count": len(updated.failure_patterns),
        "if_then_lessons_count": len(updated.if_then_lessons),
    }


# ---------------------------------------------------------------------------
# 2. Context packet endpoint
# ---------------------------------------------------------------------------


@router.get("/context")
async def read_context(
    agent_id: str,
    tenant_id: str = "ewan",
    max_recent: int = 20,
) -> dict:
    """Assemble the full context packet for an agent.

    Returns: spine + latest baton + recent entries + decisions + unread.
    This is the packet the next agent wakes up with.
    """
    packet = await assemble_context_packet(
        agent_id=agent_id,
        tenant_id=tenant_id,
        max_recent_entries=max_recent,
    )
    return {"status": "ok", **packet}


# ---------------------------------------------------------------------------
# 3. Memory candidate extraction endpoint
# ---------------------------------------------------------------------------


@router.post("/extract")
async def extract_memory(body: ExtractRequest) -> dict:
    """Extract memory candidates from all entries in a sheet.

    Scans the sheet's entries for memory-worthy items: corrections,
    failures, lessons, preferences, outcomes, tool quirks, etc.
    """
    store = get_store()
    sheet = await store.get_sheet(body.sheet_id)
    if sheet is None:
        raise HTTPException(status_code=404, detail="Sheet not found")

    candidates = extract_from_sheet_entries(sheet.entries)
    return {
        "status": "ok",
        "sheet_id": body.sheet_id,
        "candidates": [c.model_dump(mode="json") for c in candidates],
        "count": len(candidates),
    }


# ---------------------------------------------------------------------------
# 4. Ingestion gate endpoint
# ---------------------------------------------------------------------------


@router.post("/ingest")
async def ingest_memory(body: IngestRequest) -> dict:
    """Run the ingestion gate on memory candidates.

    Decides what enters long-term memory. Rule: "Save it only if
    it changes future behaviour."

    Returns a GateDecision for each candidate: ADMIT, REJECT, or
    QUARANTINE.
    """
    candidates = [MemoryCandidate(**c) for c in body.candidates]
    decisions = run_gate(candidates)

    admitted = [d for d in decisions if d.verdict == "ADMIT"]
    rejected = [d for d in decisions if d.verdict == "REJECT"]
    quarantined = [d for d in decisions if d.verdict == "QUARANTINE"]

    return {
        "status": "ok",
        "decisions": [d.model_dump(mode="json") for d in decisions],
        "summary": {
            "total": len(decisions),
            "admitted": len(admitted),
            "rejected": len(rejected),
            "quarantined": len(quarantined),
        },
    }

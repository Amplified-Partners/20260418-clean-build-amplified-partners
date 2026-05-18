"""Vellum FastAPI Server — dogfooding endpoint.

Serves the ingestion gate and signed records to Antigravity's React UI.
CORS enabled for localhost:5173 (Vite dev server).

Endpoint contract (agreed with Antigravity 2026-05-14):
  GET /api/v1/workpackets/pending → JSON with context_saturation + packets array

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import datetime as dt
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from vellum.gate.models import EpistemicStatus
from vellum.ingestion.gate import IngestionGate
from vellum.ingestion.models import (
    GateVerdict,
    SignedRecord,
    Submission,
    WriterType,
)
from vellum.ingestion.registry import build_default_registry

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Vellum Backend",
    version="0.1.0",
    description="Incorruptible message transfer layer. Correct or reject.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory state (dogfooding — will be Postgres later)
# ---------------------------------------------------------------------------

_registry = build_default_registry()
_gate = IngestionGate(_registry)
_records: list[SignedRecord] = []


# ---------------------------------------------------------------------------
# Response models (Antigravity's contract)
# ---------------------------------------------------------------------------


class RubricCheck(BaseModel):
    id: str
    rule: str
    passed: bool
    cognitive_impact: str = "MEDIUM"
    detail: str = ""


class PuddingResponse(BaseModel):
    what: str = ""
    how: str = ""
    scale: str = ""
    time: str = ""


class PacketResponse(BaseModel):
    id: str
    epistemic_tier: str
    title: str
    summary: str
    pudding: PuddingResponse
    rubric_checks: list[RubricCheck] = Field(default_factory=list)
    risk_tier: int = 1
    provenance: str = ""


class WorkpacketsPendingResponse(BaseModel):
    context_saturation_pct: int = 0
    context_saturation_state: str = "GREEN"
    packets: list[PacketResponse] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers: map SignedRecord → Antigravity's JSON contract
# ---------------------------------------------------------------------------


def _compute_context_saturation(records: list[SignedRecord]) -> tuple[int, str]:
    """Compute context saturation from current record count.

    Simple heuristic for dogfooding: saturation grows with pending work.
    """
    count = len(records)
    if count == 0:
        return (0, "GREEN")
    elif count <= 3:
        pct = min(count * 25, 75)
        return (pct, "GREEN")
    elif count <= 6:
        pct = min(50 + count * 8, 90)
        return (pct, "AMBER")
    else:
        return (100, "RED")


def _record_to_packet(record: SignedRecord) -> PacketResponse:
    """Map a SignedRecord to Antigravity's packet shape."""
    payload = record.payload

    # Extract title from payload (different fields depending on record type)
    title = (
        payload.get("task_id", "")
        or payload.get("decision", "")
        or payload.get("metric_name", "")
        or payload.get("intent", "")
        or payload.get("question", "")
        or record.record_type
    )
    if isinstance(title, str) and len(title) > 80:
        title = title[:77] + "..."

    # Extract summary
    summary = (
        payload.get("summary", "")
        or payload.get("finding", "")
        or payload.get("observation", "")
        or payload.get("decision", "")
        or f"{record.record_type} from {record.author}"
    )

    # Build rubric checks from gate validation (all passed if record exists)
    rubric_checks = [
        RubricCheck(
            id="proforma",
            rule="Proforma Validated",
            passed=True,
            cognitive_impact="HIGH",
            detail=f"All required fields present for {record.writer_type.value}/{record.record_type}",
        ),
        RubricCheck(
            id="signature",
            rule="Signature Present",
            passed=True,
            cognitive_impact="HIGH",
            detail=f"Signed by {record.author}",
        ),
        RubricCheck(
            id="tier_ceiling",
            rule="Tier Within Ceiling",
            passed=True,
            cognitive_impact="MEDIUM",
            detail=f"Assigned tier: {record.assigned_tier.label()}",
        ),
        RubricCheck(
            id="hash_chain",
            rule="Hash Chain Intact",
            passed=True,
            cognitive_impact="HIGH",
            detail=f"Chained from {record.previous_hash[:12]}...",
        ),
    ]

    # Risk tier based on epistemic status (lower tier = higher risk)
    risk_map = {
        EpistemicStatus.INTUITED: 3,
        EpistemicStatus.STRUCTURED: 2,
        EpistemicStatus.MEASURED: 1,
        EpistemicStatus.PROVEN: 0,
    }

    return PacketResponse(
        id=record.record_id,
        epistemic_tier=record.assigned_tier.label().upper(),
        title=str(title),
        summary=str(summary)[:500],
        pudding=PuddingResponse(),  # No PUDDING labels yet — will come from payload
        rubric_checks=rubric_checks,
        risk_tier=risk_map.get(record.assigned_tier, 2),
        provenance=record.provenance or f"{record.author} / Hash Chain",
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/api/v1/workpackets/pending", response_model=WorkpacketsPendingResponse)
def get_pending_workpackets() -> WorkpacketsPendingResponse:
    """Serve pending signed records to Antigravity's UI.

    This is the contract Antigravity is polling.
    """
    pct, state = _compute_context_saturation(_records)
    packets = [_record_to_packet(r) for r in _records]

    return WorkpacketsPendingResponse(
        context_saturation_pct=pct,
        context_saturation_state=state,
        packets=packets,
    )


class SubmissionRequest(BaseModel):
    """Incoming submission to the ingestion gate."""

    writer_type: str
    record_type: str
    claimed_epistemic_tier: str
    author: str
    session_id: str | None = None
    work_packet_id: str | None = None
    provenance: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    signature: str | None = None


class SubmissionResponse(BaseModel):
    """Response from the ingestion gate."""

    submission_id: str
    decision: str
    reason_codes: list[str] = Field(default_factory=list)
    effective_tier: str
    record_id: str | None = None


@app.post("/api/v1/submit", response_model=SubmissionResponse)
def submit_to_gate(req: SubmissionRequest) -> SubmissionResponse:
    """Submit a record to the ingestion gate. Correct or reject."""
    # Parse enums
    try:
        writer = WriterType(req.writer_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid writer_type: {req.writer_type}. Valid: {[w.value for w in WriterType]}",
        )

    tier_map = {
        "intuited": EpistemicStatus.INTUITED,
        "structured": EpistemicStatus.STRUCTURED,
        "measured": EpistemicStatus.MEASURED,
        "proven": EpistemicStatus.PROVEN,
    }
    tier = tier_map.get(req.claimed_epistemic_tier.lower())
    if tier is None:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid claimed_epistemic_tier: {req.claimed_epistemic_tier}. Valid: {list(tier_map.keys())}",
        )

    # Build submission
    submission = Submission(
        submission_id=str(uuid.uuid4()),
        writer_type=writer,
        record_type=req.record_type,
        claimed_epistemic_tier=tier,
        author=req.author,
        session_id=req.session_id,
        work_packet_id=req.work_packet_id,
        provenance=req.provenance,
        payload=req.payload,
        signature=req.signature,
    )

    # Evaluate
    verdict, record = _gate.evaluate(submission)

    if record is not None:
        _records.append(record)

    return SubmissionResponse(
        submission_id=submission.submission_id,
        decision=verdict.decision,
        reason_codes=verdict.reason_codes,
        effective_tier=verdict.effective_tier.label(),
        record_id=record.record_id if record else None,
    )


@app.get("/api/v1/records", response_model=list[dict[str, Any]])
def get_all_records() -> list[dict[str, Any]]:
    """Get all signed records (full detail)."""
    return [r.model_dump(mode="json") for r in _records]


@app.get("/api/v1/health")
def health() -> dict[str, Any]:
    """Health check."""
    return {
        "status": "healthy",
        "gate_version": "1.0.0",
        "record_count": _gate.record_count,
        "chain_head": _gate.previous_hash[:16] + "...",
        "registered_proformas": len(_registry),
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
    }

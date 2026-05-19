"""04_epistemic_tier — conservative deterministic tier assignment.

Rules:
  - Raw conversation chunks -> INTUITED
  - Human-approved doctrine with explicit rule -> STRUCTURED
  - Pipeline performance metric with counted sample -> MEASURED
  - Formal proof or hard DB invariant with verified preconditions -> PROVEN

Applies the min-rule: packet tier = min(own_tier_claim,
min(evidence_chunk_tiers), precondition_tier).

Uses ``epistemic_core.P0Incident`` for violations and
``epistemic_core.min_rule`` string-compat helpers for tier comparisons.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
Modified-by: Devon-d493 | 2026-05-19 | PR 2 — replace local P0TierViolation + tier_min with epistemic_core
"""

from __future__ import annotations

import json
import logging
from typing import Any

from epistemic_core.min_rule import tier_min_str as tier_min  # noqa: F401 — re-export
from epistemic_core.min_rule import tier_min_many_str as tier_min_many
from epistemic_core.p0_policy import ACTIVE_P0_POLICY, P0Incident, P0Policy
from epistemic_core.tiers import (
    TIER_INTUITED,
    TIER_MEASURED,
    TIER_RANK,
    TIER_STRUCTURED,
)

from brain_curator.config import CODE_VERSION
from brain_curator.db import complete_curation_run, connect_writer, start_curation_run

log = logging.getLogger("brain_curator.epistemic_tier")

# Backward compat alias — existing consumers may catch P0TierViolation
P0TierViolation = P0Incident


def assign_tier_for_packet(
    packet_type: str,
    source_path: str,
    evidence_tiers: list[str],
    precondition_tier: str | None = None,
) -> str:
    """Deterministic tier assignment with min-rule enforcement.

    Returns the effective tier. Raises P0Incident if the active P0 policy
    is HALT and a silent promotion is detected.
    """
    own_claim = _determine_own_claim(packet_type, source_path)

    input_floor = tier_min_many(evidence_tiers) if evidence_tiers else own_claim
    prec_floor = precondition_tier if precondition_tier else own_claim

    effective = tier_min_many([own_claim, input_floor, prec_floor])

    # Detect silent promotion — any promotion across a boundary is P0
    if TIER_RANK.get(effective, 1) > TIER_RANK.get(input_floor, 1):
        gap = TIER_RANK.get(effective, 1) - TIER_RANK.get(input_floor, 1)
        msg = (
            f"Silent promotion detected: effective={effective} > "
            f"input_floor={input_floor} for packet_type={packet_type}, "
            f"source_path={source_path}"
        )
        log.error("P0 TIER VIOLATION: %s", msg)
        if ACTIVE_P0_POLICY == P0Policy.HALT:
            raise P0Incident(msg, gap=gap)

    return effective


def _determine_own_claim(packet_type: str, source_path: str) -> str:
    """Determine the tier a packet claims based on type and source."""
    path_lower = source_path.lower() if source_path else ""

    # Conversations and raw threads are always INTUITED
    if packet_type == "conversation":
        return TIER_INTUITED
    if "thread" in path_lower or "transcript" in path_lower:
        return TIER_INTUITED
    if "chat" in path_lower or "slack" in path_lower:
        return TIER_INTUITED

    # Doctrine with explicit rules can be STRUCTURED
    if packet_type == "doctrine":
        if "authority" in path_lower or "principle" in path_lower:
            return TIER_STRUCTURED
        return TIER_INTUITED

    # Methods with formal process docs are STRUCTURED
    if packet_type == "method":
        if "sop" in path_lower or "process" in path_lower:
            return TIER_STRUCTURED
        return TIER_INTUITED

    # Decisions are STRUCTURED if from authority, else INTUITED
    if packet_type == "decision":
        if "authority" in path_lower or "decision_log" in path_lower:
            return TIER_STRUCTURED
        return TIER_INTUITED

    # Working models are INTUITED by default — need evidence to promote
    if packet_type == "working_model":
        return TIER_INTUITED

    # Pipeline metrics with counted samples are MEASURED
    if packet_type == "reference":
        if "metric" in path_lower or "benchmark" in path_lower:
            return TIER_MEASURED
        return TIER_INTUITED

    # Conservative default
    return TIER_INTUITED


async def assign_epistemic_tiers(run_id: str) -> dict[str, Any]:
    """Assign epistemic tiers to all draft packets.

    For each packet, determines the own-claim tier from packet type
    and source path, collects evidence chunk tiers, and applies the
    min-rule.
    """
    conn = await connect_writer()
    try:
        await start_curation_run(
            conn, run_id=run_id, stage="epistemic_tier", code_version=CODE_VERSION
        )

        packets = await conn.fetch(
            """
            SELECT bp.packet_id, bp.packet_type, bp.metadata,
                   bd.source_path
            FROM brain_packets bp
            LEFT JOIN brain_documents bd ON bd.document_id = bp.source_document_id
            WHERE bp.status = 'draft' AND bp.epistemic_tier IS NULL
            """
        )

        assigned = 0
        p0_violations = 0
        tier_counts: dict[str, int] = {}

        for packet in packets:
            packet_id = packet["packet_id"]
            packet_type = packet["packet_type"]
            meta = packet["metadata"] or {}
            if isinstance(meta, str):
                try:
                    meta = json.loads(meta)
                except (json.JSONDecodeError, TypeError):
                    meta = {}
            source_path = packet["source_path"] or meta.get("source_path", "")

            # Collect evidence chunk metadata for tier inference
            evidence_rows = await conn.fetch(
                """
                SELECT kv.metadata
                FROM brain_packet_evidence bpe
                JOIN knowledge_vectors kv ON kv.id = bpe.chunk_id
                WHERE bpe.packet_id = $1
                """,
                packet_id,
            )

            evidence_tiers: list[str] = []
            for erow in evidence_rows:
                emeta = erow["metadata"] or {}
                if isinstance(emeta, str):
                    try:
                        emeta = json.loads(emeta)
                    except (json.JSONDecodeError, TypeError):
                        emeta = {}
                chunk_tier = emeta.get("epistemic_tier", TIER_INTUITED)
                if chunk_tier not in TIER_RANK:
                    chunk_tier = TIER_INTUITED
                evidence_tiers.append(chunk_tier)

            try:
                effective_tier = assign_tier_for_packet(
                    packet_type, source_path, evidence_tiers
                )
            except P0Incident:
                p0_violations += 1
                effective_tier = TIER_INTUITED

            await conn.execute(
                """UPDATE brain_packets
                SET epistemic_tier = $2, updated_at = now()
                WHERE packet_id = $1""",
                packet_id,
                effective_tier,
            )
            assigned += 1
            tier_counts[effective_tier] = tier_counts.get(effective_tier, 0) + 1

        metrics = {
            "packets_assigned": assigned,
            "tier_distribution": tier_counts,
            "p0_violations": p0_violations,
        }
        await complete_curation_run(conn, run_id, status="completed", metrics=metrics)
        log.info("Epistemic tier assignment complete: %s", metrics)
        return metrics

    except Exception as e:
        await complete_curation_run(conn, run_id, status="failed", error=str(e))
        raise
    finally:
        await conn.close()

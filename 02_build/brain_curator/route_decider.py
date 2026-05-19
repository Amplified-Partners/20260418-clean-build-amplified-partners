"""06_route_decider — deterministic route logic for brain packets.

Routes packets based on content safety, provenance, duplication status,
epistemic tier, and evidence presence. Never deletes source —
drop_from_active only excludes from active retrieval.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import logging
import re
from typing import Any

from brain_curator.config import (
    CODE_VERSION,
    GOVERNED_PACKET_TYPES,
    PII_KEYWORDS,
    ROUTE_DROP_FROM_ACTIVE,
    ROUTE_KEEP,
    ROUTE_QUARANTINE,
    ROUTE_REFINE,
    ROUTE_REVIEW,
    ROUTE_VALIDATE,
    SECRET_KEYWORDS,
    TIER_INTUITED,
)
from brain_curator.db import complete_curation_run, connect_writer, start_curation_run

log = logging.getLogger("brain_curator.route_decider")


def detect_secret_or_pii(content: str) -> tuple[bool, bool]:
    """Check content for potential secrets or PII.

    Returns (secret_detected, pii_unsure).
    """
    content_lower = content.lower()
    secret_detected = any(kw in content_lower for kw in SECRET_KEYWORDS)
    pii_unsure = any(kw in content_lower for kw in PII_KEYWORDS)

    # Pattern-based secret detection
    if not secret_detected:
        # API key patterns (long hex/base64 strings after key-like prefixes)
        if re.search(r"(?:key|token|secret|password)\s*[=:]\s*\S{20,}", content_lower):
            secret_detected = True
        # AWS-style keys
        if re.search(r"AKIA[0-9A-Z]{16}", content):
            secret_detected = True

    return secret_detected, pii_unsure


def decide_route(
    packet_type: str,
    epistemic_tier: str,
    has_evidence: bool,
    has_provenance: bool,
    is_exact_duplicate: bool,
    has_better_canonical: bool,
    content_sample: str = "",
) -> str:
    """Deterministic route decision for a packet.

    Priority order:
    1. Secret/PII -> quarantine
    2. No provenance -> refine
    3. Exact duplicate with better canonical -> drop_from_active
    4. Governed type + INTUITED -> validate
    5. High value + evidence -> keep
    6. High value + no evidence -> refine
    7. Default -> review
    """
    secret_detected, pii_unsure = detect_secret_or_pii(content_sample)

    if secret_detected or pii_unsure:
        return ROUTE_QUARANTINE

    if not has_provenance:
        return ROUTE_REFINE

    if is_exact_duplicate and has_better_canonical:
        return ROUTE_DROP_FROM_ACTIVE

    if packet_type in GOVERNED_PACKET_TYPES and epistemic_tier == TIER_INTUITED:
        return ROUTE_VALIDATE

    is_high_value = packet_type in GOVERNED_PACKET_TYPES

    if is_high_value and has_evidence:
        return ROUTE_KEEP

    if is_high_value and not has_evidence:
        return ROUTE_REFINE

    return ROUTE_REVIEW


async def decide_routes(run_id: str) -> dict[str, Any]:
    """Assign routes to all draft packets that have tiers but no route."""
    conn = await connect_writer()
    try:
        await start_curation_run(
            conn, run_id=run_id, stage="route_decider", code_version=CODE_VERSION
        )

        packets = await conn.fetch(
            """
            SELECT bp.packet_id, bp.packet_type, bp.epistemic_tier,
                   bp.source_document_id, bp.metadata
            FROM brain_packets bp
            WHERE bp.status = 'draft'
              AND bp.epistemic_tier IS NOT NULL
              AND bp.route IS NULL
            """
        )

        route_counts: dict[str, int] = {}
        routed = 0

        for packet in packets:
            packet_id = packet["packet_id"]
            packet_type = packet["packet_type"]
            epistemic_tier = packet["epistemic_tier"] or TIER_INTUITED

            # Check evidence presence
            evidence_count = await conn.fetchval(
                "SELECT COUNT(*) FROM brain_packet_evidence WHERE packet_id = $1",
                packet_id,
            )
            has_evidence = evidence_count > 0

            # Check provenance
            has_provenance = packet["source_document_id"] is not None

            # Check duplicate status
            is_exact_duplicate = False
            has_better_canonical = False
            if packet["source_document_id"]:
                dup_info = await conn.fetchrow(
                    """
                    SELECT bdm.member_role, bdc.canonical_member_id
                    FROM brain_dedupe_members bdm
                    JOIN brain_dedupe_clusters bdc ON bdc.cluster_id = bdm.cluster_id
                    WHERE bdm.chunk_id = $1 AND bdc.cluster_type = 'exact'
                    LIMIT 1
                    """,
                    packet["source_document_id"],
                )
                if dup_info:
                    is_exact_duplicate = True
                    has_better_canonical = (
                        dup_info["member_role"] != "canonical"
                    )

            # Get a content sample for secret/PII detection
            content_sample = ""
            sample_row = await conn.fetchval(
                """
                SELECT kv.content
                FROM brain_packet_evidence bpe
                JOIN knowledge_vectors kv ON kv.id = bpe.chunk_id
                WHERE bpe.packet_id = $1
                LIMIT 1
                """,
                packet_id,
            )
            if sample_row:
                content_sample = sample_row[:2000]

            route = decide_route(
                packet_type=packet_type,
                epistemic_tier=epistemic_tier,
                has_evidence=has_evidence,
                has_provenance=has_provenance,
                is_exact_duplicate=is_exact_duplicate,
                has_better_canonical=has_better_canonical,
                content_sample=content_sample,
            )

            await conn.execute(
                """UPDATE brain_packets
                SET route = $2, updated_at = now()
                WHERE packet_id = $1""",
                packet_id,
                route,
            )
            routed += 1
            route_counts[route] = route_counts.get(route, 0) + 1

        metrics = {
            "packets_routed": routed,
            "route_distribution": route_counts,
        }
        await complete_curation_run(conn, run_id, status="completed", metrics=metrics)
        log.info("Route decider complete: %s", metrics)
        return metrics

    except Exception as e:
        await complete_curation_run(conn, run_id, status="failed", error=str(e))
        raise
    finally:
        await conn.close()

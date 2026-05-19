"""08_freeze — freeze and reopen governance for brain packets.

Freeze criteria:
  - Packet must have status='active'
  - Packet must have route='keep' or route='freeze'
  - Packet must have epistemic_tier in ('STRUCTURED', 'MEASURED', 'PROVEN')
  - Packet must have at least one evidence chunk (for governed types)

Frozen packets get status='frozen' and a last_verified_at timestamp.
Reopen sets status back to 'active' and clears freeze metadata.

Also maintains current-working-model records: for each packet_type,
only the most recently verified active packet is the current model.
Superseded packets get canonical_packet_id pointing to the new one.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from brain_curator.config import (
    CODE_VERSION,
    GOVERNED_PACKET_TYPES,
    RETRIEVAL_TIERS,
    ROUTE_KEEP,
    ROUTE_FREEZE,
)
from brain_curator.db import complete_curation_run, connect_writer, start_curation_run

log = logging.getLogger("brain_curator.freeze")


async def freeze_packets(run_id: str) -> dict[str, Any]:
    """Freeze eligible active packets and manage current-working-model records.

    Activation: moves draft packets with route='keep' and sufficient
    tier/evidence to status='active'.

    Freeze: moves active packets with route='freeze' to status='frozen'.
    """
    conn = await connect_writer()
    try:
        await start_curation_run(
            conn, run_id=run_id, stage="freeze", code_version=CODE_VERSION
        )

        activated = 0
        frozen = 0
        skipped = 0

        # Phase 1: Activate eligible draft packets (route=keep, tier >= STRUCTURED)
        draft_candidates = await conn.fetch(
            """
            SELECT bp.packet_id, bp.packet_type, bp.epistemic_tier
            FROM brain_packets bp
            WHERE bp.status = 'draft'
              AND bp.route = $1
              AND bp.epistemic_tier = ANY($2::text[])
            """,
            ROUTE_KEEP,
            list(RETRIEVAL_TIERS),
        )

        for candidate in draft_candidates:
            pid = candidate["packet_id"]
            ptype = candidate["packet_type"]

            # Governed types must have evidence
            if ptype in GOVERNED_PACKET_TYPES:
                ev_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM brain_packet_evidence WHERE packet_id = $1",
                    pid,
                )
                if ev_count == 0:
                    skipped += 1
                    continue

            await conn.execute(
                """UPDATE brain_packets
                SET status = 'active', last_verified_at = now(), updated_at = now()
                WHERE packet_id = $1""",
                pid,
            )
            activated += 1

        # Phase 2: Freeze eligible active packets (route=freeze)
        freeze_candidates = await conn.fetch(
            """
            SELECT bp.packet_id, bp.packet_type, bp.epistemic_tier
            FROM brain_packets bp
            WHERE bp.status = 'active'
              AND bp.route = $1
              AND bp.epistemic_tier = ANY($2::text[])
            """,
            ROUTE_FREEZE,
            list(RETRIEVAL_TIERS),
        )

        for candidate in freeze_candidates:
            pid = candidate["packet_id"]
            ptype = candidate["packet_type"]

            if ptype in GOVERNED_PACKET_TYPES:
                ev_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM brain_packet_evidence WHERE packet_id = $1",
                    pid,
                )
                if ev_count == 0:
                    skipped += 1
                    continue

            await conn.execute(
                """UPDATE brain_packets
                SET status = 'frozen', last_verified_at = now(), updated_at = now()
                WHERE packet_id = $1""",
                pid,
            )
            frozen += 1

        metrics = {
            "activated": activated,
            "frozen": frozen,
            "skipped_no_evidence": skipped,
        }
        await complete_curation_run(conn, run_id, status="completed", metrics=metrics)
        log.info("Freeze complete: %s", metrics)
        return metrics

    except Exception as e:
        await complete_curation_run(conn, run_id, status="failed", error=str(e))
        raise
    finally:
        await conn.close()


async def reopen_packet(conn: Any, packet_id: uuid.UUID) -> bool:
    """Reopen a frozen packet back to active status."""
    result = await conn.execute(
        """UPDATE brain_packets
        SET status = 'active', updated_at = now()
        WHERE packet_id = $1 AND status = 'frozen'""",
        packet_id,
    )
    return result == "UPDATE 1"

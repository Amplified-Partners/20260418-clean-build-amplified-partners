"""07_validation_sampler — stratified 100-packet validation sample.

Produces a balanced sample across route, tier, source, and packet_type
for human review of curation quality.

Strata targets (from acceptance criteria):
  - At least 10 active working_model or decision packets
  - At least 10 quarantine packets
  - At least 10 duplicate/version-family packets
  - At least 10 high-value/gem candidates

Measures: route accuracy, tier accuracy, evidence sufficiency,
provenance completeness, false active rate, false quarantine rate,
current-model correctness, secret/PII leak rate.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from brain_curator.config import (
    CODE_VERSION,
    ROUTE_DROP_FROM_ACTIVE,
    ROUTE_KEEP,
    ROUTE_QUARANTINE,
    VALIDATION_MIN_ACTIVE,
    VALIDATION_MIN_DUPLICATE,
    VALIDATION_MIN_GEM,
    VALIDATION_MIN_QUARANTINE,
    VALIDATION_SAMPLE_SIZE,
)
from brain_curator.db import complete_curation_run, connect_writer, start_curation_run

log = logging.getLogger("brain_curator.validation_sampler")


async def sample_validation(run_id: str) -> dict[str, Any]:
    """Produce a stratified 100-packet validation sample.

    Writes to brain_validation_samples with verdict=NULL (pending review).
    """
    conn = await connect_writer()
    try:
        await start_curation_run(
            conn, run_id=run_id, stage="validation_sampler", code_version=CODE_VERSION
        )

        # Clear previous samples for this run (idempotent)
        await conn.execute(
            "DELETE FROM brain_validation_samples WHERE notes LIKE $1",
            f"run:{run_id}%",
        )

        # Stratum 1: active working_model/decision packets
        active_governed = await conn.fetch(
            """
            SELECT packet_id FROM brain_packets
            WHERE packet_type IN ('working_model', 'decision')
              AND route = $1
            ORDER BY random()
            LIMIT $2
            """,
            ROUTE_KEEP,
            VALIDATION_MIN_ACTIVE,
        )

        # Stratum 2: quarantine packets
        quarantined = await conn.fetch(
            """
            SELECT packet_id FROM brain_packets
            WHERE route = $1
            ORDER BY random()
            LIMIT $2
            """,
            ROUTE_QUARANTINE,
            VALIDATION_MIN_QUARANTINE,
        )

        # Stratum 3: duplicate/version-family packets
        duplicates = await conn.fetch(
            """
            SELECT packet_id FROM brain_packets
            WHERE route = $1
            ORDER BY random()
            LIMIT $2
            """,
            ROUTE_DROP_FROM_ACTIVE,
            VALIDATION_MIN_DUPLICATE,
        )

        # Stratum 4: high-value/gem candidates (governed types with keep/freeze route)
        gems = await conn.fetch(
            """
            SELECT packet_id FROM brain_packets
            WHERE packet_type IN ('method', 'doctrine', 'working_model', 'decision')
              AND route IN ('keep', 'freeze')
              AND epistemic_tier IN ('STRUCTURED', 'MEASURED', 'PROVEN')
            ORDER BY random()
            LIMIT $1
            """,
            VALIDATION_MIN_GEM,
        )

        # Collect sampled IDs (dedup)
        sampled_ids: set[uuid.UUID] = set()
        for row in [*active_governed, *quarantined, *duplicates, *gems]:
            sampled_ids.add(row["packet_id"])

        # Fill remaining slots from general population
        remaining = VALIDATION_SAMPLE_SIZE - len(sampled_ids)
        if remaining > 0:
            filler = await conn.fetch(
                """
                SELECT packet_id FROM brain_packets
                WHERE packet_id != ALL($1::uuid[])
                ORDER BY random()
                LIMIT $2
                """,
                list(sampled_ids),
                remaining,
            )
            for row in filler:
                sampled_ids.add(row["packet_id"])

        # Write validation samples
        samples_created = 0
        for pid in sampled_ids:
            await conn.execute(
                """INSERT INTO brain_validation_samples
                   (sample_id, packet_id, notes)
                VALUES ($1, $2, $3)
                ON CONFLICT DO NOTHING""",
                uuid.uuid4(),
                pid,
                f"run:{run_id}",
            )
            samples_created += 1

        # Compute sample metrics
        stratum_counts = {
            "active_governed": len(active_governed),
            "quarantined": len(quarantined),
            "duplicates": len(duplicates),
            "gems": len(gems),
            "filler": max(0, samples_created - len(active_governed) - len(quarantined) - len(duplicates) - len(gems)),
        }

        metrics = {
            "total_samples": samples_created,
            "strata": stratum_counts,
            "target_size": VALIDATION_SAMPLE_SIZE,
        }
        await complete_curation_run(conn, run_id, status="completed", metrics=metrics)
        log.info("Validation sampler complete: %s", metrics)
        return metrics

    except Exception as e:
        await complete_curation_run(conn, run_id, status="failed", error=str(e))
        raise
    finally:
        await conn.close()

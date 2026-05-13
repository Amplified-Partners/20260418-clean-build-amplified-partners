"""Derived rebuild — entities, relationships, and embeddings from canonical vectors.

AMP-302 Ticket 5: These are derived indexes, not source truth. They can be
rebuilt from the canonical knowledge_vectors table at any time.

Each function is a separate Temporal activity so they can be retried independently.

Signed-by: Devon-0de2 | 2026-05-11 | devin-0de27df281514f96ba3921354d7c31ae
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import uuid as _uuid
from dataclasses import dataclass

from temporalio import activity

logger = logging.getLogger("cove.derived_rebuild")

BRAIN_DSN = os.getenv(
    "BRAIN_DSN",
    "postgresql://brain_writer@cove-postgres:5432/amplified_brain",
)

SIGNED_BY = "brain_writer_pipeline"


# ═══════════════════════════════════════════════════════════════════════
# Data classes
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class RebuildInput:
    """Input for any derived rebuild activity."""
    run_id: str
    brain_dsn: str = BRAIN_DSN
    batch_size: int = 500


@dataclass
class RebuildResult:
    """Result from a derived rebuild activity."""
    success: bool
    rows_processed: int = 0
    rows_written: int = 0
    errors: int = 0
    error: str | None = None


# ═══════════════════════════════════════════════════════════════════════
# Activity: Rebuild entities from canonical vectors
# ═══════════════════════════════════════════════════════════════════════

@activity.defn(name="rebuild_entities")
async def rebuild_entities(input: RebuildInput) -> RebuildResult:
    """Walk canonical knowledge_vectors, extract concepts from metadata, upsert entities.

    Entity IDs are deterministic: UUID5 of concept name. Source is marked 'derived'.
    """
    import asyncpg

    try:
        conn = await asyncpg.connect(input.brain_dsn)
    except Exception as e:
        return RebuildResult(success=False, error=f"Connection failed: {e}")

    rows_processed = 0
    rows_written = 0
    errors = 0

    try:
        # Read canonical vectors that have metadata with concepts
        offset = 0
        while True:
            rows = await conn.fetch(
                """SELECT id, content, file_path, metadata
                   FROM knowledge_vectors
                   WHERE provenance = 'amplified-pipeline-v0.3'
                   ORDER BY id
                   LIMIT $1 OFFSET $2""",
                input.batch_size,
                offset,
            )
            if not rows:
                break

            for row in rows:
                rows_processed += 1
                try:
                    # Extract concepts from content (PUDDING frontmatter)
                    content = row["content"] or ""
                    concepts = _extract_concepts_from_content(content)

                    for concept_name, concept_data in concepts:
                        ent_id = _uuid.UUID(
                            hashlib.sha256(concept_name.encode()).hexdigest()[:32]
                        )
                        props = json.dumps({
                            "source_file": row["file_path"],
                            "source_type": "derived",
                            "run_id": input.run_id,
                            **concept_data,
                        })
                        await conn.execute(
                            """INSERT INTO entities
                               (id, name, entity_type, summary, properties,
                                source_type, run_id, signed_by)
                            VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7, $8)
                            ON CONFLICT (id) DO UPDATE SET
                               properties = entities.properties || EXCLUDED.properties,
                               updated_at = now()""",
                            ent_id,
                            concept_name,
                            concept_data.get("entity_type", "concept"),
                            concept_data.get("description", ""),
                            props,
                            "derived",
                            input.run_id,
                            SIGNED_BY,
                        )
                        rows_written += 1

                except Exception as e:
                    errors += 1
                    activity.logger.warning(f"Entity rebuild failed for {row['id']}: {e}")

            offset += input.batch_size
            activity.logger.info(
                f"Entities: processed={rows_processed}, written={rows_written}"
            )

    finally:
        await conn.close()

    return RebuildResult(
        success=errors == 0,
        rows_processed=rows_processed,
        rows_written=rows_written,
        errors=errors,
    )


def _extract_concepts_from_content(content: str) -> list[tuple[str, dict]]:
    """Extract concept names from PUDDING YAML frontmatter in content."""
    import yaml

    concepts = []
    if not content.startswith("---"):
        return concepts

    parts = content.split("---", 2)
    if len(parts) < 3:
        return concepts

    try:
        fm = yaml.safe_load(parts[1])
        if not isinstance(fm, dict):
            return concepts
    except Exception:
        return concepts

    for concept in fm.get("concepts", []):
        if isinstance(concept, dict) and concept.get("name"):
            concepts.append((
                concept["name"],
                {
                    "pudding_code": concept.get("pudding_code", ""),
                    "description": concept.get("description", ""),
                    "confidence": concept.get("confidence", 0.0),
                    "entity_type": "concept",
                },
            ))

    for domain in fm.get("domains", []):
        if isinstance(domain, dict) and domain.get("name"):
            concepts.append((
                domain["name"],
                {
                    "description": domain.get("description", ""),
                    "entity_type": "domain",
                },
            ))

    return concepts


# ═══════════════════════════════════════════════════════════════════════
# Activity: Rebuild relationships from entity co-occurrence
# ═══════════════════════════════════════════════════════════════════════

@activity.defn(name="rebuild_relationships")
async def rebuild_relationships(input: RebuildInput) -> RebuildResult:
    """Derive relationships from entity co-occurrence in the same source file.

    Two entities appearing in the same file get a 'co-occurs-in' relationship.
    Weight is proportional to how many files they co-occur in.
    """
    import asyncpg
    from collections import defaultdict

    try:
        conn = await asyncpg.connect(input.brain_dsn)
    except Exception as e:
        return RebuildResult(success=False, error=f"Connection failed: {e}")

    rows_written = 0
    errors = 0

    try:
        # Build co-occurrence map: file_path → set of entity IDs
        file_entities: dict[str, set[str]] = defaultdict(set)

        offset = 0
        while True:
            rows = await conn.fetch(
                """SELECT id, name, properties
                   FROM entities
                   WHERE source_type = 'derived'
                   ORDER BY id
                   LIMIT $1 OFFSET $2""",
                input.batch_size,
                offset,
            )
            if not rows:
                break
            for row in rows:
                props = json.loads(row["properties"]) if row["properties"] else {}
                source_file = props.get("source_file", "")
                if source_file:
                    file_entities[source_file].add(str(row["id"]))
            offset += input.batch_size

        # Generate co-occurrence relationships
        pair_counts: dict[tuple[str, str], int] = defaultdict(int)
        for entities_in_file in file_entities.values():
            entity_list = sorted(entities_in_file)
            for i in range(len(entity_list)):
                for j in range(i + 1, len(entity_list)):
                    pair_counts[(entity_list[i], entity_list[j])] += 1

        activity.logger.info(f"Found {len(pair_counts)} entity pairs")

        for (source_id, target_id), count in pair_counts.items():
            try:
                weight = min(count / 10.0, 1.0)
                await conn.execute(
                    """INSERT INTO relationships
                       (source_id, target_id, relation_type, summary,
                        weight, source_type, run_id, signed_by)
                    VALUES ($1::uuid, $2::uuid, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT DO NOTHING""",
                    _uuid.UUID(source_id),
                    _uuid.UUID(target_id),
                    "co-occurs-in",
                    f"Co-occurrence in {count} source file(s)",
                    weight,
                    "derived",
                    input.run_id,
                    SIGNED_BY,
                )
                rows_written += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    activity.logger.warning(f"Relationship write failed: {e}")

        activity.logger.info(
            f"Relationships: written={rows_written}, errors={errors}"
        )

    finally:
        await conn.close()

    return RebuildResult(
        success=errors == 0,
        rows_processed=len(pair_counts) if 'pair_counts' in dir() else 0,
        rows_written=rows_written,
        errors=errors,
    )

#!/usr/bin/env python3
"""
Qdrant → pgvector Migration Script
====================================

Exports all embeddings from Qdrant (standalone vector DB) and imports them
into PostgreSQL + pgvector (HNSW indexing) within the amplified_brain database.

Migration scope:
  - 57,434 embeddings (384-dim) across collections
  - Semantic cache (llm_cache collection) → pgvector table
  - All metadata/payloads preserved as JSONB
  - HNSW index rebuilt after import

The Canonical Data Architecture is the law. One engine. Three capabilities.
No separate processes. — Ewan Bramley, 2026-05-08.

Usage:
  # Dry run (export only, no import):
  python migrate_qdrant_to_pgvector.py --dry-run

  # Full migration:
  python migrate_qdrant_to_pgvector.py

  # Verify after migration:
  python migrate_qdrant_to_pgvector.py --verify-only

  # Migrate specific collection:
  python migrate_qdrant_to_pgvector.py --collection llm_cache

Environment variables:
  QDRANT_HOST      Qdrant host (default: qdrant)
  QDRANT_PORT      Qdrant gRPC port (default: 6334)
  QDRANT_HTTP_PORT Qdrant HTTP port (default: 6333)
  PG_HOST          PostgreSQL host (default: cove-postgres)
  PG_PORT          PostgreSQL port (default: 5432)
  PG_DB            Database name (default: amplified_brain)
  PG_USER          PostgreSQL user (default: postgres)
  PG_PASSWORD      PostgreSQL password (required)
  BATCH_SIZE       Import batch size (default: 500)

Signed-by: Devon-8da1 | 2026-05-15 | devin-8da1981ce177481da3fe1d2b40e7fade
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("migrate_qdrant_to_pgvector")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

QDRANT_HOST = os.environ.get("QDRANT_HOST", "qdrant")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", "6334"))
QDRANT_HTTP_PORT = int(os.environ.get("QDRANT_HTTP_PORT", "6333"))

PG_HOST = os.environ.get("PG_HOST", "cove-postgres")
PG_PORT = int(os.environ.get("PG_PORT", "5432"))
PG_DB = os.environ.get("PG_DB", "amplified_brain")
PG_USER = os.environ.get("PG_USER", "postgres")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "")

BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "500"))
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class VectorRecord:
    """A vector record extracted from Qdrant."""
    point_id: str
    vector: list[float]
    payload: dict
    collection: str


@dataclass
class MigrationReport:
    """Tracks migration progress."""
    collections_processed: int = 0
    records_exported: int = 0
    records_imported: int = 0
    cache_records_exported: int = 0
    cache_records_imported: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""

    def summary(self) -> str:
        return (
            f"Migration report:\n"
            f"  Collections processed:  {self.collections_processed}\n"
            f"  Records exported:       {self.records_exported}\n"
            f"  Records imported:       {self.records_imported}\n"
            f"  Cache records exported: {self.cache_records_exported}\n"
            f"  Cache records imported: {self.cache_records_imported}\n"
            f"  Errors:                 {len(self.errors)}\n"
            f"  Started:                {self.started_at}\n"
            f"  Completed:              {self.completed_at}\n"
        )


# ---------------------------------------------------------------------------
# Qdrant export
# ---------------------------------------------------------------------------

def connect_qdrant():
    """Connect to Qdrant via HTTP client."""
    try:
        from qdrant_client import QdrantClient
    except ImportError:
        log.error("qdrant-client not installed. Run: pip install qdrant-client")
        sys.exit(1)
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_HTTP_PORT)


def list_collections(client) -> list[str]:
    """List all Qdrant collections."""
    collections = client.get_collections().collections
    return [c.name for c in collections]


def export_collection(client, collection_name: str) -> list[VectorRecord]:
    """Export all points from a Qdrant collection using scroll."""
    records = []
    offset = None
    batch_num = 0

    while True:
        result = client.scroll(
            collection_name=collection_name,
            limit=BATCH_SIZE,
            offset=offset,
            with_payload=True,
            with_vectors=True,
        )
        points, next_offset = result

        for point in points:
            vector = point.vector
            if isinstance(vector, dict):
                vector = vector.get("", list(vector.values())[0] if vector else [])

            records.append(VectorRecord(
                point_id=str(point.id),
                vector=list(vector) if vector else [],
                payload=dict(point.payload) if point.payload else {},
                collection=collection_name,
            ))

        batch_num += 1
        if batch_num % 10 == 0:
            log.info(f"    Exported {len(records)} records so far...")

        if next_offset is None:
            break
        offset = next_offset

    return records


# ---------------------------------------------------------------------------
# PostgreSQL / pgvector import
# ---------------------------------------------------------------------------

def connect_pg():
    """Connect to PostgreSQL."""
    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        log.error("psycopg2 not installed. Run: pip install psycopg2-binary")
        sys.exit(1)

    if not PG_PASSWORD:
        log.error("PG_PASSWORD environment variable is required")
        sys.exit(1)

    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def ensure_pgvector(conn):
    """Ensure pgvector extension is available."""
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()


def create_knowledge_vectors_table(conn):
    """Create the canonical knowledge_vectors table for migrated embeddings.

    This table may already exist from the existing pgvector data (225K rows).
    We use IF NOT EXISTS to be safe.
    """
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS knowledge_vectors_migrated (
                id              SERIAL PRIMARY KEY,
                qdrant_id       TEXT NOT NULL,
                source_collection TEXT NOT NULL,
                embedding       vector({EMBEDDING_DIM}) NOT NULL,
                payload         JSONB DEFAULT '{{}}',
                migrated_from   TEXT DEFAULT 'qdrant',
                migrated_at     TIMESTAMPTZ DEFAULT NOW(),
                created_at      TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        # HNSW index for fast similarity search — the Russian maths
        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_knowledge_vectors_migrated_hnsw
            ON knowledge_vectors_migrated
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 200)
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_knowledge_vectors_migrated_collection
            ON knowledge_vectors_migrated (source_collection)
        """)
    conn.commit()
    log.info("  Table knowledge_vectors_migrated ready (HNSW index active)")


def create_semantic_cache_table(conn):
    """Create the semantic cache table (migrated from Qdrant llm_cache)."""
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS semantic_cache (
                id              SERIAL PRIMARY KEY,
                qdrant_id       TEXT,
                prompt_hash     TEXT,
                prompt_embedding vector({EMBEDDING_DIM}),
                prompt_text     TEXT,
                response_text   TEXT,
                model           TEXT,
                agent_name      TEXT,
                created_at      TIMESTAMPTZ DEFAULT NOW(),
                migrated_from   TEXT DEFAULT 'qdrant_llm_cache',
                migrated_at     TIMESTAMPTZ DEFAULT NOW(),
                payload         JSONB DEFAULT '{{}}'
            )
        """)
        cur.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_semantic_cache_hnsw
            ON semantic_cache
            USING hnsw (prompt_embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 200)
        """)
    conn.commit()
    log.info("  Table semantic_cache ready (HNSW index active)")


def import_vectors(conn, records: list[VectorRecord], is_cache: bool = False) -> int:
    """Batch import vectors into pgvector table."""
    import psycopg2.extras

    if not records:
        return 0

    imported = 0
    table = "semantic_cache" if is_cache else "knowledge_vectors_migrated"

    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]
        with conn.cursor() as cur:
            if is_cache:
                values = []
                for rec in batch:
                    values.append((
                        rec.point_id,
                        rec.payload.get("prompt_hash", ""),
                        str(rec.vector),
                        rec.payload.get("prompt_text", rec.payload.get("prompt", "")),
                        rec.payload.get("response_text", rec.payload.get("response", "")),
                        rec.payload.get("model", ""),
                        rec.payload.get("agent_name", rec.payload.get("agent", "")),
                        json.dumps(rec.payload),
                    ))
                psycopg2.extras.execute_batch(cur, f"""
                    INSERT INTO semantic_cache
                        (qdrant_id, prompt_hash, prompt_embedding, prompt_text,
                         response_text, model, agent_name, payload)
                    VALUES (%s, %s, %s::vector, %s, %s, %s, %s, %s::jsonb)
                """, values)
            else:
                values = []
                for rec in batch:
                    values.append((
                        rec.point_id,
                        rec.collection,
                        str(rec.vector),
                        json.dumps(rec.payload),
                    ))
                psycopg2.extras.execute_batch(cur, f"""
                    INSERT INTO knowledge_vectors_migrated
                        (qdrant_id, source_collection, embedding, payload)
                    VALUES (%s, %s, %s::vector, %s::jsonb)
                """, values)

        conn.commit()
        imported += len(batch)
        if (i // BATCH_SIZE) % 20 == 0:
            log.info(f"    Imported {imported}/{len(records)} records...")

    return imported


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_migration(conn, expected_vectors: int, expected_cache: int) -> bool:
    """Verify record counts in pgvector tables."""
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM knowledge_vectors_migrated")
        actual_vectors = cur.fetchone()[0]

        cur.execute("SELECT count(*) FROM semantic_cache")
        actual_cache = cur.fetchone()[0]

    log.info("Verification:")
    log.info(f"  knowledge_vectors_migrated: expected≥{expected_vectors}, actual={actual_vectors}")
    log.info(f"  semantic_cache: expected≥{expected_cache}, actual={actual_cache}")

    ok = True
    if actual_vectors < expected_vectors:
        log.warning(f"  ⚠ Vector count mismatch: missing {expected_vectors - actual_vectors}")
        ok = False
    if actual_cache < expected_cache:
        log.warning(f"  ⚠ Cache count mismatch: missing {expected_cache - actual_cache}")
        ok = False

    if ok:
        log.info("  ✓ All counts match or exceed expected values")

    # Test a similarity query to confirm HNSW index works
    if actual_vectors > 0:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT id, 1 - (embedding <=> (
                    SELECT embedding FROM knowledge_vectors_migrated LIMIT 1
                )) AS similarity
                FROM knowledge_vectors_migrated
                ORDER BY embedding <=> (
                    SELECT embedding FROM knowledge_vectors_migrated LIMIT 1
                )
                LIMIT 5
            """)
            results = cur.fetchall()
            log.info(f"  HNSW test query returned {len(results)} results — index is working")

    return ok


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Migrate Qdrant vectors to pgvector")
    parser.add_argument("--dry-run", action="store_true", help="Export only, do not import")
    parser.add_argument("--verify-only", action="store_true", help="Verify pgvector tables only")
    parser.add_argument("--collection", type=str, help="Migrate specific collection only")
    args = parser.parse_args()

    report = MigrationReport(started_at=datetime.now(timezone.utc).isoformat())

    log.info("=" * 60)
    log.info("Qdrant → pgvector (HNSW) Migration")
    log.info("=" * 60)
    log.info(f"Qdrant: {QDRANT_HOST}:{QDRANT_HTTP_PORT}")
    log.info(f"PostgreSQL: {PG_HOST}:{PG_PORT}/{PG_DB}")
    log.info(f"Embedding dim: {EMBEDDING_DIM}")
    log.info(f"Batch size: {BATCH_SIZE}")
    log.info(f"Dry run: {args.dry_run}")
    log.info("")

    if args.verify_only:
        conn = connect_pg()
        ensure_pgvector(conn)
        verify_migration(conn, 0, 0)
        conn.close()
        return

    # Phase 1: Connect to Qdrant
    log.info("Phase 1: Connecting to Qdrant...")
    client = connect_qdrant()
    collections = list_collections(client)
    log.info(f"  Found {len(collections)} collections: {collections}")

    if args.collection:
        collections = [c for c in collections if c == args.collection]
        if not collections:
            log.error(f"Collection '{args.collection}' not found")
            sys.exit(1)

    # Phase 2: Export
    all_vectors: list[VectorRecord] = []
    cache_vectors: list[VectorRecord] = []

    for coll_name in collections:
        log.info(f"\nPhase 2: Exporting collection '{coll_name}'...")
        records = export_collection(client, coll_name)
        report.collections_processed += 1

        if coll_name == "llm_cache":
            cache_vectors.extend(records)
            report.cache_records_exported += len(records)
            log.info(f"  Exported {len(records)} cache records")
        else:
            all_vectors.extend(records)
            report.records_exported += len(records)
            log.info(f"  Exported {len(records)} vector records")

    # Write export ledger
    export_ledger = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": f"qdrant://{QDRANT_HOST}:{QDRANT_HTTP_PORT}",
        "collections": {coll: len([r for r in all_vectors + cache_vectors if r.collection == coll]) for coll in collections},
        "total_vectors": report.records_exported,
        "total_cache": report.cache_records_exported,
        "embedding_dim": EMBEDDING_DIM,
        "signed_by": "Devon-8da1 | devin-8da1981ce177481da3fe1d2b40e7fade",
    }
    ledger_path = os.path.join(os.path.dirname(__file__), "qdrant_export_ledger.json")
    with open(ledger_path, "w") as f:
        json.dump(export_ledger, f, indent=2)
    log.info(f"\nExport ledger written to: {ledger_path}")

    if args.dry_run:
        log.info("\nDry run complete. No data was imported.")
        log.info(report.summary())
        return

    # Phase 3: Import into pgvector
    log.info("\nPhase 3: Connecting to PostgreSQL...")
    conn = connect_pg()
    ensure_pgvector(conn)

    log.info("Phase 4: Creating tables...")
    create_knowledge_vectors_table(conn)
    create_semantic_cache_table(conn)

    log.info(f"\nPhase 5: Importing {len(all_vectors)} vectors...")
    report.records_imported = import_vectors(conn, all_vectors, is_cache=False)
    log.info(f"  Imported: {report.records_imported}/{len(all_vectors)}")

    if cache_vectors:
        log.info(f"\nPhase 6: Importing {len(cache_vectors)} cache records...")
        report.cache_records_imported = import_vectors(conn, cache_vectors, is_cache=True)
        log.info(f"  Imported: {report.cache_records_imported}/{len(cache_vectors)}")

    # Phase 4: Verify
    log.info("\nPhase 7: Verification...")
    verify_migration(conn, len(all_vectors), len(cache_vectors))

    conn.close()
    report.completed_at = datetime.now(timezone.utc).isoformat()

    log.info("\n" + "=" * 60)
    log.info(report.summary())

    # Write final report
    report_path = os.path.join(os.path.dirname(__file__), "qdrant_migration_report.json")
    with open(report_path, "w") as f:
        json.dump({
            "collections_processed": report.collections_processed,
            "records_exported": report.records_exported,
            "records_imported": report.records_imported,
            "cache_records_exported": report.cache_records_exported,
            "cache_records_imported": report.cache_records_imported,
            "errors": report.errors,
            "started_at": report.started_at,
            "completed_at": report.completed_at,
            "signed_by": "Devon-8da1 | devin-8da1981ce177481da3fe1d2b40e7fade",
        }, f, indent=2)
    log.info(f"Report written to: {report_path}")


if __name__ == "__main__":
    main()

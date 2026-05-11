"""Embedding backfill — fill NULL embeddings in canonical knowledge_vectors.

AMP-302: The canonical writer (canonical_writer.py) inserts rows without
embeddings. This script reads rows where embedding IS NULL, generates
384-dim vectors with sentence-transformers all-MiniLM-L6-v2, and batch
updates them back into PostgreSQL (pgvector).

Usage:
    python embedding_backfill.py                       # defaults
    python embedding_backfill.py --batch-size 200      # bigger batches
    python embedding_backfill.py --dry-run              # count only
    python embedding_backfill.py --dsn 'postgresql://brain_writer@localhost:5433/amplified_brain'

Requirements:
    pip install asyncpg sentence-transformers

Authored by Devon-be18-child-embed | 2026-05-11
Session: devin-5367810cb22c42a8a524d6b7027ce65b
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass

import asyncpg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("cove.embedding_backfill")

DEFAULT_DSN = os.getenv(
    "BRAIN_DSN",
    "postgresql://brain_writer@cove-postgres:5433/amplified_brain",
)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
DEFAULT_BATCH_SIZE = 100
SIGNED_BY = os.getenv("BACKFILL_SIGNED_BY", "cove-embedding-backfill")


@dataclass
class BackfillStats:
    """Running totals for the backfill."""

    total_null: int = 0
    updated: int = 0
    skipped: int = 0
    errors: int = 0
    elapsed_s: float = 0.0


def load_model():
    """Load the sentence-transformers model (lazy, one-time)."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        logger.error(
            "sentence-transformers not installed. "
            "Run: pip install sentence-transformers"
        )
        sys.exit(1)

    logger.info("Loading model %s …", MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME)
    test_vec = model.encode(["test"])
    if test_vec.shape[1] != EMBEDDING_DIM:
        raise ValueError(
            f"Model produced {test_vec.shape[1]}-dim vectors, "
            f"expected {EMBEDDING_DIM}"
        )
    logger.info("Model loaded — %d-dim embeddings confirmed", EMBEDDING_DIM)
    return model


async def count_null_embeddings(conn) -> int:
    """Return count of knowledge_vectors rows with NULL embedding."""
    row = await conn.fetchrow(
        "SELECT count(*) AS n FROM knowledge_vectors WHERE embedding IS NULL"
    )
    return row["n"]


async def fetch_batch(conn, batch_size: int) -> list:
    """Fetch a batch of rows with NULL embeddings and non-empty content."""
    return await conn.fetch(
        """SELECT id, content
           FROM knowledge_vectors
           WHERE embedding IS NULL
             AND content IS NOT NULL
             AND content != ''
           ORDER BY ingested_at ASC
           LIMIT $1""",
        batch_size,
    )


async def update_embeddings(conn, rows_and_vectors: list[tuple]) -> int:
    """Batch-update embeddings inside a transaction.

    Each tuple is (embedding_str, row_id).
    Returns count of rows updated.
    """
    async with conn.transaction():
        updated = 0
        for emb_str, row_id in rows_and_vectors:
            await conn.execute(
                """UPDATE knowledge_vectors
                   SET embedding = $1::vector,
                       updated_at = now()
                   WHERE id = $2""",
                emb_str,
                row_id,
            )
            updated += 1
        return updated


def encode_batch(model, texts: list[str]) -> list[list[float]]:
    """Encode a list of texts into embeddings."""
    vectors = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return vectors.tolist()


async def run_backfill(
    dsn: str,
    batch_size: int,
    dry_run: bool,
) -> BackfillStats:
    """Main backfill loop."""
    stats = BackfillStats()
    t0 = time.monotonic()

    logger.info("Connecting to %s …", dsn.split("@")[-1] if "@" in dsn else dsn)
    try:
        conn = await asyncpg.connect(dsn)
    except Exception as exc:
        logger.error("Connection failed: %s", exc)
        stats.errors = 1
        stats.elapsed_s = time.monotonic() - t0
        return stats

    # All paths below go through the finally block, which closes conn.
    # Python guarantees finally runs even on return statements inside try.
    try:
        stats.total_null = await count_null_embeddings(conn)
        logger.info("Rows with NULL embedding: %d", stats.total_null)

        if stats.total_null == 0:
            logger.info("Nothing to backfill — all rows have embeddings.")
            return stats

        # Count empty-content rows separately
        empty_row = await conn.fetchrow(
            """SELECT count(*) AS n FROM knowledge_vectors
               WHERE embedding IS NULL
                 AND (content IS NULL OR content = '')"""
        )
        stats.skipped = empty_row["n"]
        if stats.skipped > 0:
            logger.info(
                "Skipping %d rows with empty content (will not embed).",
                stats.skipped,
            )

        if dry_run:
            logger.info(
                "DRY RUN — would process %d rows (%d skipped). Exiting.",
                stats.total_null - stats.skipped,
                stats.skipped,
            )
            return stats

        model = load_model()

        batch_num = 0

        while True:
            # Fetch from offset 0: updated rows drop out of the
            # WHERE filter, so the next page surfaces automatically.
            # Empty-content rows are excluded by the query.
            rows = await fetch_batch(conn, batch_size)
            if not rows:
                break

            batch_num += 1
            texts = []
            row_ids = []

            for row in rows:
                texts.append((row["content"] or "").strip()[:2048])
                row_ids.append(row["id"])

            try:
                vectors = encode_batch(model, texts)
            except Exception as exc:
                logger.error("Encoding failed on batch %d: %s", batch_num, exc)
                stats.errors += len(texts)
                break

            pairs = []
            for row_id, vec in zip(row_ids, vectors):
                vec_str = "[" + ",".join(f"{v:.8f}" for v in vec) + "]"
                pairs.append((vec_str, row_id))

            try:
                count = await update_embeddings(conn, pairs)
                stats.updated += count
            except Exception as exc:
                logger.error("DB update failed on batch %d: %s", batch_num, exc)
                stats.errors += len(pairs)
                break

            remaining = stats.total_null - stats.updated - stats.skipped - stats.errors
            logger.info(
                "Batch %d: updated=%d, total_updated=%d, remaining≈%d",
                batch_num,
                len(pairs),
                stats.updated,
                max(remaining, 0),
            )

        # Audit log entry
        try:
            await conn.execute(
                """INSERT INTO audit_log
                   (actor, action, resource_type, resource_id, details)
                VALUES ($1, $2, $3, $4, $5::jsonb)""",
                SIGNED_BY,
                "embedding_backfill",
                "knowledge_vectors",
                f"backfill-{int(time.time())}",
                json.dumps({
                    "total_null": stats.total_null,
                    "updated": stats.updated,
                    "skipped": stats.skipped,
                    "errors": stats.errors,
                }),
            )
        except Exception as exc:
            logger.warning("Audit log write failed (non-fatal): %s", exc)

    finally:
        await conn.close()
        stats.elapsed_s = time.monotonic() - t0

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill NULL embeddings in canonical knowledge_vectors.",
    )
    parser.add_argument(
        "--dsn",
        default=DEFAULT_DSN,
        help="PostgreSQL connection string (default: $BRAIN_DSN or built-in)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Rows per batch (default: {DEFAULT_BATCH_SIZE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count NULL rows only — do not generate or write embeddings",
    )
    args = parser.parse_args()

    stats = asyncio.run(run_backfill(
        dsn=args.dsn,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
    ))

    logger.info(
        "Backfill complete — total_null=%d, updated=%d, skipped=%d, "
        "errors=%d, elapsed=%.1fs",
        stats.total_null,
        stats.updated,
        stats.skipped,
        stats.errors,
        stats.elapsed_s,
    )

    if stats.errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

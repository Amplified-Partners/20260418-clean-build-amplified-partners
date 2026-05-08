#!/usr/bin/env python3
"""
Migrate Qdrant amplified_knowledge collection → Postgres knowledge_vectors table.
Devon-a704 | 2026-05-07 | Amplified Brain migration

Runs ON Beast inside a container with access to both Qdrant (port 6333) and Postgres.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

# ── Config ──
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION = "amplified_knowledge"
BATCH_SIZE = 500  # points per scroll request
PG_BATCH = 100    # rows per INSERT

DB_HOST = os.environ.get("DB_HOST", "cove-postgres")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "amplified_brain")
DB_USER = os.environ.get("DB_USER", "brain_writer")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")  # Set via env var — never commit


def qdrant_post(path, data=None):
    url = f"{QDRANT_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def scroll_all():
    """Generator yielding all points from the collection."""
    offset = None
    total = 0
    while True:
        payload = {
            "limit": BATCH_SIZE,
            "with_payload": True,
            "with_vector": True,
        }
        if offset:
            payload["offset"] = offset

        result = qdrant_post(f"/collections/{COLLECTION}/points/scroll", payload)
        points = result["result"]["points"]
        if not points:
            break
        total += len(points)
        yield from points
        offset = result["result"].get("next_page_offset")
        if not offset:
            break
        print(f"  scrolled {total} points...", flush=True)


def build_insert_sql(points):
    """Build a multi-row INSERT statement."""
    values = []
    for pt in points:
        pid = pt["id"]
        p = pt["payload"]
        vec = pt["vector"]

        content = (p.get("text") or "").replace("'", "''")
        source = (p.get("file_path") or "").replace("'", "''")
        source_type = (p.get("category") or "qdrant_migration").replace("'", "''")

        meta = {
            "original_id": pid,
            "filename": p.get("filename"),
            "extension": p.get("extension"),
            "vertical": p.get("vertical"),
            "chunk_index": p.get("chunk_index"),
            "total_chunks": p.get("total_chunks"),
            "qdrant_collection": COLLECTION,
        }
        meta_json = json.dumps(meta).replace("'", "''")
        vec_str = "[" + ",".join(str(v) for v in vec) + "]"

        values.append(
            f"('{pid}', '{content}', '{vec_str}'::vector, '{source}', "
            f"'{source_type}', '{meta_json}'::jsonb, now(), now())"
        )

    cols = "id, content, embedding, source, source_type, metadata, created_at, updated_at"
    return f"INSERT INTO knowledge_vectors ({cols}) VALUES\n" + ",\n".join(values) + "\nON CONFLICT (id) DO NOTHING;"


def main():
    print(f"Starting Qdrant → Postgres migration for '{COLLECTION}'")
    start = time.time()

    # Get collection info
    info = qdrant_post(f"/collections/{COLLECTION}")
    total_points = info["result"]["points_count"]
    print(f"Collection has {total_points} points (384-dim, Cosine)")

    # Scroll and batch-insert
    batch = []
    migrated = 0
    sql_statements = []

    for pt in scroll_all():
        batch.append(pt)
        if len(batch) >= PG_BATCH:
            sql = build_insert_sql(batch)
            sql_statements.append(sql)
            migrated += len(batch)
            batch = []
            if migrated % 5000 == 0:
                print(f"  prepared {migrated}/{total_points} ({100*migrated/total_points:.1f}%)", flush=True)

    if batch:
        sql = build_insert_sql(batch)
        sql_statements.append(sql)
        migrated += len(batch)

    print(f"\nPrepared {migrated} rows in {len(sql_statements)} batches")
    elapsed = time.time() - start
    print(f"Scroll + prepare took {elapsed:.1f}s")

    # Write SQL to file for execution via psql
    outfile = "/tmp/qdrant_migration.sql"
    with open(outfile, "w") as f:
        f.write("-- Qdrant → Postgres migration\n")
        f.write("-- Devon-a704 | 2026-05-07\n")
        f.write(f"-- {migrated} vectors from {COLLECTION}\n\n")
        f.write("BEGIN;\n\n")
        for stmt in sql_statements:
            f.write(stmt + "\n\n")
        f.write("COMMIT;\n")

    print(f"SQL written to {outfile}")
    print(f"Total: {migrated} vectors ready for import")
    return outfile


if __name__ == "__main__":
    outfile = main()
    print(f"\nRun: psql -U {DB_USER} -d {DB_NAME} -f {outfile}")

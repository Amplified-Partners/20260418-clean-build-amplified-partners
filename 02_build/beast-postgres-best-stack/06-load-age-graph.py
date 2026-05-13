#!/usr/bin/env python3
"""
Step 6: Load business_brain AGE graph from live entities + relationships tables.

AMP-331 | Devon-0178 | 2026-05-13

Usage:
    # Dry run (default — no writes, just counts and sample output):
    python3 06-load-age-graph.py

    # Live run:
    python3 06-load-age-graph.py --execute

    # With custom connection:
    python3 06-load-age-graph.py --execute --host 127.0.0.1 --port 5432 --user cove --dbname amplified_brain

Run on Beast:
    docker cp 06-load-age-graph.py cove-postgres:/tmp/
    docker exec cove-postgres pip3 install psycopg2-binary 2>/dev/null
    docker exec cove-postgres python3 /tmp/06-load-age-graph.py --execute

Or from a machine with network access to Beast port 5433:
    pip install psycopg2-binary
    python3 06-load-age-graph.py --execute --host 135.181.161.131 --port 5433

What it does:
    1. Creates AGE graph 'business_brain' (if not exists)
    2. Reads all entities from the live 'entities' table
    3. Creates vertices with labels derived from entity_type (sanitized)
    4. Reads all relationships from the live 'relationships' table
    5. Creates edges with labels derived from relation_type (sanitized)

Estimated runtime: ~30 min for 54K entities + 34K relationships
Rollback: SELECT drop_graph('business_brain', true);

Safety:
    - Dry-run by default
    - Batched in configurable chunks (default 500)
    - Idempotent vertex creation via MERGE on entity UUID stored as property
    - Progress reporting every batch
"""

import argparse
import re
import sys
import time
from typing import Optional

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("ERROR: psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)


GRAPH_NAME = "business_brain"
BATCH_SIZE = 500

# Valid AGE label: must start with letter/underscore, contain only alnum/underscore
LABEL_RE = re.compile(r"[^a-zA-Z0-9_]")


def sanitize_label(raw: str) -> str:
    """Convert a raw string into a valid AGE vertex/edge label.

    Rules:
    - Replace non-alphanumeric chars with underscore
    - Ensure starts with a letter
    - Uppercase first letter for vertex labels (convention)
    - Collapse multiple underscores
    """
    label = LABEL_RE.sub("_", raw.strip())
    label = re.sub(r"_+", "_", label).strip("_")
    if not label:
        return "Unknown"
    if label[0].isdigit():
        label = "N_" + label
    return label[0].upper() + label[1:]


def escape_cypher_string(s: Optional[str]) -> str:
    """Escape a string for embedding in Cypher literal."""
    if s is None:
        return ""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')


def get_connection(args):
    """Create a psycopg2 connection."""
    conn = psycopg2.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        dbname=args.dbname,
    )
    conn.autocommit = True
    return conn


def init_age(cursor):
    """Load AGE extension and set search path."""
    cursor.execute("LOAD 'age'")
    cursor.execute("SET search_path = ag_catalog, public")


def ensure_graph(cursor, graph_name: str, dry_run: bool) -> bool:
    """Create the graph if it doesn't exist. Returns True if created."""
    cursor.execute(
        "SELECT count(*) FROM ag_catalog.ag_graph WHERE name = %s", (graph_name,)
    )
    exists = cursor.fetchone()[0] > 0
    if exists:
        print(f"  Graph '{graph_name}' already exists")
        return False
    if dry_run:
        print(f"  [DRY RUN] Would create graph '{graph_name}'")
        return False
    cursor.execute(f"SELECT create_graph('{graph_name}')")
    print(f"  Created graph '{graph_name}'")
    return True


def count_graph(cursor, graph_name: str):
    """Count vertices and edges in the graph."""
    try:
        cursor.execute(
            f"SELECT * FROM cypher('{graph_name}', $$MATCH (n) RETURN count(n)$$) AS (c agtype)"
        )
        v_count = cursor.fetchone()[0]
        cursor.execute(
            f"SELECT * FROM cypher('{graph_name}', $$MATCH ()-[r]->() RETURN count(r)$$) AS (c agtype)"
        )
        e_count = cursor.fetchone()[0]
        print(f"  Graph '{graph_name}': {v_count} vertices, {e_count} edges")
    except Exception as e:
        print(f"  Could not count graph contents: {e}")


def load_vertices(cursor, graph_name: str, dry_run: bool, batch_size: int) -> int:
    """Load entities as vertices into the AGE graph."""
    cursor.execute(
        "SELECT id, name, entity_type, summary FROM entities ORDER BY created_at"
    )
    rows = cursor.fetchall()
    total = len(rows)
    print(f"\n  Entities to load: {total}")

    if total == 0:
        print("  No entities found — run Step 5 first")
        return 0

    # Collect distinct labels
    labels = set()
    for row in rows:
        labels.add(sanitize_label(row[2] or "Unknown"))
    print(f"  Distinct vertex labels: {sorted(labels)}")

    if dry_run:
        for label in sorted(labels):
            count = sum(1 for r in rows if sanitize_label(r[2] or "Unknown") == label)
            print(f"    {label}: {count} vertices")
        print(f"  [DRY RUN] Would create {total} vertices in {(total + batch_size - 1) // batch_size} batches")
        return total

    loaded = 0
    errors = 0
    t0 = time.time()

    for i in range(0, total, batch_size):
        batch = rows[i : i + batch_size]
        for entity_id, name, entity_type, summary in batch:
            label = sanitize_label(entity_type or "Unknown")
            safe_name = escape_cypher_string(name)
            safe_summary = escape_cypher_string(
                (summary or "")[:500]  # Truncate long summaries for graph properties
            )
            cypher = (
                f"MERGE (n:{label} {{entity_id: '{entity_id}'}}) "
                f"ON CREATE SET n.name = '{safe_name}', "
                f"n.summary = '{safe_summary}'"
            )
            try:
                cursor.execute(
                    f"SELECT * FROM cypher('{graph_name}', $${cypher}$$) AS (v agtype)"
                )
                loaded += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"    ERROR on entity {entity_id}: {e}")

        elapsed = time.time() - t0
        rate = loaded / elapsed if elapsed > 0 else 0
        print(
            f"    Batch {i // batch_size + 1}: "
            f"{loaded}/{total} vertices ({loaded * 100 // total}%), "
            f"{rate:.0f}/s, {errors} errors"
        )

    elapsed = time.time() - t0
    print(f"  Vertices: {loaded} loaded, {errors} errors, {elapsed:.1f}s")
    return loaded


def load_edges(cursor, graph_name: str, dry_run: bool, batch_size: int) -> int:
    """Load relationships as edges into the AGE graph."""
    cursor.execute(
        "SELECT id, source_id, target_id, relation_type, summary, weight "
        "FROM relationships ORDER BY created_at"
    )
    rows = cursor.fetchall()
    total = len(rows)
    print(f"\n  Relationships to load: {total}")

    if total == 0:
        print("  No relationships found — run Step 5 first")
        return 0

    # Collect distinct edge labels
    labels = set()
    for row in rows:
        labels.add(sanitize_label(row[3] or "RELATED"))
    print(f"  Distinct edge labels: {sorted(labels)}")

    if dry_run:
        for label in sorted(labels):
            count = sum(1 for r in rows if sanitize_label(r[3] or "RELATED") == label)
            print(f"    {label}: {count} edges")
        print(f"  [DRY RUN] Would create {total} edges in {(total + batch_size - 1) // batch_size} batches")
        return total

    loaded = 0
    errors = 0
    t0 = time.time()

    for i in range(0, total, batch_size):
        batch = rows[i : i + batch_size]
        for rel_id, source_id, target_id, relation_type, summary, weight in batch:
            edge_label = sanitize_label(relation_type or "RELATED")
            safe_summary = escape_cypher_string((summary or "")[:200])
            weight_val = float(weight) if weight is not None else 1.0

            cypher = (
                f"MATCH (a {{entity_id: '{source_id}'}}), "
                f"(b {{entity_id: '{target_id}'}}) "
                f"CREATE (a)-[r:{edge_label} {{"
                f"rel_id: '{rel_id}', "
                f"summary: '{safe_summary}', "
                f"weight: {weight_val}"
                f"}}]->(b) "
                f"RETURN r"
            )
            try:
                cursor.execute(
                    f"SELECT * FROM cypher('{graph_name}', $${cypher}$$) AS (r agtype)"
                )
                loaded += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"    ERROR on rel {rel_id}: {e}")
                elif errors == 6:
                    print(f"    (suppressing further error output)")

        elapsed = time.time() - t0
        rate = loaded / elapsed if elapsed > 0 else 0
        print(
            f"    Batch {i // batch_size + 1}: "
            f"{loaded}/{total} edges ({loaded * 100 // total}%), "
            f"{rate:.0f}/s, {errors} errors"
        )

    elapsed = time.time() - t0
    print(f"  Edges: {loaded} loaded, {errors} errors, {elapsed:.1f}s")
    return loaded


def main():
    parser = argparse.ArgumentParser(
        description="Load business_brain AGE graph from live entity/relationship tables"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually write to the database (default is dry-run)",
    )
    parser.add_argument("--host", default="localhost", help="PostgreSQL host")
    parser.add_argument("--port", default=5432, type=int, help="PostgreSQL port")
    parser.add_argument("--user", default="cove", help="PostgreSQL user")
    parser.add_argument("--password", default="", help="PostgreSQL password")
    parser.add_argument(
        "--dbname", default="amplified_brain", help="PostgreSQL database"
    )
    parser.add_argument(
        "--batch-size", default=BATCH_SIZE, type=int, help="Batch size for inserts"
    )
    parser.add_argument(
        "--graph-name", default=GRAPH_NAME, help="AGE graph name to create/populate"
    )
    args = parser.parse_args()

    dry_run = not args.execute
    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"═══════════════════════════════════════════════════")
    print(f"  AGE Graph Loader — {mode}")
    print(f"  Graph: {args.graph_name}")
    print(f"  Target: {args.user}@{args.host}:{args.port}/{args.dbname}")
    print(f"═══════════════════════════════════════════════════")

    conn = get_connection(args)
    cur = conn.cursor()

    print("\n[1/5] Loading AGE extension...")
    init_age(cur)
    print("  AGE loaded, search_path set")

    print("\n[2/5] Ensuring graph exists...")
    ensure_graph(cur, args.graph_name, dry_run)

    print("\n[3/5] Loading vertices (entities)...")
    v_count = load_vertices(cur, args.graph_name, dry_run, args.batch_size)

    print("\n[4/5] Loading edges (relationships)...")
    e_count = load_edges(cur, args.graph_name, dry_run, args.batch_size)

    print("\n[5/5] Final graph state...")
    if not dry_run:
        count_graph(cur, args.graph_name)

    print(f"\n{'═' * 51}")
    print(f"  {mode} complete.")
    print(f"  Vertices: {v_count}")
    print(f"  Edges:    {e_count}")
    if dry_run:
        print(f"\n  To execute for real, re-run with --execute")
    print(f"{'═' * 51}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()

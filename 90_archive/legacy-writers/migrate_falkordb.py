#!/usr/bin/env python3
"""
LEGACY — DO NOT RUN against canonical amplified_brain.
Archived by AMP-302. One-shot ETL from FalkorDB, completed 2026-05-07.
Original: 02_build/brain-migration/migrate_falkordb.py

Migrate FalkorDB graph data → Postgres via Python redis client + CSV COPY.
Devon-a704 | 2026-05-07 | Amplified Brain migration v3
Archived-by: Devon-0de2 | 2026-05-11 | AMP-302

Uses redis-py for proper structured data extraction (handles multiline content).
Uses CSV COPY for bulk loading into Postgres.
"""

raise RuntimeError(
    "LEGACY WRITER — archived by AMP-302. "
    "Do not run against canonical amplified_brain. "
    "Use the canonical ingestion pipeline (v0.3) instead."
)
import csv
import json
import subprocess
import sys
import time
import uuid
import os
import redis

PG_CONTAINER = "cove-postgres"
DB_NAME = "amplified_brain"
DB_USER = "brain_writer"
DB_SUPERUSER = "cove"


def is_valid_uuid(s):
    try:
        uuid.UUID(str(s))
        return True
    except (ValueError, AttributeError):
        return False


def get_unique_id(raw_uuid, seen_ids):
    if raw_uuid and raw_uuid != "NULL" and is_valid_uuid(raw_uuid) and raw_uuid not in seen_ids:
        seen_ids.add(raw_uuid)
        return raw_uuid
    new_id = str(uuid.uuid4())
    while new_id in seen_ids:
        new_id = str(uuid.uuid4())
    seen_ids.add(new_id)
    return new_id


def query_graph(r, graph_name, cypher):
    """Execute a Cypher query and return list of dicts."""
    try:
        result = r.execute_command("GRAPH.QUERY", graph_name, cypher)
    except Exception as e:
        print(f"    Query error: {e}")
        return []
    
    if not result or len(result) < 2:
        return []
    
    headers = [h.decode() if isinstance(h, bytes) else str(h) for h in result[0]]
    rows = []
    for row_data in result[1]:
        row = {}
        for i, val in enumerate(row_data):
            if i < len(headers):
                if isinstance(val, bytes):
                    val = val.decode("utf-8", errors="replace")
                elif isinstance(val, (int, float)):
                    val = str(val)
                elif val is None:
                    val = ""
                else:
                    val = str(val)
                row[headers[i]] = val
        rows.append(row)
    return rows


def extract_paginated(r, graph_name, cypher_base, batch_size=2000):
    """Extract all rows using SKIP/LIMIT pagination."""
    all_rows = []
    offset = 0
    while True:
        cypher = f"{cypher_base} SKIP {offset} LIMIT {batch_size}"
        rows = query_graph(r, graph_name, cypher)
        if not rows:
            break
        all_rows.extend(rows)
        offset += batch_size
        if offset % 10000 == 0:
            print(f"      {offset} rows...", flush=True)
        if len(rows) < batch_size:
            break
    return all_rows


def psql(sql, user=DB_USER):
    """Run SQL via docker exec psql."""
    result = subprocess.run(
        ["docker", "exec", PG_CONTAINER, "psql", "-U", user, "-d", DB_NAME, "-c", sql],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout.strip(), result.stderr.strip()


def copy_csv(csv_path, table, columns, user=DB_USER):
    """COPY CSV into Postgres."""
    container_path = f"/tmp/{os.path.basename(csv_path)}"
    subprocess.run(["docker", "cp", csv_path, f"{PG_CONTAINER}:{container_path}"], check=True)
    
    cols = ", ".join(columns)
    sql = f"\\copy {table} ({cols}) FROM '{container_path}' WITH (FORMAT csv, NULL '')"
    
    result = subprocess.run(
        ["docker", "exec", PG_CONTAINER, "psql", "-U", user, "-d", DB_NAME, "-c", sql],
        capture_output=True, text=True, timeout=300
    )
    
    if result.returncode != 0:
        print(f"    COPY ERROR: {result.stderr[:300]}")
        return 0
    
    print(f"    {result.stdout.strip()}")
    # Parse count from "COPY NNNNN"
    try:
        return int(result.stdout.strip().split()[-1])
    except:
        return 0


def main():
    print("=" * 60)
    print("FalkorDB → Postgres Migration v3 (redis-py + CSV COPY)")
    print("Devon-a704 | 2026-05-07")
    print("=" * 60)
    start = time.time()
    
    # Connect to FalkorDB
    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=False)
    r.ping()
    print("Connected to FalkorDB")
    
    # ── Prep: clear old data and drop unique constraint ──
    print("\nPreparing Postgres...")
    psql("DELETE FROM relationships;")
    psql("DELETE FROM episodes;")
    psql("DELETE FROM entities;")
    psql("ALTER TABLE entities DROP CONSTRAINT IF EXISTS entities_name_entity_type_key;", user=DB_SUPERUSER)
    print("  Cleared tables, dropped unique constraint")
    
    # ══════════════════════════════════════════════════════
    # EXTRACT
    # ══════════════════════════════════════════════════════
    
    all_entities = []  # list of dicts with id, name, entity_type, summary, properties
    all_episodes = []
    all_rels = []
    
    for graph_name in ["business_knowledge", "amplified"]:
        print(f"\n[Extracting from '{graph_name}']")
        
        # ── Entities ──
        print("  Entities...")
        ents = extract_paginated(r, graph_name,
            "MATCH (n:Entity) RETURN n.uuid AS uuid, n.name AS name, n.entity_type AS entity_type, n.summary AS summary, n.group_id AS group_id, n.labels AS labels")
        print(f"    {len(ents)} Entity nodes")
        for e in ents:
            e["_type"] = e.get("entity_type") or "entity"
            e["_graph"] = graph_name
        all_entities.extend(ents)
        
        # ── Documents ──
        print("  Documents...")
        docs = extract_paginated(r, graph_name,
            "MATCH (n:Document) RETURN n.uuid AS uuid, n.name AS name, n.summary AS summary, n.group_id AS group_id")
        print(f"    {len(docs)} Document nodes")
        for d in docs:
            d["_type"] = "document"
            d["_graph"] = graph_name
        all_entities.extend(docs)
        
        # ── Categories ──
        print("  Categories...")
        cats = query_graph(r, graph_name, "MATCH (n:Category) RETURN n.uuid AS uuid, n.name AS name, n.group_id AS group_id LIMIT 1000")
        print(f"    {len(cats)} Category nodes")
        for c in cats:
            c["_type"] = "category"
            c["_graph"] = graph_name
        all_entities.extend(cats)
        
        # ── Mechanism (amplified only) ──
        mechs = query_graph(r, graph_name, "MATCH (n:Mechanism) RETURN n.uuid AS uuid, n.name AS name, n.summary AS summary, n.group_id AS group_id LIMIT 1000")
        if mechs:
            print(f"    {len(mechs)} Mechanism nodes")
            for m in mechs:
                m["_type"] = "mechanism"
                m["_graph"] = graph_name
            all_entities.extend(mechs)
        
        # ── Episodes ──
        print("  Episodes...")
        eps = extract_paginated(r, graph_name,
            "MATCH (n:Episodic) RETURN n.uuid AS uuid, n.name AS name, n.source AS source, n.source_description AS source_description, n.content AS content, n.group_id AS group_id, n.valid_at AS valid_at")
        print(f"    {len(eps)} Episodic nodes")
        for ep in eps:
            ep["_graph"] = graph_name
        all_episodes.extend(eps)
        
        # ── Relationships ──
        print("  Relationships...")
        rels = extract_paginated(r, graph_name,
            "MATCH (s)-[rel]->(t) RETURN s.uuid AS s_uuid, t.uuid AS t_uuid, type(rel) AS rel_type, rel.uuid AS r_uuid, rel.fact AS fact, rel.weight AS weight, rel.group_id AS group_id, s.name AS s_name, t.name AS t_name")
        print(f"    {len(rels)} relationships")
        for rel in rels:
            rel["_graph"] = graph_name
        all_rels.extend(rels)
    
    print(f"\nTotals: {len(all_entities)} entities, {len(all_episodes)} episodes, {len(all_rels)} relationships")
    
    # ══════════════════════════════════════════════════════
    # TRANSFORM → CSV
    # ══════════════════════════════════════════════════════
    
    print("\nWriting CSV files...")
    
    # ── Entities CSV ──
    seen_ids = set()
    name_to_id = {}  # name → postgres UUID for relationship linking
    
    with open("/tmp/entities.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for e in all_entities:
            eid = get_unique_id(e.get("uuid", ""), seen_ids)
            name = e.get("name", "") or "unnamed"
            etype = e.get("_type", "entity")
            summary = e.get("summary", "") or ""
            
            props = json.dumps({
                "group_id": e.get("group_id", ""),
                "labels": e.get("labels", ""),
                "source_graph": e.get("_graph", ""),
            })
            
            writer.writerow([eid, name, etype, summary, props])
            
            # Build lookup — first occurrence wins
            if name not in name_to_id:
                name_to_id[name] = eid
    
    print(f"  entities.csv: {len(seen_ids)} rows, {len(name_to_id)} unique names")
    
    # ── Episodes CSV ──
    ep_seen = set()
    with open("/tmp/episodes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for ep in all_episodes:
            eid = get_unique_id(ep.get("uuid", ""), ep_seen)
            content = ep.get("content", "") or ""
            source = ep.get("source", "") or ""
            name = ep.get("name", "") or ""
            
            # content is NOT NULL — skip if truly empty
            if not content and not name:
                continue
            if not content:
                content = name  # use name as fallback content
            
            meta = json.dumps({
                "source_description": ep.get("source_description", ""),
                "group_id": ep.get("group_id", ""),
                "valid_at": ep.get("valid_at", ""),
                "source_graph": ep.get("_graph", ""),
            })
            
            writer.writerow([eid, content, source, "falkordb_migration", name, meta])
    
    print(f"  episodes.csv: {len(ep_seen)} rows")
    
    # ── Relationships CSV ──
    rel_seen = set()
    rel_written = 0
    rel_skipped = 0
    
    with open("/tmp/relationships.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for rel in all_rels:
            s_name = rel.get("s_name", "")
            t_name = rel.get("t_name", "")
            
            s_id = name_to_id.get(s_name)
            t_id = name_to_id.get(t_name)
            
            if not s_id or not t_id:
                rel_skipped += 1
                continue
            
            rid = get_unique_id(rel.get("r_uuid", ""), rel_seen)
            rel_type = rel.get("rel_type", "") or "RELATED_TO"
            fact = rel.get("fact", "") or ""
            
            try:
                weight = float(rel.get("weight", "1.0") or "1.0")
            except (ValueError, TypeError):
                weight = 1.0
            
            props = json.dumps({
                "group_id": rel.get("group_id", ""),
                "source_graph": rel.get("_graph", ""),
                "original_source_uuid": rel.get("s_uuid", ""),
                "original_target_uuid": rel.get("t_uuid", ""),
            })
            
            writer.writerow([rid, s_id, t_id, rel_type, fact, weight, props])
            rel_written += 1
    
    print(f"  relationships.csv: {rel_written} rows ({rel_skipped} skipped — endpoint not in entities)")
    
    # ══════════════════════════════════════════════════════
    # LOAD into Postgres
    # ══════════════════════════════════════════════════════
    
    print("\nLoading into Postgres...")
    
    print("  [Entities]")
    ent_loaded = copy_csv("/tmp/entities.csv", "entities",
        ["id", "name", "entity_type", "summary", "properties"])
    
    print("  [Episodes]")
    ep_loaded = copy_csv("/tmp/episodes.csv", "episodes",
        ["id", "content", "source", "source_type", "summary", "metadata"])
    
    print("  [Relationships]")
    rel_loaded = copy_csv("/tmp/relationships.csv", "relationships",
        ["id", "source_id", "target_id", "relation_type", "summary", "weight", "properties"])
    
    # ── Re-add unique constraint ──
    print("\n  Re-adding unique constraint...")
    out, err = psql("CREATE UNIQUE INDEX IF NOT EXISTS idx_entities_name_type ON entities (name, entity_type);", user=DB_SUPERUSER)
    print(f"    {out or err}")
    
    # ── Final verification ──
    print("\n\n═══ FINAL COUNTS ═══")
    for table in ["knowledge_vectors", "entities", "episodes", "relationships"]:
        out, _ = psql(f"SELECT count(*) FROM {table};", user="cove")
        print(f"  {table}: {out.strip()}")
    
    elapsed = time.time() - start
    print(f"\nMigration completed in {elapsed:.1f}s")


if __name__ == "__main__":
    main()

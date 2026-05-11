# Amplified Brain Migration

Migration scripts for consolidating FalkorDB (graph) and Qdrant (vector) into unified Postgres with pgvector.

> **AMP-302 (2026-05-11): legacy writers frozen.** The scripts in this
> directory are one-shot ETL utilities. The canonical writer is the
> Temporal activity `write_to_memory_stores` in
> `02_build/cove-orchestrator/temporal/activities/ingestion_activities.py`.
> Re-running anything here requires the documented migration
> protocol — see [`RUNBOOK_LEGACY_FREEZE.md`](./RUNBOOK_LEGACY_FREEZE.md).
> See also the after-action template at
> `02_build/cove-orchestrator/docs/COMPOUND_ENGINEERING_AFTER_ACTION_TEMPLATE.md`.

## What was migrated

| Source | Target Table | Count |
|--------|-------------|-------|
| Qdrant `amplified_knowledge` | `knowledge_vectors` | 57,434 |
| FalkorDB Entity/Document/Category/Mechanism nodes | `entities` | 53,959 |
| FalkorDB Episodic nodes | `episodes` | 4,257 |
| FalkorDB Entity↔Entity relationships | `relationships` | 34,488 |
| FalkorDB Episodic→Entity MENTIONS | `episode_entities` | 59,192 |

## Scripts

- `migrate_qdrant.py` — Extracts vectors from Qdrant REST API, generates bulk SQL INSERT
- `migrate_falkordb.py` — Extracts graph data via redis-py, writes CSV, loads via COPY
- `brain_mcp_server.py` — FastAPI MCP server (read-only :8090, write :8091)
- `Dockerfile` — Container build for MCP server

## Access control

- **Read-only** (port 8090): All agents (Antigravity, Cassian, Perplexity, OpenClaw)
- **Write** (port 8091): Devin only

## Database

- Host: `cove-postgres` on Beast (135.181.161.131)
- Database: `amplified_brain`
- Users: `brain_reader` (read-only), `brain_writer` (read+write)

---

*Devon-a704 | 2026-05-07 | Amplified Brain migration from Qdrant+FalkorDB to Postgres*

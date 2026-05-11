# Amplified Brain Migration

Migration scripts for consolidating FalkorDB (graph) and Qdrant (vector) into unified Postgres with pgvector.

> **AMP-302 (2026-05-11):** The migration scripts below (`migrate_qdrant.py`,
> `migrate_falkordb.py`) are now **archived** in `90_archive/legacy-writers/`.
> They raise `RuntimeError` on import. All new data ingestion uses the
> canonical pipeline — see `02_build/pipeline/RUNBOOK.md`.
> The Brain MCP server retains **read-only** functionality; write tools have
> been removed (`ALLOW_WRITES = False`).

## What was migrated

| Source | Target Table | Count |
|--------|-------------|-------|
| Qdrant `amplified_knowledge` | `knowledge_vectors` | 57,434 |
| FalkorDB Entity/Document/Category/Mechanism nodes | `entities` | 53,959 |
| FalkorDB Episodic nodes | `episodes` | 4,257 |
| FalkorDB Entity↔Entity relationships | `relationships` | 34,488 |
| FalkorDB Episodic→Entity MENTIONS | `episode_entities` | 59,192 |

## Scripts

- ~~`migrate_qdrant.py`~~ — **Archived** (`90_archive/legacy-writers/`). Was: Qdrant REST API → bulk SQL INSERT
- ~~`migrate_falkordb.py`~~ — **Archived** (`90_archive/legacy-writers/`). Was: redis-py → CSV → COPY
- `brain_mcp_server.py` — FastAPI MCP server (**read-only** :8090; write port :8091 disabled since AMP-302)
- `Dockerfile` — Container build for MCP server

## Access control

- **Read-only** (port 8090): All agents (Antigravity, Cassian, Perplexity, OpenClaw)
- ~~**Write** (port 8091): Devin only~~ — Disabled by AMP-302. All writes go through the canonical pipeline.

## Database

- Host: `cove-postgres` on Beast (135.181.161.131)
- Database: `amplified_brain`
- Users: `brain_reader` (read-only), `brain_writer` (read+write)

---

*Devon-a704 | 2026-05-07 | Amplified Brain migration from Qdrant+FalkorDB to Postgres*
*Devon-be18-child-docs | 2026-05-11 | AMP-302 legacy path annotations*

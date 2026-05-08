---
title: Data architecture — canonical data layer for Amplified Partners
date: 2026-05-08
version: 1
status: authoritative now
signed-by:
  - Devon-973e | 2026-05-08 | devin-973ed35fae1b4b44a52594bcb53b3f0a
---

<!-- markdownlint-disable-file MD013 -->

# Data Architecture

Single source of truth for Amplified Partners' data layer. If an agent or document references graph, vector, or relational storage, this file is the authority on what is canonical.

---

## Canonical stack (current)

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Relational + primary store** | PostgreSQL | All structured data — CRM, tenants, Business Brain state, operational telemetry, financial models, compliance, audit logs. Single database engine. |
| **Graph** | PostgreSQL graph extension (Apache AGE) | Entity relationships, knowledge graph, Business Brain connections, PUDDING recipe graphs. Runs inside the same PostgreSQL instance — no separate process. |
| **Vector / similarity search** | pgvector with HNSW indexing | Semantic search, embeddings, vault content retrieval, semantic cache for LLM prompts. HNSW (Hierarchical Navigable Small World) algorithm by Malkov & Yashunin provides approximate nearest-neighbour search at scale. Runs inside the same PostgreSQL instance. |

**One database engine. Three capabilities. No separate processes for graph or vector.**

---

## Why this replaces the previous stack

The previous stack used three separate systems:

| Deprecated | Was | Replaced by |
|-----------|------|-------------|
| **FalkorDB** | Standalone graph database (Redis-protocol, port 6379) | PostgreSQL + Apache AGE |
| **Qdrant** | Standalone vector database (ports 6333-6334, 57k embeddings) | PostgreSQL + pgvector (HNSW) |
| **Multiple Postgres instances** | Fragmented across stacks (primary, cove-postgres, docker-postgres-1) | Consolidated PostgreSQL |

Reasons for the change (Ewan, 2026-05-08):

1. **FalkorDB and Qdrant are bust** — stability issues documented in AMP-141, AMP-139, clean-build PR #55 (FalkorDB stability closure), PR #54 (Graphiti hot-path patch). Ongoing operational burden exceeded value.
2. **PostgreSQL is robust** — battle-tested, single point of operational expertise, well-understood backup/restore, proven at scale.
3. **Consolidation reduces moving parts** — one process to monitor, one backup strategy, one connection pool, one upgrade path.
4. **pgvector + HNSW is production-grade** — the same algorithm (by Russian mathematicians Malkov & Yashunin) that powers dedicated vector databases, now available natively in PostgreSQL.
5. **Apache AGE gives Cypher-compatible graph queries** — same query language as FalkorDB/Neo4j, inside PostgreSQL.

---

## Terminology (locked)

| Term | Canonical meaning | Do not confuse with |
|------|------------------|---------------------|
| **the Russian maths** | HNSW algorithm (Hierarchical Navigable Small World) by Yury Malkov & Dmitry Yashunin. The vector indexing algorithm used by pgvector. | Not a library or product name — refers to the mathematical algorithm. |
| **pgvector** | PostgreSQL extension providing vector similarity search with HNSW and IVFFlat indexes. | Not Qdrant. Not a separate service. Runs inside PostgreSQL. |
| **Apache AGE** | PostgreSQL extension providing graph database functionality with openCypher query language. | Not FalkorDB. Not Neo4j. Not a separate process. Runs inside PostgreSQL. |
| **HNSW** | Hierarchical Navigable Small World — the indexing algorithm for approximate nearest-neighbour search. O(log n) query time. Published 2016 (Malkov & Yashunin). | Not a product. A mathematical algorithm implemented by pgvector. |

---

## Migration status

| Component | Status | Notes |
|-----------|--------|-------|
| FalkorDB → Apache AGE | **Planned** | Graph schema (9,000 nodes, 4 graphs) to be migrated. Cypher queries largely compatible. |
| Qdrant → pgvector | **Planned** | 57,434 embeddings (384-dim) to be migrated. HNSW index to be created on target table. |
| Token-proxy semantic cache (Qdrant `llm_cache`) | **Planned** | Migrate to pgvector table with same 0.95 threshold / 24h TTL logic. |
| CRM PostgreSQL | **Existing** | Already on PostgreSQL. Add AGE + pgvector extensions. |
| Amplified Core PostgreSQL | **Existing** | Already on PostgreSQL. Add AGE + pgvector extensions. |

---

## What this means for agents

1. **Do not provision, reference, or depend on FalkorDB or Qdrant in new work.** They are deprecated.
2. **All new graph work uses Apache AGE** (openCypher syntax inside PostgreSQL).
3. **All new vector/embedding work uses pgvector** (HNSW index).
4. **Existing code referencing FalkorDB/Qdrant** is legacy — mark it, migrate it, or flag it for migration. Do not extend it.
5. **The APDS spec** (FalkorDB schema in `90_archive/specifications/`) is historical reference. New APDS implementation targets PostgreSQL + AGE.

---

## Documents superseded by this file

These documents contain references to the old stack. They remain in the repo as historical record but their data-layer claims are superseded:

- `02_build/INFRASTRUCTURE.md` § Knowledge and search (FalkorDB, Qdrant rows) — **deprecated, pending update**
- `90_archive/specifications/mac-drop-2026-04/AMPLIFIED-PUDDING-DISCOVERY-SYSTEM.md` § FalkorDB Schema — **non-authoritative archive, historical only**
- `90_archive/2026-03_amplified-consolidated-architecture_narrative.md` — **non-authoritative archive**
- `90_archive/2026-03_amplified-consolidated-architecture_full.txt` — **non-authoritative archive**

---

## Changelog

### v1 — 2026-05-08

- Created. Establishes PostgreSQL + Apache AGE + pgvector (HNSW) as canonical data layer.
- Deprecates FalkorDB and Qdrant.
- Locks terminology: "the Russian maths" = HNSW algorithm by Malkov & Yashunin.

Signed-by: Devon-973e | 2026-05-08 | devin-973ed35fae1b4b44a52594bcb53b3f0a

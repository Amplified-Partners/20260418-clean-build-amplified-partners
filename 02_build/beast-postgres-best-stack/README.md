# Beast PostgreSQL Best-Stack Build — AMP-331

Migration runbook for the optimal Postgres + AGE + pgvector + pgvectorscale stack on the Beast.

## Current State (MEASURED 2026-05-13 05:48 UTC)

| Component | Version | Status |
|-----------|---------|--------|
| PostgreSQL | 15.17 (timescaledb-ha:pg15-latest) | Running in `cove-postgres` |
| Apache AGE | 1.6.0 | Extension installed, **NOT** in shared_preload_libraries |
| pgvector | 0.8.2 | 163,554 vectors in `knowledge_vectors` (384-dim, HNSW cosine) |
| TimescaleDB | 2.10.2 + Toolkit 1.16.0 | Preloaded |
| pgvectorscale | — | Not installed |

Container: `cove-postgres` (image: `timescale/timescaledb-ha:pg15-latest`)
Data mount: internal volume at `/home/postgres/pgdata/data`
User: `cove` (superuser)
Database: `amplified_brain`

### Critical warning: PG15 ↔ PG16 mismatch

`docker-postgres-1` runs `postgres:16-alpine` (port 5432) but `cove-postgres` (timescaledb-ha, port 5433) is the brain DB on PG15. Do **NOT** `--force-recreate` the postgres container. A proper `pg_upgrade` is separate work.

### shared_preload_libraries incident (2026-05-13)

A previous session set `shared_preload_libraries = 'timescaledb,age'` via `ALTER SYSTEM`. The timescaledb-ha image does not include the AGE `.so` in the standard preload path, causing Postgres to interpret the entire string as one library name and crash-loop. Fixed by reverting to `'timescaledb'`. AGE must be loaded **per-connection** via `LOAD 'age'`.

## Stranded Data

| Table | Rows | Status |
|-------|------|--------|
| `entities_legacy_2026_05_10` | 53,959 | Stranded (live `entities` = 0) |
| `relationships_legacy_2026_05_10` | 34,488 | Stranded (live `relationships` = 0) |
| `episodes_legacy_2026_05_10` | 4,257 | Stranded (live `episodes` = 0) |
| `knowledge_vectors_legacy_2026_05_10` | 225,841 | Backup (live `knowledge_vectors` = 163,554) |

## Execution Order

| Step | Script | Downtime | Rollback |
|------|--------|----------|----------|
| 1 | `01-age-preload-smoke-test.sql` | None | N/A (read-only smoke test) |
| 5 | `05-promote-legacy-tables.sql` | None (online DML) | `TRUNCATE entities, relationships, episodes` |
| 6 | `06-load-age-graph.py` | None (additive) | `SELECT drop_graph('business_brain', true)` |
| 7 | `07-halfvec-migration.sql` | ~5 min (index rebuild) | Reverse ALTER + rebuild original index |
| 8 | `08-pgvectorscale-install.md` | ~30s (restart) | `DROP EXTENSION vectorscale` |

Steps are independently executable and independently reversible.

## Decisions Taken (all reversible)

1. **AGE via per-connection LOAD, not shared_preload.** OPINION 95%. The timescaledb-ha image does not support AGE in shared_preload. Empirically confirmed by crash.
2. **Graph name `business_brain`**, not `compound_design`.  OPINION 90%. `compound_design` has a design-research vocabulary (Artifacts, Patterns, Research, Pudding). The legacy FalkorDB data is general-purpose entity/document/category data. Separate graphs, separate purposes.
3. **Skip pgvectorscale install today.** OPINION 88%. At 163K vectors × 384-dim, HNSW is comfortable. The crossover where DiskANN adds value is ~5M vectors. Install instructions provided for when the time comes.
4. **Defer halfvec conversion.** OPINION 82%. Saves ~396 MB on a 1.4 TB disk. Worth doing, but low urgency. Execute during next off-hours maintenance window or when upgrading embedding model to higher dimensions.
5. **Promote legacy data now.** OPINION 95%. Live tables are empty. 54K entities + 34K relationships are stranded. This is data loss waiting to happen.

---

*Devon-0178 | 2026-05-13 | session devin-01787ef6cd57476aacdb0f1dfe10b069*
*Linear: [AMP-331](https://linear.app/amplifiedpartners/issue/AMP-331)*

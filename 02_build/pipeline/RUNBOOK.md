# Canonical Ingestion Pipeline — Runbook

**AMP-302 · Pipeline v0.3 · Manifest-first, single writer**

This runbook covers the end-to-end canonical ingestion pipeline introduced
in AMP-302. It replaces all legacy write paths (Qdrant migration,
FalkorDB migration, `write_to_memory_stores`). Every row that enters the
canonical `knowledge_vectors` table must have a manifest line.

---

## Architecture overview

```
disk (store_b_clean)
        │
   ┌────▼────┐
   │ Stage 1  │  run_unified_ingestion — dedup raw → store_b_clean
   └────┬────┘
   ┌────▼────┐
   │ Stage 2  │  run_pudding_extraction — PUDDING taxonomy labelling
   └────┬────┘
   ┌────▼────┐
   │ Stage 3  │  generate_manifest — disk → deterministic JSONL manifest
   └────┬────┘
   ┌────▼────┐
   │ Stage 4  │  write_canonical_vectors — manifest → canonical DB
   └────┬────┘
   ┌────▼────┐
   │ Stage 5  │  log_pipeline_run — observability record
   └─────────┘
```

**Temporal workflow:** `APDSIngestionWorkflow` in
`02_build/cove-orchestrator/temporal/workflows/apds_ingestion_workflow.py`.

**Schedule:** `*/10 * * * *` (every 10 minutes), registered as
`apds-ingestion-10min` on the `cove-build-queue` task queue.

---

## Prerequisites

| Requirement | Detail |
|-------------|--------|
| PostgreSQL  | `amplified_brain` database on `cove-postgres` (Beast) |
| Migrations 001–007 | Applied in order. 001 creates `audit_log`, 004 creates `pipeline_runs`, 007 creates canonical tables |
| Roles | `brain_writer` (INSERT/UPDATE), `brain_reader` (SELECT) — created in migration 005, extended in 007 |
| Extensions | `vector` (pgvector), `uuid-ossp` — created by migration 007 |
| Source root | `/opt/amplified/vault/store_b_clean` (markdown files) |
| Manifest dir | `/opt/amplified/vault/manifests` |
| Temporal | Worker running on `cove-build-queue` |
| Env var | `BRAIN_DSN` — connection string for `brain_writer` role (falls back to `postgresql://brain_writer@cove-postgres:5432/amplified_brain`) |

---

## Migration 007 — canonical schema v0.3

**File:** `02_build/cove-orchestrator/db/migrations/007_canonical_schema_v0.3.sql`

### What it does

1. **Freezes legacy tables** — renames `knowledge_vectors`, `entities`,
   `relationships`, `episodes` to `*_legacy_2026_05_10`. No data deleted.
2. **Creates canonical tables** — `knowledge_vectors` (with provenance
   columns: `run_id`, `file_hash`, `chunk_hash`, `prev_hash`/`next_hash`
   chain, `signed_by`, `ingested_at`), `entities`, `relationships`,
   `episodes`.
3. **Creates HNSW vector index** on `knowledge_vectors.embedding`
   (384-dim, cosine ops, m=16, ef_construction=64).
4. **Creates consumer views** — `knowledge_vectors_canonical` (filtered
   to `provenance = 'amplified-pipeline-v0.3'`) and `legacy_pre_v0_3`
   (alias to the frozen legacy table).
5. **Creates `ingestion_manifests` table** — stores manifest metadata
   per run.
6. **Extends role grants** for `brain_writer` and `brain_reader`.

### How to run

```bash
# SSH to Beast
ssh -i ~/.ssh/beastkey root@135.181.161.131

# Run as superuser against amplified_brain
psql -U postgres -d amplified_brain \
  -f /path/to/007_canonical_schema_v0.3.sql
```

**Pre-flight checks:**

```sql
-- Verify legacy tables exist before renaming
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('knowledge_vectors', 'entities', 'relationships', 'episodes');

-- Check row counts (for post-migration comparison)
SELECT 'knowledge_vectors' AS tbl, count(*) FROM knowledge_vectors
UNION ALL SELECT 'entities', count(*) FROM entities
UNION ALL SELECT 'relationships', count(*) FROM relationships
UNION ALL SELECT 'episodes', count(*) FROM episodes;
```

**Post-migration checks:**

```sql
-- Verify renamed legacy tables
SELECT tablename FROM pg_tables
WHERE schemaname = 'public' AND tablename LIKE '%_legacy_2026_05_10';

-- Verify new canonical tables
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('knowledge_vectors', 'entities', 'relationships',
                    'episodes', 'ingestion_manifests');

-- Verify views
SELECT viewname FROM pg_views
WHERE schemaname = 'public'
  AND viewname IN ('knowledge_vectors_canonical', 'legacy_pre_v0_3');

-- Verify HNSW index
SELECT indexname FROM pg_indexes
WHERE tablename = 'knowledge_vectors'
  AND indexname = 'idx_kv_canonical_embedding';
```

### Rollback

**File:** `02_build/cove-orchestrator/db/migrations/007_rollback.sql`

```bash
psql -U postgres -d amplified_brain \
  -f /path/to/007_rollback.sql
```

This drops the canonical tables, views, and `ingestion_manifests`, then
renames the legacy tables back to their original names. Zero data loss.

---

## Manifest generator

**File:** `02_build/cove-orchestrator/temporal/activities/manifest_generator.py`
**Temporal activity:** `generate_manifest`

### What it does

- Deterministic sorted walk of `source_root` (all `*.md` files).
- Chunks each file by H2 headings (`## `), with a 4000 character max per
  chunk. Oversized chunks are split further.
- Builds a `prev_hash`/`next_hash` chain per file (SHA-256).
- Emits a JSONL manifest: one JSON line per source file, containing all
  chunk metadata.
- **Determinism contract:** same source files → identical manifest bytes.

### Inputs

| Field | Default | Description |
|-------|---------|-------------|
| `run_id` | (required) | Unique identifier for this pipeline run |
| `source_root` | `/opt/amplified/vault/store_b_clean` | Directory to scan for `.md` files |
| `manifest_dir` | `/opt/amplified/vault/manifests` | Where the JSONL manifest is written |
| `dry_run` | `False` | If `True`, emit counts + hash prediction without writing |

### Output

A JSONL file at `{manifest_dir}/{run_id}.jsonl`. Each line contains:

```json
{
  "run_id": "apds-...",
  "pipeline_version": "amplified-pipeline-v0.3",
  "source_root": "/opt/amplified/vault/store_b_clean",
  "file_path": "/opt/amplified/vault/store_b_clean/doc.md",
  "file_hash": "sha256:...",
  "size_bytes": 1234,
  "mtime": "2026-05-11T...",
  "chunks": [
    {
      "idx": 0,
      "chunk_hash": "sha256:...",
      "line_start": 1,
      "line_end": 15,
      "parent_heading": "(top-level)",
      "chunk_type": "prose",
      "prev_hash": null,
      "next_hash": "sha256:..."
    }
  ],
  "signed_by": "brain_writer_pipeline",
  "created_at": "2026-05-11T..."
}
```

### Dry-run

```python
ManifestInput(run_id="test-dry", dry_run=True)
```

Returns file/chunk counts and a manifest hash without writing to disk.

---

## Canonical writer

**File:** `02_build/cove-orchestrator/temporal/activities/canonical_writer.py`
**Temporal activity:** `write_canonical_vectors`

### What it does

- Reads the JSONL manifest from disk.
- For each chunk: reads the source file line range, generates a
  deterministic UUID5 ID (`UUID5(namespace, file_hash + ':' + chunk_index)`),
  and inserts into `knowledge_vectors` with `ON CONFLICT DO UPDATE`.
- Records the run in `pipeline_runs` (status tracking).
- Records the manifest in `ingestion_manifests`.
- Writes an `audit_log` entry with row counts.

### Inputs

| Field | Default | Description |
|-------|---------|-------------|
| `run_id` | (required) | Must match the manifest's `run_id` |
| `manifest_path` | (required) | Path to the JSONL manifest file |
| `manifest_hash` | (required) | SHA-256 hash of the manifest (from generator output) |
| `brain_dsn` | `$BRAIN_DSN` | PostgreSQL connection string |
| `batch_size` | `100` | Rows per batch |
| `dry_run` | `False` | If `True`, returns predicted counts without writing |

### Idempotency

IDs are deterministic: same `file_hash` + `chunk_index` always produce the
same UUID. Reruns upsert (`ON CONFLICT DO UPDATE`) rather than duplicating.

### Connection role

Connects as `brain_writer` only. No superuser access required.

---

## Derived rebuild

**File:** `02_build/cove-orchestrator/temporal/activities/derived_rebuild.py`

These are **derived indexes**, not source truth. They can be rebuilt from
`knowledge_vectors` at any time.

### `rebuild_entities` (Temporal activity)

- Walks canonical `knowledge_vectors` rows.
- Extracts PUDDING concepts from YAML frontmatter in content.
- Upserts into `entities` with `source_type = 'derived'`.
- IDs generated from `hashlib.sha256(concept_name)`.

### `rebuild_relationships` (Temporal activity)

- Reads all derived entities.
- Builds co-occurrence map: entities appearing in the same source file.
- Upserts `co-occurs-in` relationships with weight proportional to
  co-occurrence frequency.

### Inputs (both activities)

| Field | Default | Description |
|-------|---------|-------------|
| `run_id` | (required) | Pipeline run identifier |
| `brain_dsn` | `$BRAIN_DSN` | PostgreSQL connection string |
| `batch_size` | `500` | Rows per read batch |

### Running manually

Derived rebuilds are not part of the automated 10-minute schedule.
They should be triggered after a full re-ingestion or when entity/relationship
data needs refreshing.

---

## Running the full pipeline end-to-end

### Automated (normal operation)

The `APDSIngestionWorkflow` runs on a 10-minute Temporal schedule. No manual
intervention needed. If zero new files are found in Stage 1, Stages 2–4 are
skipped (idempotent no-op).

### Manual trigger via Temporal

```bash
# Trigger a single run from the Temporal CLI
temporal workflow start \
  --task-queue cove-build-queue \
  --type apds_ingestion \
  --workflow-id "apds-manual-$(date +%Y%m%dT%H%M)" \
  --input '{"full_rebuild": false}'
```

For a full rebuild (reprocesses all files, not just new ones):

```bash
temporal workflow start \
  --task-queue cove-build-queue \
  --type apds_ingestion \
  --workflow-id "apds-full-rebuild-$(date +%Y%m%dT%H%M)" \
  --input '{"full_rebuild": true}'
```

### Manual stage-by-stage

If you need to run individual stages outside Temporal (debugging, recovery):

```python
# Stage 3 only — generate manifest from existing store_b_clean
from temporal.activities.manifest_generator import generate_manifest, ManifestInput

result = await generate_manifest(ManifestInput(
    run_id="manual-2026-05-11",
    source_root="/opt/amplified/vault/store_b_clean",
    manifest_dir="/opt/amplified/vault/manifests",
    dry_run=True,  # set False to write
))
print(f"Files: {result.file_count}, Chunks: {result.chunk_count}")
```

```python
# Stage 4 only — write manifest to DB
from temporal.activities.canonical_writer import write_canonical_vectors, CanonicalWriterInput

result = await write_canonical_vectors(CanonicalWriterInput(
    run_id="manual-2026-05-11",
    manifest_path="/opt/amplified/vault/manifests/manual-2026-05-11.jsonl",
    manifest_hash="sha256:...",
    dry_run=True,  # set False to write
))
print(f"Written: {result.rows_written}, Skipped: {result.rows_skipped}")
```

---

## Troubleshooting

### Migration 007 fails: table already renamed

```
ERROR: relation "knowledge_vectors_legacy_2026_05_10" already exists
```

The migration was partially applied. Check which tables exist:

```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public'
  AND tablename LIKE 'knowledge_vectors%';
```

If the legacy table already exists but the canonical one does not, run
only the `CREATE TABLE` statements from section 2 onward of the
migration file.

### Manifest generator: "Source root not found"

```
ManifestResult(success=False, error="Source root not found: /opt/amplified/vault/store_b_clean")
```

The source directory does not exist or is not mounted. Verify:

```bash
ls -la /opt/amplified/vault/store_b_clean/
```

If running on a different host, override with `source_root` parameter.

### Canonical writer: "PostgreSQL connection failed"

```
CanonicalWriterResult(success=False, error="PostgreSQL connection failed: ...")
```

1. Check `BRAIN_DSN` env var is set correctly.
2. Verify `brain_writer` role exists and can connect:

```bash
psql "postgresql://brain_writer@cove-postgres:5432/amplified_brain" -c "SELECT 1;"
```

3. Check `pg_hba.conf` allows `brain_writer` connections.

### Canonical writer: "Manifest not found"

The manifest file from Stage 3 was not written to the expected path.
Check that `manifest_dir` exists and the run ID matches:

```bash
ls -la /opt/amplified/vault/manifests/
```

### Idempotent reruns produce different row counts

This is expected if source files changed between runs. The deterministic
ID contract is: same `file_hash` + `chunk_index` → same UUID. If a file's
content changed, its `file_hash` changes, producing new UUIDs. Old rows
remain (the writer does not delete).

### Derived rebuild: entity IDs

Entity IDs in `derived_rebuild.py` use `hashlib.sha256(concept_name)[:32]`
truncated to 32 hex characters and cast to UUID. This is a known
limitation from PR #91 review — the format may produce non-standard UUIDs.
Monitor for `invalid input syntax for type uuid` errors. If hit, the fix
is to switch to `uuid.uuid5()` as the canonical writer does.

### Legacy writers raise RuntimeError

```
RuntimeError: DEPRECATED: write_to_memory_stores retired by AMP-302.
```

This is intentional. All writes must go through the manifest-first
canonical pipeline. The old `write_to_memory_stores` activity,
`migrate_qdrant.py`, and `migrate_falkordb.py` are retired.
Archived copies are in `90_archive/legacy-writers/`.

### Checking pipeline health

```sql
-- Recent pipeline runs
SELECT run_id, started_at, completed_at, status, memory_pg_vectors
FROM pipeline_runs
ORDER BY started_at DESC
LIMIT 10;

-- Recent manifests
SELECT run_id, file_count, chunk_count, manifest_hash, created_at
FROM ingestion_manifests
ORDER BY created_at DESC
LIMIT 10;

-- Canonical vector counts by run
SELECT run_id, count(*) AS vectors
FROM knowledge_vectors
WHERE provenance = 'amplified-pipeline-v0.3'
GROUP BY run_id
ORDER BY run_id DESC
LIMIT 10;

-- Audit log for ingestion events
SELECT actor, action, resource_id, details, timestamp
FROM audit_log
WHERE action LIKE 'ingestion.%'
ORDER BY timestamp DESC
LIMIT 10;
```

---

## Legacy write paths (retired)

| Path | Status | Location |
|------|--------|----------|
| `migrate_qdrant.py` | Archived — raises `RuntimeError` on import | `90_archive/legacy-writers/` |
| `migrate_falkordb.py` | Archived — raises `RuntimeError` on import | `90_archive/legacy-writers/` |
| `write_to_memory_stores` | Deprecated — raises `RuntimeError` on call | `ingestion_activities.py` |
| Brain MCP write tools | Disabled — `ALLOW_WRITES = False` | `brain_mcp_server.py` |

All new data ingestion goes through the canonical pipeline (Stages 3–4).

---

Devon-be18-child-docs | 2026-05-11 | devin-29211adbdded4a8885ddb658655fb538

# Cove Ingestion Writer v0.3 — Manifest-First Canonical Contract

> Engineer B / AMP-302 / 2026-05-11
> Lane: canonical writer contract, telemetry, migrations, tests.

## Doctrine

> **Disk source material = truth.
> Manifest = proof.
> DB (knowledge_vectors) = rebuildable/searchable index.**

The DB is downstream of the manifest. If the DB is wrong, we rebuild from the
manifest. If the manifest is wrong, we rebuild from disk. The writer never
acts as a source of truth — it only renders the manifest into searchable form.

## Why v0.3 exists

Audit of the live DB found:

- `pipeline_runs` had **0 rows** despite rows in `knowledge_vectors`.
- `audit_log` had **0 rows** despite ingestion runs.
- The Temporal ingestion writer used a **path-derived** ID
  (`sha256(str(fp))[:32]`). Moving or renaming a file produced a brand-new
  row, silently duplicating content.
- The writer mutated `entities` inline. A re-ingest could rewrite graph
  edges without a separate derived step.
- `relationships` were never written.

Telemetry was *designed but not load-bearing* — the workflow logged at the
end on a best-effort basis (`except: warning`).

v0.3 fixes all of the above.

## What changed

### Code (new)

- `temporal/activities/manifest_writer.py`
  - `ManifestRow` — frozen dataclass with strict construction-time
    validation.
  - `derive_row_id(file_hash, chunk_index) -> UUIDv5` — the only allowed
    ID source. Path is informational.
  - `write_manifest_row` / `write_manifest_batch` — `ON CONFLICT (id) DO
    UPDATE` upserts. Idempotent under re-run.
  - Writer NEVER touches `entities` or `relationships`.
- `temporal/activities/ingestion_telemetry.py`
  - `start_run` — writes `pipeline_runs` row at start (status=`running`).
  - `finish_run` / `fail_run` — terminal-status close, always.
  - `audit_batch` / `audit_event` — one row per batch into
    `ingestion_audit_log`.

### Migration

- `db/migrations/007_writer_v03_provenance.sql`
  - Adds provenance columns: `file_hash`, `chunk_index`, `chunk_total`,
    `manifest_id`, `writer_version`, `ingested_at`.
  - Unique index on `(file_hash, chunk_index)`.
  - `CHECK` constraint pinning the `writer_version` format.
  - Creates `ingestion_audit_log` table.
  - Creates `knowledge_vectors_canonical` view — manifest-backed rows only.
  - **Production cutover** (the `brain_writer_pipeline` role) is wrapped
    in a `DO $$ ... $$` block that no-ops unless
    `app.allow_writer_v03_cutover = 'true'` is set on the session.
    See *Production cutover procedure* below.

### Tests

- `tests/test_manifest_writer.py` — 19 tests: ID determinism,
  idempotency, path-independence, provenance shape, chunk handling,
  batch behaviour, no-inline-mutation guard, canonical view qualification.
- `tests/test_ingestion_telemetry.py` — 10 tests: start_run /
  finish_run / fail_run, failure-as-status, audit_batch, status enum.
- `tests/test_writer_v03_migration.py` — 9 tests: migration text
  contracts (gated cutover, no ungated `GRANT`/`REVOKE`, canonical view
  filter, audit_log columns, writer_version check).

All 38 new tests pass with `pytest -q`.

## Writer contract (v0.3)

```python
from temporal.activities.manifest_writer import ManifestRow, write_manifest_batch

rows = [
    ManifestRow(
        manifest_id="2026-05-11T08-03Z/12345",
        file_hash="<sha256 of source bytes>",
        chunk_index=0,
        chunk_total=1,
        content="<chunk body>",
        source_path="/opt/amplified/archive/store_b_clean/...md",
        source_type="pudding_md",
        metadata={"taxonomy_version": "PUDDING_2026", "concepts": [...]},
    ),
    ...
]

async with asyncpg.connect(BRAIN_PIPELINE_DSN) as conn:
    result = await write_manifest_batch(conn, rows)
    # result.rows_written, result.rows_failed, result.ids
```

Guarantees:

1. **Determinism.** `derive_row_id(h, i) == derive_row_id(h, i)` always.
2. **Path-independence.** Moving a file does not produce a new row.
3. **Idempotency.** Re-writing the same row is a no-op upsert.
4. **Strict provenance.** Every written row has `file_hash`,
   `manifest_id`, `writer_version`. Rows missing any of those are
   excluded from `knowledge_vectors_canonical`.
5. **Single table.** The writer's SQL touches only `knowledge_vectors`.
   Entity / relationship derivation is a separate downstream step.

## Telemetry contract

Telemetry is **not optional** in v0.3. The workflow must:

1. Call `start_run(conn, run_id)` *before* any stage runs.
2. Call `audit_batch(...)` once per batch the writer processes.
3. Call `finish_run(..., status=COMPLETED|COMPLETED_NOOP)` on success.
4. Call `fail_run(..., failure_stage=...)` on any stage failure.

A failed run is a *status*, not a missing row. Every run, succeed or
fail, leaves exactly one `pipeline_runs` row and at least
`run_failed` / `batch_end` events in `ingestion_audit_log`.

Wiring into `APDSIngestionWorkflow` is intentionally NOT done in this PR
(engineer B lane is contract + tests). The next workflow change should:

- Insert `start_run` at the top of `run()`.
- Replace the existing `_log_run` best-effort call with `finish_run` /
  `fail_run` calls keyed off `pipeline.status`.
- Have the memory-store activity emit `audit_batch` per batch.

## Reader contract

Canonical readers should query the view, not the table:

```sql
SELECT id, content, source, metadata, file_hash, chunk_index, manifest_id
FROM   knowledge_vectors_canonical
WHERE  source_type = 'pudding_md';
```

The view excludes:

- Legacy / pre-v0.3 rows (no provenance triple).
- Rows produced by tools that bypass the writer.

This is the right behaviour: anything not produced by the documented
writer is not canonical by definition.

## Production cutover procedure

The migration's GRANT/REVOKE block is GUC-gated. Default = no-op.

**Approval gate.** Production cutover is an irreversible truth/world
commit. It requires Ewan's approval logged in
`00_authority/DECISION_LOG.md`.

**DBA procedure** (only after approval):

```sql
-- One PSQL session, superuser on amplified_brain:
SET app.allow_writer_v03_cutover = 'true';
\i 02_build/cove-orchestrator/db/migrations/007_writer_v03_provenance.sql

-- Verify
SELECT rolname FROM pg_roles WHERE rolname LIKE 'brain_%';
-- expect: brain_writer, brain_reader, brain_writer_pipeline
```

**Rollback.** The cutover only adds a role and grants — it does not
revoke from `brain_writer`. To roll back the new role:

```sql
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM brain_writer_pipeline;
DROP ROLE brain_writer_pipeline;
```

`brain_writer` continues to function during and after cutover. The
pipeline DSN should be switched to `brain_writer_pipeline` only after
all writer code paths use the v0.3 contract.

## What this lane compounds

This lane intentionally produces *contracts and tests*, not orchestration
changes. That gives downstream agents a sharper surface to work against:

- **Workflow re-wire (engineer A or future):** drop in `start_run` /
  `finish_run` / `audit_batch` and the live DB stops showing
  `pipeline_runs=0`.
- **Manifest builder (future):** must produce `ManifestRow`-shaped
  records. The dataclass refuses bad input at construction time, so a
  broken builder fails at the writer boundary, not silently in the DB.
- **Derived-entity step (future):** can be added as a new Temporal
  activity that reads from `knowledge_vectors_canonical` and writes to
  `entities` / `relationships`. The writer no longer competes with it.
- **Audit dashboards (future):** can be built directly against
  `pipeline_runs` and `ingestion_audit_log` — both load-bearing,
  both populated on every run.
- **Production cutover (Ewan-gated):** when approved, applying 007 with
  the GUC set is a one-liner; without the GUC the migration is safe to
  apply repeatedly in dev / staging.

## Bibliography

- `02_build/cove-orchestrator/temporal/activities/ingestion_activities.py` — current writer (path-derived ID, inline entity mutation).
- `02_build/cove-orchestrator/temporal/workflows/apds_ingestion_workflow.py` — workflow with best-effort `_log_run`.
- `02_build/cove-orchestrator/db/migrations/004_pipeline_runs_postgresql.sql` — `pipeline_runs` schema.
- `02_build/cove-orchestrator/db/migrations/005_brain_lockdown.sql` — existing `brain_writer` / `brain_reader` role split.
- `00_authority/DATA_ARCHITECTURE.md` — canonical data layer (`[SOURCE REQUIRED]` if missing in repo).
- Linear: `AMP-302` — Cove ingestion provenance.

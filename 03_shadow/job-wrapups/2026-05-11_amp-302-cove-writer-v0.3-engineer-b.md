---
status: complete
session_id: amp-302-engineer-b-2026-05-11
agent: Devin Engineer B
date: 2026-05-11
linear: AMP-302
branch: devin/AMP-302-cove-ingestion-provenance-engineer-b
---

# AMP-302 Cove Ingestion Provenance — Engineer B Wrap-up

## Lane

Canonical writer contract, telemetry, migrations, tests. (Engineer A is
expected to handle workflow re-wire / runtime cutover separately.)

## Doctrine applied

- **Disk = truth; Manifest = proof; DB = rebuildable index.**
- Compound Engineering: contracts + tests now → future ingestion work has
  a sharper surface and a safety net.
- Blinkers Without Ceilings: stayed in writer/telemetry/migration lane;
  did not touch workflow runtime or activity wiring.
- min-rule: one writer module, one telemetry module, one migration, three
  test files. No abstractions beyond what the contract needs.

## Findings (pre-change state)

1. `pipeline_runs = 0` and `audit_log = 0` in live DB despite rows in
   `knowledge_vectors`. Root cause: telemetry was best-effort
   (`try/except: warning`) and only fired at workflow end.
2. Writer in `temporal/activities/ingestion_activities.py:write_to_memory_stores`
   derives row IDs from `sha256(str(fp))[:32]` — path-dependent. Moving
   or renaming a file silently duplicates rows.
3. Same writer mutates `entities` inline. A re-ingest can rewrite graph
   edges without an audit boundary.
4. `relationships` table never written by any activity.
5. No `chunk_index` concept — the writer treats every file as one row,
   so large files have no chunk-level idempotency.

## Changes

| File | Type | Purpose |
|------|------|---------|
| `02_build/cove-orchestrator/temporal/activities/manifest_writer.py` | new | `ManifestRow` + deterministic ID + idempotent upsert |
| `02_build/cove-orchestrator/temporal/activities/ingestion_telemetry.py` | new | Load-bearing `pipeline_runs` + `ingestion_audit_log` writes |
| `02_build/cove-orchestrator/db/migrations/007_writer_v03_provenance.sql` | new | Provenance columns, canonical view, GUC-gated role split |
| `02_build/cove-orchestrator/tests/test_manifest_writer.py` | new | 19 tests — ID determinism, idempotency, provenance, no-inline-mutation |
| `02_build/cove-orchestrator/tests/test_ingestion_telemetry.py` | new | 10 tests — start/finish/fail, failure-as-status, audit |
| `02_build/cove-orchestrator/tests/test_writer_v03_migration.py` | new | 9 tests — migration text contracts, gated cutover |
| `02_build/cove-orchestrator/docs/ingestion-writer-v0.3.md` | new | Contract docs + cutover runbook |

## Tests run

```
$ python -m pytest tests/test_manifest_writer.py \
                    tests/test_ingestion_telemetry.py \
                    tests/test_writer_v03_migration.py -v
... 38 passed in 0.09s
```

The repo's existing `tests/test_polish_*` files fail on import because
`temporalio` is not installed in this sandbox — this is a pre-existing
environment limitation, not a regression. Skill-`coding-workflow` rule:
do not block on environment issues outside the change's lane.

## Production safety

- Migration is safe to apply repeatedly on dev/staging (idempotent).
- The `brain_writer_pipeline` role / `GRANT` block is wrapped in a
  `DO $$ ... $$` guard that no-ops unless
  `app.allow_writer_v03_cutover = 'true'` is set on the session.
- No `GRANT` / `REVOKE` outside that guarded block (asserted by
  `test_no_ungated_grant_revoke`).
- Production cutover procedure documented in
  `02_build/cove-orchestrator/docs/ingestion-writer-v0.3.md` —
  requires `00_authority/DECISION_LOG.md` entry from Ewan first.

## How this compounds future work

- **Workflow re-wire (next):** drop `start_run` / `finish_run` /
  `audit_batch` into `APDSIngestionWorkflow`; the live-DB observability
  gap closes.
- **Manifest builder (next):** must emit `ManifestRow`-shaped records.
  Bad input fails at construction, not silently in the DB.
- **Derived-entity activity (next):** can be a separate Temporal
  activity reading `knowledge_vectors_canonical` and writing
  `entities` / `relationships`. The writer is no longer in its way.
- **Dashboards / audit:** both `pipeline_runs` and
  `ingestion_audit_log` are now load-bearing and queryable.

## Open items (not in scope for engineer B)

- `APDSIngestionWorkflow` re-wire to call the new telemetry helpers.
- Replace the existing `write_to_memory_stores` activity with a
  manifest-consuming variant that delegates to `write_manifest_batch`.
- Decide and implement chunking strategy (currently `chunk_total = 1`
  for non-chunked files; the writer is already shaped for it).
- Production cutover (`app.allow_writer_v03_cutover = 'true'`) — gated
  on `DECISION_LOG.md` from Ewan.

## Signature

Devon-EngB | 2026-05-11 | AMP-302 | session amp-302-engineer-b-2026-05-11

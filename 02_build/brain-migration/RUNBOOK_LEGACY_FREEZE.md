---
title: Cove ingestion — legacy writer freeze, canonical rebuild, and approval-gated cutover
date: 2026-05-11
version: 1
status: candidate-authority
lane: AMP-302 engineer C
signed_by: Devon-AMP-302-C
linear: AMP-302
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

This runbook is the **operating contract** for everything that writes
into the canonical `amplified_brain` PostgreSQL store. It is read by:

- Future agents picking up an ingestion task — start here before
  touching any writer or migration script.
- Operators (Ewan) when approving a production cutover.
- PR reviewers asked "is this writer allowed to exist?"

If this runbook conflicts with a script's docstring or a chat message,
**this runbook wins**. If you need to change the policy, update this
file first, get sign-off, then change code.

## Doctrine alignment

- **Compound Engineering** (Plan → Work → Review → Compound). Every
  ingestion run produces an after-action note via the template at
  `02_build/cove-orchestrator/docs/COMPOUND_ENGINEERING_AFTER_ACTION_TEMPLATE.md`.
- **Blinkers Without Ceilings.** Narrow scope (Cove ingestion only) but
  no artificial cap on quality of the controls.
- **Min-rule.** Fewest possible writers; one canonical writer; everything
  else is frozen by default.

## The writer landscape (as of 2026-05-11)

| Writer | Path | Status | What it does |
|--------|------|--------|--------------|
| **CANONICAL** | `02_build/cove-orchestrator/temporal/activities/ingestion_activities.py::write_to_memory_stores` | LIVE | Upserts PUDDING-labelled files into `knowledge_vectors` + `entities` inside a Temporal activity. Manifest-first; deterministic IDs; observable in `pipeline_runs`. |
| Legacy ETL (vectors) | `02_build/brain-migration/migrate_qdrant.py` | FROZEN | One-shot Qdrant → Postgres dump that produced the original 57,297 vectors. Guarded fail-closed by `migration_guard`. |
| Legacy ETL (graph) | `02_build/brain-migration/migrate_falkordb.py` | FROZEN | Bulk CSV COPY into entities/episodes/relationships with destructive `DELETE FROM ...` and superuser-style access. Guarded fail-closed by `migration_guard`. |
| Side door | `02_build/brain-migration/brain_mcp_server.py` (write tools when `ALLOW_WRITES=true`) | HARDENED | Was a free side door; now requires `BRAIN_MCP_WRITE_ACK` token AND staging flag for canonical DB. Defaults closed. |
| Out-of-tree | `/opt/amplified/clean-build-pipeline/.../memory_writer.py` | DRIFT-RISK | Lives outside this repo. **Must not be assumed canonical.** Treat as quarantined until inspected against the canonical writer's invariants. |

## Operating rules (read me before you touch anything)

1. **Default to the canonical writer.** Any new ingestion should be
   expressed as a Temporal activity that reuses or extends
   `write_to_memory_stores`, not a one-shot script.
2. **Never resurrect a frozen writer for routine work.** The guards
   are not a hurdle to be cleared — they exist because reruns have
   produced duplicates and drift.
3. **Side-door retirement.** `brain_mcp_server.py` write tools are
   permitted only against a staging copy of the DB. If you find
   yourself writing to `amplified_brain` through the MCP server, stop
   and route it through the Temporal workflow.
4. **No mutation without provenance.** Every row landing in
   `amplified_brain` must carry `metadata.taxonomy_version` and a
   deterministic ID derived from stable inputs.
5. **No destructive ops in steady state.** `DELETE FROM`, `TRUNCATE`,
   `ALTER TABLE … DROP CONSTRAINT` against `amplified_brain` happen
   only inside the migration protocol below.

## Migration protocol (the only way to run a frozen writer)

If — and only if — Ewan has approved a re-migration (e.g. corruption
recovery, schema overhaul), the operator does the following:

1. **Plan**. Open a PR that adds an entry to
   `00_authority/DECISION_LOG.md` describing why a rerun is needed and
   what the target state looks like.
2. **Stage**. Bring up a staging Postgres named anything other than
   `amplified_brain`, or override `DB_NAME` so the legacy script
   targets a non-canonical name.
3. **Dry-run on staging first.** Set:
   ```
   export AMPLIFIED_MIGRATION_PROTOCOL=AMP-302-MIGRATION-PROTOCOL-2026-05-11
   export AMPLIFIED_MIGRATION_TARGET_DB=amplified_brain_staging
   export AMPLIFIED_MIGRATION_OPERATOR=<your-agent-id>
   ```
   Run the legacy script. Capture row counts + a diff against the
   current canonical DB.
4. **Production cutover (approval-gated).** Only after Ewan has signed
   off on the dry-run diff, run against canonical with the canonical
   ack:
   ```
   export AMPLIFIED_MIGRATION_PROTOCOL=AMP-302-MIGRATION-PROTOCOL-2026-05-11
   export AMPLIFIED_MIGRATION_TARGET_DB=amplified_brain
   export AMPLIFIED_MIGRATION_OPERATOR=<your-agent-id>
   export AMPLIFIED_MIGRATION_ACK_CANONICAL=YES-I-KNOW-AMPLIFIED_BRAIN-IS-CANONICAL
   ```
5. **After-action.** File the after-action note using the template
   below (see § After-action) before declaring done.

### Token rotation

`MIGRATION_PROTOCOL_TOKEN` and `BRAIN_MCP_WRITE_ACK_TOKEN` are rotated
each time a cutover completes. Bump the date suffix in
`migration_guard.py` and `brain_mcp_write_guard.py`, commit, and link
to the rotation in the decision log entry.

## Side-door retirement plan

Targets after AMP-302:

- `brain_mcp_server.py`: keep the read API (`brain_reader` role)
  indefinitely. Remove the write endpoints once the Temporal workflow
  covers every legitimate use case (target ≤ 60 days). Track the
  remaining write-tool callers in the Linear ticket.
- `migrate_qdrant.py` / `migrate_falkordb.py`: candidates for
  relocation to `90_archive/` once the canonical DB is stable for a
  full quarter. Until then, freeze in place so the rollback story
  remains intact.
- `/opt/amplified/.../memory_writer.py`: inspect against the
  canonical writer's invariants. If it drifts, either bring it inside
  the repo as a Temporal activity or shut it down. **Do not** treat
  the out-of-tree file as canonical even if it is what is currently
  running.

## Approval-gated production cutover (full checklist)

Use this checklist when a rerun against `amplified_brain` is
unavoidable.

- [ ] Decision log entry merged on `main` with `DECISION REQUIRED`
      resolved.
- [ ] Staging dry-run completed; row-count delta within tolerance and
      pasted into the decision log.
- [ ] Backup of canonical DB taken (pg_dump or volume snapshot) and
      verified restorable.
- [ ] Operator identifies themselves via `AMPLIFIED_MIGRATION_OPERATOR`.
- [ ] All four protocol env vars set; canonical ack present.
- [ ] Cutover window communicated; downstream consumers paused or in
      degraded-read mode.
- [ ] After-action filed within 24h of cutover.
- [ ] Protocol token rotated; previous token recorded as `RETIRED`.

## Future-agent operating rules

If you are an agent picking up an ingestion task in this repo:

1. **Read this file first.** If you cannot find it, stop and ask.
2. **Do not bypass the guards.** If a test starts blocking you, the
   correct fix is almost always to route your write through the
   canonical activity, not to weaken the guard.
3. **If you need a new writer**, justify it in a decision-log entry
   and bring it under the same fail-closed contract.
4. **Record after-actions** using the template at
   `02_build/cove-orchestrator/docs/COMPOUND_ENGINEERING_AFTER_ACTION_TEMPLATE.md`.
   Skipping the after-action is how this drift happened in the first
   place.

## Related files

- `02_build/brain-migration/migration_guard.py` — the shared
  fail-closed guard.
- `02_build/brain-migration/brain_mcp_write_guard.py` — side-door
  resolver, broken out so it is unit-testable.
- `02_build/brain-migration/tests/` — tests that prove the guards
  block; CI must keep these green.
- `02_build/cove-orchestrator/temporal/activities/ingestion_activities.py`
  — the canonical writer.
- `02_build/cove-orchestrator/docs/COMPOUND_ENGINEERING_AFTER_ACTION_TEMPLATE.md`
  — after-action template (see below).

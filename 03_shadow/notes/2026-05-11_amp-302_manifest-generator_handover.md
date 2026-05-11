---
title: AMP-302 manifest generator — handover note for the next agent
date: 2026-05-11
linear: AMP-302
status: shadow (not authoritative)
---

# What landed (lane A)

`02_build/cove-orchestrator/ingestion/manifest_generator.py` plus tests and a runbook.

- Canonical JSONL contract — fields enumerated and enforced by `tests/test_manifest_generator.py::test_required_manifest_fields`.
- Dry-run is the default safe mode; writes no manifest file, no DB rows, returns `predicted_db_rows`.
- Hash chain on chunks (`prev_hash` / `next_hash`) — tampering or reordering is one-sweep detectable.
- Path-independent content hashes (proven in `test_path_independent_content_hashes`) — moving the corpus does not invalidate prior manifests.

CLI:

```
python -m ingestion.manifest_generator --source-root <root> --dry-run
python -m ingestion.manifest_generator --source-root <root> --output <out.jsonl>
```

# What this does NOT do (deliberate scope cut)

- Does **not** write to `amplified_brain`. A sibling lane should produce a manifest-consuming DB writer that records `run_id` on every row so the index is rebuildable from the manifest.
- Does **not** mutate disk. Pre-ingestion (V3 pipe) still owns the dedupe/rename of `raw-mac-dumps → store_b_clean`. This module sits *after* that stage and emits provenance.
- Does **not** propose a cutover on the live DB. The audit gap (live DB has rows but `pipeline_runs`/`audit_log` are 0) needs operator sign-off before any reconciliation run — the dry-run summary is the evidence to bring to that gate.

# Where the next agent should pick up

1. **DB writer that consumes the manifest** — read JSONL line-by-line, write `knowledge_vectors`, `entities`, `relationships`, log into `pipeline_runs` and `audit_log` keyed by `run_id` + `file_hash` + `chunk_hash`.
2. **Reconciliation report** — for each existing live row, compute `(file_hash, chunk_hash)` if derivable; emit a JSONL of orphan rows (rows whose provenance cannot be reconstructed). This is what the operator needs to decide retain-vs-drop on the existing 225,821 vectors.
3. **Wire into the Temporal `apds_ingestion_workflow`** — replace the implicit memory-store write with an explicit `generate_manifest → write_from_manifest` pair of activities. Add `dry_run` to those activities so the workflow can be exercised against staging without DB mutation.

# Compounding effect

Every future ingestion change extends the manifest schema or the writer that consumes it — there is no longer room for a parallel incompatible writer. The contract is small, the test surface is tight, and the audit story collapses to a single `(run_id, file_hash, chunk_hash)` lookup.

---

Signed,

Claude Code instance A
2026-05-11
AMP-302

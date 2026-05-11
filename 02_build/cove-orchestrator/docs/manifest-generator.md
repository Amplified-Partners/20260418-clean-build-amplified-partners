---
title: Canonical Manifest Generator — Runbook (AMP-302)
date: 2026-05-11
version: 1
status: shadow → candidate
linear: AMP-302
---

# Canonical manifest generator

The manifest generator is the truth-shaped boundary between the clean disk corpus and `amplified_brain`.

**Doctrine recap**

- Disk source material = **truth**.
- The manifest JSONL = **proof** (signed, hash-chained, deterministic).
- The DB = **rebuildable / searchable index** over the manifest. Never the source of truth.

## What it does

Walks a `source_root` (default target: `/opt/amplified/archive/store_b_clean` on Beast), produces one JSONL record per source file containing:

- `run_id`, `pipeline_version` (`amplified-pipeline-v0.3`), `source_root`
- `file_path` (relative), `file_hash` (SHA-256 of bytes), `size_bytes`, `mtime`
- `chunks[]` — one entry per chunk window with: `idx`, `chunk_hash`, `line_start`, `line_end`, `parent_heading`, `chunk_type`, `prev_hash`, `next_hash`
- `signed_by` = `brain_writer_pipeline`, `created_at` (ISO UTC)

The chunk hash chain (`prev_hash` / `next_hash`) makes any missing or reordered chunk detectable by a single sweep.

## Why now

The live DB has 225,821 `knowledge_vectors`, 53,959 `entities`, 34,488 `relationships`, 4,257 `episodes`, but `pipeline_runs`, `audit_log`, `pudding_labels` all read **0**. The existing on-disk writer does not explain the rows that are there — multiple incompatible historic writers produced them. AMP-302 narrows the contract so every future row is attributable to one signed manifest.

## Usage

### Dry-run (default for any unapproved environment)

Writes **no manifest file**, makes **no DB calls**. Returns predicted row counts.

```
python -m ingestion.manifest_generator \
    --source-root /opt/amplified/archive/store_b_clean \
    --dry-run
```

Output (example):

```json
{
  "chunk_count": 412988,
  "file_count": 21606,
  "predicted_db_rows": {
    "audit_log": 21606,
    "knowledge_vectors": 412988,
    "pipeline_runs": 1
  },
  "dry_run": true,
  "manifest_path": null,
  "pipeline_version": "amplified-pipeline-v0.3",
  "run_id": "...",
  "signed_by": "brain_writer_pipeline",
  "source_root": "/opt/amplified/archive/store_b_clean"
}
```

### Authoritative run (manifest only, no DB writes)

```
python -m ingestion.manifest_generator \
    --source-root /opt/amplified/archive/store_b_clean \
    --output /opt/amplified/manifests/$(date -u +%Y%m%dT%H%M%SZ).jsonl
```

The DB writer is a separate concern and is **not invoked** by this tool. The manifest is the artefact that a DB writer must consume; that contract makes provenance enforceable.

## Approval gate for production cutover

Production DB cutover is out of scope for AMP-302 and **must not** be performed by this tool. The approved procedure is:

1. Operator (Ewan) signs off on a dry-run summary (`predicted_db_rows`) for the target `source_root`.
2. The manifest is generated to a `manifests/` path under `/opt/amplified/`.
3. A separate, reviewed DB writer (out of scope here — to be wired in a sibling Linear) consumes the manifest, writes rows, and records its `run_id` in `pipeline_runs`. Every written row carries the same `run_id` so the manifest can be re-derived for audit.
4. `audit_log` gets one row per file ingested, citing the manifest record by `file_hash`.

Until that DB writer lands, the manifest generator is the only authoritative writer of provenance evidence on disk.

## Determinism contract

- Same bytes + same `--chunk-lines` ⇒ same `file_hash`, same chunk hash sequence, regardless of on-disk location. Tested in `tests/test_manifest_generator.py::test_path_independent_content_hashes`.
- `run_id` and `created_at` are intentionally non-deterministic — they identify a *run*, not the content.

## How this lane compounds

- **Plan**: a single contract every future writer must satisfy. No more parallel incompatible writers.
- **Work**: drop-in for the existing pre-ingestion pipe; sits above the dedupe stage as the provenance emitter.
- **Review**: any DB row can be linked back to a manifest record via `(run_id, file_hash, chunk_hash)`. Audit goes from impossible to one-shot.
- **Compound**: downstream PUDDING labeller and embedding writer consume the manifest instead of re-walking the disk. Future ingestion features (incremental, partial, multi-source) extend the schema rather than fork a new writer.

---

Signed,

Claude Code instance A
2026-05-11
AMP-302

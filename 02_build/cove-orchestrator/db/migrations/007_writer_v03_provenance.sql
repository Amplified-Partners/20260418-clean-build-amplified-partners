-- Migration 007: Writer v0.3 — Manifest-First Provenance (AMP-302)
--
-- Adds strict provenance metadata to ingestion target tables, a canonical
-- view that exposes only manifest-backed rows, and a draft pipeline-writer
-- role split from the existing brain_writer.
--
-- Target database: amplified_brain (via BRAIN_DSN)
-- Depends on: 005_brain_lockdown.sql (role grants pattern), 004_pipeline_runs_postgresql.sql
--
-- Doctrine: "Disk source material = truth; Manifest = proof;
--           DB = rebuildable/searchable index."
--
-- Engineer B / AMP-302 / 2026-05-11
--
-- ─────────────────────────────────────────────────────────────────────────────
-- IMPORTANT: PRODUCTION CUTOVER IS GATED.
--
-- This file is *idempotent and safe to apply* on a fresh database. The
-- bottom section (`-- ── PRODUCTION CUTOVER (DO NOT EXECUTE UNGATED) ──`)
-- is wrapped in a DO-block guard that no-ops unless the explicit
-- `app.allow_writer_v03_cutover` GUC is set to 'true' on the session.
--
-- To apply on production:
--   1) Ewan approves in DECISION_LOG.md.
--   2) DBA runs `SET app.allow_writer_v03_cutover = 'true';` then `\i 007_*.sql`.
--   3) Verify with `select * from pg_roles where rolname like 'brain_%'`.
--
-- Do not run with that GUC set unless authorised.
-- ─────────────────────────────────────────────────────────────────────────────

-- ─── Provenance columns on knowledge_vectors ────────────────────────────────
-- file_hash      : sha256 of the source file's bytes (NOT path)
-- chunk_index    : 0-based chunk number within that file (0 if not chunked)
-- chunk_total    : total chunks the file was split into (1 if not chunked)
-- manifest_id    : opaque manifest row id this insert was caused by
-- writer_version : code version of the writer that produced the row
-- ingested_at    : when this row was last (re)written
ALTER TABLE IF EXISTS knowledge_vectors
    ADD COLUMN IF NOT EXISTS file_hash       TEXT,
    ADD COLUMN IF NOT EXISTS chunk_index     INT DEFAULT 0,
    ADD COLUMN IF NOT EXISTS chunk_total     INT DEFAULT 1,
    ADD COLUMN IF NOT EXISTS manifest_id     TEXT,
    ADD COLUMN IF NOT EXISTS writer_version  TEXT,
    ADD COLUMN IF NOT EXISTS ingested_at     TIMESTAMPTZ DEFAULT now();

CREATE INDEX IF NOT EXISTS idx_kv_file_hash
    ON knowledge_vectors (file_hash);
CREATE INDEX IF NOT EXISTS idx_kv_manifest_id
    ON knowledge_vectors (manifest_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_kv_filehash_chunk
    ON knowledge_vectors (file_hash, chunk_index)
    WHERE file_hash IS NOT NULL;

-- ─── Audit table for batch-level ingestion events ───────────────────────────
-- Distinct from cove's own audit_log; this lives in amplified_brain so a
-- reader can correlate ingestion events with the actual rows produced.
CREATE TABLE IF NOT EXISTS ingestion_audit_log (
    id              BIGSERIAL PRIMARY KEY,
    run_id          TEXT NOT NULL,
    event_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    event           TEXT NOT NULL,       -- 'batch_start' | 'batch_end' | 'row_failed' | 'run_start' | 'run_end'
    stage           TEXT,                -- 'ingestion' | 'pudding' | 'memory_store' | 'derive_entities'
    batch_index     INT,
    batch_size      INT,
    rows_written    INT,
    rows_skipped    INT,
    rows_failed     INT,
    details         JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_ial_run_id    ON ingestion_audit_log (run_id);
CREATE INDEX IF NOT EXISTS idx_ial_event     ON ingestion_audit_log (event);
CREATE INDEX IF NOT EXISTS idx_ial_event_at  ON ingestion_audit_log (event_at DESC);

-- ─── Canonical view: only manifest-backed rows ──────────────────────────────
-- Readers should query this view, not knowledge_vectors directly. Rows
-- without (file_hash, manifest_id, writer_version) are excluded; they are
-- legacy / pre-v0.3 rows that have not been re-derived through the manifest.
CREATE OR REPLACE VIEW knowledge_vectors_canonical AS
SELECT
    id,
    content,
    source,
    source_type,
    embedding,
    metadata,
    file_hash,
    chunk_index,
    chunk_total,
    manifest_id,
    writer_version,
    ingested_at,
    created_at,
    updated_at
FROM knowledge_vectors
WHERE file_hash      IS NOT NULL
  AND manifest_id    IS NOT NULL
  AND writer_version IS NOT NULL;

COMMENT ON VIEW knowledge_vectors_canonical IS
  'Manifest-backed rows only. Pre-v0.3 rows without provenance are excluded. See AMP-302.';

-- ─── Optional CHECK: provenance metadata shape on new rows ──────────────────
-- We deliberately do NOT enforce NOT NULL on knowledge_vectors.file_hash yet
-- because legacy rows exist. A future migration (008) tightens this.
-- This CHECK only fires when the column is set: writer_version must look
-- like 'v0.3' or higher.
ALTER TABLE knowledge_vectors
    DROP CONSTRAINT IF EXISTS ck_kv_writer_version_format;
ALTER TABLE knowledge_vectors
    ADD CONSTRAINT ck_kv_writer_version_format
        CHECK (writer_version IS NULL OR writer_version ~ '^v[0-9]+\.[0-9]+');

-- ─── Status column index on pipeline_runs for failure-state queries ─────────
CREATE INDEX IF NOT EXISTS idx_pipeline_runs_failed
    ON pipeline_runs (status)
    WHERE status LIKE 'failed_%';

-- ── PRODUCTION CUTOVER (DO NOT EXECUTE UNGATED) ─────────────────────────────
-- Wrapped in a guard. If the session GUC `app.allow_writer_v03_cutover` is
-- not 'true', this is a no-op. Approval procedure documented at the top of
-- this file and in 02_build/cove-orchestrator/docs/ingestion-writer-v0.3.md.
DO $$
DECLARE
    allow_cutover TEXT := current_setting('app.allow_writer_v03_cutover', true);
BEGIN
    IF allow_cutover IS DISTINCT FROM 'true' THEN
        RAISE NOTICE 'Skipping production cutover. Set app.allow_writer_v03_cutover=true to apply.';
        RETURN;
    END IF;

    -- New role: brain_writer_pipeline, restricted to ingestion writer use.
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'brain_writer_pipeline') THEN
        CREATE ROLE brain_writer_pipeline LOGIN;
    END IF;

    -- The pipeline role gets INSERT/UPDATE only on knowledge_vectors and on
    -- the audit/run tables. It does NOT receive write on entities or
    -- relationships — those flow from a separate derived-step writer.
    GRANT CONNECT ON DATABASE amplified_brain TO brain_writer_pipeline;
    GRANT USAGE ON SCHEMA public TO brain_writer_pipeline;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO brain_writer_pipeline;

    GRANT INSERT, UPDATE ON TABLE knowledge_vectors    TO brain_writer_pipeline;
    GRANT INSERT, UPDATE ON TABLE pipeline_runs        TO brain_writer_pipeline;
    GRANT INSERT         ON TABLE ingestion_audit_log  TO brain_writer_pipeline;
    GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO brain_writer_pipeline;
END
$$;

-- Migration 004: Pipeline Runs — repointed to amplified_brain (AMP-279)
-- Replaces Qdrant/FalkorDB metric columns with PostgreSQL equivalents.
--
-- Target database: amplified_brain (via BRAIN_DSN)
-- Signed-by: Devon-a4e2 | 2026-05-09 | devin-a4e23461f626488aaf493c55d0c87924

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id              TEXT PRIMARY KEY,
    started_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    ingestion_new_files INT NOT NULL DEFAULT 0,
    ingestion_total_unique INT NOT NULL DEFAULT 0,
    ingestion_elapsed   REAL NOT NULL DEFAULT 0,
    pudding_labelled    INT NOT NULL DEFAULT 0,
    pudding_skipped     INT NOT NULL DEFAULT 0,
    pudding_errors      INT NOT NULL DEFAULT 0,
    memory_pg_vectors   INT NOT NULL DEFAULT 0,
    memory_pg_entities  INT NOT NULL DEFAULT 0,
    memory_errors       INT NOT NULL DEFAULT 0,
    completed_at        TIMESTAMPTZ,
    status              TEXT NOT NULL DEFAULT 'running'
);

CREATE INDEX IF NOT EXISTS idx_pipeline_runs_started
    ON pipeline_runs (started_at DESC);

CREATE INDEX IF NOT EXISTS idx_pipeline_runs_status
    ON pipeline_runs (status)
    WHERE status != 'completed';

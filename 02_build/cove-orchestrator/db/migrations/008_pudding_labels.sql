-- Migration 008: PUDDING extraction → PostgreSQL+AGE+pgvector (AMP-345)
--
-- Creates the pudding_labels table for storing PUDDING taxonomy extraction
-- results with full provenance, tier tagging, and expiry.
-- Creates the business_brain Apache AGE graph for Document nodes.
--
-- Non-negotiable fields per Brain Architecture v3, §6:
--   - epistemic_tier (defaults to INTUITED)
--   - source_agent, source_session, source_model, ingest_timestamp (provenance)
--   - valid_until (expiry per content type)
--
-- Run as superuser on the amplified_brain database.
--
-- Signed-by: Devon-86e7 | 2026-05-15 | devin-86e7ca10cd27467baff9669b1d7113b5

BEGIN;

-- ═══════════════════════════════════════════════════════════════════════
-- 1. PUDDING labels table — one row per labelled file
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS pudding_labels (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_hash       TEXT NOT NULL,
    file_path       TEXT NOT NULL,
    file_name       TEXT NOT NULL DEFAULT '',

    -- PUDDING 2026 taxonomy (5 dimensions + confidence)
    what            TEXT NOT NULL DEFAULT 'UNKNOWN',
    how             TEXT NOT NULL DEFAULT 'UNKNOWN',
    scale           TEXT NOT NULL DEFAULT 'UNKNOWN',
    time_dim        TEXT NOT NULL DEFAULT 'UNKNOWN',
    pattern         TEXT NOT NULL DEFAULT 'UNKNOWN',
    confidence      REAL NOT NULL DEFAULT 0.0,

    -- Tier tagging (Brain Architecture v3, §6)
    epistemic_tier  TEXT NOT NULL DEFAULT 'INTUITED',

    -- Provenance (Brain Architecture v3, §6)
    source_agent    TEXT NOT NULL,
    source_session  TEXT NOT NULL,
    source_model    TEXT NOT NULL,
    ingest_timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Expiry (Brain Architecture v3, §6)
    valid_until     TIMESTAMPTZ,

    -- Pipeline metadata
    run_id          TEXT NOT NULL,
    signed_by       TEXT NOT NULL DEFAULT 'pudding_extractor',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Idempotency: one label per file_hash per run
    CONSTRAINT uq_pudding_labels_file_hash UNIQUE (file_hash)
);

CREATE INDEX IF NOT EXISTS idx_pudding_labels_file_hash ON pudding_labels (file_hash);
CREATE INDEX IF NOT EXISTS idx_pudding_labels_tier ON pudding_labels (epistemic_tier);
CREATE INDEX IF NOT EXISTS idx_pudding_labels_valid_until ON pudding_labels (valid_until);
CREATE INDEX IF NOT EXISTS idx_pudding_labels_run_id ON pudding_labels (run_id);
CREATE INDEX IF NOT EXISTS idx_pudding_labels_what ON pudding_labels (what);
CREATE INDEX IF NOT EXISTS idx_pudding_labels_pattern ON pudding_labels (pattern);

-- ═══════════════════════════════════════════════════════════════════════
-- 2. Apache AGE — business_brain graph
-- ═══════════════════════════════════════════════════════════════════════

CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM ag_catalog.ag_graph WHERE name = 'business_brain') THEN
        PERFORM create_graph('business_brain');
    END IF;
END $$;

-- Vertex labels
SELECT create_vlabel('business_brain', 'Document');
SELECT create_vlabel('business_brain', 'Concept');

-- Edge labels
SELECT create_elabel('business_brain', 'HAS_LABEL');
SELECT create_elabel('business_brain', 'BRIDGES');

-- Reset search_path
SET search_path = "$user", public;

-- ═══════════════════════════════════════════════════════════════════════
-- 3. Role grants
-- ═══════════════════════════════════════════════════════════════════════

DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'brain_writer') THEN
        GRANT INSERT, UPDATE ON TABLE pudding_labels TO brain_writer;
        GRANT USAGE ON SCHEMA ag_catalog TO brain_writer;
    END IF;

    IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'brain_reader') THEN
        GRANT SELECT ON TABLE pudding_labels TO brain_reader;
        GRANT USAGE ON SCHEMA ag_catalog TO brain_reader;
    END IF;
END $$;

-- ═══════════════════════════════════════════════════════════════════════
-- 4. Updated_at trigger
-- ═══════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION update_pudding_labels_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_pudding_labels_updated_at ON pudding_labels;
CREATE TRIGGER trg_pudding_labels_updated_at
    BEFORE UPDATE ON pudding_labels
    FOR EACH ROW EXECUTE FUNCTION update_pudding_labels_updated_at();

COMMIT;

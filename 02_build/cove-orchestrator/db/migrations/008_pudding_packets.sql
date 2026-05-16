-- Migration 008: PUDDING 20-Field Packets + business_brain AGE graph (AMP-356)
--
-- Creates the pudding_packets table with all 20 queryable fields (5 PUDDING
-- dimensions exposed individually), plus recurrence_count and bridge_terms
-- for spiral detection and Swanson cross-domain joins.
--
-- Also creates the business_brain AGE graph for knowledge graph traversal.
--
-- Target database: amplified_brain (via BRAIN_DSN)
-- Depends on: 007_canonical_schema_v0.3.sql
-- Signed-by: Devon-cb28 | 2026-05-16 | devin-cb283993cf974c7babc3307e140d63e4

BEGIN;

-- ═══════════════════════════════════════════════════════════════════════
-- 1. PUDDING Packets — the 20-field canonical record
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS pudding_packets (
    -- Identity
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_hash           TEXT NOT NULL,
    file_path           TEXT NOT NULL,
    filename            TEXT NOT NULL,

    -- PUDDING label (5-char: WHAT.HOW.SCALE.TIME.PATTERN)
    pudding_label       TEXT NOT NULL,               -- full label e.g. "M.=.4.∞.LOG-CAU"
    pudding_code        TEXT NOT NULL,               -- compressed 4-char e.g. "MS4T"

    -- 5 dimensions — individually queryable
    dim_what            CHAR(1) NOT NULL,            -- E/R/P/S/C/I/M
    dim_how             CHAR(1) NOT NULL,            -- +/-/~/>/=/!/? (stored as A/D/O/T/S/X/E in compressed)
    dim_scale           CHAR(1) NOT NULL,            -- 0/1/2/3/4/5/6
    dim_time            TEXT NOT NULL,               -- i/s/m/l/p/inf/v
    dim_pattern         TEXT,                        -- LOG-CAU, MAT-EXG, SYS-RFL etc. (nullable)

    -- AI-enriched fields (light LLM pass)
    confidence          REAL CHECK (confidence >= 0 AND confidence <= 1),
    canonical_summary   TEXT,                        -- AI-generated 1-line summary
    claim_type          TEXT,                        -- principle|framework|sop|technique|case_study|hypothesis|recipe|content_asset|business_logic|raw_notes
    evidence_summary    TEXT,                        -- AI-generated evidence summary

    -- Discovery fields
    bridge_terms        TEXT[] DEFAULT '{}',          -- terms for Swanson cross-domain joins
    recurrence_count    INT NOT NULL DEFAULT 1,       -- for spiral detection (Danger)

    -- Provenance
    word_count          INT NOT NULL DEFAULT 0,
    source_agent        TEXT NOT NULL DEFAULT 'deterministic-labeler-v2',
    run_id              TEXT NOT NULL,
    signed_by           TEXT NOT NULL DEFAULT 'brain_writer_pipeline',
    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Dedup constraint
    UNIQUE (file_hash)
);

-- ═══════════════════════════════════════════════════════════════════════
-- 2. Indexes — dimension slicing, discovery, provenance
-- ═══════════════════════════════════════════════════════════════════════

-- Individual dimension queries (the whole point of exposing 5 dims)
CREATE INDEX IF NOT EXISTS idx_pp_dim_what ON pudding_packets (dim_what);
CREATE INDEX IF NOT EXISTS idx_pp_dim_how ON pudding_packets (dim_how);
CREATE INDEX IF NOT EXISTS idx_pp_dim_scale ON pudding_packets (dim_scale);
CREATE INDEX IF NOT EXISTS idx_pp_dim_time ON pudding_packets (dim_time);
CREATE INDEX IF NOT EXISTS idx_pp_dim_pattern ON pudding_packets (dim_pattern)
    WHERE dim_pattern IS NOT NULL;

-- Composite: full PUDDING code for cross-domain matching
CREATE INDEX IF NOT EXISTS idx_pp_pudding_code ON pudding_packets (pudding_code);

-- Discovery: bridge terms (GIN for array containment queries)
CREATE INDEX IF NOT EXISTS idx_pp_bridge_terms ON pudding_packets USING GIN (bridge_terms);

-- Spiral detection
CREATE INDEX IF NOT EXISTS idx_pp_recurrence ON pudding_packets (recurrence_count DESC)
    WHERE recurrence_count > 1;

-- Provenance
CREATE INDEX IF NOT EXISTS idx_pp_run_id ON pudding_packets (run_id);
CREATE INDEX IF NOT EXISTS idx_pp_ingested_at ON pudding_packets (ingested_at DESC);
-- idx_pp_file_hash omitted — UNIQUE (file_hash) already creates a B-tree index

-- Claim type filtering
CREATE INDEX IF NOT EXISTS idx_pp_claim_type ON pudding_packets (claim_type)
    WHERE claim_type IS NOT NULL;

-- ═══════════════════════════════════════════════════════════════════════
-- 3. business_brain AGE graph
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
DO $$ BEGIN PERFORM create_vlabel('business_brain', 'Document'); EXCEPTION WHEN OTHERS THEN NULL; END $$;
DO $$ BEGIN PERFORM create_vlabel('business_brain', 'Concept'); EXCEPTION WHEN OTHERS THEN NULL; END $$;
DO $$ BEGIN PERFORM create_vlabel('business_brain', 'Domain'); EXCEPTION WHEN OTHERS THEN NULL; END $$;
DO $$ BEGIN PERFORM create_vlabel('business_brain', 'Pattern'); EXCEPTION WHEN OTHERS THEN NULL; END $$;

-- Edge labels
DO $$ BEGIN PERFORM create_elabel('business_brain', 'HAS_CONCEPT'); EXCEPTION WHEN OTHERS THEN NULL; END $$;
DO $$ BEGIN PERFORM create_elabel('business_brain', 'IN_DOMAIN'); EXCEPTION WHEN OTHERS THEN NULL; END $$;
DO $$ BEGIN PERFORM create_elabel('business_brain', 'EXHIBITS_PATTERN'); EXCEPTION WHEN OTHERS THEN NULL; END $$;
DO $$ BEGIN PERFORM create_elabel('business_brain', 'BRIDGES_TO'); EXCEPTION WHEN OTHERS THEN NULL; END $$;

SET search_path = "$user", public;

-- ═══════════════════════════════════════════════════════════════════════
-- 4. Audit log — reuses existing table from 001_initial_schema.sql
-- ═══════════════════════════════════════════════════════════════════════

-- audit_log already exists (001) with columns:
--   (actor, action, resource_type, resource_id, details, task_id)
-- No schema changes needed.  The ingestion pipeline writes via:
--   INSERT INTO audit_log (actor, action, resource_type, resource_id, details)
--   VALUES ($1, $2, $3, $4, $5::jsonb)

-- ═══════════════════════════════════════════════════════════════════════
-- 5. Updated_at trigger
-- ═══════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION update_pudding_packet_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER pudding_packets_updated_at
    BEFORE UPDATE ON pudding_packets
    FOR EACH ROW EXECUTE FUNCTION update_pudding_packet_updated_at();

-- ═══════════════════════════════════════════════════════════════════════
-- 6. Role grants
-- ═══════════════════════════════════════════════════════════════════════

DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'brain_writer') THEN
        GRANT INSERT, UPDATE ON TABLE pudding_packets TO brain_writer;
        GRANT INSERT ON TABLE audit_log TO brain_writer;
        GRANT USAGE ON SCHEMA ag_catalog TO brain_writer;
    END IF;

    IF EXISTS (SELECT FROM pg_roles WHERE rolname = 'brain_reader') THEN
        GRANT SELECT ON TABLE pudding_packets TO brain_reader;
        GRANT SELECT ON TABLE audit_log TO brain_reader;
        GRANT USAGE ON SCHEMA ag_catalog TO brain_reader;
    END IF;
END $$;

-- ═══════════════════════════════════════════════════════════════════════
-- 7. Update pipeline_runs to track v2 metrics
-- ═══════════════════════════════════════════════════════════════════════

ALTER TABLE pipeline_runs
    ADD COLUMN IF NOT EXISTS pudding_packets_written INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS pudding_ai_enriched INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS pudding_bridge_terms_found INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS pipeline_version TEXT NOT NULL DEFAULT 'v1';

COMMIT;

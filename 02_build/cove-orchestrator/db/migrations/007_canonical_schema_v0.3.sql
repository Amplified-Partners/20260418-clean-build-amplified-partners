-- Migration 007: Canonical ingestion schema v0.3 (AMP-302)
--
-- Freezes legacy brain tables, creates canonical tables with full provenance,
-- defines consumer views, and extends role grants.
--
-- Run as superuser on the amplified_brain database.
-- Rollback: run 007_rollback.sql (renames back, drops views).
--
-- Signed-by: Devon-0de2 | 2026-05-11 | devin-0de27df281514f96ba3921354d7c31ae

BEGIN;

-- ═══════════════════════════════════════════════════════════════════════
-- 1. Freeze legacy tables (rename, not delete — zero data loss)
-- ═══════════════════════════════════════════════════════════════════════

ALTER TABLE IF EXISTS knowledge_vectors
    RENAME TO knowledge_vectors_legacy_2026_05_10;

ALTER TABLE IF EXISTS entities
    RENAME TO entities_legacy_2026_05_10;

ALTER TABLE IF EXISTS relationships
    RENAME TO relationships_legacy_2026_05_10;

ALTER TABLE IF EXISTS episodes
    RENAME TO episodes_legacy_2026_05_10;

-- Rename legacy indexes to avoid name collisions with canonical tables
-- (discovered during live migration on Beast — Devon-be18 | 2026-05-11)
ALTER INDEX IF EXISTS idx_knowledge_vectors_embedding RENAME TO idx_knowledge_vectors_embedding_legacy;
ALTER INDEX IF EXISTS idx_knowledge_vectors_metadata RENAME TO idx_knowledge_vectors_metadata_legacy;
ALTER INDEX IF EXISTS idx_knowledge_vectors_source_type RENAME TO idx_knowledge_vectors_source_type_legacy;
ALTER INDEX IF EXISTS idx_entities_type RENAME TO idx_entities_type_legacy;
ALTER INDEX IF EXISTS idx_entities_name RENAME TO idx_entities_name_legacy;
ALTER INDEX IF EXISTS idx_entities_embedding RENAME TO idx_entities_embedding_legacy;
ALTER INDEX IF EXISTS idx_entities_properties RENAME TO idx_entities_properties_legacy;
ALTER INDEX IF EXISTS idx_relationships_source RENAME TO idx_relationships_source_legacy;
ALTER INDEX IF EXISTS idx_relationships_target RENAME TO idx_relationships_target_legacy;
ALTER INDEX IF EXISTS idx_relationships_type RENAME TO idx_relationships_type_legacy;
ALTER INDEX IF EXISTS idx_relationships_embedding RENAME TO idx_relationships_embedding_legacy;
ALTER INDEX IF EXISTS idx_episodes_created RENAME TO idx_episodes_created_legacy;
ALTER INDEX IF EXISTS idx_episodes_source_type RENAME TO idx_episodes_source_type_legacy;

-- ═══════════════════════════════════════════════════════════════════════
-- 2. Canonical tables — full provenance, manifest-backed
-- ═══════════════════════════════════════════════════════════════════════

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE knowledge_vectors (
    id              UUID PRIMARY KEY,
    content         TEXT NOT NULL,
    embedding       vector(384),
    source          TEXT,
    source_type     TEXT,
    metadata        JSONB DEFAULT '{}',

    -- v0.3 provenance (every column required by AMP-302 acceptance criteria)
    provenance      TEXT NOT NULL DEFAULT 'amplified-pipeline-v0.3',
    pipeline_version TEXT NOT NULL,
    run_id          TEXT NOT NULL,
    file_path       TEXT NOT NULL,
    file_hash       TEXT NOT NULL,
    chunk_hash      TEXT NOT NULL,
    chunk_index     INT NOT NULL DEFAULT 0,
    line_start      INT,
    line_end        INT,
    parent_heading  TEXT,
    prev_hash       TEXT,
    next_hash       TEXT,
    signed_by       TEXT NOT NULL DEFAULT 'brain_writer_pipeline',
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE entities (
    id              UUID PRIMARY KEY,
    name            TEXT NOT NULL,
    entity_type     TEXT,
    summary         TEXT,
    properties      JSONB DEFAULT '{}',
    source_type     TEXT DEFAULT 'derived',
    run_id          TEXT,
    signed_by       TEXT NOT NULL DEFAULT 'brain_writer_pipeline',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE relationships (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id       UUID NOT NULL REFERENCES entities(id),
    target_id       UUID NOT NULL REFERENCES entities(id),
    relation_type   TEXT NOT NULL,
    summary         TEXT,
    weight          REAL,
    properties      JSONB DEFAULT '{}',
    source_type     TEXT DEFAULT 'derived',
    run_id          TEXT,
    signed_by       TEXT NOT NULL DEFAULT 'brain_writer_pipeline',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE episodes (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT,
    content         TEXT,
    source          TEXT,
    source_type     TEXT DEFAULT 'derived',
    run_id          TEXT,
    signed_by       TEXT NOT NULL DEFAULT 'brain_writer_pipeline',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════════════════
-- 3. Indexes
-- ═══════════════════════════════════════════════════════════════════════

CREATE INDEX idx_kv_canonical_embedding
    ON knowledge_vectors USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX idx_kv_provenance ON knowledge_vectors (provenance);
CREATE INDEX idx_kv_run_id ON knowledge_vectors (run_id);
CREATE INDEX idx_kv_file_hash ON knowledge_vectors (file_hash);
CREATE INDEX idx_kv_ingested_at ON knowledge_vectors (ingested_at DESC);

CREATE INDEX idx_entities_type ON entities (entity_type);
CREATE INDEX idx_entities_name ON entities (name);

CREATE INDEX idx_relationships_source ON relationships (source_id);
CREATE INDEX idx_relationships_target ON relationships (target_id);
CREATE INDEX idx_relationships_type ON relationships (relation_type);

-- ═══════════════════════════════════════════════════════════════════════
-- 4. Consumer views
-- ═══════════════════════════════════════════════════════════════════════

-- Consumers read this, not the raw table
CREATE VIEW knowledge_vectors_canonical AS
    SELECT * FROM knowledge_vectors
    WHERE provenance = 'amplified-pipeline-v0.3';

-- Legacy fallback for anything that still needs old data
CREATE VIEW legacy_pre_v0_3 AS
    SELECT * FROM knowledge_vectors_legacy_2026_05_10;

-- ═══════════════════════════════════════════════════════════════════════
-- 5. Manifest storage table
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE ingestion_manifests (
    run_id          TEXT PRIMARY KEY,
    source_root     TEXT NOT NULL,
    file_count      INT NOT NULL DEFAULT 0,
    chunk_count     INT NOT NULL DEFAULT 0,
    manifest_hash   TEXT NOT NULL,
    manifest_path   TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    signed_by       TEXT NOT NULL DEFAULT 'brain_writer_pipeline'
);

-- ═══════════════════════════════════════════════════════════════════════
-- 6. Role grants (extend existing brain_writer from migration 005)
-- ═══════════════════════════════════════════════════════════════════════

-- Writer: canonical tables + manifest + audit
GRANT INSERT, UPDATE ON TABLE knowledge_vectors TO brain_writer;
GRANT INSERT, UPDATE ON TABLE entities TO brain_writer;
GRANT INSERT, UPDATE ON TABLE relationships TO brain_writer;
GRANT INSERT, UPDATE ON TABLE episodes TO brain_writer;
GRANT INSERT, UPDATE ON TABLE ingestion_manifests TO brain_writer;
GRANT INSERT ON TABLE audit_log TO brain_writer;

-- Writer can still read legacy
GRANT SELECT ON TABLE knowledge_vectors_legacy_2026_05_10 TO brain_writer;
GRANT SELECT ON TABLE entities_legacy_2026_05_10 TO brain_writer;
GRANT SELECT ON TABLE relationships_legacy_2026_05_10 TO brain_writer;
GRANT SELECT ON TABLE episodes_legacy_2026_05_10 TO brain_writer;

-- Reader: canonical views + legacy
GRANT SELECT ON TABLE knowledge_vectors TO brain_reader;
GRANT SELECT ON TABLE entities TO brain_reader;
GRANT SELECT ON TABLE relationships TO brain_reader;
GRANT SELECT ON TABLE episodes TO brain_reader;
GRANT SELECT ON TABLE ingestion_manifests TO brain_reader;
GRANT SELECT ON knowledge_vectors_canonical TO brain_reader;
GRANT SELECT ON legacy_pre_v0_3 TO brain_reader;
GRANT SELECT ON TABLE knowledge_vectors_legacy_2026_05_10 TO brain_reader;
GRANT SELECT ON TABLE entities_legacy_2026_05_10 TO brain_reader;
GRANT SELECT ON TABLE relationships_legacy_2026_05_10 TO brain_reader;
GRANT SELECT ON TABLE episodes_legacy_2026_05_10 TO brain_reader;

COMMIT;

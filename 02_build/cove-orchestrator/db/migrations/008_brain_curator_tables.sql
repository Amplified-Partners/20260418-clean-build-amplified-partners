-- Migration 008: Brain Curator tables (post-write curation layer)
--
-- Adds curation tables for the brain_curator module. This implements
-- "chunks are evidence; packets are meaning" — curation reads existing
-- knowledge_vectors and produces governed knowledge packets without
-- mutating raw source content.
--
-- Depends on: 007_canonical_schema_v0.3.sql (knowledge_vectors table)
-- Run as superuser on the amplified_brain database.
--
-- Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f

BEGIN;

-- ═══════════════════════════════════════════════════════════════════════
-- 1. Curation run audit table (created first — referenced by others)
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE brain_curation_runs (
    run_id          TEXT PRIMARY KEY,
    stage           TEXT NOT NULL,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at    TIMESTAMPTZ,
    code_version    TEXT NOT NULL DEFAULT 'brain-curator-v0.1',
    config_hash     TEXT,
    input_scope     JSONB DEFAULT '{}',
    metrics         JSONB DEFAULT '{}',
    status          TEXT NOT NULL DEFAULT 'running',
    error           TEXT
);

CREATE INDEX idx_bcr_stage ON brain_curation_runs (stage);
CREATE INDEX idx_bcr_status ON brain_curation_runs (status);
CREATE INDEX idx_bcr_started ON brain_curation_runs (started_at DESC);

-- ═══════════════════════════════════════════════════════════════════════
-- 2. Document inventory (groups chunks by source file)
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE brain_documents (
    document_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_path         TEXT NOT NULL,
    source_system       TEXT NOT NULL DEFAULT 'amplified-pipeline-v0.3',
    source_id           TEXT,
    file_hash_sha256    TEXT NOT NULL,
    raw_frontmatter     JSONB DEFAULT '{}',
    fm_metadata         JSONB DEFAULT '{}',
    title               TEXT,
    document_type       TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    pipeline_version    TEXT NOT NULL DEFAULT 'amplified-pipeline-v0.3',
    chunk_count         INT NOT NULL DEFAULT 0,
    status              TEXT NOT NULL DEFAULT 'inventoried'
);

CREATE INDEX idx_bd_source_path ON brain_documents (source_path);
CREATE INDEX idx_bd_file_hash ON brain_documents (file_hash_sha256);
CREATE INDEX idx_bd_status ON brain_documents (status);
CREATE INDEX idx_bd_document_type ON brain_documents (document_type);

-- ═══════════════════════════════════════════════════════════════════════
-- 3. Dedup clusters and members
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE brain_dedupe_clusters (
    cluster_id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cluster_type        TEXT NOT NULL,  -- 'exact' | 'metadata_family'
    method              TEXT NOT NULL,  -- 'sha256' | 'title_path' | 'source_timestamp'
    canonical_member_id UUID,
    metadata            JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_bdc_type ON brain_dedupe_clusters (cluster_type);

CREATE TABLE brain_dedupe_members (
    member_id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cluster_id          UUID NOT NULL REFERENCES brain_dedupe_clusters(cluster_id),
    chunk_id            UUID NOT NULL,
    member_role         TEXT NOT NULL DEFAULT 'member',  -- 'canonical' | 'member'
    confidence          REAL NOT NULL DEFAULT 1.0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_bdm_cluster ON brain_dedupe_members (cluster_id);
CREATE INDEX idx_bdm_chunk ON brain_dedupe_members (chunk_id);
CREATE INDEX idx_bdm_role ON brain_dedupe_members (member_role);

-- ═══════════════════════════════════════════════════════════════════════
-- 4. Knowledge packets (governed meaning units)
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE brain_packets (
    packet_id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    packet_type         TEXT NOT NULL,  -- 'decision' | 'working_model' | 'method' | 'doctrine' | 'failure' | 'prompt_pattern' | 'reference' | 'conversation'
    title               TEXT,
    summary             TEXT,
    status              TEXT NOT NULL DEFAULT 'draft',  -- 'draft' | 'active' | 'frozen' | 'superseded' | 'quarantined'
    route               TEXT,  -- 'keep' | 'freeze' | 'refine' | 'quarantine' | 'drop_from_active' | 'review' | 'validate'
    epistemic_tier      TEXT,  -- 'INTUITED' | 'STRUCTURED' | 'MEASURED' | 'PROVEN'
    claim_status        TEXT,
    decision_state      TEXT,
    valid_from          TIMESTAMPTZ,
    valid_to            TIMESTAMPTZ,
    last_verified_at    TIMESTAMPTZ,
    source_document_id  UUID REFERENCES brain_documents(document_id),
    canonical_packet_id UUID,  -- self-ref for version chains
    metadata            JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_bp_type ON brain_packets (packet_type);
CREATE INDEX idx_bp_status ON brain_packets (status);
CREATE INDEX idx_bp_route ON brain_packets (route);
CREATE INDEX idx_bp_tier ON brain_packets (epistemic_tier);
CREATE INDEX idx_bp_source_doc ON brain_packets (source_document_id);
-- Composite index for active current-model retrieval
CREATE INDEX idx_bp_active_retrieval ON brain_packets (packet_type, status, route, epistemic_tier)
    WHERE status = 'active' AND route IN ('keep', 'freeze');

-- ═══════════════════════════════════════════════════════════════════════
-- 5. Evidence links (packet <-> chunk)
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE brain_packet_evidence (
    evidence_id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    packet_id           UUID NOT NULL REFERENCES brain_packets(packet_id),
    chunk_id            UUID NOT NULL,
    evidence_role       TEXT NOT NULL DEFAULT 'supports',  -- 'supports' | 'contradicts' | 'context'
    confidence          REAL NOT NULL DEFAULT 1.0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_bpe_packet ON brain_packet_evidence (packet_id);
CREATE INDEX idx_bpe_chunk ON brain_packet_evidence (chunk_id);

-- ═══════════════════════════════════════════════════════════════════════
-- 6. Packet relationships (packet <-> packet)
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE brain_relationships (
    relationship_id     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_packet_id    UUID NOT NULL REFERENCES brain_packets(packet_id),
    target_packet_id    UUID NOT NULL REFERENCES brain_packets(packet_id),
    predicate           TEXT NOT NULL,  -- 'supersedes' | 'refines' | 'contradicts' | 'supports' | 'derived_from'
    evidence_count      INT NOT NULL DEFAULT 0,
    confidence          REAL NOT NULL DEFAULT 1.0,
    metadata            JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_br_source ON brain_relationships (source_packet_id);
CREATE INDEX idx_br_target ON brain_relationships (target_packet_id);
CREATE INDEX idx_br_predicate ON brain_relationships (predicate);

-- ═══════════════════════════════════════════════════════════════════════
-- 7. Validation samples
-- ═══════════════════════════════════════════════════════════════════════

CREATE TABLE brain_validation_samples (
    sample_id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    packet_id           UUID NOT NULL REFERENCES brain_packets(packet_id),
    verdict             TEXT,  -- 'correct' | 'incorrect' | 'ambiguous' | null (pending)
    reviewed_by         TEXT,
    reviewed_at         TIMESTAMPTZ,
    notes               TEXT,
    metrics             JSONB DEFAULT '{}'
);

CREATE INDEX idx_bvs_packet ON brain_validation_samples (packet_id);
CREATE INDEX idx_bvs_verdict ON brain_validation_samples (verdict);

-- ═══════════════════════════════════════════════════════════════════════
-- 8. Role grants — extend brain_writer and brain_reader
-- ═══════════════════════════════════════════════════════════════════════

-- Writer: full CRUD on curation tables
GRANT INSERT, UPDATE, DELETE ON TABLE brain_curation_runs TO brain_writer;
GRANT INSERT, UPDATE, DELETE ON TABLE brain_documents TO brain_writer;
GRANT INSERT, UPDATE, DELETE ON TABLE brain_dedupe_clusters TO brain_writer;
GRANT INSERT, UPDATE, DELETE ON TABLE brain_dedupe_members TO brain_writer;
GRANT INSERT, UPDATE, DELETE ON TABLE brain_packets TO brain_writer;
GRANT INSERT, UPDATE, DELETE ON TABLE brain_packet_evidence TO brain_writer;
GRANT INSERT, UPDATE, DELETE ON TABLE brain_relationships TO brain_writer;
GRANT INSERT, UPDATE, DELETE ON TABLE brain_validation_samples TO brain_writer;

-- Reader: SELECT only
GRANT SELECT ON TABLE brain_curation_runs TO brain_reader;
GRANT SELECT ON TABLE brain_documents TO brain_reader;
GRANT SELECT ON TABLE brain_dedupe_clusters TO brain_reader;
GRANT SELECT ON TABLE brain_dedupe_members TO brain_reader;
GRANT SELECT ON TABLE brain_packets TO brain_reader;
GRANT SELECT ON TABLE brain_packet_evidence TO brain_reader;
GRANT SELECT ON TABLE brain_relationships TO brain_reader;
GRANT SELECT ON TABLE brain_validation_samples TO brain_reader;

COMMIT;

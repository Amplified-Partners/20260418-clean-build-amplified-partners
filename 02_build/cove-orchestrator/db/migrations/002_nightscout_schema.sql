-- ============================================================
-- 002_nightscout_schema.sql
-- NightScout Intelligence Pipeline — Phase 2
-- ============================================================

-- Source types for the intelligence pipeline
CREATE TYPE source_type AS ENUM (
    'rss',
    'searxng',
    'api',
    'web_scrape'
);

-- Relevance categories for scored items
CREATE TYPE relevance_tier AS ENUM (
    'noise',       -- < 4/10, discarded
    'briefing',    -- 4-6.9/10, goes to morning briefing
    'rd_pipeline', -- 7-8.9/10, goes to R&D rubric evaluation
    'critical'     -- 9-10/10, immediate notification
);

-- ============================================================
-- Sources: where intelligence comes from
-- ============================================================
CREATE TABLE ns_sources (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    source_type     source_type NOT NULL,
    url             TEXT NOT NULL,
    category        TEXT NOT NULL,          -- e.g. 'ai_research', 'smb_tech', 'competitor', 'market'
    fetch_config    JSONB NOT NULL DEFAULT '{}',  -- headers, params, selectors, etc.
    schedule_cron   TEXT NOT NULL DEFAULT '0 2 * * *',  -- default: 2am daily
    enabled         BOOLEAN NOT NULL DEFAULT true,
    last_fetched_at TIMESTAMPTZ,
    last_error      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- Raw items: everything fetched before scoring
-- ============================================================
CREATE TABLE ns_raw_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id       UUID NOT NULL REFERENCES ns_sources(id),
    external_id     TEXT,                   -- dedup key (URL hash, GUID, etc.)
    title           TEXT NOT NULL,
    url             TEXT,
    content         TEXT NOT NULL,           -- full text or summary
    published_at    TIMESTAMPTZ,
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata        JSONB NOT NULL DEFAULT '{}',  -- author, tags, etc.
    UNIQUE(source_id, external_id)
);

-- ============================================================
-- Scored items: after Ollama evaluation
-- ============================================================
CREATE TABLE ns_scored_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_item_id     UUID NOT NULL REFERENCES ns_raw_items(id) ON DELETE CASCADE,
    -- Four scoring dimensions (each 0.0 to 10.0)
    relevance       NUMERIC(3,1) NOT NULL,  -- How relevant to Amplified's mission
    impact          NUMERIC(3,1) NOT NULL,  -- Potential business impact
    applicability   NUMERIC(3,1) NOT NULL,  -- How quickly we can apply this
    novelty         NUMERIC(3,1) NOT NULL,  -- How new/unexpected is this
    -- Composite
    composite_score NUMERIC(3,1) NOT NULL GENERATED ALWAYS AS (
        (relevance + impact + applicability + novelty) / 4.0
    ) STORED,
    tier            relevance_tier NOT NULL,
    -- LLM reasoning
    scoring_model   TEXT NOT NULL,           -- e.g. 'qwen3-32b' via Ollama
    reasoning       TEXT NOT NULL,           -- Why these scores
    tags            TEXT[] NOT NULL DEFAULT '{}',  -- auto-extracted topics
    -- Lifecycle
    scored_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    briefing_id     UUID,                    -- FK to briefing if included
    rd_submitted    BOOLEAN NOT NULL DEFAULT false,
    graphiti_episode_id TEXT               -- Graphiti episode reference
);

CREATE INDEX idx_scored_composite ON ns_scored_items(composite_score DESC);
CREATE INDEX idx_scored_tier ON ns_scored_items(tier);
CREATE INDEX idx_scored_date ON ns_scored_items(scored_at DESC);
CREATE INDEX idx_scored_tags ON ns_scored_items USING GIN(tags);

-- ============================================================
-- Briefings: the morning report
-- ============================================================
CREATE TABLE ns_briefings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    generated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    period_start    TIMESTAMPTZ NOT NULL,
    period_end      TIMESTAMPTZ NOT NULL,
    -- Content
    summary_md      TEXT NOT NULL,           -- Markdown morning briefing
    item_count      INTEGER NOT NULL,
    top_score       NUMERIC(3,1),
    categories      JSONB NOT NULL DEFAULT '{}',  -- { "ai_research": 5, "smb_tech": 3 }
    -- Delivery
    delivered       BOOLEAN NOT NULL DEFAULT false,
    delivered_at    TIMESTAMPTZ,
    delivery_channel TEXT                    -- 'telegram', 'email', 'command_centre'
);

-- Link scored items to briefings
ALTER TABLE ns_scored_items
    ADD CONSTRAINT fk_scored_briefing
    FOREIGN KEY (briefing_id) REFERENCES ns_briefings(id);

-- ============================================================
-- Pipeline runs: track each execution
-- ============================================================
CREATE TABLE ns_pipeline_runs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at    TIMESTAMPTZ,
    status          TEXT NOT NULL DEFAULT 'running',  -- running, completed, failed
    sources_fetched INTEGER NOT NULL DEFAULT 0,
    items_fetched   INTEGER NOT NULL DEFAULT 0,
    items_scored    INTEGER NOT NULL DEFAULT 0,
    items_briefing  INTEGER NOT NULL DEFAULT 0,
    items_rd        INTEGER NOT NULL DEFAULT 0,
    items_critical  INTEGER NOT NULL DEFAULT 0,
    error           TEXT,
    duration_ms     INTEGER
);

-- ============================================================
-- Auto-update triggers (reuse pattern from 001)
-- ============================================================
CREATE TRIGGER trg_ns_sources_updated
    BEFORE UPDATE ON ns_sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Unique constraint for source upsert
ALTER TABLE ns_sources ADD CONSTRAINT uq_ns_sources
    UNIQUE (name, source_type, url, category);

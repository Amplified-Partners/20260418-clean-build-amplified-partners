-- Step 7: halfvec Migration Cutover
-- AMP-331 | Devon-0178 | 2026-05-13
--
-- Run on: cove-postgres → amplified_brain
-- Command:
--   docker exec cove-postgres psql -U cove -d amplified_brain -f /tmp/07-halfvec-migration.sql
--
-- What this does:
--   Converts knowledge_vectors.embedding from vector(384) to halfvec(384).
--   halfvec uses 16-bit floats instead of 32-bit → 50% storage reduction.
--   At 384 dimensions, the precision loss is negligible for cosine similarity.
--
-- Current state (MEASURED 2026-05-13):
--   163,554 rows, vector(384), HNSW cosine index
--   Table + index total: 792 MB
--   Expected after: ~400 MB
--
-- Downtime: ~5 minutes (index rebuild blocks queries on this column)
-- Schedule: off-hours (brain MCP read traffic will error during rebuild)
--
-- Rollback:
--   ALTER TABLE knowledge_vectors ALTER COLUMN embedding TYPE vector(384);
--   DROP INDEX IF EXISTS idx_kv_canonical_embedding;
--   CREATE INDEX idx_kv_canonical_embedding
--     ON knowledge_vectors USING hnsw (embedding vector_cosine_ops)
--     WITH (m = 16, ef_construction = 64);
--
-- Prerequisites:
--   - pgvector 0.8.2+ (halfvec support added in 0.7.0) ✓
--   - Notify brain-mcp-readonly and brain-mcp-writer services of brief downtime
-- ─────────────────────────────────────────────────────────────────────────────

-- ── Pre-flight ──────────────────────────────────────────────────────────────

-- Verify current state
SELECT
  pg_size_pretty(pg_total_relation_size('knowledge_vectors')) AS total_size,
  pg_size_pretty(pg_relation_size('knowledge_vectors')) AS table_size,
  pg_size_pretty(pg_indexes_size('knowledge_vectors')) AS index_size;

SELECT count(*) AS row_count FROM knowledge_vectors;

-- Show current column type
SELECT column_name, udt_name, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'knowledge_vectors' AND column_name = 'embedding';

-- Show current index
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'knowledge_vectors' AND indexname LIKE '%embedding%';

-- ── Increase maintenance_work_mem for faster index build ────────────────────

SET maintenance_work_mem = '4GB';

-- ── Step 1: Drop the existing HNSW index ────────────────────────────────────

DROP INDEX IF EXISTS idx_kv_canonical_embedding;

-- ── Step 2: Convert column from vector(384) to halfvec(384) ─────────────────

ALTER TABLE knowledge_vectors
  ALTER COLUMN embedding TYPE halfvec(384);

-- ── Step 3: Rebuild the HNSW index on halfvec ───────────────────────────────
-- halfvec uses halfvec_cosine_ops instead of vector_cosine_ops

CREATE INDEX idx_kv_canonical_embedding
  ON knowledge_vectors USING hnsw (embedding halfvec_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- ── Step 4: Reset maintenance_work_mem ──────────────────────────────────────

RESET maintenance_work_mem;

-- ── Post-flight verification ────────────────────────────────────────────────

-- Verify new column type
SELECT column_name, udt_name
FROM information_schema.columns
WHERE table_name = 'knowledge_vectors' AND column_name = 'embedding';

-- Verify new index
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'knowledge_vectors' AND indexname LIKE '%embedding%';

-- Verify size reduction
SELECT
  pg_size_pretty(pg_total_relation_size('knowledge_vectors')) AS total_size_after,
  pg_size_pretty(pg_relation_size('knowledge_vectors')) AS table_size_after,
  pg_size_pretty(pg_indexes_size('knowledge_vectors')) AS index_size_after;

-- Spot-check: verify a similarity query still works
SELECT id, 1 - (embedding <=> (SELECT embedding FROM knowledge_vectors LIMIT 1)) AS similarity
FROM knowledge_vectors
ORDER BY embedding <=> (SELECT embedding FROM knowledge_vectors LIMIT 1)
LIMIT 5;

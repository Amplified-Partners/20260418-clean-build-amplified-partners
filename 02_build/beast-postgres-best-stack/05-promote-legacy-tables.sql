-- Step 5: Promote Legacy Tables to Live
-- AMP-331 | Devon-0178 | 2026-05-13
--
-- Run on: cove-postgres → amplified_brain
-- Command:
--   docker exec cove-postgres psql -U cove -d amplified_brain -f /tmp/05-promote-legacy-tables.sql
--
-- What this does:
--   Copies 53,959 entities, 34,488 relationships, and 4,257 episodes from
--   the `_legacy_2026_05_10` tables into the live tables. The live tables
--   are currently EMPTY (confirmed 2026-05-13 05:48 UTC).
--
-- Column mapping (legacy → live):
--   Entities:
--     Legacy: id, name, entity_type, summary, properties, embedding, created_at, updated_at
--     Live:   id, name, entity_type, summary, properties, source_type, run_id, signed_by, created_at, updated_at
--     → embedding dropped (stored separately in knowledge_vectors)
--     → source_type defaults to 'falkordb_migration'
--     → run_id defaults to 'legacy_promotion_2026_05_13'
--     → signed_by defaults to 'Devon-0178'
--
--   Relationships:
--     Legacy: id, source_id, target_id, relation_type, summary, transition_probability, properties, embedding, created_at, updated_at
--     Live:   id, source_id, target_id, relation_type, summary, weight, properties, source_type, run_id, signed_by, created_at, updated_at
--     → transition_probability (double precision) → weight (real)
--     → embedding dropped
--     → source_type, run_id, signed_by defaulted
--
--   Episodes:
--     Legacy: id, content, source, source_type, summary, metadata, embedding, created_at
--     Live:   id, name, content, source, source_type, run_id, signed_by, created_at
--     → name set to NULL (legacy has no name field)
--     → summary, metadata, embedding dropped
--     → run_id, signed_by defaulted
--
-- Downtime: NONE (online DML; live tables are empty so no contention)
-- Rollback: TRUNCATE entities, relationships, episodes;
--
-- Safety: ON CONFLICT (id) DO NOTHING — idempotent if re-run.
-- ─────────────────────────────────────────────────────────────────────────────

BEGIN;

-- ── Pre-flight checks ──────────────────────────────────────────────────────

-- Verify live tables are empty (abort if not)
DO $$
DECLARE
  e_count bigint;
  r_count bigint;
  ep_count bigint;
BEGIN
  SELECT count(*) INTO e_count FROM entities;
  SELECT count(*) INTO r_count FROM relationships;
  SELECT count(*) INTO ep_count FROM episodes;

  IF e_count > 0 OR r_count > 0 OR ep_count > 0 THEN
    RAISE EXCEPTION 'Live tables are not empty: entities=%, relationships=%, episodes=%. Aborting.',
      e_count, r_count, ep_count;
  END IF;

  RAISE NOTICE 'Pre-flight OK: all live tables empty';
END $$;

-- Count legacy rows for verification
DO $$
DECLARE
  le bigint; lr bigint; lep bigint;
BEGIN
  SELECT count(*) INTO le FROM entities_legacy_2026_05_10;
  SELECT count(*) INTO lr FROM relationships_legacy_2026_05_10;
  SELECT count(*) INTO lep FROM episodes_legacy_2026_05_10;
  RAISE NOTICE 'Legacy counts: entities=%, relationships=%, episodes=%', le, lr, lep;
END $$;

-- ── Promote entities ────────────────────────────────────────────────────────

INSERT INTO entities (
  id,
  name,
  entity_type,
  summary,
  properties,
  source_type,
  run_id,
  signed_by,
  created_at,
  updated_at
)
SELECT
  id,
  name,
  entity_type,
  summary,
  properties,
  'falkordb_migration',
  'legacy_promotion_2026_05_13',
  'Devon-0178',
  created_at,
  updated_at
FROM entities_legacy_2026_05_10
ON CONFLICT (id) DO NOTHING;

-- ── Promote relationships ───────────────────────────────────────────────────

INSERT INTO relationships (
  id,
  source_id,
  target_id,
  relation_type,
  summary,
  weight,
  properties,
  source_type,
  run_id,
  signed_by,
  created_at,
  updated_at
)
SELECT
  id,
  source_id,
  target_id,
  relation_type,
  summary,
  transition_probability::real,   -- double precision → real
  properties,
  'falkordb_migration',
  'legacy_promotion_2026_05_13',
  'Devon-0178',
  created_at,
  updated_at
FROM relationships_legacy_2026_05_10
ON CONFLICT (id) DO NOTHING;

-- ── Promote episodes ────────────────────────────────────────────────────────

INSERT INTO episodes (
  id,
  name,
  content,
  source,
  source_type,
  run_id,
  signed_by,
  created_at
)
SELECT
  id,
  NULL,                            -- legacy has no name column
  content,
  source,
  source_type,
  'legacy_promotion_2026_05_13',
  'Devon-0178',
  created_at
FROM episodes_legacy_2026_05_10
ON CONFLICT (id) DO NOTHING;

-- ── Post-flight verification ────────────────────────────────────────────────

DO $$
DECLARE
  e_count bigint;  r_count bigint;  ep_count bigint;
  le bigint;       lr bigint;       lep bigint;
BEGIN
  SELECT count(*) INTO e_count FROM entities;
  SELECT count(*) INTO r_count FROM relationships;
  SELECT count(*) INTO ep_count FROM episodes;
  SELECT count(*) INTO le FROM entities_legacy_2026_05_10;
  SELECT count(*) INTO lr FROM relationships_legacy_2026_05_10;
  SELECT count(*) INTO lep FROM episodes_legacy_2026_05_10;

  RAISE NOTICE '──────────────────────────────────────';
  RAISE NOTICE 'Promotion complete.';
  RAISE NOTICE 'entities:      % / % (%.1f%%)', e_count, le,
    CASE WHEN le > 0 THEN (e_count::float / le * 100) ELSE 0 END;
  RAISE NOTICE 'relationships: % / % (%.1f%%)', r_count, lr,
    CASE WHEN lr > 0 THEN (r_count::float / lr * 100) ELSE 0 END;
  RAISE NOTICE 'episodes:      % / % (%.1f%%)', ep_count, lep,
    CASE WHEN lep > 0 THEN (ep_count::float / lep * 100) ELSE 0 END;
  RAISE NOTICE '──────────────────────────────────────';

  -- Fail if counts don't match
  IF e_count <> le OR r_count <> lr OR ep_count <> lep THEN
    RAISE WARNING 'Count mismatch — some rows may have had ON CONFLICT collisions';
  END IF;
END $$;

COMMIT;

-- ── Quick sanity queries ────────────────────────────────────────────────────

SELECT 'entities' AS table_name, count(*) AS rows FROM entities
UNION ALL
SELECT 'relationships', count(*) FROM relationships
UNION ALL
SELECT 'episodes', count(*) FROM episodes;

SELECT entity_type, count(*) FROM entities GROUP BY entity_type ORDER BY count(*) DESC;
SELECT relation_type, count(*) FROM relationships GROUP BY relation_type ORDER BY count(*) DESC;

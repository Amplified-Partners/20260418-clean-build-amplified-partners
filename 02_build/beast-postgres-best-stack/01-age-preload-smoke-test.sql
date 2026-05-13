-- Step 1: AGE Preload + Smoke Test
-- AMP-331 | Devon-0178 | 2026-05-13
--
-- Run on: cove-postgres → amplified_brain
-- Command:
--   docker exec cove-postgres psql -U cove -d amplified_brain -f /tmp/01-age-preload-smoke-test.sql
-- Or copy-paste into psql session.
--
-- Prerequisites: AGE 1.6.0 extension already installed (CREATE EXTENSION age).
-- This script does NOT add AGE to shared_preload_libraries.
-- The timescaledb-ha image does not support AGE in shared_preload (confirmed
-- empirically — causes crash loop). AGE must be loaded per-connection.
--
-- Downtime: NONE
-- Rollback: N/A (smoke test only, creates then drops a test graph)
-- ─────────────────────────────────────────────────────────────────────────────

-- 1. Load AGE into this session
LOAD 'age';

-- 2. Set search path so ag_catalog functions resolve
SET search_path = ag_catalog, public;

-- 3. Verify AGE extension is present
SELECT extname, extversion FROM pg_extension WHERE extname = 'age';

-- 4. List existing graphs
SELECT * FROM ag_catalog.ag_graph;

-- 5. Smoke test: create a temporary graph
SELECT create_graph('_smoke_test');

-- 6. Create a test vertex
SELECT * FROM cypher('_smoke_test', $$
  CREATE (n:TestNode {name: 'smoke', created_at: timestamp()})
  RETURN n
$$) AS (v agtype);

-- 7. Create a second vertex and an edge
SELECT * FROM cypher('_smoke_test', $$
  CREATE (a:TestNode {name: 'alpha'})
  CREATE (b:TestNode {name: 'beta'})
  CREATE (a)-[r:CONNECTS_TO {weight: 0.95}]->(b)
  RETURN a, r, b
$$) AS (a agtype, r agtype, b agtype);

-- 8. Query: count vertices and edges
SELECT * FROM cypher('_smoke_test', $$
  MATCH (n)
  RETURN count(n) AS vertex_count
$$) AS (vertex_count agtype);

SELECT * FROM cypher('_smoke_test', $$
  MATCH ()-[r]->()
  RETURN count(r) AS edge_count
$$) AS (edge_count agtype);

-- 9. Query: traverse a relationship
SELECT * FROM cypher('_smoke_test', $$
  MATCH (a)-[r:CONNECTS_TO]->(b)
  RETURN a.name, r.weight, b.name
$$) AS (source agtype, weight agtype, target agtype);

-- 10. Clean up: drop the smoke test graph
SELECT drop_graph('_smoke_test', true);

-- 11. Confirm existing compound_design graph is untouched
SELECT * FROM ag_catalog.ag_graph;

-- ─────────────────────────────────────────────────────────────────────────────
-- If all 11 steps complete without error, AGE is functional.
-- Every application/script that uses AGE must begin with:
--   LOAD 'age';
--   SET search_path = ag_catalog, public;
-- ─────────────────────────────────────────────────────────────────────────────

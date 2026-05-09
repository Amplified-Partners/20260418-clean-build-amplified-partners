-- Migration 005: Lock down amplified_brain access (AMP-279)
--
-- Principle: ingestion ONLY through the pipeline (brain_writer),
-- everything else read-only (brain_reader).
--
-- Run as superuser on the amplified_brain database.
-- Signed-by: Devon-c329 | 2026-05-09 | devin-c3297c6e5f464d8fb6d912403b7cc3e6

-- ── Create roles if they don't exist ─────────────────────────────
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'brain_writer') THEN
        CREATE ROLE brain_writer LOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'brain_reader') THEN
        CREATE ROLE brain_reader LOGIN;
    END IF;
END
$$;

-- ── Revoke public defaults ───────────────────────────────────────
REVOKE ALL ON DATABASE amplified_brain FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM PUBLIC;

-- ── brain_reader: SELECT only ────────────────────────────────────
GRANT CONNECT ON DATABASE amplified_brain TO brain_reader;
GRANT USAGE ON SCHEMA public TO brain_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO brain_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO brain_reader;

-- ── brain_writer: INSERT/UPDATE on ingestion tables only ─────────
GRANT CONNECT ON DATABASE amplified_brain TO brain_writer;
GRANT USAGE ON SCHEMA public TO brain_writer;

-- Writer can read everything
GRANT SELECT ON ALL TABLES IN SCHEMA public TO brain_writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO brain_writer;

-- Writer can INSERT/UPDATE only on ingestion-target tables
GRANT INSERT, UPDATE ON TABLE knowledge_vectors TO brain_writer;
GRANT INSERT, UPDATE ON TABLE entities TO brain_writer;
GRANT INSERT, UPDATE ON TABLE relationships TO brain_writer;
GRANT INSERT, UPDATE ON TABLE pipeline_runs TO brain_writer;

-- Writer needs sequence usage for any serial columns
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO brain_writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE ON SEQUENCES TO brain_writer;

-- ── No DELETE for anyone except superuser ────────────────────────
-- brain_writer cannot DELETE — append-only ingestion.
-- brain_reader cannot modify anything.
-- Only superuser (postgres) can DELETE or DROP.

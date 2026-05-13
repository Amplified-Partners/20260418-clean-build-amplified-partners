-- Rollback for migration 007: Canonical ingestion schema v0.3 (AMP-302)
--
-- Restores legacy table names. Zero data loss.
-- Run as superuser on the amplified_brain database.
--
-- Signed-by: Devon-0de2 | 2026-05-11 | devin-0de27df281514f96ba3921354d7c31ae

BEGIN;

DROP VIEW IF EXISTS knowledge_vectors_canonical;
DROP VIEW IF EXISTS legacy_pre_v0_3;

DROP TABLE IF EXISTS ingestion_manifests;

DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS entities;
DROP TABLE IF EXISTS knowledge_vectors;

ALTER TABLE IF EXISTS knowledge_vectors_legacy_2026_05_10
    RENAME TO knowledge_vectors;

ALTER TABLE IF EXISTS entities_legacy_2026_05_10
    RENAME TO entities;

ALTER TABLE IF EXISTS relationships_legacy_2026_05_10
    RENAME TO relationships;

ALTER TABLE IF EXISTS episodes_legacy_2026_05_10
    RENAME TO episodes;

COMMIT;

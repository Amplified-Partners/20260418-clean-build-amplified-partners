"""Migration-text assertions for 007_writer_v03_provenance.sql (AMP-302).

We do not spin up Postgres in this repo's unit-test suite, but the
migration text still encodes contracts a reviewer (or a junior agent)
could break in seconds. These tests pin those contracts:

* Production cutover stays GUC-gated — no ungated GRANT/REVOKE.
* Canonical view restricts to manifest-backed rows.
* Provenance columns and unique index on (file_hash, chunk_index) exist.
* writer_version CHECK constraint matches the format the writer emits.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

MIGRATION = (
    Path(__file__).resolve().parent.parent
    / "db" / "migrations" / "007_writer_v03_provenance.sql"
)


@pytest.fixture(scope="module")
def sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def test_migration_file_exists(sql: str) -> None:
    assert sql, "007 migration is empty"


# ─── Provenance columns ─────────────────────────────────────────────────────


def test_adds_provenance_columns(sql: str) -> None:
    for col in (
        "file_hash", "chunk_index", "chunk_total",
        "manifest_id", "writer_version", "ingested_at",
    ):
        assert re.search(rf"ADD COLUMN IF NOT EXISTS\s+{col}\b", sql), \
            f"missing ADD COLUMN for {col}"


def test_unique_index_on_filehash_chunk(sql: str) -> None:
    """Two writes with the same (file_hash, chunk_index) must collide on the index, not just on the PK."""
    assert "uq_kv_filehash_chunk" in sql
    assert "(file_hash, chunk_index)" in sql


def test_writer_version_check_constraint_matches_writer_output(sql: str) -> None:
    from temporal.activities.manifest_writer import WRITER_VERSION
    assert "ck_kv_writer_version_format" in sql
    assert re.search(r"writer_version\s+~\s+'\^v\[0-9\]\+\\\.\[0-9\]\+'", sql)
    # The writer's stamped value must satisfy the regex
    assert re.match(r"^v[0-9]+\.[0-9]+", WRITER_VERSION)


# ─── Canonical view ─────────────────────────────────────────────────────────


def test_canonical_view_filters_manifest_backed_rows(sql: str) -> None:
    assert "CREATE OR REPLACE VIEW knowledge_vectors_canonical" in sql
    assert "file_hash      IS NOT NULL" in sql
    assert "manifest_id    IS NOT NULL" in sql
    assert "writer_version IS NOT NULL" in sql


def test_canonical_view_exposes_provenance_columns(sql: str) -> None:
    """A reader of the canonical view must see provenance, not just content."""
    view_section = sql.split("CREATE OR REPLACE VIEW knowledge_vectors_canonical")[1]
    for col in ("file_hash", "chunk_index", "chunk_total", "manifest_id", "writer_version", "ingested_at"):
        assert col in view_section


# ─── ingestion_audit_log ────────────────────────────────────────────────────


def test_audit_log_table_columns(sql: str) -> None:
    assert "CREATE TABLE IF NOT EXISTS ingestion_audit_log" in sql
    for col in (
        "run_id", "event_at", "event", "stage", "batch_index", "batch_size",
        "rows_written", "rows_skipped", "rows_failed", "details",
    ):
        assert col in sql, f"audit_log column {col} missing"


# ─── Production cutover stays gated ─────────────────────────────────────────


def test_cutover_requires_explicit_guc(sql: str) -> None:
    """The production GRANT block must be gated behind a GUC the operator sets."""
    assert "app.allow_writer_v03_cutover" in sql, \
        "production cutover must be guarded by app.allow_writer_v03_cutover"
    assert "RAISE NOTICE 'Skipping production cutover" in sql
    # The body must be inside a DO $$ ... $$ block that no-ops by default.
    assert re.search(
        r"DO\s+\$\$.*?app\.allow_writer_v03_cutover.*?RETURN.*?\$\$",
        sql, re.DOTALL,
    ), "production block is not wrapped in a GUC-gated DO block"


def test_no_ungated_grant_revoke(sql: str) -> None:
    """No GRANT/REVOKE statements outside the gated DO block."""
    # Strip the DO $$ ... $$ block (only one in this migration)
    stripped = re.sub(r"DO\s+\$\$.*?\$\$;", "", sql, flags=re.DOTALL)
    for needle in ("GRANT ", "REVOKE "):
        assert needle not in stripped, \
            f"{needle.strip()} found outside the GUC-gated block — production cutover must stay gated"


def test_no_destructive_statements(sql: str) -> None:
    """The migration must not drop tables, drop the role, or truncate data."""
    # We allow DROP CONSTRAINT IF EXISTS (idempotent re-apply of the CHECK).
    forbidden = [
        r"\bDROP\s+TABLE\b",
        r"\bDROP\s+ROLE\b",
        r"\bTRUNCATE\b",
        r"\bDELETE\s+FROM\b",
    ]
    for pat in forbidden:
        assert not re.search(pat, sql, re.IGNORECASE), f"forbidden statement matched: {pat}"

# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Synthetic-data tests for ``upsert_validation_line``.

The function must:
  - insert a single VALIDATION line directly under STATUS when none exists;
  - replace an existing VALIDATION line in place;
  - collapse duplicate VALIDATION lines into one (defends against earlier bug).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from validators import core


@pytest.fixture(autouse=True)
def _patch_catalogue(tmp_path, monkeypatch):
    fake = tmp_path / "catalogue.md"
    monkeypatch.setattr(core, "CATALOGUE_PATH", fake)
    return fake


def _seed(catalogue: Path, body: str) -> None:
    catalogue.write_text(body)


def test_inserts_below_status(_patch_catalogue):
    _seed(
        _patch_catalogue,
        "**ID:** INS-006\n**STATUS:** HYPOTHESIS\n---\n**ID:** INS-007\n**STATUS:** HYPOTHESIS\n---\n",
    )
    assert core.upsert_validation_line("INS-006", "**VALIDATION:** PROVEN | x=1")
    out = _patch_catalogue.read_text()
    assert "**STATUS:** HYPOTHESIS\n**VALIDATION:** PROVEN | x=1" in out
    # INS-007 untouched
    assert out.count("**VALIDATION:**") == 1


def test_replaces_existing_validation(_patch_catalogue):
    _seed(
        _patch_catalogue,
        "**ID:** INS-006\n**STATUS:** HYPOTHESIS\n**VALIDATION:** OLD\n---\n",
    )
    assert core.upsert_validation_line("INS-006", "**VALIDATION:** NEW")
    out = _patch_catalogue.read_text()
    assert "OLD" not in out
    assert out.count("**VALIDATION:**") == 1


def test_collapses_duplicates(_patch_catalogue):
    _seed(
        _patch_catalogue,
        "**ID:** INS-006\n**STATUS:** HYPOTHESIS\n**VALIDATION:** A\n**VALIDATION:** B\n---\n",
    )
    core.upsert_validation_line("INS-006", "**VALIDATION:** C")
    assert _patch_catalogue.read_text().count("**VALIDATION:**") == 1


def test_idempotent_when_unchanged(_patch_catalogue):
    _seed(
        _patch_catalogue,
        "**ID:** INS-006\n**STATUS:** HYPOTHESIS\n**VALIDATION:** SAME\n---\n",
    )
    assert core.upsert_validation_line("INS-006", "**VALIDATION:** SAME") is False


def test_preserves_blank_line_separator(_patch_catalogue):
    """Catalogue entries follow ``...STATUS: ...\\n\\n---``. Upserts must not
    eat the blank line between the entry and its ``---`` separator.
    """
    body = "**ID:** INS-006\n**STATUS:** HYPOTHESIS\n\n---\n**ID:** INS-007\n"
    _seed(_patch_catalogue, body)
    core.upsert_validation_line("INS-006", "**VALIDATION:** OK")
    out = _patch_catalogue.read_text()
    # The blank line between the (new) VALIDATION line and the --- separator
    # must survive the rewrite.
    assert "**VALIDATION:** OK\n\n---" in out

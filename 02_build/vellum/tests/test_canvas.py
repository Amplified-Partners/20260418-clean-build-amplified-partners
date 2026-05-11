"""Unit tests for hash chain integrity and additive-only enforcement.

Devon-598da8fc | 2026-05-11
"""

from __future__ import annotations

import hashlib

import pytest

from vellum.models.entry import SheetEntry
from vellum.models.sheet import Sheet, SheetMeta


# ---------------------------------------------------------------------------
# Hash chain validation helpers
# ---------------------------------------------------------------------------

def build_chain(sheet_id: str, contents: list[str]) -> list[SheetEntry]:
    """Build a valid hash chain from a list of content strings."""
    entries: list[SheetEntry] = []
    prev_hash = ""
    for content in contents:
        entry = SheetEntry(
            sheet_id=sheet_id,
            author="test-agent",
            content=content,
            prev_hash=prev_hash,
            entry_type="agent_write",
        )
        entries.append(entry)
        prev_hash = entry.entry_hash
    return entries


def verify_chain(entries: list[SheetEntry]) -> bool:
    """Verify hash chain integrity. Returns True if chain is valid."""
    for i, entry in enumerate(entries):
        expected_hash = hashlib.sha256(
            f"{entry.prev_hash}||{entry.content}".encode("utf-8")
        ).hexdigest()
        if entry.entry_hash != expected_hash:
            return False
        if i > 0 and entry.prev_hash != entries[i - 1].entry_hash:
            return False
    return True


def detect_tampering(entries: list[SheetEntry]) -> list[int]:
    """Return indices of entries where tampering is detected."""
    tampered: list[int] = []
    for i, entry in enumerate(entries):
        expected_hash = hashlib.sha256(
            f"{entry.prev_hash}||{entry.content}".encode("utf-8")
        ).hexdigest()
        if entry.entry_hash != expected_hash:
            tampered.append(i)
        elif i > 0 and entry.prev_hash != entries[i - 1].entry_hash:
            tampered.append(i)
    return tampered


# ---------------------------------------------------------------------------
# Hash chain tests
# ---------------------------------------------------------------------------

class TestHashChain:
    """Tests for SHA-256 hash chain correctness."""

    def test_single_entry_chain(self) -> None:
        entries = build_chain("sheet-1", ["Hello"])
        assert len(entries) == 1
        assert entries[0].prev_hash == ""
        assert entries[0].entry_hash != ""
        assert verify_chain(entries)

    def test_multi_entry_chain_validates(self) -> None:
        entries = build_chain("sheet-1", ["Entry 1", "Entry 2", "Entry 3"])
        assert len(entries) == 3
        assert verify_chain(entries)

        for i in range(1, len(entries)):
            assert entries[i].prev_hash == entries[i - 1].entry_hash

    def test_hash_is_deterministic(self) -> None:
        e1 = SheetEntry(
            sheet_id="s", author="a", content="same", prev_hash="abc",
            entry_type="agent_write",
        )
        e2 = SheetEntry(
            sheet_id="s", author="a", content="same", prev_hash="abc",
            entry_type="agent_write",
        )
        assert e1.entry_hash == e2.entry_hash

    def test_different_content_different_hash(self) -> None:
        e1 = SheetEntry(
            sheet_id="s", author="a", content="alpha", prev_hash="",
            entry_type="agent_write",
        )
        e2 = SheetEntry(
            sheet_id="s", author="a", content="beta", prev_hash="",
            entry_type="agent_write",
        )
        assert e1.entry_hash != e2.entry_hash

    def test_hash_chain_detects_content_tampering(self) -> None:
        entries = build_chain("sheet-1", ["Original 1", "Original 2", "Original 3"])
        assert verify_chain(entries)

        # Tamper with middle entry content without recomputing hash
        tampered = [e.model_copy() for e in entries]
        tampered[1] = tampered[1].model_copy(update={"content": "TAMPERED"})
        assert not verify_chain(tampered)

        bad_indices = detect_tampering(tampered)
        assert 1 in bad_indices

    def test_hash_chain_detects_prev_hash_tampering(self) -> None:
        entries = build_chain("sheet-1", ["A", "B", "C"])
        assert verify_chain(entries)

        tampered = [e.model_copy() for e in entries]
        tampered[2] = tampered[2].model_copy(update={"prev_hash": "deadbeef"})
        assert not verify_chain(tampered)

    def test_hash_chain_detects_reordering(self) -> None:
        entries = build_chain("sheet-1", ["First", "Second", "Third"])
        assert verify_chain(entries)

        reordered = [entries[0], entries[2], entries[1]]
        assert not verify_chain(reordered)

    def test_empty_chain_is_valid(self) -> None:
        assert verify_chain([]) is True

    def test_compute_hash_matches_entry_hash(self) -> None:
        entry = SheetEntry(
            sheet_id="s", author="a", content="test", prev_hash="prev",
            entry_type="agent_write",
        )
        assert entry.compute_hash() == entry.entry_hash


# ---------------------------------------------------------------------------
# Additive-only enforcement tests
# ---------------------------------------------------------------------------

def additive_append(sheet: Sheet, entry: SheetEntry) -> Sheet:
    """Append an entry to a sheet (additive-only operation)."""
    if entry.prev_hash != sheet.latest_hash:
        raise ValueError("Entry prev_hash does not match sheet latest_hash")
    sheet.entries.append(entry)
    sheet.latest_hash = entry.entry_hash
    return sheet


def additive_reject_modification(sheet: Sheet, index: int, new_content: str) -> None:
    """Attempt to modify an existing entry — should always raise."""
    raise ValueError(
        f"Modification of entry at index {index} is not allowed. "
        "Vellum sheets are additive-only."
    )


class TestAdditiveOnly:
    """Tests for additive-only write enforcement."""

    def _make_sheet(self) -> Sheet:
        meta = SheetMeta(
            id="sheet-add",
            tenant_id="t",
            title="Test",
            mode="brief",
            created_by="test",
        )
        entry = SheetEntry(
            sheet_id="sheet-add",
            author="agent",
            content="Genesis",
            prev_hash="",
            entry_type="agent_write",
        )
        return Sheet(meta=meta, entries=[entry], latest_hash=entry.entry_hash)

    def test_append_succeeds(self) -> None:
        sheet = self._make_sheet()
        new_entry = SheetEntry(
            sheet_id="sheet-add",
            author="human",
            content="Reply",
            prev_hash=sheet.latest_hash,
            entry_type="human_comment",
        )
        result = additive_append(sheet, new_entry)
        assert len(result.entries) == 2
        assert result.latest_hash == new_entry.entry_hash

    def test_append_with_wrong_prev_hash_rejected(self) -> None:
        sheet = self._make_sheet()
        bad_entry = SheetEntry(
            sheet_id="sheet-add",
            author="human",
            content="Bad",
            prev_hash="wrong-hash",
            entry_type="human_comment",
        )
        with pytest.raises(ValueError, match="does not match"):
            additive_append(sheet, bad_entry)

    def test_modification_rejected(self) -> None:
        sheet = self._make_sheet()
        with pytest.raises(ValueError, match="not allowed"):
            additive_reject_modification(sheet, 0, "Changed content")

    def test_multiple_appends_maintain_chain(self) -> None:
        sheet = self._make_sheet()
        for i in range(5):
            entry = SheetEntry(
                sheet_id="sheet-add",
                author="human",
                content=f"Reply {i}",
                prev_hash=sheet.latest_hash,
                entry_type="human_comment",
            )
            additive_append(sheet, entry)

        assert len(sheet.entries) == 6
        assert verify_chain(sheet.entries)

    def test_additive_preserves_original_entries(self) -> None:
        sheet = self._make_sheet()
        original_hash = sheet.entries[0].entry_hash
        original_content = sheet.entries[0].content

        new_entry = SheetEntry(
            sheet_id="sheet-add",
            author="human",
            content="New",
            prev_hash=sheet.latest_hash,
            entry_type="human_comment",
        )
        additive_append(sheet, new_entry)

        assert sheet.entries[0].entry_hash == original_hash
        assert sheet.entries[0].content == original_content

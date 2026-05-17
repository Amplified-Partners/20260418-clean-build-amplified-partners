"""Additive-only write enforcement. No deletes, no overwrites.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from vellum.models.entry import SheetEntry


class AdditiveGuard:

    @staticmethod
    def validate_write(new_entry: SheetEntry, existing_entries: list[SheetEntry]) -> bool:
        if not existing_entries:
            return True
        expected_sheet = existing_entries[0].sheet_id
        if new_entry.sheet_id != expected_sheet:
            return False
        for existing in existing_entries:
            if new_entry.id == existing.id:
                return False
        return True

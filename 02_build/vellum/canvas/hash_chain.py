"""SHA-256 hash chain enforcement for Vellum sheets.

Every SheetEntry's hash = sha256(prev_hash || content). The chain
provides tamper-detection: alter any entry and downstream hashes break.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import hashlib

from vellum.models.entry import SheetEntry

SEPARATOR = "||"


class HashChain:

    @staticmethod
    def compute_next_hash(prev_hash: str, content: str) -> str:
        payload = f"{prev_hash}{SEPARATOR}{content}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @staticmethod
    def verify_entry(entry: SheetEntry) -> bool:
        expected = HashChain.compute_next_hash(entry.prev_hash, entry.content)
        return entry.entry_hash == expected

    @staticmethod
    def validate_chain(entries: list[SheetEntry]) -> bool:
        if not entries:
            return True
        for idx, entry in enumerate(entries):
            if not HashChain.verify_entry(entry):
                return False
            if idx == 0:
                if entry.prev_hash != "":
                    return False
            else:
                if entry.prev_hash != entries[idx - 1].entry_hash:
                    return False
        return True

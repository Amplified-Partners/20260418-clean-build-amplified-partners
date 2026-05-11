"""Sheet entry models — the atomic unit of a Vellum sheet."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class SheetEntry(BaseModel):
    """A single line/event on a Vellum sheet. Immutable once written."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    sheet_id: str
    author: str  # agent handle or human name
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prev_hash: str = ""  # sha256 of previous entry (empty for first)
    entry_hash: str = ""  # sha256(prev_hash || content)
    entry_type: Literal["agent_write", "human_comment", "emoji_reaction"] = "agent_write"

    def compute_hash(self) -> str:
        """Compute sha256(prev_hash || content) for hash chain integrity."""
        payload = f"{self.prev_hash}||{self.content}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def model_post_init(self, __context: object) -> None:
        """Auto-compute entry_hash if not provided."""
        if not self.entry_hash:
            self.entry_hash = self.compute_hash()


class HashChainEntry(BaseModel):
    """Minimal hash chain record for verification without full content."""

    entry_id: str
    prev_hash: str
    entry_hash: str
    timestamp: datetime

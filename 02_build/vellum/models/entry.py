"""Sheet entry — the atomic unit of a Vellum sheet.

Every entry is hash-chained, attributed, timestamped, and immutable.
Extended entry_types support the contact surface: emoji routing,
decisions, read receipts, and task assignments.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

EntryType = Literal[
    "agent_write",
    "human_comment",
    "emoji_reaction",
    "decision",
    "read_receipt",
    "task_created",
    "brief_summary",
    "cleaned_prompt",
    "council_question",
    "council_answer",
    "baton_pass",
]


EpistemicTier = Literal["INTUITED", "STRUCTURED", "MEASURED", "PROVEN"]


class SheetEntry(BaseModel):
    """A single line on a Vellum sheet. Immutable once written."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    sheet_id: str
    author: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prev_hash: str = ""
    entry_hash: str = ""
    entry_type: EntryType = "agent_write"
    epistemic_tier: EpistemicTier = "INTUITED"
    metadata: dict = Field(default_factory=dict)

    def compute_hash(self) -> str:
        payload = f"{self.prev_hash}||{self.content}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def model_post_init(self, __context: object) -> None:
        if not self.entry_hash:
            self.entry_hash = self.compute_hash()

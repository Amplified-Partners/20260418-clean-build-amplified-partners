"""Token models for share-link scoped access.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

TokenRole = Literal["read", "comment", "write"]


class ShareToken(BaseModel):
    """A scoped access token for a Vellum sheet share link."""

    token_id: str = Field(default_factory=lambda: str(uuid4()))
    sheet_id: str
    role: TokenRole = "read"
    bound_to: str | None = None
    expires_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    revoked: bool = False

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired

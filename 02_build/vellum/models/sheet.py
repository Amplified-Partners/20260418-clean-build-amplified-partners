"""Sheet and tenant models.

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

SheetMode = Literal["brief", "correspondence", "council"]


class SheetMeta(BaseModel):
    """Sheet metadata — the header without content."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str = "ewan"
    title: str = ""
    mode: SheetMode = "brief"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str = ""


class Sheet(BaseModel):
    """A full Vellum sheet with metadata and entries."""

    meta: SheetMeta
    entries: list = Field(default_factory=list)
    latest_hash: str = ""

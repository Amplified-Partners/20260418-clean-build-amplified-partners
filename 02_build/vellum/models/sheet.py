"""Sheet and tenant models."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class Tenant(BaseModel):
    """Tenant isolation unit. Each customer gets one."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str  # e.g. "jesmond"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SheetMeta(BaseModel):
    """Sheet metadata — the header without content."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str
    title: str
    mode: Literal["council", "correspondence", "brief"] = "brief"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: str  # agent or human who initiated


class Sheet(BaseModel):
    """A full Vellum sheet with metadata and entries."""

    meta: SheetMeta
    entries: list = Field(default_factory=list)  # list[SheetEntry]
    latest_hash: str = ""  # tip of the hash chain

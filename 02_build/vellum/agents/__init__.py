"""Researcher agents — data fetchers for Brief mode."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

from pydantic import BaseModel, Field


class ResearcherOutput(BaseModel):
    """Standard output from any researcher agent."""

    source: str  # "stripe" | "calendar" | "searxng"
    data: dict  # structured payload
    summary: str  # one-line human-readable
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Researcher(Protocol):
    """Protocol for researcher agents. All fetchers implement this."""

    async def fetch(self, tenant_id: str, date: datetime) -> ResearcherOutput:
        """Fetch data for the given tenant and date."""
        ...

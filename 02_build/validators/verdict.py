"""Verdict dataclass — the canonical shape written to disk per insight.

Every validator returns a ``Verdict`` covering one INS-NNN. Bundles are
serialised as JSON to ``03_shadow/validators/<vertical>/<INS-NNN>.json``.

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class VerdictBand(str, Enum):
    """Three-band verdict (per ticket) plus a key-blocked signal."""

    PROVEN = "PROVEN"
    PLAUSIBLE = "PLAUSIBLE"
    DISPROVEN = "DISPROVEN"
    PENDING_API_KEY = "PENDING-API-KEY"


@dataclass
class EvidenceItem:
    """One data fetch contributing to the verdict."""

    source: str
    url: str
    accessed_at: str
    http_status: int | None
    response_sha256: str | None
    query_params: dict[str, Any] = field(default_factory=dict)
    summary: str = ""


@dataclass
class Verdict:
    """Canonical verdict bundle for one catalogue entry."""

    insight_id: str
    title: str
    vertical: str
    band: VerdictBand
    test_class: str
    rationale: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    run_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    code_sha: str = "unknown"
    agent: str = "Devon-4234"
    notes: str = ""

    def to_json(self) -> str:
        payload = asdict(self)
        payload["band"] = self.band.value
        return json.dumps(payload, indent=2, sort_keys=False)

    def write(self, root: Path) -> Path:
        """Write the bundle to ``<root>/<vertical>/<INS-NNN>.json``."""
        out_dir = root / self.vertical
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{self.insight_id}.json"
        out_path.write_text(self.to_json() + "\n", encoding="utf-8")
        return out_path

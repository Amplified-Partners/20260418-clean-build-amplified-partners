"""Core verdict + evidence types for the public-data validation pipeline.

A `Verdict` is the data-backed answer to "does this insight survive contact
with real public data". Verdicts are additive to the existing literature-class
`STATUS:` field on each catalogue entry; the literature label stays put.

Signed-by: Devon-ab74 (devin-ab740f2c78ee477a9c16ea3b6ed15293) - 2026-05-03
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


def _default_signed_by() -> str:
    """Resolve the agent attribution at verdict-creation time.

    Reads ``AMP_SIGNED_BY`` from the environment so future agents (running
    on Beast cron, in a different Devin session, etc.) attribute their
    verdicts to themselves rather than baking in the original implementer.
    Falls back to a clearly-marked placeholder if the env var is unset so
    missing attribution is visible at review time rather than silently
    inheriting a stale signature.
    """
    sig = os.environ.get("AMP_SIGNED_BY")
    if sig:
        return sig
    return "unsigned (set AMP_SIGNED_BY=<agent> | <date> | <session>)"


class VerdictBand(str, Enum):
    PROVEN = "PROVEN"
    PLAUSIBLE = "PLAUSIBLE"
    DISPROVEN = "DISPROVEN"
    BLOCKED = "BLOCKED"
    DEFERRED = "DEFERRED"


class TestClass(str, Enum):
    EXISTENCE = "existence"
    BASE_RATE = "base_rate"
    CORRELATION = "correlation"
    DISTRIBUTION = "distribution"


@dataclass
class EvidenceItem:
    """A single piece of evidence backing a verdict.

    Records source URL, the snippet that was used, and a content hash so the
    verdict is reproducible even if the upstream source changes.
    """

    source: str
    url: str
    accessed_at: str
    content_sha256: str
    summary: str
    raw_path: str | None = None


@dataclass
class EvidenceBundle:
    items: list[EvidenceItem] = field(default_factory=list)

    def add(self, item: EvidenceItem) -> None:
        self.items.append(item)

    def to_dict(self) -> list[dict[str, Any]]:
        return [asdict(i) for i in self.items]


@dataclass
class Verdict:
    insight_id: str
    vertical: str
    band: VerdictBand
    test_class: TestClass
    method: str
    finding: str
    statistic: dict[str, Any] = field(default_factory=dict)
    evidence: EvidenceBundle = field(default_factory=EvidenceBundle)
    notes: list[str] = field(default_factory=list)
    run_at: str = field(
        default_factory=lambda: datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
    )
    signed_by: str = field(default_factory=_default_signed_by)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["band"] = self.band.value
        d["test_class"] = self.test_class.value
        d["evidence"] = self.evidence.to_dict()
        # Strip the absolute home-dir prefix from cached raw_path entries so
        # committed verdicts are portable. The sha256 already uniquely
        # identifies the cached body.
        try:
            home = str(Path.home())
        except (RuntimeError, OSError):
            home = ""
        if home:
            for item in d["evidence"]:
                rp = item.get("raw_path")
                if isinstance(rp, str) and rp.startswith(home):
                    item["raw_path"] = "~" + rp[len(home):]
        return d


def write_verdict(verdict: Verdict, output_root: Path) -> Path:
    """Write a verdict and its evidence bundle to disk.

    Layout: ``output_root/<vertical>/<insight_id>/verdict.json``
    """
    target_dir = output_root / verdict.vertical.lower() / verdict.insight_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "verdict.json"
    with target_path.open("w", encoding="utf-8") as fh:
        json.dump(verdict.to_dict(), fh, indent=2, sort_keys=True)
        fh.write("\n")
    return target_path


def catalogue_line(verdict: Verdict, evidence_relpath: str) -> str:
    """Render the one-line `VALIDATION:` field for the catalogue.

    The literature `STATUS:` field on each entry is preserved unchanged; this
    line is added immediately below it.
    """
    accessed = verdict.run_at.split("T", 1)[0]
    return (
        f"**VALIDATION:** {verdict.band.value} | {verdict.test_class.value} "
        f"| accessed {accessed} | evidence: `{evidence_relpath}`"
    )

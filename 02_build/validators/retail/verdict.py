# Authored by Devon-9a6b, 2026-05-03 (session devin-9a6bd256bd7c4a90a083a471fa94a810)
"""Verdict object + writer.

Each insight runner returns a Verdict. The runner CLI persists every verdict
to results/<INS-NNN>/verdict.json with a stable schema so it can be picked up
later by the catalogue updater and the master report.
"""
from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RESULTS_ROOT = Path(__file__).resolve().parent / "results"
RESULTS_ROOT.mkdir(parents=True, exist_ok=True)


def _default_signed_by() -> str:
    """Resolve the agent signature at verdict-creation time.

    Mirrors the shared ``02_build/validators/core.py::_default_signed_by``
    pattern so re-runs by other agents (Beast cron, a different Devin
    session, OpenClaw, …) attribute their verdicts to themselves rather
    than baking in the original implementer's identity. Reads
    ``AMP_SIGNED_BY`` from the environment; falls back to a clearly-marked
    placeholder so missing attribution is visible at review time per
    ``00_authority/SIGNATURES.md`` ("Every AI signs every artefact it
    commits") rather than silently inheriting a stale signature.
    """
    sig = os.environ.get("AMP_SIGNED_BY")
    if sig:
        return sig
    return "unsigned (set AMP_SIGNED_BY=<agent> | <date> | <session>)"


def _default_session_id() -> str:
    """Resolve the Devin session id at verdict-creation time.

    Same rationale as ``_default_signed_by``: hard-coding ties every
    re-run's metadata to the original session even when a different
    session is doing the work. Reads ``AMP_SESSION_ID`` from the
    environment; falls back to a placeholder rather than a stale ID.
    """
    sid = os.environ.get("AMP_SESSION_ID")
    if sid:
        return sid
    return "unset (set AMP_SESSION_ID=devin-<uuid>)"


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(Path(__file__).resolve().parent),
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return "unknown"


@dataclass
class Verdict:
    insight_id: str           # e.g. INS-067
    title: str
    vertical: str             # 'Retail'
    verdict: str              # PROVEN | PLAUSIBLE | DISPROVEN | DEFERRED
    test_class: str           # base_rate | correlation | distribution | existence | manual
    summary: str              # one-line
    evidence: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    confidence: int = 70      # 0-100, OPINION confidence per 00_authority/OPINION_CONFIDENCE.md
    run_at_utc: str = ""
    git_sha: str = ""
    session_id: str = field(default_factory=_default_session_id)
    signed_by: str = field(default_factory=_default_signed_by)

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    def write(self) -> Path:
        if not self.run_at_utc:
            self.run_at_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if not self.git_sha:
            self.git_sha = _git_sha()
        out_dir = RESULTS_ROOT / self.insight_id
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "verdict.json"
        path.write_text(json.dumps(self.to_dict(), indent=2, default=str))
        return path


VERDICT_BANDS = ("PROVEN", "PLAUSIBLE", "DISPROVEN", "DEFERRED", "BLOCKED")

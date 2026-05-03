# Authored by Devon-6264, 2026-05-03 (session devin-6264b0ba42c6453b86b166bebc3d868a)
"""Verdict, evidence, cache, and catalogue helpers shared across validators."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import os
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

logger = logging.getLogger("validators.core")


REPO_ROOT = Path(__file__).resolve().parents[4]
RESULTS_DIR = REPO_ROOT / "02_build" / "validators" / "results"
EVIDENCE_DIR = REPO_ROOT / "03_shadow" / "validators"
CACHE_DIR = EVIDENCE_DIR / "cache"
CATALOGUE_PATH = (
    REPO_ROOT
    / "01_truth"
    / "schemas"
    / "research-index"
    / "00-insight-catalogue_v1.md"
)


class VerdictBand(StrEnum):
    """The three-band verdict scheme.

    See ``01_truth/schemas/2026-05_public-data-validation_v1.md``.
    """

    PROVEN = "PROVEN"
    PLAUSIBLE = "PLAUSIBLE"
    DISPROVEN = "DISPROVEN"
    SKIPPED = "SKIPPED"


@dataclass
class SourceRef:
    """One source reference used to derive a verdict."""

    name: str
    url: str
    accessed_at: str
    query_params: Mapping[str, Any] = field(default_factory=dict)
    response_hash: str = ""


@dataclass
class Evidence:
    """Aggregate evidence backing a single verdict."""

    sources: list[SourceRef] = field(default_factory=list)
    metric: str = ""
    notes: str = ""
    raw_pointer: str = ""

    def add_source(self, source: SourceRef) -> None:
        self.sources.append(source)


@dataclass
class Verdict:
    """A data-backed verdict for a single insight."""

    insight_id: str
    verdict: VerdictBand
    test_class: str
    evidence: Evidence
    verdict_at: str = ""
    code_sha: str = ""
    reason: str = ""

    def __post_init__(self) -> None:
        if not self.verdict_at:
            self.verdict_at = datetime.now(UTC).date().isoformat()
        if not self.code_sha:
            self.code_sha = _git_sha()

    def as_dict(self) -> dict[str, Any]:
        d = dataclasses.asdict(self)
        d["verdict"] = self.verdict.value
        return d

    def write(self) -> Path:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        out = RESULTS_DIR / f"{self.insight_id}.json"
        out.write_text(json.dumps(self.as_dict(), indent=2, sort_keys=False) + "\n")
        return out


def skipped(insight_id: str, reason: str, test_class: str = "existence") -> Verdict:
    """Build (and persist) a ``SKIPPED`` verdict (e.g. when an API key is missing)."""
    verdict = Verdict(
        insight_id=insight_id,
        verdict=VerdictBand.SKIPPED,
        test_class=test_class,
        evidence=Evidence(notes=reason),
        reason=reason,
    )
    verdict.write()
    return verdict


# --------------------------------------------------------------------------- #
# Cache (content-addressed by query hash)                                     #
# --------------------------------------------------------------------------- #


def cache_key(*parts: Any) -> str:
    """Deterministic content hash from heterogeneous query parts.

    Non-cryptographic: this is content-addressing for HTTP response caching, not
    password hashing. Callers MUST NOT pass auth headers or API keys — those
    don't change response *content* for our public-data sources, and including
    them would risk fingerprinting credentials in cache filenames.
    """
    payload = json.dumps([_canon(p) for p in parts], sort_keys=True, default=str)
    return hashlib.sha256(payload.encode(), usedforsecurity=False).hexdigest()[:24]


def _canon(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _canon(v) for k, v in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_canon(v) for v in value]
    return value


def cache_path(source: str, key: str, suffix: str = ".bin") -> Path:
    bucket = CACHE_DIR / source
    bucket.mkdir(parents=True, exist_ok=True)
    return bucket / f"{key}{suffix}"


def cache_read(path: Path) -> bytes | None:
    if not path.exists():
        return None
    return path.read_bytes()


def cache_write(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def hash_response(data: bytes) -> str:
    """Short content fingerprint of a response body.

    Non-cryptographic: used only for verdict reproducibility — re-runs that
    return identical bytes produce identical fingerprints.
    """
    return hashlib.sha256(data, usedforsecurity=False).hexdigest()[:24]


# --------------------------------------------------------------------------- #
# Catalogue helpers                                                           #
# --------------------------------------------------------------------------- #


def list_trades_insight_ids() -> list[str]:
    """All ``INS-NNN`` IDs in the trades vertical (INS-001 to INS-032)."""
    return [f"INS-{i:03d}" for i in range(1, 33)]


def parse_insight_block(insight_id: str) -> dict[str, str]:
    """Pull the catalogue block for ``insight_id`` into a flat dict.

    Field names (``INTERNAL DATA``, ``PUBLIC DATA`` …) become keys; values are
    the rest of the line. The block is delimited by ``---`` separators.
    """
    text = CATALOGUE_PATH.read_text()
    needle = f"**ID:** {insight_id}\n"
    idx = text.find(needle)
    if idx < 0:
        raise KeyError(f"Insight {insight_id} not found in catalogue")
    end = text.find("\n---", idx)
    block = text[idx : end if end > 0 else len(text)]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if line.startswith("**") and ":**" in line:
            key, _, val = line.partition(":**")
            out[key.strip("* ").strip()] = val.strip()
    return out


def upsert_validation_line(insight_id: str, line: str) -> bool:
    """Insert or replace the ``VALIDATION:`` line under the named ``STATUS:``.

    Returns True if the catalogue file was modified.
    """
    text = CATALOGUE_PATH.read_text()
    needle = f"**ID:** {insight_id}\n"
    idx = text.find(needle)
    if idx < 0:
        raise KeyError(f"Insight {insight_id} not found in catalogue")
    block_end = text.find("\n---", idx)
    block_end = block_end if block_end > 0 else len(text)
    block = text[idx:block_end]

    new_validation = line if line.startswith("**VALIDATION:**") else f"**VALIDATION:** {line}"

    lines = block.splitlines()
    has_validation = any(c.startswith("**VALIDATION:**") for c in lines)

    out_lines: list[str] = []
    inserted = False
    for current in lines:
        if current.startswith("**VALIDATION:**"):
            if not inserted:
                out_lines.append(new_validation)
                inserted = True
            # Drop any subsequent duplicate VALIDATION lines.
            continue
        out_lines.append(current)
        if (
            not has_validation
            and not inserted
            and current.startswith("**STATUS:**")
        ):
            out_lines.append(new_validation)
            inserted = True
    if not inserted:
        logger.warning("No STATUS: anchor in %s — appending VALIDATION at block end", insight_id)
        out_lines.append(new_validation)
    # Preserve the original block's trailing newline run. ``splitlines()`` /
    # ``"\n".join()`` drops trailing newlines, so we re-attach them — this
    # both keeps the blank-line separator before ``\n---`` and makes the
    # below equality check apples-to-apples (so re-runs short-circuit).
    trailing = block[len(block.rstrip("\n")) :]
    new_block_with_trailing = "\n".join(out_lines) + trailing
    if new_block_with_trailing == block:
        return False
    new_text = text[:idx] + new_block_with_trailing + text[block_end:]
    CATALOGUE_PATH.write_text(new_text)
    return True


# --------------------------------------------------------------------------- #
# Internals                                                                   #
# --------------------------------------------------------------------------- #


def _git_sha() -> str:
    """Best-effort short SHA of HEAD; empty string if git unavailable."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short=12", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return os.environ.get("GIT_SHA", "")


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")

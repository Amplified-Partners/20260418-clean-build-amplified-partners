#!/usr/bin/env python3
"""
Path Abstraction — Cross-repo path resolution for the APDS pipeline.

The APDS pipeline spans multiple repositories (clean-build, crm, corpus-raw,
marketing-engine) and needs to reference files, schemas, and data across all
of them. This module provides a single resolution layer so adapters never
hard-code absolute paths.

Resolution order:
    1. Environment variable overrides (AMPLIFIED_REPO_<NAME>).
    2. Sibling-directory convention (/home/ubuntu/repos/<name>/).
    3. Fallback to clean-build-relative paths.

Usage:
    from path_abstraction import repo_path, resolve, APDS_PATHS

    harvester_dir = repo_path("clean-build") / "02_build" / "routing"
    schema_file   = resolve("apds_spec")
    porch_dir     = APDS_PATHS["porch_incoming"]

Signed-by: Devon (Devin session f32d587cc3e54f959c5309d93f72bc97) - 2026-05-01
"""

from __future__ import annotations

import os
from pathlib import Path


# ---------------------------------------------------------------------------
# Repository roots
# ---------------------------------------------------------------------------

_REPO_ENV_PREFIX = "AMPLIFIED_REPO_"

_KNOWN_REPOS: dict[str, str] = {
    "clean-build": "Amplified-Partners/clean-build",
    "crm": "Amplified-Partners/crm",
    "corpus-raw": "Amplified-Partners/corpus-raw",
    "marketing-engine": "Amplified-Partners/marketing-engine",
}

_DEFAULT_PARENT = Path(os.getenv("AMPLIFIED_REPOS_ROOT", "/home/ubuntu/repos"))


def repo_path(name: str) -> Path:
    """Return the local checkout path for a named repository.

    Checks ``AMPLIFIED_REPO_<NAME>`` first, then falls back to
    ``<AMPLIFIED_REPOS_ROOT>/<name>/``.

    Raises ``FileNotFoundError`` if the resolved directory does not exist.
    """
    env_key = f"{_REPO_ENV_PREFIX}{name.upper().replace('-', '_')}"
    env_val = os.getenv(env_key)
    if env_val:
        p = Path(env_val)
    else:
        p = _DEFAULT_PARENT / name

    if not p.is_dir():
        raise FileNotFoundError(
            f"Repository '{name}' not found at {p}. "
            f"Set {env_key} or check AMPLIFIED_REPOS_ROOT."
        )
    return p


# ---------------------------------------------------------------------------
# Well-known paths inside the APDS ecosystem
# ---------------------------------------------------------------------------

def _clean_build() -> Path:
    return repo_path("clean-build")


APDS_PATHS: dict[str, Path] = {}


def _build_paths() -> None:
    """Populate APDS_PATHS lazily on first access.

    Lazy because repo_path() checks existence — we don't want import-time
    crashes if a repo isn't cloned yet.
    """
    if APDS_PATHS:
        return

    try:
        cb = _clean_build()
    except FileNotFoundError:
        return

    APDS_PATHS.update({
        # Spec & schema references
        "apds_spec": cb / "90_archive" / "specifications" / "mac-drop-2026-04" / "AMPLIFIED-PUDDING-DISCOVERY-SYSTEM.md",
        "pudding_schema": cb / "01_truth" / "schemas" / "2026-03_pudding-discovery-system_v1.md",
        "systems_register": cb / "01_truth" / "SYSTEMS-AND-API-REGISTER.md",  # Created in PR #22; available after merge

        # Build artefacts
        "scripts_dir": cb / "02_build" / "scripts",
        "routing_dir": cb / "02_build" / "routing",
        "nightscout_dir": cb / "02_build" / "cove-orchestrator" / "nightscout",

        # Porch directories (Beast filesystem convention)
        "porch_incoming": Path(os.getenv("PORCH_INCOMING", "/opt/amplified-machine/porch/incoming")),
        "porch_labeled": Path(os.getenv("PORCH_LABELED", "/opt/amplified-machine/porch/labeled")),
        "porch_ingested": Path(os.getenv("PORCH_INGESTED", "/opt/amplified-machine/porch/ingested")),
        "porch_failed": Path(os.getenv("PORCH_FAILED", "/opt/amplified-machine/porch/failed")),

        # Authority
        "manifest": cb / "00_authority" / "MANIFEST.md",
        "decision_log": cb / "00_authority" / "DECISION_LOG.md",
        "signatures": cb / "00_authority" / "SIGNATURES.md",
    })

    # Optional repos — add if present
    for name in ("crm", "corpus-raw", "marketing-engine"):
        try:
            APDS_PATHS[name] = repo_path(name)
        except FileNotFoundError:
            pass


# ---------------------------------------------------------------------------
# High-level resolver
# ---------------------------------------------------------------------------

_ALIASES: dict[str, str] = {
    "spec": "apds_spec",
    "schema": "pudding_schema",
    "register": "systems_register",
    "scripts": "scripts_dir",
    "routing": "routing_dir",
    "nightscout": "nightscout_dir",
}


def resolve(name: str) -> Path:
    """Resolve a well-known APDS path by name or alias.

    >>> resolve("apds_spec")
    PosixPath('/home/ubuntu/repos/clean-build/90_archive/specifications/...')
    >>> resolve("spec")          # alias
    PosixPath('/home/ubuntu/repos/clean-build/90_archive/specifications/...')

    Raises ``KeyError`` if the name is not recognised.
    """
    _build_paths()
    canonical = _ALIASES.get(name, name)
    if canonical not in APDS_PATHS:
        raise KeyError(
            f"Unknown APDS path '{name}'. "
            f"Known: {sorted(APDS_PATHS.keys())}. "
            f"Aliases: {sorted(_ALIASES.keys())}."
        )
    return APDS_PATHS[canonical]


# ---------------------------------------------------------------------------
# Beast infrastructure endpoints (env-var driven)
# ---------------------------------------------------------------------------

class BeastEndpoints:
    """Connection strings for Beast services used by the APDS pipeline."""

    searxng_url: str = os.getenv("SEARXNG_URL", "http://searxng:8888")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://ollama:11434")
    litellm_url: str = os.getenv("LITELLM_URL", "http://litellm:4000")
    falkordb_host: str = os.getenv("FALKORDB_HOST", "falkordb")
    falkordb_port: int = int(os.getenv("FALKORDB_PORT", "6379"))
    postgres_dsn: str = os.getenv(
        "POSTGRES_DSN",
        "postgresql://cove:cove@postgres:5432/cove",
    )
    minio_host: str = os.getenv("MINIO_HOST", "minio")
    langfuse_url: str = os.getenv("LANGFUSE_URL", "http://langfuse:3000")


BEAST = BeastEndpoints()

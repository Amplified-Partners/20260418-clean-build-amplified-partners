"""Canonical manifest-first ingestion (AMP-302).

Doctrine: Disk source material = truth; Manifest = proof; DB = rebuildable index.

Signed-by: Claude Code instance A | 2026-05-11 | AMP-302
"""

from .manifest_generator import (
    PIPELINE_VERSION,
    SIGNED_BY,
    ChunkRecord,
    FileManifest,
    ManifestGenerator,
    ManifestRunSummary,
    chunk_text,
    file_sha256,
    generate_manifest,
)

__all__ = [
    "PIPELINE_VERSION",
    "SIGNED_BY",
    "ChunkRecord",
    "FileManifest",
    "ManifestGenerator",
    "ManifestRunSummary",
    "chunk_text",
    "file_sha256",
    "generate_manifest",
]

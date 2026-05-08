"""Filesystem inspection tools — vault roots, raw dumps, ingestion paths, find, hash, summarise.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from .. import config
from ..audit import log_tool_call


def list_vault_roots() -> str:
    """List known vault directories with file counts and total size."""
    log_tool_call("list_vault_roots", {})
    return _summarise_roots(config.VAULT_ROOTS, "vault")


def list_raw_dump_roots() -> str:
    """List known raw dump directories with file counts and total size."""
    log_tool_call("list_raw_dump_roots", {})
    return _summarise_roots(config.RAW_DUMP_ROOTS, "raw_dump")


def list_ingestion_roots() -> str:
    """List known ingestion directories with file counts and total size."""
    log_tool_call("list_ingestion_roots", {})
    return _summarise_roots(config.INGESTION_ROOTS, "ingestion")


def _summarise_roots(roots: list[str], category: str) -> str:
    results: list[dict] = []
    for root in roots:
        p = Path(root)
        entry: dict = {"path": root, "category": category, "exists": p.exists()}
        if p.exists() and p.is_dir():
            try:
                file_count = sum(1 for _ in p.rglob("*") if _.is_file())
                dir_count = sum(1 for _ in p.rglob("*") if _.is_dir())
                entry["file_count"] = file_count
                entry["dir_count"] = dir_count
            except OSError as exc:
                entry["error"] = str(exc)
        results.append(entry)
    return json.dumps(results, indent=2)


def list_recent_files(path: str, limit: int = 100) -> str:
    """List most recently modified files under a path, newest first.

    Args:
        path: Directory to scan (must be under read allowlist).
        limit: Max files to return (default 100, max 500).
    """
    limit = min(max(limit, 1), 500)
    log_tool_call("list_recent_files", {"path": path, "limit": limit})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    p = Path(path)
    if not p.exists() or not p.is_dir():
        return json.dumps({"error": f"Not a directory: {path}"})
    try:
        proc = subprocess.run(
            ["find", str(p), "-maxdepth", "5", "-type", "f", "-printf", "%T@\t%p\n"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        lines = proc.stdout.strip().splitlines()
        entries = []
        for line in lines:
            parts = line.split("\t", 1)
            if len(parts) == 2:
                entries.append((float(parts[0]), parts[1]))
        entries.sort(key=lambda x: x[0], reverse=True)
        results = []
        for ts, filepath in entries[:limit]:
            from datetime import datetime, timezone

            results.append(
                {
                    "path": filepath,
                    "modified": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(),
                }
            )
        return json.dumps(results, indent=2)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def find_files(root: str, pattern: str, limit: int = 500) -> str:
    """Find files matching a glob pattern under a root path.

    Args:
        root: Directory to search (must be under read allowlist).
        pattern: Glob pattern (e.g. '*.py', '*.yml', 'docker-compose*').
        limit: Max results (default 500).
    """
    limit = min(max(limit, 1), 500)
    log_tool_call("find_files", {"root": root, "pattern": pattern, "limit": limit})
    if not config.is_read_allowed(root):
        return json.dumps({"error": f"Path not in read allowlist: {root}"})
    p = Path(root)
    if not p.exists():
        return json.dumps({"error": f"Path does not exist: {root}"})
    try:
        proc = subprocess.run(
            ["find", str(p), "-maxdepth", "6", "-name", pattern, "-type", "f"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        files = [f.strip() for f in proc.stdout.strip().splitlines() if f.strip()][:limit]
        return json.dumps(
            {"root": root, "pattern": pattern, "count": len(files), "files": files}, indent=2
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def hash_file(path: str) -> str:
    """Return the SHA-256 hash of a file (must be under read allowlist)."""
    log_tool_call("hash_file", {"path": path})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    p = Path(path)
    if not p.exists() or not p.is_file():
        return json.dumps({"error": f"Not a file: {path}"})
    try:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return json.dumps({"path": path, "sha256": h.hexdigest(), "size_bytes": p.stat().st_size})
    except OSError as exc:
        return json.dumps({"error": str(exc)})


def summarise_directory_counts(path: str) -> str:
    """Summarise a directory: file counts by extension, total size, subdirectory listing.

    Args:
        path: Directory to summarise (must be under read allowlist).
    """
    log_tool_call("summarise_directory_counts", {"path": path})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    p = Path(path)
    if not p.exists() or not p.is_dir():
        return json.dumps({"error": f"Not a directory: {path}"})
    try:
        ext_counts: dict[str, int] = {}
        total_size = 0
        file_count = 0
        for f in p.rglob("*"):
            if f.is_file():
                file_count += 1
                ext = f.suffix.lower() or "(no extension)"
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
                try:
                    total_size += f.stat().st_size
                except OSError:
                    pass
        subdirs = sorted([d.name for d in p.iterdir() if d.is_dir()])[:100]
        sorted_exts = sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)
        return json.dumps(
            {
                "path": path,
                "total_files": file_count,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 1),
                "extensions": dict(sorted_exts[:30]),
                "subdirectories": subdirs,
            },
            indent=2,
        )
    except OSError as exc:
        return json.dumps({"error": str(exc)})


def list_secret_names() -> str:
    """List filenames in the secrets directory. Never returns file contents."""
    log_tool_call("list_secret_names", {})
    p = config.SECRETS_DIR
    if not p.exists():
        return json.dumps({"error": f"Secrets directory not found: {p}", "names": []})
    try:
        names = sorted([f.name for f in p.iterdir() if f.is_file()])
        return json.dumps({"secrets_dir": str(p), "count": len(names), "names": names}, indent=2)
    except OSError as exc:
        return json.dumps({"error": str(exc)})

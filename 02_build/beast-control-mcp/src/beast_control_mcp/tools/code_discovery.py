"""Code and repo discovery tools — git repos, Python services, FastAPI apps.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .. import config
from ..audit import log_tool_call


def _find_git_repos() -> list[Path]:
    """Find all git repos under known roots."""
    repos: list[Path] = []
    seen: set[str] = set()
    for root in config.REPO_SEARCH_ROOTS:
        if not root.exists():
            continue
        try:
            proc = subprocess.run(
                ["find", str(root), "-maxdepth", "4", "-name", ".git", "-type", "d"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            for line in proc.stdout.strip().splitlines():
                repo_dir = Path(line.strip()).parent
                resolved = str(repo_dir.resolve())
                if resolved not in seen:
                    seen.add(resolved)
                    repos.append(repo_dir)
        except (subprocess.TimeoutExpired, OSError):
            continue
    return sorted(repos, key=lambda p: str(p))


def list_repos() -> str:
    """List all git repositories found under Beast paths."""
    log_tool_call("list_repos", {})
    repos = _find_git_repos()
    results: list[dict] = []
    for repo in repos:
        entry: dict = {"path": str(repo)}
        # Get current branch
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo), "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            entry["branch"] = proc.stdout.strip()
        except (subprocess.TimeoutExpired, OSError):
            entry["branch"] = "unknown"
        # Get remote
        try:
            proc = subprocess.run(
                ["git", "-C", str(repo), "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            entry["remote"] = proc.stdout.strip()
        except (subprocess.TimeoutExpired, OSError):
            entry["remote"] = ""
        results.append(entry)
    return json.dumps(results, indent=2)


def repo_status(path: str) -> str:
    """Get git status for a repository.

    Args:
        path: Path to the git repository.
    """
    log_tool_call("repo_status", {"path": path})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    try:
        proc = subprocess.run(
            ["git", "-C", path, "status", "--porcelain", "--branch"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = proc.stdout.strip().splitlines()
        branch_line = lines[0] if lines else ""
        changes = lines[1:] if len(lines) > 1 else []
        return json.dumps(
            {
                "path": path,
                "branch": branch_line,
                "changes": changes,
                "clean": len(changes) == 0,
            },
            indent=2,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def repo_recent_commits(path: str, limit: int = 20) -> str:
    """Get recent commits from a git repository.

    Args:
        path: Path to the git repository.
        limit: Number of commits to return (default 20, max 100).
    """
    limit = min(max(limit, 1), 100)
    log_tool_call("repo_recent_commits", {"path": path, "limit": limit})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    try:
        proc = subprocess.run(
            ["git", "-C", path, "log", f"-{limit}", "--format=%H\t%ai\t%an\t%s"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        commits: list[dict] = []
        for line in proc.stdout.strip().splitlines():
            parts = line.split("\t", 3)
            if len(parts) == 4:
                commits.append(
                    {
                        "hash": parts[0][:12],
                        "date": parts[1],
                        "author": parts[2],
                        "message": parts[3][:200],
                    }
                )
        return json.dumps({"path": path, "commits": commits}, indent=2)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def repo_search(path: str, query: str, limit: int = 100) -> str:
    """Search for a string in a git repository using grep.

    Args:
        path: Path to the git repository.
        query: Search string.
        limit: Max matching lines (default 100).
    """
    limit = min(max(limit, 1), 100)
    log_tool_call("repo_search", {"path": path, "query": query[:100], "limit": limit})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    try:
        proc = subprocess.run(
            ["git", "-C", path, "grep", "-n", "-I", "--max-count", str(limit), query],
            capture_output=True,
            text=True,
            timeout=15,
        )
        matches = proc.stdout.strip().splitlines()[:limit]
        return json.dumps(
            {"path": path, "query": query, "match_count": len(matches), "matches": matches},
            indent=2,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def repo_find_files(path: str, pattern: str, limit: int = 100) -> str:
    """Find files matching a pattern in a git repository.

    Args:
        path: Path to the git repository.
        pattern: Glob pattern (e.g. '*.py', 'docker-compose*').
        limit: Max files to return (default 100).
    """
    limit = min(max(limit, 1), 100)
    log_tool_call("repo_find_files", {"path": path, "pattern": pattern, "limit": limit})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    try:
        proc = subprocess.run(
            ["find", path, "-maxdepth", "5", "-name", pattern, "-type", "f"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        files = [f.strip() for f in proc.stdout.strip().splitlines() if f.strip()][:limit]
        return json.dumps(
            {"path": path, "pattern": pattern, "count": len(files), "files": files}, indent=2
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def list_python_services() -> str:
    """Find all Python services on Beast — looks for main.py, app.py, server.py, pyproject.toml."""
    log_tool_call("list_python_services", {})
    services: list[dict] = []
    seen: set[str] = set()
    markers = ["main.py", "app.py", "server.py", "pyproject.toml", "setup.py", "requirements.txt"]
    for root in config.REPO_SEARCH_ROOTS:
        if not root.exists():
            continue
        for marker in markers:
            try:
                proc = subprocess.run(
                    ["find", str(root), "-maxdepth", "5", "-name", marker, "-type", "f"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                for line in proc.stdout.strip().splitlines():
                    p = Path(line.strip())
                    svc_dir = str(p.parent)
                    if svc_dir not in seen:
                        seen.add(svc_dir)
                        services.append(
                            {
                                "path": svc_dir,
                                "marker": marker,
                            }
                        )
            except (subprocess.TimeoutExpired, OSError):
                continue
    return json.dumps(services, indent=2)


def list_fastapi_apps() -> str:
    """Find FastAPI applications by searching for 'FastAPI' or 'fastapi' imports."""
    log_tool_call("list_fastapi_apps", {})
    apps: list[dict] = []
    for root in config.REPO_SEARCH_ROOTS:
        if not root.exists():
            continue
        try:
            proc = subprocess.run(
                ["grep", "-rl", "--include=*.py", "-m", "1", "FastAPI", str(root)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            for line in proc.stdout.strip().splitlines():
                filepath = line.strip()
                if filepath:
                    apps.append({"file": filepath, "directory": str(Path(filepath).parent)})
        except (subprocess.TimeoutExpired, OSError):
            continue
    return json.dumps(apps[:50], indent=2)


def list_requirements() -> str:
    """Find all requirements.txt and pyproject.toml files on Beast."""
    log_tool_call("list_requirements", {})
    results: list[dict] = []
    for root in config.REPO_SEARCH_ROOTS:
        if not root.exists():
            continue
        try:
            proc = subprocess.run(
                [
                    "find",
                    str(root),
                    "-maxdepth",
                    "4",
                    "(",
                    "-name",
                    "requirements*.txt",
                    "-o",
                    "-name",
                    "pyproject.toml",
                    ")",
                    "-type",
                    "f",
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            for line in proc.stdout.strip().splitlines():
                if line.strip():
                    p = Path(line.strip())
                    results.append(
                        {
                            "path": str(p),
                            "name": p.name,
                            "size_bytes": p.stat().st_size if p.exists() else 0,
                        }
                    )
        except (subprocess.TimeoutExpired, OSError):
            continue
    return json.dumps(results, indent=2)

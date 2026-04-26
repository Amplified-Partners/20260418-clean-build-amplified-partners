"""Filesystem MCP Server — workspace file operations for agents."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

SERVICE_NAME = "filesystem"

mcp = FastMCP(
    SERVICE_NAME,
    instructions=(
        "Filesystem MCP server for Amplified Partners. "
        "Provides safe file operations within the workspace: "
        "listing, reading, writing, searching. All paths are sandboxed."
    ),
)

# Sandboxed workspace root — agents can only access files under this path
WORKSPACE_ROOT = Path(os.environ.get("WORKSPACE_ROOT", "/app/workspace"))
MAX_FILE_SIZE = 1_000_000  # 1MB read limit
MAX_WRITE_SIZE = 500_000   # 500KB write limit


def _safe_path(requested: str) -> Path:
    """Resolve path and ensure it's within WORKSPACE_ROOT. Raises ValueError if escape."""
    resolved = (WORKSPACE_ROOT / requested).resolve()
    if not str(resolved).startswith(str(WORKSPACE_ROOT.resolve())):
        raise ValueError(f"Path escape attempt blocked: {requested}")
    return resolved


# ─── Tool: List Directory ───────────────────────────────────────────


class ListDirInput(BaseModel):
    path: str = Field(default=".", description="Relative path within workspace (default: root)")
    recursive: bool = Field(default=False, description="List recursively")
    max_depth: int = Field(default=3, ge=1, le=10, description="Max recursion depth")


@mcp.tool(
    name=f"{SERVICE_NAME}_list",
    description="List files and directories in the workspace. Paths are relative to workspace root.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def list_dir(input: ListDirInput) -> str:
    try:
        target = _safe_path(input.path)
        if not target.exists():
            return json.dumps({"error": f"Path not found: {input.path}"})
        if not target.is_dir():
            return json.dumps({"error": f"Not a directory: {input.path}"})

        entries: list[dict[str, Any]] = []

        def _scan(p: Path, depth: int = 0) -> None:
            if depth > input.max_depth:
                return
            try:
                for item in sorted(p.iterdir()):
                    rel = str(item.relative_to(WORKSPACE_ROOT))
                    entry: dict[str, Any] = {
                        "name": item.name,
                        "path": rel,
                        "type": "dir" if item.is_dir() else "file",
                    }
                    if item.is_file():
                        entry["size"] = item.stat().st_size
                    entries.append(entry)
                    if item.is_dir() and input.recursive and depth < input.max_depth:
                        _scan(item, depth + 1)
            except PermissionError:
                entries.append({"path": str(p.relative_to(WORKSPACE_ROOT)), "error": "permission denied"})

        _scan(target)

        return json.dumps({
            "workspace_root": str(WORKSPACE_ROOT),
            "path": input.path,
            "count": len(entries),
            "entries": entries[:500],  # Cap at 500 entries
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Tool: Read File ────────────────────────────────────────────────


class ReadFileInput(BaseModel):
    path: str = Field(description="Relative path to file within workspace")
    max_lines: int = Field(default=500, ge=1, le=5000, description="Max lines to return")
    offset: int = Field(default=0, ge=0, description="Line offset to start from")


@mcp.tool(
    name=f"{SERVICE_NAME}_read",
    description="Read a file from the workspace. Returns content with line numbers. LAYER 0 RULE: Remember to cite the file explicitly if you use its contents.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def read_file(input: ReadFileInput) -> str:
    try:
        target = _safe_path(input.path)
        if not target.exists():
            return json.dumps({"error": f"File not found: {input.path}"})
        if not target.is_file():
            return json.dumps({"error": f"Not a file: {input.path}"})
        if target.stat().st_size > MAX_FILE_SIZE:
            return json.dumps({"error": f"File too large ({target.stat().st_size} bytes). Max: {MAX_FILE_SIZE}"})

        content = target.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        total = len(lines)
        selected = lines[input.offset:input.offset + input.max_lines]

        return json.dumps({
            "path": input.path,
            "total_lines": total,
            "offset": input.offset,
            "lines_returned": len(selected),
            "content": "\n".join(f"{input.offset + i + 1:>5} | {line}" for i, line in enumerate(selected)),
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except UnicodeDecodeError:
        return json.dumps({"error": "Binary file — cannot read as text"})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Tool: Write File ───────────────────────────────────────────────


class WriteFileInput(BaseModel):
    path: str = Field(description="Relative path to write within workspace")
    content: str = Field(description="File content to write")
    create_dirs: bool = Field(default=True, description="Create parent directories if needed")


@mcp.tool(
    name=f"{SERVICE_NAME}_write",
    description="Write content to a file in the workspace. PRIVACY RULE: Never write client PII or sensitive data to the filesystem.",
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def write_file(input: WriteFileInput) -> str:
    try:
        if len(input.content.encode("utf-8")) > MAX_WRITE_SIZE:
            return json.dumps({"error": f"Content too large. Max: {MAX_WRITE_SIZE} bytes"})

        target = _safe_path(input.path)
        if input.create_dirs:
            target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(input.content, encoding="utf-8")

        return json.dumps({
            "path": input.path,
            "size": target.stat().st_size,
            "lines": len(input.content.splitlines()),
            "status": "written",
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Tool: Search Files ─────────────────────────────────────────────


class SearchInput(BaseModel):
    query: str = Field(description="Text to search for in file contents")
    path: str = Field(default=".", description="Directory to search in")
    glob_pattern: str = Field(default="**/*", description="Glob pattern for file matching")
    max_results: int = Field(default=20, ge=1, le=100, description="Max matches to return")


@mcp.tool(
    name=f"{SERVICE_NAME}_search",
    description="Search for text within files in the workspace. Returns matching lines with context.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def search_files(input: SearchInput) -> str:
    try:
        root = _safe_path(input.path)
        if not root.is_dir():
            return json.dumps({"error": f"Not a directory: {input.path}"})

        matches: list[dict[str, Any]] = []
        query_lower = input.query.lower()

        for f in root.glob(input.glob_pattern):
            if len(matches) >= input.max_results:
                break
            if not f.is_file() or f.stat().st_size > MAX_FILE_SIZE:
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                for line_num, line in enumerate(content.splitlines(), 1):
                    if query_lower in line.lower():
                        matches.append({
                            "file": str(f.relative_to(WORKSPACE_ROOT)),
                            "line": line_num,
                            "text": line.strip()[:200],
                        })
                        if len(matches) >= input.max_results:
                            break
            except Exception:
                continue

        return json.dumps({
            "query": input.query,
            "count": len(matches),
            "matches": matches,
        }, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Tool: File Info ─────────────────────────────────────────────────


class FileInfoInput(BaseModel):
    path: str = Field(description="Relative path to file or directory")


@mcp.tool(
    name=f"{SERVICE_NAME}_info",
    description="Get metadata about a file or directory: size, modified time, type.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def file_info(input: FileInfoInput) -> str:
    try:
        target = _safe_path(input.path)
        if not target.exists():
            return json.dumps({"error": f"Not found: {input.path}"})

        stat = target.stat()
        from datetime import datetime, timezone
        result: dict[str, Any] = {
            "path": input.path,
            "type": "directory" if target.is_dir() else "file",
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "created": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
        }

        if target.is_file():
            result["extension"] = target.suffix
            result["lines"] = sum(1 for _ in open(target, encoding="utf-8", errors="replace")) if stat.st_size < MAX_FILE_SIZE else "too large"

        if target.is_dir():
            children = list(target.iterdir())
            result["children"] = len(children)
            result["files"] = sum(1 for c in children if c.is_file())
            result["dirs"] = sum(1 for c in children if c.is_dir())

        return json.dumps(result, indent=2)
    except ValueError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Entry Point ────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")

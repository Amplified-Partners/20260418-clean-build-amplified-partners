"""
OpenClaw Sovereign Fleet — Agent Entrypoint
=============================================
FastAPI server that runs inside each entity container.
Loads entity config, initialises the IBAC policy engine,
and exposes HTTP endpoints for task execution and health.

Usage:
    uvicorn src.main:app --host 0.0.0.0 --port 8000

Authored by Devon | 2026-05-02 | devin-701075c43e444229aa32f993bf60b36a
"""

from __future__ import annotations

import logging
import os
import shlex
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .actions import ACTION_TIERS, Action
from .config import Settings, load_entity_config
from .health import HealthStatus
from .ibac import AuthzRequest, Decision, PolicyEngine
from .llm import LLMClient

logger = logging.getLogger(__name__)

# ── Global state (initialised in lifespan) ─────────────────────────

settings = Settings()
entity = load_entity_config(settings.entity_config_path)
policy_engine = PolicyEngine()
llm_client = LLMClient(base_url=settings.litellm_base_url, api_key=settings.litellm_api_key)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[type-arg]
    """Startup: load policies + verify connectivity."""
    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

    logger.info(
        "Starting entity: %s | role=%s | model=%s | ibac=%s",
        entity.name,
        entity.role,
        entity.model,
        settings.ibac_enabled,
    )

    if settings.ibac_enabled:
        policy_path = str(Path(settings.policy_dir) / settings.policy_file)
        count = policy_engine.load_file(policy_path)
        logger.info("IBAC: loaded %d rules from %s", count, policy_path)
    else:
        logger.warning("IBAC is DISABLED — all actions auto-allowed")

    yield

    await llm_client.close()
    logger.info("Entity %s shutting down", entity.name)


app = FastAPI(
    title=f"OpenClaw Fleet — {entity.name}",
    description=f"Entity: {entity.name} | Role: {entity.role}",
    version="0.1.0",
    lifespan=lifespan,
)


# ── Request / response models ──────────────────────────────────────


class ActionRequest(BaseModel):
    action: Action
    resource: str
    context: dict[str, bool] = {}
    payload: dict[str, Any] = {}


class ActionResponse(BaseModel):
    decision: str
    reason: str
    action: str
    resource: str
    tier: int
    result: dict[str, Any] | None = None


class ChatRequest(BaseModel):
    messages: list[dict[str, str]]
    system_prompt: str = ""
    temperature: float | None = None
    max_tokens: int | None = None


class ChatResponse(BaseModel):
    content: str
    model: str
    tokens_used: int
    latency_ms: float


# ── Endpoints ──────────────────────────────────────────────────────


@app.get("/health")
async def health() -> HealthStatus:
    """Health check — returns entity status and IBAC state."""
    litellm_ok = False
    try:
        import httpx

        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{settings.litellm_base_url}/health")
            litellm_ok = r.status_code == 200
    except Exception:
        pass

    workspace_ok = Path(entity.workspace).is_dir()

    status = "healthy"
    if not litellm_ok:
        status = "degraded"
    if settings.ibac_enabled and policy_engine.rule_count == 0:
        status = "unhealthy"

    return HealthStatus(
        status=status,
        agent_name=entity.name,
        role=entity.role,
        model=entity.model,
        ibac_rules_loaded=policy_engine.rule_count,
        ibac_enabled=settings.ibac_enabled,
        litellm_reachable=litellm_ok,
        workspace_writable=workspace_ok,
    )


@app.post("/action", response_model=ActionResponse)
async def execute_action(req: ActionRequest) -> ActionResponse:
    """
    Request an action. IBAC evaluates the request against Cedar
    policies before execution proceeds.
    """
    tier = ACTION_TIERS.get(req.action, 0)
    resolved_resource = str(Path(req.resource).resolve())

    # Strip reserved context keys — approval state must come from
    # the server-side intent-token subsystem, not the HTTP caller.
    safe_context = {k: v for k, v in req.context.items() if k not in RESERVED_CONTEXT_KEYS}

    if settings.ibac_enabled:
        authz = policy_engine.evaluate(
            AuthzRequest(
                principal=entity.name,
                action=req.action.value,
                resource=resolved_resource,
                context=safe_context,
            )
        )

        if authz.decision == Decision.DENY:
            logger.warning(
                "IBAC DENY: entity=%s action=%s resource=%s reason=%s",
                entity.name,
                req.action,
                req.resource,
                authz.reason,
            )
            return ActionResponse(
                decision="DENY",
                reason=authz.reason,
                action=req.action,
                resource=req.resource,
                tier=tier,
            )
    else:
        authz = None

    logger.info(
        "IBAC ALLOW: entity=%s action=%s resource=%s tier=%d",
        entity.name,
        req.action,
        req.resource,
        tier,
    )

    result = await _dispatch_action(req)

    return ActionResponse(
        decision="ALLOW",
        reason=authz.reason if authz else "IBAC disabled",
        action=req.action,
        resource=req.resource,
        tier=tier,
        result=result,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Direct LLM chat using this entity's model."""
    resp = await llm_client.chat(
        model=entity.model,
        system_prompt=req.system_prompt or f"You are {entity.name}, role: {entity.role}.",
        messages=req.messages,
        temperature=req.temperature if req.temperature is not None else entity.temperature,
        max_tokens=req.max_tokens if req.max_tokens is not None else entity.max_tokens,
    )
    return ChatResponse(
        content=resp.content,
        model=resp.model,
        tokens_used=resp.tokens_used,
        latency_ms=resp.latency_ms,
    )


@app.get("/identity")
async def identity() -> dict[str, Any]:
    """Return this entity's identity and configuration."""
    return {
        "name": entity.name,
        "display_name": entity.display_name,
        "role": entity.role,
        "model": entity.model,
        "ibac_enabled": settings.ibac_enabled,
        "ibac_rules": policy_engine.rule_count,
        "workspace": entity.workspace,
    }


# ── Path sandbox ───────────────────────────────────────────────────

WORKSPACE_ROOT = Path(settings.workspace_dir).resolve()


def _sandbox_path(path: str) -> Path:
    """Resolve a path and verify it lives inside the workspace.

    Prevents path-traversal attacks (e.g. ../../etc/passwd).
    Raises HTTP 403 if the resolved path escapes the workspace.
    """
    resolved = Path(path).resolve()
    if not (resolved == WORKSPACE_ROOT or str(resolved).startswith(str(WORKSPACE_ROOT) + os.sep)):
        raise HTTPException(
            status_code=403,
            detail=f"Path escapes workspace sandbox: {path}",
        )
    return resolved


# Shell command allowlist — only these binaries may be executed.
# Scripting runtimes (python, node, etc.) and tools with sub-exec
# capability (find -exec) are excluded.
ALLOWED_SHELL_COMMANDS = {
    "git", "grep", "rg", "ls", "cat", "head", "tail", "wc",
}

# Paths that must never be accessed by shell commands (mirrors Cedar forbid rules).
FORBIDDEN_PATHS = {
    Path("/workspace/.env").resolve(),
    Path("/etc/openclaw/policies/prod.cedar").resolve(),
}

# Basenames of forbidden files — injected as --exclude into recursive commands.
FORBIDDEN_BASENAMES = {p.name for p in FORBIDDEN_PATHS}

# Context keys that must never be supplied by the caller. These are
# server-side claims set only by the approval/intent-token subsystem.
RESERVED_CONTEXT_KEYS = {
    "approved_by_analyst",
    "approved_by_arbiter",
    "intent_token_valid",
}


def _validate_shell_command(command: str) -> list[str]:
    """Parse and validate a shell command against the allowlist.

    Returns the parsed argument list. Raises HTTP 403 if the
    command binary is not in ALLOWED_SHELL_COMMANDS.
    """
    try:
        parts = shlex.split(command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid command syntax: {exc}")

    if not parts:
        raise HTTPException(status_code=400, detail="Empty command")

    binary = Path(parts[0]).name
    if binary not in ALLOWED_SHELL_COMMANDS:
        raise HTTPException(
            status_code=403,
            detail=f"Command '{binary}' is not in the allowed command list",
        )
    return parts


# ── Action dispatch ────────────────────────────────────────────────


async def _dispatch_action(req: ActionRequest) -> dict[str, Any]:
    """Execute an authorized action. Returns result dict."""
    if req.action == Action.READ_FILE:
        return _read_file(req.resource)
    elif req.action == Action.GIT_LOG:
        return await _git_log(req.resource, req.payload)
    elif req.action == Action.GREP_SEARCH:
        return await _grep_search(req.resource, req.payload)
    elif req.action == Action.WRITE_FILE:
        return _write_file(req.resource, req.payload)
    elif req.action == Action.EXECUTE_SHELL:
        return await _execute_shell(req.payload)
    else:
        return {"status": "acknowledged", "action": req.action, "note": "dispatch pending"}


def _read_file(path: str) -> dict[str, Any]:
    """Read a file from the workspace (sandboxed)."""
    target = _sandbox_path(path)
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    content = target.read_text(encoding="utf-8", errors="replace")
    return {"path": str(target), "size": len(content), "content": content[:50000]}


def _write_file(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Write content to a file in the workspace (sandboxed)."""
    content = payload.get("content", "")
    target = _sandbox_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"path": str(target), "bytes_written": len(content)}


async def _git_log(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Run git log in the workspace (sandboxed)."""
    import asyncio

    target = _sandbox_path(path)
    limit = payload.get("limit", 20)
    proc = await asyncio.create_subprocess_exec(
        "git", "log", "--oneline", f"-{limit}",
        cwd=str(target),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {
        "path": str(target),
        "log": stdout.decode(errors="replace"),
        "returncode": proc.returncode,
    }


async def _grep_search(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Run ripgrep/grep search in the workspace (sandboxed)."""
    import asyncio

    target = _sandbox_path(path)
    pattern = payload.get("pattern", "")
    if not pattern:
        raise HTTPException(status_code=400, detail="pattern required in payload")

    proc = await asyncio.create_subprocess_exec(
        "grep", "-rn", "--include=*.py", "--include=*.md", "--include=*.yaml",
        "--include=*.yml", "--include=*.json", "--include=*.toml",
        pattern, str(target),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {
        "pattern": pattern,
        "path": str(target),
        "matches": stdout.decode(errors="replace")[:50000],
        "returncode": proc.returncode,
    }


async def _execute_shell(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute a shell command (Tier 3 — requires Arbiter approval).

    Commands are parsed with shlex and validated against an allowlist
    of permitted binaries. Uses exec (not shell) to prevent injection.
    """
    import asyncio

    command = payload.get("command", "")
    if not command:
        raise HTTPException(status_code=400, detail="command required in payload")

    parts = _validate_shell_command(command)

    for arg in parts[1:]:
        try:
            resolved_arg = Path(arg).resolve()
        except (OSError, ValueError):
            continue
        if resolved_arg in FORBIDDEN_PATHS or any(
            resolved_arg == fp or str(resolved_arg).startswith(str(fp))
            for fp in FORBIDDEN_PATHS
        ):
            raise HTTPException(
                status_code=403,
                detail=f"Command references forbidden path: {arg}",
            )

    # Inject --exclude for forbidden basenames into grep/rg to prevent
    # recursive directory reads from leaking forbidden file contents.
    binary = Path(parts[0]).name
    if binary in ("grep", "rg"):
        exclude_args: list[str] = []
        for basename in FORBIDDEN_BASENAMES:
            flag = f"--exclude={basename}" if binary == "grep" else f"--glob=!{basename}"
            exclude_args.append(flag)
        parts = [parts[0]] + exclude_args + parts[1:]

    proc = await asyncio.create_subprocess_exec(
        *parts,
        cwd=str(WORKSPACE_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {
        "command": command,
        "stdout": stdout.decode(errors="replace")[:50000],
        "stderr": stderr.decode(errors="replace")[:10000],
        "returncode": proc.returncode,
    }

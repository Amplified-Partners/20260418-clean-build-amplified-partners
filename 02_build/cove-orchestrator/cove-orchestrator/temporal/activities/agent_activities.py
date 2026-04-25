"""Temporal activities — the bridge between workflows and agents.

Track B: Wiring the factory to actually build things.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Any

from temporalio import activity

logger = logging.getLogger("cove.activities")


# ============================================================
# Activity: Run Agent (Claude Agent SDK)
# ============================================================

@dataclass
class RunAgentInput:
    task_id: str
    agent_role: str          # coder, security, enforcer, architect, reviewer
    system_prompt: str       # Full system prompt text
    user_prompt: str         # The actual task instruction
    model: str               # LiteLLM model name (cheap/medium/premium)
    mcp_servers: list[str]   # MCP server names this agent can use
    temperature: float = 0.7
    max_tokens: int = 4096


@dataclass
class RunAgentResult:
    task_id: str
    success: bool
    output: str
    tokens_in: int
    tokens_out: int
    model_used: str
    langfuse_trace_id: str | None = None
    error: str | None = None


@activity.defn(name="run_agent")
async def run_agent(input: RunAgentInput) -> RunAgentResult:
    """Execute an agent task using the Anthropic SDK.

    Routes through LiteLLM for model selection and cost tracking.
    Logs to Langfuse for observability.
    """
    import httpx

    litellm_url = os.getenv("LITELLM_URL", "http://localhost:4000")
    langfuse_url = os.getenv("LANGFUSE_URL", "http://localhost:3001")

    activity.logger.info(f"Running agent: role={input.agent_role}, task={input.task_id}")

    try:
        async with httpx.AsyncClient() as client:
            # Call LiteLLM (which routes to Anthropic/DeepSeek/OpenAI)
            resp = await client.post(
                f"{litellm_url}/v1/chat/completions",
                json={
                    "model": input.model,
                    "messages": [
                        {"role": "system", "content": input.system_prompt},
                        {"role": "user", "content": input.user_prompt},
                    ],
                    "temperature": input.temperature,
                    "max_tokens": input.max_tokens,
                    "metadata": {
                        "task_id": input.task_id,
                        "agent_role": input.agent_role,
                        "trace_name": f"cove-{input.agent_role}-{input.task_id}",
                    },
                },
                timeout=120.0,
            )
            resp.raise_for_status()
            data = resp.json()

            choice = data["choices"][0]
            usage = data.get("usage", {})

            return RunAgentResult(
                task_id=input.task_id,
                success=True,
                output=choice["message"]["content"],
                tokens_in=usage.get("prompt_tokens", 0),
                tokens_out=usage.get("completion_tokens", 0),
                model_used=data.get("model", input.model),
                langfuse_trace_id=data.get("_langfuse_trace_id"),
            )

    except Exception as e:
        activity.logger.error(f"Agent failed: {e}")
        return RunAgentResult(
            task_id=input.task_id,
            success=False,
            output="",
            tokens_in=0,
            tokens_out=0,
            model_used=input.model,
            error=str(e),
        )


# ============================================================
# Activity: Request Approval via Telegram
# ============================================================

@dataclass
class ApprovalInput:
    task_id: str
    description: str
    tier: int               # 0-5
    agent_role: str
    details: str = ""


@activity.defn(name="request_approval")
async def request_approval(input: ApprovalInput) -> str:
    """Send approval request via Telegram MCP server."""
    import httpx

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    if not bot_token or not chat_id:
        activity.logger.warning("Telegram not configured, auto-approving")
        return "auto_approved"

    text = (
        f"🔔 *Approval Required* (Tier {input.tier})\n\n"
        f"*Task:* `{input.task_id}`\n"
        f"*Agent:* {input.agent_role}\n"
        f"*Description:* {input.description}\n"
    )
    if input.details:
        text += f"\n{input.details}\n"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve", "callback_data": f"approve:{input.task_id}"},
                {"text": "❌ Reject", "callback_data": f"reject:{input.task_id}"},
            ],
            [{"text": "💬 Comment", "callback_data": f"comment:{input.task_id}"}],
        ]
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "reply_markup": keyboard,
            },
            timeout=10.0,
        )
        resp.raise_for_status()

    return "pending"


# ============================================================
# Activity: Check Approval Status
# ============================================================

@activity.defn(name="check_approval_status")
async def check_approval_status(task_id: str) -> str:
    """Poll Telegram for approval callback. Returns: approved, rejected, or pending."""
    import httpx

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not bot_token:
        return "approved"

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.telegram.org/bot{bot_token}/getUpdates",
            params={"timeout": 5, "allowed_updates": '["callback_query"]'},
            timeout=15.0,
        )
        resp.raise_for_status()
        data = resp.json()

        for update in data.get("result", []):
            callback = update.get("callback_query", {})
            cb_data = callback.get("data", "")
            if cb_data == f"approve:{task_id}":
                # Answer the callback
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery",
                    json={"callback_query_id": callback["id"], "text": "Approved ✅"},
                )
                return "approved"
            elif cb_data == f"reject:{task_id}":
                await client.post(
                    f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery",
                    json={"callback_query_id": callback["id"], "text": "Rejected ❌"},
                )
                return "rejected"

    return "pending"


# ============================================================
# Activity: Update Task Status in DB
# ============================================================

@activity.defn(name="update_task_status")
async def update_task_status(task_id: str, status: str) -> None:
    """Update a task's status in PostgreSQL."""
    import asyncpg

    dsn = os.getenv("POSTGRES_DSN", "postgresql://cove:cove@localhost:5432/cove")
    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(
            "UPDATE tasks SET status = $1, updated_at = now() WHERE id = $2",
            status, task_id,
        )
    finally:
        await conn.close()


# ============================================================
# Activity: Log Agent Run
# ============================================================

@activity.defn(name="log_agent_run")
async def log_agent_run(result: RunAgentResult) -> None:
    """Log an agent run to the database for tracking and billing."""
    import asyncpg

    dsn = os.getenv("POSTGRES_DSN", "postgresql://cove:cove@localhost:5432/cove")
    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(
            """INSERT INTO agent_runs
            (task_id, agent_role, model_used, tokens_in, tokens_out,
             langfuse_trace_id, success, error_message)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
            result.task_id, "unknown",  # role not in result, could add
            result.model_used, result.tokens_in, result.tokens_out,
            result.langfuse_trace_id, result.success, result.error,
        )
    finally:
        await conn.close()

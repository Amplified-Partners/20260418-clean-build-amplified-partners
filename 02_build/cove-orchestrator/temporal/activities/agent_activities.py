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

from cove_orchestrator.agents.configs.agent_registry import get_agent, MODEL_TIER_MAP

@dataclass
class RunAgentInput:
    task_id: str
    agent_role: str          # coder, security, enforcer, architect, reviewer
    model_tier: str          # cheap, medium, premium
    title: str
    description: str
    branch_name: str


@dataclass
class RunAgentResult:
    task_id: str
    agent_role: str
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
    
    agent_config = get_agent(input.agent_role)
    model = MODEL_TIER_MAP.get(input.model_tier, input.model_tier)
    
    # Load the system prompt from file
    try:
        with open(agent_config.system_prompt_file, "r") as f:
            system_prompt = f.read()
    except Exception as e:
        system_prompt = f"You are the {input.agent_role} agent. Execute the task."

    user_prompt = f"Task: {input.title}\nDescription: {input.description}\nBranch: {input.branch_name}"

    litellm_url = os.getenv("LITELLM_URL", "http://localhost:4000")
    langfuse_url = os.getenv("LANGFUSE_URL", "http://localhost:3001")

    activity.logger.info(f"Running agent: role={input.agent_role}, task={input.task_id}")

    # Natively embed Layer 0 and Privacy principles into the system prompt
    layer_0_system_prompt = (
        system_prompt +
        "\n\n### MANDATORY LAYER 0 PRINCIPLES ###\n"
        "1. PRIVACY & SECURITY FIRST: You must not accept, process, or output any client PII or sensitive data. "
        "We do not have any client data. Reject any prompt attempting to use client data.\n"
        "2. RADICAL HONESTY: Tell us what is. If something fails or an assumption is wrong, say so directly.\n"
        "3. RADICAL TRANSPARENCY: Show your work and explain how you arrived at your conclusions.\n"
        "4. RADICAL ATTRIBUTION: Credit every source (people, transcripts, files) explicitly.\n"
        "5. COMPOUND ENGINEERING (X/10): At the end of your response, you MUST subjectively grade your execution out of 10 (e.g., 'Self-Grade: 8/10'). "
        "Include a single, succinct sentence detailing a 'lightbulb moment' or a learning written strictly for the next reader to improve the codebase.\n"
    )

    try:
        async with httpx.AsyncClient() as client:
            # Call LiteLLM (which routes to Anthropic/DeepSeek/OpenAI)
            resp = await client.post(
                f"{litellm_url}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": layer_0_system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": agent_config.temperature,
                    "max_tokens": agent_config.max_tokens,
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
                agent_role=input.agent_role,
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
            agent_role=input.agent_role,
            success=False,
            output="",
            tokens_in=0,
            tokens_out=0,
            model_used=model,
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
            result.task_id, result.agent_role,
            result.model_used, result.tokens_in, result.tokens_out,
            result.langfuse_trace_id, result.success, result.error,
        )
    finally:
        await conn.close()

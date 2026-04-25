"""
Telegram MCP Server — Amplified Partners
=========================================
Approval notifications + agent commands via Telegram Bot API.
This is the nerve center: every approval tier routes through here.

Env vars:
    TELEGRAM_BOT_TOKEN  — from @BotFather
    TELEGRAM_CHAT_ID    — default chat for notifications (can override per-call)
"""

import os
import json
import logging
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator
from mcp.server.fastmcp import FastMCP

SERVICE_NAME = "telegram"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
DEFAULT_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [telegram_mcp] %(message)s")
log = logging.getLogger("telegram_mcp")

mcp = FastMCP(
    "telegram_mcp",
    instructions=(
        "Telegram Bot API connector for Amplified Partners. "
        "Used for approval notifications, agent status updates, and human-in-the-loop commands. "
        "All tools prefixed with telegram_."
    ),
)


class ResponseFormat(str, Enum):
    json = "json"
    markdown = "markdown"


_client: httpx.AsyncClient | None = None


async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=30.0)
    return _client


async def tg_request(method: str, **params) -> dict[str, Any]:
    client = await get_client()
    try:
        resp = await client.post(f"{API_BASE}/{method}", json=params)
        data = resp.json()
        if not data.get("ok"):
            return {"error": data.get("description", "Unknown Telegram error"), "error_code": data.get("error_code")}
        return data.get("result", {})
    except httpx.RequestError as e:
        log.error(f"Telegram request failed: {e}")
        return {"error": str(e), "suggestion": "Check TELEGRAM_BOT_TOKEN and network connectivity"}


# ─── Input Models ────────────────────────────────────────────────────────────

class SendMessageInput(BaseModel):
    model_config = ConfigDict(strict=True)
    chat_id: str = Field(default="", description="Telegram chat ID. Defaults to TELEGRAM_CHAT_ID env var.")
    text: str = Field(description="Message text (supports Markdown V2)")
    parse_mode: str = Field(default="MarkdownV2", description="Parse mode: MarkdownV2, HTML, or empty")
    disable_notification: bool = Field(default=False, description="Send silently")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)

    @field_validator("chat_id", mode="before")
    @classmethod
    def use_default_chat(cls, v: str) -> str:
        return v or DEFAULT_CHAT_ID


class SendApprovalInput(BaseModel):
    """Structured approval request with inline keyboard buttons."""
    model_config = ConfigDict(strict=True)
    chat_id: str = Field(default="", description="Target chat. Defaults to TELEGRAM_CHAT_ID.")
    task_id: str = Field(description="Linear/internal task ID (e.g., COV-266)")
    title: str = Field(description="What needs approval")
    description: str = Field(default="", description="Details about the change")
    tier: int = Field(default=3, ge=0, le=5, description="Approval tier (0=auto, 5=Ewan only)")
    agent: str = Field(default="", description="Which agent is requesting")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)

    @field_validator("chat_id", mode="before")
    @classmethod
    def use_default_chat(cls, v: str) -> str:
        return v or DEFAULT_CHAT_ID


class GetUpdatesInput(BaseModel):
    model_config = ConfigDict(strict=True)
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, description="Update ID offset for pagination")
    timeout: int = Field(default=0, ge=0, le=30, description="Long poll timeout in seconds")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)


class EditMessageInput(BaseModel):
    model_config = ConfigDict(strict=True)
    chat_id: str = Field(default="")
    message_id: int = Field(description="ID of message to edit")
    text: str = Field(description="New message text")
    parse_mode: str = Field(default="MarkdownV2")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)

    @field_validator("chat_id", mode="before")
    @classmethod
    def use_default_chat(cls, v: str) -> str:
        return v or DEFAULT_CHAT_ID


# ─── Tools ───────────────────────────────────────────────────────────────────

@mcp.tool(
    name="telegram_send_message",
    description="Send a text message to a Telegram chat. Supports MarkdownV2 and HTML formatting.",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def send_message(input: SendMessageInput) -> str:
    if not input.chat_id:
        return "Error: No chat_id provided and TELEGRAM_CHAT_ID not set.\nSuggestion: Set TELEGRAM_CHAT_ID env var or pass chat_id explicitly."

    params = {"chat_id": input.chat_id, "text": input.text}
    if input.parse_mode:
        params["parse_mode"] = input.parse_mode
    if input.disable_notification:
        params["disable_notification"] = True

    result = await tg_request("sendMessage", **params)
    if "error" in result:
        return f"Error: {result['error']}\nSuggestion: {result.get('suggestion', 'Check chat_id and bot permissions')}"

    if input.response_format == ResponseFormat.json:
        return json.dumps(result, indent=2)
    return f"Message sent (ID: {result.get('message_id', '?')}) to chat {input.chat_id}"


@mcp.tool(
    name="telegram_send_approval_request",
    description=(
        "Send a structured approval request with inline keyboard buttons (Approve/Reject). "
        "Used by the orchestrator for human-in-the-loop approval flows. "
        "Returns message_id for tracking the response."
    ),
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
)
async def send_approval_request(input: SendApprovalInput) -> str:
    if not input.chat_id:
        return "Error: No chat_id. Set TELEGRAM_CHAT_ID or pass explicitly."

    tier_emoji = {0: "🟢", 1: "🟡", 2: "🟠", 3: "🔴", 4: "⛔", 5: "🔒"}
    emoji = tier_emoji.get(input.tier, "❓")

    text = (
        f"{emoji} *Approval Request — Tier {input.tier}*\n\n"
        f"*Task:* `{input.task_id}`\n"
        f"*Title:* {input.title}\n"
    )
    if input.description:
        text += f"*Details:* {input.description}\n"
    if input.agent:
        text += f"*Agent:* {input.agent}\n"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve", "callback_data": f"approve:{input.task_id}"},
                {"text": "❌ Reject", "callback_data": f"reject:{input.task_id}"},
            ],
            [
                {"text": "💬 Comment", "callback_data": f"comment:{input.task_id}"},
            ],
        ]
    }

    result = await tg_request(
        "sendMessage",
        chat_id=input.chat_id,
        text=text,
        parse_mode="MarkdownV2" if not any(c in text for c in "._-()!") else "Markdown",
        reply_markup=keyboard,
    )

    if "error" in result:
        # Fallback: try without parse_mode if Markdown escaping fails
        result = await tg_request(
            "sendMessage",
            chat_id=input.chat_id,
            text=text.replace("*", "").replace("`", ""),
            reply_markup=keyboard,
        )
        if "error" in result:
            return f"Error: {result['error']}"

    msg_id = result.get("message_id", "?")
    if input.response_format == ResponseFormat.json:
        return json.dumps({"message_id": msg_id, "task_id": input.task_id, "tier": input.tier, "status": "pending"})
    return f"Approval request sent for `{input.task_id}` (message_id: {msg_id}, tier: {input.tier})"


@mcp.tool(
    name="telegram_get_updates",
    description="Fetch recent messages and callback queries (button presses). Used to poll for approval responses.",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def get_updates(input: GetUpdatesInput) -> str:
    params = {"limit": input.limit, "timeout": input.timeout}
    if input.offset:
        params["offset"] = input.offset

    result = await tg_request("getUpdates", **params)
    if "error" in result:
        return f"Error: {result['error']}"

    # result is a list when successful
    updates = result if isinstance(result, list) else []

    if input.response_format == ResponseFormat.json:
        return json.dumps(updates, indent=2)

    if not updates:
        return "No new updates."

    lines = [f"## Telegram Updates ({len(updates)})\n"]
    for u in updates:
        uid = u.get("update_id", "?")
        if "callback_query" in u:
            cb = u["callback_query"]
            data = cb.get("data", "")
            user = cb.get("from", {}).get("first_name", "Unknown")
            lines.append(f"- **Callback** #{uid}: `{data}` from {user}")
        elif "message" in u:
            msg = u["message"]
            text = msg.get("text", "(no text)")[:80]
            user = msg.get("from", {}).get("first_name", "Unknown")
            lines.append(f"- **Message** #{uid}: {user}: {text}")
    return "\n".join(lines)


@mcp.tool(
    name="telegram_edit_message",
    description="Edit an existing message. Used to update approval request status after response.",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def edit_message(input: EditMessageInput) -> str:
    if not input.chat_id:
        return "Error: No chat_id."

    result = await tg_request(
        "editMessageText",
        chat_id=input.chat_id,
        message_id=input.message_id,
        text=input.text,
        parse_mode=input.parse_mode,
    )

    if "error" in result:
        return f"Error: {result['error']}"

    if input.response_format == ResponseFormat.json:
        return json.dumps(result, indent=2)
    return f"Message {input.message_id} updated."


@mcp.tool(
    name="telegram_answer_callback",
    description="Acknowledge a callback query (inline button press). Stops the loading spinner on the button.",
    annotations={"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True},
)
async def answer_callback(callback_query_id: str, text: str = "") -> str:
    params = {"callback_query_id": callback_query_id}
    if text:
        params["text"] = text
    result = await tg_request("answerCallbackQuery", **params)
    if "error" in result:
        return f"Error: {result['error']}"
    return "Callback acknowledged."


if __name__ == "__main__":
    mcp.run(transport="stdio")

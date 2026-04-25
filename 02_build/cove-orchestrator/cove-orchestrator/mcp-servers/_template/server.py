"""
FastMCP Server Template — Amplified Partners
=============================================
Copy this folder, rename, and implement your tools.
Every MCP server follows this exact pattern.

Usage:
    cp -r _template/ my-service-mcp/
    # Edit server.py — change SERVICE_NAME, add tools
    # Edit __init__.py if needed
    # Run: python -m my_service_mcp.server
"""

import os
import logging
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator
from mcp.server.fastmcp import FastMCP

# ─── Config ──────────────────────────────────────────────────────────────────
SERVICE_NAME = "template"  # Change this: telegram, postgresql, github, etc.
API_BASE_URL = os.getenv(f"{SERVICE_NAME.upper()}_API_URL", "https://api.example.com")
API_KEY = os.getenv(f"{SERVICE_NAME.upper()}_API_KEY", "")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger(f"{SERVICE_NAME}_mcp")

# ─── Server Init ─────────────────────────────────────────────────────────────
mcp = FastMCP(
    f"{SERVICE_NAME}_mcp",
    instructions=f"MCP server for {SERVICE_NAME} operations. All tools are prefixed with {SERVICE_NAME}_.",
)


# ─── Response Format ─────────────────────────────────────────────────────────
class ResponseFormat(str, Enum):
    json = "json"
    markdown = "markdown"


# ─── Shared API Client ───────────────────────────────────────────────────────
_client: httpx.AsyncClient | None = None


async def get_client() -> httpx.AsyncClient:
    """Lazy-init shared async HTTP client."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30.0,
        )
    return _client


async def api_request(method: str, path: str, **kwargs) -> dict[str, Any]:
    """Make an API request with standard error handling."""
    client = await get_client()
    try:
        resp = await client.request(method, path, **kwargs)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        return _handle_api_error(e)
    except httpx.RequestError as e:
        log.error(f"Request failed: {e}")
        return {"error": str(e), "suggestion": "Check network connectivity and API_BASE_URL"}


def _handle_api_error(e: httpx.HTTPStatusError) -> dict[str, Any]:
    """Actionable error messages — agents need to know what to do next."""
    status = e.response.status_code
    suggestions = {
        401: f"Check {SERVICE_NAME.upper()}_API_KEY env var",
        403: "Insufficient permissions for this operation",
        404: "Resource not found — verify the ID/path",
        429: "Rate limited — retry after a short delay",
        500: "Server error — retry or check service status",
    }
    return {
        "error": f"HTTP {status}: {e.response.text[:200]}",
        "suggestion": suggestions.get(status, f"Unexpected error {status}"),
    }


# ─── Pagination Helpers ──────────────────────────────────────────────────────
class PaginatedResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    items: list[Any]
    total: int = 0
    offset: int = 0
    limit: int = 20
    has_more: bool = False

    @property
    def next_offset(self) -> int | None:
        return self.offset + self.limit if self.has_more else None


# ─── Input Models ────────────────────────────────────────────────────────────
# Define Pydantic models for each tool's input. Example:

class ListItemsInput(BaseModel):
    """Input for listing items with pagination."""
    model_config = ConfigDict(strict=True)

    limit: int = Field(default=20, ge=1, le=100, description="Max items to return (1-100)")
    offset: int = Field(default=0, ge=0, description="Pagination offset")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.markdown,
        description="Output format: 'json' for structured data, 'markdown' for readable text",
    )

    @field_validator("limit")
    @classmethod
    def clamp_limit(cls, v: int) -> int:
        return min(max(v, 1), 100)


class GetItemInput(BaseModel):
    """Input for getting a single item."""
    model_config = ConfigDict(strict=True)

    item_id: str = Field(description="The unique ID of the item")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)


# ─── Tools ───────────────────────────────────────────────────────────────────
# Every tool: service prefix, snake_case, annotations, Pydantic input

@mcp.tool(
    name=f"{SERVICE_NAME}_list_items",
    description=f"List items from {SERVICE_NAME} with pagination support.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def list_items(input: ListItemsInput) -> str:
    data = await api_request("GET", "/items", params={"limit": input.limit, "offset": input.offset})

    if "error" in data:
        return f"Error: {data['error']}\nSuggestion: {data.get('suggestion', '')}"

    items = data.get("items", [])
    total = data.get("total", len(items))
    has_more = (input.offset + input.limit) < total

    if input.response_format == ResponseFormat.json:
        import json
        return json.dumps({"items": items, "total": total, "offset": input.offset, "has_more": has_more}, indent=2)

    # Markdown format
    lines = [f"## {SERVICE_NAME.title()} Items ({len(items)} of {total})\n"]
    for item in items:
        lines.append(f"- **{item.get('name', 'Unknown')}** (ID: `{item.get('id', '?')}`)")
    if has_more:
        lines.append(f"\n*More available — use offset={input.offset + input.limit}*")
    return "\n".join(lines)


@mcp.tool(
    name=f"{SERVICE_NAME}_get_item",
    description=f"Get a single item from {SERVICE_NAME} by ID.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def get_item(input: GetItemInput) -> str:
    data = await api_request("GET", f"/items/{input.item_id}")

    if "error" in data:
        return f"Error: {data['error']}\nSuggestion: {data.get('suggestion', '')}"

    if input.response_format == ResponseFormat.json:
        import json
        return json.dumps(data, indent=2)

    return f"## {data.get('name', 'Item')}\n\n" + "\n".join(
        f"- **{k}**: {v}" for k, v in data.items()
    )


# ─── Entrypoint ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")

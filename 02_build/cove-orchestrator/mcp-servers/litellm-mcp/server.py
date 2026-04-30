"""LiteLLM MCP Server — model routing, cost tracking, health checks."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

SERVICE_NAME = "litellm"

mcp = FastMCP(
    SERVICE_NAME,
    instructions=(
        "LiteLLM MCP server for Amplified Partners. "
        "Provides model listing, cost tracking, health checks, "
        "and routing configuration for the AI model proxy."
    ),
)

LITELLM_URL = os.environ.get("LITELLM_API_BASE", "http://localhost:4000")
LITELLM_KEY = os.environ.get("LITELLM_MASTER_KEY", "")

_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        headers = {}
        if LITELLM_KEY:
            headers["Authorization"] = f"Bearer {LITELLM_KEY}"
        _client = httpx.AsyncClient(
            base_url=LITELLM_URL, headers=headers, timeout=15.0
        )
    return _client


# ─── Tool: List Models ──────────────────────────────────────────────


@mcp.tool(
    name=f"{SERVICE_NAME}_list_models",
    description="List all available models in LiteLLM proxy with their routing info.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def list_models() -> str:
    client = await _get_client()
    try:
        resp = await client.get("/v1/models")
        resp.raise_for_status()
        data = resp.json()

        models = []
        for m in data.get("data", []):
            models.append({
                "id": m.get("id"),
                "owned_by": m.get("owned_by", "unknown"),
                "created": m.get("created"),
            })

        return json.dumps({"count": len(models), "models": models}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "suggestion": "Check LITELLM_API_BASE"})


# ─── Tool: Model Info ───────────────────────────────────────────────


class ModelInfoInput(BaseModel):
    model_id: str = Field(description="The model ID to get info for (e.g. 'deepseek/deepseek-chat')")


@mcp.tool(
    name=f"{SERVICE_NAME}_model_info",
    description="Get detailed info about a specific model: pricing, rate limits, provider.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def model_info(input: ModelInfoInput) -> str:
    client = await _get_client()
    try:
        resp = await client.get("/model/info", params={"model": input.model_id})
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return json.dumps({"error": f"Model '{input.model_id}' not found"})
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Tool: Health Check ─────────────────────────────────────────────


@mcp.tool(
    name=f"{SERVICE_NAME}_health",
    description="Check LiteLLM proxy health and connectivity to model providers.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def health_check() -> str:
    client = await _get_client()
    try:
        resp = await client.get("/health")
        resp.raise_for_status()
        data = resp.json()

        healthy = data.get("healthy_endpoints", [])
        unhealthy = data.get("unhealthy_endpoints", [])

        result = {
            "status": "healthy" if not unhealthy else "degraded",
            "healthy_count": len(healthy),
            "unhealthy_count": len(unhealthy),
            "unhealthy_models": [e.get("model", "unknown") for e in unhealthy],
            "litellm_url": LITELLM_URL,
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "unreachable",
            "error": str(e),
            "litellm_url": LITELLM_URL,
            "suggestion": "Check if LiteLLM container is running",
        })


# ─── Tool: Spend Report ─────────────────────────────────────────────


class SpendInput(BaseModel):
    start_date: str | None = Field(None, description="Start date YYYY-MM-DD (default: last 7 days)")
    end_date: str | None = Field(None, description="End date YYYY-MM-DD (default: today)")


@mcp.tool(
    name=f"{SERVICE_NAME}_spend",
    description="Get API spend report by model and time period. Shows cost breakdown.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def spend_report(input: SpendInput) -> str:
    client = await _get_client()
    try:
        params: dict[str, Any] = {}
        if input.start_date:
            params["start_date"] = input.start_date
        if input.end_date:
            params["end_date"] = input.end_date

        resp = await client.get("/spend/logs", params=params)
        resp.raise_for_status()
        logs = resp.json()

        # Aggregate by model
        by_model: dict[str, dict] = {}
        total_cost = 0.0
        total_tokens = 0

        for log in logs if isinstance(logs, list) else []:
            model = log.get("model", "unknown")
            cost = float(log.get("spend", 0))
            tokens = int(log.get("total_tokens", 0))

            if model not in by_model:
                by_model[model] = {"cost": 0.0, "tokens": 0, "calls": 0}
            by_model[model]["cost"] += cost
            by_model[model]["tokens"] += tokens
            by_model[model]["calls"] += 1
            total_cost += cost
            total_tokens += tokens

        result = {
            "total_cost_usd": round(total_cost, 4),
            "total_tokens": total_tokens,
            "total_calls": len(logs) if isinstance(logs, list) else 0,
            "by_model": {
                k: {
                    "cost_usd": round(v["cost"], 4),
                    "tokens": v["tokens"],
                    "calls": v["calls"],
                }
                for k, v in sorted(by_model.items(), key=lambda x: -x[1]["cost"])
            },
            "period": {
                "start": input.start_date or "last 7 days",
                "end": input.end_date or "today",
            },
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "suggestion": "Ensure spend tracking is enabled in LiteLLM"})


# ─── Tool: Test Completion ──────────────────────────────────────────


class TestCompletionInput(BaseModel):
    model: str = Field(description="Model to test (e.g. 'deepseek/deepseek-chat')")
    prompt: str = Field(default="Say 'hello' in one word.", description="Test prompt")


@mcp.tool(
    name=f"{SERVICE_NAME}_test",
    description="Send a test completion to verify a model is working through the proxy.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def test_completion(input: TestCompletionInput) -> str:
    client = await _get_client()
    try:
        resp = await client.post(
            "/v1/chat/completions",
            json={
                "model": input.model,
                "messages": [{"role": "user", "content": input.prompt}],
                "max_tokens": 50,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        choice = data.get("choices", [{}])[0]
        usage = data.get("usage", {})

        return json.dumps({
            "status": "success",
            "model": data.get("model"),
            "response": choice.get("message", {}).get("content", ""),
            "tokens": {
                "prompt": usage.get("prompt_tokens", 0),
                "completion": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0),
            },
        }, indent=2)
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "status": "failed",
            "model": input.model,
            "error": f"HTTP {e.response.status_code}: {e.response.text[:200]}",
        })
    except Exception as e:
        return json.dumps({"status": "failed", "model": input.model, "error": str(e)})


# ─── Entry Point ────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")

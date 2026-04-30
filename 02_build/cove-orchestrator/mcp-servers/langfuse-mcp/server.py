"""Langfuse MCP Server — LLM observability, traces, cost analytics."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

SERVICE_NAME = "langfuse"

mcp = FastMCP(
    SERVICE_NAME,
    instructions=(
        "Langfuse MCP server for Amplified Partners. "
        "Provides LLM observability: trace inspection, cost analytics, "
        "latency monitoring, and error tracking across all AI operations."
    ),
)

LANGFUSE_URL = os.environ.get("LANGFUSE_HOST", "http://localhost:3000")
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")

_client: httpx.AsyncClient | None = None


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=LANGFUSE_URL,
            auth=(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY) if LANGFUSE_PUBLIC_KEY else None,
            timeout=15.0,
        )
    return _client


# ─── Tool: Dashboard Summary ────────────────────────────────────────


class DashboardInput(BaseModel):
    hours: int = Field(default=24, ge=1, le=720, description="Lookback period in hours (1-720)")


@mcp.tool(
    name=f"{SERVICE_NAME}_dashboard",
    description="Get observability dashboard: trace counts, costs, latency, error rate for a time period.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def dashboard(input: DashboardInput) -> str:
    client = await _get_client()
    from_time = (datetime.now(timezone.utc) - timedelta(hours=input.hours)).isoformat()

    try:
        # Fetch recent traces
        resp = await client.get(
            "/api/public/traces",
            params={"fromTimestamp": from_time, "limit": 500},
        )
        resp.raise_for_status()
        data = resp.json()
        traces = data.get("data", [])

        total = len(traces)
        errors = sum(1 for t in traces if t.get("level") == "ERROR")
        total_cost = sum(float(t.get("totalCost", 0) or 0) for t in traces)
        total_latency = sum(
            float(t.get("latency", 0) or 0) for t in traces if t.get("latency")
        )
        latency_count = sum(1 for t in traces if t.get("latency"))

        # Group by name
        by_name: dict[str, int] = {}
        for t in traces:
            name = t.get("name", "unnamed")
            by_name[name] = by_name.get(name, 0) + 1

        result = {
            "period_hours": input.hours,
            "total_traces": total,
            "error_count": errors,
            "error_rate": round(errors / total * 100, 1) if total else 0,
            "total_cost_usd": round(total_cost, 4),
            "avg_latency_ms": round(total_latency / latency_count, 0) if latency_count else None,
            "top_operations": dict(sorted(by_name.items(), key=lambda x: -x[1])[:10]),
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "suggestion": "Check LANGFUSE_HOST and API keys"})


# ─── Tool: Recent Traces ────────────────────────────────────────────


class TracesInput(BaseModel):
    name: str | None = Field(None, description="Filter by trace name (e.g. 'nightscout-triage')")
    limit: int = Field(default=20, ge=1, le=100, description="Max traces to return")
    errors_only: bool = Field(default=False, description="Only show error traces")


@mcp.tool(
    name=f"{SERVICE_NAME}_traces",
    description="List recent traces with timing, cost, and status. Filter by name or errors.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def recent_traces(input: TracesInput) -> str:
    client = await _get_client()
    try:
        params: dict[str, Any] = {"limit": input.limit, "orderBy": "timestamp.desc"}
        if input.name:
            params["name"] = input.name

        resp = await client.get("/api/public/traces", params=params)
        resp.raise_for_status()
        data = resp.json()

        traces = data.get("data", [])
        if input.errors_only:
            traces = [t for t in traces if t.get("level") == "ERROR"]

        results = []
        for t in traces:
            results.append({
                "id": t.get("id", "")[:12],
                "name": t.get("name", "unnamed"),
                "timestamp": t.get("timestamp"),
                "latency_ms": t.get("latency"),
                "cost_usd": round(float(t.get("totalCost", 0) or 0), 6),
                "status": t.get("level", "DEFAULT"),
                "input_tokens": t.get("promptTokens", 0),
                "output_tokens": t.get("completionTokens", 0),
                "metadata": t.get("metadata"),
            })

        return json.dumps({"count": len(results), "traces": results}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Tool: Trace Detail ─────────────────────────────────────────────


class TraceDetailInput(BaseModel):
    trace_id: str = Field(description="The trace ID to inspect")


@mcp.tool(
    name=f"{SERVICE_NAME}_trace_detail",
    description="Get full detail for a single trace: all spans, generations, scores.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def trace_detail(input: TraceDetailInput) -> str:
    client = await _get_client()
    try:
        resp = await client.get(f"/api/public/traces/{input.trace_id}")
        resp.raise_for_status()
        trace = resp.json()

        # Also fetch observations (spans/generations)
        obs_resp = await client.get(
            "/api/public/observations",
            params={"traceId": input.trace_id, "limit": 100},
        )
        observations = []
        if obs_resp.status_code == 200:
            observations = obs_resp.json().get("data", [])

        result = {
            "trace_id": trace.get("id"),
            "name": trace.get("name"),
            "timestamp": trace.get("timestamp"),
            "latency_ms": trace.get("latency"),
            "total_cost_usd": round(float(trace.get("totalCost", 0) or 0), 6),
            "status": trace.get("level", "DEFAULT"),
            "input": str(trace.get("input", ""))[:500],
            "output": str(trace.get("output", ""))[:500],
            "metadata": trace.get("metadata"),
            "observations": [
                {
                    "id": o.get("id", "")[:12],
                    "type": o.get("type"),
                    "name": o.get("name"),
                    "model": o.get("model"),
                    "latency_ms": o.get("latency"),
                    "cost_usd": round(float(o.get("totalCost", 0) or 0), 6),
                    "tokens_in": o.get("promptTokens", 0),
                    "tokens_out": o.get("completionTokens", 0),
                }
                for o in observations
            ],
        }
        return json.dumps(result, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return json.dumps({"error": f"Trace '{input.trace_id}' not found"})
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Tool: Cost Breakdown ───────────────────────────────────────────


class CostInput(BaseModel):
    days: int = Field(default=7, ge=1, le=90, description="Lookback period in days")


@mcp.tool(
    name=f"{SERVICE_NAME}_costs",
    description="Get cost breakdown by model and operation over a time period.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def cost_breakdown(input: CostInput) -> str:
    client = await _get_client()
    from_time = (datetime.now(timezone.utc) - timedelta(days=input.days)).isoformat()

    try:
        # Get generations for cost data
        resp = await client.get(
            "/api/public/observations",
            params={
                "type": "GENERATION",
                "fromStartTime": from_time,
                "limit": 1000,
            },
        )
        resp.raise_for_status()
        generations = resp.json().get("data", [])

        by_model: dict[str, dict] = {}
        by_operation: dict[str, dict] = {}
        total_cost = 0.0

        for g in generations:
            model = g.get("model", "unknown")
            op = g.get("name", "unnamed")
            cost = float(g.get("totalCost", 0) or 0)
            tokens = int(g.get("promptTokens", 0) or 0) + int(g.get("completionTokens", 0) or 0)

            for grouping, key in [(by_model, model), (by_operation, op)]:
                if key not in grouping:
                    grouping[key] = {"cost": 0.0, "tokens": 0, "calls": 0}
                grouping[key]["cost"] += cost
                grouping[key]["tokens"] += tokens
                grouping[key]["calls"] += 1

            total_cost += cost

        def _format(d: dict) -> dict:
            return {
                k: {"cost_usd": round(v["cost"], 4), "tokens": v["tokens"], "calls": v["calls"]}
                for k, v in sorted(d.items(), key=lambda x: -x[1]["cost"])
            }

        return json.dumps({
            "period_days": input.days,
            "total_cost_usd": round(total_cost, 4),
            "total_generations": len(generations),
            "by_model": _format(by_model),
            "by_operation": _format(by_operation),
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Entry Point ────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")

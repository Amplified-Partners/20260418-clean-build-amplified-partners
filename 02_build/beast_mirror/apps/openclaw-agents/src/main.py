"""
OpenClaw Agent Service — FastAPI Entry Point
==============================================
Owns the API contract. Everything else is imported.

Lifespan pattern: Postgres pools open at startup, close at shutdown.
No pool creation in request handlers — that is a leak waiting to happen.

PII layer: Every user message is tokenised before it reaches the LLM.
Every LLM response is detokenised before it reaches the user.
Real PII never leaves our network.

Endpoints:
  POST /invoke       — synchronous agent call, returns full response
  POST /stream       — SSE streaming agent call
  GET  /agents       — list registered agents
  GET  /health       — basic liveness
  GET  /health/deep  — checks Postgres, Redis, LiteLLM
"""

import json
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import httpx
import redis.asyncio as aioredis
import structlog
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from agents import get_agent, get_all_agent_info
from config import settings
from memory.postgres import get_postgres_saver, get_postgres_store
from pii.tokeniser import PIITokeniser, get_redis_client
from pii.middleware import pii_wrap_invoke, tokenise_input, pii_wrap_stream_message
from schema.models import (
    AgentInfo,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    StreamEvent,
)
from streaming.sse import message_generator

log = structlog.get_logger()


# --- Lifespan: manage Postgres pools ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Open Postgres connection pools once at startup.
    Store them on app.state so request handlers can access them.
    Pools close automatically when the context exits.
    """
    log.info("starting", app=settings.APP_NAME, version=settings.APP_VERSION)

    async with get_postgres_saver() as saver, get_postgres_store() as store:
        app.state.checkpointer = saver
        app.state.store = store
        log.info("postgres_pools_ready")
        yield

    log.info("shutdown_complete")


# --- App ---

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Auth middleware (simple API key for now) ---


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Skip auth for health endpoints
    if request.url.path.startswith("/health"):
        return await call_next(request)

    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    if api_key != settings.API_KEY.get_secret_value():
        return JSONResponse(status_code=401, content={"detail": "Invalid API key"})
    return await call_next(request)


# --- Internal invoke helper (used by PII wrapper) ---


async def _raw_invoke(safe_message: str, thread_id: str, *, agent, config) -> str:
    """Run the agent with already-tokenised input. Returns raw response text."""
    from langchain_core.messages import HumanMessage

    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=safe_message)]},
        config=config,
    )
    ai_messages = [m for m in result["messages"] if hasattr(m, "type") and m.type == "ai"]
    return ai_messages[-1].content if ai_messages else "No response generated."


# --- Endpoints ---


@app.post("/invoke", response_model=ChatResponse)
async def invoke(request: ChatRequest):
    """Synchronous agent invocation with PII protection."""
    thread_id = request.thread_id or str(uuid.uuid4())

    try:
        agent = get_agent(
            request.agent_id,
            model=request.model,
            checkpointer=app.state.checkpointer,
            store=app.state.store,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    config = {"configurable": {"thread_id": thread_id}}

    # PII-wrapped invoke: tokenise -> agent -> detokenise
    response_text = await pii_wrap_invoke(
        user_message=request.message,
        thread_id=thread_id,
        invoke_fn=_raw_invoke,
        agent=agent,
        config=config,
    )

    log.info("invoke_complete", thread_id=thread_id, agent_id=request.agent_id)

    return ChatResponse(
        message=response_text,
        thread_id=thread_id,
        agent_id=request.agent_id,
    )


SSE_DATA_PREFIX = "data: "
SSE_NEWLINES = "\n\n"


async def _pii_stream_generator(agent, user_message: str, thread_id: str, model: str | None = None):
    """
    Wrap the SSE stream with PII detokenisation.
    1. Tokenise user input once
    2. Stream agent response
    3. Detokenise each message chunk
    """
    # Tokenise the input before it enters the stream
    safe_message = await tokenise_input(user_message, thread_id)

    # Create a Redis client for the duration of this stream
    redis_client = await get_redis_client()
    try:
        async for chunk in message_generator(agent, safe_message, thread_id, model):
            # Parse SSE data to detokenise message content
            if chunk.startswith(SSE_DATA_PREFIX):
                try:
                    payload = json.loads(chunk[len(SSE_DATA_PREFIX):].strip())
                    if payload.get("event") == "message" and payload.get("data"):
                        payload["data"] = await pii_wrap_stream_message(
                            payload["data"], thread_id, redis_client
                        )
                        yield SSE_DATA_PREFIX + json.dumps(payload) + SSE_NEWLINES
                        continue
                except (json.JSONDecodeError, KeyError):
                    pass
            # Pass through non-message events (done, error) unchanged
            yield chunk
    finally:
        await redis_client.aclose()


@app.post("/stream")
async def stream(request: ChatRequest):
    """SSE streaming agent invocation with PII protection."""
    thread_id = request.thread_id or str(uuid.uuid4())

    try:
        agent = get_agent(
            request.agent_id,
            model=request.model,
            checkpointer=app.state.checkpointer,
            store=app.state.store,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return EventSourceResponse(
        _pii_stream_generator(agent, request.message, thread_id, request.model)
    )


@app.get("/agents", response_model=list[AgentInfo])
async def list_agents():
    """List all registered agents."""
    return get_all_agent_info()


@app.get("/health", response_model=HealthResponse)
async def health():
    """Basic liveness. If this fails, the container is dead."""
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        timestamp=datetime.now(timezone.utc),
    )


@app.get("/health/deep", response_model=HealthResponse)
async def health_deep():
    """
    Deep health: checks Postgres, Redis, LiteLLM.
    Returns degraded if any dependency is unreachable.
    """
    checks = {}

    # Postgres
    try:
        pool = app.state.checkpointer.conn  # psycopg pool
        async with pool.connection() as conn:
            await conn.execute("SELECT 1")
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"error: {e}"

    # Redis
    try:
        rc = await get_redis_client()
        await rc.ping()
        await rc.aclose()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {e}"

    # LiteLLM
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{settings.LITELLM_BASE_URL}/health/liveliness",
                headers={"Authorization": f"Bearer {settings.LITELLM_API_KEY.get_secret_value()}"},
                timeout=5.0,
            )
            checks["litellm"] = "ok" if resp.status_code == 200 else f"status: {resp.status_code}"
    except Exception as e:
        checks["litellm"] = f"error: {e}"

    status = "ok" if all(v == "ok" for v in checks.values()) else "degraded"

    return HealthResponse(
        status=status,
        version=settings.APP_VERSION,
        timestamp=datetime.now(timezone.utc),
        checks=checks,
    )

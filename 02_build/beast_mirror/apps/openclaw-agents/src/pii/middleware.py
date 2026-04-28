"""
PII Middleware for Agent Invocations
=====================================
Wraps the tokeniser into the request/response flow.

Before agent: tokenise user message (PII → tokens)
After agent: detokenise agent response (tokens → PII)

This is NOT a FastAPI middleware — it wraps the agent call itself.
FastAPI middleware can't easily intercept JSON body content both ways.
Instead, we wrap the invoke/stream logic.

Usage in main.py:
    from pii.middleware import pii_wrap_invoke, pii_wrap_stream
"""

import redis.asyncio as aioredis

from pii.tokeniser import PIITokeniser, get_redis_client


async def pii_wrap_invoke(
    user_message: str,
    thread_id: str,
    invoke_fn,
    **invoke_kwargs,
) -> str:
    """
    Tokenise input → call agent → detokenise output.
    Returns the detokenised (real) response text.

    invoke_fn should be an async callable that takes (message, thread_id, **kwargs)
    and returns the raw agent response text.
    """
    redis_client = await get_redis_client()
    try:
        tokeniser = PIITokeniser(redis_client, thread_id)

        # Tokenise the user's message before it reaches the LLM
        safe_message = await tokeniser.tokenise(user_message)

        # Call the agent with tokenised input
        raw_response = await invoke_fn(safe_message, thread_id, **invoke_kwargs)

        # Detokenise the agent's response before returning to the user
        real_response = await tokeniser.detokenise(raw_response)

        return real_response
    finally:
        await redis_client.aclose()


async def pii_wrap_stream_message(
    message: str,
    thread_id: str,
    redis_client: aioredis.Redis | None = None,
) -> str:
    """
    Detokenise a single streamed message.
    For streaming, we tokenise once before the stream starts,
    then detokenise each message chunk as it comes through.

    Caller should create redis_client once and pass it in for efficiency.
    """
    if redis_client is None:
        redis_client = await get_redis_client()

    tokeniser = PIITokeniser(redis_client, thread_id)
    return await tokeniser.detokenise(message)


async def tokenise_input(user_message: str, thread_id: str) -> str:
    """Standalone tokenisation — call before starting a stream."""
    redis_client = await get_redis_client()
    try:
        tokeniser = PIITokeniser(redis_client, thread_id)
        return await tokeniser.tokenise(user_message)
    finally:
        await redis_client.aclose()

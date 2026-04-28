"""
Server-Sent Events Streaming
==============================
Message-based SSE (not token-based) — better for multi-agent flows
where you want complete agent messages rather than token fragments.

Protocol:
  event: token   -> partial content (for typing indicators)
  event: message -> complete agent message
  event: error   -> something went wrong
  event: done    -> stream finished
"""

import json
from collections.abc import AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.state import CompiledStateGraph as CompiledGraph


async def message_generator(
    agent: CompiledGraph,
    user_input: str,
    thread_id: str,
    model: str | None = None,
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields SSE-formatted strings.
    Each yield is a complete 'data: {...}\n\n' line.
    """
    config = {"configurable": {"thread_id": thread_id}}
    input_msg = {"messages": [HumanMessage(content=user_input)]}

    try:
        # Stream complete messages (not tokens)
        async for event in agent.astream(input_msg, config=config, stream_mode="messages"):
            msg, metadata = event
            if isinstance(msg, AIMessage) and msg.content:
                payload = {
                    "event": "message",
                    "data": msg.content,
                    "thread_id": thread_id,
                }
                yield f"data: {json.dumps(payload)}\n\n"

        # Signal completion
        yield f"data: {json.dumps({'event': 'done', 'thread_id': thread_id})}\n\n"

    except Exception as e:
        error_payload = {
            "event": "error",
            "data": str(e),
            "thread_id": thread_id,
        }
        yield f"data: {json.dumps(error_payload)}\n\n"

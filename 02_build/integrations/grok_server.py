"""
Grok MCP Server

Connects to xAI's Grok models via MCP protocol.
Provides cognitive diversity through real-time data and X integration.

Tools:
- grok_chat: Basic conversation with Grok
- grok_web_search: Web search + reasoning
- grok_x_search: X (Twitter) search + analysis
- grok_code_execute: Python code execution
- grok_reasoning: Deep reasoning mode (extended timeout)
- grok_multimodal: Analyze images with text

Part of the Cognitive Biodiversity Architecture.
"""

import os
import json
import asyncio
from typing import Any, Optional
import httpx

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server

# MCP Server
server = Server("grok")

# xAI API Configuration
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_BASE_URL = "https://api.x.ai/v1"
DEFAULT_MODEL = "grok-4"
REASONING_MODEL = "grok-4-1-fast-reasoning"
DEFAULT_TIMEOUT = 120  # 2 minutes
REASONING_TIMEOUT = 3600  # 1 hour for deep reasoning


async def call_grok_api(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    tools: Optional[list] = None,
    timeout: int = DEFAULT_TIMEOUT,
    use_responses_endpoint: bool = False,
) -> dict:
    """
    Call xAI Grok API.

    Args:
        messages: List of message dicts with role and content
        model: Model ID (grok-4 or grok-4-1-fast-reasoning)
        tools: Optional list of tools to enable (web_search, x_search, code_interpreter)
        timeout: Request timeout in seconds
        use_responses_endpoint: Use /v1/responses endpoint (for tools) instead of /v1/chat/completions

    Returns:
        API response dict
    """
    if not XAI_API_KEY:
        raise ValueError("XAI_API_KEY environment variable not set")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}",
    }

    # Choose endpoint and payload format
    if use_responses_endpoint or tools:
        # Responses endpoint uses "input" not "messages"
        endpoint = f"{XAI_BASE_URL}/responses"
        payload = {
            "model": model,
            "input": messages,
            "stream": False,
        }
    else:
        # Chat completions endpoint
        endpoint = f"{XAI_BASE_URL}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }

    # Add tools if specified
    if tools:
        payload["tools"] = tools

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            endpoint,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available Grok tools.

    6 tools covering conversation, search, reasoning, and multimodal analysis.
    """
    return [
        types.Tool(
            name="grok_chat",
            description="Chat with Grok - general purpose conversation and reasoning. Use for questions, analysis, brainstorming.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The question or prompt for Grok",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional system prompt to set context/behavior",
                    },
                    "conversation_history": {
                        "type": "array",
                        "description": "Optional previous messages for multi-turn conversation",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "content": {"type": "string"},
                            },
                        },
                    },
                },
                "required": ["prompt"],
            },
        ),
        types.Tool(
            name="grok_web_search",
            description="Search the web via Grok with built-in web_search tool. Returns current information from the internet. Use for: market research, competitor analysis, current events, fact-checking.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query or question requiring web data",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional context about what you're researching",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="grok_x_search",
            description="Search X (Twitter) via Grok's built-in x_search tool. Returns recent posts, trends, sentiment. Use for: social listening, trend detection, public opinion, brand monitoring.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for X posts",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional context about what you're analyzing",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="grok_code_execute",
            description="Execute Python code via Grok's built-in code_execution tool. Use for: calculations, data processing, testing logic, generating data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute",
                    },
                    "context": {
                        "type": "string",
                        "description": "Optional context about what the code should do",
                    },
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="grok_reasoning",
            description="Deep reasoning mode with extended thinking time (up to 1 hour timeout). Use for: complex problems, strategic decisions, multi-step analysis, difficult questions requiring deep thought.",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "The complex problem or question requiring deep reasoning",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional framing or constraints for the reasoning",
                    },
                },
                "required": ["problem"],
            },
        ),
        types.Tool(
            name="grok_multimodal",
            description="Analyze images with Grok's multimodal capabilities. Provide image URL and question. Use for: visual analysis, diagram interpretation, screenshot analysis, image Q&A.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_url": {
                        "type": "string",
                        "description": "URL of the image to analyze",
                    },
                    "question": {
                        "type": "string",
                        "description": "Question about the image",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional context or instructions",
                    },
                },
                "required": ["image_url", "question"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool calls to Grok API.

    Routes to appropriate handler based on tool name.
    """
    if not arguments:
        arguments = {}

    try:
        if name == "grok_chat":
            return await handle_grok_chat(arguments)
        elif name == "grok_web_search":
            return await handle_grok_web_search(arguments)
        elif name == "grok_x_search":
            return await handle_grok_x_search(arguments)
        elif name == "grok_code_execute":
            return await handle_grok_code_execute(arguments)
        elif name == "grok_reasoning":
            return await handle_grok_reasoning(arguments)
        elif name == "grok_multimodal":
            return await handle_grok_multimodal(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_grok_chat(arguments: dict) -> list[types.TextContent]:
    """Handle basic Grok chat."""
    prompt = arguments.get("prompt")
    system_prompt = arguments.get("system_prompt", "You are Grok, a highly intelligent AI assistant.")
    conversation_history = arguments.get("conversation_history", [])

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)

    # Add current prompt
    messages.append({"role": "user", "content": prompt})

    # Call API
    response = await call_grok_api(messages, model=DEFAULT_MODEL)

    # Extract response
    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_grok_web_search(arguments: dict) -> list[types.TextContent]:
    """Handle web search via Grok."""
    query = arguments.get("query")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Grok with web search capabilities. Search the web and provide accurate, current information."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    # Enable web_search tool
    tools = [{"type": "web_search"}]

    # Call API with web search enabled
    response = await call_grok_api(messages, model=DEFAULT_MODEL, tools=tools, use_responses_endpoint=True)

    # Extract text from responses endpoint - it's in the response text field
    assistant_message = response.get("response", {}).get("content", "")

    # If that's empty, try output field
    if not assistant_message:
        output = response.get("output", [])
        if output and isinstance(output, list) and len(output) > 0:
            # Find the last assistant message in output
            for item in reversed(output):
                if isinstance(item, dict) and item.get("role") == "assistant":
                    assistant_message = item.get("content", "")
                    break

    return [types.TextContent(type="text", text=str(assistant_message))]


async def handle_grok_x_search(arguments: dict) -> list[types.TextContent]:
    """Handle X (Twitter) search via Grok."""
    query = arguments.get("query")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Grok with X (Twitter) search capabilities. Search X posts and analyze trends, sentiment, and discussions."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    # Enable x_search tool
    tools = [{"type": "x_search"}]

    # Call API with X search enabled
    response = await call_grok_api(messages, model=DEFAULT_MODEL, tools=tools, use_responses_endpoint=True)

    # Extract text from responses endpoint
    assistant_message = response.get("response", {}).get("content", "")

    if not assistant_message:
        output = response.get("output", [])
        if output and isinstance(output, list) and len(output) > 0:
            for item in reversed(output):
                if isinstance(item, dict) and item.get("role") == "assistant":
                    assistant_message = item.get("content", "")
                    break

    return [types.TextContent(type="text", text=str(assistant_message))]


async def handle_grok_code_execute(arguments: dict) -> list[types.TextContent]:
    """Handle code execution via Grok."""
    code = arguments.get("code")
    context = arguments.get("context", "Execute the following Python code and return the result.")

    prompt = f"{context}\n\n```python\n{code}\n```"

    messages = [
        {"role": "system", "content": "You are Grok with Python code execution capabilities. Execute code and return results."},
        {"role": "user", "content": prompt},
    ]

    # Enable code_interpreter tool (correct name)
    tools = [{"type": "code_interpreter"}]

    # Call API with code execution enabled
    response = await call_grok_api(messages, model=DEFAULT_MODEL, tools=tools, use_responses_endpoint=True)

    # Extract text from responses endpoint
    assistant_message = response.get("response", {}).get("content", "")

    if not assistant_message:
        output = response.get("output", [])
        if output and isinstance(output, list) and len(output) > 0:
            for item in reversed(output):
                if isinstance(item, dict) and item.get("role") == "assistant":
                    assistant_message = item.get("content", "")
                    break

    return [types.TextContent(type="text", text=str(assistant_message))]


async def handle_grok_reasoning(arguments: dict) -> list[types.TextContent]:
    """Handle deep reasoning with extended timeout."""
    problem = arguments.get("problem")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Grok in deep reasoning mode. Take your time to think through this problem carefully and thoroughly."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": problem},
    ]

    # Use reasoning model with extended timeout
    response = await call_grok_api(
        messages,
        model=REASONING_MODEL,
        timeout=REASONING_TIMEOUT
    )

    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_grok_multimodal(arguments: dict) -> list[types.TextContent]:
    """Handle multimodal image analysis."""
    image_url = arguments.get("image_url")
    question = arguments.get("question")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Grok with vision capabilities. Analyze the image and answer the question accurately."
    )

    # xAI uses different type names: "input_image" and "input_text"
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": image_url,  # Direct URL, not nested
                    "detail": "high"
                },
                {
                    "type": "input_text",
                    "text": question
                },
            ],
        },
    ]

    # Use grok-4 for multimodal (supports images) via responses endpoint
    response = await call_grok_api(messages, model=DEFAULT_MODEL, use_responses_endpoint=True)

    # Extract text from responses endpoint
    assistant_message = response.get("response", {}).get("content", "")

    if not assistant_message:
        output = response.get("output", [])
        if output and isinstance(output, list) and len(output) > 0:
            for item in reversed(output):
                if isinstance(item, dict) and item.get("role") == "assistant":
                    assistant_message = item.get("content", "")
                    break

    return [types.TextContent(type="text", text=str(assistant_message))]


async def main():
    """Run the MCP server."""
    from mcp.server.models import InitializationOptions

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="grok",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import mcp.server.stdio
    asyncio.run(main())

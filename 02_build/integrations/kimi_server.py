"""
Kimi MCP Server (Moonshot AI)

Connects to Moonshot AI's Kimi models via MCP protocol.
Provides cognitive diversity through Chinese perspective and 256K context.

Tools:
- kimi_chat: Basic conversation with Kimi
- kimi_long_context: Analyze long documents (up to 256K tokens)
- kimi_tool_chain: Autonomous tool calling (200-300 sequential calls)
- kimi_translate: Chinese/English translation
- kimi_research: Deep research with extended context
- kimi_compare: Compare multiple documents/perspectives

Part of the Cognitive Biodiversity Architecture.
Chinese training data + 256K context + tool calling master.
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
server = Server("kimi")

# Moonshot AI API Configuration
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
MOONSHOT_BASE_URL = "https://api.moonshot.ai/v1"
DEFAULT_MODEL = "kimi-k2.5"  # Latest model with 256K context
FALLBACK_MODEL = "kimi-k2"
DEFAULT_TIMEOUT = 180  # 3 minutes
LONG_CONTEXT_TIMEOUT = 600  # 10 minutes for long docs


async def call_kimi_api(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    tools: Optional[list] = None,
    timeout: int = DEFAULT_TIMEOUT,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
) -> dict:
    """
    Call Moonshot AI Kimi API (OpenAI-compatible).

    Args:
        messages: List of message dicts with role and content
        model: Model ID (kimi-k2.5, kimi-k2, moonshot-v1-32k, etc.)
        tools: Optional list of tools for function calling
        timeout: Request timeout in seconds
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens in response

    Returns:
        API response dict
    """
    if not MOONSHOT_API_KEY:
        raise ValueError("MOONSHOT_API_KEY environment variable not set")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MOONSHOT_API_KEY}",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    # Kimi k2.5 only accepts temperature=1, so only add if explicitly set to 1
    # Otherwise omit it entirely
    if temperature == 1.0:
        payload["temperature"] = temperature

    if max_tokens:
        payload["max_tokens"] = max_tokens

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{MOONSHOT_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available Kimi tools.

    6 tools covering conversation, long context, tool chains, translation, and research.
    """
    return [
        types.Tool(
            name="kimi_chat",
            description="Chat with Kimi - Chinese-trained LLM with 256K context. Use for questions, analysis, Chinese perspective, cultural insights.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The question or prompt for Kimi",
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
                    "temperature": {
                        "type": "number",
                        "description": "Sampling temperature 0-1 (default 0.7)",
                    },
                },
                "required": ["prompt"],
            },
        ),
        types.Tool(
            name="kimi_long_context",
            description="Analyze long documents with Kimi's 256K context window. Use for: analyzing entire codebases, long reports, books, transcripts, research papers. Much larger context than Claude (200K) or Grok (2M but expensive).",
            inputSchema={
                "type": "object",
                "properties": {
                    "document": {
                        "type": "string",
                        "description": "The long document text to analyze (up to 256K tokens)",
                    },
                    "question": {
                        "type": "string",
                        "description": "What to analyze or extract from the document",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional context about the analysis task",
                    },
                },
                "required": ["document", "question"],
            },
        ),
        types.Tool(
            name="kimi_tool_chain",
            description="Autonomous tool calling - Kimi can execute 200-300 sequential tool calls. Use for: complex multi-step tasks, research pipelines, data processing workflows, autonomous problem-solving.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The complex task requiring multiple steps/tools",
                    },
                    "available_tools": {
                        "type": "array",
                        "description": "Tools Kimi can use (search, calculate, etc.)",
                        "items": {"type": "object"},
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional instructions for tool usage",
                    },
                },
                "required": ["task"],
            },
        ),
        types.Tool(
            name="kimi_translate",
            description="Chinese/English translation with cultural context. Use for: translating documents, understanding Chinese business concepts, cultural bridge, bilingual analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to translate",
                    },
                    "source_language": {
                        "type": "string",
                        "description": "Source language (zh/en)",
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Target language (zh/en)",
                    },
                    "preserve_cultural_context": {
                        "type": "boolean",
                        "description": "Explain cultural nuances (default true)",
                    },
                },
                "required": ["text", "target_language"],
            },
        ),
        types.Tool(
            name="kimi_research",
            description="Deep research with 256K context and systematic analysis. Use for: comprehensive topic research, literature review, pattern finding across multiple sources, strategic analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Research topic or question",
                    },
                    "sources": {
                        "type": "string",
                        "description": "Source materials to analyze (can be very long)",
                    },
                    "focus": {
                        "type": "string",
                        "description": "What aspect to focus on",
                    },
                },
                "required": ["topic"],
            },
        ),
        types.Tool(
            name="kimi_compare",
            description="Compare multiple documents/perspectives/viewpoints. Use for: decision-making, comparing approaches, finding consensus/differences, perspective analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "Items to compare (documents, viewpoints, etc.)",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "content": {"type": "string"},
                            },
                        },
                    },
                    "comparison_criteria": {
                        "type": "string",
                        "description": "What to compare on",
                    },
                },
                "required": ["items"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool calls to Kimi API.

    Routes to appropriate handler based on tool name.
    """
    if not arguments:
        arguments = {}

    try:
        if name == "kimi_chat":
            return await handle_kimi_chat(arguments)
        elif name == "kimi_long_context":
            return await handle_kimi_long_context(arguments)
        elif name == "kimi_tool_chain":
            return await handle_kimi_tool_chain(arguments)
        elif name == "kimi_translate":
            return await handle_kimi_translate(arguments)
        elif name == "kimi_research":
            return await handle_kimi_research(arguments)
        elif name == "kimi_compare":
            return await handle_kimi_compare(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_kimi_chat(arguments: dict) -> list[types.TextContent]:
    """Handle basic Kimi chat."""
    prompt = arguments.get("prompt")
    system_prompt = arguments.get("system_prompt", "You are Kimi, an AI assistant created by Moonshot AI.")
    conversation_history = arguments.get("conversation_history", [])
    # Note: Kimi k2.5 doesn't support temperature parameter, so we ignore it

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)

    # Add current prompt
    messages.append({"role": "user", "content": prompt})

    # Call API
    response = await call_kimi_api(messages, model=DEFAULT_MODEL)

    # Extract response
    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_kimi_long_context(arguments: dict) -> list[types.TextContent]:
    """Handle long document analysis with 256K context."""
    document = arguments.get("document")
    question = arguments.get("question")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Kimi with 256K context window. Analyze the entire document carefully and answer the question thoroughly."
    )

    # Combine document and question
    combined_prompt = f"Document:\n\n{document}\n\n---\n\nQuestion: {question}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": combined_prompt},
    ]

    # Use extended timeout for long docs
    response = await call_kimi_api(
        messages,
        model=DEFAULT_MODEL,
        timeout=LONG_CONTEXT_TIMEOUT
    )

    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_kimi_tool_chain(arguments: dict) -> list[types.TextContent]:
    """Handle autonomous tool calling."""
    task = arguments.get("task")
    available_tools = arguments.get("available_tools", [])
    system_prompt = arguments.get(
        "system_prompt",
        "You are Kimi with autonomous tool calling capabilities. Break down the task and execute tools sequentially as needed."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task},
    ]

    # If tools provided, enable tool calling
    tools = available_tools if available_tools else None

    response = await call_kimi_api(
        messages,
        model=DEFAULT_MODEL,
        tools=tools,
        timeout=LONG_CONTEXT_TIMEOUT
    )

    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_kimi_translate(arguments: dict) -> list[types.TextContent]:
    """Handle translation with cultural context."""
    text = arguments.get("text")
    source_lang = arguments.get("source_language", "auto-detect")
    target_lang = arguments.get("target_language")
    preserve_context = arguments.get("preserve_cultural_context", True)

    context_instruction = ""
    if preserve_context:
        context_instruction = " Also explain any cultural nuances, idioms, or concepts that don't translate directly."

    system_prompt = f"You are Kimi, a bilingual AI assistant. Translate accurately from {source_lang} to {target_lang}.{context_instruction}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]

    response = await call_kimi_api(messages, model=DEFAULT_MODEL)

    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_kimi_research(arguments: dict) -> list[types.TextContent]:
    """Handle deep research with extended context."""
    topic = arguments.get("topic")
    sources = arguments.get("sources", "")
    focus = arguments.get("focus", "comprehensive analysis")

    prompt = f"Research topic: {topic}\n\n"
    if sources:
        prompt += f"Source materials:\n{sources}\n\n"
    prompt += f"Focus: {focus}"

    system_prompt = "You are Kimi, a research assistant with 256K context. Provide systematic, thorough analysis with citations."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    response = await call_kimi_api(
        messages,
        model=DEFAULT_MODEL,
        timeout=LONG_CONTEXT_TIMEOUT
    )

    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_kimi_compare(arguments: dict) -> list[types.TextContent]:
    """Handle comparison of multiple items."""
    items = arguments.get("items", [])
    criteria = arguments.get("comparison_criteria", "general comparison")

    # Build comparison prompt
    prompt = f"Compare the following items based on: {criteria}\n\n"

    for idx, item in enumerate(items, 1):
        name = item.get("name", f"Item {idx}")
        content = item.get("content", "")
        prompt += f"**{name}:**\n{content}\n\n"

    system_prompt = "You are Kimi. Analyze and compare systematically, highlighting similarities, differences, strengths, and weaknesses."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    response = await call_kimi_api(
        messages,
        model=DEFAULT_MODEL,
        timeout=LONG_CONTEXT_TIMEOUT
    )

    assistant_message = response["choices"][0]["message"]["content"]

    return [types.TextContent(type="text", text=assistant_message)]


async def main():
    """Run the MCP server."""
    from mcp.server.models import InitializationOptions

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kimi",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

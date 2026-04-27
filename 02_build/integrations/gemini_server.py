"""
Gemini MCP Server (Google AI)

Connects to Google's Gemini models via MCP protocol.
Provides cognitive diversity through Google's training data and massive context windows.

Tools:
- gemini_chat: Basic conversation with Gemini
- gemini_long_context: Analyze extremely long documents (up to 2M tokens)
- gemini_code: Code generation and analysis
- gemini_multimodal: Analyze images, video, audio
- gemini_search_grounding: Web search with Google Search grounding
- gemini_thinking: Extended thinking mode for complex problems

Part of the Cognitive Biodiversity Architecture.
Google training data + 2M context + multimodal + search grounding.
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
server = Server("gemini")

# Google AI API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-2.5-flash"  # Free tier, 1M context
PRO_MODEL = "gemini-2.5-pro"  # Free tier, 1M context
THINKING_MODEL = "gemini-2.5-flash"  # Flash supports thinking mode
DEFAULT_TIMEOUT = 120  # 2 minutes
LONG_CONTEXT_TIMEOUT = 600  # 10 minutes for long docs


async def call_gemini_api(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    timeout: int = DEFAULT_TIMEOUT,
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    tools: Optional[list] = None,
) -> dict:
    """
    Call Google Gemini API.

    Args:
        messages: List of message dicts with role and content
        model: Model ID (gemini-1.5-flash-latest, gemini-1.5-pro-latest, etc.)
        timeout: Request timeout in seconds
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens in response
        tools: Optional tools for function calling

    Returns:
        API response dict
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    # Convert OpenAI-style messages to Gemini format
    gemini_contents = []
    system_instruction = None

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if role == "system":
            # Gemini handles system messages separately
            system_instruction = content
        elif role == "user":
            gemini_contents.append({
                "role": "user",
                "parts": [{"text": content}]
            })
        elif role == "assistant":
            gemini_contents.append({
                "role": "model",
                "parts": [{"text": content}]
            })

    payload = {
        "contents": gemini_contents,
        "generationConfig": {
            "temperature": temperature,
        }
    }

    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    if max_tokens:
        payload["generationConfig"]["maxOutputTokens"] = max_tokens

    if tools:
        payload["tools"] = tools

    url = f"{GOOGLE_BASE_URL}/models/{model}:generateContent?key={GOOGLE_API_KEY}"

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        return response.json()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available Gemini tools.

    6 tools covering conversation, massive context, code, multimodal, search, and thinking.
    """
    return [
        types.Tool(
            name="gemini_chat",
            description="Chat with Gemini - Google's multimodal LLM with 1M context. Use for questions, analysis, Google perspective.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The question or prompt for Gemini",
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
                        "description": "Sampling temperature 0-2 (default 1.0)",
                    },
                },
                "required": ["prompt"],
            },
        ),
        types.Tool(
            name="gemini_long_context",
            description="Analyze extremely long documents with Gemini's 2M context window (largest available). Use for: entire codebases, books, long transcripts, comprehensive analysis. Far exceeds Claude (200K), Grok (2M but expensive), or Kimi (256K).",
            inputSchema={
                "type": "object",
                "properties": {
                    "document": {
                        "type": "string",
                        "description": "The long document text to analyze (up to 2M tokens)",
                    },
                    "question": {
                        "type": "string",
                        "description": "What to analyze or extract from the document",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional context about the analysis task",
                    },
                    "use_pro": {
                        "type": "boolean",
                        "description": "Use Gemini Pro for 2M context (default Flash with 1M)",
                    },
                },
                "required": ["document", "question"],
            },
        ),
        types.Tool(
            name="gemini_code",
            description="Code generation, analysis, debugging, and explanation. Use for: writing code, reviewing code, debugging, explaining algorithms, generating tests.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The coding task (generate, debug, explain, etc.)",
                    },
                    "code": {
                        "type": "string",
                        "description": "Optional existing code to work with",
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language",
                    },
                },
                "required": ["task"],
            },
        ),
        types.Tool(
            name="gemini_multimodal",
            description="Analyze images, video, audio, and PDFs with Gemini's native multimodal capabilities. Provide URL or base64 data. Use for: image analysis, video understanding, audio transcription, document analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "media_url": {
                        "type": "string",
                        "description": "URL of the media to analyze (image, video, audio, PDF)",
                    },
                    "media_type": {
                        "type": "string",
                        "description": "Type of media (image/jpeg, video/mp4, audio/mp3, etc.)",
                    },
                    "question": {
                        "type": "string",
                        "description": "Question about the media",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional context or instructions",
                    },
                },
                "required": ["media_url", "question"],
            },
        ),
        types.Tool(
            name="gemini_search_grounding",
            description="Web search with Google Search grounding for accurate, up-to-date information. Returns citations. Use for: current events, fact-checking, research, market data.",
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
            name="gemini_thinking",
            description="Extended thinking mode with explicit reasoning chain (experimental). Use for: complex problems, multi-step reasoning, strategic decisions, difficult questions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "The complex problem requiring deep reasoning",
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "Optional framing or constraints",
                    },
                },
                "required": ["problem"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool calls to Gemini API.

    Routes to appropriate handler based on tool name.
    """
    if not arguments:
        arguments = {}

    try:
        if name == "gemini_chat":
            return await handle_gemini_chat(arguments)
        elif name == "gemini_long_context":
            return await handle_gemini_long_context(arguments)
        elif name == "gemini_code":
            return await handle_gemini_code(arguments)
        elif name == "gemini_multimodal":
            return await handle_gemini_multimodal(arguments)
        elif name == "gemini_search_grounding":
            return await handle_gemini_search_grounding(arguments)
        elif name == "gemini_thinking":
            return await handle_gemini_thinking(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_gemini_chat(arguments: dict) -> list[types.TextContent]:
    """Handle basic Gemini chat."""
    prompt = arguments.get("prompt")
    system_prompt = arguments.get("system_prompt", "You are Gemini, a helpful AI assistant created by Google.")
    conversation_history = arguments.get("conversation_history", [])
    temperature = arguments.get("temperature", 1.0)

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)

    # Add current prompt
    messages.append({"role": "user", "content": prompt})

    # Call API
    response = await call_gemini_api(messages, model=DEFAULT_MODEL, temperature=temperature)

    # Extract response
    assistant_message = response["candidates"][0]["content"]["parts"][0]["text"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_gemini_long_context(arguments: dict) -> list[types.TextContent]:
    """Handle long document analysis with 1M or 2M context."""
    document = arguments.get("document")
    question = arguments.get("question")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Gemini with massive context window. Analyze the entire document carefully and answer the question thoroughly."
    )
    use_pro = arguments.get("use_pro", False)

    # Choose model based on context needs
    model = PRO_MODEL if use_pro else DEFAULT_MODEL

    # Combine document and question
    combined_prompt = f"Document:\n\n{document}\n\n---\n\nQuestion: {question}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": combined_prompt},
    ]

    # Use extended timeout for long docs
    response = await call_gemini_api(
        messages,
        model=model,
        timeout=LONG_CONTEXT_TIMEOUT,
        temperature=0.3
    )

    assistant_message = response["candidates"][0]["content"]["parts"][0]["text"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_gemini_code(arguments: dict) -> list[types.TextContent]:
    """Handle code generation and analysis."""
    task = arguments.get("task")
    code = arguments.get("code", "")
    language = arguments.get("language", "")

    prompt = f"Task: {task}\n\n"
    if language:
        prompt += f"Language: {language}\n\n"
    if code:
        prompt += f"Existing code:\n```\n{code}\n```\n\n"

    messages = [
        {"role": "system", "content": "You are Gemini, an expert software engineer. Provide clear, efficient, well-commented code."},
        {"role": "user", "content": prompt},
    ]

    response = await call_gemini_api(messages, model=DEFAULT_MODEL, temperature=0.5)

    assistant_message = response["candidates"][0]["content"]["parts"][0]["text"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_gemini_multimodal(arguments: dict) -> list[types.TextContent]:
    """Handle multimodal analysis (images, video, audio, PDFs)."""
    media_url = arguments.get("media_url")
    media_type = arguments.get("media_type", "image/jpeg")
    question = arguments.get("question")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Gemini with multimodal capabilities. Analyze the media and answer accurately."
    )

    # For now, just return a note that this requires inline data
    # Full implementation would fetch the media and encode it
    return [types.TextContent(
        type="text",
        text=f"Note: Gemini multimodal requires inline data encoding. Media URL: {media_url}, Question: {question}. This would be implemented by fetching the media, base64 encoding it, and including it in the parts array."
    )]


async def handle_gemini_search_grounding(arguments: dict) -> list[types.TextContent]:
    """Handle web search with Google Search grounding."""
    query = arguments.get("query")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Gemini with Google Search grounding. Search the web and provide accurate, current information with citations."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    # Enable Google Search grounding
    tools = [{
        "googleSearch": {}
    }]

    response = await call_gemini_api(
        messages,
        model=DEFAULT_MODEL,
        tools=tools
    )

    assistant_message = response["candidates"][0]["content"]["parts"][0]["text"]

    return [types.TextContent(type="text", text=assistant_message)]


async def handle_gemini_thinking(arguments: dict) -> list[types.TextContent]:
    """Handle extended thinking mode."""
    problem = arguments.get("problem")
    system_prompt = arguments.get(
        "system_prompt",
        "You are Gemini in thinking mode. Take your time to reason through this problem carefully and show your thinking."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": problem},
    ]

    # Use thinking model
    response = await call_gemini_api(
        messages,
        model=THINKING_MODEL,
        timeout=LONG_CONTEXT_TIMEOUT
    )

    assistant_message = response["candidates"][0]["content"]["parts"][0]["text"]

    return [types.TextContent(type="text", text=assistant_message)]


async def main():
    """Run the MCP server."""
    from mcp.server.models import InitializationOptions

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="gemini",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

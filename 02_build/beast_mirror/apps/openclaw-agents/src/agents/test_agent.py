"""
Test Agent — proof-of-life for the orchestration layer.
Uses create_react_agent with a simple search tool.
This validates: LiteLLM routing, Postgres checkpointing, SSE streaming.
"""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph.state import CompiledStateGraph as CompiledGraph

from config import settings

AGENT_ID = "test"
AGENT_DESCRIPTION = "Simple test agent with search. Validates the full stack."
AGENT_TOOLS: list[str] = ["search"]


def _make_search_tool():
    """Basic SearXNG search tool. Proves tool calling works end-to-end."""
    import httpx
    from langchain_core.tools import tool

    @tool
    def search(query: str) -> str:
        """Search the web using SearXNG. Returns top 3 results."""
        resp = httpx.get(
            f"{settings.SEARXNG_BASE_URL}/search",
            params={"q": query, "format": "json", "engines": "google", "categories": "general"},
            timeout=10.0,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])[:3]
        if not results:
            return "No results found."
        return "\n\n".join(
            f"**{r['title']}**\n{r.get('content', 'No snippet')}\n{r['url']}"
            for r in results
        )

    return search


def create_agent(model: str | None = None, checkpointer=None, store=None) -> CompiledGraph:
    """Build the test agent. Called by the registry."""
    llm = ChatOpenAI(
        model=model or settings.DEFAULT_MODEL,
        base_url=settings.LITELLM_BASE_URL,
        api_key=settings.LITELLM_API_KEY.get_secret_value(),
        temperature=0,
    )
    tools = [_make_search_tool()]
    return create_react_agent(
        llm,
        tools,
        checkpointer=checkpointer,
        store=store,
    )

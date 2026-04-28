"""
Marketing Engine — Research Agent
Gathers market intelligence for content generation.

Runs daily at 6am on The Beast.
Uses SearXNG for web search, FalkorDB for knowledge graph context.
"""

import asyncio
import httpx
import yaml
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field

logger = logging.getLogger("marketing.research")


@dataclass
class ResearchResult:
    """One piece of market intelligence."""
    topic: str
    source: str
    summary: str
    relevance_score: float  # 0-1
    content_type: str       # "trend", "competitor", "local_event", "seasonal", "news"
    raw_data: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class ResearchBrief:
    """Complete research output for content agent."""
    client_id: str
    date: str
    results: list[ResearchResult]
    suggested_topics: list[str]
    seasonal_context: str
    local_context: str


class ResearchAgent:
    """
    Gathers market intelligence for a client.

    Flow:
    1. Load client config
    2. Check seasonal relevance (what month/season)
    3. Search for local market trends
    4. Search for competitor activity
    5. Search for local events/news
    6. Query knowledge graph for client context
    7. Score and rank findings
    8. Output research brief for content agent
    """

    def __init__(self, config_path: str = "/app/config/engine_config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.searxng_url = self.config["services"]["searxng"]["base_url"]
        self.max_results = self.config["services"]["searxng"]["max_results"]

    async def search(self, query: str, categories: str = "general") -> list[dict]:
        """Search via SearXNG JSON API."""
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.get(
                    f"{self.searxng_url}/search",
                    params={
                        "q": query,
                        "format": "json",
                        "categories": categories,
                        "language": "en-GB",
                        "time_range": "month",
                    },
                )
                resp.raise_for_status()
                data = resp.json()
                return data.get("results", [])[:self.max_results]
            except Exception as e:
                logger.error(f"SearXNG search failed: {e}")
                return []

    def get_seasonal_context(self) -> tuple[str, list[str]]:
        """Determine current season and relevant topics."""
        month = datetime.now().month
        season_map = {
            12: "winter", 1: "winter", 2: "winter",
            3: "spring", 4: "spring", 5: "spring",
            6: "summer", 7: "summer", 8: "summer",
            9: "autumn", 10: "autumn", 11: "autumn",
        }
        season = season_map[month]
        return season, []  # Topics loaded from client config

    async def research_local_market(self, client_config: dict) -> list[ResearchResult]:
        """Search for local market trends and news."""
        location = client_config["business"]["location"]
        business_type = client_config["business"]["type"]
        area = location["area"]
        city = location["city"]

        queries = [
            f"{business_type} tips {city} {datetime.now().year}",
            f"{area} local news community events",
            f"{business_type} trends UK {datetime.now().strftime('%B %Y')}",
            f"home improvement {city} popular",
        ]

        results = []
        for query in queries:
            search_results = await self.search(query)
            for sr in search_results:
                results.append(ResearchResult(
                    topic=sr.get("title", ""),
                    source=sr.get("url", ""),
                    summary=sr.get("content", ""),
                    relevance_score=0.5,  # Scored later by LLM
                    content_type="trend",
                    raw_data=sr,
                ))

        return results

    async def research_competitors(self, client_config: dict) -> list[ResearchResult]:
        """Check what competitors are posting."""
        competitors = client_config.get("competitors", {}).get("local", [])
        location = client_config["business"]["location"]
        business_type = client_config["business"]["type"]

        results = []
        # Search for competitor social media activity
        query = f"{business_type} {location['city']} social media marketing"
        search_results = await self.search(query)
        for sr in search_results:
            results.append(ResearchResult(
                topic=sr.get("title", ""),
                source=sr.get("url", ""),
                summary=sr.get("content", ""),
                relevance_score=0.4,
                content_type="competitor",
                raw_data=sr,
            ))

        return results

    async def run(self, client_id: str) -> ResearchBrief:
        """Run full research cycle for a client."""
        # Load client config
        client_path = Path(f"/app/config/clients/{client_id}.yaml")
        with open(client_path) as f:
            client_config = yaml.safe_load(f)

        logger.info(f"Starting research for {client_id}")

        # Get seasonal context
        season, _ = self.get_seasonal_context()
        seasonal_topics = (
            client_config.get("content", {})
            .get("topics", {})
            .get("seasonal", {})
            .get(season, [])
        )

        # Run searches concurrently
        local_results, competitor_results = await asyncio.gather(
            self.research_local_market(client_config),
            self.research_competitors(client_config),
        )

        all_results = local_results + competitor_results

        # Build brief
        brief = ResearchBrief(
            client_id=client_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            results=all_results,
            suggested_topics=seasonal_topics + client_config.get("content", {}).get("topics", {}).get("evergreen", []),
            seasonal_context=f"Current season: {season}. Seasonal topics: {', '.join(seasonal_topics)}",
            local_context=f"Service area: {', '.join(client_config['business'].get('service_area', []))}",
        )

        logger.info(f"Research complete: {len(all_results)} results, {len(brief.suggested_topics)} topic suggestions")
        return brief


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = ResearchAgent()
    brief = asyncio.run(agent.run("jesmond-plumbing"))
    print(json.dumps({
        "client": brief.client_id,
        "date": brief.date,
        "result_count": len(brief.results),
        "suggested_topics": brief.suggested_topics[:5],
        "seasonal": brief.seasonal_context,
    }, indent=2))

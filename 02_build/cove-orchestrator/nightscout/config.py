"""NightScout configuration and source definitions."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum


class SourceType(str, Enum):
    RSS = "rss"
    SEARXNG = "searxng"
    API = "api"
    WEB_SCRAPE = "web_scrape"


class RelevanceTier(str, Enum):
    NOISE = "noise"           # < 4.0
    BRIEFING = "briefing"     # 4.0 - 6.9
    RD_PIPELINE = "rd_pipeline"  # 7.0 - 8.9
    CRITICAL = "critical"     # 9.0 - 10.0

    @classmethod
    def from_score(cls, score: float) -> "RelevanceTier":
        if score >= 9.0:
            return cls.CRITICAL
        if score >= 7.0:
            return cls.RD_PIPELINE
        if score >= 4.0:
            return cls.BRIEFING
        return cls.NOISE


@dataclass(frozen=True)
class SourceDef:
    """Definition of an intelligence source."""
    name: str
    source_type: SourceType
    url: str
    category: str
    fetch_config: dict = field(default_factory=dict)
    enabled: bool = True


# ============================================================
# Environment
# ============================================================
SEARXNG_URL = os.getenv("SEARXNG_URL", "https://search.beast.amplifiedpartners.ai")
LITELLM_URL = os.getenv("LITELLM_URL", "http://localhost:4000")
POSTGRES_DSN = os.getenv("POSTGRES_DSN", "postgresql://cove:cove@localhost:5432/cove")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Scoring model — runs through LiteLLM → Ollama
SCORING_MODEL = os.getenv("NIGHTSCOUT_SCORING_MODEL", "cheap")  # maps to deepseek/qwen via LiteLLM

# How many items to score per batch (controls concurrency)
SCORING_BATCH_SIZE = int(os.getenv("NIGHTSCOUT_BATCH_SIZE", "10"))

# ============================================================
# Source Definitions — The 50+ Sources
# ============================================================
# Organised by category. SearXNG queries are the fastest to add.
# RSS feeds give us structured data. APIs for specific platforms.
# ============================================================

SOURCES: list[SourceDef] = [
    # --- AI Research & News ---
    SourceDef("Anthropic Blog", SourceType.RSS, "https://www.anthropic.com/feed.xml", "ai_research"),
    SourceDef("OpenAI Blog", SourceType.RSS, "https://openai.com/blog/rss.xml", "ai_research"),
    SourceDef("DeepMind Blog", SourceType.RSS, "https://deepmind.google/blog/rss.xml", "ai_research"),
    SourceDef("Hugging Face Blog", SourceType.RSS, "https://huggingface.co/blog/feed.xml", "ai_research"),
    SourceDef("AI News - SearXNG", SourceType.SEARXNG, "artificial intelligence breakthroughs 2026", "ai_research",
              {"categories": "news", "time_range": "day"}),
    SourceDef("LLM Developments", SourceType.SEARXNG, "large language model new release", "ai_research",
              {"categories": "news,it", "time_range": "day"}),
    SourceDef("Agent AI News", SourceType.SEARXNG, "AI agents autonomous software", "ai_research",
              {"categories": "news,it", "time_range": "day"}),
    SourceDef("MCP Protocol News", SourceType.SEARXNG, "model context protocol MCP servers", "ai_research",
              {"categories": "news,it", "time_range": "week"}),

    # --- SMB & Business Technology ---
    SourceDef("SMB AI Adoption", SourceType.SEARXNG, "small business AI adoption tools", "smb_tech",
              {"categories": "news", "time_range": "day"}),
    SourceDef("SMB Automation", SourceType.SEARXNG, "small business automation software 2026", "smb_tech",
              {"categories": "news", "time_range": "day"}),
    SourceDef("Hacker News", SourceType.RSS, "https://hnrss.org/best?count=30", "smb_tech"),
    SourceDef("TechCrunch AI", SourceType.RSS, "https://techcrunch.com/category/artificial-intelligence/feed/", "smb_tech"),
    SourceDef("The Verge AI", SourceType.RSS, "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "smb_tech"),

    # --- Competitors & Market ---
    SourceDef("AI Consultancy Market", SourceType.SEARXNG, "AI consultancy small business UK", "competitor",
              {"categories": "news", "time_range": "week"}),
    SourceDef("AI Operating System", SourceType.SEARXNG, "AI operating system business automation", "competitor",
              {"categories": "news,it", "time_range": "week"}),

    # --- Infrastructure & DevOps ---
    SourceDef("Temporal.io Blog", SourceType.RSS, "https://temporal.io/blog/feed.xml", "infrastructure"),
    SourceDef("Docker Blog", SourceType.RSS, "https://www.docker.com/blog/feed/", "infrastructure"),
    SourceDef("Self-Hosted News", SourceType.SEARXNG, "self-hosted open source server tools", "infrastructure",
              {"categories": "it", "time_range": "week"}),
    SourceDef("Hetzner News", SourceType.SEARXNG, "Hetzner dedicated server updates", "infrastructure",
              {"categories": "news,it", "time_range": "month"}),

    # --- Graph & Knowledge ---
    SourceDef("FalkorDB News", SourceType.SEARXNG, "FalkorDB graph database", "knowledge",
              {"categories": "it", "time_range": "month"}),
    SourceDef("Knowledge Graphs AI", SourceType.SEARXNG, "knowledge graph AI agents memory", "knowledge",
              {"categories": "it", "time_range": "week"}),

    # --- Voice & Communication ---
    SourceDef("Voice AI News", SourceType.SEARXNG, "voice AI assistant phone agent", "communication",
              {"categories": "news,it", "time_range": "week"}),
    SourceDef("Email AI Automation", SourceType.SEARXNG, "AI email automation triage", "communication",
              {"categories": "news,it", "time_range": "week"}),

    # --- Finance & Fintech ---
    SourceDef("Stripe Updates", SourceType.RSS, "https://stripe.com/blog/feed.rss", "finance"),
    SourceDef("Fintech SMB", SourceType.SEARXNG, "fintech small business tools 2026", "finance",
              {"categories": "news", "time_range": "week"}),

    # --- Regulation & Compliance ---
    SourceDef("AI Regulation UK", SourceType.SEARXNG, "AI regulation UK business compliance", "regulation",
              {"categories": "news", "time_range": "week"}),
    SourceDef("Data Protection AI", SourceType.SEARXNG, "GDPR AI data protection business", "regulation",
              {"categories": "news", "time_range": "month"}),

    # --- Productivity & Psychology ---
    SourceDef("Productivity Science", SourceType.SEARXNG, "productivity science behavioural nudge", "behavioural",
              {"categories": "news,science", "time_range": "month"}),
    SourceDef("Decision Making", SourceType.SEARXNG, "decision making frameworks business", "behavioural",
              {"categories": "news,science", "time_range": "month"}),
]

# Convenience: count by category
SOURCE_CATEGORIES = {}
for s in SOURCES:
    SOURCE_CATEGORIES.setdefault(s.category, []).append(s.name)

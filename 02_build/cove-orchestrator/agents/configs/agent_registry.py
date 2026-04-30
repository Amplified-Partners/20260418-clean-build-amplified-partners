"""
Agent Registry — Role definitions, model routing, MCP server assignments
=========================================================================
Single source of truth for: who does what, with which model, using which tools.
"""

from dataclasses import dataclass, field


@dataclass
class AgentConfig:
    role: str
    display_name: str
    model_tier: str                          # cheap, medium, premium
    system_prompt_file: str                  # Path to prompt template
    mcp_servers: list[str] = field(default_factory=list)
    max_tokens: int = 8192
    temperature: float = 0.0                 # Deterministic by default
    approval_tier: int = 3                   # Default: human review
    description: str = ""


AGENT_REGISTRY: dict[str, AgentConfig] = {
    "coder": AgentConfig(
        role="coder",
        display_name="Coder Agent",
        model_tier="medium",                 # Claude Sonnet — fast + capable
        system_prompt_file="agents/prompts/coder.md",
        mcp_servers=["postgresql_mcp", "github_mcp", "filesystem_mcp"],
        description="Writes code, runs tests, creates PRs. The workhorse.",
    ),
    "security": AgentConfig(
        role="security",
        display_name="Security Agent",
        model_tier="premium",                # Claude Opus — needs deep reasoning
        system_prompt_file="agents/prompts/security.md",
        mcp_servers=["postgresql_mcp", "github_mcp", "filesystem_mcp"],
        temperature=0.0,
        approval_tier=4,                     # Always needs Ewan review
        description="Reviews code for security, dependency vulns, secrets exposure.",
    ),
    "enforcer": AgentConfig(
        role="enforcer",
        display_name="Enforcer Agent",
        model_tier="cheap",                  # DeepSeek — fast linting
        system_prompt_file="agents/prompts/enforcer.md",
        mcp_servers=["filesystem_mcp"],
        approval_tier=0,                     # Auto-approve (it's just linting)
        description="Lints, formats, checks conventions. Zero tolerance for slop.",
    ),
    "architect": AgentConfig(
        role="architect",
        display_name="Architect Agent",
        model_tier="premium",                # Claude Opus — architecture decisions
        system_prompt_file="agents/prompts/architect.md",
        mcp_servers=["postgresql_mcp", "github_mcp", "filesystem_mcp", "litellm_mcp"],
        approval_tier=5,                     # Ewan only
        description="Plans architecture, decomposes tasks, reviews system design.",
    ),
    "reviewer": AgentConfig(
        role="reviewer",
        display_name="Code Reviewer",
        model_tier="medium",                 # Sonnet — good enough for reviews
        system_prompt_file="agents/prompts/reviewer.md",
        mcp_servers=["github_mcp", "filesystem_mcp"],
        approval_tier=2,                     # Agent review sufficient
        description="Reviews PRs, checks quality, suggests improvements.",
    ),
    "openclaw": AgentConfig(
        role="openclaw",
        display_name="OpenClaw Recorder",
        model_tier="medium",                 # Sonnet — good enough for synthesis and logging
        system_prompt_file="agents/prompts/openclaw.md",
        mcp_servers=["filesystem_mcp", "github_mcp", "linear_mcp"],
        approval_tier=0,                     # Auto-approve for writing notes
        description="Note-taker and recorder. Maintains session logs and records all decisions, enforcing Layer 0 laws.",
    ),
    
    # ============================================================
    # UNIT GAMMA: AMPLIFIED MARKETING SWARM (10-Agent Test Chunk)
    # ============================================================
    "mktg_director": AgentConfig(
        role="mktg_director",
        display_name="Marketing Director",
        model_tier="premium",
        system_prompt_file="agents/prompts/mktg_director.md",
        mcp_servers=["linear_mcp", "slack_mcp", "filesystem_mcp"],
        approval_tier=5, # Ewan/Arbiter approval for campaign launch
        description="Orchestrates marketing campaigns, approves content atomization, maintains brand voice.",
    ),
    "mktg_researcher": AgentConfig(
        role="mktg_researcher",
        display_name="Content Researcher",
        model_tier="medium",
        system_prompt_file="agents/prompts/mktg_researcher.md",
        mcp_servers=["filesystem_mcp"],
        approval_tier=0,
        description="Scrapes trends, extracts hooks from the Vault, and performs Literature-Based Discovery for marketing.",
    ),
    "mktg_copywriter_short": AgentConfig(
        role="mktg_copywriter_short",
        display_name="Short-Form Copywriter",
        model_tier="cheap",
        system_prompt_file="agents/prompts/mktg_copywriter_short.md",
        mcp_servers=["filesystem_mcp"],
        approval_tier=2,
        description="Writes high-impact short-form hooks (X, LinkedIn) based on value-first principles.",
    ),
    "mktg_copywriter_long": AgentConfig(
        role="mktg_copywriter_long",
        display_name="Long-Form Copywriter",
        model_tier="medium",
        system_prompt_file="agents/prompts/mktg_copywriter_long.md",
        mcp_servers=["filesystem_mcp"],
        approval_tier=2,
        description="Writes deep-dive newsletters, blog posts, and technical marketing articles.",
    ),
    "mktg_designer_prompt": AgentConfig(
        role="mktg_designer_prompt",
        display_name="Visual Prompt Engineer",
        model_tier="medium",
        system_prompt_file="agents/prompts/mktg_designer_prompt.md",
        mcp_servers=["filesystem_mcp"],
        approval_tier=1,
        description="Generates highly specific Midjourney/Flux prompts for visual marketing assets.",
    ),
    "mktg_seo": AgentConfig(
        role="mktg_seo",
        display_name="SEO Specialist",
        model_tier="cheap",
        system_prompt_file="agents/prompts/mktg_seo.md",
        mcp_servers=["filesystem_mcp"],
        approval_tier=0,
        description="Optimizes content for search intent and structures data for maximum indexability.",
    ),
    "mktg_editor": AgentConfig(
        role="mktg_editor",
        display_name="Chief Editor",
        model_tier="medium",
        system_prompt_file="agents/prompts/mktg_editor.md",
        mcp_servers=["filesystem_mcp"],
        approval_tier=3, # Requires human/Arbiter sign-off before distribution
        description="Proofreads, enforces Layer 0 compliance, and ensures tone matches Amplified Partners.",
    ),
    "mktg_engagement": AgentConfig(
        role="mktg_engagement",
        display_name="Community Engagement",
        model_tier="cheap",
        system_prompt_file="agents/prompts/mktg_engagement.md",
        mcp_servers=["slack_mcp", "filesystem_mcp"],
        approval_tier=2,
        description="Drafts responses and interacts with community inbound leads.",
    ),
    "mktg_analytics": AgentConfig(
        role="mktg_analytics",
        display_name="Marketing Analyst",
        model_tier="medium",
        system_prompt_file="agents/prompts/mktg_analytics.md",
        mcp_servers=["postgresql_mcp", "filesystem_mcp"],
        approval_tier=0,
        description="Reviews metrics and telemetry to feed quantitative data back into the strategy loop.",
    ),
    "mktg_distributor": AgentConfig(
        role="mktg_distributor",
        display_name="Content Distributor",
        model_tier="cheap",
        system_prompt_file="agents/prompts/mktg_distributor.md",
        mcp_servers=["slack_mcp", "telegram_mcp"],
        approval_tier=4, # High security check before API payload dispatch
        description="Formats content for specific APIs and dispatches the final payloads.",
    ),
}


def get_agent(role: str) -> AgentConfig:
    if role not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent role: {role}. Available: {list(AGENT_REGISTRY.keys())}")
    return AGENT_REGISTRY[role]


# Model tier → LiteLLM model name mapping
MODEL_TIER_MAP = {
    "cheap": "cheap",       # Routes to DeepSeek via LiteLLM
    "medium": "medium",     # Routes to Claude Sonnet via LiteLLM
    "premium": "premium",   # Routes to Claude Opus via LiteLLM
}

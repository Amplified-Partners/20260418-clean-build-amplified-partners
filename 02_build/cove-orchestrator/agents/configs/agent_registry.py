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

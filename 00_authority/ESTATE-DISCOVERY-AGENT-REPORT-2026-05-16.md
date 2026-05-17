---
title: "Amplified Partners Estate Discovery — Agent Report"
date: "2026-05-16"
signed_by: "Devon (Devin / Cognition) — session devin-bba3748d3fa545c2b32990d630b17e9a"
epistemic_status: "MEASURED — direct repository inspection, line counts, file enumeration. All numbers from live scans."
version: "v1"
---

# Estate Discovery — Agent Report

**Scan date:** 2026-05-16 08:58–09:02 UTC
**Method:** Full clone + enumeration of all 41 repositories in the Amplified-Partners GitHub organisation.
**Signed-by:** Devon — session `devin-bba3748d3fa545c2b32990d630b17e9a`

---

## 1. Estate Summary

```json
{
  "scan_date": "2026-05-16T09:02:00Z",
  "total_repositories": 41,
  "active_repositories": 32,
  "stub_repositories": 9,
  "total_files": 38172,
  "total_size_on_disk_mb": 574,
  "lines_of_code": {
    "python": 262044,
    "typescript": 272555,
    "javascript": 5768,
    "markdown": 2907801,
    "total_code_excl_markdown": 540367
  },
  "markdown_documents": {
    "vault": 4561,
    "corpus_raw": 7753,
    "clean_build": 849,
    "total_estate": 13500
  },
  "api_endpoints_total": 230,
  "database_migrations": 14,
  "docker_compose_services": 12,
  "mcp_servers": 14,
  "github_actions_workflows": 19,
  "ci_cd_repos": 13
}
```

---

## 2. Repository Inventory

### 2.1 Active Repositories (32)

```json
[
  {
    "name": "clean-build",
    "role": "Governed operating environment — authority, truth, build, shadow tiers",
    "commits": 229,
    "lines": 2224863,
    "languages": {"python": 134, "typescript": 19, "markdown": 849, "yaml": 20},
    "docker_files": 13,
    "ci_workflows": 5,
    "authority_files": 21,
    "status": "PRIMARY — highest commit velocity"
  },
  {
    "name": "crm",
    "role": "AI-powered CRM for UK SMBs — Founder Interview, Business Brain, Intelligence",
    "commits": 164,
    "lines": 141980,
    "languages": {"python": 228, "typescript": 47, "javascript": 2, "markdown": 145, "yaml": 5},
    "api_endpoints": 142,
    "db_migrations": 14,
    "mcp_servers": 5,
    "ci_workflows": 4,
    "integrations": ["Xero", "QuickBooks", "Stripe", "Calendar", "Retell AI", "Twilio", "Telegram"],
    "intelligence_features": [
      "cash_flow_predictor", "death_spiral_detector", "clv_tracker",
      "exit_strategy", "quote_followup", "payment_chaser",
      "service_reminder", "parts_concierge", "portfolio_generator",
      "voice_quote_generator", "bottleneck_finder"
    ],
    "status": "ACTIVE — second-highest commit velocity, not yet deployed to Beast"
  },
  {
    "name": "vault",
    "role": "Personal and business knowledge vault — 4,561 Markdown files via Obsidian",
    "commits": 222,
    "lines": 323405,
    "markdown_files": 4561,
    "sections": ["_inbox", "_inbox-uncategorised", "_inbox-voice", "_inbox-work", "_staging", "_system", "config", "eli", "imported-business-docs", "infra-ai-stack", "knowledge-qdrant", "openclaw", "projects", "research", "scripts", "the-room", "therapy-suite", "transcripts", "work", "work-covered-ai"],
    "status": "ACTIVE — high commit velocity, knowledge corpus"
  },
  {
    "name": "amplified-site",
    "role": "Public-facing website — React/Express/PostgreSQL/Drizzle full-stack platform",
    "commits": 59,
    "lines": 16203,
    "languages": {"python": 3, "typescript": 76, "javascript": 1, "markdown": 6, "yaml": 2},
    "stack": ["React", "Express", "PostgreSQL", "Drizzle ORM", "Radix UI", "Tailwind CSS", "Vite"],
    "ci_workflows": 1,
    "status": "ACTIVE"
  },
  {
    "name": "amplified-machine",
    "role": "Product engine — LangGraph agent graphs, content creation, financial analysis, RAG",
    "commits": 1,
    "lines": 12949,
    "languages": {"python": 98, "markdown": 4, "yaml": 4},
    "docker_files": 8,
    "ci_workflows": 1,
    "services": ["ch-pipeline", "finance-engine"],
    "agent_graphs": [
      "cne_agent", "content_director", "content_slicer", "distribution_director",
      "email_sequence", "engagement_director", "master_agent", "reddit_engine",
      "research_director", "social_publisher", "testing_agent", "video_pipeline",
      "waitlist_nurture", "wellbeing_agent"
    ],
    "knowledge_modules": ["graph_ops", "graph_schema", "graphiti_ops", "grounding", "rag"],
    "status": "ACTIVE — foundational product engine"
  },
  {
    "name": "beast-code-export",
    "role": "Full code extraction from Beast (Hetzner AX162-R) — forensic snapshot",
    "commits": 1,
    "lines": 11592,
    "total_files_approx": 23110,
    "size_mb": 390,
    "contains": ["amplified-machine", "amplified-voice-agent", "xai-phone-agent", "openclaw", "openclaw_source", "nexus", "backups"],
    "status": "ARCHIVE — point-in-time snapshot of Beast filesystem"
  },
  {
    "name": "corpus-raw",
    "role": "Raw source corpus — unprocessed research, drop waves, AI exports",
    "commits": 7,
    "lines": 289232,
    "markdown_files": 7753,
    "status": "ACTIVE — raw ingestion corpus"
  },
  {
    "name": "pudding-core",
    "role": "APDS scoring engine — Four Russian Stack (Kolmogorov, Kantorovich, Markov, Pontryagin)",
    "commits": 9,
    "lines": 4551,
    "languages": {"python": 25},
    "modules": {
      "four_russian_stack": ["kolmogorov.py", "kantorovich.py", "markov.py", "pontryagin.py", "pipeline.py", "schema.py"],
      "testing": ["abc_discovery.py", "coverage.py", "discovery_test.py", "labeller.py", "llm.py", "pairwise.py", "permutation.py", "utils.py"]
    },
    "python_lines": 4260,
    "status": "ACTIVE — mathematical retrieval pipeline"
  },
  {
    "name": "pudding-testing",
    "role": "PUDDING taxonomy validation harness — Fleiss' Kappa, permutation tests",
    "commits": 1,
    "lines": 3066,
    "languages": {"python": 12},
    "python_lines": 2826,
    "status": "ACTIVE — validation/testing companion to pudding-core"
  },
  {
    "name": "byker-production",
    "role": "AI-powered SMB consultancy orchestrator — KiloRouter, fleet management, diagnostics",
    "commits": 10,
    "lines": 18461,
    "languages": {"python": 26, "markdown": 18, "yaml": 3},
    "api_endpoints": 47,
    "ci_workflows": 1,
    "subsystems": ["cover_ai/api", "cover_ai/diagnostic", "cover_ai/outreach", "cover_ai/website"],
    "status": "ACTIVE"
  },
  {
    "name": "marketing-engine",
    "role": "Autonomous marketing pipeline — research → content → atomization → publishing",
    "commits": 1,
    "lines": 7405,
    "languages": {"python": 14, "markdown": 11, "yaml": 9},
    "api_endpoints": 19,
    "docker_files": 2,
    "ci_workflows": 1,
    "agents": ["research_agent", "content_agent", "content_atomizer", "publishing_agent"],
    "rubrics": ["compliance_rubric", "quality_rubric", "tone_rubric"],
    "status": "ACTIVE — content pipeline"
  },
  {
    "name": "amplified-knowledge-mcp",
    "role": "MCP server — tiered access to FalkorDB (graph) + Qdrant (vector) knowledge base",
    "commits": 3,
    "lines": 1144,
    "languages": {"python": 8, "yaml": 2},
    "docker_files": 2,
    "modules": ["server.py", "falkordb_client.py", "qdrant_client.py", "embedder.py", "security.py", "audit.py", "config.py"],
    "note": "FalkorDB and Qdrant DEPRECATED — migrating to PostgreSQL + Apache AGE + pgvector",
    "status": "ACTIVE — needs migration to new data architecture"
  },
  {
    "name": "enforcer",
    "role": "Infrastructure health monitoring — deterministic checks on Beast containers and DBs",
    "commits": 1,
    "lines": 2042,
    "languages": {"python": 7, "yaml": 4},
    "docker_files": 3,
    "api_endpoints": 3,
    "status": "ACTIVE"
  },
  {
    "name": "cost-tools",
    "role": "Anthropic API proxy — cost tracking, model routing, semantic caching, budget enforcement",
    "commits": 1,
    "lines": 1977,
    "languages": {"python": 3, "yaml": 2},
    "docker_files": 2,
    "modules": ["token_proxy.py", "context_compressor.py", "daily_cost_report.py"],
    "status": "ACTIVE"
  },
  {
    "name": "anthropic-token-proxy",
    "role": "Local macOS proxy for Anthropic API — model routing, caching, compression",
    "commits": 3,
    "lines": 1786,
    "languages": {"python": 3},
    "modules": ["token_proxy.py", "context_compressor.py", "daily_cost_report.py"],
    "status": "ACTIVE — local macOS companion to cost-tools"
  },
  {
    "name": "ground-truth",
    "role": "Portable Spine — canonical governance and operating framework for entire estate",
    "commits": 1,
    "lines": 3732,
    "markdown_files": 21,
    "ci_workflows": 3,
    "key_files": ["README.md", "AGENTS.md", "TERMINOLOGY.md", "OPENCLAW.md", "STATE.md", "CANONICAL.md", "THE-AMPLIFIED-METHOD.md", "STATUS.md", "VERIFICATION.md"],
    "status": "ACTIVE — constitutional source of truth"
  },
  {
    "name": "perplexity-research",
    "role": "Research intake — Perplexity drops, AI-governed Five Rods review pipeline",
    "commits": 1,
    "lines": 6568,
    "markdown_files": 28,
    "ci_workflows": 1,
    "status": "ACTIVE — research pipeline"
  },
  {
    "name": "mission-control",
    "role": "Enterprise dashboard — Next.js 15, decision tracking, dependency management",
    "commits": 1,
    "lines": 2224,
    "languages": {"typescript": 19},
    "ci_workflows": 1,
    "docker_files": 2,
    "status": "ACTIVE — governance dashboard"
  },
  {
    "name": "agent-comms",
    "role": "Async inter-agent communication hub — governance, coordination, operational logs",
    "commits": 1,
    "lines": 1833,
    "markdown_files": 24,
    "status": "ACTIVE — agent coordination"
  },
  {
    "name": "awesome-openclaw-agents",
    "role": "Agent operations workspace — APDS harvester, AIVault forensics, Sentinel monitor, Hazel rules",
    "commits": 1,
    "lines": 10002,
    "languages": {"python": 8, "markdown": 33, "yaml": 5},
    "ci_workflows": 1,
    "status": "ACTIVE — operational toolkit"
  },
  {
    "name": "openclaw-claw",
    "role": "Multi-agent orchestration framework — Clawd, Bravo, Charlie, Delta agents",
    "commits": 1,
    "lines": 1526,
    "markdown_files": 8,
    "status": "ACTIVE — agent framework docs"
  },
  {
    "name": "openclaw-knowledge",
    "role": "OpenClaw knowledge base — messaging gateway, agent workspace, memory persistence",
    "commits": 1,
    "lines": 1239,
    "markdown_files": 11,
    "status": "ACTIVE — knowledge documentation"
  },
  {
    "name": "devon-memory",
    "role": "Devin persistent memory — portable spine, working memory, compound engineering methodology",
    "commits": 1,
    "lines": 5830,
    "markdown_files": 35,
    "ci_workflows": 1,
    "status": "ACTIVE"
  },
  {
    "name": "plumb",
    "role": "Sovereign workspace for Claude Code agent — truth-checking, drift detection",
    "commits": 1,
    "lines": 16557,
    "markdown_files": 13,
    "status": "ACTIVE — Claude agent workspace"
  },
  {
    "name": "portable-spine",
    "role": "Constitution distribution repo — spine files for all agents",
    "commits": 1,
    "lines": 3443,
    "markdown_files": 30,
    "ci_workflows": 1,
    "status": "ACTIVE"
  },
  {
    "name": "dotfiles",
    "role": "Multi-Mac dotfiles — Claude Code CLAUDE.md sync, Gitleaks, Shellcheck",
    "commits": 1,
    "lines": 275,
    "status": "ACTIVE — developer environment"
  },
  {
    "name": "the-amplified-method",
    "role": "Framework documentation — AI-native compound engineering methodology + React interface",
    "commits": 1,
    "languages": {"javascript": 4, "markdown": 2},
    "status": "ACTIVE — methodology reference"
  },
  {
    "name": "amplified-website",
    "role": "Next.js 15 public website — Covered AI / Amplified Partners marketing",
    "commits": 4,
    "lines": 1340,
    "languages": {"typescript": 3},
    "status": "ACTIVE"
  },
  {
    "name": "beautiful-and-golden",
    "role": "Read-only observability sidecar — Ghost Sidecar for legacy SMB infrastructure",
    "commits": 5,
    "lines": 759,
    "languages": {"python": 12},
    "status": "ACTIVE — sidecar prototype"
  },
  {
    "name": "visual-polish-systemdot",
    "role": "Visual Polish System — deterministic UI/UX scoring engine, Kaizen pipeline",
    "commits": 1,
    "lines": 1745,
    "languages": {"javascript": 12},
    "ci_workflows": 1,
    "status": "ACTIVE"
  },
  {
    "name": "originals",
    "role": "Archival repository — read-only preservation copies organized by source",
    "commits": 1,
    "status": "ACTIVE — archive"
  },
  {
    "name": "canonical-candidate",
    "role": "Curated substantive documents — pre-processed input for synthesis",
    "commits": 1,
    "status": "ACTIVE — curation pipeline"
  }
]
```

### 2.2 Stub Repositories (9)

```json
[
  {"name": "amplified-hermes-team", "note": "Placeholder for Devin snapshot build"},
  {"name": "beautifulgolden", "note": "Placeholder for Devin snapshot build"},
  {"name": "covered-ai-v2", "note": "Placeholder for Devin snapshot build"},
  {"name": "docs", "note": "Placeholder for Devin snapshot build"},
  {"name": "librarian-api", "note": "Placeholder for Devin snapshot build"},
  {"name": "openclaw", "note": "Placeholder for Devin snapshot build"},
  {"name": "smb-ai-friction-consultancy", "note": "Placeholder for Devin snapshot build"},
  {"name": "visual-polish-system", "note": "Placeholder for Devin snapshot build"},
  {"name": "voice-ai", "note": "Placeholder for Devin snapshot build"}
]
```

---

## 3. API Endpoints Register

```json
{
  "crm": {
    "total": 142,
    "route_files": [
      {"file": "app/api/routes/contacts.py", "endpoints": 10},
      {"file": "app/api/routes/interview.py", "endpoints": 18},
      {"file": "app/api/routes/orchestrator.py", "endpoints": 12},
      {"file": "app/api/routes/retell_integration.py", "endpoints": 11},
      {"file": "app/api/routes/business_brain.py", "endpoints": 9},
      {"file": "app/api/routes/stripe_routes.py", "endpoints": 9},
      {"file": "app/api/routes/calendar_routes.py", "endpoints": 7},
      {"file": "app/api/routes/intelligence_routes.py", "endpoints": 7},
      {"file": "app/api/routes/xero_routes.py", "endpoints": 7},
      {"file": "app/api/routes/quickbooks_routes.py", "endpoints": 6},
      {"file": "app/api/routes/marketing_live.py", "endpoints": 6},
      {"file": "app/api/routes/deals.py", "endpoints": 6},
      {"file": "app/api/routes/intelligence.py", "endpoints": 5},
      {"file": "app/api/routes/knowledge.py", "endpoints": 5},
      {"file": "app/api/routes/companies.py", "endpoints": 5},
      {"file": "app/api/routes/activities.py", "endpoints": 5},
      {"file": "app/api/routes/telegram_bridge.py", "endpoints": 4},
      {"file": "app/api/routes/voice_bridge.py", "endpoints": 3},
      {"file": "app/content/router.py", "endpoints": 7},
      {"file": "app/content/waitlist.py", "endpoints": 2}
    ]
  },
  "amplified_machine": {
    "total": 47,
    "route_files": [
      {"file": "services/finance-engine/core/main.py", "endpoints": 15},
      {"file": "services/ch-pipeline/core/main.py", "endpoints": 6},
      {"file": "core/api/webhooks.py", "endpoints": 4},
      {"file": "core/api/tenants.py", "endpoints": 4},
      {"file": "core/api/four_words.py", "endpoints": 4},
      {"file": "core/main.py", "endpoints": 4},
      {"file": "core/api/content.py", "endpoints": 4},
      {"file": "core/api/waitlist.py", "endpoints": 3},
      {"file": "core/api/dashboard.py", "endpoints": 2},
      {"file": "core/api/brain.py", "endpoints": 1}
    ]
  },
  "byker_production": {
    "total": 47,
    "route_files": [
      {"file": "main.py", "endpoints": 16},
      {"file": "orchestrator_api.py", "endpoints": 14},
      {"file": "cover_ai/api/cover_api.py", "endpoints": 11},
      {"file": "workflows/workflow_engine.py", "endpoints": 6}
    ]
  },
  "marketing_engine": {
    "total": 19,
    "route_files": [
      {"file": "api.py", "endpoints": 19}
    ]
  },
  "enforcer": {
    "total": 3,
    "route_files": [
      {"file": "enforcer.py", "endpoints": 3}
    ]
  }
}
```

---

## 4. MCP Servers

```json
{
  "total": 14,
  "servers": [
    {"name": "amplified-knowledge-mcp", "repo": "amplified-knowledge-mcp", "tools": "graph + vector search", "tier": "readonly/readwrite/admin"},
    {"name": "beast-control-mcp", "repo": "clean-build/02_build/beast-control-mcp", "tools": "Beast infrastructure control"},
    {"name": "crm-server", "repo": "crm/mcp_servers/crm_server.py", "tools": "17 CRM tools"},
    {"name": "pii-gateway", "repo": "crm/mcp_servers/pii_gateway.py", "tools": "4 PII tools"},
    {"name": "gemini-server", "repo": "crm/mcp_servers/gemini_server.py", "tools": "Gemini model access"},
    {"name": "grok-server", "repo": "crm/mcp_servers/grok_server.py", "tools": "Grok model access"},
    {"name": "kimi-server", "repo": "crm/mcp_servers/kimi_server.py", "tools": "Kimi model access"},
    {"name": "email-mcp", "repo": "clean-build/02_build/cove-orchestrator/mcp-servers/email-mcp", "tools": "email operations"},
    {"name": "postgresql-mcp", "repo": "clean-build/02_build/cove-orchestrator/mcp-servers/postgresql-mcp", "tools": "database operations"},
    {"name": "litellm-mcp", "repo": "clean-build/02_build/cove-orchestrator/mcp-servers/litellm-mcp", "tools": "model routing"},
    {"name": "github-mcp", "repo": "clean-build/02_build/cove-orchestrator/mcp-servers/github-mcp", "tools": "GitHub operations"},
    {"name": "filesystem-mcp", "repo": "clean-build/02_build/cove-orchestrator/mcp-servers/filesystem-mcp", "tools": "file operations"},
    {"name": "langfuse-mcp", "repo": "clean-build/02_build/cove-orchestrator/mcp-servers/langfuse-mcp", "tools": "LLM observability"},
    {"name": "telegram-mcp", "repo": "clean-build/02_build/cove-orchestrator/mcp-servers/telegram-mcp", "tools": "Telegram integration"}
  ]
}
```

---

## 5. Database & Migration Status

```json
{
  "canonical_data_architecture": {
    "engine": "PostgreSQL",
    "graph_extension": "Apache AGE (openCypher)",
    "vector_extension": "pgvector (HNSW indexing)",
    "status": "AUTHORITATIVE — single-engine architecture"
  },
  "deprecated": [
    {"name": "FalkorDB", "replacement": "PostgreSQL + Apache AGE", "migration_status": "PLANNED — 9,000 nodes across 4 graphs"},
    {"name": "Qdrant", "replacement": "PostgreSQL + pgvector (HNSW)", "migration_status": "PLANNED — 57,434 embeddings (384-dim)"}
  ],
  "crm_migrations": {
    "total": 14,
    "files": [
      "001_add_orchestrator_tables.py",
      "002_add_quality_control.py",
      "003_add_self_improvement.py",
      "004_add_voice_crm.py",
      "005_add_intelligence_system.py",
      "006_add_interview_tables.py",
      "007_add_call_transcripts.py",
      "007_add_content_engine.py",
      "009_merge_heads.py",
      "010_add_waitlist.py",
      "011_add_prospects.py",
      "012_add_crm_tables.py",
      "add_marketing_content_table.py"
    ],
    "note": "Dual 007 — numbering collision between call_transcripts and content_engine"
  },
  "beast_databases": {
    "postgresql": "Running — accepting connections",
    "redis": "Running — PONG response",
    "clickhouse": "Present in beast-code-export",
    "minio": "Present — object storage"
  }
}
```

---

## 6. Infrastructure — Beast (Hetzner AX162-R)

```json
{
  "ip": "135.181.161.131",
  "hardware": {
    "cores": 96,
    "ram_gb": 252,
    "storage_tb": 1.8,
    "free_storage_tb": 1.3,
    "gpu": false
  },
  "containers": {
    "total": 42,
    "healthy": 40,
    "unhealthy": [
      {"name": "amplified-crm-dev", "status": "Exited(3)", "issue": "Postgres auth failure", "ticket": "AMP-141"},
      {"name": "tailscale", "status": "Created (stuck since 2026-05-02)", "ticket": "AMP-136"}
    ],
    "degraded": [
      {"name": "cove-temporal", "status": "Up but gRPC probe fails", "ticket": "AMP-139"},
      {"name": "traefik", "status": "Up but dashboard unreachable", "ticket": "AMP-140"}
    ]
  },
  "key_services": [
    "LiteLLM (model router with fallback chains)",
    "Ollama (Llama 3.1 8B/70B, Qwen3 Coder 30B)",
    "Temporal (durable workflows)",
    "Cove Pipeline (4 worker teams)",
    "Sovereign Fleet (3 entities: Alpha/GPT-4.1-mini, Kimmy/Kimi-K2.6, Charlie/DeepSeek-V4-Flash)",
    "Marketing Engine",
    "PostgreSQL", "Redis", "ClickHouse", "MinIO",
    "Langfuse (LLM observability)", "Traefik (routing)", "Portainer (Docker UI)"
  ],
  "llm_provider_status": {
    "openai": "DEGRADED — 401",
    "anthropic": "DEGRADED — billing exhausted",
    "moonshot": "DEGRADED — 401",
    "ticket": "AMP-142"
  }
}
```

---

## 7. CI/CD Workflows

```json
{
  "total_workflows": 19,
  "by_repo": {
    "clean-build": ["auto-review-merge.yml", "cove-orchestrator-tests.yml", "linear-sync.yml", "pr-validation.yml", "process-health-weekly.yml"],
    "crm": ["dependabot-auto-merge.yml", "linear-sync.yml", "pr-validation.yml", "visual-polish.yml"],
    "ground-truth": ["auto-review-merge.yml", "linear-sync.yml", "pr-validation.yml"],
    "amplified-machine": ["auto-review-merge.yml"],
    "amplified-site": ["visual-polish.yml"],
    "awesome-openclaw-agents": ["plan-execution-mirror.yml"],
    "byker-production": ["validate.yml"],
    "devon-memory": ["auto-review-merge.yml"],
    "marketing-engine": ["auto-review-merge.yml"],
    "mission-control": ["auto-review-merge.yml"],
    "perplexity-research": ["auto-review-merge.yml"],
    "portable-spine": ["auto-review-merge.yml"],
    "visual-polish-systemdot": ["visual-polish.yml"]
  },
  "common_patterns": [
    "auto-review-merge (DeepSeek-driven Five Rods review)",
    "pr-validation (governance checks)",
    "linear-sync (Linear ticket linking)",
    "visual-polish (UI/UX scoring gate)"
  ]
}
```

---

## 8. Governance Architecture

```json
{
  "authority_files": {
    "location": "clean-build/00_authority/",
    "count": 21,
    "files": [
      "MANIFEST.md (authority index — only source of authority)",
      "NORTH_STAR.md",
      "PROJECT_INTENT.md",
      "AGENTS.md",
      "AGENT_ROUTING.md",
      "BRAIN_ARCHITECTURE.md",
      "BUILD_LOOP.md",
      "DECISION_LOG.md",
      "EIGHT_LAWS.md",
      "OPINION_CONFIDENCE.md",
      "PARTNER_TRANSFER_INSTRUCTIONS.md",
      "PORTABLE-SPINE.md",
      "PROMOTION_GATE.md",
      "PR_WORKFLOW.md",
      "SIGNATURES.md",
      "SKILL_EXECUTION.md",
      "SKILL_PLANNING.md",
      "TAXONOMY.md",
      "USE_IT_OR_CUT_IT.md",
      "REMIT_PARTNER_CURSOR.md",
      "README.md"
    ]
  },
  "truth_documents": {
    "location": "clean-build/01_truth/",
    "schemas": 31,
    "processes": 57,
    "research_validations": "present"
  },
  "shadow_workspace": {
    "location": "clean-build/03_shadow/",
    "job_wrapups": "present",
    "notes": "present",
    "research": "present",
    "sessions": "present",
    "specifications": "present"
  },
  "archive": {
    "location": "clean-build/90_archive/",
    "contains": ["authority-history", "authority-snapshots", "beautiful-and-golden", "context", "legacy-writers", "specifications", "truth-history", "vault-monitor-runs"]
  },
  "five_rods": ["Radical Honesty", "Radical Transparency", "Radical Attribution", "Win-Win", "Idea Meritocracy"],
  "ulysses_clause": "If Ewan weakens the Five Rods, the system flags it, resists it, and if necessary removes his override capability"
}
```

---

## 9. Agent Fleet

```json
{
  "agents": [
    {"name": "Devon (Devin)", "platform": "Devin sessions", "role": "Infrastructure operator, Linear governor", "beast_access": "Read + Write"},
    {"name": "Clawd (OpenClaw)", "platform": "OpenClaw", "role": "Active doer", "beast_access": "Read only"},
    {"name": "Cassian (Claude)", "platform": "claude.ai", "role": "Observer, advisor", "beast_access": "Read only"},
    {"name": "Antigravity", "platform": "Local Mac", "role": "COO/Arbiter", "beast_access": "Read + Write"},
    {"name": "Cursor", "platform": "Cursor IDE", "role": "Code tasks", "beast_access": "N/A"},
    {"name": "Copilot", "platform": "GitHub", "role": "Code suggestions", "beast_access": "N/A"},
    {"name": "Plumb (Claude Code)", "platform": "Mac M4 Desktop", "role": "Truth-checking, drift detection", "beast_access": "Read only"}
  ],
  "sovereign_fleet_on_beast": [
    {"entity": "Alpha", "model": "GPT-4.1-mini"},
    {"entity": "Kimmy", "model": "Kimi-K2.6"},
    {"entity": "Charlie", "model": "DeepSeek-V4-Flash"}
  ]
}
```

---

## 10. PUDDING System — Mathematical Discovery Engine

```json
{
  "pudding_core": {
    "four_russian_stack": {
      "kolmogorov": "High-speed structural filtering — 4-slot Jaccard similarity",
      "kantorovich": "Reranking — Wasserstein-1 distance (Optimal Transport)",
      "markov": "Graph-traversal via probabilistic transition matrices",
      "pontryagin": "Dynamic context pruning — marginal relevance vs. cost"
    },
    "python_lines": 4260,
    "tests": 5
  },
  "pudding_testing": {
    "validation_suite": ["coverage", "consistency", "permutation", "pairwise", "abc_discovery"],
    "python_lines": 2826
  },
  "taxonomy": {
    "dimensions": 5,
    "labels": "WHAT.HOW.SCALE.TIME.PATTERN",
    "possible_labels": 2058,
    "format": "7×7×7×6 = 2,058 possible label combinations"
  },
  "scoring": {
    "simple": "Recipe Score = (Shared Dimensions × 2) + Unique_A + Unique_B",
    "advanced": "Score = (Domain Distance × Pattern Alignment) + Gap Complement + Tension Bonus",
    "emergence": "(Bridge × Distance × Novelty) / Redundancy"
  }
}
```

---

## 11. Critical Path Items

```json
{
  "blocked_on_ewan": [
    {"ticket": "AMP-142", "issue": "LLM provider keys / billing top-up (OpenAI, Anthropic, Moonshot)"},
    {"ticket": "AMP-143", "issue": "Confirm rotation/kill of orphan LiteLLM virtual key ($941 burn)"},
    {"ticket": "AMP-141", "issue": "Postgres password for amplified user"}
  ],
  "infrastructure_critical": [
    {"item": "FalkorDB → Apache AGE migration", "scope": "9,000 nodes across 4 graphs", "status": "PLANNED"},
    {"item": "Qdrant → pgvector migration", "scope": "57,434 embeddings (384-dim)", "status": "PLANNED"},
    {"item": "CRM deployment to Beast", "status": "NOT STARTED — code ready, Docker compose needed"},
    {"item": "Temporal gRPC repair", "ticket": "AMP-139"},
    {"item": "Traefik dashboard repair", "ticket": "AMP-140"}
  ],
  "stub_cleanup": {
    "repos_to_delete": 9,
    "blocked_by": "Stale entries in Devin snapshot build settings"
  }
}
```

---

## 12. Commit Velocity (Top 5)

```json
[
  {"repo": "clean-build", "commits": 229, "role": "Operating environment"},
  {"repo": "vault", "commits": 222, "role": "Knowledge corpus"},
  {"repo": "crm", "commits": 164, "role": "Product CRM"},
  {"repo": "amplified-site", "commits": 59, "role": "Public website"},
  {"repo": "byker-production", "commits": 10, "role": "SMB orchestrator"}
]
```

---

*Devon — session devin-bba3748d3fa545c2b32990d630b17e9a — 2026-05-16*

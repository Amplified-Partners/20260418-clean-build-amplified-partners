# Code Extraction Catalogue

**Generated:** 2026-04-27 03:46 UTC
**Signed-by:** Devon (Devin) | Session `7cd95caf339c46a2896fbf6ffbda02be`
**Scope:** All code files in `corpus-raw/vault/` and `clean-build/02_build/`
**Method:** Read every code file. Assessed function, completeness, and whether it's the best version. Separated signal from noise.
**Note:** All `corpus-raw/vault/` paths are `[SOURCE REQUIRED]` — verify against the `corpus-raw` repo (`devon/initial-corpus-dump` branch). Clean-build paths verified in-repo.

---

## Summary

| Layer | Location | Code files | Worth keeping | Shite |
|-------|----------|-----------|--------------|-------|
| Vault _inbox | `corpus-raw/vault/_inbox/` | 93 Python | 32 unique modules | 61 (versions, empties, tests) |
| Vault scripts | `corpus-raw/vault/scripts/` | 7 files | 5 | 2 (bake.py superseded by bake_fixed.py) |
| Clean-build | `clean-build/02_build/` | ~90 files | ~88 (already organised) | 2 (test files) |

**Total useful code extracted:** ~127 files across 12 functional systems.

---

## A. NightScout — Intelligence Pipeline

**Location:** `clean-build/02_build/cove-orchestrator/nightscout/`
**Status:** Complete module. 7 files, ~895 lines. Has its own DB schema, MCP server, and SQL migrations.
**What it does:** Nightly scrape → LLM score → fork → morning briefing. Fetches 25+ sources (RSS + SearXNG), scores each item on four dimensions (relevance, impact, applicability, novelty) using Ollama via LiteLLM, forks by tier (noise / briefing / R&D pipeline / critical), stores in PostgreSQL, generates markdown morning briefings, sends Telegram alerts for critical items.

| File | Lines | Purpose |
|------|-------|---------|
| `config.py` | 138 | Source definitions (25+ RSS/SearXNG), env config, scoring tiers |
| `pipeline.py` | 248 | Master orchestrator: fetch → dedup → store → score → fork → notify |
| `fetchers.py` | 182 | RSS + SearXNG fetchers, date parsing, dedup key generation |
| `scorer.py` | 131 | LLM scoring prompt, batch scoring via LiteLLM → Ollama |
| `briefing.py` | 144 | Morning briefing markdown generator from scored items |
| `main.py` | 47 | CLI entry point (`run` or `briefing`) |
| `__init__.py` | 5 | Package docstring |

**MCP Server:** `cove-orchestrator/mcp-servers/nightscout-mcp/server.py` (181 lines) — exposes NightScout data to other agents.
**DB Schema:** `cove-orchestrator/db/migrations/002_nightscout_schema.sql` (139 lines) — ns_sources, ns_raw_items, ns_scored_items, ns_briefings, ns_pipeline_runs.
**Dependencies:** asyncpg, httpx, mcp SDK, Ollama (via LiteLLM).

---

## B. The Business Brain — Core Product

**Location:** `corpus-raw/vault/_inbox/`
**Status:** Three separate files that form the heart of the product. Not wired together in the vault, but the logic is all there.

| File (best version) | Lines | What it does |
|---------------------|-------|-------------|
| `brain.py` | 474 | Intelligence engine. Interview data + Qdrant knowledge + Claude → Business Bible. Includes `InterviewContext` data model, semantic search over Qdrant, `generate_business_bible()` multi-section Claude synthesis. |
| `engine.py` | 493 | Interview engine. "The interview IS the product." Founder + staff interview flows, Claude-driven question selection, insight extraction with confidence scores. Life first, then business. |
| `business_brain_service.py` | 598 | Week 1 Universal Onboarding orchestrator. Day 1: founder interview → initial brain. Days 2-3: staff interviews. Days 3-5: MCP server connections. Days 6-7: recommendations. |
| `claude_client.py` (v1, 303 lines) | 303 | Anthropic API client with prompt caching (cache_control: ephemeral). v2 is smaller (likely a stripped version). **Keep v1.** |

**Dependencies:** anthropic, qdrant_client, sentence_transformers, app.interview.* (internal module structure).

---

## C. Voice & Phone System

**Location:** `corpus-raw/vault/_inbox/`
**Status:** Two distinct approaches. Both substantial.

| File (best version) | Lines | What it does |
|---------------------|-------|-------------|
| `voice_bridge.py` | 490 | Full-stack phone system. Twilio Voice + Deepgram Nova-3 (STT, UK accents) + ElevenLabs Flash v2.5 (TTS, British voices) + Claude (conversation). Inbound + outbound modes. GDPR recording consent. WebSocket streaming. |
| `retell_integration.py` (v1, 683 lines — but v4 at 28KB is largest/latest) | 683 | Retell AI + Cartesia integration. 600ms latency voice agent for Jesmond Plumbing. Calendar check, appointment booking, emergency SMS, CRM logging. **Keep v4 (28KB) — most complete.** |
| `webhook_server_failsafe.py` (v1, 580 lines) | 580 | Three-layer failsafe: Layer 1 (Retell AI UK) → Layer 2 (backup AI US / recorded message) → Layer 3 (direct forward to owner's mobile). SMS alerting via Twilio. **v2 and v3 are ~identical (22.8KB each). Keep v1 (23KB) — slightly larger, the original.** |
| `webhook_server.py` (v2, 118 lines) | 118 | Simpler Telnyx webhook → Retell handoff. **Keep v2.** |
| `twilio_integration.py` | (imported by retell_integration) | Twilio SMS/voice wrapper. |

**Also in clean-build:**
| File | Lines | What it does |
|------|-------|-------------|
| `02_build/command-centre/backend/voice_agent.py` | 394 | Simpler TwiML Gather+Say+Claude Haiku approach. No WebSockets. Battle-tested. |

---

## D. Content Engine — Atomiser + Scheduler + Review Gate

**Location:** `corpus-raw/vault/_inbox/`
**Status:** Complete content pipeline in pieces. Pillar → atomise → schedule → approve → publish.

| File | Lines | What it does |
|------|-------|-------------|
| `atomiser.py` | 196 | Pillar content → 5 platform variants (LinkedIn, Twitter thread, Substack intro, Facebook, carousel outline). Ewan's voice baked into every platform prompt. 3:1 value ratio. |
| `scheduler.py` | 307 | APScheduler-based content queue. Platform-optimal UK timing (LinkedIn Tue/Wed 08:00, Twitter Wed 10:00, etc.). Nothing publishes without Telegram approval. |
| `telegram_gate.py` (v2, 287+ lines) | 287 | Content review via Telegram. Ewan approves/edits/rejects each variant via inline buttons. Long-polling, no public URL needed. **Keep v2.** |
| `substack.py` | 100 | Substack API integration for publishing. |
| `linkedin.py` | 112 | LinkedIn posting integration. |
| `twitter.py` | 118 | Twitter/X posting integration. |

---

## E. CRM & Prospect System

**Location:** `corpus-raw/vault/_inbox/`
**Status:** FastAPI route handlers for CRM. Designed for multi-tenant (one business per tenant).

| File | Lines | What it does |
|------|-------|-------------|
| `contacts.py` | 277 | Contact CRUD. Phone, email, address. Source tracking. |
| `companies.py` | 107 | Company CRUD. |
| `deals.py` | 140 | Deal/opportunity tracking. |
| `activities.py` | 119 | Activity logging (calls, emails, meetings). |
| `crm.py` | 137 | CRM aggregate queries. |
| `waitlist.py` | 375 | Waitlist management with interest scoring. |
| `prospect_research.py` | 750 | **Big one.** Companies House API + Google Places API + ICP scoring + Claude personalisation for outreach. Auto-researches prospects before contact. |
| `models_orm.py` | 140 | SQLAlchemy ORM models. |
| `enums.py` | 169 | Shared enums for the CRM. |

---

## F. Orchestration & Routing

**Location:** Split between vault/_inbox and clean-build.

| File (best version) | Lines | Location | What it does |
|---------------------|-------|----------|-------------|
| `task_router.py` | 426 | vault/_inbox | Smart message parsing. "Send invoice to Mrs Johnson £450" → invoice task. Claude intent + regex fallback. |
| `model_router.py` | 205 | vault/_inbox | Routes prompts to Haiku (cheap) or Sonnet (reasoning). Keyword + task type + token count heuristics. Goal: >70% to Haiku. |
| `router.py` (v2) | ~230 | vault/_inbox | FastAPI API router. **Keep v2.** |
| `main.py` (v5, largest) | ~100 | vault/_inbox | FastAPI app entry point. **Keep v5 (4KB) — most complete.** |

**In clean-build:**
| File | Lines | What it does |
|------|-------|-------------|
| `cove-orchestrator/agents/executive/runner.py` | 408 | AG2 Executive GroupChat. Believability-weighted speaker selection. The "sovereign core" brain. |
| `cove-orchestrator/agents/executive/team.py` | 282 | Executive team definitions (CFO, CTO, etc.) with topic expertise routing. |
| `cove-orchestrator/agents/configs/agent_registry.py` | 186 | Agent role definitions and model tier assignments. |
| `cove-orchestrator/temporal/workflows/build_workflow.py` | 204 | Temporal workflow for build tasks. |
| `cove-orchestrator/temporal/activities/agent_activities.py` | 283 | Temporal activities: clone, test, lint, deploy. |

---

## G. Email Agent

**Location:** `clean-build/02_build/cove-orchestrator/email_agent/`
**Status:** Complete module. 8 files, ~1,200 lines.

| File | Lines | What it does |
|------|-------|-------------|
| `pipeline.py` | 341 | Master pipeline: fetch → triage → draft → store → notify |
| `fetcher.py` | 255 | IMAP email fetcher (Gmail) |
| `triage.py` | 234 | LLM-based email triage (priority, action, category) |
| `drafter.py` | 150 | Draft response generation via Claude |
| `config.py` | 101 | Email account config, confidence thresholds |
| `status.py` | 88 | Status reporting |
| `main.py` | 47 | CLI entry point |
| `__init__.py` | 1 | Package init |

**Also in vault:** `gmail_automation.py` (130 lines) — simpler Gmail triage script using Google API directly. Predecessor to the email agent module.

---

## H. Safety & Monitoring

| File (best version) | Lines | Location | What it does |
|---------------------|-------|----------|-------------|
| `security_scanner.py` | 383 | vault/_inbox | Prompt injection detection via llm-guard (with regex fallback). Input + output scanning. |
| `prompt_sanitizer.py` | 64 | vault/_inbox | Wraps external input before it hits Claude. Central utility. |
| `cost_monitor.py` | 326 | vault/_inbox | LLM cost tracking: per-call, per-model, per-task. Langfuse dashboard + Telegram daily alerts. Includes cache pricing. |
| `sentinel.py` (v3 is latest, 141 lines; sentinel_v2-v2 is 307 lines — the biggest) | 141–307 | vault/_inbox | Codebase health monitoring. Three layers: basic health → detailed analysis → alert and halt. **Keep sentinel_v2-v2.py (307 lines) — most complete.** |
| `secrets.py` | 234 | vault/_inbox | Secret management. Loads from `~/.amplified/keys.env`. |

---

## I. Knowledge & Ingestion

| File (best version) | Lines | Location | What it does |
|---------------------|-------|----------|-------------|
| `semantic_cache.py` (v3) | 282 | vault/_inbox | Drop-in Anthropic wrapper with Qdrant semantic cache. 0.95 cosine threshold, 24h TTL. Target: 70-90% savings on interview engine. **Keep v3.** |
| `ingest_transcripts.py` (v3) | ~160 | vault/_inbox | Voice transcript ingestion to Qdrant. **Keep v3.** |
| `ingest_all_monologue.py` | 176 | vault/_inbox | Batch monologue transcript ingestion. |
| `run_all_puddings.py` (v2) | ~220 | vault/_inbox | Pudding analysis pipeline using Qdrant + fastembed. **Keep v2.** |
| `run_puddings.py` | (older version of above) | | **Discard.** |
| `pudding_labeler.py` | 354 | clean-build scripts | PUDDING 2026 taxonomy labeler: [WHAT].[HOW].[SCALE].[TIME].[PATTERN] |
| `porch_watcher.py` | 234 | clean-build scripts | Deterministic file ingestion: incoming/ → PUDDING label → Qdrant embed → labeled/ |

**Vault scripts:**
| File | Lines | What it does |
|------|-------|-------------|
| `vault-sync.py` | ~80 | Vault sync daemon — monitors source dirs, syncs to Obsidian vault. |
| `vault-to-qdrant.py` | ~80 | Vault → Qdrant ingestion pipeline. Monitors for new/changed markdown. |
| `vault-push-github.py` | ~50 | Auto-push vault commits to GitHub. |
| `classify-content.py` | ~60 | Claude-powered content classification. |
| `bake_fixed.py` | ~50 | Qdrant collection creator with sentence-transformers. **Keep bake_fixed.py, discard bake.py.** |
| `manual-vault-sync.sh` | ~30 | Interactive 5-minute manual sync. |
| `start-vault-sync.sh` | ~30 | Vault sync service start/stop. |

---

## J. MCP Servers

**Location:** `clean-build/02_build/cove-orchestrator/mcp-servers/`
**Status:** 8 MCP servers, all following the same FastMCP pattern.

| Server | Lines | What it does |
|--------|-------|-------------|
| `email-mcp/server.py` | 269 | Email agent tools for other agents |
| `filesystem-mcp/server.py` | 303 | File read/write/search tools |
| `github-mcp/server.py` | 311 | GitHub PR/issue/repo tools |
| `langfuse-mcp/server.py` | 294 | LLM cost and trace tools |
| `litellm-mcp/server.py` | 275 | LLM model routing tools |
| `nightscout-mcp/server.py` | 181 | Intelligence pipeline query tools |
| `postgresql-mcp/server.py` | 234 | Database query tools |
| `telegram-mcp/server.py` | 292 | Telegram messaging tools |
| `_template/server.py` | 195 | Template for new MCP servers |

---

## K. Command Centre

**Location:** `clean-build/02_build/command-centre/`
**Status:** React + Vite frontend with FastAPI backend.

**Backend:**
| File | Lines | What it does |
|------|-------|-------------|
| `main.py` | 469 | FastAPI server: proxies Beast voice, serves tasks/promises, Docker status |
| `voice_agent.py` | 394 | TwiML phone agent (Claude Haiku, no WebSockets) |
| `search_db.py` | 238 | SearXNG search with local result caching |
| `search_watcher.py` | 107 | Background search result watcher |

**Frontend (React/TypeScript):**
- `App.tsx`, `main.tsx`, `index.css`
- Components: AgentsPanel, NowPanel, PromisesCard, RnDPanel, SearchBar, SearchHistory, StreamPanel, WritingPanel
- API layer: beastApi, eventsApi, sessionsApi, tasksApi, types

---

## L. Database Migrations

**Location:** `clean-build/02_build/cove-orchestrator/db/migrations/`

| File | Lines | What it does |
|------|-------|-------------|
| `001_initial_schema.sql` | 212 | Foundation: projects, tasks, approvals, agent_runs, budget_daily, mcp_servers, model_configs |
| `002_nightscout_schema.sql` | 139 | NightScout: ns_sources, ns_raw_items, ns_scored_items, ns_briefings, ns_pipeline_runs |
| `003_email_agent_schema.sql` | — | Email agent tables |

---

## M. Integrations & Utilities (vault/_inbox, unique only)

| File | Lines | What it does | Keep? |
|------|-------|-------------|-------|
| `todoist-amplified-sync.py` | 177 | Todoist project sync for 3 Claude instances + Clawd + Ewan | Yes — coordination tool |
| `gmail_automation.py` | 130 | Gmail triage (Google API). Predecessor to email agent | Yes — simpler standalone version |
| `grok_server.py` (v4, 421 lines) | 421 | Grok MCP server | **Keep v4** |
| `gemini_server.py` (v1 or v3 — nearly identical ~480 lines) | 480 | Gemini MCP server | **Keep v3** |
| `kimi_server.py` (v2, 479 lines) | 479 | Kimi MCP server | **Keep v2** |
| `grok_agent.py` (v2, 141 lines) | 141 | Grok-powered X/Twitter agent | **Keep v2** |

---

## What to Discard

These are the version duplicates and genuine noise. 65 files:

**Version duplicates (keep latest only):**
- `*-v1.py` through `*-vN.py` where a later version exists (see "best version" notes above)
- `bake.py` (superseded by `bake_fixed.py`)

**Empty / boilerplate:**
- `__init__.py`, `__init__-v2.py`, `__init__-v3.py`, `__init__-v4.py` (empty or near-empty package inits)

**Test files (useful as reference, not production code):**
- `test_cognitive_diversity.py`, `test_cognitive_diversity_aggressive.py` + v2
- `test_gemini_server.py`, `test_grok_server.py` + v2, `test_kimi_server.py` + v2
- `test_call.py` (in command-centre)
- `test_integration.py` (in scripts)

**DB migration scripts (vault versions — superseded by clean-build migrations):**
- `006_add_interview_tables.py` through `012_add_crm_tables.py`
- `add_marketing_content_table.py`

---

## The Architecture That Emerges

When you lay all the code out, it's not 93 random files. It's a **complete AI operating system for small businesses** in six layers:

```
Layer 0: Safety       security_scanner, prompt_sanitizer, cost_monitor, sentinel
Layer 1: Intelligence NightScout (fetch → score → brief), semantic_cache
Layer 2: Knowledge    brain.py, engine.py, Qdrant, PUDDING taxonomy
Layer 3: Operations   email_agent, voice_bridge/retell, task_router, CRM
Layer 4: Content      atomiser, scheduler, telegram_gate, social integrations
Layer 5: Coordination command_centre, cove-orchestrator, AG2 executive team, Temporal, MCP servers
```

The vault/_inbox code is Layer 0-4. The clean-build code is Layer 1, 2, 3, and 5. They're the same product at different stages of organisation.

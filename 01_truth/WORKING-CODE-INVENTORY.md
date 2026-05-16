---
title: "Working Code Inventory — What's Running, What's Teed Up, What's Mentioned"
id: "working-code-inventory"
version: 1
created: 2026-05-15
last_validated: 2026-05-15
type: register
status: candidate
signed_by: "Devon, 2026-05-15, devin-7e8210cfe08f46b29042573424e899f0"
---

<!-- markdownlint-disable-file MD013 -->

# Working Code Inventory

**Purpose:** One document that answers three questions: What code is actually running? What's built and just needs wiring? What's been mentioned but nothing exists yet?

**Sources:** Cross-referenced from `02_build/INFRASTRUCTURE.md` (containers), `01_truth/SYSTEMS-AND-API-REGISTER.md` (APIs), `00_authority/BRAIN_ARCHITECTURE.md` (architecture), CRM repo code scans, knowledge notes, and `STATUS.md`. All internal — no external research.

**Last validated:** 2026-05-15 by Devon (session `devin-7e8210cfe08f46b29042573424e899f0`). Container statuses from `02_build/INFRASTRUCTURE.md` v2 (2026-05-03). Code scans from GitHub repos as of 2026-05-15.

---

## How to read this

- **Section 1 — Running:** Code deployed on Beast, containers up, serving requests. This is the live estate.
- **Section 2 — Teed Up:** Code written, tested (at least partially), sitting in GitHub. Needs deploying or wiring to go live. These are your easy wins.
- **Section 3 — Mentioned But Not Built:** Referenced in architecture docs, specs, or knowledge notes, but no implementation code exists. This is intent without execution.

Each entry has: **what it is**, **where it lives** (repo + file path or Beast path), **what it depends on**, and **current health** where known.

---

## 1. What's Running (Live on Beast)

Beast server: `135.181.161.131` — Hetzner AX162-R, 96 cores, 252 GB RAM, Ubuntu 24.04.

### 1.1 Core Platform

| Service | Container | Compose File | Port | What It Does | Health |
|---------|-----------|-------------|------|-------------|--------|
| **Traefik** | `traefik` | `/opt/amplified/traefik/docker-compose.yml` | 80, 443 | Reverse proxy + TLS. Routes `api.amplifiedpartners.ai` to backends. | Running (dashboard port 8080 unreachable — [AMP-140](https://linear.app/amplifiedpartners/issue/AMP-140)) |
| **PostgreSQL (primary)** | `postgres` | `/opt/amplified/docker-compose.yml` | 5432 (internal) | Primary DB. `amplified_machine` database. Used by core, finance, marketing, ch-pipeline. | Running, accepting connections |
| **PostgreSQL (secondary)** | `docker-postgres-1` | `/opt/amplified/agent-stack/cove-orchestrator/docker/docker-compose.yml` | 5432 (host) | Secondary instance for Temporal and other stacks. | Running |
| **Redis** | `redis` | `/opt/amplified/docker-compose.yml` | 6379 (internal) | Shared cache + message broker. | Running (PONG) |
| **MinIO** | `minio` | `/opt/amplified/docker-compose.yml` | 9000 (internal) | S3-compatible object storage. | Running |

### 1.2 AI / ML Services

| Service | Container | Compose File | Port | What It Does | Health |
|---------|-----------|-------------|------|-------------|--------|
| **Ollama** | `ollama` | `/opt/amplified/apps/ollama/docker-compose.yml` | 11434 (internal) | Local LLM inference. Hosts Llama 3.1 8B/70B, Qwen3 Coder 30B. | Running |
| **LiteLLM** | `litellm` | `/opt/amplified/apps/litellm/docker-compose.yml` | 4000 (internal) | Unified LLM proxy — routes local + remote models with failover chains. Does NOT classify by cost. | Running (auth-gated) |
| **Token Proxy** | `token-proxy` | `/opt/amplified/apps/cost-tools/docker-compose.yml` | 8088 (internal, `127.0.0.1:8088` host) | Anthropic reverse proxy. Sonnet→Haiku routing on extractive/classification prompts. Semantic cache (Qdrant `llm_cache`, 0.95 threshold, 24h TTL). $100/day budget circuit-breaker. | Running (healthy). **At risk:** Anthropic billing exhausted ([AMP-142](https://linear.app/amplifiedpartners/issue/AMP-142)). |
| **Langfuse** | `langfuse` | `/opt/amplified/apps/langfuse/docker-compose.yml` | — | LLM observability — traces, costs, prompt versioning. | Running |
| **SearXNG** | `searxng` | `/opt/amplified/apps/searxng/docker-compose.yml` | 8080 (internal) | Metasearch engine for research agents. | Running |

**Repo:** [`Amplified-Partners/anthropic-token-proxy`](https://github.com/Amplified-Partners/anthropic-token-proxy) — `token_proxy.py` (~988 lines). Haiku model: `claude-haiku-4-5-20251001`. Sonnet model: `claude-sonnet-4-20250514`.

### 1.3 Amplified Machine (Core Product API)

| Service | Container | Compose File | Route | What It Does | Health |
|---------|-----------|-------------|-------|-------------|--------|
| **Amplified Core API** | `amplified-core` | `/opt/amplified-machine/docker-compose.yml` | `api.amplifiedpartners.ai/` | Main API gateway. Vault ingestion, knowledge graph queries, orchestration. 2 GB mem limit. | Running (healthy) |
| **Amplified Worker** | `amplified-worker` | `/opt/amplified-machine/docker-compose.yml` | — | Background async tasks (indexing, embeddings, heavy processing). 4 GB mem limit. | Running |
| **Finance Engine** | `finance-engine` | `/opt/amplified-machine/docker-compose.yml` | `/api/v1/finance` | Financial analytics — CLV, cash flow, valuation scoring. Port 8700. | Running (healthy) |

**Repo:** [`Amplified-Partners/amplified-machine`](https://github.com/Amplified-Partners/amplified-machine)

### 1.4 Marketing Engine

| Service | Container | Compose File | Route | What It Does | Health |
|---------|-----------|-------------|-------|-------------|--------|
| **Marketing Engine** | `amplified-marketing-engine` | `/opt/amplified/apps/marketing/docker-compose.marketing.yml` | `/api/v1/marketing` | Content pipeline: research → generate → evaluate → queue → learn. Three-avatar synthetic evaluator (Bob, Lisa, Marcus). API auth: admin/pipeline/readonly tiers. v0.4.0. 19 endpoints. | Running |
| **Kaizen Optimizer** | `kaizen-kaizen` | `/opt/amplified/apps/kaizen/docker-compose.yml` | — | Continuous improvement loop. Analyses feedback → generates preferences → feeds back into content gen. | Running (healthy) |

**Repo:** [`Amplified-Partners/marketing-engine`](https://github.com/Amplified-Partners/marketing-engine)

### 1.5 Cove & Temporal (Workflow Orchestration)

| Service | Container | Compose File | Port | What It Does | Health |
|---------|-----------|-------------|------|-------------|--------|
| **Cove API** | `cove-api` | `/root/cove-repo/infrastructure/docker-compose.yml` | 8081 (host) | Cove API server. | Running (healthy) |
| **Cove Temporal** | `cove-temporal` | same | 7233 (localhost) | Temporal workflow engine. | Running |
| **Cove Temporal UI** | `cove-temporal-ui` | same | 8233 (localhost) | Temporal web dashboard. | Running |
| **Cove Postgres** | `cove-postgres` | same | 5433 (localhost) | Cove-specific TimescaleDB. | Running |
| **Cove Translator** | `cove-translator` | same | 8090 | Translation layer. | Running |
| **Cove Workers (×5)** | `cove-worker`, `-alpha`, `-bravo`, `-charlie`, `-delta` | same | — | Workflow execution fleet. | Running |
| **Secondary Temporal** | `docker-temporal-1` | `/opt/amplified/agent-stack/cove-orchestrator/docker/docker-compose.yml` | — | Secondary Temporal instance. | Running |

### 1.6 Agent Services

| Service | Container | Compose File | Port | What It Does | Health |
|---------|-----------|-------------|------|-------------|--------|
| **OpenClaw Agents** | `openclaw-agents` | `/opt/amplified/apps/openclaw-agents/docker-compose.yml` | 8100 | Agent platform — note-taking, recording, coordination. | Running (healthy) |
| **Enforcer** | `enforcer` | `/opt/amplified/apps/enforcer/docker-compose.yml` | 8000 | Codebase health monitor + automated build circuit breaker. | Running (healthy) |
| **Knowledge MCP** | `amplified-knowledge-mcp` | `/opt/amplified/apps/amplified-knowledge-mcp/docker-compose.yml` | — | MCP server for AI agents to query knowledge base. | Running (healthy) |

**Repo:** [`Amplified-Partners/amplified-knowledge-mcp`](https://github.com/Amplified-Partners/amplified-knowledge-mcp)

### 1.7 Voice Services

| Service | Container | Compose File | Route | What It Does | Health |
|---------|-----------|-------------|-------|-------------|--------|
| **Voice Agent** | `amplified-voice-agent` | `/opt/amplified-voice-agent/docker-compose.yml` | `voice.beast.amplifiedpartners.ai` | Twilio (+441917433558) + Deepgram STT + Anthropic conversation + FalkorDB knowledge. Port 8080. | Running. **Note:** Was using FalkorDB (now decommissioned, AMP-329). Needs rewiring to PostgreSQL + AGE. |
| **xAI Phone Agent** | `xai-phone-agent` | `/opt/xai-phone-agent/docker-compose.yml` | `phone.beast.amplifiedpartners.ai` | xAI/Grok voice experiment (voice: "Sal"). Native xAI voice API, no Twilio. | Running |

**Repos:** [`Amplified-Partners/voice-ai`](https://github.com/Amplified-Partners/voice-ai)

### 1.8 Knowledge & Search

| Service | Container | Compose File | Port | What It Does | Status |
|---------|-----------|-------------|------|-------------|--------|
| **FalkorDB** | ~~`falkordb-temp`~~ | `/opt/amplified/docker-compose.yml` | ~~6379~~ | Graph DB. Was 9,000 nodes, 4 graphs. | **Decommissioned** (AMP-329, 2026-05-13). Data migrated to PostgreSQL + Apache AGE: 53,959 entities, 34,488 relationships, 4,257 episodes. See `02_build/brain-migration/README.md`. |
| **Qdrant** | ~~`qdrant-temp`~~ | `/opt/amplified/docker-compose.yml` | ~~6333-6334~~ | Vector DB. Was 57,434 embeddings (384-dim). | **Decommissioned** (AMP-329, 2026-05-13). Data migrated to `knowledge_vectors` table in PostgreSQL + pgvector. See `02_build/brain-migration/README.md`. |
| **ClickHouse** | `clickhouse` | `/opt/amplified/docker-compose.yml` | 8123 (HTTP), 9000 (native) | Columnar analytics. | Running |

**Note:** `STATUS.md:59` and `02_build/security/2026-05-09_beast-hardening-phase2_v1.md:34-35` confirm FalkorDB and Qdrant were decommissioned under AMP-329 (2026-05-13). `02_build/INFRASTRUCTURE.md` v2 (2026-05-03) predates the decommission and needs updating.

### 1.9 Dashboards & Tools

| Service | Container | Compose File | Port | What It Does |
|---------|-----------|-------------|------|-------------|
| **Portainer** | `portainer` | standalone | 8000, 9000, 9443 | Docker management GUI. |
| **Code Server** | `amplified-code-server` | `/opt/amplified/docker-compose.yml` | 8443 | VS Code in browser. |
| **Nexus Dashboard** | `nexus-dashboard` | `/opt/nexus/dashboard/docker-compose.yml` | 8090 | Trading/analytics dashboard. |
| **Watchtower** | `watchtower` | `docker run` | — | Auto Docker image updates. |

### 1.10 Scheduled Jobs (crontab)

| Schedule | What | Compose/Script |
|----------|------|----------------|
| Daily 3am | Amplified Core backup | `/opt/amplified/backups/amplified-core-backup.sh` |
| Daily 3am | Vault rsync | `/mnt/vault-backup/vault/` |
| Monthly 1st 3am | Secret key rotation | `/opt/amplified/secrets/rotation/rotate-keys.sh` |
| Daily 4am | Marketing content pipeline | API call to marketing engine |
| Weekly Sun 5am | Internal Kaizen | Analyses Ewan's feedback patterns |
| Monthly 1st 5am | External Kaizen | Analyses engagement metrics |
| Weekly Mon 8am | Learning report email | Email to Ewan |

### 1.11 Paused / Stopped (data preserved)

| Service | Container | Status | Why | Restart |
|---------|-----------|--------|-----|---------|
| **CH Pipeline** | `ch-pipeline` | **Paused** | Ewan paused 2026-04-30. Not ready for production. Data preserved: 9,740 filings from 9,707 companies. Original intent: offer 3 months free to newly registered companies. | `cd /opt/amplified-machine && docker compose -f docker-compose.yml -f docker-compose.services.yml up -d ch-pipeline` |
| **Voice Pipeline** | `voice-pipeline` | **Stopped** | Exited 6 weeks ago. Deepgram + LiteLLM + Redis pipeline. | Needs investigation before restart. |

### 1.12 Devin Scheduled Sessions (Cloud — not on Beast)

`[SOURCE REQUIRED]` — Schedule below is from org-wide knowledge notes (`00_authority/AGENT_ROUTING.md:64` marks this as `[SOURCE REQUIRED]` for in-repo authority). Verify against live Devin schedule configuration.

| Time (UTC) | Purpose |
|-----------|---------|
| 7:00 | Beast health check — SSH, verify containers, report anomalies |
| 8:00 | Linear update — scan Linear, update statuses |
| 9:00 | Review and plan — plan day's work |
| 14:00 | Linear triage sweep — check for `!escalate`/`!urgent`, triage new issues |

### 1.13 Sovereign Fleet (on Beast via LiteLLM)

| Entity | Model | Status |
|--------|-------|--------|
| Entity Alpha | GPT-4.1-mini | Active |
| Kimmy | Kimi-K2.6 | Active |
| Entity Charlie | DeepSeek-V4-Flash | Active |

---

## 2. What's Teed Up (Built, Needs Deploying or Wiring)

These are your easy wins. Code exists, tests exist (at least partially), just needs Docker-compose on Beast or API keys wired.

### 2.1 The CRM — Entire Product

**This is the single biggest teed-up item.**

| Property | Value |
|----------|-------|
| **Repo** | [`Amplified-Partners/crm`](https://github.com/Amplified-Partners/crm) |
| **Stack** | Python/FastAPI backend, Next.js frontend, PostgreSQL |
| **Dockerfile** | `crm/Dockerfile` — 39 lines, production-ready (Python 3.14-slim, non-root user, uvicorn) |
| **Endpoints** | 50+ REST API across 18 route modules in `app/api/routes/` |
| **Status** | Code in GitHub. **NOT deployed to Beast.** Next milestone: Docker-compose on Beast. |
| **Architecture ref** | `00_authority/BRAIN_ARCHITECTURE.md` § 5 — "Code in GitHub. NOT yet deployed to Beast." |

**What's inside and ready:**

#### 2.1.1 Founder Interview (Core Product)

| Module | File | Lines | What It Does |
|--------|------|-------|-------------|
| Interview routes | `app/api/routes/interview.py` | — | 7-phase Founder Interview → Business Bible |
| Interview engine | `app/interview/` | multi-file | Life first, then business. Core product. |
| Claude client | `app/interview/claude_client.py` | ~50 | Haiku-powered interview conversations |

#### 2.1.2 Intelligence Engine (11 features)

All in `app/intelligence/` — Python Logic Canon pattern (published formulas, deterministic, auditable).

| Feature | File(s) | Class | Tests |
|---------|---------|-------|-------|
| **Cash Flow Predictor** | `core/analytics_engine.py:315` | `compute_cash_flow_forecast()` | `tests/intelligence/test_analytics_engine.py` |
| **Death Spiral Detector** | `death_spiral_detector.py:200` | `DeathSpiralDetector` | Yes |
| **CLV Tracker** | `core/` | via analytics engine | `tests/intelligence/test_clv_tracker.py` |
| **Bottleneck Finder** | `bottleneck_finder.py:101` | `BottleneckFinder` | Yes |
| **Voice Quote Generator** | `features/voice_quote_generator.py:48` | `VoiceQuoteGenerator` | Yes |
| **Quote Follow-Up** | `features/` | via intelligence engine | `tests/intelligence/test_quote_followup.py` |
| **Payment Chaser** | `features/` | via intelligence engine | `tests/intelligence/test_payment_chaser.py` |
| **Service Reminder** | `features/service_reminder.py` (398 lines) | Full feature class | `tests/intelligence/test_service_reminder.py` |
| **Industry Benchmarks** | `core/industry_benchmarks.py:358` | Comparison engine | `tests/intelligence/test_industry_benchmarks.py` |
| **Insight Generator** | `core/insight_generator.py:37` | `InsightGenerator` | Yes |
| **Performance Monitor** | `core/performance_monitor.py:252` | `BaselineTracker` | Yes |

**Note:** Exit Strategy, Parts Concierge, and Portfolio Generator are **mentioned in BRAIN_ARCHITECTURE.md** as intelligence features but have thin or no implementation code — see Section 3.

#### 2.1.3 Integrations (built, need API keys and/or wiring)

| Integration | Files | What It Does | What's Needed |
|-------------|-------|-------------|---------------|
| **Xero** | `app/api/routes/xero_routes.py` | Accounting integration | API keys, OAuth flow |
| **QuickBooks** | `app/api/routes/quickbooks_routes.py` | Accounting integration | API keys, OAuth flow |
| **Stripe** | `app/api/routes/stripe_routes.py`, `backend/app/api/routes/stripe_routes.py` | Payment processing, webhooks | API keys, webhook URL config |
| **Calendar** | `app/api/routes/calendar_routes.py` | Scheduling | Calendar API config |
| **Retell AI Voice** | `app/api/routes/retell_integration.py` (819 lines, 11 endpoints) | Full voice agent — calendar check, appointment booking, emergency SMS, CRM logging | Retell API key, Twilio wiring |
| **Telegram Bridge** | `app/api/routes/telegram_bridge.py` (426 lines, 4 endpoints) | Task routing, interview-complete notifications, status polling | Telegram bot token |
| **Voice Bridge** | `app/api/routes/voice_bridge.py` (490 lines, 3 endpoints) | Twilio + Deepgram Nova-3 STT + ElevenLabs TTS + Claude. GDPR recording consent. | API keys for all providers |

#### 2.1.4 WhatsApp Bot (built, needs Evolution API connection)

| Component | Location | What It Does |
|-----------|----------|-------------|
| Claude bot | `scripts/whatsapp_claude_bot.py` | WhatsApp conversational AI |
| Setup script | `scripts/setup_whatsapp_complete.sh` | Automated setup |
| DB schema | `scripts/create_whatsapp_table.sql` | WhatsApp message storage |
| Twilio config | `scripts/configure_twilio_whatsapp.py` | WhatsApp via Twilio |
| Frontend client | `frontend/lib/whatsapp/client.ts` | WhatsApp API client |
| Business handler | `frontend/lib/whatsapp/business-handler.ts` | Business logic layer |
| Demo handler | `frontend/lib/whatsapp/demo-handler.ts` | Demo mode |
| Session store | `frontend/lib/whatsapp/session-store.ts` | Session management |
| Webhook route | `frontend/app/api/whatsapp/webhook/route.ts` | Incoming message handler |

#### 2.1.5 MCP Servers (CRM-side)

| Server | File | Tools | What It Does |
|--------|------|-------|-------------|
| **PII Gateway** | `mcp_servers/pii_gateway.py` | 4 | PII tokenization/detokenization for GDPR |
| **CRM Server** | `mcp_servers/crm_server.py` | 17 | Full CRM data access for agents |
| **Gemini Server** | `mcp_servers/test_gemini_server.py` | — | Multimodal experiment |

#### 2.1.6 Model Router (CRM-side)

| Component | File | What It Does |
|-----------|------|-------------|
| Model router | `app/core/model_router.py` | Routes calls: classification/extraction → Haiku, analysis/reasoning → Sonnet. Goal: >70% volume to Haiku. |
| Cost monitor | `app/core/cost_monitor.py` | Per-model cost tracking via span tracking |

#### 2.1.7 Marketing Machine (CRM-side)

| Component | Location | What It Does |
|-----------|----------|-------------|
| Content generator | `app/marketing_machine/content/generator.py` | Generates marketing content |
| Service business agents | `app/marketing_machine/agents/service_businesses.py` | Business-specific marketing automation |
| Orchestrator routes | `app/api/routes/orchestrator.py` | Pipeline orchestration |

#### 2.1.8 Frontend (Next.js)

| Component | Location | What It Does |
|-----------|----------|-------------|
| Pain Point Demos | `frontend/app/demo/pain-points/` | Interactive business pain point demos |
| Trade Landing Page | `frontend/components/landing/TradeLandingPageClient.tsx` | Customer-facing landing |
| Demo system | `frontend/app/demo/` | Full demo flow |

**Deployment status:** CRM Docker image `amplified-crm:dev` (9.95GB) was previously built on Beast. Containers `amplified-crm` (port 8001) and `amplified-crm-dev` (port 8003) exist on Beast but are **blocked** — CRM codebase has import issues (missing `twilio_integration.py` module, eager imports). Ports were bound to `127.0.0.1` during Beast hardening (2026-05-09). **Next step:** fix CRM codebase import issues, then restart containers. Source: `agent-comms/beast-ops/handoff-kimmy-2026-05-05.md`, `02_build/security/2026-05-09_beast-hardening-phase2_v1.md`.

### 2.2 Covered AI v2 (Standalone Product)

| Property | Value |
|----------|-------|
| **Repo** | [`Amplified-Partners/covered-ai-v2`](https://github.com/Amplified-Partners/covered-ai-v2) |
| **Stack** | TypeScript, Vapi.ai, Twilio, Railway |
| **What** | AI phone answering for UK service businesses |
| **Status** | Active — separate product, own deployment (Railway) |

### 2.3 NightScout Intelligence Pipeline

| Property | Value |
|----------|-------|
| **Location** | `clean-build/02_build/cove-orchestrator/nightscout/` |
| **Files** | 7 files, ~895 lines |
| **What** | RSS + SearXNG fetchers (27 sources defined), 4-dimension Ollama scorer, tiered routing, Postgres storage, Telegram briefing |
| **MCP server** | `cove-orchestrator/mcp-servers/nightscout-mcp/server.py` (181 lines) |
| **DB schema** | `cove-orchestrator/db/migrations/002_nightscout_schema.sql` (139 lines) — `ns_sources`, `ns_raw_items`, `ns_scored_items`, `ns_briefings`, `ns_pipeline_runs` |
| **Dependencies** | asyncpg, httpx, MCP SDK, Ollama (via LiteLLM) |
| **Status** | Code complete. Needs deploying as a Cove workflow on Beast. |

### 2.4 CH Pipeline (Paused — Data Preserved)

| Property | Value |
|----------|-------|
| **Container** | `ch-pipeline` on Beast |
| **Status** | Paused by Ewan (2026-04-30). Data preserved: 9,740 filings, 9,707 companies. |
| **Original intent** | Monitor Companies House API for newly registered UK companies → offer 3 months free as go-to-market channel. |
| **To resume** | `cd /opt/amplified-machine && docker compose -f docker-compose.yml -f docker-compose.services.yml up -d ch-pipeline` |
| **Needs** | Ewan's decision on production readiness. |

### 2.5 PUDDING Labelling (Code exists, 0 pipeline runs)

| Property | Value |
|----------|-------|
| **Location** | `clean-build/02_build/beast/apds-labeller/apds_labeller_v3_amp173.py` |
| **What** | Extracts PUDDING labels (WHAT.HOW.SCALE.TIME taxonomy, 2,058 possible labels) from text using Claude Haiku via Anthropic Messages API. |
| **API key** | Dedicated `pudlabelhaiku` key exists. |
| **Dependencies** | Anthropic API (currently exhausted — [AMP-142](https://linear.app/amplifiedpartners/issue/AMP-142)) |
| **Status** | Code exists. Zero pipeline runs recorded. Needs Anthropic billing restored + scheduled trigger. |

### 2.6 Epistemic Status Engine

| Property | Value |
|----------|-------|
| **Location** | `clean-build/02_build/routing/epistemic_status.py` (~540 lines) |
| **What** | Layer 0 reference implementation — the Python definitions ARE the operating rules. Four tiers (INTUITED → STRUCTURED → MEASURED → PROVEN), min-rule enforcement, staleness decay, boundary checks. |
| **Status** | Code complete, stdlib-only, auditable. Used as reference but not yet wired into any runtime pipeline. |

### 2.7 Harvest-to-Label Adapter

| Property | Value |
|----------|-------|
| **Location** | `clean-build/02_build/routing/harvest_to_label.py` |
| **What** | Normalises NightScout `RawItem` objects and Porch Watcher file drops into `HarvestRecord` format for PUDDING labelling. Streaming + batch modes. |
| **Status** | Code complete. Ready to wire between NightScout pipeline and PUDDING labeller. |

### 2.8 Sentinel v2

| Property | Value |
|----------|-------|
| **Location** | `crm/scripts/sentinel_v2.py` (~300 lines) |
| **What** | System monitoring and alerting — WhatsApp notifications. |
| **Status** | Code exists, needs deploying. |

### 2.9 Websites

| Site | Repo | Stack | Status |
|------|------|-------|--------|
| `amplifiedpartners.ai` | [`amplified-site`](https://github.com/Amplified-Partners/amplified-site) | TypeScript | Active |
| Marketing/acquisition site | [`amplified-website`](https://github.com/Amplified-Partners/amplified-website) | TypeScript | Active |

### 2.10 Other Teed-Up Repos

| Repo | Purpose | Status |
|------|---------|--------|
| [`mission-control`](https://github.com/Amplified-Partners/mission-control) | Enterprise governance dashboard — code review, decision tracking | Active, not deployed on Beast |
| [`amplified-hermes-team`](https://github.com/Amplified-Partners/amplified-hermes-team) | Agent orchestration framework — team manager, BATON protocol | Active |
| [`pudding-core`](https://github.com/Amplified-Partners/pudding-core) | Core PUDDING technique implementation (Swanson ABC model) | Active |

---

## 3. Mentioned But Not Built (Intent Without Code)

These appear in architecture docs, specs, or knowledge notes but have no implementation code found in any scanned repo.

### 3.1 Vellum — Correspondence Mode

| Property | Value |
|----------|-------|
| **Source** | `00_authority/BRAIN_ARCHITECTURE.md:598` — "Correspondence mode: Not yet built" |
| **Context** | Vellum has Brief mode (running) and Council mode (running). Correspondence is the third mode — inter-agent async communication. |
| **Blocking?** | No — Brief and Council are operational. |

### 3.2 DeepSeek Second-Machine Verification

| Property | Value |
|----------|-------|
| **Source** | `00_authority/BRAIN_ARCHITECTURE.md:726` — "Layer 4: Second-machine verification (different model, checks maths)" |
| **Knowledge note** | `note-2fe79a8d01d74305b195ccdb631aca81` — "Could be small model on Beast or API call (just maths, cheap)" |
| **Context** | The Python Logic Canon (Layer 2) exists. DeepSeek as navigator (Layer 3) is architecturally defined. Layer 4 (a second, different model that independently verifies the maths) has no code. |
| **Infrastructure needed** | Separate Hetzner box for DeepSeek (64GB+ RAM, 16+ cores). Not yet provisioned. |

### 3.3 Client-Side PII Tokenisation (Shamir's Secret Sharing)

| Property | Value |
|----------|-------|
| **Source** | `00_authority/BRAIN_ARCHITECTURE.md` § 13 — "PII-tokenized on the client's own hardware before it moves anywhere" + "Shamir's Secret Sharing" |
| **CRM code** | `mcp_servers/pii_gateway.py` exists (server-side tokenisation using Microsoft Presidio). No client-side tokenisation implementation found. No Shamir implementation found. |
| **Context** | The full privacy architecture (P1: client machine, P2: client container, P3: anonymised data leaving client infra) is documented but only P2-level Presidio exists in code. |

### 3.4 Ingestion Pipe — New Three-Stage Shape

| Property | Value |
|----------|-------|
| **Source** | `00_authority/BRAIN_ARCHITECTURE.md` § 6 — "deduplicate → classify → TIER → TIMESTAMP → ATTRIBUTE → route → ingest" |
| **Current state** | Old shape ("deduplicate → refine → ingest") is the running version. The three new non-negotiable stages (epistemic tier tagging, provenance, expiry) are specified but not implemented as a running pipeline. |
| **Partial code** | `02_build/routing/epistemic_status.py` (tier engine) and `02_build/routing/harvest_to_label.py` (classification adapter) exist as components but are not wired into a running pipeline. |

### 3.5 ~~FalkorDB → Apache AGE Migration~~ DONE

**Correction:** Migration was completed and FalkorDB decommissioned (AMP-329, 2026-05-13). 53,959 entities, 34,488 relationships, 4,257 episodes migrated. Scripts archived to `90_archive/legacy-writers/`. See `02_build/brain-migration/README.md`. Updated in Section 1.8.

### 3.6 ~~Qdrant → pgvector Migration~~ DONE

**Correction:** Migration was completed and Qdrant decommissioned (AMP-329, 2026-05-13). 57,434 vectors migrated to `knowledge_vectors` table. Scripts archived to `90_archive/legacy-writers/`. See `02_build/brain-migration/README.md`. Updated in Section 1.8.

**Remaining:** Token-proxy semantic cache (`llm_cache` collection) — status unclear. Token-proxy `docker-compose.yml` may still reference Qdrant for the cache layer.

### 3.7 Email Learning Reports to Ewan

| Property | Value |
|----------|-------|
| **Source** | `STATUS.md:52` — "Email learning reports to Ewan not yet built." |
| **Cron entry** | Weekly Mon 8am is scheduled, but the underlying report-generation code is not confirmed to exist. |
| **Context** | Listed in STATUS.md as needing attention since 2026-04-29. |

### 3.8 Radical Attribution in Generated Content

| Property | Value |
|----------|-------|
| **Source** | `STATUS.md:54` — "All three avatars flagged same issue: content doesn't cite sources. Radical attribution not yet showing up in generated content." |
| **Context** | The marketing engine generates content, but the synthetic evaluators (Bob, Lisa, Marcus) all flagged that sources are not cited. No code found to inject attribution into generated content. |

### 3.9 WhatsApp / Evolution API Alerting

| Property | Value |
|----------|-------|
| **Source** | `00_authority/BRAIN_ARCHITECTURE.md` § 7 — "WhatsApp (Evolution API): The pager — alerts only. Tier 3 escalations, daily health summaries." |
| **CRM code** | WhatsApp bot code exists (`scripts/whatsapp_claude_bot.py`, frontend handlers) but is a conversational bot, not the alerting/pager function described in the architecture. |
| **No code found** | Evolution API integration for Tier 3 escalation alerts. No health summary sender. |

### 3.10 Intelligence Features — Thin or Missing

These are listed in `BRAIN_ARCHITECTURE.md:463` as intelligence features but have little or no implementation:

| Feature | Code Found | Status |
|---------|------------|--------|
| **Exit Strategy** | No class or function found | Mentioned only |
| **Parts Concierge** | No class or function found | Mentioned only |
| **Portfolio Generator** | No class or function found | Mentioned only |

### 3.11 Tailscale VPN

| Property | Value |
|----------|-------|
| **Source** | `02_build/security/2026-05-09_beast-hardening-phase2_v1.md:66-73` |
| **Linear** | [AMP-136](https://linear.app/amplifiedpartners/issue/AMP-136) |
| **Context** | Container is **running** (Tailscale image on `openclaw_default` network) but **not authenticated** — `TS_AUTHKEY` is empty. Needs interactive login via Tailscale admin. Has `CAP_NET_ADMIN` and `CAP_SYS_MODULE` with `/dev/net/tun` mounted. |

### 3.12 Linear-to-Vellum Migration

| Property | Value |
|----------|-------|
| **Source** | `00_authority/BRAIN_ARCHITECTURE.md:605` — "Vellum gains parity → dual-running (Vellum primary, Linear read-only) → Linear archived → Linear contract closed." |
| **Spec** | `2026-05-14_SPEC_linear-to-vellum-migration.md` (referenced, not yet executed) |
| **Context** | Migration phases documented. No migration code or tooling found. Vellum Brief + Council modes running; the migration itself hasn't started. |

---

## Known Blockers (Cross-Cutting)

These issues affect multiple items across all three sections:

| Blocker | Linear | Impact | Blocked On |
|---------|--------|--------|------------|
| **Anthropic billing exhausted** | [AMP-142](https://linear.app/amplifiedpartners/issue/AMP-142) | Token proxy, PUDDING labeller, CRM model router, voice agent conversation — all at risk | Ewan (billing top-up) |
| **OpenAI/Moonshot 401** | [AMP-142](https://linear.app/amplifiedpartners/issue/AMP-142) | Sovereign fleet fallbacks, LiteLLM chains degraded | Ewan (key refresh) |
| **Postgres password missing** | [AMP-141](https://linear.app/amplifiedpartners/issue/AMP-141) | Cannot connect to `amplified` user for migrations | Ewan |
| **Traefik dashboard unreachable** | [AMP-140](https://linear.app/amplifiedpartners/issue/AMP-140) | Cannot verify routing config via dashboard | Investigation needed |
| **Orphan LiteLLM virtual key** | [AMP-143](https://linear.app/amplifiedpartners/issue/AMP-143) | $941 burn on a key that may be unused | Ewan (confirm rotation/kill) |

---

## Changelog

### v1 — 2026-05-15

Inventory created from cross-referencing: `02_build/INFRASTRUCTURE.md` v2, `01_truth/SYSTEMS-AND-API-REGISTER.md` v2, `00_authority/BRAIN_ARCHITECTURE.md` v5, `STATUS.md` v2, CRM repo code scans (all `app/` directories), knowledge notes, and Linear ticket references.

Signed-by: Devon | 2026-05-15 | devin-7e8210cfe08f46b29042573424e899f0

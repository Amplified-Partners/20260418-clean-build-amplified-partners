---
title: "Systems and API Register"
id: "systems-and-api-register"
version: 1
created: 2026-05-01
last_validated: 2026-05-01
type: register
status: candidate
signed_by: "Devon, 2026-05-01, devin-f32d587cc3e54f959c5309d93f72bc97"
---

# Systems and API Register

**Purpose:** Single document that tells you what's where. Every API, MCP server, telephony system, and functional module across Amplified Partners — with file paths, line counts, and endpoint counts.

**Last validated:** 2026-05-01 by Devon (automated scan of all repos).

---

## Summary

| Category | Count | Total Lines |
|----------|-------|-------------|
| CRM API route modules | 16 | 5,964 |
| Command Centre API endpoints | 24 | 863 |
| Marketing Engine API endpoints | 19 | ~600 |
| MCP Servers (Cove Orchestrator) | 8 | ~2,160 |
| MCP Servers (CRM) | 5 | 2,256 |
| NightScout Intelligence Pipeline | 7 | ~895 |
| Telephony & Voice (all locations) | 6 modules (8 files) | ~4,100 |
| Content Engine | 6 | ~1,120 |
| Safety & Monitoring | 4 | ~1,080 |
| Knowledge & Ingestion | 7 | ~1,500 |

---

## 1. CRM — REST API Routes

**Repo:** `Amplified-Partners/crm`
**Location:** `app/api/routes/`
**Framework:** FastAPI + SQLAlchemy + Alembic
**Total:** 16 route modules, 124 endpoints, 5,964 lines

### 1a. Telephony & Voice (CRM)

| Module | File | Lines | Endpoints | What It Does |
|--------|------|-------|-----------|-------------|
| Retell AI Integration | `retell_integration.py` | 819 | 11 | Full voice agent — calendar check, appointment booking, emergency SMS, CRM logging. Webhooks for call lifecycle (incoming → started → ended → analysis). 600ms latency target. |
| Voice Bridge | `voice_bridge.py` | 490 | 3 | Twilio Voice + Deepgram Nova-3 (STT, UK accents) + ElevenLabs Flash v2.5 (TTS, British voices) + Claude. Inbound/outbound TwiML. GDPR recording consent. WebSocket streaming. |
| Telegram Bridge | `telegram_bridge.py` | 426 | 4 | Task routing, interview-complete notifications, status polling, callback handling via Telegram. |

**Retell endpoints:**
- `POST /functions/check_calendar_availability` — check free slots
- `POST /functions/book_appointment` — book a slot
- `POST /functions/send_emergency_sms` — emergency SMS via Twilio
- `POST /functions/log_call_to_crm` — write call record to CRM
- `POST /webhook/call-incoming` — inbound call handler
- `POST /webhook/call-status` — call status update
- `POST /webhook/call-started` — call start event
- `POST /webhook/call-ended` — call end event
- `POST /webhook/call-analysis` — post-call AI analysis
- `GET /status` — integration health
- `POST /test-call` — test call trigger

**Voice Bridge endpoints:**
- `POST /twiml/inbound` — inbound call TwiML
- `POST /twiml/consent` — GDPR recording consent
- `POST /twiml/outbound` — outbound call TwiML

**Telegram Bridge endpoints:**
- `POST /task` — route task via Telegram
- `POST /interview-complete` — interview completion notification
- `GET /status/{task_id}` — task status
- `POST /callback` — Telegram callback handler

### 1b. Interview System

| Module | File | Lines | Endpoints | What It Does |
|--------|------|-------|-----------|-------------|
| Interview | `interview.py` | 673 | 18 | "The interview IS the product." Founder + staff interview flows. Claude-driven question selection, insight extraction with confidence scores. Life first, then business. |

**Endpoints:**
- `POST /start` — start new interview session
- `POST /{session_id}/respond` — submit response
- `POST /{session_id}/pause` — pause session
- `POST /{session_id}/resume` — resume session
- `POST /{session_id}/complete` — complete and generate extractions
- `GET /{session_id}` — session summary
- `GET /{session_id}/extractions` — extracted insights
- `POST /{session_id}/extractions/{extraction_id}/confirm` — confirm extraction
- `GET /{session_id}/messages` — message history
- `GET /{session_id}/progress` — interview progress
- `GET /{session_id}/state` — session state
- `DELETE /{session_id}` — delete session
- `GET /sessions/list` — list all sessions
- `POST /{session_id}/save` — save session
- `GET /{session_id}/support-plan` — staff support plan
- `GET /{session_id}/boss-summary` — owner summary
- `GET /{session_id}/weekly-checkin-questions` — weekly check-in
- `GET /{session_id}/crisis-check` — crisis detection

### 1c. Business Brain

| Module | File | Lines | Endpoints | What It Does |
|--------|------|-------|-----------|-------------|
| Business Brain | `business_brain.py` | 435 | 9 | RAG-based strategic recommendations. Interview data + Qdrant knowledge + Claude → Business Bible. |

**Endpoints:**
- `POST /create-from-founder-interview` — generate brain from founder interview
- `POST /add-staff-interview` — add staff interview data
- `POST /connect-mcp-server` — connect MCP data source
- `POST /generate-recommendations/{tenant_id}` — generate recommendations
- `GET /summary/{tenant_id}` — brain summary
- `GET /{tenant_id}` — full brain data
- `GET /{tenant_id}/completeness` — data completeness score
- `GET /{tenant_id}/friction` — friction analysis
- `GET /{tenant_id}/wow-opportunities` — wow opportunity detection

### 1d. Intelligence & Analytics

| Module | File | Lines | Endpoints | What It Does |
|--------|------|-------|-----------|-------------|
| Intelligence (Core) | `intelligence.py` | 355 | 5 | CLV analysis, death-spiral detection, bottleneck identification, dashboards. |
| Intelligence (Routes) | `intelligence_routes.py` | 256 | 7 | Weekly insights, pricing analysis, industry benchmarks, seasonal patterns, optimal timing. |

**Core Intelligence endpoints:**
- `POST /analyze/{tenant_id}` — full business analysis
- `POST /death-spiral/{tenant_id}` — death-spiral indicator check
- `POST /bottlenecks/{tenant_id}` — bottleneck identification
- `GET /dashboard/{tenant_id}` — intelligence dashboard
- `GET /insight/{tenant_id}/{insight_id}` — specific insight

**Intelligence Routes endpoints:**
- `GET /insights/weekly` — weekly insight digest
- `GET /insights/pricing` — pricing analysis
- `GET /benchmarks/compare` — cross-business comparison
- `GET /benchmarks/industry-insights` — industry benchmarks
- `GET /benchmarks/optimal-timing/{feature_name}` — timing optimisation
- `GET /benchmarks/seasonal` — seasonal patterns
- `GET /health` — service health

### 1e. CRM Core (Contacts, Companies, Deals, Activities)

| Module | File | Lines | Endpoints | What It Does |
|--------|------|-------|-----------|-------------|
| Contacts | `contacts.py` | 277 | 10 | Contact CRUD, PII management, anonymisation, GDPR consent. |
| Companies | `companies.py` | 107 | 5 | Company CRUD. |
| Deals | `deals.py` | 140 | 6 | Deal tracking, pipeline summary. |
| Activities | `activities.py` | 119 | 5 | Activity logging (calls, emails, meetings). |

### 1f. Accounting & Payments

| Module | File | Lines | Endpoints | What It Does |
|--------|------|-------|-----------|-------------|
| Stripe | `stripe_routes.py` | 298 | 9 | Checkout sessions, subscription management, customer portal, webhooks. |
| Xero | `xero_routes.py` | 411 | 7 | OAuth connect/callback, invoice/bill creation, webhook handling. |
| QuickBooks | `quickbooks_routes.py` | 340 | 6 | OAuth connect/callback, invoice/expense creation. |
| Calendar | `calendar_routes.py` | 390 | 7 | OAuth connect/callback, event CRUD, conflict detection. |

### 1g. Orchestration

| Module | File | Lines | Endpoints | What It Does |
|--------|------|-------|-----------|-------------|
| Orchestrator | `orchestrator.py` | 428 | 12 | Project/task management, approval workflows, agent spawning. |

**Endpoints:**
- `POST /projects` — create project
- `GET /projects/{project_id}` — get project
- `GET /projects/{project_id}/status` — project status
- `POST /tasks` — create task
- `GET /projects/{project_id}/tasks` — list project tasks
- `GET /tasks/{task_id}` — get task
- `GET /approvals` — list pending approvals
- `GET /approvals/{approval_id}` — get approval
- `POST /approvals/{approval_id}/respond` — approve/reject
- `POST /agents/spawn` — spawn sub-agent
- `GET /health` — health check
- `GET /stats` — orchestrator stats

---

## 2. Command Centre — REST API

**Repo:** `Amplified-Partners/clean-build`
**Location:** `02_build/command-centre/backend/`
**Framework:** FastAPI
**Total:** 24 endpoints, ~863 lines (main.py 469 + voice_agent.py 394)

### 2a. Command Centre Main (`main.py` — 469 lines, 20 endpoints)

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/api/promises` | GET | List promises |
| `/api/tasks` | GET | List tasks |
| `/api/sessions/current` | GET | Current session info |
| `/api/beast/stats` | GET | Beast server statistics |
| `/api/beast/transcripts` | GET | Voice transcripts |
| `/api/beast/briefings` | GET | NightScout briefings |
| `/api/enforcer/health` | GET | Enforcer health check |
| `/api/kaizen/health` | GET | Kaizen health check |
| `/api/graphiti/stats` | GET | Graph database stats |
| `/api/search` | GET | SearXNG search |
| `/api/searches` | GET | Search history |
| `/api/searches/watched` | GET | Watched searches |
| `/api/searches/{search_id}` | GET | Specific search |
| `/api/searches/watch` | POST | Watch a search |
| `/api/searches/watch` | DELETE | Unwatch a search |
| `/api/searches/diffs` | GET | Search result diffs |
| `/api/searches/seen` | POST | Mark search seen |
| `/api/infra/containers` | GET | Beast container status |
| `/api/infra/containers/mac` | GET | Mac container status |
| `/api/health` | GET | Health check |

### 2b. Voice Agent (TwiML) (`voice_agent.py` — 394 lines, 4 endpoints)

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/incoming-call` | POST | TwiML inbound call handler (Claude Haiku, no WebSockets) |
| `/respond` | POST | Gather+Say response loop |
| `/health` | GET | Health check |
| `/test-claude` | POST | Test Claude connectivity |

---

## 3. Marketing Engine — REST API

**Repo:** `Amplified-Partners/marketing-engine`
**Location:** `api.py`
**Framework:** FastAPI
**Total:** 19 endpoints

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/clients` | GET | List clients |
| `/pipeline/{client_id}` | POST | Run pipeline for client |
| `/pipeline` | POST | Run default pipeline |
| `/pipeline/{client_id}/status` | GET | Pipeline status |
| `/review` | GET | Content review queue |
| `/review/{piece_id}` | GET | Specific piece for review |
| `/review/{piece_id}/feedback` | POST | Submit feedback |
| `/feedback/stats/{client_id}` | GET | Feedback statistics |
| `/content/{client_id}` | GET | Client content |
| `/outputs/{client_id}` | GET | Published outputs |
| `/engagement/{piece_id}` | POST | Log engagement |
| `/preferences/{client_id}` | GET | Client preferences |
| `/evaluate/{client_id}` | POST | Run synthetic evaluator panel |
| `/evaluate/piece/{content_id}` | POST | Evaluate specific piece |
| `/platforms` | GET | Platform configuration |
| `/atomise` | POST | Pillar → platform variants |
| `/kaizen/{client_id}` | POST | Run Kaizen improvement cycle |
| `/kaizen/{client_id}/history` | GET | Kaizen history |

---

## 4. MCP Servers — Cove Orchestrator

**Repo:** `Amplified-Partners/clean-build`
**Location:** `02_build/cove-orchestrator/mcp-servers/`
**Framework:** FastMCP (Python MCP SDK)
**Total:** 8 servers, 37 tools, ~2,160 lines

| Server | File | Lines | Tools | What It Does |
|--------|------|-------|-------|-------------|
| Email MCP | `email-mcp/server.py` | 269 | 5 | inbox_status, search, get_drafts, review_draft, run_pipeline |
| Filesystem MCP | `filesystem-mcp/server.py` | 303 | 5 | list, read, write, search, info |
| GitHub MCP | `github-mcp/server.py` | 311 | 5 | list_repos, list_issues, create_issue, list_prs, search_code |
| Langfuse MCP | `langfuse-mcp/server.py` | 294 | 4 | dashboard, traces, trace_detail, costs |
| LiteLLM MCP | `litellm-mcp/server.py` | 275 | 5 | list_models, model_info, health, spend, test |
| NightScout MCP | `nightscout-mcp/server.py` | 181 | 4 | get_briefing, search_intel, pipeline_status, run_pipeline |
| PostgreSQL MCP | `postgresql-mcp/server.py` | 234 | 4 | query, list_tables, describe_table, execute |
| Telegram MCP | `telegram-mcp/server.py` | 292 | 5 | send_message, send_approval_request, get_updates, edit_message, answer_callback |

---

## 5. MCP Servers — CRM

**Repo:** `Amplified-Partners/crm`
**Location:** `mcp_servers/`
**Total:** 5 servers, 2,256 lines

| Server | File | Lines | What It Does |
|--------|------|-------|-------------|
| CRM Server | `crm_server.py` | 442 | CRM data access tools for agents |
| Grok Server | `grok_server.py` | 481 | Grok/X AI integration |
| Gemini Server | `gemini_server.py` | 480 | Google Gemini integration |
| Kimi Server | `kimi_server.py` | 480 | Moonshot Kimi integration |
| PII Gateway | `pii_gateway.py` | 373 | Privacy-preserving data access (Presidio) |

---

## 6. Telephony & Voice — Complete Inventory

Everything related to phone, voice, SMS, and real-time communication across all repos.

### 6a. Production-Ready (CRM repo)

| System | File | Lines | Tech Stack | Status |
|--------|------|-------|-----------|--------|
| Retell AI Voice Agent | `crm/app/api/routes/retell_integration.py` | 819 | Retell AI + Cartesia TTS, 600ms latency | Complete, 11 endpoints |
| Voice Bridge | `crm/app/api/routes/voice_bridge.py` | 490 | Twilio + Deepgram Nova-3 (STT) + ElevenLabs Flash v2.5 (TTS) + Claude | Complete, 3 endpoints |
| Telegram Bridge | `crm/app/api/routes/telegram_bridge.py` | 426 | Telegram Bot API, long-polling | Complete, 4 endpoints |

### 6b. Production-Ready (Clean-build)

| System | File | Lines | Tech Stack | Status |
|--------|------|-------|-----------|--------|
| TwiML Voice Agent | `clean-build/02_build/command-centre/backend/voice_agent.py` | 394 | Twilio Gather+Say + Claude Haiku | Complete, 4 endpoints, battle-tested |

### 6c. Vault Code (Earlier Versions / Standalone)

| System | File | Lines | Tech Stack | Notes |
|--------|------|-------|-----------|-------|
| Webhook Failsafe | `corpus-raw/vault/_inbox/webhook_server_failsafe.py` | 580 | Retell AI + Twilio SMS, 3-layer failover | Layer 1: AI UK → Layer 2: backup US → Layer 3: forward to mobile |
| Retell Integration (v4) | `corpus-raw/vault/_inbox/retell_integration-v4.py` | 789 | Retell + Cartesia + Calendar + CRM | Most complete standalone version |
| Voice Bridge | `corpus-raw/vault/_inbox/voice_bridge.py` | 490 | Twilio + Deepgram + ElevenLabs + Claude | Earlier version of CRM voice_bridge |
| Webhook Server | `corpus-raw/vault/_inbox/webhook_server-v2.py` | 118 | Telnyx → Retell handoff | Simpler webhook relay |

### 6d. Telephony Dependencies & Providers

| Provider | Used For | Integration Point |
|----------|----------|-------------------|
| **Retell AI** | Primary voice agent (UK voice, sub-second latency) | `retell_integration.py` |
| **Twilio** | Voice calls (TwiML), SMS (emergency, notifications) | `voice_bridge.py`, `webhook_server_failsafe.py` |
| **Telnyx** | Alternative voice/webhook provider | `webhook_server-v2.py` |
| **Deepgram** | Speech-to-text (Nova-3 model, UK accent support) | `voice_bridge.py` |
| **ElevenLabs** | Text-to-speech (Flash v2.5, British voices) | `voice_bridge.py` |
| **Cartesia** | Text-to-speech (used by Retell integration) | `retell_integration.py` |
| **Telegram** | Approval gateway, task routing, notifications | `telegram_bridge.py`, `telegram-mcp` |

---

## 7. NightScout — Intelligence Pipeline

**Location:** `clean-build/02_build/cove-orchestrator/nightscout/`
**Total:** 7 files, ~895 lines
**What it does:** Nightly scrape → LLM score → fork → morning briefing

| File | Lines | Purpose |
|------|-------|---------|
| `config.py` | 138 | 25+ source definitions (RSS + SearXNG), scoring tiers |
| `pipeline.py` | 248 | Master orchestrator: fetch → dedup → store → score → fork → notify |
| `fetchers.py` | 182 | RSS + SearXNG fetchers, date parsing, dedup key generation |
| `scorer.py` | 131 | LLM scoring (relevance, impact, applicability, novelty) via Ollama |
| `briefing.py` | 144 | Morning briefing markdown generator |
| `main.py` | 47 | CLI entry point |
| `__init__.py` | 5 | Package init |

**Plus:**
- MCP Server: `nightscout-mcp/server.py` (181 lines) — exposes intel to other agents
- DB Schema: `db/migrations/002_nightscout_schema.sql` (139 lines)

---

## 8. Content Engine

**Location:** `corpus-raw/vault/_inbox/` (vault code) + `marketing-engine/` (production repo)
**Total:** ~1,120 lines (vault) + full marketing-engine repo

### Vault Code (Pipeline Components)

| File | Lines | What It Does |
|------|-------|-------------|
| `atomiser.py` | 196 | Pillar → 5 platform variants (LinkedIn, Twitter, Substack, Facebook, carousel) |
| `scheduler.py` | 307 | APScheduler content queue, UK-optimal timing |
| `telegram_gate-v2.py` | 287 | Content approval via Telegram inline buttons |
| `substack.py` | 100 | Substack publishing |
| `linkedin.py` | 112 | LinkedIn posting |
| `twitter.py` | 118 | Twitter/X posting |

### Marketing Engine (Production)

| File | Lines | What It Does |
|------|-------|-------------|
| `api.py` | ~600 | 19 REST endpoints (see Section 3) |
| `orchestrator.py` | — | Pipeline orchestration |
| `synthetic_evaluator.py` | — | Bob/Lisa/Marcus evaluator panel |
| `kaizen.py` | — | Continuous improvement cycles |
| `agents/research_agent.py` | — | SearXNG research |
| `agents/content_agent.py` | — | Content generation |
| `agents/content_atomizer.py` | — | Content atomisation |
| `agents/publishing_agent.py` | — | Multi-platform publishing |
| `integrations/brevo.py` | — | Brevo email integration |
| `integrations/heygen.py` | — | HeyGen video integration |

---

## 9. Safety & Monitoring

**Location:** `corpus-raw/vault/_inbox/`

| File | Lines | What It Does |
|------|-------|-------------|
| `security_scanner.py` | 383 | Prompt injection detection via llm-guard + regex fallback |
| `prompt_sanitizer.py` | 64 | Wraps external input before it hits Claude |
| `cost_monitor.py` | 326 | Per-call, per-model cost tracking + Telegram daily alerts |
| `sentinel_v2-v2.py` | 307 | Codebase health: basic health → detailed analysis → alert and halt |

---

## 10. Knowledge & Ingestion

**Location:** `corpus-raw/vault/_inbox/` + `clean-build/02_build/scripts/`

| File | Lines | Location | What It Does |
|------|-------|----------|-------------|
| `semantic_cache-v3.py` | 282 | vault/_inbox | Anthropic wrapper + Qdrant semantic cache (0.95 cosine, 24h TTL) |
| `ingest_transcripts-v3.py` | ~160 | vault/_inbox | Voice transcript → Qdrant |
| `ingest_all_monologue.py` | 176 | vault/_inbox | Batch monologue ingestion |
| `run_all_puddings-v2.py` | ~220 | vault/_inbox | PUDDING analysis pipeline + fastembed |
| `pudding_labeler.py` | 354 | clean-build scripts | PUDDING 2026 taxonomy: WHAT.HOW.SCALE.TIME |
| `porch_watcher.py` | 234 | clean-build scripts | File intake: incoming/ → PUDDING label → Qdrant → labeled/ |
| `gmail_automation.py` | 130 | vault/_inbox | Gmail triage via Google API |

---

## 11. Business Brain (Core Product Logic)

**Location:** `corpus-raw/vault/_inbox/`

| File | Lines | What It Does |
|------|-------|-------------|
| `brain.py` | 474 | Intelligence engine: interview data + Qdrant + Claude → Business Bible |
| `engine.py` | 493 | Interview engine: Claude-driven question selection, insight extraction |
| `business_brain_service.py` | 598 | Week 1 Universal Onboarding orchestrator |
| `claude_client.py` | 303 | Anthropic API client with prompt caching |

---

## 12. Database Migrations

**Location:** `clean-build/02_build/cove-orchestrator/db/migrations/`

| File | Lines | What It Does |
|------|-------|-------------|
| `001_initial_schema.sql` | 212 | Foundation: projects, tasks, approvals, agent_runs, budget, MCP, models |
| `002_nightscout_schema.sql` | 139 | NightScout: sources, raw items, scored items, briefings, pipeline runs |
| `003_email_agent_schema.sql` | — | Email agent tables |

**CRM migrations:** `crm/alembic/` — full Alembic migration history for CRM schema.

---

## 13. Specifications (Mac Drop — now merged to main)

**Location:** `clean-build/90_archive/specifications/mac-drop-2026-04/`
**Status:** Non-authoritative reference. 30 files, 33,153 lines.

Key specs relevant to this register:

| Spec | Lines | Covers |
|------|-------|--------|
| ATTRIBUTION-AND-CURATION-v1 | 965 | 5 Curator agents, data provenance |
| CURATOR-GATE-SPEC-v1-pandoc | 503 | 5 sequential quality gates |
| watchman-expansion-strategy | 708 | Local LLM migration, 35+ processes |
| extraction-department-spec | 1,028 | Ingest → Extract → Synthesise → Route |
| AMPLIFIED-PUDDING-DISCOVERY-SYSTEM | 1,050 | APDS 5-stage pipeline |
| amplified_master_architecture | 2,073 | Master architecture, Eight Laws |
| VISUAL-POLISH-SYSTEM-COMPLETE-BUILD-GUIDE | 4,527 | Design system + scoring |

Full index: `90_archive/specifications/mac-drop-2026-04/README.md`

---

## Architecture Overview

```
Layer 0: Safety         security_scanner, prompt_sanitizer, cost_monitor, sentinel, PII gateway
Layer 1: Intelligence   NightScout (fetch → score → brief), semantic_cache, PUDDING labeler
Layer 2: Knowledge      brain.py, engine.py, Qdrant, PUDDING taxonomy, porch_watcher
Layer 3: Operations     email_agent, voice_bridge, retell, task_router, CRM (contacts/companies/deals)
Layer 4: Content        atomiser, scheduler, telegram_gate, marketing_engine, social integrations
Layer 5: Coordination   command_centre, cove-orchestrator, AG2 executive, Temporal, MCP servers
Layer 6: Accounting     Stripe, Xero, QuickBooks, Calendar integrations
```

---

## Cross-Reference: Where Code Lives

| System | CRM Repo | Clean-Build | Vault (_inbox) | Marketing Engine |
|--------|----------|-------------|----------------|-----------------|
| Voice/Telephony | retell, voice_bridge, telegram | voice_agent | webhook_failsafe, voice_bridge, retell v1-v4 | — |
| Interview | interview.py | — | interview.py | — |
| Business Brain | business_brain.py | — | brain.py, engine.py, business_brain_service.py | — |
| Intelligence | intelligence.py, intelligence_routes.py | — | — | — |
| CRM CRUD | contacts, companies, deals, activities | — | contacts, companies, deals, activities | — |
| Content | — | — | atomiser, scheduler, telegram_gate | Full pipeline |
| NightScout | — | nightscout/ | — | — |
| MCP Servers | crm, grok, gemini, kimi, pii | email, filesystem, github, langfuse, litellm, nightscout, postgresql, telegram | grok, gemini, kimi (older versions) | — |
| Safety | — | — | security_scanner, prompt_sanitizer, cost_monitor, sentinel | — |
| Accounting | stripe, xero, quickbooks, calendar | — | — | — |

---

*This register is a living document. Update it when new systems are added or existing ones move.*

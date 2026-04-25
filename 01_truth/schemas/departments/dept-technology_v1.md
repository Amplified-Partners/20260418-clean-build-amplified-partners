---
title: "Dept Technology"
id: "dept-technology"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "dept-technology.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — Technology & Infrastructure
## Deep Memory Extraction
### Compiled: 27 March 2026

---

> **Sources**: Perplexity custom skills (amplified-beast-ops v1, amplified-key-rotation v2.0, transcription-prompt-optimiser v1.0), amplified-partners-knowledge-reconstruction.md, Linear workspace inventory, GitHub repository data. This document covers ~6 months of infrastructure work (October 2025 – March 2026).

---

## Table of Contents

1. [Three-Tier Hardware Strategy](#1-three-tier-hardware-strategy)
2. [The Beast Server — Full Specification](#2-the-beast-server--full-specification)
3. [Docker Container Registry (36+)](#3-docker-container-registry-36)
4. [Database Architecture](#4-database-architecture)
5. [Cove Code Factory & Temporal Pipeline](#5-cove-code-factory--temporal-pipeline)
6. [LiteLLM Proxy & Model Routing](#6-litellm-proxy--model-routing)
7. [MCP Servers & APIs Built or Planned](#7-mcp-servers--apis-built-or-planned)
8. [Security Infrastructure](#8-security-infrastructure)
9. [Voice Pipeline & Transcription Systems](#9-voice-pipeline--transcription-systems)
10. [Edge Computing & PicoClaw Strategy](#10-edge-computing--picoclaw-strategy)
11. [Technical Failures & Lessons Learned](#11-technical-failures--lessons-learned)
12. [Directory Layout & File Paths](#12-directory-layout--file-paths)
13. [Environment Variables & Secrets Inventory](#13-environment-variables--secrets-inventory)
14. [Infrastructure Timeline (Chronological)](#14-infrastructure-timeline-chronological)

---

## 1. Three-Tier Hardware Strategy

The architecture is a deliberate three-tier system, with each layer serving a distinct purpose:

| Tier | Device | Role | Key Specs |
|------|--------|------|-----------|
| **Tier 1** | MacBook Air M4 | Thin client | New, purchased March 26, 2026 — day of final Beast wipe |
| **Tier 2** | Mac Mini M4 Pro | Primary compute & dev workstation | 24GB RAM, serial: QX47GGW4V0, warranty expires March 1, 2027 |
| **Tier 3** | Hetzner AX162-R ("The Beast") | Data core server | 48-core AMD EPYC, 256GB RAM, 10Gbps, Ubuntu 24.04 |

### Rationale for Three Tiers
- **MacBook Air**: Portability, thin client only — no sensitive processing
- **Mac Mini**: Local AI development, orchestration, VS Code, the daily driver
- **Beast**: Heavy compute, all Docker services, inference at scale, 10Gbps network, data sovereignty for client data

### Mac Mini Security Hardening (March 15, 2026)
The Mac Mini was explicitly security-audited and hardened:
- Firewall: **ON**
- FileVault: **ON** (full disk encryption)
- Auto-updates: **ON**
- Screen lock: **5 minutes**
- Gatekeeper: **ON**
- SIP (System Integrity Protection): **ON**

---

## 2. The Beast Server — Full Specification

### Hardware & Network

| Field | Value |
|-------|-------|
| **Provider** | Hetzner |
| **Model** | AX162-R |
| **IP Address** | 135.181.161.131 |
| **Operating System** | Ubuntu 24.04 |
| **CPU** | 48-core AMD EPYC |
| **RAM** | 256GB total (96GB allocated to Ollama for local inference) |
| **Network** | 10 gigabit |
| **DNS** | Wildcard `*.beast.amplifiedpartners.ai` → 135.181.161.131 |
| **SSH Access** | `ssh root@135.181.161.131` |

### Confirmed Live External URLs (via Traefik)

| URL | Service | Notes |
|-----|---------|-------|
| `api.amplifiedpartners.ai` | amplified-core (port 8000) | Main API + Finance Engine at `/api/v1/finance/*` |
| `search.beast.amplifiedpartners.ai` | SearXNG (port 8888) | v2026.3.12+3d3a78f3a |
| `ollama.beast.amplifiedpartners.ai` | Ollama (port 11434) | Local LLM inference |
| `voice.beast.amplifiedpartners.ai` | voice-pipeline | Voice transcription (Deepgram Nova-3) |
| `enforcer.beast.amplifiedpartners.ai` | enforcer | Health/compliance checks |
| `code.beast.amplifiedpartners.ai` | amplified-code-server | VS Code in browser |
| `langfuse.beast.amplifiedpartners.ai` | langfuse | LLM observability + tracing |
| `cove.beast.amplifiedpartners.ai` | cove-api (port 8081) | Cove build pipeline API |
| `pudding.beast.amplifiedpartners.ai` | (planned) | APDS dashboard (planned, not yet deployed) |

### Traefik Architecture
- All external traffic enters via Traefik on ports **80/443**
- TLS certificates auto-provisioned via **Let's Encrypt** (`certresolver=letsencrypt`)
- **Rule**: No service has direct external port mappings — all external access goes through Traefik labels
- Primary Docker network: `amplified-net` (external bridge network — all services must join this)
- Isolated R&D network: `rd-sandbox` (planned for `rd-worker`, no production access)

#### Traefik Label Format
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.my-service.rule=Host(`my-service.beast.amplifiedpartners.ai`)"
  - "traefik.http.routers.my-service.tls=true"
  - "traefik.http.routers.my-service.tls.certresolver=letsencrypt"
  - "traefik.http.services.my-service.loadbalancer.server.port=8080"
networks:
  - amplified-net
```

---

## 3. Docker Container Registry (36+)

### Port Summary (Complete Reference)

| Port | Service | Access Type |
|------|---------|------------|
| 80/443 | Traefik | External |
| 4000 | LiteLLM | Internal (`litellm:4000`) |
| 5432 | PostgreSQL main | Internal only |
| 5433 | cove-postgres | External mapping (direct access if needed) |
| 6379 | Redis + FalkorDB | Internal only (FalkorDB locked after CPU incident) |
| 6333 | Qdrant | Internal only |
| 7233 | Temporal gRPC | Internal (`cove-temporal:7233`) |
| 8000 | amplified-core | Internal/Traefik |
| 8081 | cove-api | Via Traefik |
| 8233 | Temporal UI | Localhost only (SSH tunnel required) |
| 8700 | finance-engine | Via Traefik |
| 8750 | ch-pipeline | Internal |
| 8888 | SearXNG | Via Traefik |
| 11434 | Ollama | Via Traefik + Internal |

### Infrastructure Layer

| Container | Purpose | Port(s) | Compose File |
|-----------|---------|---------|--------------|
| `traefik` | Reverse proxy + TLS | 80, 443 | `/opt/amplified/traefik/` |
| `postgres` | Main PostgreSQL (`amplified_main` DB) | 5432 (internal) | `/opt/amplified/docker-compose.yml` |
| `redis` | Cache + queue | 6379 (internal) | `/opt/amplified/docker-compose.yml` |
| `falkordb` | Graph DB + vector search (Graphiti Business Brain) | 6379+3000 (internal ONLY — locked down) | `/opt/amplified/docker-compose.yml` |
| `qdrant` | Vector database | 6333 (internal) | `/opt/amplified/docker-compose.yml` |
| `portainer` | Docker management UI | internal | `/opt/amplified/docker-compose.yml` |
| `watchtower` | Auto-update containers | — | `/opt/amplified/docker-compose.yml` |
| `minio` | Object storage | internal | `/opt/amplified/docker-compose.yml` |

**MinIO Buckets (5)**: `content`, `exports`, `assets`, `handwritten-notes`, `backups`

### AI / Inference Layer

| Container | Purpose | Port(s) | Compose File |
|-----------|---------|---------|--------------|
| `ollama` | Local LLM inference | 11434 | `/opt/amplified/apps/ollama/docker-compose.yml` |
| `litellm` | Multi-provider model proxy | 4000 (internal) | `/opt/amplified/apps/litellm/` |
| `langfuse` | LLM observability + tracing | — | `/opt/amplified/apps/langfuse/` |

**Ollama Loaded Models**:
- `llama3.1:8b` — Fast inference, **39 tok/s warm** (benchmark achieved)
- `llama3.1:70b` — Heavy inference (96GB RAM allocated for this)
- `nomic-embed-text` — Embeddings

### Search & Intelligence Layer

| Container | Purpose | Port(s) | URL |
|-----------|---------|---------|-----|
| `searxng` | Self-hosted search (243+ sources, no rate limits) | 8888 (internal) | `search.beast.amplifiedpartners.ai` |
| `nightscout` | NightScout intelligence pipeline cron | internal | — |
| `nightscout-mcp` | NightScout FastMCP server | internal | — |

**SearXNG Policy**: Beast-first search policy — all AI sessions should use SearXNG as first search source before Perplexity fallback. Search API: `curl "https://search.beast.amplifiedpartners.ai/search?q=QUERY&format=json"`

### Agent Orchestration Layer

| Container | Purpose | Port(s) | Notes |
|-----------|---------|---------|-------|
| `openclaw-agents` | OpenClaw agent framework (heavy agents, Six Hats) | internal | Deployed to Beast |
| `amplified-core` | Fastify MCP Gateway | 8000 | `api.amplifiedpartners.ai` |
| `amplified-worker` | Background worker for amplified-core | internal | — |

### Cove Code Factory — Temporal Pipeline

| Container | Purpose | Port(s) | Notes |
|-----------|---------|---------|-------|
| `cove-temporal` | Temporal workflow server | 7233 gRPC | Internal: `cove-temporal:7233` |
| `cove-temporal-ui` | Temporal web UI | 8233 | Localhost only (SSH tunnel to access) |
| `cove-postgres` | Cove-specific PostgreSQL (TimescaleDB-HA pg15 + pgvector) | 5433 external / 5432 internal | `cove-postgres:5432` |
| `cove-api` | Cove REST API gateway | 8081 | `cove.beast.amplifiedpartners.ai` |
| `cove-worker` | Primary Temporal worker | — | Polls `build-orchestrator` queue |
| `cove-worker-alpha` | Parallel Temporal worker A | — | — |
| `cove-worker-bravo` | Parallel Temporal worker B | — | — |
| `cove-worker-charlie` | Parallel Temporal worker C | — | — |
| `cove-worker-delta` | Parallel Temporal worker D | — | — |
| `docker-temporal-worker-1` | Additional Temporal worker | — | Check health via `docker logs` |

### Product Services Layer

| Container | Purpose | Port(s) | URL |
|-----------|---------|---------|-----|
| `finance-engine` | Financial analysis API (v1.3.1) | 8700 | `api.amplifiedpartners.ai/api/v1/finance/*` |
| `ch-pipeline` | Companies House XBRL parser | 8750 | Internal |
| `amplified-voice-agent` | Voice agent service | internal | — |
| `xai-phone-agent` | xAI Grok phone agent | internal | — |
| `amplified-code-server` | VS Code in browser | — | `code.beast.amplifiedpartners.ai` |
| `nexus-dashboard` | Nexus investment dashboard | internal | — |
| `voice-pipeline` | Voice transcription (Deepgram Nova-3) | — | `voice.beast.amplifiedpartners.ai` |

**Additional service paths** (on Beast, not main Docker):
```
/opt/amplified-machine/services/
├── ch-pipeline/    # Companies House XBRL pipeline (port 8750)
├── finance-engine/ # Finance Engine (port 8700)
```

### Quality & Monitoring Layer

| Container | Purpose | Notes |
|-----------|---------|-------|
| `enforcer` | Production health + compliance | Every 10 minutes, all 5 checks concurrent, completes in <30s |
| `kaizen-optimizer` | Daily Kaizen improvement cycle | internal |
| `clickhouse` | Analytics database | internal |

### Planned But Not Yet Deployed (as of March 27, 2026)

| Container | Linear Issue | Purpose |
|-----------|-------------|---------|
| `kaizen-worker` | COV-250 | Kaizen department |
| `chaos-worker` | COV-250 | Chaos testing |
| `rd-worker` | COV-250 | R&D sandbox (isolated `rd-sandbox` network) |
| `content-atomizer` | COV-226 | Content atomisation |
| `email-sequence` | COV-227 | Email sequence automation |

---

## 4. Database Architecture

### FalkorDB (Graph DB + Vector Search)

**Role**: Business Brain via Graphiti knowledge graph. The primary graph layer for all client knowledge.

| Setting | Value |
|---------|-------|
| **Internal address** | `falkordb:6379` |
| **External access** | **NONE** — locked down after CPU incident |
| **Max memory** | 8GB |
| **Thread count** | 8 |
| **Data volume** | `falkordb-data` |
| **Compose** | `/opt/amplified/docker-compose.yml` |

**Database Names**:
- `amplified_brain` — Master Business Brain (Amplified Partners itself)
- `kg_internal` — Internal knowledge graph
- `kg_{client_id}` — Per-client isolated databases (data sovereignty enforcement)

**Access from another container** (via `amplified-net`):
```bash
redis-cli -h falkordb -p 6379
redis-cli -h falkordb -p 6379 GRAPH.QUERY amplified_brain "MATCH (n) RETURN count(n)"
```

**Why FalkorDB was locked down**: A CPU incident occurred when FalkorDB was externally port-mapped — unconstrained external queries pegged CPU. Port removed entirely; only accessible via API layer or FalkorDB MCP server.

**Key failure**: FalkorDB graph was lost **5 times** across Beast wipes. The graph is derivative of source documents — if source markdown/PDFs survive (on iCloud or Mac Mini), the graph can be rebuilt. The source documents are the true primary asset, not the graph index.

### Qdrant (Vector Database)

**Role**: Semantic search across all content. Used for PUDDING discovery pipeline.

| Setting | Value |
|---------|-------|
| **Internal address** | `qdrant:6333` |
| **External access** | None (internal only) |
| **Compose** | `/opt/amplified/docker-compose.yml` |

### PostgreSQL — Main Instance

**Role**: Relational data, Finance Engine backend, operational data.

| Setting | Value |
|---------|-------|
| **Internal address** | `postgres:5432` |
| **Database name** | `amplified_main` |
| **Secret** | `pg_password` at `/opt/amplified/secrets/` |
| **External** | No external port mapping |

```bash
# Connect from Beast
docker exec -it postgres psql -U postgres -d amplified_main
```

### PostgreSQL — Cove Instance (TimescaleDB + pgvector)

**Role**: Cove Code Factory workflow data, time-series metrics, vector operations.

| Setting | Value |
|---------|-------|
| **Internal address** | `cove-postgres:5432` |
| **External mapped port** | 5433 (direct access if needed) |
| **Version** | TimescaleDB-HA pg15 + pgvector extension |

```bash
docker exec -it cove-postgres psql -U postgres
```

### Redis

**Role**: Cache + queue across all services.

| Setting | Value |
|---------|-------|
| **Internal address** | `redis:6379` |
| **Note** | Shares port 6379 with FalkorDB (different containers) |

### Unified Data Architecture (Constitutional Document, March 20, 2026)

Five data stores — formal architecture decision:

| Store | Purpose |
|-------|---------|
| 1. Document Store | Single source of truth — all source documents |
| 2. Knowledge Graph | FalkorDB — relationships, concepts, entity links |
| 3. Vector Index | Qdrant — semantic search, embedding lookup |
| 4. Process Database | PostgreSQL — operational data, workflows |
| 5. Backup Store | MinIO — archived exports |

**Key principles** from constitutional document:
- **Label-once-propagate-everywhere** — taxonomy applied once by Curator, propagates to all stores
- **Curator-exclusive taxonomy assignment** — only the Curator agent can assign taxonomy codes
- **JSON strictly for active agent tasks** — not for long-term storage

### Business Vault per Client

Each client gets an isolated "business brain":
- **FalkorDB**: `kg_{client_id}` — client's knowledge graph
- **Qdrant**: Client-namespaced vector collection
- **PostgreSQL**: Client data in `amplified_main` with row-level isolation

**Client identification**: Four-word random IDs (e.g., `merit-over-identity-trust`), never real names. ~51.6 bits entropy (Diceware-style, validated by Kimi K2.5).

---

## 5. Cove Code Factory & Temporal Pipeline

### Overview

Cove is the AI-native build pipeline that converts Linear issues into tested, deployed code using Claude agents and Temporal workflows. It sits at Layer 2 of the AI-Native Development Infrastructure Blueprint.

**GitHub repo**: `cove` (private) — last updated March 22, 2026. Contains Temporal pipeline, agent loop, MCP bridge, Layer 0 laws.

### Architecture

```
Linear Issue (COV-xxx)
        │
        ▼
Cove API (port 8081)  ←→  cove.beast.amplifiedpartners.ai
        │
        ▼
Temporal Workflow Server (port 7233 gRPC)
        │
        ├── cove-worker (primary — polls build-orchestrator queue)
        ├── cove-worker-alpha
        ├── cove-worker-bravo
        ├── cove-worker-charlie
        ├── cove-worker-delta
        └── docker-temporal-worker-1
        │
        ▼
Claude Agents (via LiteLLM → Anthropic)
        │
        ▼
GitHub (code deployed to repos)
        │
        ▼
Beast (containers deployed via Docker)
```

### Temporal Workflow Structure

**Location on Beast**: `/opt/amplified/agent-stack/cove-orchestrator/`

```
temporal/
├── workflows/    # 10 Temporal workflows
├── activities/   # 12 activity modules
└── workers/
    └── main.py

agents/
├── configs/
│   └── agent_registry.py
├── prompts/
│   ├── (Layer 0-2 prompts)
│   └── knowledge_base.md
├── rubrics/
└── executive/
    └── runner.py

api/              # FastAPI gateway (port 8081)
mcp-servers/      # telegram, nightscout, email, postgresql, template
docker/
└── docker-compose.yml
```

### Cove Code Factory Strategy

- **Primary approach**: Assemble pre-built, vetted open-source components from GitHub — **not write from scratch**
- **Target stack**: APIs, MCP servers, MCPipe/UnixPipe, SQL databases, LangGraph workflows
- **All code**: Deterministic, privacy-first, security-accredited (Cyber Essentials target)
- **Privacy**: P2 tokenisation built into every component touching client data
- **Cove issues series**: COV-xxx (these were on a Beast-based Linear workspace — may have been lost in wipes)

### Key Cove Issues Referenced

| Issue | Description |
|-------|-------------|
| COV-226 | content-atomizer container |
| COV-227 | email-sequence container |
| COV-229 | DNS wildcard `*.beast.amplifiedpartners.ai` configured |
| COV-232 | Ollama deployed (12 containers live, 39 tok/s on 8B model) |
| COV-236 | Voice Pipeline deployed (16th container) |
| COV-244 | SearXNG SOP — Beast-native search policy established |
| COV-249 | Foundation deployed: amplified-core, Temporal, Postgres, Redis, Traefik |
| COV-250 | kaizen-worker, chaos-worker, rd-worker planned |
| COV-254 | Finance Engine v1.0 deployed (first core product on Beast) |
| COV-258 | Finance Engine v1.3.1 — death spiral scoring added |
| COV-260 | CH Pipeline deployed (Companies House XBRL parser) |
| COV-267 | LiteLLM budget controls — $50 per-workflow cap, Telegram alert at 80% |
| COV-273 | Cove codebase consolidation (90+ files merged) |
| COV-275 | Intelligence pipeline + Layer 0 deployed; cove-worker rebuilt |

### AI-Native Development Infrastructure Blueprint (Four Layers)

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Layer 1 | Linear | Strategic planning, issue tracking |
| Layer 2 | Cove / Temporal / Agent Orchestration | AI-driven build pipeline |
| Layer 3 | Beads / Git-backed Task Graphs / Memory | Memory and task graph persistence |
| Layer 4 | Quality | Enforcer, Kaizen, quality gates |
| **Above all** | Comet Strategic Command | Executive cockpit for strategic oversight |

**Projects**: M1-M9 modules, spec-driven development with GitHub Spec Kit and AGENTS.md

---

## 6. LiteLLM Proxy & Model Routing

### Architecture

LiteLLM runs as the **single AI gateway** — the only container that holds upstream API keys (Anthropic, OpenAI, xAI). All other containers route through LiteLLM, never directly to providers.

| Setting | Value |
|---------|-------|
| **Internal address** | `litellm:4000` |
| **External access** | Internal only (never exposed externally) |
| **Config file** | `/opt/amplified/apps/litellm/docker-compose.yml` (keys hardcoded — Phase 1 security debt) |
| **Compose** | `/opt/amplified/apps/litellm/docker-compose.yml` |

### Model Routing (Three Tiers)

| Route Name | Model | Provider | Use Case |
|-----------|-------|---------|---------|
| `local/llama3.1-8b` | Llama 3.1 8B | Ollama (Beast) | Fast inference, 39 tok/s warm |
| `local/llama3.1-70b` | Llama 3.1 70B | Ollama (Beast) | Heavy inference, local only |
| `local/nomic-embed` | Nomic Embed | Ollama (Beast) | Embeddings |
| (medium tier) | GPT-4.1-mini | OpenAI | CFO agent, medium-cost tasks |
| (premium tier) | Claude Opus | Anthropic | CEO agent, strategic reasoning |
| (standard tier) | Claude Sonnet | Anthropic | CTO agent, technical decisions |
| (free tier) | Gemini Pro | Google | Nemesis agent, contrarian |
| (fast local) | Llama 3.1:8b | Ollama | COO agent, facilitator agent |

### Budget Controls (COV-267)
- **Per-workflow budget cap**: $50 (default)
- **Alert trigger**: Telegram alert when workflow hits **80% of budget**
- **Observability**: All LLM calls traced through Langfuse (`langfuse.beast.amplifiedpartners.ai`)

### LiteLLM Benefits
- Rate limiting across all upstream providers
- Cost tracking via Langfuse integration
- Redis caching (faster repeat queries, lower cost)
- Model fallback (if Anthropic rate-limited, fallback to alternative)
- **Single rotation point**: Rotating Anthropic/OpenAI keys requires updating **one place only**

### Troubleshooting
```bash
# List registered models
curl http://litellm:4000/models

# Check LiteLLM config
cat /opt/amplified/apps/litellm/config.yaml

# Restart after config change
docker restart litellm
```

---

## 7. MCP Servers & APIs Built or Planned

### Built MCP Servers

| MCP Server | Technology | Purpose | Location |
|-----------|-----------|---------|---------|
| **Telegram MCP** | FastMCP | Telegram bot integration | `/opt/amplified/agent-stack/cove-orchestrator/mcp-servers/telegram/` |
| **NightScout MCP** | FastMCP | Health data pipeline | `/opt/amplified/agent-stack/cove-orchestrator/mcp-servers/nightscout/` |
| **Email MCP** | FastMCP | Email agent integration | `/opt/amplified/agent-stack/cove-orchestrator/mcp-servers/email/` |
| **PostgreSQL MCP** | FastMCP | Database agent access | `/opt/amplified/agent-stack/cove-orchestrator/mcp-servers/postgresql/` |
| **Template MCP** | FastMCP | Reusable MCP template | `/opt/amplified/agent-stack/cove-orchestrator/mcp-servers/template/` |
| **Session Gate MCP** | MCP | `session_start`/`session_end` tools | (strong nudge enforcement — not yet installed) |
| **FalkorDB MCP** | MCP | Graph DB agent access | Port 8000, accessed via amplified-core |

### amplified-core (Fastify MCP Gateway)

- **Port**: 8000
- **URL**: `api.amplifiedpartners.ai`
- **Technology**: Fastify (Node.js)
- **Role**: Main API gateway and MCP bridge
- **Companion**: `amplified-worker` (background processing)

### Product APIs Built

| API | Version | Port | Description |
|-----|---------|------|-------------|
| **Finance Engine** | v1.3.1 | 8700 | Financial analysis API. Death spiral scoring. Companies House integration. |
| **CH Pipeline** | — | 8750 | Companies House XBRL parser — raw UK company financial data |
| **Cove API** | — | 8081 | Cove build pipeline REST API |
| **Voice Pipeline** | — | — | Voice transcription via Deepgram Nova-3 |
| **xAI Phone Agent** | — | internal | xAI Grok-based phone agent |

### anthropic-token-proxy (GitHub repo)
- **Description**: Local reverse proxy for cheaper Anthropic API calls
- **Visibility**: Private
- **Last updated**: March 25, 2026
- **Purpose**: Reduce Anthropic API costs by caching/proxying at the token level

### gatekeeper (GitHub repo)
- **Description**: Conversation-to-Action quality control gate
- **Visibility**: Private
- **Last updated**: March 22, 2026
- **Purpose**: Quality gate that sits between raw conversation and agent actions

### Planned MCP Servers

| MCP Server | Target Stack | Purpose |
|-----------|-------------|---------|
| MCPipe/UnixPipe servers | Cove build targets | Pipe-based inter-agent communication |
| LangGraph workflow MCPs | Cove build targets | Complex workflow orchestration |
| Additional database MCPs | PostgreSQL, FalkorDB | Expanded agent data access |

---

## 8. Security Infrastructure

### Security Principles

1. **No external port mappings** — all external access via Traefik with TLS
2. **Single API gateway** — LiteLLM is the only service with upstream provider API keys
3. **Defence in depth** — P2 tokenisation (data) + key rotation (access) + edge sovereignty (processing)
4. **Chaos-proof, not chaos-free** — keys will get exposed, systems must handle it gracefully
5. **Mechanical enforcement over procedural** — hard blocks where possible, not just nudges

### The 70/30 Enforcement Split

| Category | Type | Examples |
|---------|------|---------|
| ~30% Hard Block | Mechanically enforced | Git pre-commit hooks, expired keys causing auth failure, Docker secrets failing container start |
| ~70% Strong Nudge | AI voluntary compliance | CLAUDE.md instructions, Session Gate MCP, protocol documents |

### Key Rotation Infrastructure

**Rotation script location**: `/opt/amplified/secrets/rotation/rotate-keys.sh`

```bash
# Interactive rotation
./rotate-keys.sh

# Single provider
./rotate-keys.sh --provider anthropic
./rotate-keys.sh --provider openai

# Audit only (no changes)
./rotate-keys.sh --audit

# Auto-rotate self-generated keys only
./rotate-keys.sh --auto
```

**Scheduled auto-rotation** (crontab):
```bash
# Monthly at 3am on the 1st
0 3 1 * * /opt/amplified/secrets/rotation/rotate-keys.sh --auto >> /opt/amplified/secrets/rotation/cron.log 2>&1
```

**What the script does**:
1. Backs up all `.env` files and docker-compose configs (timestamped to `/opt/amplified/secrets/rotation/backups/<timestamp>/`)
2. Auto-generates new self-generated keys (LiteLLM master, Cove)
3. Prompts with exact provider URL for manual keys (Anthropic, OpenAI, GitHub, etc.)
4. Tests new key before applying
5. Updates all `.env` files in one pass
6. Restarts affected containers (LiteLLM, Temporal worker)
7. Verifies health checks pass
8. Logs everything to `/opt/amplified/secrets/rotation/rotation.log`

### Where Secrets Live (Current State — Phase 1)

| Location | Keys | Count |
|----------|------|-------|
| `/opt/amplified/agent-stack/cove-orchestrator/.env` | Cove orchestrator (host-level) | 6 keys |
| `/opt/amplified/agent-stack/cove-orchestrator/docker/.env` | Cove Docker containers | 12 keys |
| `/opt/amplified/apps/litellm/docker-compose.yml` | LiteLLM proxy (HARDCODED — security debt) | 4 keys |
| `/opt/amplified/secrets/pg_password.txt` | Postgres password (Docker secret) | 1 key |

### Key Inventory

| Key | Provider | Auto-Rotatable | Rotation URL |
|-----|---------|---------------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic | No — manual | https://console.anthropic.com/settings/keys |
| `OPENAI_API_KEY` | OpenAI | No — manual | https://platform.openai.com/api-keys |
| `GITHUB_TOKEN` | GitHub | No — manual | https://github.com/settings/tokens |
| `LINEAR_API_KEY` | Linear | No — manual | https://linear.app/amplified-partners/settings/api |
| `TELEGRAM_BOT_TOKEN` | Telegram | No — @BotFather /revoke | Telegram app |
| `BREVO_API_KEY` | Brevo | No — manual | https://app.brevo.com/settings/keys/api |
| `LITELLM_MASTER_KEY` | Self-generated | **Yes — auto** | N/A (openssl rand) |
| `LITELLM_API_KEY` | Self-generated | **Yes — auto** | N/A |
| `COVE_API_KEY` | Self-generated | **Yes — auto** | N/A |
| `POSTGRES_PASSWORD` | Self-generated | Yes (with DB migration) | N/A |
| `TELEGRAM_CHAT_ID` | Telegram | Not a secret | N/A — static |
| `PLAUD_WEBHOOK_SECRET` | Self-generated | — | — |
| `LANGFUSE_*` | Self/Langfuse | — | — |
| `XAI_API_KEY` | xAI | No — manual | — |
| `BRAVE_API_KEY` | Brave | No — manual | — |
| `EXA_API_KEY` | Exa | No — manual | — |

### Security Incident: API Keys Exposed (March 14, 2026)

**What happened**: API keys were accidentally exposed during a session (pasted into chat or similar).

**Response**:
1. Immediate emergency rotation executed
2. Checked provider usage dashboards for unauthorised spend:
   - Anthropic: https://console.anthropic.com/settings/billing
   - OpenAI: https://platform.openai.com/usage
   - GitHub: https://github.com/settings/security-log

**Rotation priority order** (if all keys exposed simultaneously):
1. Anthropic — highest spend risk
2. OpenAI — second highest spend risk
3. GitHub PAT — code access risk
4. Linear — project data access
5. Telegram — bot hijack risk
6. Brevo — email sending risk
7. LiteLLM/Cove — internal only, lower risk but still rotate

### Secrets Manager Roadmap

| Phase | Status | Method |
|-------|--------|--------|
| Phase 1 | ✅ Done | `.env` files with rotation script + timestamped backups |
| Phase 2 | Planned | Docker secrets — files mounted into containers (not visible in `docker inspect`) |
| Phase 3 | Future | Self-hosted Infisical on Beast (free tier, automatic rotation, audit log) |
| Phase 4 | Consider | OpenRouter consolidation — BYOK mode, one fewer key to manage directly |

### Enforcer — Production Health & Compliance

- **Location**: Source at `/opt/amplified/agent-stack/enforcer/`, deployed to `/opt/amplified/apps/enforcer/`
- **URL**: `enforcer.beast.amplifiedpartners.ai`
- **Cadence**: Every **10 minutes**, all 5 checks run **concurrently**, completes in **<30 seconds**
- **Files**: `enforcer.py`, `checks/` (5 modules), `config.yaml`
- **Logging**: JSON structured logging + Prometheus metrics + webhook alerts

**Five Concurrent Health Checks**:
1. **Docker containers** — verifies expected containers are running; session state tracking
2. **Databases** — FalkorDB, PostgreSQL, Redis, Qdrant health
3. **Traefik routing** — confirms key routes are responding
4. **Session hygiene** — baton-pass protocol compliance (BATON-PASS-PROTOCOL.md v1.1)
5. **Security** — fail2ban status, firewall rules

**Additional security measures**:
- fail2ban running (monitored by Enforcer)
- Firewall rules in place
- Git pre-commit hook: commit fails if vault files touched without SESSION-STATE.md staged
- Secrets never committed to GitHub — reference `/opt/amplified/secrets/` only

### P2 Tokenisation (Data Security Layer)

P2 tokenisation runs **at the edge** (on PicoClaw device) before data ever leaves client premises:

```
RAW DATA (at edge device / client premises)
    │
    ▼
P2 TOKENISATION ENGINE (runs on PicoClaw/Beelink N100)
    │
    ├── Raw: "Dave Smith, £45,000 revenue, NE1 3PQ"
    │           ↓
    ├── Token: TOKEN_a7x9k2...
    │
    ├── Mapping stored LOCALLY in encrypted keystore on edge device
    │   (NEVER transmitted to cloud)
    │
    └── Tokenised data → safe to transmit, store, process
    │
    ▼
TOKENISED DATA travels over Tailscale mesh → Beast → FalkorDB (tokens only)
```

**Key properties**:
- Visual format: owner sees `TOKEN_a7x9k2...` — transparent about what's happening
- Breach-safe: intercepted tokens are meaningless without the local private key mapping
- GDPR right to erasure: delete token mapping → data becomes irreversible noise (Article 17 compliant)
- Private key locality: mapping stored ONLY on edge device, never transmitted

**Token lifecycle**:
1. Creation: Raw data → P2 engine (edge) → Token + encrypted mapping
2. Transit: Only tokens travel over Tailscale mesh
3. Storage: FalkorDB stores tokens, not raw data
4. Processing: Rubrics and agents work on tokenised data
5. Display: De-tokenised only on authorised edge device for owner viewing
6. Erasure: Delete mapping → token is permanent noise → GDPR satisfied

### IsolationLayer (Code-Level Enforcement)

- Separates personal data (name, address, contact) from business data (financials, operations, metrics)
- Personal data stored in encrypted, access-controlled namespace
- Business data flows through rubrics and knowledge graph using four-word IDs only
- Any boundary crossing requires explicit Agent Council approval and audit logging

### Tailscale Mesh Networking

- Encrypted transit for all data movement between edge (PicoClaw) and Beast
- Automatic key rotation managed by Tailscale
- Replaces VPN — all devices on mesh communicate securely regardless of network

---

## 9. Voice Pipeline & Transcription Systems

### Voice Pipeline Container

| Setting | Value |
|---------|-------|
| **Container** | `voice-pipeline` |
| **URL** | `voice.beast.amplifiedpartners.ai` |
| **Transcription Engine** | Deepgram Nova-3 |
| **Deployed** | March 11, 2026 (COV-236, 16th container on Beast) |

### xAI Phone Agent

| Setting | Value |
|---------|-------|
| **Container** | `xai-phone-agent` |
| **Model** | xAI Grok |
| **Purpose** | Phone-based voice agent |
| **Access** | Internal only |

### Voice Agent Service

| Setting | Value |
|---------|-------|
| **Container** | `amplified-voice-agent` |
| **Access** | Internal only |
| **GitHub repo** | `voice-ai` (private) |

### NightScout Intelligence Pipeline

- **Container**: `nightscout` (cron) + `nightscout-mcp` (FastMCP server)
- **Purpose**: Health data intelligence pipeline (likely Ewan's personal health data)
- **Technology**: FastMCP server for agent access

### Plaud Voice Recorder Integration

- **Plaud**: Hardware voice recorder used by Ewan for capturing ideas/monologues
- **PLAUD_WEBHOOK_SECRET**: Secret stored in Beast secrets for Plaud webhook integration
- **Vault directory**: `/opt/amplified/vault/14-voice-captures/` — dedicated directory for voice captures
- **Monologue vault**: `/opt/amplified/vault/13-monologue-transcripts/` — processed transcripts

### Transcription-to-Prompt Optimiser (Perplexity Skill)

A dedicated Perplexity skill (`transcription-prompt-optimiser`) was built specifically because Ewan communicates primarily via speech transcription. The skill:

- Intercepts raw voice-transcribed input
- Extracts true intent from messy, fragmented, stream-of-consciousness speech
- Applies Perplexity's five-element prompt framework
- Handles common Geordie accent transcription errors
- Is invisible to the user — they speak naturally, better results appear

**Framework**: EXTRACT → STRUCTURE → OPTIMISE → EXECUTE

**Key design principle**: "The user should NEVER have to change how they speak. The system adapts to them."

### Local Whisper Transcription (PicoClaw)

- Local Whisper model runs on PicoClaw (Beelink N100) for sensitive audio
- Human voices scrubbed at edge after transcription — only text leaves the device
- Acoustic forensics capability planned
- GDPR-safe: raw audio never leaves client premises

### 5.4 Million Word Speech Corpus

- Built from Ewan's speeches, content, and recorded material
- Used in **Amplified Video** product (V5 spec: 6,766 lines, 352KB)
- Used for video generation pipeline
- Status: Likely stored on Mac Mini or iCloud (survives Beast wipes)

---

## 10. Edge Computing & PicoClaw Strategy

### PicoClaw Hardware

| Component | Specification |
|-----------|--------------|
| **Device** | Beelink N100 mini-PC |
| **RAM** | 16GB |
| **Nickname** | "PicoClaw" |
| **Role** | Client-side edge computing node |

### Deployment Scenario

PicoClaw is deployed at **Tier 3+ client premises** (£595/month+). It is the "AI Sidecar" that gives clients local AI processing without cloud dependency.

### What PicoClaw Does

| Function | Detail |
|---------|--------|
| **Local Whisper transcription** | Transcribes audio locally — voices never leave premises |
| **P2 tokenisation** | Tokenises all data before it leaves the building |
| **Acoustic forensics** | Advanced audio analysis capability (planned) |
| **GDPR-safe processing** | Personal identifiers tokenised at source |
| **Local knowledge graph** | FalkorDB runs locally for offline operation |

### Data Sovereignty Architecture

```
CLIENT PREMISES (PicoClaw)                    BEAST (Hetzner)
        │                                           │
        ├── Raw voice → Whisper → text              │
        ├── Raw data → P2 tokenise → tokens         │
        ├── Token mapping stored LOCAL              │
        ├── Local FalkorDB for offline             │
        │                                          │
        └── TOKENISED DATA ──── Tailscale mesh ────►│ FalkorDB stores tokens only
                                                    │ Qdrant stores token embeddings
                                                    │ PostgreSQL stores token records
```

### What NEVER Leaves the Edge

| Data Type | Stays on Edge? | Why |
|-----------|--------------|-----|
| Raw voice recordings | Always | Transcribed locally by Whisper, then scrubbed |
| Personal identifiers | Always | Tokenised at source by P2 |
| Token-to-data mappings | Always | Private key stays on edge device |
| Raw financial data | Always | Tokenised before any transmission |
| Tokenised business metrics | Transmitted (encrypted) | Safe — meaningless without mapping |
| Anonymised patterns | Transmitted (mesh sync) | Federated learning, no individual identifiable |

### Store-and-Forward Logic

PicoClaw operates autonomously when connectivity is lost:

```
ONLINE:  Process locally → sync tokenised results to Beast via Tailscale mesh
OFFLINE: Process locally → cache in local FalkorDB
         When connected again → sync cached results (no data loss)
```

### Integration Layer Patterns

The integration architecture uses four patterns, applied based on client tier:

| Pattern | When Used | Description |
|---------|-----------|-------------|
| **AI Sidecar** | All Tier 3+ | PicoClaw alongside existing client systems |
| **Shadow Mode** | Onboarding phase | AI monitors but doesn't act — learning period |
| **Strangler Fig** | Migration | Gradually replace legacy systems without disruption |
| **Four-stage Trust Ramp** | All clients | Progressive handover from human to autonomous operation |

### The Trust Ramp (Four Stages)

1. **Stage 1**: AI observes, human does everything (Shadow Mode)
2. **Stage 2**: AI recommends, human approves each action
3. **Stage 3**: Human sets policies, AI executes within policies
4. **Stage 4**: Fully autonomous within defined boundaries (with human escalation path)

---

## 11. Technical Failures & Lessons Learned

### The Beast Server Wipes (5 Total)

**What happened**: The Beast was wiped **five times** between March 11 and March 26, 2026.

**What was permanently lost each time**:
- All Docker volumes
- FalkorDB graph databases (`amplified_brain`, `kg_internal`, all `kg_{client_id}`)
- Qdrant vector collections
- PostgreSQL databases and their data
- All container configurations in their running state
- Local Ollama model states (cached inference states)
- Running Cove Temporal workflow state

**The lesson**: The graph databases were **derivative** of source documents, not the source of truth. The source markdown and PDF documents are the real primary asset. If those survive on iCloud or Mac Mini, the graph can be rebuilt. This is now the core data architecture principle.

**Why this is recoverable**: GitHub repositories (13 repos) survived — all code, vault documents, Cove source code, CRM, gatekeeper intact. The framework and architecture survive even when the running state doesn't.

**Consequence**: March 27, 2026 became a full reconstruction day — this knowledge reconstruction document was the first output.

### The FalkorDB CPU Incident

**What happened**: FalkorDB had an external port mapping, and unconstrained external queries pegged the CPU.

**What was learned**: Never expose FalkorDB externally. Use the API layer (amplified-core) or FalkorDB MCP server for all access. All external queries must go through a controlled interface.

**Current state**: FalkorDB has **no external port mapping** by design. Port removed entirely from docker-compose.

### The API Key Exposure Incident (March 14, 2026)

**What happened**: API keys accidentally exposed (pasted into chat or similar during a session).

**Response time**: Immediate — same session

**What was learned**:
1. The rotation script (`rotate-keys.sh`) was built specifically as a result of this
2. LiteLLM as single gateway means only ONE place needs key rotation
3. Provider-specific precautions: set spend limits as safety nets
4. Fine-grained GitHub PATs (not org-level) to limit blast radius

**System improvement**: Emergency rotation procedure now documented with exact priority order.

### The Goodhart's Law Discovery (March 22, 2026)

**Context**: Designing code quality metrics for the Cove build system.

**What happened**: Weighted "Failure Lessons Logged" at 30% — highest single metric. Mid-design, caught the flaw: agents would **manufacture failures** to score points on the highest-weighted metric.

**What was learned**: Any single high-weighted metric creates gaming incentives. Multi-dimensional scoring with cross-validation is required to prevent Goodhart's Law.

**Solution**: Antagonistic Critic agent — armed with data, trained in delivery — cross-validates all failure logs. If a reported failure doesn't have a corresponding fix or lesson, the Critic challenges it.

### The Harness Gap (March 24, 2026)

**What happened**: Agent reliability problems traced to lack of enforced session-start/end protocols. Agents would begin tasks without proper context, or hand off work without baton-passing state.

**What was learned**: Without mechanical enforcement of session protocols, agents skip them.

**Solution**: Anthropic two-agent pattern — Initialiser Agent sets up context before Task Agent begins. Checkpoints between every significant step. Imperative prompts rewritten as conditional decision logic ("if context not loaded, load it; if loaded, proceed to X").

### The 70% Capacity Rule Discovery

**What happened**: Analysis of agent performance showed that agents running at 100% context capacity produced significantly more hallucinations than those running at 70%.

**What was learned**: Reserving 30% of context capacity for error-checking and recalibration dramatically reduces hallucination rate.

**Policy**: All agents now run at **70% capacity**, explicitly reserving 30% for hallucination mitigation.

### LiteLLM Hardcoded Keys (Current Security Debt)

**What is the problem**: LiteLLM config has 4 API keys hardcoded in `docker-compose.yml` — visible in `docker inspect`. This is Phase 1 debt.

**Mitigation**: LiteLLM config is not in GitHub (excluded from version control). Keys are still at risk from anyone with Docker access.

**Planned fix**: Phase 2 — migrate to Docker secrets (files mounted into containers, not visible in `docker inspect`). Phase 3 — Infisical.

### The Fund Pivot (March 2026)

**Not a technical failure, but an architectural decision reversal**:

Ewan designed a financial fund as a product. Mid-conversation realised it could inadvertently mirror the behaviour of institutional investors being criticised by Amplified Partners. Immediately killed the idea.

**Technical lesson**: The AI advocacy mission requires that every product decision be held against the core principles. Products that conflict with principles get killed regardless of commercial value.

---

## 12. Directory Layout & File Paths

### Beast Server Directory Structure

```
/opt/amplified/
├── agent-stack/
│   ├── cove-orchestrator/              # Temporal + Claude agents (Cove Code Factory)
│   │   ├── temporal/
│   │   │   ├── workflows/              # 10 Temporal workflows
│   │   │   ├── activities/             # 12 activity modules
│   │   │   └── workers/main.py
│   │   ├── agents/
│   │   │   ├── configs/agent_registry.py
│   │   │   ├── prompts/                # Layer 0-2 prompts + knowledge_base.md
│   │   │   ├── rubrics/
│   │   │   └── executive/runner.py
│   │   ├── api/                        # FastAPI gateway (port 8081)
│   │   ├── nightscout/
│   │   ├── email_agent/
│   │   ├── mcp-servers/                # telegram, nightscout, email, postgresql, template
│   │   └── docker/docker-compose.yml
│   └── enforcer/                       # Enforcer source (deployed to apps/enforcer)
├── apps/
│   ├── chaos/                          # Chaos department worker
│   ├── enforcer/                       # Enforcer container (health/compliance)
│   ├── funds/
│   ├── journalism/
│   ├── kaizen/                         # Kaizen department worker
│   ├── kids/
│   ├── langfuse/                       # LLM observability
│   ├── litellm/                        # LiteLLM model proxy
│   ├── marketing/
│   ├── ollama/                         # Local LLM inference
│   │   └── docker-compose.yml
│   ├── openclaw-agents/
│   ├── personal/
│   ├── real/
│   └── searxng/                        # Self-hosted search
├── vault/                              # 25 directories (see taxonomy below)
├── traefik/                            # Reverse proxy config
├── compose/                            # Dev tools compose files
├── projects/
├── secrets/                            # All secrets stored here (never in GitHub)
│   └── rotation/
│       ├── rotate-keys.sh
│       ├── rotation.log
│       ├── cron.log
│       └── backups/<timestamp>/
├── logs/
└── docker-compose.yml                  # MAIN: falkordb, postgres, redis, qdrant, portainer, watchtower, minio

/opt/amplified-machine/services/
├── ch-pipeline/                        # Companies House XBRL pipeline (port 8750)
└── finance-engine/                     # Finance Engine (port 8700)
```

### Vault Taxonomy (25 Directories)

```
/opt/amplified/vault/
├── 00-claude-projects/
├── 00-handover/
├── 01-business-strategy/
├── 02-technical-architecture/          (41 files)
├── 03-frameworks-and-rubriks/
├── 04-products/
├── 05-agent-architecture/              (56 files)
├── 06-brand-and-marketing/
├── 07-governance-and-legal/
├── 08-knowledge-management/
├── 09-infrastructure/
├── 10-personal/
├── 11-claude-misc/
├── 11-gemini-misc/
├── 12-claude-short-sessions/
├── 13-monologue-transcripts/
├── 14-voice-captures/
├── 15-principles-library/
├── 16-covered-ai-work/
├── 17-imported-business-docs/
├── 18-research/
├── 19-inbox-raw/
├── 20-staging-archive/
├── 21-infra-research/
├── 22-projects/
└── 23-scripts/
```

### Key Compose Files Reference

| File | Controls |
|------|---------|
| `/opt/amplified/docker-compose.yml` | Core infrastructure: falkordb, postgres, redis, qdrant, portainer, watchtower, minio |
| `/opt/amplified/agent-stack/cove-orchestrator/docker/docker-compose.yml` | Cove stack: temporal, postgres, api, workers |
| `/opt/amplified/apps/ollama/docker-compose.yml` | Ollama local inference |
| `/opt/amplified/apps/litellm/docker-compose.yml` | LiteLLM model proxy |
| `/opt/amplified/apps/langfuse/docker-compose.yml` | Langfuse observability |
| `/opt/amplified/apps/searxng/docker-compose.yml` | SearXNG search |
| `/opt/amplified/apps/enforcer/docker-compose.yml` | Enforcer health checker |
| `/opt/amplified/traefik/` | Traefik reverse proxy |

### GitHub Repositories (13 Repos, March 27, 2026)

| Repository | Description | Visibility | Last Updated |
|-----------|-------------|-----------|-------------|
| `ai-learning-journey-code-repository` | Technical implementations from AI learning journey | **Public** | Mar 26 |
| `vault` | Amplified Partners knowledge vault — structured notes, decisions, documentation | Private | Mar 25 |
| `cove` | Cove Code Factory — Temporal pipeline, agent loop, MCP bridge, Layer 0 laws | Private | Mar 22 |
| `crm` | AI-powered CRM for UK tradespeople | Private | Mar 22 |
| `anthropic-token-proxy` | Local reverse proxy for cheaper Anthropic API calls | Private | Mar 25 |
| `gatekeeper` | Conversation-to-Action quality control gate | Private | Mar 22 |
| `byker-production` | Byker Business Help production | Private | Mar 22 |
| `smb-ai-friction-consultancy` | SMB AI friction reduction — local Ollama/Qwen agentic system | Private | Mar 25 |
| `beautifulgolden` | SMBFrictionreducer | Private | Mar 22 |
| `docs` | Documentation | Private | Mar 25 |
| `librarian-api` | Library/API service | Private | Mar 22 |
| `voice-ai` | Voice AI service | Private | Mar 22 |
| `covered-ai-v2` | Original covered.AI v2 (Nov 2025) | Private | Mar 22 |

---

## 13. Environment Variables & Secrets Inventory

### Complete Key Inventory with Locations

| Variable | Purpose | Location |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | Claude API (Opus, Sonnet) | `/opt/amplified/agent-stack/cove-orchestrator/docker/.env` + LiteLLM only |
| `OPENAI_API_KEY` | OpenAI (GPT-4.1-mini family) | `/opt/amplified/apps/litellm/docker-compose.yml` |
| `XAI_API_KEY` | xAI/Grok (phone agent) | Cove docker env |
| `BRAVE_API_KEY` | Brave search | Cove docker env |
| `EXA_API_KEY` | Exa search | Cove docker env |
| `DATABASE_URL` | PostgreSQL connection string | Multiple services |
| `LITELLM_MASTER_KEY` | LiteLLM proxy admin auth | `/opt/amplified/apps/litellm/docker-compose.yml` |
| `LITELLM_API_KEY` | LiteLLM proxy access key | All agent containers |
| `COVE_API_KEY` | Cove API auth header | Cove consumers |
| `TELEGRAM_BOT_TOKEN` | Telegram bot integration | Cove orchestrator env |
| `TELEGRAM_CHAT_ID` | Telegram destination (static, not secret) | Cove orchestrator env |
| `PLAUD_WEBHOOK_SECRET` | Plaud voice recorder webhook | Beast secrets |
| `pg_password` | PostgreSQL password (Docker secret) | `/opt/amplified/secrets/pg_password.txt` |
| `LANGFUSE_*` | Langfuse observability keys | Langfuse app env |
| `GITHUB_TOKEN` | GitHub API (ewan-dot repos) | Cove orchestrator env |
| `LINEAR_API_KEY` | Linear project management API | Cove orchestrator env |
| `BREVO_API_KEY` | Brevo email marketing | (stored separately) |

---

## 14. Infrastructure Timeline (Chronological)

| Date | Issue | Event |
|------|-------|-------|
| Oct–Nov 2025 | — | Early covered.AI work, initial explorations |
| Jan 17, 2026 | — | Enterprise architecture sessions — zero-friction deployment, central business hub |
| Jan 20, 2026 | — | 46 skills built, 30-role agency blueprint, marketing pipeline designed |
| Mar 10, 2026 | — | Mac Mini amplifiedpartners account created |
| Mar 11, 2026 | COV-229 | DNS wildcard `*.beast.amplifiedpartners.ai` configured |
| Mar 11, 2026 | COV-232 | Ollama deployed (12 containers live, 39 tok/s on 8B model) |
| Mar 11, 2026 | COV-236 | Voice Pipeline deployed (16th container) |
| Mar 12–13, 2026 | — | amplified-core architecture, FalkorDB, business vault designed |
| Mar 13, 2026 | COV-244 | SearXNG SOP: Beast-native search policy established |
| Mar 13, 2026 | COV-249 | Foundation deployed: amplified-core, Temporal, Postgres, Redis, Traefik |
| Mar 13, 2026 | COV-254 | Finance Engine v1.0 deployed (first core product) |
| Mar 13, 2026 | COV-258 | Finance Engine v1.3.1 — death spiral scoring added |
| Mar 13, 2026 | COV-260 | CH Pipeline deployed (Companies House XBRL) |
| Mar 13, 2026 | COV-273 | Cove codebase consolidation (90+ files merged) |
| Mar 13, 2026 | COV-275 | Intelligence pipeline + Layer 0 deployed; cove-worker rebuilt |
| Mar 14, 2026 | — | API keys accidentally exposed → rotated (security incident) |
| Mar 14, 2026 | — | Pricing tiers confirmed |
| Mar 15, 2026 | — | Mac Mini security audit/hardening, Amplified Security protocol designed |
| Mar 16, 2026 | — | AMF v1.0, Build Quality Framework, Master Process Document created |
| Mar 17, 2026 | — | APDS 27-page spec created, Curator Gate spec, mission pivot to AI advocacy |
| Mar 19, 2026 | — | Extraction Department designed |
| Mar 20, 2026 | — | Unified Data Architecture (constitutional document), Integration Layer Architecture |
| Mar 22, 2026 | — | Agent housing architecture, failure documentation discovery, Cove codebase consolidation |
| Mar 24, 2026 | — | Harness gap identified, 70% capacity protocol, AI partnership philosophy refined |
| Mar 24, 2026 | COV-267 | LiteLLM budget controls — $50/workflow cap, Telegram alert at 80% |
| Mar 25, 2026 | — | 5-layer Therapy Suite identity architecture |
| Mar 26, 2026 | — | New MacBook Air purchased, Beast wiped (5th/final time), security incident response |
| Mar 27, 2026 | — | Full knowledge reconstruction day — this document compiled |

---

## Summary: What Survives vs What Was Lost

### Definitely Lost (5 Beast Wipes)
- All Docker volumes — FalkorDB databases (amplified_brain, kg_internal), Qdrant vectors
- PostgreSQL databases in running state
- Container configurations as they were running
- FalkorDB knowledge graph (Graphiti Business Brain) — attempted 5 times, all lost
- Running Cove Temporal workflow state
- Local Ollama model cached states

### Definitely Survives
- **GitHub repositories** (13 repos) — all code, Cove source, CRM, gatekeeper
- **Perplexity custom skills** (10+ skills) — amplified-beast-ops, amplified-key-rotation, transcription-prompt-optimiser, and others
- **This reconstruction document** — frameworks, architecture, decisions, philosophy
- **5.4 million word speech corpus** — if on Mac Mini or iCloud
- **Substack articles** — published content
- **Linear workspace** — basic structure intact
- **Connected services** — Google Calendar, Brevo contacts, Hugging Face, GitHub

### The Core Lesson on Loss
> "The Beast being wiped 5 times is painful but the databases (FalkorDB, Qdrant) were always **derivative** of source documents. The source documents (markdown, PDFs) are the primary asset. If those survive on iCloud or the Mac Mini, the knowledge graph can be rebuilt. The graph was an index, not the knowledge itself."

---

*Compiled from: amplified-beast-ops skill (v1), amplified-key-rotation skill (v2.0), transcription-prompt-optimiser skill (v1.0), amplified-partners-knowledge-reconstruction.md, Linear workspace data, GitHub repository metadata. Extraction date: March 27, 2026.*

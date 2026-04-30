---
title: Infrastructure manifest — Amplified Partners Core Server
date: 2026-04-30
version: 1
status: authoritative now
signed-by: Devon | devin-66aa3ce48c7e407f8ad9bf066541b604
---

<!-- markdownlint-disable-file MD013 -->

# Infrastructure Manifest

Single source of truth for what is running on Amplified Partners infrastructure. If it is not listed here, we do not know about it. If it is listed here, this is what it does.

**Server:** `amplified-core` — Hetzner AX162-R (`135.181.161.131`)
**OS:** Ubuntu 24.04.4 LTS (Noble Numbat)
**CPU:** AMD EPYC 9454P 48-Core (96 threads)
**RAM:** 252 GB
**Disk:** 1.8 TB RAID (`/dev/md2`), 170 GB used (11%)

---

## How to read this

- **Running** = container is up and healthy (or up without healthcheck).
- **Paused** = intentionally stopped; data preserved; restart command provided.
- **Stopped** = exited and not expected to run (init containers, deprecated services).
- Each entry says what it does in plain language. If you don't know what something means, the entry is wrong — fix it.

---

## Network topology

All application containers run on `amplified-net` (Docker bridge). Traefik handles external HTTPS routing via `api.amplifiedpartners.ai`. Internal services communicate by container name on the Docker network.

| Network | Purpose |
|---------|---------|
| `amplified-net` | Primary application network (all services) |
| `traefik-public` | Traefik edge routing |
| `docker_default` | Docker default (Temporal, some Postgres) |
| `amplified_default` | Legacy default network |

---

## Core platform services

These are shared infrastructure that other services depend on.

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **traefik** | `traefik:latest` | Running | Reverse proxy + TLS. Routes `api.amplifiedpartners.ai` to backend services. Ports 80/443 exposed to internet. |
| **postgres** | `postgres:16-alpine` | Running | Primary PostgreSQL database. DB: `amplified_machine`. Used by amplified-core, finance-engine, ch-pipeline, marketing engine. Internal port 5432. |
| **docker-postgres-1** | `postgres:16-alpine` | Running | Secondary PostgreSQL instance. Exposed on host port 5432. Used by Temporal and other stacks. |
| **redis** | `redis:7-alpine` | Running | Shared cache and message broker. Internal port 6379. |
| **minio** | `minio/minio:latest` | Running | S3-compatible object storage. Internal port 9000. |
| **minio-init** | `minio/mc:latest` | Stopped | One-time bucket initialisation. Ran 2026-03-11. Not needed again unless buckets change. |

## AI / ML services

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **ollama** | `ollama/ollama:latest` | Running | Local LLM inference server. Hosts llama3.1-8b and other models. Internal port 11434. |
| **litellm** | `ghcr.io/berriai/litellm:main-latest` | Running | LLM proxy — unified API for local (Ollama) and remote (OpenAI, Anthropic) models. Internal port 4000. |
| **langfuse** | `langfuse/langfuse:latest` | Running | LLM observability — traces, costs, prompt versioning. |

## Knowledge and search

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **falkordb** | `falkordb/falkordb:latest` | Running | Graph database. 9,000 nodes across 4 graphs. Stores entity relationships from vault content. Internal port 6379. |
| **qdrant** | `qdrant/qdrant:latest` | Running | Vector database. 57,434 embeddings (384-dim). Semantic search over vault content. Internal ports 6333-6334. |
| **clickhouse** | `clickhouse/clickhouse-server:latest` | Running | Columnar analytics database. Internal ports 8123 (HTTP), 9000 (native). |
| **searxng** | `searxng/searxng:latest` | Running | Metasearch engine for research agents. Internal port 8080. |

## Amplified Machine (core product)

Source: `/opt/amplified-machine/` — `docker-compose.yml` + `docker-compose.services.yml`

| Container | Image | Status | Route | Purpose |
|-----------|-------|--------|-------|---------|
| **amplified-core** | `amplified-machine-amplified-core` | Running (healthy) | `api.amplifiedpartners.ai/` | Main API gateway. Vault ingestion, knowledge graph queries, orchestration. Memory limit 2 GB. |
| **amplified-worker** | `amplified-machine-amplified-worker` | Running | — | Background worker for async tasks (indexing, embeddings, heavy processing). Memory limit 4 GB. Depends on amplified-core healthy. |
| **finance-engine** | `amplified-machine-finance-engine` | Running (healthy) | `/api/v1/finance` | Financial analytics — CLV, cash flow, valuation scoring. Port 8700. |
| **ch-pipeline** | `amplified-machine-ch-pipeline` | **Paused** | `/api/v1/ch` | Companies House new-company registration pipeline. Monitors CH API for newly registered UK companies. **Original intent: offer three months free to brand-new companies as go-to-market channel.** Data preserved: 9,740 filings from 9,707 companies (BS dates 2019-03-31 → 2026-03-11). Paused 2026-04-30 by Ewan — not ready for production use yet. Port 8750. |

**To restart ch-pipeline:**
```bash
cd /opt/amplified-machine
docker compose -f docker-compose.yml -f docker-compose.services.yml up -d ch-pipeline
```

## Marketing engine

Source: `/opt/amplified/apps/marketing/`

| Container | Image | Status | Route | Purpose |
|-----------|-------|--------|-------|---------|
| **amplified-marketing-engine** | `marketing-marketing-engine` | Running | `/api/v1/marketing` (via port 8000) | Content generation pipeline. Research → generate → evaluate → queue → learn. Three-avatar synthetic evaluator (Bob, Lisa, Marcus). API auth: admin/pipeline/readonly tiers. v0.4.0. |
| **kaizen-optimizer** | `kaizen-kaizen` | Running (healthy) | — | Continuous improvement loop. Analyses feedback patterns → generates learned preferences → feeds back into content generation. |

## Cove (workflow orchestration)

Source: `/root/cove-repo/infrastructure/`

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **cove-api** | `cove-api:latest` | Running (healthy) | Cove API server. Port 8081 exposed to host. |
| **cove-translator** | `cove-translator:latest` | Running | Translation layer. Port 8092→8090. |
| **cove-temporal** | `temporalio/auto-setup:latest` | Running | Temporal workflow engine for Cove. Port 7233 (localhost only). |
| **cove-temporal-ui** | `temporalio/ui:latest` | Running | Temporal web UI. Port 8233 (localhost only). |
| **cove-postgres** | `timescale/timescaledb-ha:pg15-latest` | Running | Cove-specific TimescaleDB. Port 5433 (localhost only). |
| **cove-worker** | `cove-worker:latest` | Running | Primary Cove workflow worker. |
| **cove-worker-alpha** | `cove-worker:latest` | Running | Scaled worker instance. |
| **cove-worker-bravo** | `cove-worker:latest` | Running | Scaled worker instance. |
| **cove-worker-charlie** | `cove-worker:latest` | Running | Scaled worker instance. |
| **cove-worker-delta** | `cove-worker:latest` | Running | Scaled worker instance. |
| **docker-temporal-1** | `temporalio/auto-setup:1.24` | Running | Secondary Temporal instance (Docker default stack). |

## Agent services

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **openclaw-agents** | `openclaw-agents-openclaw-agents` | Running (healthy) | OpenClaw agent platform. Note-taking, recording, coordination. Port 8100. Source: `/opt/amplified/apps/openclaw-agents/` |
| **enforcer** | `enforcer-enforcer` | Running (healthy) | Codebase health monitor and automated build circuit breaker. Port 8000. Source: `/opt/amplified/apps/enforcer/` |
| **amplified-knowledge-mcp** | `amplified-knowledge-mcp-amplified-knowledge-mcp` | Running (healthy) | MCP server for AI agents to query knowledge base. Source: `/opt/amplified/apps/amplified-knowledge-mcp/` |

## Voice services

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **amplified-voice-agent** | `amplified-voice-agent-voice-agent` | Running | Voice AI agent. Port 8080 exposed to host. Source: `/opt/amplified-voice-agent/` |
| **xai-phone-agent** | `xai-phone-agent-xai-phone-agent` | Running | xAI-powered phone agent. Internal port 8080. Source: `/opt/xai-phone-agent/` |
| **voice-pipeline** | `voice-pipeline-voice-pipeline` | **Stopped** | Voice processing pipeline. Exited 6 weeks ago. Source: `/root/services/voice-pipeline/` |

## Dashboards and tools

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **portainer** | `portainer/portainer-ce:latest` | Running | Docker management GUI. Ports 8000, 9000, 9443. |
| **amplified-code-server** | `lscr.io/linuxserver/code-server:latest` | Running | VS Code in the browser. Port 8443. |
| **nexus-dashboard** | `nexus-dashboard-dashboard` | Running | Nexus trading/analytics dashboard. Internal port 8090. Source: `/opt/nexus/dashboard/` |
| **watchtower** | `containrrr/watchtower` | Running (healthy) | Automatic Docker image updates. Watches for new image tags and auto-pulls. |

---

## Scheduled jobs (crontab)

| Schedule | What | Added by |
|----------|------|----------|
| `0 3 * * *` | Amplified Core backup (`/opt/amplified/backups/amplified-core-backup.sh`) | — |
| `0 3 * * *` | Vault rsync to `/mnt/vault-backup/vault/` | — |
| `0 3 1 * *` | Secret key rotation (`/opt/amplified/secrets/rotation/rotate-keys.sh`) | — |
| `0 4 * * *` | Marketing content pipeline run (daily, 6am CEST) | Devon, 2026-04-29 |
| `0 5 * * 0` | Internal Kaizen — weekly (Sunday 5am UTC). Analyses Ewan's feedback patterns. | Devon, 2026-04-30 |
| `0 5 1 * *` | External Kaizen — monthly (1st of month, 5am UTC). Analyses engagement metrics. | Devon, 2026-04-30 |
| `0 8 * * 1` | Weekly learning report email to Ewan (Monday 8am UTC). | Devon, 2026-04-30 |

---

## Compose file locations

| Stack | Path | Containers |
|-------|------|------------|
| Amplified Machine (core) | `/opt/amplified-machine/docker-compose.yml` + `docker-compose.services.yml` | amplified-core, amplified-worker, finance-engine, ch-pipeline |
| Traefik | `/opt/amplified/traefik/docker-compose.yml` | traefik |
| Marketing | `/opt/amplified/apps/marketing/docker-compose.marketing.yml` | amplified-marketing-engine |
| Kaizen | `/opt/amplified/apps/kaizen/docker-compose.yml` | kaizen-optimizer |
| Enforcer | `/opt/amplified/apps/enforcer/docker-compose.yml` | enforcer |
| LiteLLM | `/opt/amplified/apps/litellm/docker-compose.yml` | litellm |
| Langfuse | `/opt/amplified/apps/langfuse/docker-compose.yml` | langfuse |
| Ollama | `/opt/amplified/apps/ollama/docker-compose.yml` | ollama |
| SearXNG | `/opt/amplified/apps/searxng/docker-compose.yml` | searxng |
| OpenClaw Agents | `/opt/amplified/apps/openclaw-agents/docker-compose.yml` | openclaw-agents |
| Knowledge MCP | `/opt/amplified/apps/amplified-knowledge-mcp/docker-compose.yml` | amplified-knowledge-mcp |
| Cove | `/root/cove-repo/infrastructure/docker-compose.yml` | cove-api, cove-translator, cove-temporal, cove-temporal-ui, cove-postgres, cove-worker-* |
| Voice Agent | `/opt/amplified-voice-agent/docker-compose.yml` | amplified-voice-agent |
| Voice Pipeline | `/root/services/voice-pipeline/docker-compose.yml` | voice-pipeline |
| xAI Phone Agent | `/opt/xai-phone-agent/docker-compose.yml` | xai-phone-agent |
| Nexus Dashboard | `/opt/nexus/dashboard/docker-compose.yml` | nexus-dashboard |
| Base infra | `/opt/amplified/docker-compose.yml` | postgres, redis, falkordb, qdrant, clickhouse, minio, portainer, amplified-code-server |

---

## Changelog

### v1 — 2026-04-30

Infrastructure manifest created. Full audit of all 40 containers on Amplified Core server. ch-pipeline paused (data preserved). voice-pipeline noted as stopped (6 weeks).

Signed-by: Devon | 2026-04-30 | devin-66aa3ce48c7e407f8ad9bf066541b604

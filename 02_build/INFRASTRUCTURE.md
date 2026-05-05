---
title: Infrastructure manifest — Amplified Partners Core Server
date: 2026-05-04
version: 3
status: authoritative now
signed-by:
  - Devon | 2026-04-30 | devin-66aa3ce48c7e407f8ad9bf066541b604
  - Devon-6ca5 | 2026-05-03 | devin-6ca57553eefe4806b613070325964703
  - Devon-3adb | 2026-05-04 | devin-3adb98db92e24792ab959ea658cc34bc
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
| **litellm** | `ghcr.io/berriai/litellm:main-latest` | Running | LLM proxy — unified API for local (Ollama) and remote (OpenAI, Anthropic) models. Internal port 4000. Routes by `simple-shuffle` with failover chains; **does not** classify by cost. |
| **token-proxy** | `amplified/token-proxy:latest` (built locally from `Amplified-Partners/cost-tools`) | Running (healthy) | Anthropic-only reverse proxy. Sonnet→Haiku model-layer routing on extractive/classification prompts; prompt caching; semantic similarity cache (Qdrant `llm_cache`, 0.95, 24h TTL); native context compaction; daily $100 budget circuit-breaker; per-agent cost log. Container port 8088 (host-bound to `127.0.0.1:8088` for diagnostics; agents reach it via DNS name `token-proxy:8088` on `amplified-net`). Compose file: `/opt/amplified/apps/cost-tools/docker-compose.yml`. RUNBOOK: `cost-tools/RUNBOOK.md`. Linear: AMP-28. |
| **langfuse** | `langfuse/langfuse:latest` | Running | LLM observability — traces, costs, prompt versioning. |

**To wire an agent through the token-proxy:**
```bash
# inside the agent's container, on amplified-net:
export ANTHROPIC_BASE_URL=http://token-proxy:8088
```
Reversal: unset the env var. 30 seconds, no restart of the proxy needed.

**Self-heal layers for token-proxy:**
1. Docker `restart: always` + `healthcheck: /proxy/stats` every 30s (handles ~90% of transient failures).
2. Optional Temporal workflow checking `/proxy/stats` every 5 min and running `docker compose restart token-proxy` on 2 consecutive failures (pattern matches existing `cove-*` self-heal).
3. RUNBOOK at `cost-tools/RUNBOOK.md` — 5 failure modes (F1–F5), per-failure 30-second fix, escalation rule (2 attempts → rollback → page Ewan via Telegram).

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

**Voice/telephony stack not finalised.** Active subscriptions: Deepgram, Twilio, Telnyx, Retell, Vapi, Cartesia, Eleven Labs. Current deployment uses Deepgram (STT / noise suppression) + Twilio (UK number, WhatsApp API access) + Anthropic. Final provider choices TBD.

| Container | Image | Status | Purpose |
|-----------|-------|--------|---------|
| **amplified-voice-agent** | `amplified-voice-agent-voice-agent` | Running | Voice AI agent. Currently wired: Twilio (+441917433558), Deepgram STT, Anthropic conversation, FalkorDB knowledge. Port 8080 exposed to host. Routes to `voice.beast.amplifiedpartners.ai`. Source: `/opt/amplified-voice-agent/` |
| **xai-phone-agent** | `xai-phone-agent-xai-phone-agent` | Running | xAI/Grok voice experiment (voice: "Sal"). No Twilio — uses xAI native voice API. Routes to `phone.beast.amplifiedpartners.ai`. Source: `/opt/xai-phone-agent/` |
| **voice-pipeline** | `voice-pipeline-voice-pipeline` | **Stopped** | Voice processing pipeline (Deepgram + LiteLLM + Redis). Exited 6 weeks ago. Source: `/root/services/voice-pipeline/` |

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
| Langfuse | `/opt/amplified/apps/langfuse/docker-compose.yml` | langfuse, minio-init |
| Ollama | `/opt/amplified/apps/ollama/docker-compose.yml` | ollama |
| SearXNG | `/opt/amplified/apps/searxng/docker-compose.yml` | searxng |
| OpenClaw Agents | `/opt/amplified/apps/openclaw-agents/docker-compose.yml` | openclaw-agents |
| Knowledge MCP | `/opt/amplified/apps/amplified-knowledge-mcp/docker-compose.yml` | amplified-knowledge-mcp |
| Cove (primary) | `/root/cove-repo/infrastructure/docker-compose.yml` | cove-api, cove-translator, cove-temporal, cove-temporal-ui, cove-postgres, cove-worker-* |
| Cove (orchestrator) | `/opt/amplified/agent-stack/cove-orchestrator/docker/docker-compose.yml` | docker-postgres-1, docker-temporal-1 |
| Voice Agent | `/opt/amplified-voice-agent/docker-compose.yml` | amplified-voice-agent |
| Voice Pipeline | `/root/services/voice-pipeline/docker-compose.yml` | voice-pipeline |
| xAI Phone Agent | `/opt/xai-phone-agent/docker-compose.yml` | xai-phone-agent |
| Nexus Dashboard | `/opt/nexus/dashboard/docker-compose.yml` | nexus-dashboard |
| Base infra | `/opt/amplified/docker-compose.yml` | postgres, redis, falkordb, qdrant, clickhouse, minio, portainer, amplified-code-server |
| Cost-tools (token-proxy) | `/opt/amplified/apps/cost-tools/docker-compose.yml` | token-proxy |
| _(standalone)_ | `docker run` | watchtower |

---

## Changelog

### v3 — 2026-05-04

- Corrects the v2 changelog entry below: the v2 entry stated "No changes to existing rows; all edits are additive" but the same entry also clarified the **litellm** row's behaviour text two bullets above. The litellm clarification was additive in semantic effect (no behavioural change to the running container), but the row text was edited, so the v2 line as written was self-contradictory. The contradictory line has been removed from the v2 entry; the Linear reference (AMP-28) is preserved on its own line.
- No changes to any container row, the Compose-file-locations table, or the self-heal / wiring instructions added in v2. This is a bibliography-integrity correction to the v2 changelog only. Companion follow-up to PR #39.
- Frontmatter `date` advanced to 2026-05-04 to match this entry and the new `signed-by` line for Devon-3adb.

Signed-by: Devon-3adb | Devin (Cognition AI) | 2026-05-04 | session `devin-3adb98db92e24792ab959ea658cc34bc`

### v2 — 2026-05-03

- Added **token-proxy** container row under § AI / ML services: Anthropic-only reverse proxy on `amplified-net`, Sonnet→Haiku model-layer routing on extractive/classification prompts, prompt caching, semantic similarity cache (Qdrant `llm_cache`, 0.95, 24h TTL), native context compaction, daily $100 budget circuit-breaker. Container reachable as `token-proxy:8088` on `amplified-net`; host-bound to `127.0.0.1:8088` for diagnostics. Compose file at `/opt/amplified/apps/cost-tools/docker-compose.yml`. RUNBOOK in the `cost-tools` repo.
- Added the cost-tools stack to the **Compose file locations** table for symmetry with every other compose-managed container.
- Clarified the **litellm** row: routes by `simple-shuffle` with failover chains; **does not** classify by cost. Cost-tier classification is the proxy's job (per `00_authority/TAXONOMY.md` v2/v3 lock).
- Documented the **self-heal layers** for token-proxy (Docker `restart: always` + healthcheck on `/proxy/stats`; Temporal workflow check every 5 min; RUNBOOK escalation rule — 2 attempts → rollback → page Ewan via Telegram).
- Added agent-wiring instructions: `ANTHROPIC_BASE_URL=http://token-proxy:8088` on agents that hit Anthropic directly; reversible in 30 sec by unsetting the env var.
- Linear: AMP-28.

Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### v1 — 2026-04-30

Infrastructure manifest created. Full audit of all 40 containers on Amplified Core server. ch-pipeline paused (data preserved). voice-pipeline noted as stopped (6 weeks).

Signed-by: Devon | 2026-04-30 | devin-66aa3ce48c7e407f8ad9bf066541b604

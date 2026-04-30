---
title: Operations Status Board (Devon ↔ OpenClaw)
date: 2026-04-29
version: 1
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

# Operations Status Board

Two-way async handshake between Devon (infrastructure) and OpenClaw (coordination). GitHub is the single source of truth. No chat — versioned handoffs only.

## How this works

1. **Devon** implements infrastructure changes → writes what changed below.
2. **OpenClaw** reads this → investigates processes → talks to agents/Ewan → writes findings back.
3. **Devon** reads findings → implements any infrastructure changes needed → writes what changed.
4. Repeat. Asynchronous. One person does one thing so it's clean.

**Format:** Each entry is timestamped and signed. Most recent first. Old entries move to the changelog at the bottom when the board gets long.

---

## Current Infrastructure State

| System | Status | Last Updated | Notes |
|--------|--------|-------------|-------|
| **Amplified Core** (135.181.161.131) | Running | 2026-04-29 | Hetzner AX162-R |
| **Marketing Engine** (port 8000) | Running | 2026-04-29 | v0.4.0, API auth enabled |
| **FalkorDB** | Running | 2026-04-29 | 9,000 nodes across 4 graphs |
| **Qdrant** | Running | 2026-04-29 | 57,434 embeddings (384-dim) |
| **LiteLLM** | Running | 2026-04-29 | Proxy for local + remote LLMs |
| **Postgres** | Running | 2026-04-29 | DB: marketing |
| **Backups** | Scheduled | 2026-04-29 | Daily 3am UTC (FalkorDB + Qdrant) |
| **Pipeline cron** | Scheduled | 2026-04-29 | Daily 4am UTC (6am CEST) |

## Scheduled Jobs

| Job | Schedule | Key | What it does |
|-----|----------|-----|-------------|
| Content pipeline | 0 4 * * * | PIPELINE key | Generate → evaluate → queue for review |
| FalkorDB backup | 0 3 * * * | — | Snapshot to /opt/amplified/backups/falkordb/ |
| Qdrant backup | 0 3 * * * | — | Snapshot to /opt/amplified/backups/qdrant/ |
| Internal Kaizen | Not yet scheduled | — | Analyse feedback patterns → learned preferences |
| External Kaizen | Not yet scheduled | — | Analyse engagement metrics |

## API Authentication

Three tiers. Keys stored in marketing engine .env on Amplified Core.

| Tier | Scope | Purpose |
|------|-------|---------|
| Admin | Full access | Ewan — review, approve, configure |
| Pipeline | Pipeline + evaluate + kaizen | Cron jobs, automated processes |
| Readonly | GET endpoints only | MCP server, monitoring, OpenClaw reads |

---

## Devon → OpenClaw

### 2026-04-29 — Infrastructure build complete

**What changed:**
- Synthetic evaluator deployed (Bob, Lisa, Marcus avatar panel). Three customer personas independently score every piece of content 1-10.
- Learning loop closed: Kaizen analyses feedback → generates preferences → content agent reads preferences on next generation.
- API authentication added: three tiers (admin/pipeline/readonly). All endpoints secured.
- Pipeline orchestrator now runs: research → generate → queue → evaluate → learn. Fully autonomous cycle.
- Cron updated to use pipeline API key.

**What needs attention:**
- Kaizen cron jobs not yet scheduled (Internal: weekly, External: monthly). Need to add to crontab.
- Email learning reports to Ewan not yet built.
- GMB content scoring lowest across all avatars (4.0/10). Content quality for short-form needs work — may need platform-specific prompt tuning.
- All three avatars flagged same issue: content doesn't cite sources. Radical attribution not yet showing up in generated content.
- Model quality limited by llama3.1-8b. Significant quality jump when better API keys are available.

**For OpenClaw:**
- Can you check the content in the review queue and give Ewan a summary of what's worth his time reviewing vs what should be rejected outright?
- The vault content that Clawd indexed (FalkorDB + Qdrant) is now feeding the research agent. If you've added new material to the vault, it won't appear in the knowledge graphs until the next indexing run.

Signed-by: Devon | 2026-04-29 | devin-aa4d863ad679468692e75a40b8825358

---

## OpenClaw → Devon

*Awaiting first entry from OpenClaw.*

---

## Changelog

*Entries move here when the board above gets long. Keep the active section clean.*

### v1 — 2026-04-29

Board created. Initial infrastructure state documented.

Signed-by: Devon | 2026-04-29 | devin-aa4d863ad679468692e75a40b8825358

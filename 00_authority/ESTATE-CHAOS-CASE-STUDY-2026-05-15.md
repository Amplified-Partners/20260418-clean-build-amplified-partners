---
title: "Estate Chaos → Order: The Amplified Partners Repository Cleanup Case Study"
date: 2026-05-15
version: 1
status: authoritative now
signed-by:
  - Devon-8da1 | 2026-05-15 | devin-8da1981ce177481da3fe1d2b40e7fade
---

<!-- markdownlint-disable-file MD013 -->

# Estate Chaos → Order

**The Amplified Partners Repository Cleanup & Canonical Data Architecture Migration**

Date: 2026-05-15
Architect: Ewan Bramley
Executor: Devon-8da1

---

## 1. What We Found

45 repositories across two GitHub organisations (`Amplified-Partners` and `ewan-dot`). 7 months of AI-native compound engineering, 4+ AI agents, one non-coder architect — and the estate had grown organically. The chaos was the cost of speed, not negligence.

### The Numbers

| Metric | Before | After (Target) |
|--------|--------|----------------|
| **Repositories** | 45 | 27 |
| **Duplicate repos** | 7 (ewan-dot stubs) | 0 |
| **Stub/empty repos** | 5 | 0 |
| **Dormant repos** | 6 | 0 (archived) |
| **Active repos** | 27 | 27 |
| **Database engines** | 3 (PostgreSQL + FalkorDB + Qdrant) | 1 (PostgreSQL + AGE + pgvector) |
| **Local storage (Beast)** | ~330 GB | ~130 GB target |
| **Data architecture status** | Fragmented | Canonical |

---

## 2. Full Repository Classification

### 2.1 ewan-dot Organisation (7 Repos) — ALL STUBS, DELETE

Every repo in `ewan-dot` is an acknowledged stub created as a placeholder for Devin snapshot builds. Each contains only a `README.md` marking it as "Safe to delete once stale entry is removed from Devin settings."

| # | Repo | Description | Last Updated | Content | Verdict |
|---|------|-------------|-------------|---------|---------|
| 1 | `ewan-dot/voice-ai` | Stub — Devin snapshot placeholder | 2026-05-11 | README only | **DELETE** |
| 2 | `ewan-dot/docs` | Stub — Devin snapshot placeholder | 2026-05-11 | README only | **DELETE** |
| 3 | `ewan-dot/beautifulgolden` | Stub — Devin snapshot placeholder | 2026-05-11 | README only | **DELETE** |
| 4 | `ewan-dot/librarian-api` | Stub — Devin snapshot placeholder | 2026-05-11 | README only | **DELETE** |
| 5 | `ewan-dot/covered-ai-v2` | Stub — Devin snapshot placeholder | 2026-05-11 | README only | **DELETE** |
| 6 | `ewan-dot/visual-polish-system` | Stub — Devin snapshot placeholder | 2026-05-11 | README only | **DELETE** |
| 7 | `ewan-dot/the-amplified-method` | Fork — methodology docs + React UI | 2026-05-07 | Full fork of Amplified-Partners/the-amplified-method | **DELETE** (attribution preserved — original in AP org) |

**Metadata comparison:** `ewan-dot/the-amplified-method` is the only repo with substantive content. It is a direct fork of `Amplified-Partners/the-amplified-method`. All commits and attribution are preserved in the Amplified-Partners canonical version. No unique content at risk.

### 2.2 Amplified-Partners Stub Repos (5 Repos) — DELETE

| # | Repo | Description | Last Updated | Content | Verdict |
|---|------|-------------|-------------|---------|---------|
| 8 | `amplified-hermes-team` | Agent orchestration framework — mostly scaffolding, Dockerfile, Makefile, role.md | 2026-05-07 | Minimal scaffolding | **DELETE** — concept absorbed into agent-comms and devon-memory |
| 9 | `openclaw` | Stub — Devin snapshot placeholder | 2026-05-04 | README only | **DELETE** |
| 10 | `beautifulgolden` | Contains only `.gitattributes` | 2026-05-10 | `.gitattributes` only | **DELETE** |
| 11 | `originals` | Archival preservation copy of business docs | 2026-05-04 | Documents organised by source repo | **DELETE** — content absorbed into corpus-raw and vault |
| 12 | `canonical-candidate` | Curated synthesis input pile | 2026-05-04 | Pre-processed documents | **DELETE** — function absorbed into the canonical ingestion pipe |

### 2.3 Dormant Repos (6 Repos) — ARCHIVE

These repos contain real code and historical value but are not part of the active build. Archive preserves attribution and history while removing them from active estate.

| # | Repo | Description | Last Updated | Language | Verdict | Reason |
|---|------|-------------|-------------|----------|---------|--------|
| 13 | `amplified-website` | Next.js 15 marketing site | 2026-05-10 | TypeScript | **ARCHIVE** | Superseded by `amplified-site` |
| 14 | `voice-ai` | Voice pipeline (Whisper/Claude/Cartesia) | 2026-04-24 | Python | **ARCHIVE** | Feature absorbed into CRM voice bridge |
| 15 | `visual-polish-system` | UI/UX scoring engine | 2026-05-10 | Python | **ARCHIVE** | Concept parked; `visual-polish-systemdot` is the active fork if needed |
| 16 | `smb-ai-friction-consultancy` | Stub — Devin snapshot placeholder | N/A | None | **ARCHIVE** | Empty stub, but name has historical significance |
| 17 | `beautiful-and-golden` | Ghost Sidecar — legacy system observer | 2026-05-10 | Python | **ARCHIVE** | Parked (per description). Concept sound, not active. |
| 18 | `beast-code-export` | Full code extraction from Beast | 2026-05-04 | TypeScript | **ARCHIVE** | Historical snapshot. All active code lives in dedicated repos now. |

### 2.4 Active Repos (27 Repos) — KEEP

#### Governance & Spine (4)

| # | Repo | Purpose | Status |
|---|------|---------|--------|
| 19 | `clean-build` | Governed agent workspace. Authority rules, specs, build code. THIS repo. | **Active — Build** |
| 20 | `ground-truth` | The Portable Spine. Canonical operating context for all agents. | **Active — Governance** |
| 21 | `portable-spine` | Minimal portable spine template + compound engineering skills | **Active — Governance** |
| 22 | `devon-memory` | Devon's terminal repo — working memory, baton passes | **Active — Agent Memory** |

#### Core Products (3)

| # | Repo | Purpose | Stack | Status |
|---|------|---------|-------|--------|
| 23 | `crm` | Core CRM — 50+ endpoints, Business Brain, Interview Engine | Python/FastAPI, Next.js, PostgreSQL | **Active — Product** |
| 24 | `covered-ai-v2` | AI phone answering for UK service businesses | TypeScript, Vapi.ai, Twilio | **Active — Product** |
| 25 | `amplified-site` | Public-facing website & visual polish system | TypeScript, React, Express | **Active — Product** |

#### Infrastructure & Tooling (8)

| # | Repo | Purpose | Status |
|---|------|---------|--------|
| 26 | `amplified-machine` | Beast server deployment configs, Docker compose stacks | **Active — Infra** |
| 27 | `marketing-engine` | Automated content pipeline — pillar-to-atom, Kaizen loops | **Active — Marketing** |
| 28 | `amplified-knowledge-mcp` | MCP server for AI agent access to knowledge graph | **Active — Infra** |
| 29 | `anthropic-token-proxy` | Local reverse proxy — prompt caching, semantic caching | **Active — Infra** |
| 30 | `cost-tools` | API cost tracking and optimisation utilities | **Active — Infra** |
| 31 | `mission-control` | Enterprise governance dashboard | **Active — Dashboard** |
| 32 | `enforcer` | Infrastructure health monitoring and compliance | **Active — Infra** |
| 33 | `.github` | Org-level defaults: Copilot instructions, community health | **Active — Config** |

#### Research & Knowledge (6)

| # | Repo | Purpose | Status |
|---|------|---------|--------|
| 34 | `perplexity-research` | Research intake from Perplexity — automated governance | **Active — Research** |
| 35 | `vault` | Curated knowledge store (4,891 markdown files) | **Active — Knowledge** |
| 36 | `corpus-raw` | Raw research corpus (~10k files) | **Active — Data Lake** |
| 37 | `pudding-core` | Core PUDDING technique (Swanson ABC model) | **Active — Research** |
| 38 | `pudding-testing` | PUDDING test harness — taxonomy validation | **Active — Research** |
| 39 | `the-amplified-method` | The Amplified Method — methodology docs | **Active — Docs** |

#### Agent Infrastructure (4)

| # | Repo | Purpose | Status |
|---|------|---------|--------|
| 40 | `agent-comms` | Agent coordination hub, handover files | **Active — Comms** |
| 41 | `openclaw-knowledge` | OpenClaw knowledge base for agent team | **Active — Knowledge** |
| 42 | `openclaw-claw` | OpenClaw framework — agent deployment, Beast integration | **Active — Agent** |
| 43 | `dotfiles` | Multi-Mac dotfiles for Mirror (Claude on Mac) | **Active — Config** |

#### Other Active (2)

| # | Repo | Purpose | Status |
|---|------|---------|--------|
| 44 | `plumb` | Plumb agent workspace — truth-checking, drift detection | **Active — Agent** |
| 45 | `byker-production` | Orchestration platform for AI-powered code gen / diagnostics | **Active — Infra** |

**Note:** `visual-polish-systemdot` (Amplified-Partners) and `librarian-api` (Amplified-Partners) are present in the GitHub org but not listed in the active set above. `visual-polish-systemdot` appears to be a JavaScript fork of the visual polish concept. `librarian-api` is the SQLite-backed search API for the knowledge base. Both should be evaluated — OPINION 70% they belong in the active set if still in use.

**Needs Ewan:** Confirm whether `librarian-api` and `visual-polish-systemdot` are active or dormant. I'll proceed with them as active unless you push back.

---

## 3. The Canonical Data Architecture

### Before (Fragmented)

```
PostgreSQL (cove-postgres:5432)
  └── amplified_brain database
      ├── Relational tables (CRM, tenants, entities, relationships)
      ├── pgvector (225K rows, 384-dim HNSW) — ACTIVE
      └── Apache AGE (compound_design graph) — ACTIVE

FalkorDB (falkordb:6379) — SEPARATE PROCESS
  └── 9,000 nodes across 4 graphs — LEGACY, READ-ONLY

Qdrant (qdrant:6333-6334) — SEPARATE PROCESS
  └── 57,434 embeddings (384-dim) — DEPRECATED
  └── llm_cache collection (semantic cache) — DEPRECATED
```

Three database engines. Two of them deprecated. Legacy code still references them. Docker containers still running.

### After (Canonical)

```
PostgreSQL (cove-postgres:5432)
  └── amplified_brain database
      ├── Relational tables (all structured data)
      ├── pgvector + HNSW (ALL embeddings — 225K existing + 57K migrated from Qdrant)
      ├── Apache AGE (ALL graphs — existing + 9K nodes migrated from FalkorDB)
      └── semantic_cache table (migrated from Qdrant llm_cache)
```

**One database engine. Three capabilities. No separate processes.** The Canonical Data Architecture is the law.

### Migration Scope

**Note:** AMP-302 (2026-05-11) already completed bulk data migration to relational tables. See `02_build/brain-migration/README.md` for what was migrated. The scripts in `02_build/scripts/` target the next step: Apache AGE graph format + pgvector HNSW verification.

| Source | Target | Records | Status |
|--------|--------|---------|--------|
| FalkorDB → relational tables | `entities`, `episodes`, `relationships`, `episode_entities` | 53,959 + 4,257 + 34,488 + 59,192 | **Completed** (AMP-302) |
| Qdrant → `knowledge_vectors` | pgvector table | 57,434 | **Completed** (AMP-302) |
| FalkorDB relational → Apache AGE graphs | openCypher graph format | 9,000 nodes | **Planned** (new script) |
| Qdrant `llm_cache` → `semantic_cache` | pgvector HNSW table | Unknown count | **Planned** (new script) |

---

## 4. Local Storage (Beast)

### Directories to Delete (200 GB)

| Directory | Size | Purpose | Risk |
|-----------|------|---------|------|
| `~/bible-extraction-source` | ~155 GB | Raw bible extraction — processed, no longer needed | None — processed data exists elsewhere |
| `~/Knowledge_labelled_temp` | ~21 GB | Temporary labelling workspace | None — temporary by definition |
| `~/Knowledge_raw_temp` | ~20 GB | Temporary raw knowledge staging | None — temporary by definition |

**These are Ewan's action items.** The commands:

```bash
rm -rf ~/bible-extraction-source  # 155GB
rm -rf ~/Knowledge_labelled_temp  # 21GB
rm -rf ~/Knowledge_raw_temp       # 20GB
```

---

## 5. Hidden Value Discovery

### What 7 Months of AI-Native Work Produced

The chaos obscures real value. Across 45 repos:

| Asset | Location | Value |
|-------|----------|-------|
| **CRM with 50+ endpoints** | `crm` | Full business intelligence platform for UK SMBs |
| **PUDDING technique (Swanson ABC)** | `pudding-core`, `pudding-testing` | Novel cross-domain discovery engine — IP |
| **Epistemic Status Invariant** | `clean-build/02_build/routing/` | Layer 0 reference implementation — unique governance |
| **Five Rods governance** | `clean-build/00_authority/` | Constitutional AI governance framework |
| **Business Brain architecture** | `clean-build/00_authority/BRAIN_ARCHITECTURE.md` | 986-line canonical architecture doc with 99-source research grounding |
| **17-and-3 Principle** | Architecture | Novel cardinality rendering — AI reasons on 17, humans see 3 |
| **Marketing Engine** | `marketing-engine` | Automated Five Rods-governed content pipeline |
| **Compound Engineering methodology** | `the-amplified-method`, `portable-spine` | Operational methodology with attribution |
| **Knowledge vault (4,891 files)** | `vault` | Curated Obsidian knowledge base |
| **Raw corpus (~10k files)** | `corpus-raw` | Deduplicated research corpus |
| **Sovereign Fleet (3 entities)** | Beast containers | Multi-model AI fleet on dedicated hardware |

**OPINION 85%:** The hidden value across these repos, if productised and delivered to SMB clients, represents £100k+ in annual recurring revenue potential. The CRM alone (50+ endpoints, Business Brain, Interview Engine, Intelligence Engine) is a complete SaaS product. The PUDDING technique is genuine IP — Swanson's Literature-Based Discovery adapted for business knowledge synthesis.

---

## 6. What This Cleanup Enables

### Immediate

1. **Repository clarity** — 27 repos, each with a clear purpose, no duplicates
2. **Single database engine** — PostgreSQL with AGE + pgvector. No FalkorDB/Qdrant maintenance burden
3. **200 GB disk recovery** on Beast
4. **Clean dependency graph** — new agents can understand the estate in minutes, not hours

### Strategic

1. **Business Brain implementation** — 19-field schema with PUDDING taxonomy, transmission layer (17→3, 3→17)
2. **CRM deployment to Beast** — blocked by data architecture cleanup
3. **Client onboarding** — clean architecture enables the first paying client
4. **Compound engineering** — every future unit of work starts from order, not chaos

---

## 7. Execution Plan

### Day 1: Foundation & Cleanup

| Time | Actor | Action |
|------|-------|--------|
| Morning | Ewan | Run 3 `rm -rf` commands on Beast (200 GB freed) |
| Morning | Devon | Create this case study document ✓ |
| Morning | Devon | Classify all 45 repos ✓ |
| Afternoon | Devon | Delete ewan-dot stubs (7 repos) |
| Afternoon | Devon | Delete Amplified-Partners stubs (5 repos) |
| Afternoon | Devon | Archive dormant repos (6 repos) |
| Afternoon | Devon | Update BRAIN_ARCHITECTURE.md repo map |
| Evening | Ewan | Review and sign off |

### Day 2: Database Migration

| Time | Actor | Action |
|------|-------|--------|
| Morning | Devon | Create + execute FalkorDB → Apache AGE migration script |
| Morning | Ewan | Verify AGE graph data integrity on Beast |
| Afternoon | Devon | Create + execute Qdrant → pgvector migration script |
| Afternoon | Devon | Migrate token-proxy semantic cache |
| Afternoon | Ewan | Verify pgvector embeddings + semantic cache |

### Day 3: Business Brain Implementation

| Time | Actor | Action |
|------|-------|--------|
| Morning | Devon | Implement 19-field `business_brain_context` schema |
| Morning | Devon | Build transmission layer (19→3, 3→19) |
| Afternoon | Devon | Connect CRM + ingestion pipe to Business Brain |
| Afternoon | Devon | Update all agent rules for Canonical Data Architecture |
| Afternoon | Devon | Final BRAIN_ARCHITECTURE.md update |
| Evening | Ewan | End-to-end verification |

---

## 8. Attribution & Provenance

This document is the radical transparency receipt. Every finding, every classification, every deletion target is documented here before execution begins.

**The chaos was not a failure.** It was the cost of building fast with multiple AI agents across 7 months. The order that follows is the compounding. Every future session starts from 27 repos, one database engine, and a clear architecture — not 45 repos and three database engines.

> "We will look at what you said you were going to do and what you did." — Ewan Bramley

This case study is what we said we were going to do. The PRs, scripts, and commits that follow are what we did. The delta is the learning.

---

*Devon-8da1 | 2026-05-15 | devin-8da1981ce177481da3fe1d2b40e7fade*

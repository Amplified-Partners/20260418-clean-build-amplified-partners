---
title: "Amplified Marketing Engine — Full-Stack Spec"
date: 2026-04-30
version: 2
status: candidate
process_family_id: PF-marketing-engine
parents:
  - 00_authority/PROJECT_INTENT.md
  - 00_authority/NORTH_STAR.md
  - 01_truth/processes/2026-04_three-brain-data-isolation_privacy-architecture_v1.md
sources:
  - "Perplexity Deep Research thread (2026-04-30, Ewan prompt): https://www.perplexity.ai/search/4cc30084-cd13-4e28-9b77-3f46ed86a4c1#29"
  - "Ewan reconciled spec (2026-04-30): amplified_machine_spec_for_devon.md — ground truth from Beast SSH + code inventory"
  - "STATUS.md (2026-04-29, Devon): Marketing Engine v0.4.0 running on Amplified Core"
  - "CRM repo: app/marketing_machine/ (avatars, content generator, transparent prompts)"
  - "APDS knowledge note (Ewan + Claude, March 2026): 5-stage Harvest→Extract→Label→Match→Score"
  - "Pudding Technique knowledge note (Ewan + Claude, 2026): Swanson LBD adaptation"
  - "Data Protection Architecture (Ewan dictation, 2026-04-27): Shamir + on-client tokenization"
  - "Remotion (remotion-dev/remotion, 34.4K GitHub stars): React-based programmatic video"
  - "LangGraph (LangChain): stateful agent orchestration with deterministic transitions"
---

<!-- markdownlint-disable-file MD013 -->

# Amplified Marketing Engine — Full-Stack Specification

## What this document is

A candidate specification that maps the Perplexity Deep Research output ("The Amplified Machine", 2026-04-30) against what Amplified Partners has **actually built**, identifies gaps, and produces a unified architecture for an automated, privacy-first, value-giving digital marketing system.

This is `03_shadow/` material — not authoritative. Intended for Ewan's review and selective promotion into `01_truth/` or `02_build/`.

## What already exists (ground truth)

> **Reconciled 2026-04-30** from Ewan's spec (Beast SSH inspection + code inventory). Previous version used repo-only data and was incomplete. Where this document and what's running on Beast disagree, **what's running on Beast wins.**

### Hardware

**Beast = Hetzner AX162-R**
- AMD EPYC 9454P, 48-core / 96-thread
- 251 GB RAM (12 GB used, 238 GB available)
- 1.8 TB storage (169 GB used, 1.5 TB available)
- 10 Gbit pipe, Falkenstein, Germany (EU/GDPR jurisdiction)
- **No GPU.** Ollama runs on CPU. Video rendering and inference share the same compute pool.
- Hostname: `amplified-core` · IP: `135.181.161.131`

### What's running (38 containers, 36 healthy)

**Do not rebuild any of these — extend or call them.**

#### Core infrastructure

| Container | Purpose | Status |
|-----------|---------|--------|
| `falkordb` | Graph DB. 4 graphs: `business_knowledge` (4,973 nodes), `amplified` (3,868 nodes), `amplified_brain` (empty), `amplified_graph` (empty). ~9,000 nodes total. | Up |
| `qdrant` | Vector DB. 57,434 embeddings (384-dim). RAG grounding for content. | Up |
| `litellm` | Model router (local → standard → premium tiers). Port 4000. | Up |
| `postgres` | DB `marketing` — content pipeline state, audit logs. | Up |
| `redis` | Cache. | Up |
| `minio` | Object storage. Port 9000. | Up |
| `searxng` | **243+ source search engine.** Primary harvest engine. Port 8080. | Up |
| `traefik` | Reverse proxy `*.beast.amplifiedpartners.ai`. Ports 80/443. | Up |
| `ollama` | Local LLM. **Models loaded:** llama3.1:70b (42GB), llama3.1:8b (4.9GB), qwen3-coder:30b (18GB), nomic-embed-text (274MB). Port 11434. | Up |

#### Cove orchestration (Temporal stack)

`cove-temporal`, `cove-temporal-ui`, `cove-api`, `cove-postgres` (port 5433), `cove-translator` (8092), `cove-worker` + 4 worker pool (alpha/bravo/charlie/delta), `docker-temporal-1`. **All up.**

#### Application layer

| Container | Purpose |
|-----------|---------|
| `amplified-marketing-engine` | **Marketing Engine v0.4.0** — port 8000, 3-tier API auth (admin/pipeline/readonly). Full pipeline: research → generate → queue → evaluate → learn. |
| `amplified-knowledge-mcp` | **MCP server for FalkorDB + Qdrant** — the canonical knowledge interface. Tools: `query_graph`, `search_vectors`, `ingest_knowledge`, `update_entity`, `tag_entity`, `archive_entity`, `get_audit_log`. **All knowledge ops route through here — do not write directly to FalkorDB or Qdrant.** |
| `enforcer` | 10-min health checks. Currently flagging `ch-pipeline`, `voice-pipeline`, `minio-init`. |
| `kaizen-optimizer` | Standalone Kaizen loop, running. |
| `openclaw-agents` | Agent runtime, port 8100. |
| `langfuse` | Token + cost tracing. |
| `finance-engine`, `nexus-dashboard`, `clickhouse`, `xai-phone-agent`, `amplified-voice-agent`, `amplified-code-server` | Other production services. |

#### Schedulers running

- **Content pipeline cron** — 4am UTC. Generate → evaluate → queue.
- **Backup cron** — 3am UTC. FalkorDB + Qdrant snapshots.

#### Schedulers NOT yet running (Phase 0 fix list)

- Internal Kaizen cron (weekly)
- External Kaizen cron (monthly)
- Email learning reports to Ewan

### The live marketing pipeline

**Pipeline:** `research → generate → queue → evaluate → learn`. Sequential cron, port 8000, 3-tier auth.

- **Stage 1 — Research:** `agents/research_agent.py` (461 lines). Source: SearXNG (243+ sources). Grounding: Qdrant + FalkorDB via `amplified-knowledge-mcp`.
- **Stage 2 — Content generation:** `agents/content_agent.py` (369 lines). Atomiser: `agents/content_atomizer.py` (317 lines) — pillar content → 5 platform variants. Routes through LiteLLM → llama3.1:8b currently.
- **Stage 3 — Synthetic evaluation:** `synthetic_evaluator.py` (546 lines). **8 personas built:** Bob, Lisa, Marcus, Sarah, Technical Tom, Skeptical Sam, Budget Brian, Growth Gina. **Currently running 3** (Bob/Lisa/Marcus). 5 dimensions, 1–10 scale.
- **Stage 4 — Human review:** Mandatory. Ewan sign-off via Command Centre + API. Telegram gate for publish approval.
- **Stage 5 — Distribution:** `agents/publishing_agent.py` (256 lines), `platform_adapters.py` (431 lines). **Built adapters:** LinkedIn (OAuth), Substack, Twitter/X, Email (Brevo), Blog. Platform-optimal UK timing.
- **Stage 6 — Kaizen:** `kaizen.py` (367 lines) + `kaizen-optimizer` container. Cove Kaizen workflow: `kaizen_workflow.py` + activities (1,320 lines) on Temporal — production, self-improving, auto-applying. Layer 0 locked, max 3 auto-applies/cycle.

### Code inventory on Beast

| Codebase | Lines | What it provides |
|----------|-------|-----------------|
| `cove-orchestrator` | 20,218 | Temporal workflows, Kaizen, Chaos, Self-heal, Quality gates. Repo: `github.com/ewan-dot/amplified-partners.git` (Ewan's personal account, NOT the org). |
| `nightscout/` | 952 | RSS + SearXNG fetchers, 4-dimension Ollama scorer, tiered routing, Postgres storage, Telegram briefing. **27 sources defined.** Pattern for any harvest extension. |
| `marketing-engine/` | 4,477 | Detailed above. |
| `amplified-knowledge-mcp` | 1,016 | FalkorDB + Qdrant with 3-tier access, audit log, embedder via Ollama nomic-embed-text. |
| `pudding-testing/` | 2,826 | `/opt/amplified/pudding-testing/` — `abc_discovery.py`, `labeller.py`, `pairwise.py`, `discovery_test.py`. Vault was sparse at first test (2026-03-15); now has 4,755 markdown files. |
| `real/token_proxy.py` | 988 | Intercepts LLM calls, tracks costs, enforces budgets. |
| `daily_cost_report.py` | 278 | Telegram daily cost reports. |
| `agent-service-toolkit/` | 7,743 | LangGraph agent framework fork (JoshuaC215). **Use this when LangGraph migration triggers.** |
| `vault-to-qdrant.py` | 418 | Monitors `.md` changes, chunks, embeds, upserts. Pattern for any new ingestion. |

**Vault:** `/opt/amplified/vault/` — 4,755 files across 25 directories.

### CRM codebase (`Amplified-Partners/crm`)

| Component | What it does |
|-----------|-------------|
| `app/marketing_machine/agents/avatars.py` | 40 campaigns: 10 trades × 4 archetypes (Bob, Sheila, Dave, Russell). Revenue brackets, pain points, tone, channels. |
| `app/marketing_machine/agents/service_businesses.py` | 50+ UK business types: 33 trades + 20+ service businesses. Pain points as questions (permission-based marketing). |
| `app/marketing_machine/agents/transparent_prompts.py` | Honest messaging — Amplified speaking as itself, not pretending to be tradespeople. |
| `app/marketing_machine/content/generator.py` | Claude Sonnet content generation with prompt caching. 160 pieces/day target. ~£100–150/month with caching. |

### `clean-build` codebase

| Component | What it does |
|-----------|-------------|
| `02_build/scripts/pudding_labeler.py` | PUDDING 2026 taxonomy: `WHAT.HOW.SCALE.TIME.PATTERN` labels for vault ingestion. |
| `02_build/command-centre/` | React frontend (Vite + TypeScript). Search, agents panel, writing panel, R&D panel. |
| `02_build/cove-orchestrator/` | Email agent + MCP servers (filesystem, email, Langfuse). |

### Governance and methodology

| Artifact | What it provides |
|----------|-----------------|
| **Layer 0 Amplified Laws** (`agents/prompts/layer0_laws.py`, authoritative: `00_authority/EIGHT_LAWS.md`) | 8 physically locked laws: (1) Don't Hurt Anyone, (2) HR Is Absolute, (3) No Telling People Off, (4) Radical Honesty, (5) Radical Transparency, (6) Ideas Meritocracy, (7) Radical Attribution, (8) Win-Win or Don't Play. **Kaizen cannot modify these.** |
| **APDS** (knowledge note) | 5-stage autonomous discovery: Harvest → Extract → Label → Match → Score. FalkorDB schema. Container architecture. |
| **Pudding Technique** (knowledge note) | Swanson LBD adapted for business. Neutral taxonomy at ingestion, lens at query time. Mathematical validation (p < 0.001). |
| **Three-Brain Isolation** (`01_truth/processes/`) | Amplified Brain / Per-Client Brain / Federated Brain. Privacy by architecture. |
| **Data Protection Architecture** (knowledge note) | On-client PII tokenization. Shamir's Secret Sharing. Amplified never holds personal data. |
| **Strangler Fig Migration** (`01_truth/processes/`) | Shadow → Sidecar → Gradual → Cutover pattern for client onboarding. |
| **Gated Pipelines** (`01_truth/processes/`) | Deterministic stages, pass/fail gates, halt-on-failure, privacy tokenization. |

---

## What Perplexity proposed vs what we have

| Perplexity proposal | Amplified reality | Verdict |
|--------------------|--------------------|---------|
| Hetzner Beast with Docker, Ollama, vLLM, Qdrant, PostgreSQL, Redis, MinIO, Prometheus, Grafana | **Already running.** 38 containers, 36 healthy. Core has FalkorDB, Qdrant, LiteLLM, PostgreSQL, Redis, MinIO, SearXNG, Traefik, Ollama (70b + 8b + qwen3-coder + nomic-embed), Cove Temporal stack, knowledge-mcp, backups. Missing: Grafana (not yet configured). Prometheus config exists in `02_build/config/`. | Exists. Fill monitoring gap when pipeline is heavier. |
| LangGraph state machine for orchestration | **Not yet implemented.** Current pipeline is sequential cron (research → generate → queue → evaluate → learn). LangGraph would add: conditional routing, parallel branches, human-in-the-loop breakpoints, state checkpointing. | **Genuine upgrade.** Worth building when pipeline complexity justifies it. |
| RAG grounding / "zero hallucination" | **Already running.** Qdrant (57K embeddings) + FalkorDB (9K nodes) feed the research agent. Content grounded against vault. | Exists. Perplexity overclaims "zero hallucination." Our deterministic sandwich is more honest. |
| OCEAN personality profiling from social media | **Not implemented. Should not be.** Scraping social media for psychographic profiling violates GDPR/DPA 2018 and contradicts our Data Protection Architecture (Amplified never holds personal data). | **Reject as described.** See §Privacy-safe alternative below. |
| VARK learning style detection | **Not implemented.** Interesting for content adaptation but the ANN-based approach Perplexity describes requires individual-level data we don't hold. | **Reject individual profiling. Adapt the concept** — see §Content adaptation below. |
| Remotion programmatic video | **Not in current stack.** React-based, 34.4K GitHub stars, MCP integration as of Jan 2026. Beast is CPU-only — benchmark render times before committing to scale. | **Genuine addition.** Worth prototyping. |
| AI email engine with predictive send-time | **Partially exists.** Cove orchestrator has email agent (`02_build/cove-orchestrator/email_agent/`). Not yet doing AI-generated marketing emails at scale. | **Extend existing.** Don't rebuild. |
| Reddit value engine | **Not in current stack.** Philosophy aligns perfectly with Amplified (90% value, 10% mention, human-in-the-loop). | **Genuine addition.** Worth building. |
| Multi-agent 4-tier hierarchy | **Partially exists.** Agent roster (TAXONOMY.md) defines Devon, OpenClaw, Cursor, AG, Perplexity, Qwen. Marketing engine has synthetic evaluators. Not yet a formal orchestration hierarchy for content. | **Adapt, don't duplicate.** LangGraph subgraphs per agent role. |
| Sentiment analysis (spaCy + HuggingFace) | **Partially exists.** APDS Extract stage does entity/relationship/concept extraction. Not yet doing aspect-based sentiment on engagement data. | **Extend APDS.** Add sentiment as an extraction dimension. |
| Flywheel / feedback loop | **Already running.** Kaizen analyses feedback → generates preferences → content agent reads preferences. Bob/Lisa/Marcus score content. Missing: external engagement metrics feeding back. | Exists internally. External loop is the gap. |

---

## Unified Architecture

### Design principles (non-negotiable)

1. **Privacy by architecture.** Amplified never holds personal data. No individual psychographic profiles. No social media scraping for PII. The Data Protection Architecture and Three-Brain Isolation are structural constraints, not optional.

2. **Deterministic-first (90/10).** Per `PRINCIPLES.md`: deterministic representations for 90% (schemas, pipelines, gated stages). LLM freedom for the 10% where synthesis adds value (content generation, research discovery). LangGraph enforces this — deterministic graph edges, probabilistic node internals.

3. **Value-first marketing.** We give everything away free. No gated content, no email capture requirements, no dark patterns. Permission-based marketing: pain points as questions, not assertions. Transparent prompts — Amplified speaks as itself.

4. **Radical attribution.** Every piece of content cites its sources. Every agent signs its work. This is not optional — it is the brand.

5. **Blinkers without ceilings.** Agents operate with full autonomy inside defined constraints. The constraints are the blinkers. There is no ceiling on ingenuity within them.

6. **Layer 0 Amplified Laws** (`agents/prompts/layer0_laws.py`, authoritative: `00_authority/EIGHT_LAWS.md`) — physically locked. Kaizen cannot modify them. 8 laws: (1) Don't Hurt Anyone, (2) HR Is Absolute, (3) No Telling People Off, (4) Radical Honesty, (5) Radical Transparency, (6) Ideas Meritocracy, (7) Radical Attribution, (8) Win-Win or Don't Play.

### System boundary model

```
┌─────────────────────────────────────────────────────────┐
│  AIR (sandbox / research / discovery)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Perplexity / Brave / SearXNG / Reddit listener   │  │
│  │  APDS Harvest stage                                │  │
│  │  Content research agents                           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
           │ (validated, attributed data only)
           ▼
┌─────────────────────────────────────────────────────────┐
│  AMPLIFIED CORE (Hetzner AX162-R, 135.181.161.131)     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ FalkorDB │ │  Qdrant  │ │ Postgres │ │  Redis   │  │
│  │ (9K nds) │ │ (57K em) │ │(mktg db) │ │ (cache)  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ LiteLLM  │ │  Ollama  │ │  MinIO   │ │ SearXNG  │  │
│  │ (router) │ │(70b+8b+) │ │ (object) │ │(243+src) │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────────────────┐ ┌────────────────────────┐   │
│  │ knowledge-mcp        │ │ Marketing Engine v0.4+ │   │
│  │ (canonical KG iface) │ │ + Cove Temporal stack   │   │
│  └──────────────────────┘ └────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐│
│  │  LangGraph Orchestrator (when justified)            ││
│  │  Remotion video render (CPU, when prototyped)       ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
           │ (approved, attributed content only)
           ▼
┌─────────────────────────────────────────────────────────┐
│  DISTRIBUTION (outbound channels)                       │
│  LinkedIn · Facebook · Reddit · GMB · Email · TikTok    │
│  (human-in-the-loop approval before publish)            │
└─────────────────────────────────────────────────────────┘
```

Client infrastructure is **separate** per Three-Brain Isolation. Marketing Engine operates in the Amplified Brain only. No client data enters the marketing pipeline.

### The pipeline (what runs)

The current sequential pipeline (cron, 4am UTC) evolves into a staged, gated pipeline. Each stage has explicit inputs, outputs, and pass/fail gates.

#### Stage 1: Research

**Inputs:** Standing lenses (from Pudding Technique), trending topics, engagement feedback from previous cycles, Reddit/community signals.

**Process:**
- APDS Harvest pulls from: **SearXNG (243+ sources, already running on Beast port 8080)**, Perplexity searches, RSS feeds, Reddit monitoring, trade press, academic sources. All research via SearXNG first.
- APDS Extract + Label: entities tagged with PUDDING 2026 taxonomy (`WHAT.HOW.SCALE.TIME.PATTERN`).
- APDS Match + Score: cross-domain bridge discovery. Emergence score `E = (B × D × N) / R`.
- Output: research briefs with attributed sources and confidence bands (PROVEN / VALID / HYPOTHESIS).

**Gate:** Every research brief must have ≥1 attributed source. No `[SOURCE REQUIRED]` briefs pass to content generation.

**What's new vs current:** Reddit monitoring feed, APDS integration into the marketing pipeline (currently APDS is specified but not wired to content generation).

#### Stage 2: Content generation

**Inputs:** Research briefs, avatar definitions (40 campaigns from `avatars.py`, 50+ business types from `service_businesses.py`), PUDDING recipes, engagement preferences from Kaizen.

**Process:**
- Text content: Claude Sonnet via transparent prompts. 160 pieces/day across avatar × channel matrix. Prompt caching for cost control (~£100–150/month).
- Video content `[LOGIC TO BE CONFIRMED]`: Remotion pipeline (see §Remotion below).
- Email content: extend existing Cove email agent for marketing sequences. Value-first: educate → demonstrate → soft offer.

**Content adaptation — put it in their language, don't profile who's listening:**

The goal is simple: a plumber should hear plumber words. An electrician should hear electrician words. A solo operator worried about cash flow should hear someone who understands cash flow anxiety — not corporate marketing speak. We adapt the voice to the audience, not surveil the listener.

This is **segment-level adaptation**, not individual profiling:
- **By trade**: plumbers get plumbing pain points, electricians get electrical pain points (already implemented in `avatars.py`).
- **By archetype**: Bob (solo, pragmatic), Sheila (professional, quality-driven), Dave (scaling, team coordination), Russell (established, strategic) — already implemented.
- **By channel**: platform-specific tone adaptation (LinkedIn = professional, Facebook = conversational, Reddit = helpful peer, GMB = local and direct).
- **By format preference**: same content, multiple formats (text post, short video, infographic, thread). Let the audience self-select. No surveillance required.

**What we never do:**
- Build individual profiles. We don't need to know who's reading — we need to know what trade they're in and what stage they're at.
- Store anything about the individual. If a platform tells us someone is a plumber in Newcastle, we match them to the plumber segment and discard the individual signal. Transient matching only.
- Scrape social media for personal data. The Data Protection Architecture is structural — Amplified never holds personal data. This applies to marketing as much as it applies to client delivery.

The intelligence is in understanding trades and archetypes deeply (50+ business types, 4 archetypes with distinct pain points, tones, and channels). That's our knowledge, not theirs. We translate what we know into language they recognise. That's respectful communication, not surveillance.

**Gate:** Every piece of content passes synthetic evaluation (Bob/Lisa/Marcus panel, score ≥ 6/10 per existing system). Content must cite at least one source (radical attribution). Content must pass the transparent prompt check — Amplified speaks as itself.

#### Stage 3: Evaluation

**Inputs:** Generated content from Stage 2.

**Process:**
- Synthetic evaluators score 1–10 on: relevance, honesty, clarity, actionability, attribution. **8 personas built** (Bob, Lisa, Marcus, Sarah, Technical Tom, Skeptical Sam, Budget Brian, Growth Gina); **3 currently running** (Bob/Lisa/Marcus).
- Automated checks: source citations present, no claims without backing, tone matches channel, length within bounds.
- Quality routing: ≥7/10 → auto-queue for human review. 6/10 → revision queue. <6/10 → reject with feedback to Kaizen.

**Gate:** No content reaches human review without passing both synthetic evaluation and automated checks.

**What's new vs current:** Automated attribution checking. Channel-specific scoring criteria. Revision routing (currently binary pass/fail).

#### Stage 4: Human review and approval

**Inputs:** Evaluated content in review queue.

**Process:**
- Ewan (or delegated reviewer) reviews queued content via Command Centre or API.
- Approve / reject / edit. Edits feed back to Kaizen preferences.
- Approved content tagged with publish schedule (optimal time per channel).

**Gate:** Human approval is mandatory before any content is published. No automated publishing without explicit human sign-off. This is a non-negotiable — per `AGENTS.md` ("Every single thing is Ewan's responsibility") and the Reddit value engine philosophy.

`[DECISION REQUIRED]` — When volume scales beyond what Ewan can review personally, define delegation rules and trust thresholds per avatar/channel. The Trust Ramp (`01_truth/processes/2026-04_trust-ramp_four-stage-autonomy_v1.md`) provides a framework for this.

#### Stage 5: Distribution

**Inputs:** Approved content with publish schedules.

**Process:**
- Multi-platform publishing via **built adapters** (already exist): LinkedIn (OAuth), Substack, Twitter/X, Email (Brevo), Blog. TikTok when video pipeline is live.
- Publishers: `agents/publishing_agent.py` (256 lines), `platform_adapters.py` (431 lines). Platform-optimal UK timing.
- **Telegram gate:** Ewan approves everything before publish.
- Reddit posts are **never automated**. The Reddit Value Engine (see §Reddit below) uses human-in-the-loop posting.

**Gate:** Content published only at scheduled times. Rate limiting per platform. No duplicate posting.

#### Stage 6: Feedback and Kaizen

**Inputs:** Engagement metrics from published content. Synthetic evaluation scores. Human edit patterns.

**Process:**
- **Internal Kaizen (running):** `kaizen.py` (367 lines) + `kaizen-optimizer` container + Cove Kaizen workflow (`kaizen_workflow.py` + activities, 1,320 lines) on Temporal. Self-improving, auto-applying with Layer 0 locked and max 3 auto-applies per cycle. Retrospective → insights → suggestions → auto-apply.
- **Internal Kaizen cron:** Not yet scheduled (Phase 0 fix).
- External Kaizen `[LOGIC TO BE CONFIRMED]`: engagement metrics (likes, comments, shares, DMs, Reddit karma) feed back into research briefs and avatar refinements.
- APDS standing lenses run against new engagement data: "Does this engagement pattern match a known Pudding recipe?"

**Reuse for external loop:** `kaizen_workflow.py` Temporal pattern, `kaizen_apply_activities.py` auto-apply pattern, `langfuse` for engagement event tracing.

**What's new vs current:** External engagement metrics feedback loop. APDS integration for pattern discovery in engagement data.

---

## New components (from Perplexity, adapted for Amplified)

### Remotion Video Pipeline `[LOGIC TO BE CONFIRMED]`

**What:** [Remotion](https://github.com/remotion-dev/remotion) (34.4K GitHub stars) creates MP4 videos programmatically using React. As of January 2026, Remotion Agent Skills allow AI-to-video generation via MCP.

**Why:** Video is the highest-engagement format on every platform. Programmatic generation means: same template, different data, hundreds of variations at near-zero marginal cost.

**Constraint: Beast is CPU-only.** No GPU. The AX162-R was chosen with video load in mind (96 threads, 256GB RAM), but render times will be slower than GPU-equivalent. Benchmark render queue depth and concurrency vs Ollama inference load before committing to scale.

**Architecture:**

```
Research brief
    ↓
Script Node → segment-adapted scripts from Claude (by trade, archetype, channel)
    ↓
Asset Node → source images + generate voiceover (ElevenLabs or local TTS)
    ↓
Composition Node → Remotion React composition from branded templates
    ↓
Render Node → server-side MP4 render on Beast CPU (96 threads)
    ↓
Evaluation Node → synthetic evaluator panel scores the video
    ↓
Human review → approve/reject
    ↓
Distribute → TikTok, Instagram, YouTube, LinkedIn
```

**Dependencies:**
- Node.js + React environment on Beast (for Remotion)
- Branded templates (design work — `[DECISION REQUIRED]` on brand assets)
- Voiceover: ElevenLabs API or local TTS model on Beast
- CPU capacity planning — rendering vs Ollama inference share the same compute pool. Benchmark before scaling.
- Synthetic evaluator extension — video-specific dimensions (visual coherence, pacing, voiceover quality)

**Risk:** Remotion adds significant complexity. **Recommendation:** prototype with one avatar (Bob the plumber), one template, one channel (LinkedIn) before scaling. If evaluators score ≥7/10 and engagement beats text-only, expand. Otherwise revisit per `USE_IT_OR_CUT_IT.md`.

### Reddit Value Engine `[LOGIC TO BE CONFIRMED]`

**What:** Automated discovery of high-value Reddit threads where Amplified's knowledge can genuinely help, with human-in-the-loop posting.

**Philosophy:** 90% pure value, 10% natural mention. We answer questions because we know the answers, not because we want clicks. This is the most aligned channel for Amplified's "give everything away free" ethos.

**Architecture:**

```
Reddit Monitor (APDS Harvest)
    ↓
Subreddit listener → r/plumbing, r/electricians, r/HVAC,
                     r/smallbusiness, r/UKbusiness, r/selfemployed,
                     r/contractor, r/trades, etc.
    ↓
Intent classifier → high-intent question? pain point? competitor mention?
    ↓
RAG-grounded draft → Qdrant + FalkorDB knowledge → attributed answer
    ↓
Human review → team member reviews, personalises, posts manually
    ↓
Value tracking → karma, engagement, DMs → feeds back to Kaizen
```

**Rules (non-negotiable):**
1. **Never automate posting.** Reddit detects and bans bots. More importantly, automated posting violates the value-first principle — real help requires human judgment.
2. **Never self-promote in the first paragraph.** Lead with the answer. If Amplified is mentioned, it's in context ("we built a tool that does X" — only if relevant to the answer).
3. **Cite sources.** Radical attribution applies on Reddit too.
4. **Respect subreddit rules.** Some subs ban self-promotion entirely. The monitor must flag these.

**Implementation (reuse existing code):**
- Extend `nightscout/fetchers.py` (952 lines, 27 sources already defined) with Reddit API — NightScout is the ready-made pattern for any harvest extension
- Reuse `amplified-knowledge-mcp` for RAG grounding (do not write directly to FalkorDB/Qdrant)
- Reuse `synthetic_evaluator.py` for draft quality scoring
- Add Reddit-specific dimensions to evaluator (subreddit fit, helpfulness, non-promotional tone)
- New intent classifier — small LLM via LiteLLM cheap tier

**Dependencies:**
- Reddit API access (free tier sufficient for monitoring; posting is manual anyway)
- Subreddit list curation (start with 10, expand based on engagement data)
- Human reviewer capacity (initially Ewan; later delegated per Trust Ramp)
- `[DECISION REQUIRED]` Reddit account strategy: company / personal / multiple per vertical?

### LangGraph Orchestration `[LOGIC TO BE CONFIRMED]`

**What:** Replace the current sequential cron pipeline with a LangGraph state machine that supports conditional routing, parallel branches, and human-in-the-loop breakpoints.

**Why:** The current pipeline is linear (research → generate → queue → evaluate → learn). As channels multiply (text + video + email + Reddit), the pipeline needs branching. LangGraph provides:
- **Deterministic graph edges** (satisfies our 90/10 principle)
- **Probabilistic node internals** (LLM calls wrapped in structured output)
- **State checkpointing** (resume from failure, not restart)
- **Human-in-the-loop breakpoints** (approval gates as graph nodes)
- **Subgraph composition** (each agent role is a composable subgraph)

**When:** Not now. The current sequential pipeline works for single-channel text content. LangGraph is justified when:
- Video pipeline comes online (parallel branch)
- Reddit engine comes online (different cadence and approval flow)
- Email sequences come online (multi-step stateful flows)
- **Trigger:** when the cron pipeline requires ≥3 conditional branches, migrate to LangGraph.

**Implementation:** Use `agent-service-toolkit/` (7,743 lines, already on Beast) — LangGraph agent framework fork (JoshuaC215). This is the starting point, not a from-scratch build.

**Risk:** Premature abstraction. LangGraph adds infrastructure complexity. Per `USE_IT_OR_CUT_IT.md`: if we build it and don't use the branching, cut it.

---

## What we explicitly reject from Perplexity

### Individual psychographic profiling (OCEAN/VARK on individuals)

Perplexity proposes scraping social media to build Big Five personality profiles per prospect and classifying individuals into learning styles.

**Rejected because:**

1. **GDPR / UK DPA 2018 violation.** Processing personal data for profiling without explicit consent is unlawful. Our Data Protection Architecture is designed so we never hold personal data. Individual psychographic profiles are personal data by definition.

2. **Contradicts Three-Brain Isolation.** The Amplified Brain contains proprietary frameworks and research. It does not contain individual prospect data. Psychographic profiles of identifiable individuals would breach the isolation boundary.

3. **Contradicts the product philosophy.** We help businesses make better decisions with *their own data*. We don't build profiles of their customers without consent.

4. **The alternative is better.** Segment-level adaptation (by trade, archetype, channel, format) gives us effective personalisation without surveillance. The intelligence is in understanding trades and archetypes deeply — which we already do (50+ business types, 4 archetypes with distinct pain points, tones, and channels).

### "Zero hallucination surface"

Overclaim. RAG grounding reduces hallucination — it does not eliminate it. Our deterministic sandwich pattern (deterministic input validation → LLM generation → deterministic output validation) is more honest about the residual risk. Synthetic evaluators catch remaining drift. Human review is the final gate.

### Single-box deployment

Perplexity dumps everything on one Hetzner box with no boundary model. We maintain Air / Core / Distribution separation. Research happens in the Air sandbox. Core runs the pipeline. Distribution is outbound-only. Client infrastructure is never co-located.

---

## Deployment roadmap (adapted for what exists)

Perplexity's 16-week generic roadmap is replaced with phases grounded in current state.

### Phase 0: Tighten what's running (weeks 1–2)

No new components. Fix known gaps from STATUS.md:

- [ ] Schedule Internal Kaizen cron (weekly)
- [ ] Schedule External Kaizen cron (monthly)
- [ ] Fix radical attribution in generated content (all three avatars flagged this)
- [ ] Tune GMB content quality (currently 4.0/10 — needs platform-specific prompts)
- [ ] Email learning reports to Ewan (weekly digest of Kaizen output)
- [ ] `[DECISION REQUIRED]` Model upgrade: llama3.1:8b is the current content quality bottleneck. **llama3.1:70b is already loaded on Beast** (42GB). Options: (a) switch pipeline to 70b locally, (b) Claude API for generation (CRM already uses it, ~£100–150/mo), (c) hybrid — local for research, API for generation.

### Phase 1: Reddit Value Engine (weeks 3–6)

Lowest complexity, highest alignment with brand values:

- [ ] Extend `nightscout/fetchers.py` with Reddit API (free tier, read-only monitoring)
- [ ] Set up subreddit listener for 10 target subreddits
- [ ] Wire APDS Harvest to ingest Reddit threads as a source
- [ ] Build intent classifier (small LLM via LiteLLM cheap tier)
- [ ] RAG-grounded draft response generator via `amplified-knowledge-mcp` → attributed answer
- [ ] Reuse `synthetic_evaluator.py` + add Reddit-specific scoring dimensions
- [ ] Human review interface in Command Centre
- [ ] Value tracking dashboard (karma, engagement, DM conversions)

### Phase 2: External feedback loop (weeks 5–8)

Close the loop between published content and content generation:

- [ ] Platform API integrations for engagement metrics (LinkedIn, Facebook, GMB)
- [ ] External Kaizen: engagement data → preference updates → content agent
- [ ] APDS standing lens: "What engagement patterns match known Pudding recipes?"
- [ ] Automated reporting: weekly summary to Ewan (email or Slack)

### Phase 3: Remotion video prototype (weeks 7–12)

Single avatar, single template, single channel:

- [ ] Install Remotion on Beast. **Benchmark CPU rendering vs Ollama inference load** (shared compute pool, no GPU).
- [ ] Design one branded video template (Bob the plumber, LinkedIn)
- [ ] Script generation node (Claude → structured video script)
- [ ] Voiceover: evaluate ElevenLabs API vs local TTS
- [ ] Render pipeline: script → assets → composition → MP4
- [ ] Synthetic evaluation for video (extend Bob/Lisa/Marcus panel)
- [ ] Human review → publish to LinkedIn
- [ ] `[DECISION REQUIRED]` If prototype scores ≥7/10 from evaluators and engagement beats text-only, expand to more avatars/channels.

### Phase 4: LangGraph migration (weeks 10–14, only if triggered)

Only proceed if pipeline complexity justifies it (≥3 conditional branches):

- [ ] Model current pipeline as LangGraph state machine
- [ ] Add conditional routing: text vs video vs email vs Reddit
- [ ] Add parallel branches: generate text + video simultaneously
- [ ] Add state checkpointing (resume from failure)
- [ ] Human-in-the-loop breakpoints as graph nodes
- [ ] `[DECISION REQUIRED]` If LangGraph doesn't produce measurable improvement in pipeline reliability or throughput within 2 weeks of deployment, revert to sequential cron per `USE_IT_OR_CUT_IT.md`.

### Phase 5: Scale (weeks 12+, ongoing)

- [ ] Expand avatars: 50+ business types × 4 archetypes × multiple channels
- [ ] Expand Reddit to 20+ subreddits
- [ ] Expand video to multiple templates and channels
- [ ] Email marketing sequences (value-first drip campaigns via Cove email agent)
- [ ] APDS cross-vertical pattern reports feeding content strategy

---

## Economics

Current (from CRM repo `app/marketing_machine/content/generator.py`):

| Item | Cost |
|------|------|
| Claude Sonnet content generation (CRM, with caching) | ~£100–150/month |
| Hetzner AX162-R | Already provisioned |
| FalkorDB + Qdrant + PostgreSQL + Redis + MinIO + Cove + LiteLLM | All on Beast, no marginal cost |

Projected additions:

| Item | Estimated cost | Notes |
|------|---------------|-------|
| Remotion rendering | £0 (self-hosted, CPU) | Open-source, CPU on Beast. |
| ElevenLabs voiceover | ~£5–22/month (Starter–Creator) | `[LOGIC TO BE CONFIRMED]` — local TTS may be sufficient |
| Reddit API | £0 (free tier) | Read-only monitoring. Posting is manual. |
| Platform API integrations | £0–50/month | Depends on tier. Most have free tiers sufficient for our volume. |
| Better LLM access | £50–200/month | `[DECISION REQUIRED]` — depends on model choice |

**Total projected:** £155–422/month for a full-stack, multi-channel, value-first marketing system generating 160+ pieces of content/day with video, Reddit engagement, and closed-loop learning.

---

## Metrics (what we measure)

| Metric | Source | Frequency |
|--------|--------|-----------|
| Content quality (synthetic) | Bob/Lisa/Marcus evaluator scores | Per piece |
| Content quality (human) | Ewan approval/rejection rate | Per review batch |
| Engagement rate | Platform APIs | Weekly |
| Reddit karma + engagement | Reddit API | Weekly |
| Video engagement vs text | Platform APIs | Weekly |
| Content cost per piece | LiteLLM via Langfuse | Monthly |
| Pipeline reliability | Success/failure logs | Per run |
| Kaizen preference drift | Internal Kaizen output | Weekly |
| APDS emergence discoveries | APDS scorer output | Weekly |
| Source citation rate | Automated content check | Per piece |

**Vanity metrics ignored:** impressions, follower count, "reach", likes.

---

## Open questions (`[DECISION REQUIRED]`)

1. **Model quality:** llama3.1:8b vs llama3.1:70b (already loaded) vs Claude API vs hybrid. Content quality is directly gated by model quality. The CRM codebase already uses Claude Sonnet for generation — should the Beast pipeline do the same?

2. **Video brand assets:** Remotion needs branded templates. Who designs them? What's the visual identity?

3. **Delegation threshold:** When content volume exceeds Ewan's review capacity, what are the delegation rules? Trust Ramp provides a framework but specific thresholds are `[DECISION REQUIRED]`.

4. **Covered AI vs Cove relationship:** Distinct products per TAXONOMY.md. How does Marketing Engine relate to each?

5. **Email marketing routing:** Through existing Cove email agent or separate pipeline? Separation of concerns vs consolidation.

6. **Reddit account strategy:** Company account? Personal account? Multiple accounts per trade vertical?

7. **Xero / QuickBooks integrations:** Disabled (Python 3.13 compatibility). Fix or drop?

8. **Voice bridge:** Disabled (Deepgram SDK compatibility). Fix or migrate to Retell-only?

9. **Redis for conversation state:** Currently in-memory dict. Production blocker for voice.

---

## Build posture for Devon

- **Reuse aggressively.** Directly reusable code on Beast: marketing-engine (4,477), knowledge-mcp (1,016), pudding-testing (2,826), token proxy + cost report (1,266), vault-to-qdrant (418), agent-service-toolkit (7,743) = ~17.7K lines. Additionally, cove-orchestrator (20,218 lines including nightscout/952) in Ewan's personal repo. Estimated new code: ~5,800 lines.
- **All knowledge ops** via `amplified-knowledge-mcp` — never write directly to FalkorDB or Qdrant.
- **All LLM calls** via LiteLLM — use tier names (local/standard/premium), never raw model names.
- **All web research** via SearXNG first.
- **All Layer 0 laws** physically locked. Kaizen cannot modify them.
- **All published content** requires human approval. No exceptions until delegation thresholds are defined.
- **Cove-orchestrator** lives in `github.com/ewan-dot/amplified-partners.git` (Ewan's personal account, NOT the Amplified-Partners org). Note this for PRs.
- If anything in this spec contradicts what's running on Beast right now, **what's running on Beast wins.** Ask before deviating.

---

Signed-by: Devon | 2026-04-30 | devin-0fce62f4c12d4a209748f9daae4ec607

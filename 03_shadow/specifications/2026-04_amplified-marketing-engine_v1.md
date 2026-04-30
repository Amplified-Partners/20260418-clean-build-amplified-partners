---
title: "Amplified Marketing Engine — Full-Stack Spec"
date: 2026-04-30
version: 1
status: candidate
process_family_id: PF-marketing-engine
parents:
  - 00_authority/PROJECT_INTENT.md
  - 00_authority/NORTH_STAR.md
  - 01_truth/processes/2026-04_three-brain-data-isolation_privacy-architecture_v1.md
sources:
  - "Perplexity Deep Research thread (2026-04-30, Ewan prompt): https://www.perplexity.ai/search/4cc30084-cd13-4e28-9b77-3f46ed86a4c1#29"
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

Before designing anything new, here is what is **running** on Amplified Core (`135.181.161.131`) as of 2026-04-29:

| System | Status | What it does |
|--------|--------|-------------|
| **Marketing Engine v0.4.0** | Running (port 8000) | Content pipeline: research → generate → queue → evaluate → learn |
| **FalkorDB** | Running | 9,000 nodes across 4 graphs. Knowledge graph for vault content. |
| **Qdrant** | Running | 57,434 embeddings (384-dim). Vector search for RAG grounding. |
| **LiteLLM** | Running | Proxy for local + remote LLMs. Currently llama3.1-8b local. |
| **PostgreSQL** | Running | DB: marketing. State persistence, audit logs. |
| **Synthetic Evaluators** | Running | Bob, Lisa, Marcus avatar panel. Score every piece of content 1–10. |
| **Content Pipeline Cron** | Scheduled 4am UTC | Generate → evaluate → queue for review. Fully autonomous. |
| **Backup Cron** | Scheduled 3am UTC | FalkorDB + Qdrant snapshots. |
| **API Auth** | 3-tier | Admin / Pipeline / Readonly keys. All endpoints secured. |

CRM codebase (`Amplified-Partners/crm`) contains:

| Component | What it does |
|-----------|-------------|
| `app/marketing_machine/agents/avatars.py` | 40 campaigns: 10 trades × 4 archetypes (Bob, Sheila, Dave, Russell). Revenue brackets, pain points, tone, channels. |
| `app/marketing_machine/agents/service_businesses.py` | 50+ UK business types: 33 trades + 20+ service businesses. Pain points as questions (permission-based marketing). |
| `app/marketing_machine/agents/transparent_prompts.py` | Honest messaging — Amplified speaking as itself, not pretending to be tradespeople. |
| `app/marketing_machine/content/generator.py` | Claude Sonnet content generation with prompt caching. 160 pieces/day target. ~£100–150/month with caching. |

`clean-build` codebase contains:

| Component | What it does |
|-----------|-------------|
| `02_build/scripts/pudding_labeler.py` | PUDDING 2026 taxonomy: `WHAT.HOW.SCALE.TIME.PATTERN` labels for vault ingestion. |
| `02_build/command-centre/` | React frontend (Vite + TypeScript). Search, agents panel, writing panel, R&D panel. |
| `02_build/cove-orchestrator/` | Email agent + MCP servers (filesystem, email, Langfuse). |

Governance and methodology:

| Artifact | What it provides |
|----------|-----------------|
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
| Hetzner Beast with Docker, Ollama, vLLM, Qdrant, PostgreSQL, Redis, MinIO, Prometheus, Grafana | **Already running.** Core has FalkorDB, Qdrant, LiteLLM, PostgreSQL, backups. Missing: Redis (not needed yet), MinIO (not needed yet), Grafana (not yet configured). Prometheus config exists in `02_build/config/`. | Exists. Fill monitoring gap when pipeline is heavier. |
| LangGraph state machine for orchestration | **Not yet implemented.** Current pipeline is sequential cron (research → generate → queue → evaluate → learn). LangGraph would add: conditional routing, parallel branches, human-in-the-loop breakpoints, state checkpointing. | **Genuine upgrade.** Worth building when pipeline complexity justifies it. |
| RAG grounding / "zero hallucination" | **Already running.** Qdrant (57K embeddings) + FalkorDB (9K nodes) feed the research agent. Content grounded against vault. | Exists. Perplexity overclaims "zero hallucination." Our deterministic sandwich is more honest. |
| OCEAN personality profiling from social media | **Not implemented. Should not be.** Scraping social media for psychographic profiling violates GDPR/DPA 2018 and contradicts our Data Protection Architecture (Amplified never holds personal data). | **Reject as described.** See §Privacy-safe alternative below. |
| VARK learning style detection | **Not implemented.** Interesting for content adaptation but the ANN-based approach Perplexity describes requires individual-level data we don't hold. | **Reject individual profiling. Adapt the concept** — see §Content adaptation below. |
| Remotion programmatic video | **Not in current stack.** React-based, 34.4K GitHub stars, MCP integration as of Jan 2026. GPU rendering on Beast is feasible. | **Genuine addition.** Worth prototyping. |
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
│  ┌─────────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │  FalkorDB   │  │  Qdrant   │  │  PostgreSQL      │  │
│  │  (9K nodes) │  │ (57K emb) │  │  (marketing db)  │  │
│  └─────────────┘  └───────────┘  └──────────────────┘  │
│  ┌─────────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │  LiteLLM    │  │  Remotion │  │  Marketing       │  │
│  │  (proxy)    │  │  (render) │  │  Engine v0.4.0+  │  │
│  └─────────────┘  └───────────┘  └──────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐│
│  │  LangGraph Orchestrator (when justified)            ││
│  │  Content pipeline · Evaluation · Kaizen · Publish   ││
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
- APDS Harvest pulls from: Perplexity searches, RSS feeds, Reddit monitoring, trade press, academic sources.
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

**Content adaptation** (privacy-safe alternative to VARK/OCEAN):
Instead of profiling individuals, adapt content at the **segment level**:
- **By trade**: plumbers get plumbing pain points, electricians get electrical pain points (already implemented in `avatars.py`).
- **By archetype**: Bob (solo, pragmatic), Sheila (professional, quality-driven), Dave (scaling, team coordination), Russell (established, strategic) — already implemented.
- **By channel**: platform-specific tone adaptation (LinkedIn = professional, Facebook = conversational, Reddit = helpful peer, GMB = local and direct).
- **By format preference**: same content, multiple formats (text post, short video, infographic, thread). Let the audience self-select. No surveillance required.

This gives us personalisation without profiling. The intelligence is in the segment model, not in individual tracking.

**Gate:** Every piece of content passes synthetic evaluation (Bob/Lisa/Marcus panel, score ≥ 6/10 per existing system). Content must cite at least one source (radical attribution). Content must pass the transparent prompt check — Amplified speaks as itself.

#### Stage 3: Evaluation

**Inputs:** Generated content from Stage 2.

**Process:**
- Synthetic evaluators (Bob, Lisa, Marcus) score 1–10 on: relevance, honesty, clarity, actionability, attribution.
- Automated checks: source citations present, no claims without backing, tone matches channel, length within bounds.
- Quality routing: ≥7/10 → auto-queue for human review. 5–6/10 → revision queue. <5/10 → reject with feedback to Kaizen.

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
- Multi-platform publishing: LinkedIn, Facebook, Reddit, GMB, email, TikTok (when video pipeline is live).
- Platform API integration: scheduling, formatting, media upload.
- Reddit posts are **never automated**. The Reddit Value Engine (see §Reddit below) uses human-in-the-loop posting.

**Gate:** Content published only at scheduled times. Rate limiting per platform. No duplicate posting.

#### Stage 6: Feedback and Kaizen

**Inputs:** Engagement metrics from published content. Synthetic evaluation scores. Human edit patterns.

**Process:**
- Internal Kaizen (existing, not yet scheduled): analyse feedback patterns → update learned preferences → content agent reads on next generation.
- External Kaizen `[LOGIC TO BE CONFIRMED]`: engagement metrics (likes, comments, shares, DMs, Reddit karma) feed back into research briefs and avatar refinements.
- APDS standing lenses run against new engagement data: "Does this engagement pattern match a known Pudding recipe?"

**What's new vs current:** External engagement metrics feedback loop. APDS integration for pattern discovery in engagement data.

---

## New components (from Perplexity, adapted for Amplified)

### Remotion Video Pipeline `[LOGIC TO BE CONFIRMED]`

**What:** [Remotion](https://github.com/remotion-dev/remotion) (34.4K GitHub stars) creates MP4 videos programmatically using React. As of January 2026, Remotion Agent Skills allow AI-to-video generation via MCP.

**Why:** Video is the highest-engagement format on every platform. Programmatic generation means: same template, different data, hundreds of variations at near-zero marginal cost. GPU rendering on the Beast is feasible.

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
Render Node → server-side MP4 render on Beast GPU
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
- GPU capacity allocation (rendering vs inference — need to benchmark)

**Risk:** Remotion adds significant complexity. **Recommendation:** prototype with one avatar (Bob the plumber), one template, one channel (LinkedIn) before scaling.

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

**Dependencies:**
- Reddit API access (free tier sufficient for monitoring; posting is manual anyway)
- Subreddit list curation (start with 10, expand based on engagement data)
- Human reviewer capacity (initially Ewan; later delegated per Trust Ramp)

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
- [ ] `[DECISION REQUIRED]` Better model access: llama3.1-8b is the current bottleneck. Options: (a) larger local model on Beast GPU, (b) API keys for Claude/GPT for content generation (already using Claude in CRM codebase), (c) hybrid — local for research, API for generation.

### Phase 1: Reddit Value Engine (weeks 3–6)

Lowest complexity, highest alignment with brand values:

- [ ] Set up Reddit API monitoring for 10 target subreddits
- [ ] Wire APDS Harvest to ingest Reddit threads as a source
- [ ] Build intent classifier (high-intent question detection)
- [ ] RAG-grounded draft response generator (Qdrant + FalkorDB → attributed answer)
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

- [ ] Install Remotion on Beast. Benchmark GPU rendering vs inference load.
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
| Claude Sonnet content generation | ~£100–150/month with prompt caching |
| Infrastructure (Hetzner AX162-R) | Already provisioned |
| FalkorDB + Qdrant + PostgreSQL | Running on Core, no additional cost |

Projected additions:

| Item | Estimated cost | Notes |
|------|---------------|-------|
| Remotion rendering | £0 (self-hosted on Beast GPU) | Compute cost already covered. Remotion is open source. |
| ElevenLabs voiceover | ~£5–22/month (Starter–Creator) | `[LOGIC TO BE CONFIRMED]` — local TTS may be sufficient |
| Reddit API | £0 (free tier) | Read-only monitoring. Posting is manual. |
| Platform API integrations | £0–50/month | Depends on tier. Most have free tiers sufficient for our volume. |
| Better LLM access | £50–200/month | `[DECISION REQUIRED]` — depends on model choice |

**Total projected:** £155–420/month for a full-stack, multi-channel, value-first marketing system generating 160+ pieces of content/day with video, Reddit engagement, and closed-loop learning.

---

## Metrics (what we measure)

| Metric | Source | Frequency |
|--------|--------|-----------|
| Content quality (synthetic) | Bob/Lisa/Marcus evaluator scores | Per piece |
| Content quality (human) | Ewan approval/rejection rate | Per review batch |
| Engagement rate | Platform APIs | Weekly |
| Reddit karma + engagement | Reddit API | Weekly |
| Video engagement vs text | Platform APIs | Weekly |
| Content cost per piece | Claude API billing | Monthly |
| Pipeline reliability | Success/failure logs | Per run |
| Kaizen preference drift | Internal Kaizen output | Weekly |
| APDS emergence discoveries | APDS scorer output | Weekly |
| Source citation rate | Automated content check | Per piece |

---

## Open questions (`[DECISION REQUIRED]`)

1. **Model quality:** llama3.1-8b vs Claude API vs hybrid. Content quality is directly gated by model quality. The CRM codebase already uses Claude Sonnet for generation — should the Beast pipeline do the same?

2. **Video brand assets:** Remotion needs branded templates. Who designs them? What's the visual identity?

3. **Delegation threshold:** When content volume exceeds Ewan's review capacity, what are the delegation rules? Trust Ramp provides a framework but specific thresholds are `[DECISION REQUIRED]`.

4. **Covered AI vs Cove:** Per TAXONOMY.md, these are separate products. How does the Marketing Engine relate to each?

5. **Email marketing scope:** The Cove email agent exists. Should marketing emails run through Cove, or through a separate pipeline? Separation of concerns vs infrastructure consolidation.

6. **Reddit account strategy:** Company account? Personal account? Multiple accounts per trade vertical?

---

Signed-by: Devon | 2026-04-30 | devin-0fce62f4c12d4a209748f9daae4ec607

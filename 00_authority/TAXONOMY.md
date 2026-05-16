---
title: Taxonomy — Amplified Partners entity definitions and agent roles
date: 2026-05-16
version: 4
status: draft
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

This file is the single canonical reference for:

1. The Amplified Partners company structure — what each entity is and is not
2. The agent roster — who does what, where the boundaries are
3. Terminology — locked definitions so agents do not confuse similarly-named things

If a name is not in this file, treat it as `[SOURCE REQUIRED]`.

## What this taxonomy is not

This file defines **entities, agents, and locked terminology**. It does **not** assign **cost tiers** to agents (e.g. "Devon = always-Sonnet", "Cassian = always-Haiku"). Cost-tier classification is the job of `cost-tools/token_proxy.py`, which routes per-call based on prompt content (see `01_truth/SYSTEMS-AND-API-REGISTER.md` § 14 and `02_build/INFRASTRUCTURE.md` § AI / ML services). Agent-layer routing (which agent runs which task) lives in `00_authority/AGENT_ROUTING.md`. The two layers stack and are deliberately independent of this file.

---

## Company structure

**Amplified Partners** is the umbrella. Everything below is a function or product within it — not a separate legal entity (unless noted). The legal registration is in progress as of 2026-04-29. Until registration is confirmed, treat `[LOGIC TO BE CONFIRMED]` as the legal status of all sub-entities.

| Entity | Type | What it is | What it is not |
|--------|------|------------|----------------|
| **Amplified Partners** | Umbrella / parent | The business. The brand. The operating entity. | A product. A legal subdivision (yet). |
| **Amplified Core** | Infrastructure | The Hetzner AX162-R server (`amplified-core`, `135.181.161.131`). The physical compute home. PostgreSQL (+ AGE + pgvector), LLM inference, marketing engine. | A team, a product, or a department. Strictly infrastructure. |
| **Amplified Marketing** | Function | The content pipeline and marketing engine. Runs on the Core. Produces social, GMB, LinkedIn content. Evaluated by Bob/Lisa/Marcus synthetic avatars. | The marketing *team* or strategy. The engine that executes the strategy. |
| **Amplified Central Ops** | Function | AI-native governance layer. The clean-build workspace, agent operating contracts, decision logs, authority hierarchy. The spine of how the business runs. | A tech team. Not code. Not infrastructure. The rules and governance that infrastructure runs under. |
| **Amplified Client** | Product tier | The client-facing advisory product for businesses — Bob, Lisa, Marcus. The CRM, the Interview Engine, the federated architecture, the PicoClaw sidecar. | Internal tooling. Does not include personal/consumer products. |
| **Cove** | Product | The WhatsApp-native AI interface for clients. Conversational, channel-based. Where Bob talks to the system. | The Core. Not a server. A product surface. |
| **Covered AI** | Product | `[DECISION REQUIRED]` — distinct from Cove. Definition to be provided by Ewan. Do not conflate with Cove. | Cove. These are separate. |
| **Amplified Personal** | Product | Consumer/public product. Data sovereignty for individuals. Secure personal vault hosting — Amplified cannot see inside it, one click to leave and take everything. | The client business product. This is for individuals, not SMBs. |

**On naming conflicts:**
- **Amplified Core** (the server) ≠ **Amplified Central Ops** (governance). Core = hardware. Central Ops = rules.
- **Amplified Client** (the product) ≠ **client** (a customer of Amplified Partners). Context distinguishes.
- **Cove** ≠ **Covered AI**. These are separate products. Do not use interchangeably. Covered AI definition is `[DECISION REQUIRED]`.

---

## Agent roster

The operating model: each agent is self-contained. Projects are independent. Coordination is not needed day-to-day — clarity of role is what prevents collision. Agents communicate asynchronously through GitHub (STATUS.md) and Slack, not in real time.

| Agent | Name | Core responsibility | Access scope | Reports to |
|-------|------|---------------------|--------------|------------|
| **Devin** | Devon | Infrastructure & systems coordinator. The only agent who writes code to Amplified Core or any production system. Maintains GitHub. Keeps repos clean, cohesive, and canonical. Deploys updates. Sets schedules. Makes everyone else's work better by keeping the foundation solid. | Core (SSH), GitHub, Linear, Slack | OpenClaw (status updates) → Ewan (escalations) |
| **OpenClaw** | Sam / Clawd / Cassian | Partner and coordinator. Lives on Ewan's Mac. Reads vault, processes voice notes, talks to Ewan via Telegram/WhatsApp/Slack. Investigates process failures (not people failures). Maintains shared state. | Local filesystem, all channels, vault, all repos (read) | Ewan directly |
| **Cursor** | — | Builder. Produces code in clean-build workspace. Outputs to GitHub. Does not deploy directly — deployment goes through Devon. | clean-build workspace, GitHub (write to own branches) | Devon (for deployment), Ewan (for direction) |
| **Antigravity / AG** | — | Business Arbiter and COO. Strategic decisions for the firm. Does not direct agent cognition — directs the business. | Strategic review | Ewan |
| **Perplexity** | Comet (in browser) | Researcher. External research, synthesis, brainstorm inputs. | External web | Ewan / whoever runs the session |
| **Qwen** | — | Hive mind. Escalation routing. Collective knowledge base. Novel decisions route here when no agent can own them. | Via clean-build escalation path | — |

---

## Operating model (agent coordination)

The operating model is **isolation with visibility**, not orchestration.

- Each agent works in a self-contained project. No real-time coordination needed.
- Every agent reads `ground-truth` (the portable spine) before acting — so principles and state are shared.
- Every agent writes a handover to `STATUS.md` in `clean-build` when they finish significant work.
- **Devon** is the only agent who touches Amplified Core or production GitHub. Others write to their own branches; Devon integrates.
- **OpenClaw** reads `STATUS.md`, investigates if a process is failing, writes findings back. If infrastructure changes are needed, OpenClaw signals Devon — Devon implements.
- **Slack** is for asynchronous partner communication. OpenClaw communicates there as a partner.
- **Linear** is the record. Each department/function has its own project. Independent. Status visible to all.

The principle: one person does one thing. Clean boundaries. No stepping on each other. The STATUS.md is the handshake point — versioned, structured, no ambiguity about who said what and when.

---

## Terminology — rules

Four meta-rules that resolve capitalisation, spelling, and naming questions across the entire estate. All files, all repos, all agents.

1. **Standard English in prose.** Capitalise proper nouns and sentence starts. Nothing else. No arbitrary title case. No all-caps for concept names in prose.
2. **Standard Python in code.** PEP 8: constants `UPPER_SNAKE`, variables/functions `snake_case`, classes `PascalCase`.
3. **UK English spelling.** `labeller`, `capitalise`, `organise`. The architect is British.
4. **One canonical form per concept.** If a term is in the glossary below, use only the canonical form. If it is not in the glossary, it is not locked — use standard English and move on.

**Pudding dimensions in particular:** in prose, capitalise the first letter only ("the What dimension"). In Python constants, all-caps (`WHAT`, `PATTERN`). In Python variables, `dim_what`, `dim_pattern`.

---

## Terminology — locked glossary

Three columns: the canonical form, what it means, and what not to write. If a term has a code form that differs from the prose form, the code form is shown in backticks after the canonical name.

### Five Rods

Source: Ray Dalio (*Principles*), adapted by Ewan Bramley. Bedrock. Nobody changes these.

| Canonical form | Meaning | Not this |
|----------------|---------|----------|
| **Radical Honesty** | Only claim fact when it is fact. Rod #1. | |
| **Radical Transparency** | Show the reasoning path. Rod #2. | |
| **Radical Attribution** | Every decision has a named source. Rod #3. | |
| **Win-win** | If somebody loses, the decision is wrong. Rod #4. | Win-Win, win win |
| **Idea Meritocracy** | Best idea wins regardless of source. Rod #5. | Ideas Meritocracy, ideas meritocracy |

### Infrastructure

| Canonical form | Meaning | Not this |
|----------------|---------|----------|
| **the Core** · `amplified_core` | Hetzner AX162-R server, `135.181.161.131`. The physical compute home. | Beast, The Beast, the Beast |
| **the vault** · `vault` | Content store at `/opt/amplified/vault/` on the Core. | The Vault, Core Vault |
| **real-vault** | Local Obsidian vault on Ewan's Mac. | the vault (different thing) |
| **clean-build** | The governed agent workspace. GitHub: `Amplified-Partners/clean-build`. | The Core (not infrastructure — governance) |
| **ground-truth** | The portable spine repo. GitHub: `Amplified-Partners/ground-truth`. | clean-build (spine vs workspace) |
| **Mini** · `mini` | Local Mac development environment. | |
| **Air** · `air` | Sandbox / research / discovery environment. | |
| **Byker** | Production system codename on Railway. The factory runtime. | the Core (different infrastructure) |

### Agents

| Canonical form | Meaning | Not this |
|----------------|---------|----------|
| **Devon** · `devon` | Devin platform sessions within Amplified Partners. The phonetic name Ewan uses. Sign as Devon. | Devin (only when referring to Cognition's platform itself) |
| **Sam / Clawd / Cassian** | OpenClaw aliases. Ewan uses all three interchangeably. One agent, three names. | Devon (different agent) |
| **Antigravity / AG** | Business Arbiter and COO. Strategic decisions. | Andy Gravity, A Energy (speech-to-text artefacts) |
| **Cursor** | Builder. Code tasks in clean-build workspace. | |
| **Copilot** | GitHub code suggestions. | |
| **Comet** | Perplexity in-browser. Researcher. | |

### Methodology

| Canonical form | Meaning | Not this |
|----------------|---------|----------|
| **Pudding** · `PUDDING` (constant), `pudding_*` (variables) | Cross-domain discovery methodology. Swanson's LBD adapted by Ewan Bramley + Claude. In prose: "Pudding". In constants only: `PUDDING`. | PUDDING in prose, pudding as common noun |
| **Kaizen** | Continuous refinement. The pipeline itself is subject to Kaizen. | |
| **Swanson** | Don R. Swanson (1924–2012). Literature-based discovery originator. | |
| **LBD** | Literature-based discovery. Abbreviation acceptable alongside full form. | |
| **ABC model** | Swanson's A→B→C bridging logic. | |
| **Compound Engineering** | Each unit of work makes the next unit easier. Attributed to Every (Shipper, Klaassen). | |
| **Plan-Execution Mirror** | Every non-trivial work unit has two receipts: plan before, execution log after. The delta is the learning. | |
| **Portable Spine** | Constitutional framework every agent loads before project-specific instructions. | |
| **Ulysses Clause** | Ewan's pre-commitment: if he overrides the Five Rods, the system removes his ability to override. | |
| **Baton Pass** | Structured handover between sessions. | |

### Data architecture

| Canonical form | Meaning | Not this |
|----------------|---------|----------|
| **PostgreSQL** | The canonical database engine. One instance, three capabilities (relational + graph + vector). | Postgres (acceptable in speech, not in docs or code) |
| **Apache AGE** | PostgreSQL extension for graph queries (openCypher syntax). Not a separate process. | FalkorDB (deprecated), Neo4j (deprecated) |
| **pgvector** | PostgreSQL extension for vector/embedding search (HNSW indexing). Not a separate process. | Qdrant (deprecated) |
| **HNSW** | Hierarchical Navigable Small World. The vector indexing algorithm (Malkov & Yashunin, 2016). | "the Russian maths" (Ewan's informal name — acceptable in speech) |
| **Business Brain** · `business_brain` | The PostgreSQL schema powering the product. Where the Brain lives. | amplified_brain, business_knowledge, knowledge_graph, Unified Business Brain |
| **Cypher** | Query language for graph operations via Apache AGE (openCypher dialect). | |

### Products

| Canonical form | Meaning | Not this |
|----------------|---------|----------|
| **Cove** · `cove_*` (Python), `cove-orchestrator` (Docker) | WhatsApp-native AI interface for clients + the orchestration layer. | Covered AI (separate product) |
| **Covered AI** | Separate product from Cove. `[DECISION REQUIRED]` — definition to be provided by Ewan. | Cove (do not conflate) |
| **Chit** | Ghost sidecar product for multi-person SMBs. Sits beside existing tools. | the CRM (Chit is UI, not data) |
| **PicoClaw** | Beelink N150 mini PC placed on-site at Tier 3+ clients. Client-side hardware. | the Core (not central infrastructure) |

### Pipeline and orchestration

| Canonical form | Meaning | Not this |
|----------------|---------|----------|
| **labeller** · `labeller`, `pudding_labeller` | Component that applies Pudding taxonomy labels. UK spelling. | labeler (US spelling — do not use) |
| **brain writer** · `brain_writer`, `brain_writer_pipeline` | Pipeline that writes extracted knowledge to the Business Brain. | |
| **Temporal** | Workflow orchestration engine (Temporal.io). | |
| **ingestion pipe** · `ingestion_activities` | The pipeline that harvests, extracts, labels, and writes content. | canonical pipeline (vague — avoid) |
| **audit log** · `audit_log` | Append-only record of pipeline actions. | |

### Pudding taxonomy dimensions

| Dimension | In prose | In constants | In variables | What it captures |
|-----------|---------|-------------|-------------|------------------|
| What | "the What dimension" | `WHAT` | `dim_what` | Content subject matter |
| How | "the How dimension" | `HOW` | `dim_how` | Mechanism or methodology |
| Scale | "the Scale dimension" | `SCALE` | `dim_scale` | Level of application |
| Time | "the Time dimension" | `TIME` | `dim_time` | Temporal relevance |
| Pattern | "the Pattern dimension" | `PATTERN` | `dim_pattern` | Recurrence signature |

### Deprecated technology (do not use in new work)

See `00_authority/DATA_ARCHITECTURE.md` (knowledge note) for full migration context.

| Deprecated | Replaced by | References remaining | Action |
|------------|-------------|---------------------|--------|
| FalkorDB | PostgreSQL + Apache AGE | ×1,037 across 9 repos | Migrate graph queries. Mark legacy references. |
| Qdrant | PostgreSQL + pgvector | ×726 across 13 repos | Migrate embeddings. Mark legacy references. |
| Neo4j | PostgreSQL + Apache AGE | ×188 across 3 repos | Never used in production. Remove references. |

**Ratio:** deprecated terms (1,951 occurrences) outnumber canonical replacements (392) by 5:1 as of 2026-05-16.

---

## What is not decided yet (as of 2026-05-16)

- `[DECISION REQUIRED]` — Legal registration of Amplified Partners Ltd. Required before Google My Business can be set up under the brand.
- `[DECISION REQUIRED]` — The confirmed product name for Amplified Personal (content captured in `ground-truth/PERSONAL-VAULT.md` `[SOURCE REQUIRED — not in this repo]`; name deferred by Ewan).
- `[DECISION REQUIRED]` — Covered AI definition. Distinct from Cove. To be provided by Ewan.
- `[LOGIC TO BE CONFIRMED]` — Legal sub-entity structure for each department/product (currently all functions of one entity).

---

## Changelog

### v4 — 2026-05-16

- **Major expansion of terminology section.** Replaced the 13-row flat glossary with a structured terminology law: 4 meta-rules (standard English, standard Python, UK spelling, one canonical form per concept) + 8 category tables covering Five Rods, infrastructure, agents, methodology, data architecture, products, pipeline/orchestration, and Pudding dimensions + deprecated technology table with migration counts.
- **Evidence base:** full estate scan of 32 repos, 1,456 load-bearing files, 155 distinct terms, 28,281 total occurrences. Terminology audit identified 16 major inconsistency clusters; this version locks the canonical forms.
- **Company structure fix:** updated Amplified Core description to reference canonical data stack (PostgreSQL + AGE + pgvector) instead of deprecated FalkorDB/Qdrant.
- **Decisions taken (all reversible, OPINION 88%):** Win-win not Win-Win; Idea Meritocracy not Ideas Meritocracy; labeller not labeler (UK English); Pudding in prose / PUDDING in constants only; Devon not Devin for the agent identity; Business Brain as canonical database name; the Core not Beast for the server. Meta-rule source: Ewan Bramley verbal direction 2026-05-16 ("standard English, standard Python, no arbitrary caps, UK English").
- Frontmatter `version` bumped to v4, `date` to 2026-05-16.

Signed-by: Devon-cb28 | Devin (Cognition AI) | 2026-05-16 | session `devin-cb283993cf974c7babc3307e140d63e4`

### v3 — 2026-05-03

- Added **Cassian** as a canonical alias for OpenClaw (alongside the existing **Sam / Clawd**) in both the agent-roster row and the locked-terminology table. Ewan uses "Cassian" interchangeably with "OpenClaw" / "Clawd" / "Sam" in chat and knowledge notes; this brings the locked terminology in line with established usage so `AGENT_ROUTING.md` and other authority files can use "Cassian" without violating bibliography integrity. **No changes to the company structure or agent roster** — same agent, additional canonical alias.
- Frontmatter `version` bumped to v3.

Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

### v2 — 2026-05-03

- Added § "What this taxonomy is not": an explicit lock that cost-tier classification is the job of `cost-tools/token_proxy.py`, not this file. Agent-layer routing rules live in `00_authority/AGENT_ROUTING.md`. The two layers (model-layer routing in the proxy + agent-layer routing in `AGENT_ROUTING.md`) stack and are independent of this taxonomy.
- No changes to the company structure or agent roster.

Signed-by: Devon-6ca5 | Devin (Cognition AI) | 2026-05-03 | session `devin-6ca57553eefe4806b613070325964703`

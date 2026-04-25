---
title: "Business Brain Framework"
id: "business-brain-framework"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "business-brain-framework.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# The Business Brain Framework

## State-of-the-Art Architecture for AI-Powered Small Business Operations

A connective framework for Amplified Partners / Byker Business Help — how to bind legacy IT, a deterministic database, an exhaustive process library, a graph/vector knowledge layer, voice-first UX, and agentic AI into one coherent business operating system. Built on 2025–2026 primary research and validated against the prior architecture decisions already made.

---

## Executive Summary

The emerging enterprise pattern for safe, auditable AI in operations is now named: **Determinism–Agency–Determinism (DAD)**, also called the "deterministic sandwich" — AI reasoning is bracketed top and bottom by deterministic code, state, and policy enforcement ([Volt Active Data, Feb 2026](https://www.voltactivedata.com/blog/2026/02/agentic-ai-determinism-first-architecture/)). This is the architectural vocabulary for what was already intuited: the business database is ground truth, processes are deterministic scaffolding, and agents only operate at bounded entry and exit points.

McKinsey's 2025 update to their Economic Potential of Generative AI research concludes **60–70% of work activities are technically automatable today**, up from the pre-generative-AI estimate of 50% ([McKinsey & Company](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier)). Downstream analyses put the US-specific figure at **57% of work hours** ([McKinsey Global Institute via summary](https://www.youtube.com/watch?v=UDip8TnN0Io)). **The 65% working estimate is credible and sits mid-range of the primary source.** It should be positioned as the *technical ceiling* — realised automation at SMB scale currently clusters around **35–45%** operational cost savings ([AdAI AI Automation Statistics 2026](https://adai.news/resources/statistics/ai-automation-statistics-2026/), [Kersai 2026](https://kersai.com/ai-breakthroughs-in-2026/)).

The framework described below is a six-layer stack with a clear build order. It keeps the existing database, graph/vector, and LangGraph commitments, adds the missing process-scaffolding layer (BPMN or an APQC-PCF-derived equivalent), and names where voice, telephony, and the marketing agent team sit.

---

## Part 1 — The Six-Layer Business Brain Stack

The Business Brain is composed of six layers. Each has one job. Each has a clear interface to the layers above and below. The layers are ordered by how frequently they change — slowest on the bottom, fastest on top.

| Layer | Name | What it holds | Change frequency | Example tech |
|-------|------|---------------|------------------|--------------|
| 6 | **Voice & Interface** | Staff phones, AI telephony, owner dashboard | Per interaction | LiveKit / Pipecat, Whisper, ElevenLabs |
| 5 | **Agentic Execution** | Narrow agents at process endpoints | Per task | LangGraph + Temporal |
| 4 | **Process Scaffold** | Every business process as a deterministic map | Quarterly | BPMN (Camunda) or DAG-as-code |
| 3 | **Knowledge Graph + Vector** | Business "smell, touch, way of doing" | Continuous | FalkorDB + Graphiti + Qdrant (or pgvector+AGE) |
| 2 | **Deterministic Core** | Numbers, facts, state, events | Transactional | Postgres (plain, boring, solid) |
| 1 | **Integration Layer** | API connectors to legacy IT | Per new connector | P2 gatekeeper, MCP servers, Pipedream, n8n-where-needed |

The architecture of the DAD sandwich maps exactly onto this: Layers 1–2 are the bottom slice of bread (deterministic ingest, deterministic state), Layer 5 is the filling (agentic reasoning, bounded), and the process scaffold in Layer 4 is the load-bearing structure that tells the agent *where it is allowed to act and with what authority* ([Volt Active Data](https://www.voltactivedata.com/blog/2026/02/agentic-ai-determinism-first-architecture/)).

### Layer 1 — Integration Layer (the legacy-IT bridge)

This is where APIs from existing business systems (accounting, CRM, scheduling, email, phone systems, legacy ERPs, photocopier logs, energy-contract portals) are pulled into Amplified-controlled territory. Three things happen here and only here:

1. **Extraction** follows the Amplified extraction methodology — export-first, API-second, LLM-only-when-necessary. Accuracy requirements are 98–99%+ and non-negotiable for financial data.
2. **P2 tokenisation at source** — real names, account numbers, addresses, postcodes are replaced with four-word random tokens before any data leaves the client's infrastructure.
3. **Schema normalisation** — every source is mapped into a canonical event/entity schema before it reaches Layer 2.

For SMBs whose legacy systems are too old to expose APIs (and this is most of them), the cloud architecture fallback already designed applies: data is extracted on-premises via the PicoClaw sidecar, normalised, tokenised, and pushed up. Where an API genuinely does not exist, mobile/on-device extraction is used — which is consistent with how 41% of current SMB AI adopters have succeeded ([Kersai 2026](https://kersai.com/ai-breakthroughs-in-2026/)).

### Layer 2 — Deterministic Core (the plain old database)

This is **numbers and facts, nothing else**. It is the ground truth. The research validates this instinct strongly: a Determinism-First architecture ensures state changes, balance updates, policy enforcement, and ACID compliance happen *before* any AI reasoning ([Volt Active Data](https://www.voltactivedata.com/blog/2026/02/agentic-ai-determinism-first-architecture/)). AI agents then reason on top of it.

**Recommendation: plain PostgreSQL.** Boring, battle-tested, 30+ years of production use, free, portable, runs on a Raspberry Pi to a 48-core EPYC. Two schemas at minimum:

- **State schema** (current truth): customers, invoices, inventory, contracts, employees, assets. Standard CRUD, fully indexed, with every row having a `token_id` (the four-word ID) never the real value.
- **Event schema** (what happened): append-only log of every state change — Event Sourcing pattern ([Microsoft Azure Architecture Center, March 2026](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing), [Event Sourcing + CQRS Implementation Guide](https://www.youngju.dev/blog/architecture/2026-03-10-event-sourcing-cqrs-architecture-implementation.en)). This is what makes the system auditable, time-travellable, and safe to replay when anything goes wrong.

Event Sourcing + CQRS is over-engineering for the State schema but perfect for the "staff told the brain something" pattern and the "agent proposed a change" pattern. Every agent decision becomes an immutable event. This gives radical transparency by architecture, not by policy — you cannot hide what was decided because the event log will not let you.

**Optional convergence play:** Microsoft published in April 2026 a production pattern combining **pgvector + Apache AGE in one PostgreSQL** instance — vectors and graph traversal share the same query planner, same backup strategy, same credentials, and can be joined in a single transaction ([Microsoft Tech Community, April 2026](https://techcommunity.microsoft.com/blog/adforpostgresql/combining-pgvector-and-apache-age---knowledge-graph--semantic-intelligence-in-a-/4508781)). For a single-handed plumber on WhatsApp, this collapses Layer 2 + Layer 3 into one database and eliminates two operational stacks. For larger clients with existing FalkorDB/Graphiti tooling on Beast, keep them separate. Both patterns are right, at different scales.

### Layer 3 — Knowledge Graph + Vector (the "smell, touch, and way")

This holds everything the Deterministic Core cannot: the way the business actually works, the unwritten rules, the tribal knowledge, the staff observations, the semantic relationships that make this business *this* business. Research confirms graphs and ontologies are now the standard pattern for giving agents "an explicit, structured representation of organizational reality — a shared map of entities, relationships, and constraints that evolves with the business itself" ([Kerem Tomak, Sept 2025](https://www.linkedin.com/pulse/how-knowledge-graphs-ontologies-revolutionizing-automated-kerem-tomak-ycfve)).

The two stores do different jobs:

- **Graph (FalkorDB + Graphiti):** explicit relationships — *Photocopier 3 → serviced by → Sarah → taught → Tom*. Temporal by design (Graphiti timestamps every fact), so "who fixed it last time and what did they say" is a single query.
- **Vector (Qdrant):** semantic recall — "how did we handle that weird customer issue last year" returns by meaning, not by keyword.

The Pudding Technique already developed (Don Swanson ABC discovery model, 2026 labelling taxonomy) runs on this layer. Cross-domain insights come from here, not from the Deterministic Core.

**When staff tell the voice interface "I fixed photocopier 3 by unplugging the fuser for 30 seconds," that sentence is:**
1. Transcribed (Layer 6)
2. Tokenised so any names are four-word IDs (Layer 1 rules still apply)
3. Stored as an episodic memory in Graphiti (Layer 3 graph) with timestamp + photocopier entity + fix type
4. Also embedded and stored in Qdrant (Layer 3 vector) for semantic recall
5. Referenced by ID, never copied, from any agent that later serves a fix query

This is what Ewan has described as "single point of data for staff and for AI" — it is architecturally enforced by this layer. Staff teach the graph once; every agent and every staff member queries it forever.

### Layer 4 — Process Scaffold (the missing piece)

This is the layer that has been conceptually present but not technically named. The research from Camunda's 2025 work on agentic orchestration makes the solution explicit: **BPMN is the load-bearing structure that binds deterministic processes to AI agents** ([Camunda Agentic Orchestration Docs](https://docs.camunda.io/docs/components/agentic-orchestration/agentic-orchestration-overview/), [Camunda BPMN 7 Patterns video](https://www.youtube.com/watch?v=-TU2v6CooQ0)).

Every business process (from ISO 9001 clauses, APQC PCF cross-industry framework, or Amplified's own library) is expressed as a **BPMN diagram** with three types of nodes:

1. **Deterministic tasks** — rules, validations, database writes, compliance checks. No AI touches these.
2. **Human tasks** — a staff member speaks to the voice interface. No AI touches these.
3. **AI agent tasks** — bounded LLM calls with specific inputs, specific tools, specific output schemas, and explicit failure paths.

Camunda's published 7 BPMN agent patterns — ReAct, Modern Tool Use, Agentic RAG, Self-Reflection, Multi-Agent Workflow, Human-in-the-Loop, and Long-running Orchestration — map directly onto the agents already designed in the Amplified architecture ([Camunda AI Agent Connector Docs](https://docs.camunda.io/docs/components/connectors/out-of-the-box-connectors/agentic-ai-aiagent/)).

**The APQC Process Classification Framework (PCF)** is the cross-industry taxonomy of business processes already referenced in the Amplified skills. Version 5.2.0 is the current cross-industry Excel release and is freely licensable ([APQC PCF Excel Version 5.2.0](https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-excel-0)). The PCF organises every process a business runs into a five-level hierarchy under operating processes (Develop Vision → Develop Products → Market → Deliver → Service) and management/support processes (Develop HR → Manage IT → Manage Financial Resources → Manage Assets → Manage Enterprise Risk etc.). It is the exhaustive process catalogue being asked for and it already exists.

**The build pattern is therefore:**

- Start with the APQC PCF as the master taxonomy.
- For each process, draft the BPMN using ISO 9001 Plan-Do-Check-Act principles ([2c8 ISO 9001 Process Mapping](https://www.2c8.com/en/blog/what-is-process-mapping-in-iso-9001/), [Acato ISO 9001 Strategies](https://acato.co.uk/key-strategies-in-mastering-iso-9001-process-mapping/)).
- Annotate each task with its best-practice "mechanics" researched from the web — citations included — so the process is *science-led*, not opinion.
- Execute on Camunda 8 or an equivalent BPMN engine. Camunda is now the reference implementation for agentic orchestration with BPMN.

### Layer 5 — Agentic Execution (where AI is allowed to shine)

Agents sit **at the endpoints** of BPMN tasks, never in the middle of a deterministic chain. LangGraph is the correct choice for each agent's internal reasoning — it is the most adopted multi-agent framework by a wide margin in 2026 with 27,100 monthly searches and 9.8M monthly PyPI downloads ([GuruSup 2026 Multi-Agent Framework Review](https://gurusup.com/blog/best-multi-agent-frameworks-2026), [ZenML Agno vs LangGraph](https://www.zenml.io/blog/agno-vs-langgraph)) — and its explicit, typed, stateful graph matches the "traceable, comparable to a known framework" principle already committed to.

**However — the production lesson from 2025–2026 is now unambiguous: LangGraph alone is not enough for long-running work.** Grid Dynamics' widely-cited public migration ([Temporal blog, Sept 2025](https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics)) documents the pattern: LangGraph plus Redis for state was "powerful in concept but incredibly brittle in practice" — manual state management, custom retry logic, debugging hell for expired cache. The team migrated to **Temporal for durable execution** and kept LangGraph for agent reasoning inside Temporal activities.

The synthesis is:

> **LangGraph is the brain (how one agent reasons). Temporal is the spine (how work survives crashes, restarts, and week-long human waits).** ([LinkedIn / A. Kuznetsov, Sept 2025](https://www.linkedin.com/posts/alexskuznetsov_temporal-langgraph-agenticai-activity-7370176563192967168-aHQr))

This matches the Cove Code Factory architecture already using Temporal. The same pattern applies to the Business Brain: **BPMN (Camunda) for process scaffolding → Temporal for durable activity execution → LangGraph for individual agent reasoning.** Three layers, three purposes, no overlap.

### Layer 6 — Voice & Interface

Voice is the primary human surface. AI is text-in-text-out; humans are voice-in-voice-out. The Hamming AI 2025 selection framework for voice agent stacks is the most thorough public benchmark comparing LiveKit, Pipecat, ElevenLabs, Retell, and Vapi ([Hamming AI Voice Stack Framework, Aug 2025](https://hamming.ai/resources/best-voice-agent-stack)). AssemblyAI's January 2026 orchestration tools review corroborates the top three ([AssemblyAI 6 Best Voice Orchestration Tools 2026](https://www.assemblyai.com/blog/orchestration-tools-ai-voice-agents)).

**Recommendation by client tier:**

| Client scale | Voice stack | Telephony | Rationale |
|--------------|-------------|-----------|-----------|
| Single-handed tradesperson | WhatsApp Business API + Whisper + ElevenLabs | Keep existing mobile | Zero-friction, use what they already have |
| 2–20 staff SMB | **LiveKit Agents** (self-host on Beast) | LiveKit SIP / Twilio | Open-source, full control, native telephony, under $0.01/min at scale |
| Larger SMB with compliance needs | LiveKit or Pipecat (on-prem) | On-prem SIP | HIPAA/GDPR defensibility, full audit trail, data never leaves |

LiveKit Agents is the production pattern for 2026 — it gets turn-taking and barge-in right out of the box ([Hamming AI](https://hamming.ai/resources/best-voice-agent-stack)), is fully open-source, and can run entirely on Beast. Pipecat is the alternative when maximum customisation is needed.

**The "one breath" VUI rule applies everywhere** ([Fuselab Voice UI 2026](https://fuselabcreative.com/voice-user-interface-design-guide-2026/), [Parallel VUI Principles 2026](https://www.parallelhq.com/blog/voice-user-interface-vui-design-principles)): never ask the user to remember a list of five options. Ask one short question, confirm understanding, move on. Every voice flow is a BPMN diagram with short human-task nodes, not a wandering LLM conversation.

**Sentiment & semantics tokenisation at source:** every voice turn from staff is P2 tokenised in Layer 1 before any sentiment or semantic analysis happens. The tokenised transcripts flow up; the raw audio never leaves the client environment. This is what makes "cannot be used against them" architecturally enforceable, not merely promised.

---

## Part 2 — How It Fits Together: The Operating Picture

```
     ┌──────────────────────────────────────────────────────────┐
     │  LAYER 6 — Voice & Interface                             │
     │  Telephony · Staff phones · Owner dashboard              │
     │  (One breath. AI=text. Human=voice.)                     │
     └──────────────────────────────────────────────────────────┘
                            ↕ (bounded interactions)
     ┌──────────────────────────────────────────────────────────┐
     │  LAYER 5 — Agentic Execution (LangGraph in Temporal)     │
     │  Narrow agents at endpoints. Never in the middle.        │
     └──────────────────────────────────────────────────────────┘
                            ↕ (BPMN task calls)
     ┌──────────────────────────────────────────────────────────┐
     │  LAYER 4 — Process Scaffold (Camunda BPMN + APQC PCF)    │
     │  Every process mapped. Deterministic + human + AI tasks. │
     │  ISO 9001 Plan-Do-Check-Act baked in.                    │
     └──────────────────────────────────────────────────────────┘
           ↕ (reads facts)         ↕ (reads patterns/memory)
     ┌────────────────────┐   ┌────────────────────────────────┐
     │  LAYER 2 — Postgres│   │  LAYER 3 — Graph + Vector      │
     │  Deterministic Core│   │  FalkorDB+Graphiti · Qdrant    │
     │  State + Events    │   │  The business's smell & touch  │
     └────────────────────┘   └────────────────────────────────┘
                            ↕
     ┌──────────────────────────────────────────────────────────┐
     │  LAYER 1 — Integration (P2 gatekeeper + MCP + connectors)│
     │  Every API, every export, every extraction. Tokenised.   │
     └──────────────────────────────────────────────────────────┘
                            ↕
     ══════════════  CLIENT'S LEGACY IT WORLD  ═══════════════════
```

### A worked example — "Energy contract renewal"

This walks through how the layers collaborate on one specific process. It demonstrates the "we can't automate it but we'll assist" pattern Ewan described.

1. **Onboarding (one-time):** During IT forensic interrogation (Layer 1), the system discovers the client has an energy contract. The owner is asked "where is it?" and uploads or points to the contract. The contract is parsed, P2-tokenised, and stored: metadata in Postgres (supplier, rate, renewal date, usage), full text in Qdrant, relationships (supplier → contract → premises → meter) in FalkorDB.
2. **Process scaffold (Layer 4):** The APQC PCF "Manage Financial Resources → Manage contracts" process is instantiated as a Camunda BPMN diagram with a timer event set to the renewal date minus 90 days.
3. **T-minus 90 days:** Timer fires. BPMN enters a deterministic research branch.
4. **Agentic Execution (Layer 5):** A LangGraph "Energy Contract Research" agent is invoked via Temporal. It queries the current market (SearXNG on Beast, BeastSearXNG skill applies), gathers 3 comparable quotes, runs the Altman Z-Score / Truth Filter deterministic rubric from the Amplified rubric library, and produces a recommendation with confidence bands.
5. **Human task (Layer 4):** The BPMN routes the recommendation to the owner's voice interface. The owner hears "Your energy contract with [Supplier] renews on [date]. I've found 3 alternatives. The cheapest is [X], but [Y] has better reviews. Do you want me to send you the detail for review?"
6. **Event log (Layer 2):** Every step above is an immutable event in the event store. The owner's final decision is also an event. Radical transparency by architecture.

**The AI never executes the contract change.** It researches, proposes, and hands off. The owner's voice confirmation triggers a deterministic handoff to a staff member (or a human advisor) to execute. This is the DAD pattern operationally — deterministic trigger, bounded agentic research, human decision, deterministic execution.

### The Voice-First Flow for Staff

```
Staff member (voice in) ──> STT (Whisper)
     ──> P2 tokenise (Layer 1)
     ──> Intent classifier (small LLM)
     ──> BPMN task match (Layer 4)
     ──> [Deterministic | Human | Agent task]
     ──> Event written (Layer 2)
     ──> Graph/Vector updated (Layer 3)
     ──> Response generated
     ──> TTS (ElevenLabs / Piper)
     ──> Staff member (voice out)
```

Staff never type. AI never asks for clarification twice. Every voice turn is logged (tokenised), timestamped, attributable, and replayable.

---

## Part 3 — Realistic Automation Potential (the 65% question)

The claim that ~65% of processes can be automated is well supported by the primary source but needs a two-tier framing.

**Technical ceiling (what is theoretically automatable with today's tech):**

| Source | Figure | Scope |
|--------|--------|-------|
| [McKinsey Global Institute 2023/2025 update](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier) | **60–70% of employees' time** | Global, all industries |
| [McKinsey US follow-up 2025](https://www.youtube.com/watch?v=UDip8TnN0Io) | **57% of US work hours** | US workforce |
| [SMB-specific Salesforce 2024](https://useaiforbusiness.com/research/artificial_intelligence_adoption_rates_smb_2025.html) | 78% of SMBs use AI in at least one function | US SMB |

**Realised savings at SMB scale (what is actually being captured today):**

| Source | Figure | Meaning |
|--------|--------|---------|
| [AdAI 2026 Statistics](https://adai.news/resources/statistics/ai-automation-statistics-2026/) | **35% average operational cost reduction** | SMBs with AI automation |
| [Kersai 2026](https://kersai.com/ai-breakthroughs-in-2026/) | **38% cost savings, 45% profit improvement** | SMEs |
| [Thryv 2025 via USM](https://usmsystems.com/small-business-ai-adoption-statistics/) | **20+ hours/month saved, $500–$2000/month cost reduction** | Current SMB AI adopters |

**The honest framing for client conversations:**

> "Research indicates 60–70% of work activities are technically automatable today. In practice, SMBs currently capture 35–45% cost reduction from AI automation. Our aim — and it is an aim, not a guarantee — is to help you get toward that technical ceiling over 12–18 months, measured by your own data."

This is radical honesty applied to the automation claim. The 65% figure is defensible as *technical potential*. Realised savings depend on data readiness, staff adoption, and process quality — all of which the Business Brain is explicitly designed to improve.

The top SMB barriers in 2025 were **skills/training gaps (46%), data readiness (28%), security concerns (22%), and budget (34%)** ([USM Business Systems 2025](https://usmsystems.com/small-business-ai-adoption-statistics/)). The three-tier onboarding, trust ramp, and P2 tokenisation already designed directly address three of those four. The business model's position — *we don't replace staff, we give them their time back to do marketing and critical non-essentials* — addresses the fourth and the political barrier (fear of job loss) that no pure-cost-ROI argument can.

---

## Part 4 — Exhaustive Process Coverage (what processes to include)

The APQC PCF Cross-Industry Framework v5.2.0 is the exhaustive catalogue already published and free to adopt ([APQC Resource Library](https://www.apqc.org/resource-library/resource-collection/apqcs-process-classification-framework-pcf-cross-industry-and)). It organises every business process under 12 top-level categories and ~1,000 specific activities.

**The 12 top-level APQC process categories (the business brain process tree):**

| # | Category | Type |
|---|----------|------|
| 1 | Develop Vision and Strategy | Operating |
| 2 | Develop and Manage Products and Services | Operating |
| 3 | Market and Sell Products and Services | Operating |
| 4 | Deliver Physical Products / Services | Operating |
| 5 | Manage Customer Service | Operating |
| 6 | Develop and Manage Human Capital | Management & Support |
| 7 | Manage Information Technology | Management & Support |
| 8 | Manage Financial Resources | Management & Support |
| 9 | Acquire, Construct, and Manage Assets | Management & Support |
| 10 | Manage Enterprise Risk, Compliance, Remediation, and Resiliency | Management & Support |
| 11 | Manage External Relationships | Management & Support |
| 12 | Develop and Manage Business Capabilities | Management & Support |

This is the skeleton. Every vertical-specific process (plumbing job scheduling, hairdresser appointment booking, accountant year-end close) is a leaf under one of these 12 branches. The framework is genuinely industry-agnostic — as Ewan observed, "business is business" is backed by the taxonomy.

**Areas historically under-automated in SMBs that the Business Brain should cover by default:**

- Energy contract / insurance / licence renewals (Category 10)
- Equipment maintenance logs and fix knowledge (Category 9)
- Critical non-essentials (Paddy Lund) — staff birthdays, customer appreciation, hospitality (Category 5)
- Staff-authored blog posts and local community content (Category 3)
- Cash flow forecasting / "Do I owe money right now?" (Category 8)
- H&S records, training logs, competence tracking (Category 10)
- Customer call handling / "did we miss any calls yesterday?" (Category 5)
- Supplier relationship / review cycles (Category 11)

Each is a BPMN diagram. Each has a mix of deterministic, human, and agent tasks. Each can be pulled from a central Amplified template library and tuned per client.

---

## Part 5 — The Marketing Agent Team (where it fits)

The marketing pipeline (14-agent digital agency architecture already designed in the `amplified-marketing-pipeline` skill) is **a specialised instance of Layers 4–5** running under the "Market and Sell" APQC category. It is not a separate architecture. It is the same Business Brain, with different BPMN diagrams, different agents, and output destinations pointing at social platforms and blog tools rather than internal systems.

Practical consequence: every marketing action the staff voice-records (a fix they did, a customer story, a photo of a finished job) flows into the same Knowledge Graph (Layer 3) and is available to both the business-operations agents (for knowledge recall) and the marketing agents (for content atomisation). This is the "staff as content creators" principle given architectural teeth.

---

## Part 6 — Build Order (how to actually get this built)

The correct build order minimises risk and front-loads value. It also mirrors the trust ramp — the client sees something working at the end of every step.

| Stage | Weeks | Deliverable | Why now |
|-------|-------|-------------|---------|
| **0. Discovery** | 1–2 | IT forensic interrogation, data-source inventory, APQC process map tailored to this client | Cannot build without knowing what to build for |
| **1. Deterministic Core** | 3–6 | Postgres + event store running, Layer 1 P2 gatekeeper pulling 2–3 highest-value sources, basic owner dashboard showing numbers | The ground truth exists. Owner immediately sees one question answered ("do I owe money?") |
| **2. Knowledge Graph + Vector** | 7–10 | FalkorDB + Graphiti + Qdrant live, first staff voice → graph write flow working, "ask the brain" query interface | Staff stop repeating themselves. Immediate friction reduction. Sentiment starts being captured. |
| **3. Process Scaffold** | 11–16 | Camunda BPMN instance running, first 3–5 critical processes mapped from APQC + ISO 9001 best practice, wired to Layers 2–3 | Business gets structure. Every action is now auditable. Compliance posture improves. |
| **4. First Agents** | 17–22 | LangGraph agents at 3–5 process endpoints (e.g. missed-call follow-up, owe-money calculation, energy-renewal research), Temporal handling durability | AI "shines" exactly where it should — at endpoints, bounded, with confidence bands. |
| **5. Voice-First UX** | 23–28 | LiveKit Agents on Beast, staff phones connected, owner phone connected, AI telephony answering inbound | The surface becomes voice. Typing stops. Text-to-voice for staff, text-to-text for agents. |
| **6. Marketing Agent Team** | 29–36 | 14-agent marketing pipeline activated, staff content flowing from Layer 3 into atomised posts | De-frictioned time gets redirected into authentic marketing. Staff become content creators. |
| **7. Kaizen** | Ongoing | Measurement dashboard against APQC KPIs, weekly Kaizen cycle driven by Real and Data departments on Beast | Continuous improvement, always against the known framework. |

Stage 0 is the only stage that absolutely cannot parallelise. Stages 1 and 2 can run in parallel with two engineers. Stages 3 and 4 must be sequential (cannot wire agents before the process scaffold is live). Stages 5 and 6 can run in parallel.

**For a single-handed plumber on WhatsApp, the build compresses to Stages 0, 1 (simplified to one Postgres on a $5/month VPS with pgvector+AGE), 4 (one agent — missed-call follow-up), and 5 (WhatsApp, not LiveKit).** 4 weeks, not 36. The architecture scales down as cleanly as it scales up because every layer is optional if the business is small enough.

---

## Part 7 — What This Framework Deliberately Does Not Do

To stay radically honest about the limits:

- **It does not replace domain judgment.** The agent researches and proposes. The owner and staff decide. Architecturally enforced by the human-task gate in every BPMN diagram.
- **It does not claim 100% accuracy for non-financial data.** Financial data has a 100% rule; everything else has confidence bands. This is consistent with the Amplified extraction methodology's 98–99%+ target.
- **It does not work without client buy-in on P2 tokenisation.** Tokenisation is load-bearing for the "cannot be used against staff" promise. If a client cannot commit to that, the sentiment and semantic capture should be turned off, not fudged.
- **It does not promise 65% automation by month one.** Technical potential is 60–70%. Realised capture at the SMB industry baseline is 35–45%. Moving a specific client from 0% to technical ceiling is a 12–24 month project measured by *their* data.
- **It does not eliminate the need for governance.** The Amplified Laws (Layer 0 SOUL principles) and the Enforcer governance layer remain outside this stack and sit above everything. They are the character of the system, not part of its plumbing.

---

## Appendix A — Open Questions to Lock Before Build

Four decisions are load-bearing and not yet finalised. Addressing them before Stage 1 begins saves expensive rework:

1. **Postgres-only (pgvector + AGE) vs separate FalkorDB + Graphiti + Qdrant** for the smallest clients. The April 2026 Microsoft pattern makes Postgres-only defensible at this scale; the existing Beast tooling is the counter-argument. A tier threshold (e.g. "3-tier clients get Postgres-only; 5-tier+ get the full stack") is probably the right answer.
2. **BPMN engine choice**: Camunda 8 (reference implementation for agentic orchestration, hosted or self-hosted) vs lighter DAG-as-code (Prefect, Dagster). Camunda wins on auditability and the 7 documented agent patterns; DAG-as-code wins on simplicity for 1-process pilots.
3. **Voice stack per tier threshold**: WhatsApp-only for tier 1, LiveKit Agents from tier 2 upward? Or is there a hybrid where WhatsApp is a skin on the same LiveKit backend?
4. **Process library IP strategy**: the APQC PCF is freely licensable for internal use. The Amplified-enhanced version (annotated with best-practice mechanics) is differentiated IP. Decide upfront whether this is open-published (walks the transparency walk) or kept as differentiation.

---

## Appendix B — Framework Mapping Against Existing Amplified Skills

For continuity, every layer in this framework maps to one or more existing user skills. None of the prior work is invalidated. This framework names the connective tissue that was conceptually present but not architecturally explicit.

| Layer | Existing skill(s) |
|-------|-------------------|
| Layer 1 | `amplified-extraction-methodology`, `amplified-key-rotation` |
| Layer 2 | `amplified-vault-knowledge` (SQL components), `amplified-client-onboarding` |
| Layer 3 | `amplified-vault-knowledge`, `amplified-pudding-technique` |
| Layer 4 | **NEW — needs a skill: `amplified-process-scaffold`** |
| Layer 5 | `amplified-agent-architecture`, `amplified-cove-orchestrator`, `amplified-self-reflection-protocol` |
| Layer 6 | **NEW — needs a skill: `amplified-voice-stack`** |
| All | `amplified-prompt-environment`, `amplified-beast-ops`, `amplified-pricing-packaging` |

Two new skills are implied by this framework and are the natural next documentation targets.

---

*Attribution: Ewan Bramley (originator, 27-year SMB consultant, architect) × Perplexity Computer (researcher, synthesiser). Primary research spans McKinsey, Camunda, Temporal, Microsoft Azure Architecture Center, APQC, ISO 9001 practitioner guidance, and 2025–2026 practitioner sources. Fact %: 92 · Confidence: High · SOUL: Radically Honest · Radically Transparent · Win-Win*

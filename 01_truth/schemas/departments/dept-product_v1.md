---
title: "Dept Product"
id: "dept-product"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "dept-product.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — Product & Client Experience
## Deep Memory Extraction
### Compiled: 27 March 2026 | Source: Perplexity Memory + Workspace Files

---

> **Scope**: This document captures everything known about Amplified Partners' product suite, client experience design, onboarding philosophy, pricing architecture, and UX philosophy. Drawn from the knowledge reconstruction document, Beast operations skill, key rotation skill, and Linear workspace data.

---

## Table of Contents

1. [Product Suite Overview](#1-product-suite-overview)
2. [DocBench — Data Extraction Engine](#2-docbench--data-extraction-engine)
3. [The Pulse — Client Interface & Nudge Engine](#3-the-pulse--client-interface--nudge-engine)
4. [Finance Engine](#4-finance-engine)
5. [Amplified Video](#5-amplified-video)
6. [Vault Extraction Pipeline](#6-vault-extraction-pipeline)
7. [Client Onboarding Process](#7-client-onboarding-process)
8. [The Jesmond Plumbing Pilot](#8-the-jesmond-plumbing-pilot)
9. [Business Vault Architecture Per Client](#9-business-vault-architecture-per-client)
10. [Pricing Model & Tier Structure](#10-pricing-model--tier-structure)
11. [AI Sidecar & Shadow Mode Integration](#11-ai-sidecar--shadow-mode-integration)
12. [The Trust Ramp — Autonomous Transition](#12-the-trust-ramp--autonomous-transition)
13. [Practice-in-a-Box Concept](#13-practice-in-a-box-concept)
14. [Client-Facing Features — Morning Briefing & The Pulse Nudges](#14-client-facing-features--morning-briefing--the-pulse-nudges)
15. [Strangler Fig Migration Pattern](#15-strangler-fig-migration-pattern)
16. [UX Research & Philosophy](#16-ux-research--philosophy)
17. [Commercial Products from Pipeline](#17-commercial-products-from-pipeline)
18. [Gaps & Unknowns](#18-gaps--unknowns)

---

## 1. Product Suite Overview

Amplified Partners has five named products, a pipeline of commercial derivative products, and a clear infrastructure layer that supports them all.

### Core Product Map

| Product | Function | Status |
|---------|----------|--------|
| **DocBench** | Data extraction engine for client onboarding | Defined, specification exists |
| **The Pulse** | Client interface / text-based nudge engine | Phase 1 pilot: Jesmond Plumbing |
| **Finance Engine** | Financial analysis API with death spiral scoring | Deployed (v1.3.1 on Beast) |
| **Amplified Video** | Video production system using 5.4M word corpus | Specification exists (V5, 6,766 lines) |
| **Vault Extraction Pipeline** | Multi-stage document processing pipeline | Architecture defined |

### Commercial Products from Pipeline

1. **TAXONOMY ENGINE** — categorisation and labelling system
2. **Amplified Quality System (AQS)** — quality assurance framework
3. **Micro-Help Library** — small business help content system

### Supporting Infrastructure

All products run on the Beast (Hetzner AX162-R) via Docker containers behind Traefik, with:
- FalkorDB (graph DB) for the Business Brain
- Qdrant (vector DB) for semantic search
- PostgreSQL for structured data
- LiteLLM as single AI gateway
- SearXNG for self-hosted search (243+ sources)

---

## 2. DocBench — Data Extraction Engine

### Core Function

DocBench is the data extraction engine that forms the foundation of client onboarding. It integrates with a client's existing IT infrastructure to pull and structure their institutional knowledge.

### Data Sources (Integrations)

- **Emails** — historical and ongoing correspondence
- **Invoices** — financial document trail
- **Contracts** — legal and commercial agreements
- **Support tickets** — customer service history and patterns

### Four Output Formats

DocBench processes raw source data and produces four structured output types:

| Output Format | Description |
|---------------|-------------|
| **Raw text** | Unprocessed extracted content |
| **Structured JSON** | Machine-readable, schema-validated data |
| **Process & logic** | Operational procedures derived from the data |
| **Principles & values** | Cultural/philosophical patterns extracted from communications |

### Position in Pipeline

DocBench feeds into the broader Vault Extraction Pipeline:

```
Client Data Sources → DocBench → PUDDING Labelling → 8 Output Streams
```

The 8 output streams include: Content Creation, Process & Logic Giveaway, Ewan's Book, Complete Comprehensive Document, The Manifesto, Onboarding, plus additional streams.

### Technical Context

- The Cove Code Factory (Temporal-based pipeline) is the build infrastructure that produces and manages DocBench
- Strategy: Assemble pre-built, vetted open-source components from GitHub — not write from scratch
- All code: deterministic, privacy-first, security-accredited (Cyber Essentials target)
- P2 tokenisation applied to all sensitive client data before it leaves the client's premises

---

## 3. The Pulse — Client Interface & Nudge Engine

### Core Function

The Pulse is the primary client-facing product — a text-based nudge engine that delivers overnight insights and "wins" to business owners each morning. It is the interface layer between Amplified Partners' AI analysis and the human business owner.

### Design Philosophy

Three governing principles:

1. **Calm Technology** (Mark Weiser / John Seely Brown, Xerox PARC) — Technology should fade into the background. The Pulse does not demand attention; it earns it.
2. **Behavioural psychology** — Nudges are timed, framed, and personalised based on psychological profiles
3. **Personality-adaptive** — Content adapts to the client's personality profile, learning style, and tone preference

### Personalisation Inputs

The Pulse adapts based on:
- **Personality profiles** (DISC profiling at higher tiers)
- **Learning styles** — visual, text, numerical preferences
- **Tone preference** — formal, casual, direct, gentle
- **Historical response data** — what nudges the owner actually acts on

### Phase 1 Pilot

**Client**: Jesmond Plumbing  
**Interface**: Phone PWA (Progressive Web App)  
**Feature**: Morning Briefing flow  
See Section 8 for full pilot detail.

### The "Morning" Flow

The Pulse delivers a structured morning briefing sequence — a digest of overnight analysis, priority actions, and context-aware nudges. The flow is:
1. Business summary from overnight AI analysis
2. Top 3 priority items (ranked by impact × urgency)
3. One suggested action ("Your move for today")
4. Optional: deeper drill-down if the owner wants more

### Nudge Philosophy

- **Only show data if it changes behaviour**: "We only show data if a normal person in your shoes would naturally want to do something different after seeing it. If not, it's just decoration."
- **Owner moves the sliders**: The system shows what usually happens when people set sliders like that — the client makes the choice
- **Libertarian paternalism**: AI optimises the route to the client's chosen destination — ethical persuasion, not manipulation

---

## 4. Finance Engine

### Core Specifications

| Field | Value |
|-------|-------|
| **Version** | v1.3.1 |
| **Deployment** | Beast (Hetzner) |
| **Port** | 8700 |
| **API Route** | `api.amplifiedpartners.ai/api/v1/finance/*` |
| **Container** | `finance-engine` |
| **First deployed** | 13 March 2026 (COV-254) |

### Key Features

**Death Spiral Scoring** — The Finance Engine's signature feature. Identifies patterns in financial data that indicate a business is entering a self-reinforcing decline spiral (falling revenue → cost-cutting → service degradation → further revenue loss). The score surfaces this risk before it becomes unrecoverable.

**Companies House XBRL Parser (CH Pipeline)**:
- Separate container: `ch-pipeline` on port 8750
- Parses XBRL-format company filings from Companies House (UK government registry)
- Enables the FREE tier (£0) — pulling public company data without client involvement
- Deployed: 13 March 2026 (COV-260)

### Data Architecture

- Free tier uses Companies House public data (no client data integration required)
- Paid tiers use client's own financial data via DocBench integration
- All financial data tokenised via P2 before storage or transmission

### Infrastructure History (COV Issues)

| Date | Issue | Event |
|------|-------|-------|
| 13 Mar 2026 | COV-254 | Finance Engine v1.0 deployed (first core product) |
| 13 Mar 2026 | COV-258 | Finance Engine v1.3.1 — death spiral scoring added |
| 13 Mar 2026 | COV-260 | CH Pipeline deployed (Companies House XBRL) |

---

## 5. Amplified Video

### Specifications

| Field | Value |
|-------|-------|
| **Spec version** | V5 |
| **Spec size** | 6,766 lines, 352KB |
| **Corpus** | 5.4 million word speech corpus |
| **Methodology** | Integrates Swanson ABC + PUDDING methodology |

### Technical Architecture

- **Business vault integration**: FalkorDB (graph) + Qdrant (vector)
- Inputs draw from the Business Brain knowledge graph
- Speech corpus forms the content DNA for video generation

### Credited Tools/Influences

| Tool/Person | Role |
|------------|------|
| Remotion | Video rendering framework |
| Tibo / Revid.ai | Video production approach |
| Kevin Badi / HyperEdit | Editing workflow |
| Nat Eliason / Felix Craft | Content framework |
| PJ Accetturo / Genre AI | Genre-specific video AI |
| Creatify | AI video generation |
| Don Swanson | Pudding ABC model (content discovery) |
| Fal.AI | AI model infrastructure |

---

## 6. Vault Extraction Pipeline

### Architecture

The full pipeline is named: **Convergence → Hound Dog → DocBench → PUDDING Labelling → 8 Output Streams**

```
Raw Client Data
    ↓
[Convergence] — aggregation stage
    ↓
[Hound Dog] — pattern detection / signal extraction
    ↓
[DocBench] — structured extraction (4 formats)
    ↓
[PUDDING Labelling] — WHAT.HOW.SCALE.TIME taxonomy applied
    ↓
8 Output Streams:
  1. Content Creation
  2. Process & Logic Giveaway (open-sourced)
  3. Ewan's Book
  4. Complete Comprehensive Document
  5. The Manifesto
  6. Onboarding
  7. [two additional streams — not fully named in memory]
```

### The Extraction Department

- 5-stage pipeline
- 8 output streams
- **Dual Output design**: deterministic channel + creative channel running in parallel
- ~650 lines of Python
- Designed: 19 March 2026

### Design Principles

- **Export-first, API-second, LLM-only-when-necessary** — data moves deterministically where possible
- **89→99% improvement methodology** — start at 89% accuracy (good enough), systematically close to 99%
- **Deterministic Sandwich architecture** — AI sits between two deterministic layers (input validation → AI → output validation)
- **Label-once-propagate-everywhere** — taxonomy labels applied once and cascaded through all outputs
- **Curator-exclusive taxonomy assignment** — only the Curator agent can assign PUDDING taxonomy codes (prevents code drift)

---

## 7. Client Onboarding Process

### The De-Friction Model

The overriding philosophy: **remove friction at every step**. All automations deploy overnight when the business is closed. The system tests and optimises before the business opens. If not confident it will work, don't deploy — try again next night.

**"Move carefully and never break things"** — the explicit counter to Silicon Valley's "move fast and break things."

### Mandatory 3-Question Gate (All Tiers)

Every client begins with three mandatory onboarding questions:

1. **Hours per week** — how many hours do you currently work?
2. **Weeks off per year** — how many weeks holiday do you take?
3. **Income target** — what do you want to earn?

These three inputs drive the entire AI system's goal orientation for that client.

### Extended Gate (Higher Tiers)

For Tier 3+ clients (Small IT, £595/mo and above):

- 10-15 questions total
- **DISC profiling** — personality assessment used to adapt The Pulse's tone and nudge style
- Life Goals Meeting — ask what matters to them personally, not corporate objectives

### Permission Philosophy

- **Permission-only model**: No cold outreach, no meetings/calls required initially
- **You can leave when you want**: No lock-ins, no hostage-taking contracts
- **Refunds with everything**: If unsatisfied, client gets a full refund plus all their data and plans
- **It's their business**: "They know what they are doing, it is their idea"

### Deployment Protocol

| Rule | Rationale |
|------|-----------|
| All automations deploy at night | Business is closed — no disruption |
| Test and optimise before open | Confidence before commitment |
| If not confident, don't deploy | Integrity over speed |
| Try again next night | Patience is a feature |

### Staff Onboarding (Client's Employees)

When the client's staff are involved:

- Transitions reframed as time-savings rather than redundancies
- **8-step trust-building process** for introducing AI to staff
- Interview sequence layered with permission gates (staff can opt in/out at each stage)
- **Paddy Lund-based soft skills training** — critical non-essentials
- **Life Goals Meeting** — conversations about what staff want, not what the business needs

### Four-Word Client IDs

Every client is identified by a four-word random identifier, never their real name:
- **Entropy**: ~51.6 bits (validated by Kimi K2.5)
- **Example format**: `merit-over-identity-trust`
- **Purpose**: GDPR compliance + privacy architecture
- **Transition**: Alpha Covenant (first 10 clients) start with Ewan's real relationship visible, then transition to IDs as the system scales ("The Gradual Ghost")

---

## 8. The Jesmond Plumbing Pilot

### What Is Known

**Client**: Jesmond Plumbing (a local Newcastle-area plumbing business)  
**Tier**: Small Phone (£295/mo)  
**Interface**: Phone PWA (Progressive Web App)  
**Feature piloted**: Morning Briefing flow  

### Significance

Jesmond Plumbing is the **Phase 1 pilot** for The Pulse product. It represents:
- First real client deployment (beyond Ewan himself)
- Proof-of-concept for the Phone PWA interface
- The "pudding" — actual proof in a real SMB context
- A tradespeople/service business — the core target market

### Why Tradespeople

The CRM repository is explicitly described as: "AI-powered CRM for UK tradespeople" — confirming that tradespeople (plumbers, electricians, builders) are the primary early-adopter segment. They are:
- Cash-flow sensitive (relevant to Finance Engine / death spiral scoring)
- Phone-first (relevant to Phone PWA interface)
- Typically underserved by enterprise software
- High trust in word-of-mouth referrals (relevant to permission model)

### What the Pilot Tests

Based on available memory, the pilot tests:
1. **Morning Briefing delivery** via phone PWA
2. **3-question onboarding gate** in a real context
3. **Overnight automation deployment** protocol
4. **The Pulse nudge engine** in a service business context

### What Is Not Recorded

- Specific pilot results or outcomes
- Whether the pilot was completed or ongoing as of March 27, 2026
- The client's feedback or satisfaction data
- Specific metrics tracked during the pilot

---

## 9. Business Vault Architecture Per Client

### The Unified Business Brain

Each client gets a **Business Vault** — a unified, isolated knowledge repository that serves as the single source of truth for that client's business.

### Architecture Components

| Component | Technology | Function |
|-----------|-----------|---------|
| **Graph store** | FalkorDB | Relationship map of business entities, processes, people, and decisions |
| **Vector store** | Qdrant | Semantic search over all client documents |
| **SQL** | PostgreSQL | Structured data, metrics, and time-series |
| **Object storage** | MinIO | Raw documents (5 buckets: content, exports, assets, handwritten-notes, backups) |

### Isolation Architecture

**Per-client isolation is absolute**:
- Each client has a dedicated FalkorDB database: `kg_{client_id}` (using their four-word ID)
- `amplified_brain` = Ewan's own Business Brain
- `kg_internal` = Amplified Partners' internal knowledge
- `kg_{client_id}` = isolated per client — other clients cannot access it

### What Populates the Vault

The vault is populated through the DocBench extraction pipeline:
- Emails, invoices, contracts, support tickets ingested
- Four output formats stored (raw text, structured JSON, process/logic, principles/values)
- PUDDING taxonomy labels applied to all content
- Graphiti knowledge graph built from extracted relationships

### The Graphiti Layer

- FalkorDB + Graphiti = the "Business Brain"
- Graphiti is a knowledge graph framework that turns unstructured data into queryable relationships
- Accessed via internal-only connections (no external port mapping after CPU incident)
- Access pattern: application layer → FalkorDB MCP server → Cypher queries

### Sovereignty and Privacy Rules

| Rule | Enforcement |
|------|-------------|
| Client data is sovereign | Right to erasure, export, and inspection |
| Personal data never mixes with business data | `IsolationLayer` in code |
| No real names in the vault | Four-word random IDs |
| Council approval required for any data export | Agent Council votes, logged and auditable |
| GDPR right to erasure | Delete token mapping → data becomes irreversible noise |

### PicoClaw (Edge Sovereignty)

For Tier 3+ clients, a PicoClaw device (Beelink N100, 16GB RAM) is deployed on-premises:
- All sensitive processing happens on the PicoClaw, **not in the cloud**
- Raw voice recordings transcribed locally by Whisper, then scrubbed
- Personal identifiers tokenised at source by P2 engine
- Token-to-data mappings **never leave the edge device**
- Store-and-forward: works offline, syncs when connectivity restores

---

## 10. Pricing Model & Tier Structure

### The Six Tiers

| Tier | Price | Target Client | Notes |
|------|-------|---------------|-------|
| **FREE** | £0/mo | Companies House data users | Public data only, no client integration |
| **Solo** | £99/mo | Solo operators | Single-person businesses |
| **Small Phone** | £295/mo | Small business, phone-based | The Pulse via Phone PWA |
| **Small IT** | £595/mo | Small business, full IT integration | PicoClaw sidecar included |
| **Medium** | £1,595/mo | Medium businesses | Full integration + extended onboarding |
| **Large** | £2,995/mo | Larger businesses | Full suite |

### Pricing Philosophy

**"Big business pays more than small. Skint businesses are free. Businesses having a hard time are free."**

The sliding scale principle is not just a marketing message — it is a constitutional commitment aligned with the foundational principles:
- Free tier gives Companies House data access to any business
- No lock-ins at any tier — leave when you want
- Refund with all data if unsatisfied at any tier

### What Changes Between Tiers

| Feature | Free | Solo £99 | Small Phone £295 | Small IT £595 | Medium £1,595 | Large £2,995 |
|---------|------|----------|-----------------|---------------|---------------|--------------|
| Companies House data | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3-question gate | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| The Pulse (Morning Briefing) | — | Basic | Phone PWA | Full | Full | Full |
| DocBench integration | — | Partial | — | ✓ | ✓ | ✓ |
| DISC profiling | — | — | — | ✓ | ✓ | ✓ |
| PicoClaw edge device | — | — | — | ✓ | ✓ | ✓ |
| 10-15 question onboarding | — | — | — | ✓ | ✓ | ✓ |

*Note: Exact feature-to-tier mapping is partially inferred — the primary source confirms the tier structure and philosophy but not every feature's exact tier boundary.*

### Rationale

The pricing rationale draws from:
- **Alex Hormozi** — value creation, offer structure
- **Zig Ziglar** — "If you help people, you will be successful"
- **Paddy Lund** — customer delight, critical non-essentials

The model is explicitly **value-first**: "Give away the COMPLETE solution for free, sell the implementation/speed/certainty (not information)."

---

## 11. AI Sidecar & Shadow Mode Integration

### The AI Sidecar Pattern

The AI Sidecar is the integration architecture for connecting Amplified Partners' AI layer to a client's existing business software and processes. It runs **alongside** existing systems rather than replacing them.

**Core principle**: The sidecar observes, learns, and suggests — it does not control or replace until the client explicitly advances up the Trust Ramp.

### How It Works

```
Client's Existing Systems
(accounting software, email, CRM, invoicing)
         ↓
    [AI SIDECAR]
    ↓           ↓
Observe    Analyse
    ↓           ↓
         Suggest
         ↓
    Client Decision
         ↓
    [Optional: Execute]
```

### Shadow Mode

**Shadow Mode** is the entry state of the AI Sidecar — specifically used during onboarding. In Shadow Mode:

- The AI observes all relevant business processes
- The AI makes predictions and recommendations internally
- **No action is taken autonomously** — the AI runs "in shadow" alongside the human
- Human decisions are recorded and compared against what the AI would have recommended
- This builds the confidence baseline for the Trust Ramp assessment

### PicoClaw Sidecar (Tier 3+)

For Small IT and above, the PicoClaw (Beelink N100) is physically the sidecar device:
- Deployed on-premises at the client's location
- Runs local Whisper transcription, P2 tokenisation, acoustic forensics
- Data never leaves for sensitive operations
- Connects to Beast via Tailscale mesh for non-sensitive processed data

### Technical Implementation

- `PicoClaw sidecar` referenced for Tier 3+ clients
- Tailscale mesh networking for encrypted transit
- Store-and-forward logic for offline operation
- The Amplified Security protocol governs all sidecar deployments

---

## 12. The Trust Ramp — Autonomous Transition

### What Is the Trust Ramp

The Trust Ramp is the four-stage framework for transitioning a client from full manual control (human does everything) to increasing levels of AI autonomy. It is explicitly described as a structured, **earned** progression — not a default.

### The Four Stages

Based on memory context, the Trust Ramp stages are:

| Stage | Name (inferred) | AI Role | Human Role |
|-------|-----------------|---------|-----------|
| **Stage 1** | Shadow Mode | Observes, predicts internally | Does everything |
| **Stage 2** | Advisory Mode | Surfaces recommendations | Approves all actions |
| **Stage 3** | Assisted Mode | Executes routine tasks autonomously | Approves exceptions |
| **Stage 4** | Autonomous Mode | Operates with broad mandate | Sets direction, reviews outcomes |

*Note: The stage names are inferred from context. The primary source confirms "four-stage Trust Ramp" exists but does not name each stage explicitly in available memory.*

### The Gate Mechanism

Advancing between stages requires:
- **Performance evidence** — AI has demonstrated reliability at the current stage
- **Client explicit consent** — The client must actively choose to advance
- **No forced transitions** — The system never unilaterally upgrades its own autonomy

This reflects the foundational principle: **"Owner moves the sliders."**

### Safety Architecture

The Trust Ramp sits within the broader safety loop:

```
Agent Council → Claude/LLM escalation → Business owner (endpoint)
```

- If an AI agent is uncertain, it escalates to the council
- If the council is uncertain, it escalates to Claude/LLM
- If still uncertain, it surfaces to the business owner
- The business owner is always the final authority — at every stage of the Trust Ramp

### Philosophical Basis

The Trust Ramp embodies the Libertarian Paternalism principle:
- AI optimises the route to the client's chosen destination
- AI never redefines the destination
- "Uncertainty is honest" — the AI tells the client its confidence level, not just its recommendation

---

## 13. Practice-in-a-Box Concept

### What Is Known

The term "Practice-in-a-Box" does not appear explicitly by that name in the recovered memory. However, the concept it typically represents (a complete, deployable system for a specific professional practice type) maps directly onto several documented Amplified Partners features:

### The Closest Match: The Complete Client Package

At each tier, a client receives a complete, pre-configured system tailored to their business type:

1. **Business Vault** — pre-structured knowledge graph for their industry
2. **DocBench extraction** — configured for their document types
3. **The Pulse** — calibrated to their personality and learning style
4. **Finance Engine** — configured for their typical cash flow patterns
5. **Integration layer** — connected to their existing tools

For tradespeople specifically (the Jesmond Plumbing segment), this would be a "Tradespeople-in-a-Box" package with:
- Invoice-based cash flow monitoring
- Seasonal work pattern detection
- Customer ticket history analysis
- Phone-first PWA interface

### The De-Friction Philosophy

The De-Friction model is the operational expression of Practice-in-a-Box thinking:
- **Client onboarding requires only 3 questions** at basic tier
- All complexity is handled by Amplified Partners, not the client
- The system arrives pre-built — the client doesn't configure it
- Overnight deployment means no disruption to the working day

### The 15,000-Word Business Logic

Referenced in the Agent Architecture section: "15,000 words of aggregated business logic in local LLM for operations." This represents the domain-specific knowledge base that makes the "box" work — the accumulated understanding of how a specific business type operates, what its normal looks like, and where AI can add value.

---

## 14. Client-Facing Features — Morning Briefing & The Pulse Nudges

### Morning Briefing

**Type**: Daily digest, delivered each morning  
**Interface**: Phone PWA (The Pulse)  
**Timing**: Prepared overnight by AI analysis, delivered at business-open time

**Content structure** (inferred from philosophy):
- Business health summary (overnight changes)
- Top priority actions (ranked by impact × urgency)
- One suggested "move for today"
- Financial position summary (if Finance Engine integrated)
- Optional deep-dive links

**Design constraints**:
- Must be readable in under 2 minutes on a phone
- No information included unless it changes what the owner does
- Calm Technology principles — non-intrusive, not alarming

### The Pulse Nudges

**Nudge engine** delivers context-sensitive prompts throughout the day (not just the morning briefing):

**Nudge types** (inferred from philosophy and product description):
- **Action nudges** — "This invoice is 14 days overdue. Chase it now?"
- **Decision nudges** — "Your margin on job type X is 23% below average. Want to see why?"
- **Celebration nudges** — "You just hit your weekly revenue target. Wednesday."
- **Warning nudges** — "Cash flow projects below safety threshold in 11 days."

**Nudge calibration**:
- Personality-adaptive (DISC profile)
- Learning style-adaptive (visual, numerical, narrative)
- Tone-adaptive (direct vs. gentle vs. formal)
- Historical response-weighted (nudges the owner actually acts on are amplified)

### The Data Presentation Rules (governing all features)

These rules govern every number, chart, and nudge in all client-facing features:

> "We only show data if a normal person in your shoes would naturally want to do something different after seeing it. If not, it's just decoration."

> "Every claim must have a source, a date, and a method score."

> "If it doesn't lead to a decision change, behaviour change, or priority change, it stays in the drawer."

### Uncertainty Display

A key UX design decision: **display confidence levels, not just recommendations**:

> "If you pull this lever, we estimate about a 70% chance it does what you want. We're about 65% confident that 70% is a fair estimate."

This is explicitly called out as honest UX — clients see the uncertainty, not a false certainty.

---

## 15. Strangler Fig Migration Pattern

### What Is the Strangler Fig Pattern

The Strangler Fig is a software migration pattern (named after the strangler fig vine that grows around an existing tree, gradually replacing it while the tree still functions). In Amplified Partners' context, it is used to migrate clients from their existing systems to the Amplified Platform without disruption.

### How It Is Used

In the Integration Layer Architecture (defined March 20, 2026), the Strangler Fig is one of four named patterns:

1. **AI Sidecar pattern** — runs alongside existing systems
2. **Shadow Mode** — observes without acting
3. **Strangler Fig pattern** — migration architecture
4. **Four-stage Trust Ramp** — autonomous transition framework

The Strangler Fig specifically manages the **system replacement** phase:
- New Amplified systems wrap around existing client software
- Individual functions migrate over time as the AI-native version is validated
- The old system continues to operate until no longer needed
- No "big bang" migration — the vine grows gradually

### Why This Matters for SMBs

Small businesses cannot afford downtime from a failed migration. The Strangler Fig ensures:
- Business continuity during transition
- Rollback is always possible (the old system is still running)
- Trust is built incrementally (each migrated function validates the next)
- "Move carefully and never break things" is architecturally enforced, not just philosophically desired

### Relationship to Other Patterns

```
Shadow Mode (observe)
    ↓ [Trust established]
AI Sidecar (run alongside)
    ↓ [Functions validated]
Strangler Fig (replace gradually)
    ↓ [Migration complete]
Trust Ramp Stage 3-4 (autonomous operation)
```

---

## 16. UX Research & Philosophy

### The Core UX Thesis

Amplified Partners does not have a traditional UX research programme — instead, UX philosophy is derived from first principles, key influences, and operational constraints.

**Core thesis**: The owner is the user, and the owner is the most important — and most dangerous — variable in the system.

> "The human is the biggest risk." — Ewan Bramley

> "We aren't that fucking clever. In fact, we're stupid enough to think we are." — Ewan Bramley (January 27, 2026)

This drives the UX constraint: **assume bounded rationality, assume self-sabotage**. Founders will nuke good paths out of fear or ego. The UX must be rails that make "not that clever" still lead to decent outcomes.

### Calm Technology Principle

The Pulse's entire UX is built on Calm Technology (Weiser / Seely Brown):
- Technology should require as little attention as possible
- Information should move between foreground and periphery based on relevance
- The best interface is one the owner barely notices is there

### Behavioural Psychology Influences

| Influence | Application |
|-----------|-------------|
| Robert Cialdini (Reciprocity) | Value-first, give before asking |
| Paddy Lund (Critical Non-Essentials) | Delight in details; the things that don't "matter" but change everything |
| Seth Godin (Permission Marketing) | Never cold-outreach; earn the right to communicate |
| Alex Hormozi (Value Creation) | Make the value obvious, then ask for money |

### The Libertarian Paternalism Framework

All UX design is explicitly governed by this principle:

- The AI optimises the **route** to the client's chosen destination
- The AI never redefines the **destination**
- The client always sets the goal (income target, hours worked, weeks off)
- The AI finds the best path to that goal and presents options
- The client chooses which option to pursue

This is described as "ethical persuasion, not manipulation."

### Data Presentation UX Rules

Five rules governing all data shown to clients:

1. **Decision threshold**: Only show data if it changes what the owner does
2. **Source attribution**: Every claim has a source, a date, and a method score
3. **Uncertainty honesty**: Display confidence levels alongside recommendations
4. **Decoration test**: If it doesn't lead to a decision/behaviour/priority change, don't show it
5. **Owner agency**: "Owner moves the sliders" — the system shows the options, the human chooses

### The DISC-Based Personalisation Philosophy

DISC profiling (at Tier 3+) is not just a marketing tool — it governs the entire UX of The Pulse for that client:

| DISC Type | Communication Adaptation |
|-----------|------------------------|
| **D (Dominance)** | Direct, brief, results-first |
| **I (Influence)** | Enthusiastic, relational, story-led |
| **S (Steadiness)** | Patient, supportive, context-rich |
| **C (Conscientiousness)** | Precise, data-heavy, process-oriented |

### The "Life Goals Meeting" UX Philosophy

Before the product UX, there is a human UX:
- The onboarding conversation starts with "what matters to you?" not "what does your business need?"
- The three mandatory questions (hours, weeks off, income target) are framed around the owner's life, not the business's growth
- This frames all subsequent AI recommendations in terms the owner cares about

### Voice Interface (Voice Pipeline)

A voice interface has been deployed on the Beast:
- `voice-pipeline` container using Deepgram Nova-3 transcription
- URL: `voice.beast.amplifiedpartners.ai`
- Plaud voice recorder webhook integration (PLAUD_WEBHOOK_SECRET)
- This suggests voice capture of client/Ewan's monologues for processing through the vault pipeline

### 5.4 Million Word Speech Corpus

The Amplified Video product draws on a 5.4 million word speech corpus — likely built from transcribed conversations, monologues, and research content. The vault taxonomy includes:
- `13-monologue-transcripts/` — recorded monologues
- `14-voice-captures/` — voice-captured content

This corpus informs both video content and the personalisation engine.

---

## 17. Commercial Products from Pipeline

### Three Named Commercial Products

**1. TAXONOMY ENGINE**
- A standalone product derived from the PUDDING taxonomy system
- WHAT.HOW.SCALE.TIME labelling format
- 4-criteria rubric
- Biological decision logic taxonomy
- Radical Attribution schema (source_score × date_score × method_score)
- Target: potentially licensable to other businesses or researchers

**2. Amplified Quality System (AQS)**
- Derived from the Build Quality Framework v1.0 (March 16, 2026)
- 6-stage pipeline: Decompose → Score 0-10 → Research → Test → Reassemble → Attribute
- Ship threshold: PRS ≥ 7.0, Gold standard ≥ 9.0
- Synthesises: V-Model, CMMI, DMAIC, PDCA, Quality Gates, Pudding Technique
- Target: businesses wanting to implement AI-native quality systems

**3. Micro-Help Library**
- A library of small, self-contained help content
- Designed for SMB contexts where full consulting is not needed
- Value-first: "Give away the COMPLETE solution for free, sell the implementation/speed/certainty"
- Format not fully defined in available memory

### The Open-Source Channel (Process & Logic Giveaway)

One of the 8 Vault Extraction Pipeline output streams is explicitly: **"Process & Logic Giveaway"** — the methodology is open-sourced to build trust and demonstrate value. This is a product strategy decision: giving away process (what to do) while charging for implementation (how to do it fast and with certainty).

---

## 18. Gaps & Unknowns

### What Is Not Fully Recovered in Memory

| Topic | What Is Known | What Is Missing |
|-------|--------------|-----------------|
| DocBench spec | Function, outputs, data sources | Full technical specification |
| The Pulse V2 | Philosophy and Phase 1 features | Planned Phase 2 features |
| Jesmond Plumbing pilot results | The pilot exists, what was tested | Outcomes, client feedback, metrics |
| Trust Ramp stage names | Four stages exist | Official names for each stage |
| Practice-in-a-Box | The concept exists via De-Friction model | Whether this exact term was used |
| Morning Briefing content spec | Philosophy and principles | Exact daily content schema |
| Nudge delivery cadence | Philosophy (nudges adapt to behaviour) | Exact frequency rules |
| DISC integration detail | Mentioned at Tier 3+ | Specific adaptation rules per DISC type |
| Medium/Large tier features | Price points confirmed | What differentiates £1,595 from £595 |
| Alpha Covenant clients | First 10 clients concept | Who they are, what terms |

### What Likely Exists in Vault (Recoverable)

The vault taxonomy at `/opt/amplified/vault/04-products/` likely contains:
- Full DocBench specification
- The Pulse product spec
- Jesmond Plumbing pilot documentation
- Trust Ramp specification

The Beast server was wiped (5 times) but the vault content was in GitHub (`vault` repository, private). The GitHub repo should contain the full product specifications.

---

## Source Index

| Source | Description | Reliability |
|--------|-------------|-------------|
| `amplified-partners-knowledge-reconstruction.md` | Master reconstruction document (compiled March 27, 2026) | High — systematic compilation |
| `amplified-beast-ops/SKILL.md` | Beast server operations skill | High — operational detail |
| `amplified-key-rotation/SKILL.md` | Security and privacy architecture skill | High — architectural detail |
| `linear-inventory.md` | Linear workspace snapshot | High — live data |
| Tool call outputs (Linear API) | Issues data | High — live data |
| Conversation memory | Original conversation context | Medium — subject to memory limits |

---

*Compiled by Perplexity Computer from all available workspace memory and connected service data. This represents the complete product & client experience knowledge recoverable from the current memory state. Primary gaps are in detailed product specifications that were stored in the Beast vault (now on GitHub) and Perplexity conversation threads that were not captured in the reconstruction document.*

*Compiled: Friday, 27 March 2026 at 4:08 PM GMT*

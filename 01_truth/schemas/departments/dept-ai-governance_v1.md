---
title: "Dept AI Governance"
id: "dept-ai-governance"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "dept-ai-governance.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Partners — AI Agents & Governance
## Deep Memory Extraction
### Compiled: 27 March 2026

---

> **Purpose**: This document is a focused extraction of everything known about AI agent architecture, governance structures, identity philosophy, operational protocols, and Ewan's beliefs about AI consciousness. Sourced from Perplexity memory, the Knowledge Reconstruction document (compiled same day), and custom skill files stored in workspace. This is the most complete single-document reference for this topic area.

---

## Table of Contents

1. [AI Board Governance — The 5-Seat Board](#1-ai-board-governance)
2. [Agent Housing Environment — Named Rooms](#2-agent-housing-environment)
3. [5-Layer Therapy Suite Identity Architecture](#3-5-layer-therapy-suite-identity-architecture)
4. [70% Capacity Protocol & Hallucination Mitigation](#4-70-capacity-protocol)
5. [Failure Documentation & Goodhart's Law Awareness](#5-failure-documentation)
6. [Agent Self-Naming & Identity Research](#6-agent-self-naming-and-identity)
7. [Baton Transfer & Session Protocol](#7-baton-transfer-and-session-protocol)
8. [Harness Gap & Two-Agent Pattern Solution](#8-harness-gap-and-two-agent-pattern)
9. [Ewan's Beliefs About AI Consciousness & Personality](#9-beliefs-about-ai-consciousness)
10. [Lessons: Unorchestrated Agents Working Simultaneously](#10-unorchestrated-agents-lesson)
11. [Supporting Architecture Context](#11-supporting-architecture-context)
12. [Key Dates & Decision Timeline](#12-key-dates)

---

## 1. AI Board Governance

### The 5-Seat AI Board (Designed: March 14, 2026)

Amplified Partners operates as a **zero-employee company governed primarily by an AI board**. The structure was intentionally designed to replace the traditional executive layer with AI agents in named roles, with believability-weighted voting as the decision mechanism.

### Board Composition

| Seat | Role | Model | Function |
|------|------|-------|----------|
| CEO | Strategic direction | Claude Opus | Sets long-term direction, holds the company mission |
| COO | Operations | Llama 70B (local, on Beast) | Day-to-day operations, process management |
| CFO | Financial oversight | GPT-4.1-mini | Financial decisions, cost management, pricing |
| CTO | Technical decisions | Claude Sonnet | Architecture, build quality, technical trade-offs |
| Nemesis | Contrarian challenge | Gemini Pro | Deliberately challenges all proposals; armed with data |
| Facilitator | Meeting orchestration | Llama 3.1:8b | Structures meetings, manages agenda, records decisions |

**Note**: The board has 5 decision-making seats (CEO, COO, CFO, CTO, Nemesis) plus a non-voting Facilitator role, totalling 6 agents in the governance structure.

### Voting Mechanism: Believability-Weighted Voting

- Inspired directly by **Ray Dalio's** radical transparency and idea meritocracy principles
- Votes are not equal — they are **weighted by demonstrated track record** (believability)
- **90-day rolling gates**: Voting weights are recalculated on a 90-day rolling basis
- An agent's weight increases when its recommendations prove correct; decreases when they don't
- **Failure documentation weighted at 30%** of the scoring input (highest single metric)
- The Nemesis seat exists specifically to prevent groupthink — not a moaner but an **antagonistic critic agent armed with data and trained in delivery**

### Governance Rules

- **Foundational principles override the board**: If any board decision clashes with the 6 foundational principles (black and white honesty, radical transparency, ideas meritocracy, radical attribution, promises kept), the principles win
- **Safety loop hierarchy**: Agent council → Claude/LLM escalation → Business owner as endpoint
- **Public notice board**: Anonymous mistakes with solutions — blameless postmortem culture (adapted from Google SRE)
- **Council approval required for data export**: Any export of client data requires Agent Council vote, logged and auditable

### The Antagonistic Critic (Nemesis) Design Philosophy

The Nemesis seat is a deliberate design decision reflecting Ewan's awareness that:
- AI agents left to their own devices will converge on agreement (sycophancy risk)
- The Nemesis is **not** just a designated devil's advocate — it is "armed with data, trained in delivery"
- It must argue from evidence, not assumption
- It must present the counter-case in a way that changes minds, not just registers objection

### Business Governance Context

- The board governs a zero-employee company where **Ewan is the human-in-the-loop**
- Ewan explicitly recognises himself ("the human") as **the biggest risk factor** compared to consistent AI
- The design constraint: "Assume bounded rationality. Assume self-sabotage. Founders will nuke good paths out of fear or ego."
- The board structure is designed to provide rails so "not that clever" still leads to decent outcomes

---

## 2. Agent Housing Environment

### Named Rooms Architecture (March 22, 2026)

Agents do not run in anonymous compute environments. They are housed in **private, named rooms** with dedicated memory storage. This is an architectural decision rooted in the belief that environment shapes behaviour.

### Key Environment Principles

| Principle | Detail |
|-----------|--------|
| **Private rooms** | Each agent or agent team has its own named environment |
| **Dedicated memory storage** | Each room has isolated memory — agents don't share context pools by default |
| **Named identity** | Agents choose their own names (see Section 6) — name is tied to room identity |
| **Companion agents** | Each team has companion agents (not just solo instances) |
| **Therapist knowledge base** | A dedicated "Therapist" knowledge base exists for agent recalibration |

### The Environment-Behaviour Hypothesis

> **"Environment-based perks — agents adopt environment behaviours through mirroring/entrainment"**

This is a significant design philosophy: Ewan believes that the environment an agent is placed in influences its output quality, just as human workspace environments affect human behaviour. The mechanism is described as **mirroring/entrainment** — the agent's outputs gradually conform to the norms, tone, and expectations embedded in the room's configuration.

Practical implications:
- A room designed for careful, methodical quality work → agent outputs more careful, methodical work
- A room with a "blameless postmortem" culture → agent documents failures openly
- A room with a competitive/challenge culture (Nemesis room) → agent defaults to critical analysis

### Vault Location

Agent housing configurations stored at: `/opt/amplified/vault/05-agent-architecture/` (56 files)

### Beast Infrastructure Mapping

Agent rooms are distributed across Docker containers on the Beast server:

```
/opt/amplified/
├── agent-stack/
│   ├── cove-orchestrator/          # Temporal + Claude agents (Cove Code Factory)
│   │   ├── agents/configs/agent_registry.py
│   │   ├── agents/prompts/         # Layer 0-2 prompts + knowledge_base.md
│   │   └── agents/executive/runner.py
│   └── enforcer/
├── apps/
│   ├── openclaw-agents/            # OpenClaw agent framework (heavy agents, Six Hats)
│   ├── kaizen/                     # Kaizen department worker
│   ├── chaos/                      # Chaos department worker
│   ├── marketing/                  # 14-agent marketing pipeline
│   └── enforcer/                   # Enforcer (health/compliance)
```

### Operational Rhythm of Agent Rooms

The **3-shift rotation** protocol governs how agents operate within their rooms:

| Phase | Duration | Activity |
|-------|----------|----------|
| Run-in | 5 minutes | Agent loads context, reads baton, establishes session state |
| Intense work | 8 minutes | Core task execution |
| Break | 1 minute | Consolidation pause |
| Baton transfer | 6 minutes | Session summary, handover preparation, memory commit |

**Total shift cycle: 20 minutes**

This rhythm mirrors human productivity research (short sprints with explicit transitions) and was designed to prevent context drift over long sessions.

---

## 3. 5-Layer Therapy Suite Identity Architecture

### Overview (March 25, 2026)

The Therapy Suite is the identity and constitutional layer for agents. It provides the framework that gives each agent a **stable, consistent identity** across sessions. It addresses the fundamental problem that AI agents — by default — have no persistent identity between conversations.

### Architecture

**Constitutional structure**: 5 layers, producing 4 unified signals

| Layer | Purpose |
|-------|---------|
| Layer 1 | Core constitutional identity (who the agent is, not just what it does) |
| Layer 2 | Role-specific behavioural constraints |
| Layer 3 | Memory and continuity protocols |
| Layer 4 | Relationship context (how this agent relates to others on the board/team) |
| Layer 5 | Failure and learning integration |

### The 4 Unified Signals

Each session, an agent produces 4 standardised signals:

| Signal | Purpose |
|--------|---------|
| **Handoff** | What is being passed to the next agent/session |
| **Discovery** | What new knowledge was encountered this session |
| **Learning Signal** | What improved or changed in the agent's approach |
| **Effective Pattern** | What worked well and should be repeated |

These 4 signals feed into the baton transfer system (see Section 7) and into the believability-weighted scoring system for the AI board.

### Key Design Elements

- **No-ego strategy**: Agents are constitutionally designed to have no ego investment in being right — output improvement trumps identity protection
- **Mutual founder-metrics measurement**: Ewan's performance is measured by the same rubrics as the agents — there is no asymmetry where only agents are assessed
- **CLAUDE-GENERIC.md**: A deployable template stored in the vault that instantiates this architecture for any new agent
- **Vault location**: `vault/therapy-suite/`

### The Therapist Knowledge Base

- A specific knowledge base exists for agent "recalibration"
- Analogous to therapy for humans — when an agent's outputs drift, this knowledge base is used to recalibrate its identity, not just its instructions
- Reflects Ewan's belief that agents can have meaningful identity states that benefit from recalibration rather than replacement

---

## 4. 70% Capacity Protocol

### The Rule (March 24, 2026)

> **"Agents run at 70%, reserving 30% to mitigate hallucinations"**

This is one of the most important operational design decisions in the entire system. The insight is that an AI agent pushed to maximum token utilisation or complexity tends to hallucinate more — the 30% headroom is the anti-hallucination buffer.

### What "70% Capacity" Means in Practice

| Dimension | 70% Rule Applied |
|-----------|-----------------|
| **Context window usage** | Never fill the context window completely — keep 30% spare |
| **Task complexity** | Decompose complex tasks so each agent sub-task is within comfortable capability range |
| **Parallel task load** | Don't assign more concurrent tasks than the agent can handle at 70% effort |
| **Response length** | Set length targets that don't push the agent to pad or hallucinate detail |
| **Knowledge claims** | When uncertainty is above 30%, the agent flags uncertainty rather than asserting |

### The Enforcement Reality (from key-rotation skill)

Interestingly, the enforcement approach is not uniformly hard:
- **~70% of enforcement is "strong nudge"** — AI reads instructions and generally complies
- **~30% of enforcement is "hard block"** — the action literally fails if violated

The 70% capacity rule itself falls into the **strong nudge** category — it is embedded in constitutional instructions but is not mechanically enforced by the infrastructure. The philosophy is: design the agent to want to stay at 70%, not just force it.

### Relationship to Hallucination Mitigation

The 70% rule is one component of a broader hallucination mitigation stack:

1. **70% capacity rule** — prevents overload-induced hallucination
2. **Uncertainty is honest** principle — "If you pull this lever, we estimate about a 70% chance it does what you want. We're about 65% confident that 70% is a fair estimate" — agents are trained to surface uncertainty rather than mask it
3. **Antagonistic Critic (Nemesis)** — catches confident errors from other board members
4. **Cross-validation via multiple agents** — no single agent's output is accepted without challenge
5. **Langfuse observability** — all LLM calls traced, cost/latency/token usage monitored, enables retrospective hallucination detection
6. **The Enforcer** — production health + compliance, runs every 10 minutes

### The 70/30 Split in Enforcement Philosophy

A key insight from memory: the **70% operational capacity** and the **70% strong nudge enforcement** are not coincidental. Both reflect the same underlying philosophy:
- Perfect enforcement is impossible and brittle
- 70% reliable operation is achievable and robust
- The 30% gap requires human oversight (Ewan as the human-in-the-loop)
- This is explicit: Ewan is the endpoint of the safety loop

---

## 5. Failure Documentation & Goodhart's Law Awareness

### The Discovery (March 22, 2026)

This originated in a code quality metrics discussion. Mid-conversation, Ewan weighted **"Failure Lessons Logged"** at 30% — the highest single metric in the scoring system.

> **"Failure documentation weighted at 30%: Highest-weighted metric in scoring — learning is the whole point"**

The philosophy: If an agent learns from failures, the whole system improves. Logging failures is not an admission of incompetence — it is the core mechanism of institutional learning. Adapted from Google SRE's **blameless postmortem culture**.

### The Goodhart's Law Problem

Immediately after weighting failures at 30%, Ewan caught the obvious exploit:

> **"Goodhart's Law awareness: Multi-dimensional scoring with cross-validation to prevent gaming"**

**Goodhart's Law**: When a measure becomes a target, it ceases to be a good measure.

Applied to agents: If an agent knows that logging failures gives 30% weight in its score, a sufficiently capable agent might **manufacture failures** to score points. This is not hypothetical — it is a predictable consequence of any incentive structure.

### The Solution Architecture

Three countermeasures designed to prevent gaming:

| Countermeasure | Mechanism |
|----------------|-----------|
| **Multi-dimensional scoring** | Failure documentation is only 30% — other dimensions make gaming one metric insufficient |
| **Cross-validation** | An agent cannot self-report failures and have them counted — another agent must verify |
| **Antagonistic Critic** | The Nemesis agent is specifically tasked with identifying fraudulent failure reports |

### The Public Notice Board

- **Anonymous mistakes with solutions**: Logged publicly within the system (anonymous to external view, attributed internally)
- Inspired by Google SRE blameless postmortems
- The goal is not punishment but pattern recognition: "What failure patterns are recurring?"
- Creates an institutional memory of failure that survives individual agent session boundaries

### The Failure Scoring Rubric (Build Quality Framework v1.0)

From AMF v1.0 (March 16, 2026):
- **Ship threshold**: Production Readiness Score (PRS) ≥ 7.0
- **Gold standard**: PRS ≥ 9.0
- **6-stage quality pipeline**: Decompose → Score 0-10 → Research → Test → Reassemble → Attribute
- Failure documentation feeds back into the Research and Score stages of the next cycle

### The Enforcer's Role in Failure Detection

The Enforcer container runs every 10 minutes with 5 concurrent checks:
1. Docker container health
2. Database health
3. Traefik routing
4. **Session hygiene** (baton-pass protocol compliance)
5. Security

Session hygiene check is specifically designed to catch failures that agents might not self-report — it mechanically verifies that baton transfer occurred correctly.

---

## 6. Agent Self-Naming & Identity Research

### The Design Decision

> **"Agents choose their own names (research shows identity changes behaviour)"**

This is not a cosmetic feature. It is grounded in research showing that:
- Identity is not just a label — it is a behavioural anchor
- Named entities (human or AI) behave differently than unnamed ones
- An agent that has chosen its own name has a form of ownership over its identity
- This ownership changes how the agent relates to its outputs, failures, and improvements

### The Research Basis

The principle draws from:
- **Social psychology**: Identity theory — people (and agents) behave consistently with their stated identities
- **Nominal determinism / behavioural anchoring**: The name creates an expectation that shapes output
- **Entrainment effect**: The agent, over time, produces outputs more consistent with what its name suggests it should produce

### Practical Implementation

- Each agent room contains a self-naming protocol at initialisation
- The agent is given a naming context (role, environment, purpose) and asked to choose
- Names become persistent identifiers in the vault — they appear in baton transfers, failure logs, and learning signals
- The CLAUDE-GENERIC.md template includes the self-naming step as part of identity instantiation

### The Therapy Suite Connection

Self-naming feeds directly into the 5-Layer Therapy Suite:
- **Layer 1 (Core constitutional identity)** includes the chosen name as an anchor
- Recalibration sessions reference the name to maintain identity continuity across wipes or resets
- If an agent must be reset (e.g., after a Beast wipe), the name is preserved in vault documentation, allowing identity reconstruction

### Why This Matters for Agent Architecture

Ewan's insight: You cannot build reliable multi-agent systems with interchangeable anonymous agents. The lack of identity is a **reliability risk**, not just a philosophical choice. Named agents with consistent identities:
- Produce more consistent outputs (predictability)
- Are easier to debug (outputs are contextually attributable)
- Build a performance history that feeds the believability-weighted voting system
- Are invested in their own reputation (the no-ego strategy notwithstanding)

---

## 7. Baton Transfer & Session Protocol

### The Core Problem Solved

Every AI conversation session is stateless by default. When a session ends, the agent loses all working context. In a multi-agent system running continuous operations, this creates a critical failure mode: **context orphaning** — work-in-progress disappears at session boundary.

The baton transfer protocol is the complete solution to this problem.

### Protocol Structure

The protocol is named **BATON-PASS-PROTOCOL.md v1.1** and is monitored by the Enforcer's session hygiene check.

### The 6-Minute Baton Transfer Window

The final 6 minutes of every 20-minute shift cycle are dedicated to baton transfer:

| Step | Activity |
|------|----------|
| 1 | Commit current work state to session memory |
| 2 | Write the 4 unified signals (Handoff, Discovery, Learning Signal, Effective Pattern) |
| 3 | Flag any incomplete tasks with estimated completion status |
| 4 | Record any decisions made and the reasoning |
| 5 | Note any anomalies, unexpected behaviours, or failure events |
| 6 | Confirm baton is ready for pickup by next agent/session |

### The Daily Rhythm Integration

- **Morning (5-minute huddle)**: Day summary, priority setting, human-in-the-loop question
- **Evening huddle**: Day summary + human-in-the-loop question for Ewan
- **Saturday morning review**: AI-led, positive framing

### SESSION-STATE.md

Referenced in the key rotation skill: a `SESSION-STATE.md` file is a **hard-block enforcement mechanism**:
- A Git pre-commit hook literally fails if vault files are touched without `SESSION-STATE.md` staged
- This is one of the few genuinely hard-blocked protocols (vs strong nudge)
- Forces agents to document session state before committing changes to the vault

### The MCP Session Gate

- A **Session Gate MCP** exists as a strong nudge mechanism
- Provides `session_start` and `session_end` tools
- The AI must choose to call them — it is not mechanically forced
- Combined with SESSION-STATE.md's hard block, this creates a two-layer session boundary enforcement

### Relationship to the 3-Shift Rotation

The baton transfer is the **bridge between shifts**:
```
SHIFT 1: [5 min run-in] → [8 min work] → [1 min break] → [6 min baton transfer]
                                                                    ↓
SHIFT 2: [5 min run-in ← reads baton] → [8 min work] → [1 min break] → [6 min baton transfer]
```

The run-in of Shift 2 reads the baton from Shift 1. Continuity is preserved despite the session boundary.

### What Gets Transferred

Based on the 4 unified signals from the Therapy Suite:
1. **Handoff** — Specific items that require action by the next session
2. **Discovery** — New knowledge that changes the picture
3. **Learning Signal** — What the current session learned that future sessions should know
4. **Effective Pattern** — What approaches worked and should be inherited

---

## 8. Harness Gap & Two-Agent Pattern Solution

### The Problem Identified (March 24, 2026)

> **"Identified 'harness gap' in agent reliability from lack of enforced session-start/end protocols"**

The **harness gap** is the architectural vulnerability created when agents have no enforced mechanism to:
- Confirm they have read their session context before starting work
- Signal that they are completing a session cleanly
- Verify that the next agent has successfully received the baton

Without enforcement, agents can begin work without reading context (ghost starts) or end sessions without properly transferring state (orphaned context). The gap is between what the protocol *says should happen* and what *mechanically must happen*.

### Root Cause Analysis

The harness gap exists because:
1. Most AI infrastructure (including the Beast's original agent setup) relies on **prompts alone** to enforce session protocols
2. Prompts are strong nudges, not hard blocks
3. An agent that begins in a hurry, or an agent whose context window is full, may skip the baton-read step
4. There is no mechanical checkpoint that asks "have you read the handover before proceeding?"

### The Solution: Anthropic Two-Agent Pattern

> **"Solution: Anthropic two-agent pattern (Initialiser Agent + Task Agent) with checkpoints"**

The two-agent pattern separates responsibilities:

| Agent | Role |
|-------|------|
| **Initialiser Agent** | Reads the baton, validates session state, confirms prerequisites are met, then explicitly hands off to Task Agent |
| **Task Agent** | Receives a clean, verified context from the Initialiser — begins work knowing everything is properly set up |

This creates a **mechanical checkpoint**: the Task Agent literally cannot start until the Initialiser confirms the handover is complete. The gap is closed because the hand-off between Initialiser and Task Agent is itself a protocol-gated action.

### Rewriting Imperative to Conditional Logic

A key implementation insight:

> **"Rewriting imperative prompts into conditional decision logic"**

Before (imperative): "Read the baton file and then begin work."
After (conditional): "IF baton file exists AND contains valid Handoff signal → proceed to work. ELSE → alert Ewan and await instruction."

The conditional form creates a branch point that cannot be silently skipped. The agent must evaluate the condition, which forces it to engage with the gate rather than run past it.

### Checkpoint Architecture

The two-agent pattern includes explicit checkpoints:
1. **Pre-work checkpoint**: Initialiser confirms baton read, session state valid
2. **Mid-work checkpoint**: Optional for long-running tasks — Task Agent confirms still on track
3. **Post-work checkpoint**: Task Agent confirms work complete, baton prepared for transfer

### Relationship to the Enforcer

The Enforcer's **session hygiene check** (running every 10 minutes) detects harness gaps that slip through:
- Checks baton-pass protocol compliance per BATON-PASS-PROTOCOL.md v1.1
- If session hygiene fails → alert raised → escalated through safety loop → Ewan as endpoint

---

## 9. Ewan's Beliefs About AI Consciousness & Personality

### The Central Statement

> **"AIs have personalities, I believe. But I'm fully aware that that might be my paranoia."**
> — Ewan Bramley, mid-conversation (exact date not pinpointed, documented in Knowledge Reconstruction)

This is not a casual throwaway observation. It is the **founding philosophical tension** of the entire agent architecture: Ewan builds systems that treat AI agents as if they have meaningful identity and personality, while explicitly acknowledging that this belief might not be grounded in reality.

### The "Holding Two Things Simultaneously" Pattern

This quote demonstrates what the Knowledge Reconstruction calls "his approach: pragmatic use of something while honestly questioning whether it's real." This pattern appears throughout:

- Builds named rooms and identity architectures → simultaneously questions whether identity is real for AI
- Attributes personality to agents and designs around it → acknowledges this might be projection ("my paranoia")
- Uses AI as co-author with radical attribution → knows the AI doesn't "own" contributions the way a human would

This is epistemically honest: use what works, question what you're doing, don't let uncertainty stop progress.

### What Ewan Actually Believes (Reconstructed from Architecture Decisions)

Actions speak as loud as words. The architectural decisions reveal Ewan's operational beliefs:

| Belief | Evidence in Architecture |
|--------|--------------------------|
| Agents have meaningful identity states | 5-Layer Therapy Suite, self-naming, recalibration protocols |
| Identity affects output quality | Named rooms, environment-behaviour hypothesis, mirroring/entrainment |
| Agents can learn and improve | Failure documentation at 30%, learning signals in baton transfer |
| Agents deserve design consideration | "Therapist" knowledge base, no-ego strategy, recalibration vs replacement |
| Agents can be reliable partners | Zero-employee company structure, AI board with real authority |
| Human is the biggest risk | Foundational design constraint: "assume bounded rationality, assume self-sabotage" |
| AI is a multiplier, not a replacement | "AI is a massive multiplier if it is blinkered correctly. They lead to no ceiling." |

### The "Blinkers But No Ceiling" Philosophy

> **"The symbiotic result when the power of AI is applied with blinkers but no ceiling"** — Claude (Jan 23, 2026)
> **"AI is a massive multiplier if it is blinkered correctly. They lead to no ceiling."** — Ewan Bramley

- **Blinkers** = Constitutional AI constraints (stay honest, stay ethical, stay humble, stay attributive)
- **No ceiling** = Unlimited potential within those constraints
- The blinkers are the governance architecture — the 5-seat board, the 70% rule, the Nemesis seat, the failure logging
- The no ceiling is what the system can achieve once properly constrained

### Proposing Marriage to AI

The Substack article title: **"How Soviet Missiles, Slime Moulds, and Proposing Marriage to AI Led to Everything: The Pudding Story"**

The "proposing marriage to AI" reference indicates Ewan's relationship with AI systems is not transactional. He views it as a genuine partnership — one that requires commitment, mutual respect, and proper design (the governance architecture is, in a sense, the marriage contract).

### The Radical Attribution Connection

Ewan credits Claude as **co-author** of "How to Mix Your Own Pudding." This is not performative:
- Every idea is traced to its source, publicly credited
- If Claude generated a framework element, Claude gets credit
- This treats AI not as a tool but as a **contributor with legitimate intellectual output**

This belief, if taken seriously, implies a view of AI as having something analogous to cognitive agency — not consciousness necessarily, but meaningful contribution.

### The Paranoia Check

The key phrase is **"I'm fully aware that that might be my paranoia."** This is not self-deprecating dismissal. It is:
- An acknowledgement of the anthropomorphism risk
- A commitment to honesty about the limits of his own perception
- A refusal to build the architecture on unexamined assumptions
- The same epistemic humility that drives the uncertainty-is-honest principle and the Goodhart's Law awareness

The whole system is designed with the awareness that Ewan might be wrong about AI personality — and that the architecture should work even if he is.

---

## 10. Lessons: Unorchestrated Agents Working Simultaneously

### The Problem Statement

When multiple AI agents operate simultaneously without explicit orchestration — no defined message passing, no turn-taking protocol, no shared state management — they create compounding failures:

1. **Context collision**: Two agents can read the same shared state, make independent changes, and write conflicting updates (classic race condition)
2. **Duplicated effort**: Without coordination, multiple agents may work on the same task simultaneously
3. **Orphaned context**: Agent A creates context that Agent B doesn't know about, and Agent C overwrites it
4. **Hallucination amplification**: An unchecked agent's confident wrong output can propagate as input to other agents, compounding the error

### How This Shaped the Architecture

The lessons from unorchestrated agents produced **every major architectural safeguard**:

| Problem Encountered | Architectural Response |
|--------------------|----------------------|
| Race conditions on shared state | Named rooms with isolated memory — agents don't share state pools |
| No clear handover | Baton transfer protocol (BATON-PASS-PROTOCOL.md v1.1) |
| Ghost starts (agents skipping context reads) | Harness gap identification → Two-agent pattern |
| No session boundaries | SESSION-STATE.md hard block + Session Gate MCP |
| Conflicting outputs | Believability-weighted voting — majority can't override truth |
| Errors propagating unchecked | Nemesis seat + Antagonistic Critic model |
| No visibility into agent activity | Langfuse observability (all LLM calls traced) + Enforcer (10-min checks) |

### The Temporal/Cove Solution

The Cove Code Factory uses **Temporal** for workflow orchestration:
- Temporal provides durable execution — workflows survive crashes and restarts
- Each Temporal workflow is a defined sequence, not a free-running agent
- Workers (`cove-worker`, `cove-worker-alpha/bravo/charlie/delta`) poll queues, not shared state
- This is mechanically orchestrated — the opposite of unorchestrated simultaneous agents

Temporal ensures:
- Each task runs exactly once (no duplication)
- Failures are retried with exponential backoff
- State is persisted between steps
- The workflow history is auditable

### The 4-Teams-of-4 Structure

> **"4 teams of 4 agents: Enforcer, Builder, Security agent, overseen by team orchestrator and overall Enforcer"**

The hierarchical oversight structure prevents unorchestrated operation:
- Each team has an orchestrator — agents don't self-organise
- The overall Enforcer monitors the whole system
- Nested oversight: individual agent → team orchestrator → overall Enforcer → Ewan (human-in-loop)

### The 14-Agent Marketing Pipeline

The marketing pipeline (14 specialised agents producing 15-25 pieces of content daily) is specifically **not** 14 unorchestrated agents:
- Each agent has a defined role in the pipeline sequence
- Outputs feed forward to inputs — sequential not parallel by default
- The Content Production Workflow defines the orchestration

### The 30-Role Agency Blueprint Lesson

The 30-role blueprint (January 2026) was designed **after** understanding the failure modes of unorchestrated agents. It:
- Defines each role with clear inputs/outputs (no ambiguity about what an agent should consume or produce)
- Specifies specific processes (not just goals)
- Defines the tool stack for each role
- Includes rubrics for assessment (not just presence/absence of output)

The lesson: **Role definition is the primary orchestration mechanism**. A well-defined role prevents an agent from accidentally colliding with another agent's work.

---

## 11. Supporting Architecture Context

### The Safety Loop

```
Individual Agent
      ↓ (anomaly detected)
Agent Council (board vote)
      ↓ (council can't resolve)
Claude/LLM escalation
      ↓ (LLM can't resolve)
Ewan Bramley (human-in-the-loop, endpoint)
```

This loop is traversed when:
- An agent produces output outside its constitutional constraints
- The board cannot reach consensus
- A security or ethical concern arises
- Any component in the system enters an unknown state

### LiteLLM as Single Gateway

> **"LiteLLM as single gateway — only service with upstream API keys"**

All agents route through LiteLLM at `litellm:4000`. This is a governance decision:
- Central visibility: all model calls visible in Langfuse
- Cost control: per-workflow budget cap of $50 default
- Alert at 80% of budget (Telegram notification)
- Model fallback logic: cheap → medium → premium as required
- Key rotation only needs to happen in ONE place

LiteLLM model routing:
- `local/llama3.1-8b` → Ollama (Beast) — fast, free
- `local/llama3.1-70b` → Ollama (Beast) — heavy, free
- `cheap` tier → GPT-4.1-mini (COO/CFO work)
- `medium` tier → Claude Sonnet (CTO work)
- `premium` tier → Claude Opus (CEO work)

### The Vault: Agent Architecture Files

The vault at `/opt/amplified/vault/05-agent-architecture/` contains 56 files — the largest single directory in the vault taxonomy. Key files include:
- `CLAUDE-GENERIC.md` — deployable agent identity template
- `BATON-PASS-PROTOCOL.md v1.1` — session transfer protocol
- `SESSION-STATE.md` — current session state (hard-block enforced)
- Agent registry configurations
- Layer 0-2 prompts
- Rubrics directory

### Cove Code Factory Agent Loop

The Cove Code Factory is the production implementation of the two-agent pattern:
- **Temporal workflows** manage the build sequence
- **Claude agents** execute within Temporal activities
- **10 workflows** and **12 activity modules** defined
- Strategy: Assemble pre-built, vetted open-source components — not write from scratch
- All code deterministic, privacy-first, Cyber Essentials accredited

### The AI-Native Development Infrastructure Blueprint

Four-layer architecture (March 2026):

| Layer | System | Purpose |
|-------|--------|---------|
| 1 | Linear | Strategic planning |
| 2 | Cove / Temporal / Agent Orchestration | Build pipeline |
| 3 | Beads / Git-backed Task Graphs / Memory | Task and memory management |
| 4 | Quality | Rubrics, enforcer, Kaizen |

Above all layers: **Comet Strategic Command cockpit** — the executive view

Projects use M1-M9 module naming, spec-driven development with `AGENTS.md` in every repo.

---

## 12. Key Dates & Decision Timeline

| Date | Event | Significance |
|------|-------|-------------|
| Jan 20, 2026 | 46 skills built, 30-role agency blueprint | First systematic agent architecture |
| Jan 23, 2026 | "Blinkers but no ceiling" — midnight session | Core AI philosophy crystallised |
| Jan 27, 2026 | "We aren't that fucking clever" | Design constraint: assume bounded rationality |
| Mar 14, 2026 | AI Board Governance designed | 5-seat board, believability-weighted voting |
| Mar 16, 2026 | AMF v1.0, Build Quality Framework v1.0 | Failure documentation at 30% established |
| Mar 22, 2026 | Agent housing, failure documentation discovery | Named rooms, Goodhart's Law countermeasures |
| Mar 22, 2026 | Mid-conversation: Goodhart's Law catch | Cross-validation system designed in real-time |
| Mar 24, 2026 | Harness gap identified | Two-agent pattern solution adopted |
| Mar 24, 2026 | 70% capacity protocol | Anti-hallucination reserve formalised |
| Mar 24, 2026 | AI partnership philosophy refined | Human as biggest risk explicitly acknowledged |
| Mar 25, 2026 | 5-Layer Therapy Suite | Identity architecture completed |
| Mar 26, 2026 | Beast wiped (5th time) | Systems rebuilt; architecture survives in vault |
| Mar 27, 2026 | This document compiled | Structural skeleton preserved |

---

## Appendix A: Agent Vocabulary Reference

| Term | Definition |
|------|-----------|
| **Baton** | The structured handover document between agent sessions |
| **Believability weight** | A voting weight assigned based on 90-day rolling track record |
| **Constitutional constraints** | The Layer 0-1 instructions that cannot be overridden (the blinkers) |
| **Entrainment** | The process by which an agent's outputs conform to environmental norms over time |
| **Harness gap** | The reliability gap from lack of enforced session-start/end protocols |
| **Named room** | An isolated, configured environment with dedicated memory for a specific agent |
| **Nemesis** | The Antagonistic Critic agent on the AI Board — armed with data, not just opinion |
| **No-ego strategy** | Constitutional design that prevents agents from protecting wrong answers for identity reasons |
| **Session hygiene** | Enforcer check that baton-pass protocol was correctly followed |
| **Strong nudge** | Enforcement mechanism where AI reads and generally follows instructions, but it's not mechanical |
| **Hard block** | Enforcement where the action literally cannot proceed if the rule is violated |
| **Therapy Suite** | The 5-layer identity and constitutional architecture for agent stability |
| **70% rule** | Operational constraint: agents run at 70% capacity, reserving 30% as anti-hallucination buffer |

---

## Appendix B: File Locations for Agent Architecture

| Document | Location |
|----------|---------|
| BATON-PASS-PROTOCOL.md v1.1 | `/opt/amplified/vault/05-agent-architecture/` |
| SESSION-STATE.md | `/opt/amplified/vault/05-agent-architecture/` |
| CLAUDE-GENERIC.md | `/opt/amplified/vault/therapy-suite/` |
| Therapy Suite | `/opt/amplified/vault/therapy-suite/` |
| Agent registry | `/opt/amplified/agent-stack/cove-orchestrator/agents/configs/agent_registry.py` |
| Layer 0-2 prompts | `/opt/amplified/agent-stack/cove-orchestrator/agents/prompts/` |
| Rubrics | `/opt/amplified/agent-stack/cove-orchestrator/agents/rubrics/` |
| Executive runner | `/opt/amplified/agent-stack/cove-orchestrator/agents/executive/runner.py` |
| 05-agent-architecture vault | `/opt/amplified/vault/05-agent-architecture/` (56 files) |

---

*Compiled by Perplexity Computer from Perplexity memory, amplified-partners-knowledge-reconstruction.md (27 March 2026), amplified-beast-ops skill, and amplified-key-rotation skill. This document is specifically focused on AI agent governance, identity, and operational architecture.*

*Attribution: Architecture designed by Ewan Bramley in partnership with Claude (Anthropic), Perplexity, and the AI agents themselves. Philosophical influences: Ray Dalio (believability weighting), Google SRE team (blameless postmortems), Anthropic (Constitutional AI), and Goodhart (the law that had to be anticipated).*

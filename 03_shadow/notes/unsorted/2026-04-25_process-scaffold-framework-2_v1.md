---
title: "The Process Scaffold — Layer 4 of the Business Brain"
id: "process-scaffold-framework-2"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# The Process Scaffold — Layer 4 of the Business Brain

*A deep research report on how every business process, in every vertical, is taken down to runnable granularity — and labelled for deterministic execution, human judgement, or agentic reasoning.*

**Companion to** `business-brain-framework.pplx.md`. This document expands Layer 4 only — the connective tissue between the deterministic core (Layers 1-3) and the agentic execution layer (Layer 5).

---

## Executive Summary

Layer 4 is the single most under-engineered piece of almost every AI deployment. Agents get wired up, databases get provisioned, voice gets polished — but the processes those agents are meant to run remain vibes. That is why 80% of AI projects fail: not because the models are weak, but because nobody has written down, unambiguously, what the business actually does, in what order, and who (or what) is responsible for each step.

The Process Scaffold fixes that. It is a three-standard stack:

1. **APQC Process Classification Framework (PCF)** — the industry-neutral taxonomy that tells you *what* processes exist in a business, decomposed across five levels from category down to individual task. Used by hundreds of leading companies as a common benchmarking language ([APQC — Industry-Specific PCFs](https://www.apqc.org/process-frameworks/industry-specific-process-frameworks)).
2. **BPMN 2.0 + DMN + CMMN — the OMG Triple Crown** — the notation standards for *how* each process actually runs. BPMN for structured sequences, DMN for repeatable decisions, CMMN for unstructured case work ([OMG Triple Crown overview](https://www.omg.org/intro/TripleCrown.pdf)).
3. **ISO 9001:2015** — the compliance-and-audit frame that says *why* the process exists, what must be documented, and how it is continuously improved via PDCA ([Advisera — ISO 9001 mandatory documents](https://advisera.com/9001academy/knowledgebase/list-of-mandatory-documents-required-by-iso-90012015/)).

On top of that stack sits the **Triage Decomposition Rubric** — every leaf task in every process is labelled **D** (deterministic), **H** (human), or **A** (agentic), following the Triage Pattern formalised in recent agentic BPMS literature ([arXiv — Agentic Business Process Management Systems, 2026](https://arxiv.org/html/2601.18833v1)).

The output artefact is precise: **one BPMN file per APQC leaf process**, with any repeatable decisions extracted into a linked DMN table, any unstructured investigations modelled in CMMN, and every task labelled D/H/A with a named executor and an SLA. This is the scaffold the Agentic Execution Layer runs against. Without it, agents hallucinate workflows. With it, they execute them.

This report covers: the APQC taxonomy and how to use it for SMBs; the BPMN element library that matters (stripped back from the 100+ available); when to use DMN versus CMMN versus BPMN; the D/H/A triage rubric in detail; a full worked example (Bob the Plumber, emergency callout) decomposed across all five APQC levels and labelled at every node; ISO 9001 clause-to-artefact mapping; vertical adaptation method; and integration with the existing Build Quality Framework v1.0 and AMPS.

---

## 1. Why Layer 4 Is the Missing Piece

The current industry consensus (March 2026) is that **deterministic orchestration remains essential** for enterprise scale — auditability, predictable outcomes, governance — and that AI agents *expand* the envelope into interpretation, drafting, summarisation, classification, and exception handling, but do not replace the deterministic spine ([BPM Skills in 2026 — Part 3](https://bpmtips.com/bpm-skills-in-2026-part-3/)).

Camunda, the reference BPMN engine, puts this explicitly: "Blend deterministic and non-deterministic process execution to balance control with flexibility. Agents are embedded in BPMN and don't replace processes. Use workflows where possible, agents only where necessary." ([Camunda — AI Agents and BPMN, 2025](https://page.camunda.com/hubfs/EMEA%20W%20and%20APAC%20Events/May%202025%20-%20Camundacon%20Amsterdam/Slidedecks/CamundaCon%202025_%20AI%20agents%20and%20BPMN.pdf)).

This matches the Determinism-Agency-Determinism (DAD) architectural pattern identified by [Volt Active Data, February 2026](https://www.voltactivedata.com/blog/2026/02/agentic-ai-determinism-first-architecture/): deterministic pre-processing, a bounded non-deterministic agentic middle, and deterministic post-processing for persistence and audit. BPMN is the notation that makes DAD legible. APQC PCF is the taxonomy that tells you which processes need it.

For small and medium businesses, the payoff is concrete. **McKinsey's 2025 work-activity automation analysis** places the technical ceiling of automation at 60-70% of activities across sectors; realised SMB savings from well-scoped programmes have been in the 35-45% range. The gap between ceiling and realised is almost entirely a Layer 4 gap. SMBs do not fail because they lack agents — they fail because nobody wrote the process down.

---

## 2. APQC PCF — The Taxonomy

### 2.1 What it is

The APQC Process Classification Framework is an open-standard, industry-neutral taxonomy of business processes maintained by APQC, originally developed in the early 1990s and now in version 7.4.0 (cross-industry). The cross-industry PCF covers the full operating and management span of any organisation and is explicitly designed to allow apples-to-apples benchmarking across companies and sectors ([APQC — Understanding the PCF Elements](https://www.apqc.org/sites/default/files/files/PCF%20Collateral/Understanding%20the%20PCF%20Elements%20%20-%20FINAL.pdf)).

### 2.2 The five levels

Every PCF element sits in a strict five-level hierarchy:

| Level | Name | Scope | Example |
|-------|------|-------|---------|
| 1 | **Category** | Highest-level group of related work | 3.0 Market and Sell Products and Services |
| 2 | **Process Group** | Major work grouping within a category | 3.5 Manage Sales Opportunities |
| 3 | **Process** | End-to-end set of activities producing an outcome | 3.5.3 Convert Prospects to Customers |
| 4 | **Activity** | Major set of actions within a process | 3.5.3.2 Qualify Prospect |
| 5 | **Task** | Specific, named piece of work | 3.5.3.2.1 Verify Prospect Decision Authority |

Each element has a hierarchical number (e.g. `3.5.3.2.1`) plus a unique five-digit APQC ID (e.g. `14213`). APQC reserves IDs 95000–99999 for client-specific custom extensions. This matters: you can legally add your own Level 5 tasks (or even Level 4 activities) without breaking benchmarking comparability, as long as they live in the 95000+ range.

### 2.3 The 13 Level-1 categories (cross-industry v7.x)

The cross-industry PCF divides all business work into **Operating Processes** (what you do to deliver value) and **Management and Support Services** (how you run the business). The current top level:

**Operating Processes**
1. Develop Vision and Strategy
2. Develop and Manage Products and Services
3. Market and Sell Products and Services
4. Deliver Physical Products
5. Deliver Services
6. Manage Customer Service

**Management and Support Services**
7. Develop and Manage Human Capital
8. Manage Information Technology
9. Manage Financial Resources
10. Acquire, Construct, and Manage Assets
11. Manage Enterprise Risk, Compliance, Remediation, and Resiliency
12. Manage External Relationships
13. Develop and Manage Business Capabilities

### 2.4 Industry-specific PCFs

APQC maintains adapted PCFs for specific industries. The Retail PCF, for example, restructures the Operating categories (adding "Develop and Manage Customer Experience", "Merchandise Products and Services") to reflect retail-native work patterns ([APQC — Retail PCF Press Release](https://www.apqc.org/about-apqc/news-press-release/apqc-releases-retail-process-classification-framework)). Other maintained verticals include banking, consumer products, education, petroleum, pharmaceutical, telecommunications, and utilities ([APQC — Industry-Specific PCFs](https://www.apqc.org/process-frameworks/industry-specific-process-frameworks)).

Critically, **no official plumbing, trades, or micro-SMB PCF exists**. This is a gap we fill by using the cross-industry PCF as the spine and adding 95000+ custom tasks for the trades-specific realities (callout dispatch, on-van stock, parts fetch).

### 2.5 Operationalising PCF for an SMB

The default trap is to treat APQC as documentation theatre. The actual use is ruthless:

1. **Map only what exists.** If the business does not do it, it is not in your tree. A single-van plumber has no "3.4 Manage Sales Force" process group.
2. **Stop at the smallest useful level.** Many SMB processes terminate at Level 4 (Activity). Go to Level 5 (Task) only where the task will be run by software or by a named role with an SLA.
3. **One BPMN file per Level 3 (Process).** This is the unit of execution. Level 4/5 items are tasks inside that BPMN file, not separate diagrams.
4. **Use the IBM Blueworks linking pattern.** Each Level 3 PCF node links to its BPMN file; each BPMN file links back to its PCF ID for traceability ([IBM Blueworks — APQC-to-BPMN example](https://community.ibm.com/community/user/automation/blogs/genevieve-van-den-boer1/2019/11/19/example-process-framework-based-on-apqc-pcf)).

---

## 3. BPMN 2.0 — The Structural Notation

### 3.1 Why BPMN and not flowcharts

BPMN 2.0 is a published ISO standard (ISO/IEC 19510:2013) with unambiguous execution semantics. Unlike flowcharts, a BPMN model can be deployed directly to an engine (Camunda, Zeebe, Flowable, Activiti, jBPM) and executed — the diagram *is* the program. For a business brain, this means the process map is not documentation *about* the system; it *is* the system ([Camunda — Essential Agentic Patterns for AI Agents in BPMN, 2025](https://camunda.com/blog/2025/03/essential-agentic-patterns-ai-agents-bpmn/)).

### 3.2 The BPMN library trap

BPMN has over 100 notational elements. Using all of them produces unreadable diagrams. The industry solution is **subsets per abstraction level** — different audiences see different detail levels, drawn from distinct element subsets ([Signavio — BPMN Subsets](https://www.signavio.com/post/bpmn-subsets/)).

We adopt a three-tier subset:

**Overview tier** (board-level, not drawn in BPMN): a simple tile map of the APQC Level 1-2 tree. No BPMN elements at all.

**Operational tier** (the BPMN files themselves, one per Level 3 process). Uses the **Essential BPMN Subset** below.

**Execution tier** (the engine runs this). Adds Zeebe/Camunda extensions: forms, assignments, listeners, boundary events with timers.

### 3.3 The Essential BPMN Subset

The only elements you need, in six groups:

| Group | Element | Icon shorthand | Purpose |
|-------|---------|----------------|---------|
| **Start/End Events** | Start | ○ | Process begins |
| | End | ◎ | Process ends |
| | Message Start | ✉○ | Triggered by incoming message (email, webhook) |
| | Timer Start | ⏱○ | Scheduled (cron, daily, monthly) |
| **Tasks** | User Task | 👤□ | Human does this step |
| | Service Task | ⚙□ | Automated call (API, DB, deterministic script) |
| | Script Task | {}□ | Inline code (validation, transformation) |
| | Business Rule Task | ▤□ | Decision evaluated against a DMN table |
| | **Agent Task** (Camunda extension) | 🤖□ | AI agent with tools, prompt, loop |
| **Gateways** | Exclusive (XOR) | ◇ | Choose exactly one path |
| | Parallel (AND) | ◇+ | All paths run |
| | Event-Based | ◇⌑ | Wait for whichever event fires first |
| **Sub-processes** | Call Activity | □→□ | Calls another BPMN file (reusable process) |
| | Ad-hoc Sub-process | □~ | Set of tasks with no prescribed sequence — agent picks order |
| | Event Sub-process | □! | Triggered by event, handles exceptions |
| **Intermediate Events** | Timer | ⏱◯ | Wait N minutes/hours/days |
| | Message | ✉◯ | Wait for incoming message |
| | Error | ⚡◯ | Throw/catch named error |
| | Escalation | ↑◯ | Bubble up to parent process |
| **Boundary Events** | Timer (interrupting) | ⏱◯ on task | SLA breach — cancel task and reroute |
| | Message (non-interrupting) | ✉◯ on task | Customer replies mid-task, inject context |
| | Error (interrupting) | ⚡◯ on task | Task failed, go to recovery path |

That is it. Everything else in BPMN 2.0 is an optimisation of these 18 elements.

### 3.4 The seven agentic BPMN patterns (Camunda)

Senior Developer Advocate Niall Deehan's canonical breakdown of how agents embed in BPMN ([Camunda — 7 Patterns for Building Better AI Agents Using BPMN, 2025](https://www.youtube.com/watch?v=-TU2v6CooQ0)):

1. **ReAct (Reason + Act)** — Loop between a reasoning task and an action task. Modelled as a sequence flow loop with an exclusive gateway for "continue?" vs "done?".
2. **Modern Tool Use** — Agent is given an explicit list of tools (service tasks it can call) rather than left to hallucinate them. Modelled as an ad-hoc sub-process with the tool palette inside.
3. **Agentic RAG** — Retrieval is itself an agent decision (which corpus, which filter), not a fixed pre-step. Modelled with a business rule task to pick the retrieval strategy, then a service task for the retrieval itself.
4. **Self-Reflection** — Agent output is scored by a reviewer agent against rubric; loop back if below threshold. Modelled as two user/agent tasks in sequence with a quality gateway.
5. **Multi-Agent** — Multiple agents collaborate or compete in separate pools connected by message flows. Each pool is its own swimlane with its own state.
6. **Human-in-the-Loop** — Agent escalates to a user task on uncertainty. Modelled with an escalation event and an event sub-process that creates the human review task.
7. **Long-Running Agentic Orchestration** — Agent work spans hours or days. Modelled with timer events, intermediate message events, and Temporal-style persistence under the BPMN engine.

All seven are **BPMN-native**. No custom framework is needed. This is what "LangGraph inside Temporal inside BPMN" looks like in practice.

---

## 4. DMN and CMMN — The Supporting Standards

BPMN alone is over-stretched when it tries to model two things: branching decision logic, and fundamentally unstructured work. The OMG Triple Crown solves this by pairing BPMN with two siblings ([OMG — Triple Crown overview](https://www.omg.org/intro/TripleCrown.pdf)).

### 4.1 DMN (Decision Model and Notation)

Use DMN when:
- A decision is made more than once
- The decision has multiple inputs
- The decision would otherwise sprawl across five or more gateway branches in BPMN
- The decision rules change faster than the process structure

A DMN decision table is a spreadsheet of rules with a hit policy (Unique, First, Priority, Collect). The FEEL (Friendly Enough Expression Language) is the official expression language.

**Example — Plumbing callout triage decision table:**

| # | Time of Day | Leak Severity | Customer Type | → | Priority | Dispatch Route |
|---|-------------|---------------|---------------|---|----------|----------------|
| 1 | 22:00-06:00 | Flooding | Any | | P1 Emergency | Nearest on-call van |
| 2 | 22:00-06:00 | Dripping | Any | | P3 Next Day | Add to morning queue |
| 3 | 06:00-22:00 | Flooding | Commercial | | P1 Emergency | Disrupt schedule |
| 4 | 06:00-22:00 | Flooding | Residential | | P2 Today | Next available slot |
| 5 | 06:00-22:00 | Dripping | Any | | P3 Next Day | Next available slot |

In BPMN, this entire decision collapses to a single **Business Rule Task** pointing at the DMN table. Change the table, the process updates — no redeploy. This is why DMN exists.

### 4.2 CMMN (Case Management Model and Notation)

Use CMMN when:
- The work is knowledge-driven, not process-driven
- Human judgement determines the next step
- The sequence cannot be predicted in advance
- Examples: customer complaint investigation, insurance claim, HR grievance, creative project, medical diagnosis

CMMN has no sequence flows. Instead, it models **cases** containing **discretionary tasks** that become available when **entry criteria** (sentries) fire. A knowledge worker picks from the available tasks.

**Example — Customer Complaint Case:**

- Case: `Customer Complaint`
- Mandatory stage: `Receive and Log`
- Discretionary tasks (available based on context):
  - Request additional information
  - Offer refund
  - Offer replacement
  - Escalate to manager
  - Offer goodwill credit
  - File regulatory notification (if data-protection complaint)
- Exit criterion: `Customer confirms resolution OR 30 days elapsed`

In an agentic world, CMMN stages are the natural home for **ad-hoc sub-processes** where the agent has the palette but picks the order. [Camunda's MCP human-in-the-loop pattern](https://docs.camunda.io/docs/components/early-access/alpha/mcp-client/mcp-client-human-in-the-loop/) uses exactly this construction.

### 4.3 The decision rule — which notation?

| Work Characteristic | Notation |
|---------------------|----------|
| Fixed sequence, predictable | **BPMN** |
| Branching rules repeated often | BPMN with **DMN** business rule task |
| No fixed sequence, knowledge-driven | **CMMN** |
| Mostly fixed but one unstructured investigation step | BPMN with **CMMN stage** embedded |
| One-off creative work | Don't model. Journal it. |

---

## 5. ISO 9001:2015 — The Audit and Improvement Frame

### 5.1 What ISO 9001 adds

ISO 9001:2015 is the international quality management standard. For a business brain, it contributes three things BPMN cannot:

1. **Mandatory documentation discipline** — a checklist of what must be written down.
2. **PDCA (Plan-Do-Check-Act)** — the continuous improvement loop, mapped to specific clauses.
3. **Records and traceability** — what must be recorded as evidence of execution.

### 5.2 The four mandatory documents

ISO 9001:2015 explicitly requires four documents ([Advisera — ISO 9001 Mandatory Documents](https://advisera.com/9001academy/knowledgebase/list-of-mandatory-documents-required-by-iso-90012015/)):

| Clause | Document | BPMN Layer 4 Artefact |
|--------|----------|------------------------|
| 4.3 | Scope of the QMS | Root README in the process repo |
| 5.2 | Quality Policy | SOUL principles document (Amplified Partners equivalent) |
| 6.2 | Quality Objectives | AMPS targets and Build Quality thresholds |
| 8.4.1 | Criteria for Supplier Evaluation | Vendor scorecard DMN table |

### 5.3 The 18 mandatory records

Records are the trail that proves each process ran. The headline 18 per [Effivity — ISO 9001 Mandatory Documentation](https://www.effivity.com/blog/mandatory-documentation-as-per-iso-90012015-standard):

1. Monitoring and measuring equipment calibration records (7.1.5.1)
2. Records of training, skills, experience, qualifications (7.2)
3. Product/service requirements review records (8.2.3.2)
4. Design and development inputs (8.3.3)
5. Design and development controls (8.3.4)
6. Design and development outputs (8.3.5)
7. Design and development changes (8.3.6)
8. Characteristics of products and services (8.5.1)
9. Records of customer property (8.5.3)
10. Production/service provision change control (8.5.6)
11. Record of conformity of product/service with acceptance criteria (8.6)
12. Record of nonconforming outputs (8.7.2)
13. Monitoring and measurement results (9.1.1)
14. Internal audit programme (9.2)
15. Results of internal audits (9.2)
16. Results of management review (9.3)
17. Results of corrective actions (10.1)
18. Records required by clause 8.4 (externally provided processes, products, and services)

Every one of these maps cleanly to a table row in the Postgres deterministic core (Layer 2 of the Business Brain). The BPMN engine writes to these tables as side-effects of task completion. **Compliance becomes a schema, not a folder.**

### 5.4 PDCA mapped to clauses

ISO 9001 is organised around the PDCA cycle ([Advisera — PDCA in the ISO 9001 Standard](https://advisera.com/9001academy/knowledgebase/plan-do-check-act-in-the-iso-9001-standard/)):

| PDCA Stage | ISO Clauses | Where It Lives in Business Brain |
|-----------|-------------|------------------------------------|
| **Plan** | 4-7 (Context, Leadership, Planning, Support) | APQC tree + BPMN models + DMN tables |
| **Do** | 8 (Operation) | Running BPMN processes on the engine |
| **Check** | 9 (Performance Evaluation) | Postgres event log + metrics + AMPS scoring |
| **Act** | 10 (Improvement) | Daily Kaizen + Build Quality Framework + agent self-reflection |

Clause **4.4.2** is the one that makes ISO demand BPMN: "the organisation shall maintain documented information to support the operation of its processes". BPMN files in a versioned repo are that documented information.

---

## 6. The Triage Decomposition Rubric — D / H / A

This is the piece almost nobody writes down. Every leaf task in every BPMN process gets exactly one label from the set {D, H, A}, following the **Triage Pattern** formalised in [Agentic Business Process Management Systems (arXiv, January 2026)](https://arxiv.org/html/2601.18833v1):

> The Triage Pattern involves intelligent decision-making that dynamically routes cases or activities to the most appropriate executor — human, rule-based, or agent-based. For instance, simple inquiries may be handled autonomously by AI; moderately complex issues that can be solved by executing predefined steps — e.g. billing disputes — may be processed by rule-based systems; and sensitive complaints may be escalated to human actors.

### 6.1 The three labels

**D — Deterministic.** The task has a known input, a known transformation, and a known output. Writing it as code is cheaper, faster, more auditable, and more reliable than an agent call. Example: parse a date, sum a column, generate an invoice number, send a templated email.

**H — Human.** The task requires judgement, relationship, or legal accountability that cannot be delegated to software. Example: sign a contract, take a safety decision on a customer site, fire an employee, override a system suggestion.

**A — Agentic.** The task requires reasoning over unstructured or incomplete information, tool selection, or context-sensitive adaptation. A deterministic script cannot capture the decision space; a human could, but the volume or speed makes it impractical. Example: read five emails and summarise the thread, classify a new service request into 40 categories, draft a follow-up based on call notes.

### 6.2 The decision flow

For every leaf task, ask these questions in order:

1. **Is the input structured and the output computable?** → **D**. Stop.
2. **Is there legal, financial, or safety accountability that must attach to a named person?** → **H**. Stop.
3. **Does the task require interpreting unstructured input or selecting between tools based on context?** → **A**. Stop.
4. **Can't decide?** → Default to **H** and add an agent-assist suggestion. Never default to A. The burden of proof is on the agent.

This matches the published agentic BPMN guidance: "Use workflows where possible, agents only where necessary" ([Camunda — Essential Agentic Patterns, 2025](https://camunda.com/blog/2025/03/essential-agentic-patterns-ai-agents-bpmn/)).

### 6.3 The confidence band

Alongside the label, every agentic (A) task carries a confidence band:

- **A-High** — agent operates autonomously, logged but not reviewed (bulk classification, suggestion generation)
- **A-Medium** — agent operates, human reviews async within 24h (content drafts, low-value decisions under £100)
- **A-Low** — agent drafts, human approves synchronously before effect (customer-facing responses, spending over £100, regulatory filings)

This is the **Confidence Calibration** principle from the Self-Reflection Protocol and the same pattern seen in [Camunda's Human-in-the-Loop Pattern](https://camunda.com/blog/2025/03/essential-agentic-patterns-ai-agents-bpmn/).

### 6.4 Why labelling at the leaf is non-negotiable

Without D/H/A labels:
- You cannot estimate automation potential (you don't know the D:H:A ratio)
- You cannot price a pilot (H is the expensive label)
- You cannot audit (ISO wants to know who did what)
- Agents default to doing everything, including things that should be deterministic — costing money and introducing hallucination where none was needed

With D/H/A labels, the Layer 5 execution engine (LangGraph inside Temporal) can route deterministically: D → service task, H → user task, A → agent task. No ambiguity.

---

## 7. Full Worked Example — Bob the Plumber, Emergency Callout

Bob is a one-van plumbing operation in Newcastle. He already has calendar, WhatsApp, and a price book. This is the APQC → BPMN → D/H/A decomposition of his highest-value process.

### 7.1 APQC placement (custom 95000+ IDs in brackets)

```
5.0   Deliver Services
 └─ 5.2   Deliver Service to Customer
     └─ 5.2.1   Provide Emergency Callout Response     [APQC 95001]
         ├─ 5.2.1.1   Receive and Triage Request       [95002]
         ├─ 5.2.1.2   Dispatch and Travel              [95003]
         ├─ 5.2.1.3   Diagnose and Quote On-Site       [95004]
         ├─ 5.2.1.4   Execute Repair                   [95005]
         ├─ 5.2.1.5   Invoice and Collect Payment      [95006]
         └─ 5.2.1.6   Follow Up and Log                [95007]
```

**One BPMN file**: `5.2.1-emergency-callout.bpmn`.
**Linked DMN tables**: `callout-priority.dmn`, `quote-ladder.dmn`.
**Linked CMMN case**: `complex-diagnosis.case` (used if Activity 5.2.1.3 triggers escalation).

### 7.2 The BPMN in prose (element by element)

| # | Element | Label | Element Type | D/H/A | Notes / Confidence |
|---|---------|-------|--------------|-------|--------------------|
| 1 | Start | Message Start — WhatsApp message received | Event | — | Triggered by inbound message via Green API |
| 2 | Script Task | Extract customer info and issue text from WhatsApp payload | Service | **D** | Deterministic parse of JSON body |
| 3 | Business Rule Task | Classify request severity and urgency | Rule (DMN) | **D** | `callout-priority.dmn` — table of 20 rules |
| 4 | Service Task | Check calendar availability and van location | Service | **D** | API call to Google Calendar and Traccar |
| 5 | Agent Task | Draft customer acknowledgment reply with ETA and price band | Agent | **A-Medium** | Tools: price-book lookup, Met Office weather, canned template lookup |
| 6 | Service Task | Send drafted reply via WhatsApp | Service | **D** | Deterministic post |
| 7 | Timer Event (boundary on #6) | If no customer response in 10 min, escalate | Event | — | Boundary event |
| 8 | Exclusive Gateway | Customer accepts? | Gateway | — | Routes based on reply classification |
| 9 | Agent Task | Classify customer reply (accept / decline / question) | Agent | **A-High** | Short classification, autonomous |
| 10 | User Task | Bob confirms dispatch on his phone | User | **H** | Quick tap-to-confirm — legal commitment |
| 11 | Service Task | Add job to dispatch queue | Service | **D** | DB insert |
| 12 | Service Task | Notify customer of departure | Service | **D** | Templated message |
| 13 | User Task (mobile) | Bob arrives, assesses site, confirms or revises scope | User | **H** | Safety judgement on site — human-only |
| 14 | Business Rule Task | Generate quote from parts + labour + emergency uplift | Rule (DMN) | **D** | `quote-ladder.dmn` |
| 15 | Ad-hoc Sub-process | If diagnosis is unclear: investigate (CMMN case) | Sub-proc | **A-Low / H** | Triggers `complex-diagnosis.case` |
| 16 | User Task | Customer approves quote | User | **H** | Legal — customer signs on phone |
| 17 | User Task | Bob executes repair | User | **H** | Physical work |
| 18 | Script Task | Generate invoice from quote + actual parts used | Service | **D** | Templated |
| 19 | Service Task | Send invoice + payment link | Service | **D** | Stripe integration |
| 20 | Intermediate Message Event | Wait for payment confirmation | Event | — | |
| 21 | Agent Task | Draft follow-up message (thank you + care advice) | Agent | **A-Medium** | Bob reviews before send |
| 22 | User Task | Bob approves follow-up | User | **H** | 10-second review |
| 23 | Service Task | Send follow-up via WhatsApp | Service | **D** | |
| 24 | Service Task | Log job to customer record and learning pool | Service | **D** | Postgres + FalkorDB ingest |
| 25 | End | Callout complete | Event | — | |

### 7.3 Counts

Twenty-five nodes total. Seven are events/gateways (no label). Of the remaining 18 tasks:

- **D (Deterministic)**: 10 tasks (55%) — the invoicing, routing, logging, templated messaging spine
- **H (Human)**: 5 tasks (28%) — on-site judgement, approvals, physical work
- **A (Agentic)**: 3 tasks (17%) — drafts and classifications that need context

This is the ratio to expect for trade services. Professional services (law, accounting) typically show 40/40/20 (more H). Pure digital services (marketing agency content pipeline) can hit 20/20/60 (more A).

### 7.4 The £6-8k/year recovery

For a one-van plumber running 4-6 callouts per day, this BPMN process recovers £6-8k per year in previously-lost billable time, per the established Bob the Plumber baseline. The savings come specifically from:

- 40 minutes/day saved on WhatsApp triage (replaced by tasks 2-6)
- 15 minutes/day saved on invoicing (tasks 18-19)
- 20 minutes/day saved on follow-up (tasks 21-23)
- ~2% uplift in cash collection via automated follow-up

None of this requires Bob to change how he works. The BPMN runs around him. He still signs, judges, and fixes. The scaffold handles everything else.

---

## 8. Vertical Adaptation — The Method

Different verticals need different Level 4/5 details. The method is the same:

### 8.1 Step by step

1. **Start from the cross-industry PCF Level 1-2 tree.** It already covers every vertical.
2. **Pick the 3-5 Level-3 processes that drive 80% of the business value.** For a plumber: callout, recurring maintenance, quote-to-job conversion, stock management, statutory certification (gas safe, water regs). For a law firm: client intake, matter management, time recording, billing, compliance filing.
3. **Model each as a BPMN file.** Use only the Essential Subset (§3.3).
4. **Extract repeated decisions into DMN tables.** If a gateway has more than three branches, it is a DMN table waiting to happen.
5. **Model unstructured investigations as CMMN cases.** Anything that says "it depends what we find" is a CMMN stage.
6. **Label every leaf task D/H/A.** Default to H when uncertain.
7. **Map each BPMN file to its APQC ID.** Use 95000+ for any custom Level 3 you invent.
8. **Wire ISO 9001 records into Postgres side-effects.** Every task completion writes the evidence row.

### 8.2 What is actually vertical-specific

Very little at Level 1-2. Most vertical difference is at Level 3-5, in:

- **The content of DMN tables** (pricing rules, severity triage, compliance tests)
- **The weight of H vs A** (trades are H-heavy, digital services are A-heavy)
- **The industry-specific records** (e.g. Gas Safe certs for plumbers, regulated advice records for financial services, RIDDOR for industrial)

The structural spine — APQC tree, BPMN engine, ISO record schema — is universal. This is why one platform can serve a plumber and a law firm without being rebuilt.

### 8.3 Referenceable SOP libraries per vertical

Where published SOP libraries exist, use them as starter content for Level 5 tasks (then refine with client-specific detail):

- **Accounting / finance**: mature SOP libraries from Scribe, Whale, and professional bodies ([Scribe — SOPs for Accounting Teams](https://scribe.com/library/standard-operating-procedures-accounting), [Whale — Ultimate Guide to Accounting SOPs](https://usewhale.io/blog/sop-for-accounting-department/)) cover AR, AP, tax, payroll, reporting.
- **Legal**: ([Attorney at Work — Law Firm SOPs in Five Steps](https://www.attorneyatwork.com/got-a-process-for-your-processes-create-law-firm-sops-in-5-easy-steps/)) covers intake, document drafting, billing.
- **Trades (plumbing, electrical, HVAC)**: no public SOP library of note, but the feature sets of FieldPulse, Service Fusion, and Shwego implicitly document the canonical trade workflow: quote → schedule → dispatch → execute → invoice → follow-up ([FieldPulse — Plumbing Software](https://www.fieldpulse.com/solutions/plumbing), [Service Fusion — Plumbing Software](https://www.servicefusion.com/plumbing-software), [Shwego — Plumbing Software](https://shwego.com/industries/plumbing/)).
- **Retail**: APQC maintains an official Retail PCF to Level 4 ([APQC — Retail PCF v7.2.1](https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-retail-pdf-version-721)).

---

## 9. Process Discovery — How the Scaffold Gets Populated

The scaffold is useless empty. Populating it fast matters. The state of the art:

### 9.1 Three discovery techniques

1. **Process mining** — analyse event logs from existing systems (CRM, accounting, email) to reconstruct what actually happens end-to-end. Answers: "how does the workflow really flow?"
2. **Task mining** — keystroke/click-level capture on a user's desktop to reveal what a person actually does (vs. what they say they do). Answers: "what repetitive steps are they stuck on?"
3. **Task capture** — user performs a task once with capture on; the tool produces a click-by-click structured document. Answers: "how would we document this for someone else?"

Each has a role. Process mining finds bottlenecks; task mining finds automation candidates; task capture produces the Level 5 SOP text. ([Process Excellence Network — Streamlining Process Discovery](https://www.processexcellencenetwork.com/rpa-artificial-intelligence/articles/streamlining-process-discovery-in-rpa-process-mining-task-mining-task-capture)).

### 9.2 The RPA candidate checklist

When a Level 5 task is discovered, run it through the standard RPA/agent candidacy filter ([Blueprint — RPA Process Assessment Checklist](https://www.blueprintsys.com/hubfs/RPA-Process-Assessment-Candidate-Checklist.pdf)):

- Rule-based with clear logic?
- Repetitive with high volume?
- Structured input data?
- Low variability?
- Free of frequent changes?
- Stable upstream and downstream systems?

Score 6/6 → strong D candidate (deterministic service task).
Score 4-5/6 with ambiguity in input interpretation → A-High candidate.
Score below 4 → H task with agent-assist only.

### 9.3 The integration with systematic literature

[ScienceDirect — RPA Using Process Mining, Systematic Review](https://www.sciencedirect.com/science/article/abs/pii/S0169023X23000897) confirms that successful automation depends on modelling the process in detail before automating. Automating a non-compliant or ineffective process just makes it fail faster. The scaffold-first, automate-second rule is why Layer 4 is Layer 4, not Layer 5.

---

## 10. Integration With Existing Amplified Partners IP

This document extends — it does not replace — two earlier pieces of Amplified Partners architecture:

### 10.1 Build Quality Framework v1.0

The existing six-stage pipeline (Decompose → Score → Research → Test → Reassemble → Attribute) now has a clear home: it runs against the BPMN/DMN artefacts in this scaffold. The PRS formula and ship thresholds (≥ 7.0 to ship, ≥ 9.0 for gold standard) apply per BPMN file. Decompose in the Build Quality Framework *is* the APQC → BPMN → D/H/A decomposition described here.

### 10.2 AMPS (Amplified Process Maturity Score)

AMPS scores a client's process maturity across six weighted dimensions on a 0-10 scale. The scaffold defines the artefacts AMPS measures:

- **Documented (0-10)** — is there a BPMN file for this Level 3 process?
- **Decomposed (0-10)** — is every leaf task labelled D/H/A?
- **Decision-Extracted (0-10)** — are repeated gateways DMN tables?
- **Instrumented (0-10)** — are ISO 9001 records written to Postgres on task completion?
- **Reviewed (0-10)** — is there a Kaizen loop against this process?
- **Continuously Improved (0-10)** — have the metrics moved in the last quarter?

A fully scaffolded process (this document) starts AMPS at ~6/10. The remaining four points come from running it, measuring it, and improving it.

### 10.3 The Enforcer and Daily Kaizen

The Enforcer (the quality gate in the agent architecture) uses the D/H/A labels as hard routing rules. A task labelled D cannot be executed by an agent — the Enforcer blocks the call. A task labelled A-Low cannot be sent without human approval. This is how a rubric stops being advisory and becomes code-enforced.

Daily Kaizen reads the event log, identifies tasks where realised time significantly exceeds modelled SLA, and drafts a BPMN change proposal. The client accepts or rejects. This is PDCA at 24-hour cadence.

---

## 11. Implementation Order for a New Client

For each new client (per the client onboarding skill), the Layer 4 build happens in this order:

1. **Hour 1-4 — Rapid APQC mapping.** Walk through the PCF Level 1-2 tree; tick what the business does; cross out what it doesn't; identify the 3-5 highest-value Level 3 processes.
2. **Hour 4-8 — Process discovery.** Use task capture on the owner's real work for one or two canonical instances per priority process. Produce raw step lists.
3. **Day 2 — First BPMN drafts.** One BPMN file per priority Level 3 process, using only the Essential Subset.
4. **Day 3 — D/H/A labelling and DMN extraction.** Every leaf task labelled; every gateway with 3+ branches extracted to DMN.
5. **Day 4 — ISO record schema.** Map the relevant ISO 9001 records to Postgres tables; wire task completion to writes.
6. **Day 5 — Agent wiring.** The Layer 5 LangGraph/Temporal agents read the BPMN files and execute against them. Humans approve A-Low tasks.
7. **Week 2-4 — Iterate from live event logs.** Process mining on the real runs; refine BPMN and DMN; expand coverage to next Level 3.

This takes one onboarding week to scaffold the high-value spine, not three months. The scaffold is the tool, not the deliverable. The deliverable is the working business.

---

## 12. Common Failure Modes and How to Avoid Them

### 12.1 Over-modelling

Symptom: 400 BPMN files covering every niche. Result: nobody reads any of them.
Fix: Stop at the 3-5 Level 3 processes that drive 80% of value. Park the rest in a backlog.

### 12.2 Under-modelling

Symptom: one mega-BPMN file covering "running the business". Result: unreadable spaghetti.
Fix: One BPMN per Level 3 APQC node. Use Call Activities to compose.

### 12.3 A-labelling everything

Symptom: agents handle tasks that should be deterministic (string formatting, date parsing, database lookups). Result: high cost, hallucination, slow.
Fix: Apply §6.2 decision flow ruthlessly. Default to D when the input is structured.

### 12.4 Not labelling at all

Symptom: BPMN exists but nobody knows which task is human and which is machine.
Fix: D/H/A is mandatory. Every leaf task. No exceptions.

### 12.5 Ignoring CMMN

Symptom: forcing a knowledge-worker investigation into a BPMN sequence. Result: an agent runs off a cliff when a step doesn't fit.
Fix: Use CMMN for investigations. Embed as ad-hoc sub-process inside the BPMN.

### 12.6 BPMN without an engine

Symptom: BPMN drawn in Visio. Result: diagrams, not execution.
Fix: Use a real engine (Camunda Platform 8 on Beast, Zeebe for Amplified Partners clients). The diagram runs. That is the point.

### 12.7 ISO theatre

Symptom: mandatory ISO documents written once and ignored. Result: audit debt.
Fix: ISO records are schema, not folders. Every task completion writes its evidence row. The audit is a SQL query.

---

## 13. Summary — The Layer 4 Artefact Format

For every client, Layer 4 delivers:

```
/process-scaffold/
  README.md                         # QMS scope (ISO clause 4.3)
  soul.md                           # Quality policy (ISO clause 5.2)
  amps-targets.yaml                 # Quality objectives (ISO clause 6.2)
  vendor-scorecard.dmn              # Supplier criteria (ISO clause 8.4.1)
  apqc-map.yaml                     # Full APQC tree (Level 1-5) with owned flags
  processes/
    5.2.1-emergency-callout.bpmn    # One BPMN per Level 3 process
    5.2.1-emergency-callout.md      # Human-readable SOP, generated from BPMN
    callout-priority.dmn            # Linked decision tables
    quote-ladder.dmn
    complex-diagnosis.case          # CMMN cases for investigations
    ...
  labels/
    dha-labels.yaml                 # D/H/A label per leaf task, engine-enforced
  records/
    schema.sql                      # Postgres schema for ISO 9001 records
    mappings.yaml                   # Task-completion → record-insert mappings
  kaizen/
    daily.log                       # PDCA Act-stage change log
```

This is what Layer 4 delivers. Layer 5 (LangGraph in Temporal) reads it and runs the business. Layer 3 (FalkorDB + Graphiti + Qdrant) holds the knowledge the agents draw on. Layer 2 (Postgres) persists events and records. Layer 1 (P2 tokenisation) sanitises integration traffic. Layer 6 (voice and interface) is how the humans interact.

Six layers. One business brain. The process scaffold is the layer that makes everything else honest.

---

*Companion document to `business-brain-framework.pplx.md`. Together these define the architecture of the Amplified Partners build.*

---

**Attribution**
Ewan Bramley (originator, 27 years SMB consulting) x Perplexity Computer (research, synthesis, drafting)
Fact %: 90 — primary claims cross-verified across APQC, OMG, Camunda, Advisera, Effivity, Blueprint, ScienceDirect sources
Confidence: High on architecture and standards mapping; Medium on specific Level-5 task counts (verticals vary)
SOUL: Radically Honest · Radically Transparent · Win-Win
Date: 18 April 2026

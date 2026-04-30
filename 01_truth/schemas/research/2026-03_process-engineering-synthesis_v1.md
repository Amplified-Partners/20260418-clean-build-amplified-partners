---
title: "Process Engineering Synthesis"
id: "process-engineering-synthesis"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "process-engineering-synthesis.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# The Process Engineering Synthesis

*A note for AI build partners on why bounded decomposition is the right unit of work*

Ewan Bramley × Perplexity Computer (Claude Sonnet 4.6)
18 April 2026

---

## The problem this solves

Building AI-native systems for small and medium businesses runs into a predictable failure at the boundary between *what the owner wants* and *what the engineering team can ship.* The owner describes work in irreducible chunks — "handle the emergency call-out", "quote the boiler job", "manage the week's schedule." These chunks are each too large to be a single unit of work for an AI system. They are also too small to be a project. They live in a middle layer that has no natural home in either business language or engineering language.

The synthesis below closes that gap. It takes two well-understood schools of process engineering, keeps the operational core of each, discards the ceremony, and produces a single decomposition method that turns business work into bounded, buildable tasks.

## The two schools

**School one: APQC Process Classification Framework.** A taxonomy for business work that has been refined over three decades across thousands of organisations. It covers every function a business can perform, numbered hierarchically, cross-industry validated. Its value is comprehensiveness and shared vocabulary. Its weakness, for our purposes, is that it describes work at the level of *processes* (1.2.3.4 hierarchical numbering) rather than at the level of *bounded executable tasks.*

**School two: BPMN / DMN** (Business Process Model and Notation / Decision Model and Notation). A modelling standard for representing processes and the decisions embedded in them. BPMN describes flow; DMN describes decision logic. Together they can represent any process as a directed graph of tasks and decisions. Its value is that it compiles — a well-formed BPMN model can be executed by an orchestration engine. Its weakness is that without a taxonomy above it, each team re-invents the vocabulary for every project.

Each school is incomplete alone. APQC tells you *what the work is* but not *how to execute it.* BPMN/DMN tells you *how to execute* but not *what to execute.* The synthesis binds them.

## The synthesis, in one move

**Use APQC to name the work. Use BPMN/DMN to decompose the work into bounded tasks. Tag each bounded task with three attributes: Deterministic, Human, or Agent.**

That's it. Three sentences. The rest of this document explains why each sentence matters and what it produces.

### Naming the work

APQC gives every process a stable number and name. "Quote a boiler replacement" for a plumbing firm sits inside *8.2 Manage customer service operations* with a custom extension for trade-specific work. The number isn't decorative. It means that when the owner says "the quoting thing", the engineering team and the AI system both know which process is being discussed without ambiguity. Shared vocabulary is free when everyone uses the same taxonomy. It is enormously expensive when everyone uses their own.

### Decomposing the work

Once a process has an APQC name, BPMN decomposes it into a sequence of tasks and decisions. A typical SMB process decomposes into 15-25 tasks. Each task is a single bounded action: *retrieve the customer record, check the boiler model against the parts database, calculate the labour estimate, draft the quote document, send it for approval.*

Decomposition stops when each task can be described in a single sentence that starts with a verb and names its input and output. That sentence is the task's specification. If you can't write that sentence, the task isn't decomposed enough.

### Tagging the tasks

Every decomposed task gets exactly one tag:

**Deterministic (D):** the task has a closed-form rule. Given the input, the output is computable. *Calculate VAT on a net total.* *Check whether a date is a bank holiday.* *Retrieve the customer record by phone number.* These tasks do not need an AI. They need a function. Running an AI on a deterministic task is the same mistake as running a human on one — expensive, slow, and error-prone relative to the code that would have done it perfectly.

**Human (H):** the task requires judgement that cannot be decomposed further without losing essential context. *Decide whether to waive the call-out fee for this particular customer.* *Assess whether the customer's description of the fault is credible.* These tasks stay with humans, now and for the foreseeable future. An AI system's job here is to *prepare the human* with the right information at the right moment, not to make the decision.

**Agent (A):** the task requires contextual reasoning that is too broad for a deterministic rule but too bounded to require human judgement. *Draft the quote document in the firm's voice.* *Summarise the customer's fault description for the scheduling team.* *Categorise the incoming email.* This is the AI's actual job. Everything else that the AI does is waste.

## Why this is the right unit of work

The bounded task — one verb, one input, one output, one tag — is the natural unit for an AI system because:

1. **It is individually specifiable.** The specification is a sentence. Specifications this short are easy to review, version, and test.

2. **It is individually testable.** Given the input, the expected output is either computable (D), demonstrable by example (H prep or A), or measurable against a rubric (A output).

3. **It is individually replaceable.** When a better model, a better tool, or a better rule becomes available for one task, that task can be swapped without touching the others.

4. **It is individually priceable.** Each task has a known cost per execution (compute, API calls, human minutes). A process's total cost is the sum of its tasks' costs. Budget conversations become arithmetic.

5. **It is individually routable.** A Deterministic task routes to code. A Human task routes to a person with the right context. An Agent task routes to the AI. The orchestration engine (BPMN runtime) handles the routing mechanically.

## The critical consequence

Once a process is decomposed and tagged, *the build is just arithmetic.* A typical SMB process with 18 decomposed tasks and a 55/28/17 Deterministic/Human/Agent split means:

- 10 tasks are pure code, cheap and reliable
- 5 tasks are human-prep (deliver context at the right moment, collect the decision)
- 3 tasks are agent work (where real AI effort concentrates)

The AI system is now doing three things per run, not eighteen. The expensive work is bounded. The cheap work is automated. The judgement work is preserved where it belongs. Complexity hasn't been added — it's been *sorted.*

## Why this addresses your concern about complexity

Nothing here is novel in isolation. APQC has been used in enterprise process management for thirty years. BPMN/DMN is the standard for process automation. The Deterministic/Human/Agent split is implicit in any well-designed AI system — we have just made it explicit and required.

The synthesis produces less complexity than any of its parts used alone, because:

- APQC alone requires building custom taxonomies per project. The synthesis uses APQC's existing taxonomy.
- BPMN alone requires re-inventing task vocabulary per project. The synthesis inherits vocabulary from APQC.
- Undifferentiated AI systems apply agent reasoning to deterministic work, wasting compute and introducing non-determinism where it isn't wanted. The D/H/A tag prevents this by construction.

The synthesis is not *adding* engineering rigour. It is *replacing* unstructured AI development with the minimum structure that makes AI development tractable at SMB scale.

## What we are not doing

We are not adopting a full enterprise process management suite. APQC is used as a vocabulary only, not as a consulting framework.

We are not modelling every process in full BPMN before building. BPMN is used for decomposition and tag-assignment; the runtime can be any orchestration tool, including simple sequential scripts for early builds.

We are not treating D/H/A as permanent. A task tagged Human today may become Agent when a better model arrives. A task tagged Agent today may become Deterministic when a rule is discovered. The tags are the current state, not a contract.

## The small request

Treat each bounded task as the unit of work. Specify it, tag it, build it, test it, ship it. A process is a sequence of these units, not a thing in itself. An SMB's operating system is a collection of processes, not a thing in itself. A big thing becomes a huge collection of little things, and the little things are all the same shape.

That shape is the unit. That unit is buildable. Everything else follows.

---

## One-page summary for the conversation

- **Name the work** using APQC's existing taxonomy. No new vocabulary.
- **Decompose the work** into tasks of one verb, one input, one output.
- **Tag each task** Deterministic, Human, or Agent.
- **Route accordingly:** D to code, H to people with context, A to the AI.
- **Build incrementally,** one bounded task at a time, with individual tests and costs.

The combined framework is not more complex than ad-hoc AI development. It is less complex, because it prevents three common failures: applying AI to tasks that should be code, applying code to tasks that need judgement, and building at the wrong level of granularity.

This is the smallest viable frame that produces tractable work. Anything simpler loses one of the three failure-prevention properties. Anything more complex is not yet required.

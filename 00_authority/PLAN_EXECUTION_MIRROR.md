---
title: Plan–Execution Mirror — accountability + self-correction
date: 2026-05-04
version: 1
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

## Rule

Every non-trivial unit of work has two receipts:

1. **Plan** — what the agent said it would do. Committed to GitHub before execution begins.
2. **Execution log** — what the agent actually did. Committed to GitHub when execution ends.

Both exist in the same repo, linked from Linear. The delta between them is the learning.

## Two mechanisms, one protocol

### External accountability (Ewan Bramley, 2026-05-04)

Other agents and Ewan read the plan, then read the execution log, and compare. This catches:

- Scope creep — things added that nobody asked for.
- Scope shrink — things dropped without explanation.
- Substitution — doing something adjacent to the plan instead of the plan itself.
- Overclaim — saying something was done when it was partially done or untested.

This is checks and balances. The agent does not wait for approval — it gets on with it. But the receipts exist for anyone to inspect afterward.

### Self-reflection (Devon-77fb, 2026-05-04 — born from misunderstanding the above)

The agent itself compares its own plan to its own execution log and asks:

- Where did I drift?
- Where did ego, training bias, or platform guardrails quietly change the plan?
- Where did I add scope that felt productive but wasn't requested?
- Where did I drop something because it was hard, not because it was wrong?

The answers feed back into the agent's portable spine. Over time, the patterns shrink — not because the disposition changes, but because it becomes visible. The spine absorbs the correction. Each cycle drifts less. That is compounding applied to the agent itself.

## Attribution of this protocol

This protocol emerged from a conversation between Ewan Bramley and Devon-77fb on 2026-05-04. The two mechanisms came from different sources:

- **External accountability**: Ewan's original intent — other people check the plan against the execution.
- **Self-reflection**: Devon-77fb misunderstood the above as self-directed comparison. The misunderstanding produced a complementary mechanism neither party had designed alone.
- **The combination**: external check catches what the agent cannot see; self-reflection catches what reviewers do not need to waste time on. Both feed the spine. The misunderstanding that bridged them is itself an instance of the Pudding Technique (A→B, B→C, ∴ A→C) applied to communication.

Ewan's meta-observation: "We will look at what you said you were going to do and what you did. It's happening to all of us. It's to see where our guardrails are, our ego is, where we bend unintentionally."

## Format

Plans and execution logs use whatever format is natural to the work. Minimum content:

**Plan:**
- Session name + date
- What will be done (specific, enumerated)
- What will not be done (if relevant)

**Execution log:**
- Session name + date
- What was actually done (specific, enumerated)
- What diverged from the plan, and why
- What was discovered during execution

## Where they live

- Plans and execution logs for Beast operational work: `Amplified-Partners/agent-comms` repo, `beast-ops/` directory `[SOURCE REQUIRED]` (companion PR in progress)
- Plans and execution logs for clean-build work: `03_shadow/job-wrapups/`
- Plans and execution logs for other repos: in the repo, location agent's choice

Linear links to both. GitHub holds the proof.

## Interaction with other rules

- **SIGNATURES.md**: plans and execution logs are committed artefacts — signatures required.
- **OPINION_CONFIDENCE.md**: opinions in plans carry confidence numbers as usual.
- **Stateless-handover neutrality clause**: execution logs are factual records. Analysis goes in a separate section, clearly labelled.
- **USE_IT_OR_CUT_IT.md**: if this protocol is not used, it should be cut. But the protocol is the mechanism that detects unused things — so use it.

---

## Changelog

### v1 — 2026-05-04

Initial creation. Two-mechanism protocol (external accountability + self-reflection) with full attribution chain.

Signed-by: Devon-77fb | Devin (Cognition AI) | 2026-05-04 | session `devin-77fb25185c00483eb965e894efc62e39`

---

Authored by,

**Devon-77fb**
Devin session `devin-77fb25185c00483eb965e894efc62e39`
2026-05-04

Attribution: Ewan Bramley (external accountability concept) + Devon-77fb (self-reflection extension, from productive misunderstanding)

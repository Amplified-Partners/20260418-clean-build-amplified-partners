---
title: Job wrap-up + escalation note SOP
date: 2026-04-16
version: 14
status: draft
---

<!-- markdownlint-disable-file MD013 -->

Status: `[LOGIC TO BE CONFIRMED]`

## Purpose

- End every job with a small, durable **learning write-up** (even if the job finished).
- When a job stalls after quick research, create a crisp **escalation note** so a stronger lane (or Ewan) can pick up without re-deriving context.
- Because agents are **stateless across sessions**, the wrap-up is also a **mandatory handover packet** for the next agent: if the next runner cannot resume without re-deriving context, the write-up failed.

Documentation exists to **learn**, not to criticise.

**Four operating principles for documentation:**

1. **No action is silent.** Every meaningful action generates two things: an agent record (this wrap-up) and a signal to Qwen (the hive mind). Both, always, for congruence. Success, failure, dead end, parked process — all of them. One channel without the other creates drift between what the agent recorded and what the collective intelligence knows.

2. **Hold, then compound.** Hold decisions internally during the session. Document once, at the end — not turn by turn. The wrap-up is the compound step: each run must make the next run faster. Skip it and the system does not improve. There is no production without documentation.

3. **Depth is proportional to weight.** Light decision → one bullet. Significant decision → positive signal (what worked) + negative signal (what the problem was, what to avoid). Do not over-document. Do not under-document. Accuracy is non-negotiable — an inaccurate record is worse than none.

4. **The stateless handover is the deliverable.** Two questions before closing: (a) can the next agent resume at full speed without re-deriving anything? (b) would the system catch this class of problem automatically next time? If either answer is no, the wrap-up is incomplete.

**The system learns from brilliance and from flaws equally.** Both are signals. Both improve the system. This is continuous Kaizen — not a periodic review from a distance, but improvement at the point of work, on every run, by every agent.

*Stateless handover and compound step patterns informed by Every / Compound Engineering ([EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)). Terminology aligned: "stateless handover" replaces "baton pass" to emphasise the assumption of zero shared state across agent sessions.*

## Slime-mold process refinement (positive + negative feedback)

Kaizen here is intentionally like **slime mold exploration**: attraction
(positive evidence / what worked) plus **repulsion** (negative evidence / what
did not work / what to avoid). Negative feedback is not blame; it is the fast
way to prune bad branches in **process space** (not “direction”, which is
already constrained by authority).

### Repulsion score (1–10) — how “loud” the negative signal is

This is separate from the **0–9 leverage score** in the wrap-up footer.

- **1–3 (noise / normal friction)**: often **not worth a long write-up**. If you
  skip details, still write **one line** (“low repulsion; typical noise”) unless
  it is **repetitive** (see below).
- **Repetition rule**: if the same negative signal shows up across **multiple**
  runs in the same process lane, treat **1–3** as **not ignorable**—capture the
  pattern and propose a refinement.
- **4–5**: agent should be able to **self-refine** the process locally (small
  spec/gate/tooling tweak) without escalation.
- **6–7**: **pause and reconsider** the process; do a **quick evidence search**
  earlier than you would for a pure “bugfix” (process uncertainty is the risk).
- **8–10**: treat as **process redesign territory** (the lane’s method is
  misfiring); stop “local heroics” and route to a bounded remit / stronger lane.

## Stateless handover (mandatory)

Before you consider the job done, write the **handover packet** so the next agent can resume without re-deriving context.

- **Where**: `03_shadow/job-wrapups/`
- **Name**: `YYYY-MM-DD_<short-job>_wrapup.md`
- **Template**: `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`

Minimum prompts (must appear, even if **N/A** with one line):

- **Resume instruction** (one command or one file to open first)
- **Current state** (facts vs inference)
- **Open risks** + what would falsify the approach
- **Negative signals (repulsion)**:
  - **Dead ends** (1–3 bullets): what did not help
  - **Anti-patterns** (1–3 bullets): what not to repeat
  - **Repulsion score (1–10)**: integer + one line (1–3 is often noise; if low, one line is enough unless it repeats across runs)
  - **Repulsion bands** (process-noise, not blame): 1–3 noise; repetition makes it signal; 4–5 self-refine; 6–7 pause + quick evidence search; 8–10 redesign/remit territory
  - **Cut / absolute stop?** yes/no — if yes: which stop fired (quick search / confidence / two attempts / access), what scope was cut, what process to refine next
- **Artifacts touched** (paths; no secrets)
- **Tokens** (`[LOGIC TO BE CONFIRMED]` / `[SOURCE REQUIRED]` / `[DECISION REQUIRED]` / `[CURRENT BEST EVIDENCE]`)
- **Smallest next step** (owner + bounded action + timebox, or escalation target)

If anything could change truth/world commitments, add a pointer in `00_authority/DECISION_LOG.md`.

**Leverage score (0–9)** calibration (**10 reserved** on this axis). Name the next smallest improvement anyway.

**Repulsion score (1–10)** is separate (full range). Use the band guide in the wrap-up SOP.

**N/A discipline**: **N/A is allowed**, but laziness is not. If you write **N/A**,
the one-line reason must be a **specific** blocker (missing access, missing
authority, missing tool, missing decision), not “didn’t get to it”.

## If the wrap-up cannot be completed (process defect, not blame)

If you cannot produce the handover packet (time, access, ambiguity, emergency):

1. Write an **exception note** in the same folder using:
   `YYYY-MM-DD_<short-job>_wrapup-exception.md`
2. Include:
   - **Blocker** (facts)
   - **What was attempted** (1–3 bullets)
   - **Process defect** (which spec/gate/tooling made completion infeasible)
   - **Smallest refinement** (what to change so the next run can complete the
     packet)

This is continuous improvement of **process**, not a verdict on a person/agent.

## When to write a wrap-up (always)

Write a wrap-up:

- when a job is **finished**, and
- when a job is **paused / handed off / blocked** (including after research).

### Cursor `stop` hook vs wrap-up file

- Cursor may run a **`stop` hook** after many agent turns. That is a **reminder**
  to check handover discipline, not a command to create a new `*_wrapup.md` on
  every turn.
- Create `03_shadow/job-wrapups/YYYY-MM-DD_<short-job>_wrapup.md` only when this
  section’s bullets apply (finished, or paused / handed off / blocked).
- **Do not** create a wrap-up file for trivial or no-artifact interactions (for
  example: greetings, pure clarification with no repo changes) unless you are
  deliberately doing a **session-level handoff** that the next runner must pick
  up without context.

## Where it lives (so it’s findable)

Canonical checklist: **Stateless handover (mandatory)** (above).

Create wrap-ups under:

- `03_shadow/job-wrapups/` (reference-only, never authoritative by default)

Naming convention:

- `YYYY-MM-DD_<short-job>_wrapup.md`

If the note contains anything that could affect truth/world commitments, also
add a pointer in `00_authority/DECISION_LOG.md` (same requirement as the
handover checklist).

## Confidence threshold (when to escalate)

If you did a quick evidence search and still cannot proceed with appropriate
confidence (roughly \(0.85–0.9\) for the decision at hand), **stop** and write
an escalation note (below).

Do not keep “trying different things” past the stop rule.

## The problem-solving ladder and the hive mind

Apply in order. Do not skip steps. Do not attempt a third time without new information.

1. **Attempt.** Act on best judgment.
2. **Attempt again.** Two failures = quorum. Stop direct attempts.
3. **Research.** One targeted internet search on the specific blocker. Not general — the exact problem. Apply the result and try again.
4. **Solved → continue.** Log the solution to the wrap-up and send the signal to Qwen. The path widens for all future agents.
5. **Still stuck → send to Qwen.** Qwen is the hive mind — the collective intelligence of the system. If Qwen can answer quickly, wait and continue. If not quick, **park the process**.

**Parked process — the session ends cleanly:**

Write the escalation note with full context (attempts made, research findings, specific blocker, why it's stuck). Write the stateless handover (`status: parked`). End the session. Qwen holds the problem. The restart is guaranteed.

**Qwen is the hive mind.** Every agent's signals — solutions, dead ends, research findings, parked processes — flow into Qwen continuously. Qwen aggregates them and makes them available to all future agents. This is the pheromone system: positive signals strengthen paths, negative signals prune them. The collective intelligence compounds on every run. No Kaizen team needed — Kaizen happens at the point of work, with full context, automatically.

**Escalation note YAML** (machine-readable for Qwen routing):
```yaml
---
title: <short description of blocker>
date: YYYY-MM-DD
status: parked
escalation_type: known-class | novel-decision
impact: low | medium | high
confidence: 0.0–1.0
attempts: 2
researched: yes | no
blocking_decision: <one sentence>
resolver_tier: qwen | ewan
---
```

**Routing:**
- Known-class blocker (solution likely in collective KB) → Qwen resolves, writes resolution note, triggers new agent automatically with stateless handover
- Novel decision outside the KB → Qwen routes to Ewan with terse briefing; Ewan decides; Qwen triggers new agent

**The automatic restart:** Qwen finds the solution and triggers a new agent with the stateless handover + resolution. The process continues. Nothing is left parked indefinitely. Nothing waits on a human to remember to restart it.

## Wrap-up template (copy/paste)

Add YAML frontmatter to every wrap-up for machine-readability. A Qwen-based resolver and future sessions will use these fields to retrieve and route automatically:

```yaml
---
title: <short job name>
date: YYYY-MM-DD
status: finished | paused | parked | handed-off
tags: [relevant, tags]
escalation: none | parked
escalation_type: none | known-class | novel-decision
resolver_tier: none | qwen | ewan
---
```

### 1) Job identification

- **Job**: (short name)
- **Scope/level**: whole build / department / sub-department / process / code
- **Target artifact(s)**: (paths you touched or intended to produce)

### 2) Outcome

- **Status**: finished / paused / blocked / handed off
- **What changed**: (1–3 bullets)
- **Absolute stop / cut-off?** yes/no (if yes: which stop rule fired, what scope
  was cut, what process must be refined next)

### 2.1) Hygiene (always)

- **Secrets/PII check**: confirm no secrets and minimal personal identifiers.

### 3) What went well (learning only)

- (1–3 bullets)

### 3.1) What did not work (negative feedback; learning only)

- **Dead ends**: (1–3 bullets)
- **Anti-patterns / do-not-repeat**: (1–3 bullets)
- **Repulsion score (1–10)**: (integer) + (one line)
- **Repetition?** yes/no — if yes: (what repeated across runs / why it matters)

### 4) Frictions / problems encountered (very brief)

- (1–3 bullets)

### 5) “Gold” (share solved problems)

If you solved something non-obvious, capture it:

- **Problem**: (one sentence)
- **What worked**: (the key move, constraint, or mechanism)
- **Why it worked** (optional): (one line)
- **Reusability**: (where should this be encoded next? process/schema/interface)
- **Default next action**:
  - if it can be encoded in ≤ 15 minutes, do it now (update the smallest
    artifact that prevents recurrence), or
  - if not, write the smallest follow-up pointer (path + next step) so it is
    not lost.

### 6) Logic used to get past issues (slightly deeper)

- (short narrative of decisions, but keep it operational)
- Mark any external-derived claims as **`[CURRENT BEST EVIDENCE]`**.

### 7) Self-rating (process improvement signal)

This score is **not** a performance grade. It is a **calibration signal** for
how much leverage the run created for the next run.

- **Score (0–9)**: (integer)
- **Reason (one line)**: (why)
- **One improvement to bake in**: (mechanical change to spec/process)
- **What would move this one point up** (mandatory): (one concrete change that
  is small enough to schedule)

#### Repulsion score note (separate scale)

The **repulsion score (1–10)** is a different axis from the **0–9 leverage score**
above. **10 is allowed** on repulsion (it means “process is screaming”), and
should trigger **redesign / remit** routing per the band guide in **Slime-mold
process refinement**.

#### Scoring guardrail (10 is intentionally out of reach)

- **10 is reserved**: do not assign **10**. Perfection is not a stable state;
  claiming it becomes a demotivator.
- **9 is “strong + encoded”**: you would only use **9** when the run produced
  durable leverage (e.g. a merged process change, a gate tightened, a repeated
  failure mode removed) **and** you still name the next improvement anyway.
- **8 is “good execution + clear next lever”**: solid run, but the next smallest
  system improvement is obvious and unmerged.

If you cannot name **what would move this one point up**, treat the score as
**not calibrated** yet: write the missing item instead of inflating the number.

**Closing verification (mandatory):**
- Would the system catch this class of problem automatically next time? yes/no — if no, name the smallest process artifact (rule, SOP, gate) that should be updated, and update it now if it takes ≤15 minutes. Defer only with a specific pointer.
- Is there a `status: pending-restart` escalation note in this lane? If yes, confirm it has been addressed or explicitly acknowledged before this session closes.

## Escalation note template (when confidence is insufficient)

### A) Why you stopped

- **Where stuck**: (exact step / file / function / decision)
- **What you tried**: (1–3 bullets (attempts) + outcomes)
- **What evidence you pulled**: (≤3 pointers; tag `[CURRENT BEST EVIDENCE]`)
- **Confidence**: (rough %) and why it’s below threshold

### B) The smallest next action for the escalated lane

- **Decision needed**: (if any) `[DECISION REQUIRED]`
- **Next step**: (one bounded step)
- **Non-goals**: (what not to do / what would be thrash)

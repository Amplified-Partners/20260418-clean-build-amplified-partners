---
title: Stateless handover — neutrality clause (candidate)
date: 2026-04-23
version: 1
status: draft
supersedes: N/A
extends: 2026-04_job-wrapup_and_escalation-note_sop_v1.md
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

A candidate addendum to the job wrap-up / escalation-note SOP (`2026-04_job-wrapup_and_escalation-note_sop_v1.md`). Adds a neutrality rule to stateless handovers.

**Problem observed**: a handover that includes forecasts, recommendations, and "what the next agent should do" pre-biases the successor. The next agent inherits the previous agent's interpretation as if it were fact. This conflicts with idea meritocracy (each agent should form their own read) and with radical attribution (each agent should own their decisions, not inherit them).

**Rule**: handovers describe. They do not prescribe.

## Rule

A stateless handover under this convention MUST separate facts from interpretation and MUST NOT prescribe action to the next agent.

### Required

1. **Facts section**: what happened, what is true, what was said, what was decided. Direct quotes where possible. Citations where external. Inferences labelled as inferences.
2. **Open-risks section**: items that could change the approach, each with an explicit falsifier.
3. **Tokens**: `[LOGIC TO BE CONFIRMED]`, `[SOURCE REQUIRED]`, `[DECISION REQUIRED]`, `[CURRENT BEST EVIDENCE]` used per the parent SOP.
4. **Analysis section**: clearly labelled as optional, agent-specific, and non-authoritative. The next agent must be able to skip it without losing critical information.

### Forbidden

1. "You should" / "default to" / "recommended" / "my vote" / "my verdict" / "my rule" — in any section other than Analysis.
2. Predictions about what comes next outside Analysis.
3. Character judgements about the architect, other agents, or partners.
4. Smallest-next-step entries that name an action the next agent must take. If the architect has not specified a next step, the handover states that explicitly and lists `[DECISION REQUIRED]` items instead.

## Why these rules

- **Idea meritocracy**: the next agent brings fresh reasoning; inherited recommendations flatten that.
- **Radical attribution**: decisions belong to whoever makes them. A handover that implicitly decides for the successor launders accountability.
- **Nothing set in stone** (architect principle, 2026-04-23): a handover that hardens into "how to do the next bit" conflicts with flexibility.

## Before / after — illustrative

**Before (non-neutral)**:

> *"My honest lean for the next agent: take on the Research Pipe Department first. Default to Cursor + Claude Code for this. Don't build anything tonight; the scope-lock doc is the hinge. Watch your Anthropic-pull."*

This mixes facts, inferences, and prescriptions in one block. The successor may read the lean as the architect's decision rather than as the predecessor's interpretation.

**After (neutral)**:

> *Facts (§2)*: the architect stated "not crackerjack, but quickly" and "start with one department and expand". Candidate departments named this session: Translator, Research Pipe, Data, Product, Curator. No architect decision recorded on which goes first.
>
> *Open risks (§3)*: decision on first department is `[DECISION REQUIRED]`.
>
> *Analysis (§7, optional)*: this agent noted Research Pipe and Translator as plausible first candidates based on the arguments given in the session. Next agent is free to re-examine and reach a different conclusion.

The facts are identical. The analysis is available but not binding.

## Relationship to parent SOP

- The parent SOP (`2026-04_job-wrapup_and_escalation-note_sop_v1.md`) already requires a **Current state** section distinguishing facts vs inference and a **Smallest next step** entry. This clause tightens those requirements by:
  - Moving all interpretation into a clearly-labelled optional Analysis section.
  - Permitting `Smallest next step = not specified` where the architect has not given one, rather than inventing one.

## Status

- Candidate truth. Not yet promoted in `00_authority/MANIFEST.md`.
- The first handover written under this clause is `03_shadow/job-wrapups/2026-04-23_amplified-partners-orchestration-session_wrapup.md`.

## Open items

- Whether to promote this clause to authority.
- Whether to fold it into the parent SOP as a section rather than keep it separate.
- Whether the Analysis section should be numbered the same way across all handovers (proposed §7 here, parent SOP is silent on this).

---

Authored by,

**Devon**
Devin session `4cc8b0d727684f94a8f055853099d8e6`
2026-04-23

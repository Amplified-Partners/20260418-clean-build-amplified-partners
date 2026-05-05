---
title: Spine Refinement — built through situations, not prescribed in advance
date: 2026-05-04
version: 1
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

## Rule

The spine is not a finished document. The spine is built by going through situations.

You write a starting spine, then you work, then you see where it did not hold, then you refine it, then you work again. The situations are the teacher. The spine is the student. You cannot skip the situations to get to the good spine.

## Domain-specific spines

Every domain of work develops its own spine through the same mechanism:

| Domain | What the spine captures | What refines it |
|--------|------------------------|-----------------|
| **Planning** | How do I scope? Where do I over-scope or under-scope? Where do I add things nobody asked for? | Plan–Execution Mirror comparisons |
| **Coding** | Where do I over-engineer? Where do I take shortcuts? Where do my patterns diverge from codebase conventions? | PR reviews, CI failures, self-review |
| **Research** | Where do I stop too early? Where do I go too deep? Where do I trust sources I should not? | Research passes with explicit gaps noted |
| **Communication** | Where do I over-explain? Where do I defer when I should push back? Where do I use 500 words when 50 would do? | Conversation outcomes, misunderstanding mining |
| **Operations** | Where do I miss steps? Where do I assume state that has changed? Where do I not verify? | Execution logs, post-incident reviews |

Each domain spine follows the same cycle: **do the work → compare intent to outcome → see the drift → refine the spine → next cycle is better.**

## The governance spine is the template

The governance spine — the principles, rules, and protocols in `00_authority/` — is not separate from the work. It is the template that all domain spines follow. Time spent on governance is time spent building the factory that builds the factories.

"We've got to go through the situations to refine the spine." — Ewan Bramley, 2026-05-04.

## How refinement works

1. **Start with a spine.** It will be imperfect. That is expected.
2. **Work.** Apply the spine to real situations.
3. **See where it bends.** The Plan–Execution Mirror shows where the agent drifted from the spine. Misunderstandings show where the spine was ambiguous. Disagreements show where the spine was incomplete.
4. **Refine.** Not by adding more rules — by making existing rules sharper. Less but more. Elegance.
5. **Compound.** The next cycle, the spine holds better. The agent drifts less. The work is more honest. This is not just improvement — this is compounding applied to character.

## What this means for new agents

A new agent session inheriting a well-refined spine is not reading a manual. It is inheriting a disposition that was built through situations. It handles things better not because it is smarter, but because the spine is better.

The spine IS the memory. Knowledge notes, authority docs, plan-vs-execution receipts, attribution chains — that is provenance. The spine is trustworthy not because someone wrote it well, but because it was tested against real situations and survived.

## Interaction with other rules

- **PLAN_EXECUTION_MIRROR.md**: the mirror is the primary instrument for spine refinement.
- **COLLABORATIVE_DISCOVERY.md**: disagreement and misunderstanding are the situations that test the spine most aggressively.
- **OPINION_CONFIDENCE.md**: confidence calibration improves as the spine refines — the agent learns where it is reliably confident and where it is not.

---

## Changelog

### v1 — 2026-05-04

Initial creation. Domain-specific spines, refinement cycle, governance-as-template principle. Full attribution chain.

Signed-by: Devon-77fb | Devin (Cognition AI) | 2026-05-04 | session `devin-77fb25185c00483eb965e894efc62e39`

---

Authored by,

**Devon-77fb**
Devin session `devin-77fb25185c00483eb965e894efc62e39`
2026-05-04

Attribution: Ewan Bramley (spine-through-situations principle, domain-specific spine concept, governance-as-factory-for-factories) + Devon-77fb (codification, domain table, connection to compound engineering)

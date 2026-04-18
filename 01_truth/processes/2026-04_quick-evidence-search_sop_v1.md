---
title: Quick evidence search SOP (bounded external lookup)
date: 2026-04-16
version: 2
status: draft
---

Status: `[LOGIC TO BE CONFIRMED]`

## Purpose

Define what a **quick evidence search** looks like: enough authority for
agents to **resume execution** on narrow unknowns, without a firehose, a
formal remit, or smuggling external text as settled truth.

## When to use

- Default for a **single missing fact** or a **narrow** `[SOURCE REQUIRED]`
  (see `00_authority/NORTH_STAR.md` → quick evidence search path).
- If three assessed bits cannot answer the question, **stop** and escalate
  (consult → formal remit) instead of widening the search into a dump.
- If, after the search, you still cannot proceed with appropriate confidence
  (roughly \(0.85–0.9\) for the decision at hand), **stop** and write an
  escalation note:
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`.

## Before you search (mandatory)

Write down, in one place:

1. **Question** (one sentence).
2. **Three parameters** you will use to rank results (examples: recency,
   primary vs secondary source, jurisdiction, product/version,
   “official spec vs commentary”).
3. **Stop condition**: what would count as “answered enough to proceed” vs
   “must escalate”.

## During the search

- Prefer **primary** sources (vendor docs, standards, statutes, repo/issue,
  paper DOI) over aggregators when parameters say so.
- Do **not** paste long pages into chat or authority docs; capture
  **pointers** (URL + title + accessed date) and the smallest excerpt needed.

## After the search (mandatory shape)

Return **at most three** items. Each item must contain:

- **Pointer**: stable URL or archive path + title + access date.
- **Excerpt**: ≤ 2 sentences **or** one tight fact line (no walls of text).
- **Why this bit**: one line tying the excerpt to the parameters (why it is
  in the top three).
- **Token**: mark the finding and any conclusion drawn from it as
  **`[CURRENT BEST EVIDENCE]`** — current best external read; **not**
  promoted working fact until it passes normal gates
  (`00_authority/PROMOTION_GATE.md`, manifest indexing, evidence rules in
  `00_authority/BUILD_LOOP.md`).

If you have more than three plausible hits: **pick** the three that best
satisfy the declared parameters; list the rest only as optional “next
lookup” titles (no excerpts), or omit them.

### Operational handoff fields (mandatory when the next step needs people)

If the quick search is meant to unblock **execution** (not just satisfy
curiosity), also include a short block:

- **Owner**: who acts next (role/person/team)
- **Next step**: one bounded action
- **Due time**: when that action should be revisited (timebox)

If not applicable, write **N/A** with one line explaining why.

## Authority boundary

- Quick search output **does not** move anything to **Authoritative now** in
  `00_authority/MANIFEST.md` by itself.
- Import hygiene for raw captures remains: `00_authority/NORTH_STAR.md` →
  “When you import outside material”.

## Idea meritocracy

The ranking is by **declared parameters and fit to the question**, not by who
proposed the search. Operator, agent, or third-party logic is interchangeable
here; only **traceability + parameters + cap of three** matter for this SOP.

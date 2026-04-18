---
title: Canonical agent entry + permissions + human operator voice
date: 2026-04-17
status: finished
tags: [authority, routing, agents, permissions, transfer]
escalation: none
---

## Resume

Next agent: **single canonical entry** for clean-build agents is root
**`AGENTS.md`** → **§ Agent session (clean-build) — first 60 seconds**. **`MANIFEST.md` v31** adds **§ Permissions** (GitHub org repo creation = human operator;
`.cursor/` policy/hooks vs mechanical edits + `HOOKS_TESTING_NEED`). Human layer
(questions vs diktats; diktats in committed rules) lives in **`AGENTS.md` § Outcome**
and **`PROJECT_INTENT.md` v5**. **`DECISION_LOG.md` v5** records the decision.
**`NORTH_STAR.md` v10** points at the canonical entry and aligns `90_archive`
wording with **`90_archive/README.md`**.

## Current state

- **Done**: PARTNER_TRANSFER v8 + changelog; NORTH_STAR v10; MANIFEST v31;
  `90_archive/README.md` immutability/provenance paragraph; `01_truth/README.md`
  defer line; DECISION_LOG entry; prior README / authority README / AGENTS /
  PROJECT_INTENT already aligned from earlier pass in this thread.
- **Open risks**: none. **Operator follow-up:** run `qwen_signal` out-of-band if
  your stack requires it beyond this file’s `## qwen_signal` block.

## Repulsion / cut

- N/A.

## Artifacts touched (this continuation)

- `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`
- `00_authority/NORTH_STAR.md`
- `00_authority/MANIFEST.md`
- `90_archive/README.md`
- `01_truth/README.md`
- `00_authority/DECISION_LOG.md`
- `03_shadow/job-wrapups/2026-04-17_canonical-entry-permissions-human-voice_wrapup.md`

## Tokens

Session-sized; documentation-only.

## Smallest next step

Operator: `git add` + commit when ready; no code or hooks changed.

## qwen_signal

Topic: canonical-entry-permissions-human-voice-2026-04-17 — positive path:
one entry (`AGENTS.md` § first 60s) + explicit permissions in MANIFEST + human
voice in PROJECT_INTENT/AGENTS + DECISION_LOG surface; archive language de-conflicted
with provenance posture.

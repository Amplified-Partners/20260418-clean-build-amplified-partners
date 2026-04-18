---
title: Wrap-up — Partner execution contract (intent-confirm then complete)
date: 2026-04-16
status: finished
---

### Resume instruction

Open `00_authority/PRINCIPLES.md` and review `## Collaboration norms (how to operate)`.

### Current state (facts vs inference)

- **Facts**:
  - Added explicit partner contract language to `AGENTS.md`: intent confirmation,
    agent-first language, transferability, and end-to-end completion.
  - Updated `00_authority/PRINCIPLES.md` to v35 with new collaboration norms
    encoding the same behavior.
  - Updated `00_authority/NORTH_STAR.md` translation contract with a 3-step
    operational default (confirm intent, execute end-to-end, encode reusable method).
  - Updated `00_authority/MANIFEST.md` to v25 and synced principles anchor to v35+.
  - Added a decision entry in `00_authority/DECISION_LOG.md`.
- **Inference**:
  - This reduces variation in agent behavior and makes partner expectations
    explicit for future sessions.

### Open risks + what would falsify the approach

- **Risk**: wording may still be interpreted differently by different model
  families.
  - **Falsify**: repeated runs that still skip intent restatement or stop short
    of end-to-end completion.
- **Risk**: overlapping guidance across several authority files can drift.
  - **Falsify**: contradictory phrasing appears in future edits.

### Negative signals (repulsion)

- **Dead ends**:
  - None material; updates were direct and aligned with existing direction.
- **Anti-patterns**:
  - Avoid adding prose that is not operationally testable by an agent.
- **Repulsion score (1–10)**: 2 — low-friction alignment update.
- **Repulsion bands** (process-noise, not blame): 1–3 noise; repetition makes it signal; 4–5 self-refine; 6–7 pause + quick evidence search; 8–10 redesign/remit territory
- **Cut / absolute stop?** no

### Artifacts touched (paths; no secrets)

- `AGENTS.md`
- `00_authority/PRINCIPLES.md`
- `00_authority/NORTH_STAR.md`
- `00_authority/MANIFEST.md`
- `00_authority/DECISION_LOG.md`
- `03_shadow/job-wrapups/2026-04-16_partner-execution-contract_wrapup.md`

### Tokens

- N/A — no new unresolved logic/source/decision tokens introduced.

### Smallest next step (owner + bounded action + timebox, or escalation target)

- **Owner**: Ewan + next partner run
- **Action**: validate on next 2–3 tasks that agents consistently restate intent
  and complete end-to-end; if not, tighten examples in `AGENTS.md`.
- **Timebox**: 20 minutes total across next runs.

### Leverage score (0–9)

- **Score (0–9)**: 7
- **Reason (one line)**: Converts a spoken meta-expectation into explicit
  authority-level operating behavior.
- **One improvement to bake in**: add a tiny checklist snippet in `AGENTS.md`
  for what "intent confirmation" must contain.
- **What would move this one point up**: encode that checklist and verify with a
  short process test artifact in `01_truth/processes/`.


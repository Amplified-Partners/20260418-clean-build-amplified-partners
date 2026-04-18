---
title: Wrap-up — Stop hook vs wrap-up file scope (full plan executed)
date: 2026-04-16
status: finished
---

### Resume instruction

Open `.cursor/hooks/stateless-handover-stop.py` and confirm the new paragraph after the italic hook line.

### Current state (facts vs inference)

- **Facts**:
  - Plan approved: align hook copy, Cursor rule, SOP, decision log, and partner instructions so wrap-up **files** are job-scoped, not every Cursor `stop`.
  - SOP was already at v14 with subsection **Cursor `stop` hook vs wrap-up file**; `DECISION_LOG.md` already contained entry **Stop hook reminder vs wrap-up file duty**.
  - Completed deferred edits in Agent mode: `.cursor/hooks/stateless-handover-stop.py` and `.cursor/rules/stateless-handover-kaizen.mdc` now state the same scope guard; `AGENTS.md` gained a matching bullet; decision log “where encoded” includes `AGENTS.md`.
- **Inference**:
  - Agents should stop writing `_wrapup.md` after greetings/no-op turns unless doing an explicit session handoff.

### Open risks + what would falsify the approach

- **Risk**: Some agents still treat any injected “mandatory” heading as a hard order.
  - **Falsify**: repeated no-op wrap-up files after this rollout.
- **Risk**: Cursor stdin never sets `stop_hook_active` on chained stops (separate from this change).
  - **Falsify**: duplicate reminder spam returns; revisit chain detection only.

### Negative signals (repulsion)

- **Dead ends**: Plan mode initially blocked `.py`/`.mdc` edits; required mode switch.
- **Anti-patterns**: Declaring wrap-up mandatory per turn without defining “job.”
- **Repulsion score (1–10)**: 3 — process friction, now reduced by explicit copy.
- **Repulsion bands** (process-noise, not blame): 1–3 noise; repetition makes it signal; 4–5 self-refine; 6–7 pause + quick evidence search; 8–10 redesign/remit territory
- **Cut / absolute stop?** no

### Artifacts touched (paths; no secrets)

- `.cursor/hooks/stateless-handover-stop.py`
- `.cursor/rules/stateless-handover-kaizen.mdc`
- `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` (v14; subsection present)
- `00_authority/DECISION_LOG.md`
- `AGENTS.md`
- `03_shadow/job-wrapups/README.md`
- `03_shadow/job-wrapups/2026-04-16_stop-hook-wrapup-scope_fix_wrapup.md`

### Tokens

- N/A — no new unresolved authority tokens introduced by this fix.

### Smallest next step (owner + bounded action + timebox, or escalation target)

- **Owner**: Ewan + next agent run
- **Action**: After a few real sessions, spot-check `03_shadow/job-wrapups/` for spurious wrap-ups; if noise persists, shorten hook headline wording further.
- **Timebox**: 15 minutes review.

### Leverage score (0–9)

- **Score (0–9)**: 8
- **Reason (one line)**: Closes the semantic gap between product `stop` frequency and handover file duty across hook, rule, SOP, and `AGENTS.md`.
- **One improvement to bake in**: Optional one-line in `03_shadow/job-wrapups/README.md` pointing to SOP subsection **Cursor `stop` hook vs wrap-up file**.
- **What would move this one point up**: Add that README pointer in one edit.

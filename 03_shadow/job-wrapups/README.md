---
title: Job wrap-ups (learning notes)
date: 2026-04-17
version: 6
status: draft
---

<!-- markdownlint-disable-file MD013 -->

Status: `[NON-AUTHORITATIVE]`

This folder stores **job wrap-ups** and **escalation notes**.

- Purpose: learning + handoff clarity, not blame.
- Authority: reference-only; nothing here becomes authoritative by proximity.
- Template: `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
- When to create a wrap-up file: see SOP subsection **Cursor `stop` hook vs wrap-up file**.
  **There is no registered `stop` hook** (`.cursor/hooks.json` → `"hooks": {}`); the
  SOP still documents the *conceptual* split (trivial turn vs real job end). Follow
  SOP job-end rules only — no hook reminder fires.

## Stateless handover (mandatory)

Use the checklist in the SOP section **Stateless handover (mandatory)** (same
headings as `.cursor/rules/stateless-handover-kaizen.mdc`):
resume instruction, current state, open risks, repulsion block (dead ends,
anti-patterns, repulsion score + bands, cut/absolute stop), artifacts touched,
tokens, smallest next step; plus leverage **0–9** (**10 reserved**) vs
repulsion **1–10** (separate axis). **N/A** is allowed only with a one-line
specific reason.

Naming convention:

- `YYYY-MM-DD_<short-job>_wrapup.md`

If you cannot complete the wrap-up, write:

- `YYYY-MM-DD_<short-job>_wrapup-exception.md` (blocker + process refinement)

Cursor enforcement:

- Rule: `.cursor/rules/stateless-handover-kaizen.mdc` (`alwaysApply`)
- **Hooks: none (production).** `.cursor/hooks.json` → `"hooks": {}`. **TESTING NEED**
  only if you ever re-wire hooks — read and satisfy **`.cursor/HOOKS_TESTING_NEED.md`**
  first; do not enable for day-to-day work without that gate.
- Dormant script (not invoked): `.cursor/hooks/stateless-handover-stop.py`. History:
  `03_shadow/2026-04-16_stop-hook_followup-checklist-loop_bug-report.md` (§ Final resolution).

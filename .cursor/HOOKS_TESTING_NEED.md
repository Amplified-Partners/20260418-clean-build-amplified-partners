# Cursor hooks — **TESTING NEED** (not production)

**Status:** No hooks are registered. This workspace intentionally keeps
`.cursor/hooks.json` as `"hooks": {}`.

## Why

Per `03_shadow/2026-04-16_stop-hook_followup-checklist-loop_bug-report.md` (§ Final
resolution): Cursor’s `stop` hook fires **per turn**, not per session, which
produced unavoidable follow-up noise. Handover discipline lives in:

- `.cursor/rules/stateless-handover-kaizen.mdc` (`alwaysApply`)
- `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`

## **TESTING NEED** — before any hook is re-enabled

Do **not** wire hooks for “real” work until **all** of the following are explicit
and signed off (human operator + manifest/decision log if policy changes):

1. **Purpose** — which event, which script, what user-visible effect.
2. **Loop risk** — proof that follow-up cannot recurse or spam the UI each turn.
3. **Exit** — how to disable again (`hooks` back to `{}`) in one step.
4. **Docs** — `00_authority/MANIFEST.md`, `03_shadow/job-wrapups/README.md`, and this
   file updated to match reality.

The script at `.cursor/hooks/stateless-handover-stop.py` is **preserved only** for
optional experiments under the above gate — **not** invoked while `hooks` is empty.

---
title: Bug report — stop hook re-emits full handover checklist (felt “loop”)
date: 2026-04-16
status: draft
---

<!-- markdownlint-disable-file MD013 -->

Status: `[NON-AUTHORITATIVE]` (shadow diagnostic; not promoted truth)

## Summary

The **Cursor `stop` hook** configured in this workspace runs
`.cursor/hooks/stateless-handover-stop.py` on every `stop` event. That script
always returns a **full multi-line handover checklist** as `followup_message`
(~1705 characters). Each agent completion that triggers `stop` therefore surfaces
**the same checklist again**, which can feel like a **loop**, independent of
whether the user typed it as a template.

## Symptoms

- The full “# Stateless handover (mandatory) …” block appears repeatedly in the
  product UI around agent turns.
- User reports it is **not** coming from a personal text template; sensation of
  an unexplained loop.

## Configuration (code)

- `/.cursor/hooks.json` registers `stop` →
  `.cursor/hooks/stateless-handover-stop.py`.
- The script builds a fixed `msg` string and writes
  `{"followup_message": msg}` to stdout.

## Runtime evidence (NDJSON log)

**Log path:** `.cursor/debug-6cbcd2.log`  
**Session ID:** `6cbcd2`  
**Instrumentation (historical):** during investigation, NDJSON lines were
appended from `stateless-handover-stop.py`; that logging has been **removed**
after verification (log excerpts below remain as evidence of the pre/post
sizes).

Captured **two** `stop` invocations in one session (timestamps ~1.9s apart). Each
pair: `stop_hook_invoked` then `emit_followup_message`.

```json
{"sessionId": "6cbcd2", "hypothesisId": "H2_stdin", "location": "stateless-handover-stop.py:main", "message": "stop_hook_invoked", "data": {"stdin_len": 673}, "timestamp": 1776361046973, "runId": "stop-hook"}
{"sessionId": "6cbcd2", "hypothesisId": "H1_followup_payload", "location": "stateless-handover-stop.py:main", "message": "emit_followup_message", "data": {"followup_chars": 1705, "followup_starts_with": "# Stateless handover (mandatory)\\n\\nBefore you con"}, "timestamp": 1776361046973, "runId": "stop-hook"}
{"sessionId": "6cbcd2", "hypothesisId": "H2_stdin", "location": "stateless-handover-stop.py:main", "message": "stop_hook_invoked", "data": {"stdin_len": 672}, "timestamp": 1776361066855, "runId": "stop-hook"}
{"sessionId": "6cbcd2", "hypothesisId": "H1_followup_payload", "location": "stateless-handover-stop.py:main", "message": "emit_followup_message", "data": {"followup_chars": 1705, "followup_starts_with": "# Stateless handover (mandatory)\\n\\nBefore you con"}, "timestamp": 1776361066855, "runId": "stop-hook"}
```

### Interpretation

- **H1** — Each `stop` emits the same large checklist in `followup_message`:
  **CONFIRMED** (`followup_chars` 1705, identical prefix twice).
- **H2** — Hook runs on Cursor `stop` pipeline (stdin present):
  **CONFIRMED** (`stdin_len` 672–673).

**Not ruled out by this log alone:** always-on rule
(`.cursor/rules/stateless-handover-kaizen.mdc`) also duplicating context in the
model; that would be separate from hook NDJSON.

## Root cause (engineering)

**By design of the current hook:** every `stop` event produces the same
`followup_message` payload. The product then shows that payload again →
**repetition scales with the number of `stop` events**, not with “template” text
the user typed.

## Instrumentation status

Debug NDJSON logging was used to confirm **H1/H2**, then **removed** from
`.cursor/hooks/stateless-handover-stop.py` after the short follow-up was
verified.

## Recommended next steps (product choice)

1. **Keep** — accept full checklist on every `stop` (current behavior).
2. **Shorten** — replace `followup_message` with a one-liner + pointer to
   `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
   (and keep detail in SOP / rule).
3. **Disable** — remove the `stop` entry from `.cursor/hooks.json` if the
   injection is too noisy (rule + SOP still document the requirement).

After any change: clear `.cursor/debug-6cbcd2.log`, trigger two stops, confirm
log shape and UI.

## Artifacts touched (this investigation)

- `.cursor/hooks/stateless-handover-stop.py` — short `followup_message`
  (investigation used temporary NDJSON logging, since removed).
- `03_shadow/2026-04-16_stop-hook_followup-checklist-loop_bug-report.md` —
  this file.

## Resolution (implemented — SHORTEN)

- **`followup_message`** in `.cursor/hooks/stateless-handover-stop.py` was
  replaced with a **short-v1** pointer (~**506** characters vs ~**1705**
  previously). The **full checklist** remains the source of truth in
  `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` and
  `.cursor/rules/stateless-handover-kaizen.mdc`.
- Post-fix verification used NDJSON (`followup_chars` ~505,
  **`followup_variant`: `short-v1`**); that debug logging was then **removed**.
- **Clarity pack:** hook `followup_message` now opens with an italic line labeling
  it as the Cursor **stop** hook; `.cursor/rules/stateless-handover-kaizen.mdc`
  and `AGENTS.md` note short injection vs full checklist; `03_shadow/job-wrapups/README.md`
  links this bug report under Cursor enforcement.

## Smallest next step (verification)

Restart Cursor if hooks are cached, trigger a `stop`, and confirm the follow-up
is the **short** pointer (paths + two bullets + `DECISION_LOG` line), not the
long checklist. NDJSON logging is no longer written to
`.cursor/debug-6cbcd2.log`.

## Final resolution (2026-04-16) — hook disabled, system redesigned

**Decision:** hook disabled entirely (not just shortened). `.cursor/hooks.json` `hooks` set to `{}`. Hook script preserved at `.cursor/hooks/stateless-handover-stop.py` for reinstatement if Cursor adds a true session-end event.

**Rationale:** the per-turn loop was not fixable within Cursor's `stop` hook architecture. Every `stop` event is per-turn, not per-session. Shortening the `followup_message` reduced noise but did not fix the structural cause. The agent's response to the followup creates a new turn, which fires a new stop, which is a new loop — `loop_limit: 1` only blocks the immediate chain, not a new conversational turn.

**What replaced the hook:**
- `.cursor/rules/stateless-handover-kaizen.mdc` (`alwaysApply: true`) — the agent always has the operating principles in context without injection or loop
- `AGENTS.md` — updated with documentation philosophy, autonomy decision matrix, three-tier escalation model, natural feedback logic (quorum sensing, slime mold, viral/bacterial), and session-start acknowledgment
- `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` — updated with hold-then-compound principle, proportionality, YAML frontmatter for machine-readability, three-tier escalation routing, and automatic restart loop design

**Net effect:** loop eliminated at source. Agent operates from principles, not injected prompts. Documentation is proportional, accurate, and designed for the compound loop. Escalation notes are machine-readable for future Qwen-based Tier 1.5 resolver. Every / Compound Engineering attributed where their patterns appear.

**Artifacts touched:**
- `.cursor/hooks.json`
- `.cursor/rules/stateless-handover-kaizen.mdc`
- `AGENTS.md`
- `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md`
- `03_shadow/2026-04-16_stop-hook_followup-checklist-loop_bug-report.md` (this file)

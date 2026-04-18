---
title: Job wrap-up — stop hook follow-up loop
date: 2026-04-16
job: stop-hook-followup-loop
---

## Resume instruction

Open `.cursor/hooks/stateless-handover-stop.py`, then `.cursor/hooks.json`.

## Current state

**Facts**

- Prior chat transcript `6cbcd258-0fdf-4f81-9756-1b5247b4cefe` ends with **two consecutive** `<user_query>` blocks containing the **same** `followup_message` body from the stop hook (handover reminder), i.e. the hook text surfaced twice back-to-back as user turns.
- The hook previously **discarded stdin** and always printed `{"followup_message": ...}`, which matches a follow-up chain re-injecting the same reminder on every `stop`.

**Inference (pending Cursor verification)**

- Cursor likely sets `stop_hook_active` on hook-driven continuation stops (same pattern as Claude Code stop hooks). Local CLI check: `echo '{"stop_hook_active": true}' | .cursor/hooks/stateless-handover-stop.py` → `{}` and NDJSON `skip_followup_chain_stop`.

## Open risks + falsification

- **Risk:** Cursor’s stdin may omit `stop_hook_active` or use a different key → gate never fires.
  - **Falsify:** After a real agent run, read `.cursor/debug-f827aa.log`: if every line shows `"stop_hook_active": null` across two stops yet the UI still duplicates the handover block, extend parsing or rely on `loop_limit` only.
- **Risk:** `loop_limit` in `hooks.json` might be ignored or rejected by some Cursor versions.
  - **Falsify:** Hooks output channel shows a parse error; remove `loop_limit` and re-test.

## Negative signals (repulsion)

- **Dead ends:** Guessing stdin schema without transcript + one local stdin simulation.
- **Anti-patterns:** Shipping a “short” checklist that still always re-`followup_message`s on every stop in a chain.
- **Repulsion score:** 4 — repetition was user-visible and confusing; localized fix.
- **Repulsion bands:** 4–5 self-refine (hook + config).
- **Cut / absolute stop?** no

## Artifacts touched

- `.cursor/hooks/stateless-handover-stop.py` — parse stdin; gate on `stop_hook_active`; NDJSON debug log (session `f827aa`).
- `.cursor/hooks.json` — `loop_limit`: 1 on the `stop` hook entry.

## Tokens

- N/A for this hygiene fix.

## Smallest next step

- **Owner:** Ewan — restart Cursor if hooks cache, complete one agent turn that hits `stop`, then a second natural stop after any hook-driven continuation.
- **Timebox:** 5 minutes; inspect `.cursor/debug-f827aa.log` for `skip_followup_chain_stop` on the second stop if the chain fires.

**Leverage score:** 6 (stops noisy re-injection; small diff, high annoyance reduction).

**Repulsion score:** 4 (see above).

## Post-fix verification (NDJSON, session `f827aa`)

Source: `.cursor/debug-f827aa.log` (and mirror `.cursor/hooks/debug-stop-hook-f827aa.ndjson`).

- **H_snake_only REJECTED for Cursor:** payload showed **`stopHookActive`** at top level, not `stop_hook_active` (e.g. log line with `"stdin_top_keys": ["stopHookActive"]`, `"stopHookActive": true` → `skip_followup_chain_stop`).
- **H_emit CONFIRMED for normal stop:** payload included `conversation_id`, `loop_count`, `hook_event_name`, etc., with both flags null/omitted → single `emit_followup_message` (`followup_chars`: 641).
- **Follow-up:** debug NDJSON was **removed** from the hook after this evidence; production hook now gates on **`stopHookActive` + `stop_hook_active`** (top level + shallow container keys only).

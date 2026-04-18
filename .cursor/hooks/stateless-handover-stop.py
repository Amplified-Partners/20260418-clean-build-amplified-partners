#!/usr/bin/env python3
"""
Cursor stop hook: inject a mandatory stateless handover / Kaizen wrap-up prompt.

Reads hook JSON from stdin. When the session is already in a hook-driven follow-up,
Cursor sends `stopHookActive` (camelCase) and/or `stop_hook_active` (snake_case)
as truthy — then return `{}` so the same `followup_message` is not re-injected.

Also checks one level under common container keys (`input`, `payload`, `context`,
`metadata`, `data`) in case the flag is nested without a full-tree walk (avoids
false positives from large transcript-shaped subtrees).

Short follow-up points to SOP + always-on rule (full checklist not inlined).
See: 03_shadow/2026-04-16_stop-hook_followup-checklist-loop_bug-report.md
"""

from __future__ import annotations

import json
import sys

_CHAIN_KEYS = ("stop_hook_active", "stopHookActive")
_CONTAINER_KEYS = ("input", "payload", "context", "metadata", "data")


def _truthy(v: object) -> bool:
    return v in (True, "true", "True", 1, "1")


def _stdin_payload() -> dict:
    raw = ""
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        out = json.loads(raw)
        return out if isinstance(out, dict) else {}
    except json.JSONDecodeError:
        return {}


def _chain_active(payload: dict) -> bool:
    for key in _CHAIN_KEYS:
        if _truthy(payload.get(key)):
            return True
    for ckey in _CONTAINER_KEYS:
        sub = payload.get(ckey)
        if isinstance(sub, dict):
            for key in _CHAIN_KEYS:
                if _truthy(sub.get(key)):
                    return True
    return False


def main() -> int:
    payload = _stdin_payload()

    if _chain_active(payload):
        sys.stdout.write("{}")
        sys.stdout.flush()
        return 0

    msg = "\n".join(
        [
            "# Stateless handover (mandatory)",
            "",
            "_Cursor **stop** hook — short reminder only; full checklist lives in "
            "the wrap-up SOP + `.cursor/rules/stateless-handover-kaizen.mdc`._",
            "",
            "This hook can run on **every** Cursor `stop`; that is not the same as "
            "owing a wrap-up file every time. **Only** create "
            "`03_shadow/job-wrapups/YYYY-MM-DD_<short-job>_wrapup.md` when the "
            "wrap-up SOP says so: job **finished**, or **paused / handed off / "
            "blocked** (including after research). **Skip** for trivial or "
            "no-artifact turns (e.g. greetings, pure Q&A) unless you are doing an "
            "explicit session handoff.",
            "",
            "Before you consider the job done, write the **handover packet** in "
            "`03_shadow/job-wrapups/` as `YYYY-MM-DD_<short-job>_wrapup.md`.",
            "",
            "Full minimum prompts, repulsion bands, leverage vs repulsion, and "
            "templates are in:",
            "- `01_truth/processes/2026-04_job-wrapup_and_escalation-note_sop_v1.md` "
            "(section **Stateless handover (mandatory)**)",
            "- `.cursor/rules/stateless-handover-kaizen.mdc`",
            "",
            "If truth/world commitments could change, add a pointer in "
            "`00_authority/DECISION_LOG.md`.",
        ]
    )

    sys.stdout.write(json.dumps({"followup_message": msg}, ensure_ascii=False))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

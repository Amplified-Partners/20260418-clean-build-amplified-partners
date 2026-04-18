# `90_archive/` — gate for agents

Status: `[NON-AUTHORITATIVE]`  
Purpose: **Sanitised reference** — legacy snapshots, narrative context, and bulk
imports. **Never** treat as current policy or production truth.

**Immutability (audit posture):** verbatim **history** snapshots (e.g.
`authority-history/`) are **not** rewritten to “update” policy — they record what
was believed then. Current law lives in `00_authority/` + manifest. New material
lands here via **transfer / sanitisation** rules; **triage** may add files under
`inbox/` — that is not the same as editing authority.

## Agent rules (read first)

1. **Do not bulk-read** `90_archive/inbox/` (or other dumps) end-to-end. Those
   files exist for **human triage** and selective promotion into `01_truth/`.
   Only open paths **explicitly named** in your task, manifest, or decision log.
2. If you need a principle: read `00_authority/` first, not an archive copy.
3. **Authority-history** (`90_archive/authority-history/`) is verbatim old
   `00_authority/` — useful for diffing intent, **not** for “what we do now.”
4. **Context** (`90_archive/context/`): operator voice / `[NARRATIVE]` — see
   `90_archive/context/README.md`.

## Relation to the clean-build file budget

This tree **supports** agent clarity by **quarantining** noise and provenance
outside `00_authority/` and `01_truth/`. It does not replace them.

Signed-by: Keystone (AI) — 2026-04-17

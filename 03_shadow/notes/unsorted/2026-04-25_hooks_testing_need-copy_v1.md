---
title: "HOOKS_TESTING_NEED.md"
id: "hooks_testing_need-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

<!-- [NON-AUTHORITATIVE] gate checklist before any Cursor hook wiring -->

# HOOKS_TESTING_NEED.md

Production posture: no hooks (`"hooks": {}` in `hooks.json`).

## Gate checklist before any hook is activated

- [ ] Hook script tested in isolation (not just syntax-checked)
- [ ] Failure mode defined: what happens if the hook errors?
- [ ] Confirmed: hook does not block work it should not block
- [ ] Reviewed by Ewan before activation

Do not activate hooks by editing `hooks.json` without completing this checklist.

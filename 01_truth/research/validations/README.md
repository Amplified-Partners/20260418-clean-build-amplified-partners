---
title: "Truth-tier validations directory"
date: 2026-05-03
status: candidate
signed_by: "Devon-ab74 | 2026-05-03 | devin-ab740f2c78ee477a9c16ea3b6ed15293"
parent_ticket: AMP-67
---

# `01_truth/research/validations/`

Promotion target for verdicts produced by `02_build/validators/` once they
have been reviewed and accepted as authoritative.

## Lifecycle

```
02_build/validators/  →  03_shadow/validators/<vertical>/<INS-NNN>/verdict.json
                                          │
                                          │  (human review pass)
                                          ▼
                          01_truth/research/validations/<vertical>/<INS-NNN>.md
```

Each promoted file is a short markdown summary with:

- The verdict band (PROVEN / PLAUSIBLE / DISPROVEN)
- A one-line finding
- The evidence bundle (source URLs, accessed dates, sha256 hashes)
- A `signed_by` line for the reviewer who promoted it

The catalogue's `VALIDATION:` line is then re-pointed from the shadow JSON
to the truth-tier markdown.

## Status

This directory is currently empty — no verdicts have been promoted yet.
The first promotion candidate is the AMP-67 ProfServices sweep, which
will be reviewed before any entries land here.

## Schema

See `01_truth/schemas/2026-05_public-data-validation_v1.md`.

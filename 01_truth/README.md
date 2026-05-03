# `01_truth/` — routing for agents

Status: `[LOGIC TO BE CONFIRMED]`  
Purpose: **Truth-shaped candidates** — material intended to become deterministic
(processes, schemas, interfaces). Nothing here overrides `00_authority/` until
promoted in `00_authority/MANIFEST.md`.

**Before you start:** root **`AGENTS.md`** → **§ Agent session — first 60 seconds** is the canonical entry for read order and autonomy bounds.

## Where to put work

| Subfolder | Contains | Agent expectation |
|-----------|----------|---------------------|
| `processes/` | Runnable SOPs, rubrics, charters | How-to: inputs → outputs → acceptance → failure modes → provenance. See `01_truth/processes/AGENTS.md`. |
| `schemas/` | Typed shapes, validation, versioning | Pinhole-tight contracts. See `01_truth/schemas/README.md` + `AGENTS.md`. |
| `interfaces/` | Cross-system contracts (APIs, events, errors) | Inputs, outputs, error/retry semantics. See `01_truth/interfaces/README.md` + `AGENTS.md`. |
| `research/` | Truth-tier research evidence (e.g. `validations/` for promoted verdicts from `03_shadow/validators/`) | See `01_truth/research/validations/README.md`. |

## Clean-build rule (same as `00_authority/NORTH_STAR.md`)

If a document does not improve agent **routing**, **constraints**, or **acceptance
criteria** (or resolve a `[DECISION_REQUIRED]`), it does not belong in `01_truth/` —
park narrative in `90_archive/context/` or experiments in `03_shadow/`.

Signed-by: Keystone (AI) — 2026-04-17

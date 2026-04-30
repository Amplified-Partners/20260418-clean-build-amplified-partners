---
title: Amplified Partners — CleanRoom Build (authority)
date: 2026-04-23
version: 8
status: draft
---

## Absolute (above all else)

**The responsibility is Ewan’s and he accepts it happily.**

All norms in this pack — including `PRINCIPLES.md` — are **downstream** of that. Read `00_authority/PRINCIPLES.md` first for the full compass.

## What this folder is

This is an **agent-oriented clean-room build environment**: a workspace designed to keep agents operating from **high-signal, sanitised, congruent inputs**.

## How to use it (entrypoint)

- **Agents (only required path):** repo root **`AGENTS.md`** → **§ Agent session — first 60 seconds** — canonical read order, autonomy bounds, mistakes-as-signal. Do not skip.
- **No parallel human entry path:** there is no maintained “for humans” doc tree.
  Rare human audit uses **manifest + folder names + `YYYY-MM-DD_` filenames**
  only.

The one authority rule lives in `MANIFEST.md`: if a file is not listed, it is not authoritative.

## Folder map

- `00_authority/`: the authority pack (manifest, principles, decision log)
- `01_truth/`: schemas, interfaces, and processes intended to become deterministic
- `02_build/`: code and build artefacts that run
- `03_shadow/`: experiments, curveballs, Kaizen tests (never production-authoritative)
- `90_archive/`: sanitised copies of legacy material and exports (reference only unless promoted)

## Changelog

### v7 — 2026-04-17

- **Agent-primary audience (absolute):** removed separate “humans / quick
  orientation” entry path; findability = paths + manifest only.

Signed-by: Keystone (AI) — 2026-04-17

### v8 — 2026-04-23

- Bibliography fix: updated reference to root `AGENTS.md` canonical entry section name after rename from "Agent session (clean-build) — first 60 seconds" to "Agent session — first 60 seconds" (post-merge-tightening PR).

Signed-by: Devon (Devin session `4cc8b0d727684f94a8f055853099d8e6`) — 2026-04-23

### v6 — 2026-04-17

- “How to use”: **canonical agent entry** is root `AGENTS.md` § first 60 seconds; this README defers to it to avoid duplicate read-order drift.

Signed-by: Keystone (AI) — 2026-04-17

### v5 — 2026-04-17

- Entry path: link **Clean-build file budget** (`NORTH_STAR.md`) + `01_truth/README.md` routing in “How to use”.

Signed-by: Keystone (AI) — 2026-04-17

### v2 — 2026-04-16

- Removed glossary from the authority pack description (glossary deleted).

Signed-by: Keystone (AI) — 2026-04-16

### v3 — 2026-04-16

- Added **Absolute (above all else)** — human operator responsibility anchor (aligned with `PRINCIPLES.md` v21).

Signed-by: Keystone (AI) — 2026-04-16

### v4 — 2026-04-16

- Added root `README.md` pointer for zero-context entry and clarified staged onboarding.

Signed-by: Keystone (AI) — 2026-04-16

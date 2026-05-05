---
title: Amplified Partners — CleanRoom Build (authority)
date: 2026-04-17
version: 7
status: active
---

# Absolute (above all else)

The responsibility is Ewan's and he accepts it happily.

All norms in this pack — including PRINCIPLES.md — are downstream of that. Read `00_authority/PRINCIPLES.md` first for the full compass.

## What this folder is

An agent-oriented clean-room build environment: a workspace designed to keep agents operating from high-signal, sanitised, congruent inputs.

## How to use it (entrypoint)

**Agents (only required path):** repo root `AGENTS.md` → § Agent session (clean-build) — first 60 seconds — canonical read order, autonomy bounds, mistakes-as-signal. Do not skip.

No parallel human entry path. Rare human audit uses manifest + folder names + YYYY-MM-DD filenames only.

The one authority rule lives in MANIFEST.md: if a file is not listed, it is not authoritative.

## Folder map

- `00_authority/`: the authority pack (manifest, principles, decision log)
- `01_truth/`: schemas, interfaces, processes, and known-issues — intended to become deterministic
- `02_build/`: code and build artefacts that run
- `03_shadow/`: experiments, wrap-ups, Kaizen tests (never production-authoritative)
- `90_archive/`: sanitised copies of legacy material and exports (reference only unless promoted)

---
Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd

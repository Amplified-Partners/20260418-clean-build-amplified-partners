---
title: Project intent (clean room build)
date: 2026-04-16
version: 2
status: draft
---

## Status

This document is a **starting point** for the clean-room build. It contains a mix of confirmed constraints and `[LOGIC TO BE CONFIRMED]` hypotheses. For norms on how agents should work (including “best on the day” and human-operator ownership), see `00_authority/PRINCIPLES.md`.

## Purpose (what we are building) `[LOGIC TO BE CONFIRMED]`

Working hypothesis: we are building an **AI-native operating environment** for Amplified Partners:

- a **deterministic core** (“database of reality”) for black-and-white operational truth
- a **process layer** that makes as much work as possible deterministic
- a **semantic layer** (graph / vectors / retrieval) that adds relationship context without polluting truth
- a **shadow path** for Kaizen testing and “curveballs” that must not touch production until promoted deliberately

The immediate mission in this clean room is to make the environment **congruent** so assistants can execute safely and quickly.

## Success definition (how we know we’re winning)

An assistant working *only* inside this clean room can:

1. Identify what is **authoritative** vs what is **reference** (from `MANIFEST.md`).
2. Build or refine deterministic artefacts (schemas, contracts, processes) without needing legacy context.
3. Stop cleanly when logic is missing by using `[LOGIC TO BE CONFIRMED]` rather than guessing.
4. Move faster over time because the workspace becomes progressively more coherent and sanitised.
5. Work **independently** at **best on the day** (see `00_authority/PRINCIPLES.md`) — without owing perfection, and without hiding uncertainty — while the **human operator** remains able to observe, decide, and unblock from the **right perspective** (not only from inside the code).

## Non-negotiables (constraints)

- **Privacy first**: no client secrets in tracked content; minimise personal data.
- **Radical honesty / transparency / attribution**: do not invent facts; cite sources; show what is assumed.
- **Win–win only**: duty-of-care posture in outputs and decisions.
- **Congruence over cleverness**: contradictions are surfaced, not smoothed.
- **Deterministic-first (90/10)**: facts + processes first, models for the remainder.

## What is in scope (initial)

- Establish the **authority pack** in `00_authority/` (manifest, principles, transfer instructions, remit, decision log, and related authority docs as listed in `MANIFEST.md`).
- Populate `01_truth/` with:
  - schemas for the “database of reality” `[LOGIC TO BE CONFIRMED]` (exact tables/shape to be confirmed)
  - initial deterministic processes `[LOGIC TO BE CONFIRMED]`
  - interface contracts and failure modes `[LOGIC TO BE CONFIRMED]`
- Set up `90_archive/` as a sanitised staging area where legacy material can be referenced without diluting authority.

## What is out of scope (for now)

- Building the full production system end-to-end in one pass.
- Importing large volumes of unsanitised legacy content.
- Any “HR / employee monitoring” posture (explicitly out of scope).

## Known gaps (explicit)

- `[LOGIC TO BE CONFIRMED]` exact schema for the SQL “database of reality”
- `[LOGIC TO BE CONFIRMED]` what the first vertical / first proof-of-value slice is
- `[LOGIC TO BE CONFIRMED]` what the initial automated pipelines are (API/Unix pipe sources and refresh cadence)

## Working agreement (how we proceed)

- If a claim lacks provenance: mark `[SOURCE REQUIRED]`.
- If a decision is required to proceed safely: mark `[DECISION REQUIRED]`.
- If logic is incomplete: mark `[LOGIC TO BE CONFIRMED]` and stop guessing.

## Changelog

### v2 — 2026-04-16

- Removed obsolete glossary reference from in-scope authority pack; pointed **Status** and success criteria at `PRINCIPLES.md` for agent independence and human-operator ownership; removed time-bound session wording.

Signed-by: Keystone (AI) — 2026-04-16

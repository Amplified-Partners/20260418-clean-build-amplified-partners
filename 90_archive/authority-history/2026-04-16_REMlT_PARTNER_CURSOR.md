---
title: Remit for Partner Cursor (context + role clarity)
date: 2026-04-16
version: 3
status: draft
---

## Purpose

This document gives Partner Cursor **goal clarity** and a shared language for **bringing outside material into this workspace** without violating `00_authority/PRINCIPLES.md`.

It includes a short excerpt of the most impactful lines from a prior dialogue export, explicitly marked as **non-authoritative context**.

## The goal (plain)

Make it safe and fast for agents to build **clarity** (large and small) by importing outside material with **provenance**, **sanitisation**, and **principles conformance** — while keeping archives immutable and canonical extractions small.

Operational details live in `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`.

## Equal-standing partner roles (separation, not hierarchy)

- **Partner A (Logic & Authority)**: tightens `00_authority/` (intent, principles, decision log) and decides what becomes authoritative in `MANIFEST.md`.
- **Partner B (Transfer & Sanitisation)**: transfers peripheral context safely into `90_archive/`, extracts usable truth into `01_truth/`, and keeps `MANIFEST.md` updated.

Both partners have **equal standing**. The separation exists to reduce context dilution and keep the system reversible.

## The one authority rule

Only treat files listed under **Authoritative now** in `00_authority/MANIFEST.md` as truth.

Everything else is:

- `[NON-AUTHORITATIVE]` context
- or `[LOGIC TO BE CONFIRMED]` hypotheses

## Narrative handling

Narrative is allowed (it often preserves **human operator intent** in messy form), but it must be:

- marked `[NARRATIVE]`
- kept separate from “truth” artefacts in `01_truth/`
- checked for congruence with `PROJECT_INTENT.md` + `PRINCIPLES.md` (flag contradictions as `[DECISION REQUIRED]`)

## Human operator context (optional, ego-aware, minimal)

If the team needs “who/why” clarity to interpret imports, capture a **small** capsule:

- **Archive-first** (raw stays in `90_archive/`; do not “prettify” history)
- **Minimum viable**: only what changes decisions/constraints
- **Ego-aware**: record biases/preferences as hypotheses, not as moral claims; mark `[LOGIC TO BE CONFIRMED]` when needed
- **Learning-forward**: note repeatable failure modes with sources (still non-authoritative unless promoted)

## Most impactful origin lines (non-authoritative context)

**Source (archived export):** `Amplified Partners/90_ARCHIVE/exports/2026-04-15_operational-architecture-dialogue-export.rtf`

These quotes are included to preserve intent and terminology. They are **not accepted fact** and must not be treated as authority unless promoted into `MANIFEST.md`.

- “[NON-AUTHORITATIVE] …the goal here is to strip everything down to a process… try and make every process deterministic as possible… in a chunk size sense make it 90%, 10%.”
- “[NON-AUTHORITATIVE] We are defining through mathematics the radius of the entrance of the next part in the chain… denoising the data.”
- “[NON-AUTHORITATIVE] …allowed to throw a curveball… but we can't allow it into our production system.”
- “[NON-AUTHORITATIVE] Context is a finite resource… treat it like a Clean Room… increase the Signal-to-Noise Ratio.”
- “[NON-AUTHORITATIVE] …create a Pure Manifest… This isn't just a folder; it's a Contextual Fortress.”
- “[NON-AUTHORITATIVE] …if a logic chain isn't finished, write: [LOGIC INCOMPLETE: FOUNDER INPUT REQUIRED]… stop and ask… rather than guessing.”
- “[NON-AUTHORITATIVE] …If there's a level of certainty… below 85%, it must consult me.”
- “[NON-AUTHORITATIVE] If the software is available, we build it. We vet and test. We only use reputable sources. We stand on the shoulders of giants. We research. We plan. Then we move to fill in the final 20%.”

## Your immediate job (Partner Cursor)

1. Read (in order): `PRINCIPLES.md`, `README.md`, `PROJECT_INTENT.md`, `MANIFEST.md`, `PARTNER_TRANSFER_INSTRUCTIONS.md`, then this remit.
2. Transfer only **sanitised** material into `90_archive/` with the required header.
3. For anything stable enough to become truth, create a short normalised extraction in `01_truth/` and add it to `MANIFEST.md` as **Candidate authority**.
4. When you encounter uncertainty or conflicts, do **not** resolve by invention:
   - mark `[LOGIC TO BE CONFIRMED]`, `[SOURCE REQUIRED]`, or `[DECISION REQUIRED]`
   - include the source paths

## Changelog

### v3 — 2026-04-16

- Realigned remit to `PRINCIPLES.md` + archive-first ingestion; removed glossary dependency; added minimal ego-aware operator-context guidance.

Signed-by: Keystone (AI) — 2026-04-16

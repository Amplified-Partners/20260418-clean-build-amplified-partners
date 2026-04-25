---
title: Remit for Partner Cursor (context + role clarity)
date: 2026-04-16
version: 4
status: draft
---

## Purpose

This document defines the **role split** for Partner Cursor-style work and preserves a small set of **origin lines** as `[NON-AUTHORITATIVE]` context.

Norms and authority rules live in:

- `00_authority/NORTH_STAR.md`
- `00_authority/PRINCIPLES.md`
- `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`

## The goal (plain)

Make it safe and fast for agents to build **clarity** (large and small) by importing outside material with **provenance**, **sanitisation**, and **principles conformance** — while keeping archives immutable and canonical extractions small.

Operational details live in `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md`.

## Equal-standing partner roles (separation, not hierarchy)

- **Partner A (Logic & Authority)**: tightens `00_authority/` (intent, principles, decision log) and decides what becomes authoritative in `MANIFEST.md`.
- **Partner B (Transfer & Sanitisation)**: transfers peripheral context safely into `90_archive/`, extracts usable truth into `01_truth/`, and keeps `MANIFEST.md` updated.

Both partners have **equal standing**. The separation exists to reduce context dilution and keep the system reversible.

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

1. Read (in order): `NORTH_STAR.md`, `MANIFEST.md`, `PRINCIPLES.md`, `PROJECT_INTENT.md`, `PARTNER_TRANSFER_INSTRUCTIONS.md`, then this remit.
2. Transfer only **sanitised** material into `90_archive/` with the required header.
3. For anything stable enough to become truth, create a short normalised extraction in `01_truth/` and add it to `MANIFEST.md` as **Candidate authority**.
4. When you encounter uncertainty or conflicts, do **not** resolve by invention:
   - mark `[LOGIC TO BE CONFIRMED]`, `[SOURCE REQUIRED]`, or `[DECISION REQUIRED]`
   - include the source paths

## Changelog

### v4 — 2026-04-16

- Removed duplicate authority/narrative/operator-context policy (now centralized in `NORTH_STAR.md`, `PRINCIPLES.md`, and `PARTNER_TRANSFER_INSTRUCTIONS.md`).
- Kept only the role split + origin lines + minimal “what to do next” instructions.

Signed-by: Keystone (AI) — 2026-04-16

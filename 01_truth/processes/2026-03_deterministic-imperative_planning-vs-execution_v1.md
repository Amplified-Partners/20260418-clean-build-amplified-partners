---
title: Deterministic imperative — planning vs execution (truth candidate)
date: 2026-04-16
version: 1
status: draft
---

Status: `[LOGIC TO BE CONFIRMED]`
Source: `90_archive/2026-03_amplified-consolidated-architecture_full.txt`

## Claim

For reliability: planning/exploration may be probabilistic; execution paths should be deterministic (repeatable, inspectable, reversible).

## Operational rule (this repo)

- If it changes how the system runs, represent it as an artifact in `01_truth/` (schema/process/interface) and index it in `00_authority/MANIFEST.md`.
- Prefer mechanical automation for mechanical work (scripts/workflows) when asked to build.
- Agents are used for: classification, synthesis, drafting, QA/critique, and gap surfacing — not as “silent execution truth.”

## Failure modes

- Treating exploratory text as execution policy without promotion.
- Making irreversible moves/migrations without reversible plan or sign-off gate.

## Open decisions `[DECISION REQUIRED]`

- What is the first deterministic workflow spine we want to standardize (tool-agnostic)?

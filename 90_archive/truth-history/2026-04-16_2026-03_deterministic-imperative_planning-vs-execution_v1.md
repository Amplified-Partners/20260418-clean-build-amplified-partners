---
title: Deterministic imperative — planning vs execution (truth candidate)
date: 2026-04-16
version: 1
status: draft
---

Status: [LOGIC TO BE CONFIRMED]
Source: `90_archive/2026-03_amplified-consolidated-architecture_full.txt`

## Claim (candidate)

For reliability:

- planning and exploration may be probabilistic
- execution paths should be deterministic (repeatable, inspectable, reversible)

## Implications for this clean room

- Decisions produce **artefacts** (schemas, process specs, interface contracts).
- Mechanical work is done by scripts/workflows where possible.
- Agents are used for: classification, synthesis, drafting, QA/critique loops, and surfacing gaps.

## What must be confirmed tonight

- Which deterministic workflow spine we are actually using in this project (tool-agnostic description first).
- What “execution must be deterministic” means for file moves, schema changes, and deployments in our current stack.

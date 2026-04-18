---
title: Candidate nuggets from Dept 5 (operations methodology)
date: 2026-04-16
version: 1
status: draft
source:
  path: /Users/ewansair/Amplified Partners/dept-5-operations-methodology.docx.md
  described_as: "Operations & Foundation — Methodology Reference (March 2026)"
sanitisation:
  - "Minimal extraction; do not promote implied artefacts into workspace truth."
---

## Status

`[LOGIC TO BE CONFIRMED]` — extracted “starter truth” nuggets only; **not** authoritative unless promoted via `00_authority/MANIFEST.md`.

## Nugget 1 — Research routing (pattern only)

### Claim

- Start research with a **metasearch-first** default (in the source: **SearXNG-first**) and only escalate to paid/external search when results are insufficient.
- Keep a **research index** so queries are recorded (the source names `RESEARCH-INDEX.md`) — but that artefact is not in this workspace yet.

### Minimal extraction

Default: start internal; escalate external only if insufficient; record queries/results.

### Notes

- Do not treat any named tools/files from the source as present here unless added.
- `[SOURCE REQUIRED]`: any concrete tool choice, index filename, or taxonomy details.

## Nugget 2 — Capability routing (pattern only)

### Claim

- Route tasks to tools/models by **task type + quality requirement + cost constraint**, rather than using one model for everything.
- Treat “tooling exposure” patterns explicitly: the source describes exposing internal systems as an **MCP server** and/or an **OpenAI-compatible proxy**.

### Minimal extraction

Default: explicit routing layer; explicit interface boundary; explicit quality gate.

### Notes

- `[SOURCE REQUIRED]`: any named products/systems/performance claims from the source.

## Nugget 3 — Metadata + identifiers (pattern only)

### Claim

- Enforce **machine-readable document metadata** (frontmatter) so artefacts can be retrieved, filtered, and audited without manual heroics.
- Use **stable identifiers** for processes (the source uses an atom ID scheme) to prevent name drift and ambiguity.

### Minimal extraction

Default: minimal frontmatter; stable IDs when scale demands.

### Notes

- In this repo, keep frontmatter minimal; do not import a large standard unless needed.
- `[SOURCE REQUIRED]`: any detailed frontmatter spec, ID scheme, or naming standard from the source.

Signed-by: Keystone (AI) — 2026-04-16

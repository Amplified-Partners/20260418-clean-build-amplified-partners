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

## Absolute

**The responsibility is Ewan’s and he accepts it happily.**

## Status

`[LOGIC TO BE CONFIRMED]` — extracted “starter truth” nuggets only; **not** authoritative unless promoted via `00_authority/MANIFEST.md`.

## Nugget 1 — Research routing SOP (what to do first)

### Nugget 1 — Candidate claim

- Start research with a **metasearch-first** default (in the source: **SearXNG-first**) and only escalate to paid/external search when results are insufficient.
- Keep a **research index** so queries are recorded (the source names `RESEARCH-INDEX.md`) — but that artefact is not in this workspace yet.

### Nugget 1 — Extract (paraphrased, faithful)

- The source states an “operational mandate” that research should begin with a local SearXNG instance before using external search APIs, for privacy, cost, and quality reasons.
- The source includes steps that (a) start with SearXNG, (b) stop if sufficient, (c) escalate to an external research API if insufficient, and (d) record queries in a research index.

### Nugget 1 — Workspace alignment notes

- This aligns with our principles-first stance: **minimise external leakage**, **be cost-aware**, and keep outputs **inspectable**.
- **Do not** treat `Beast SearXNG`, “Perplexity Sonar API”, `APDS`, “4‑Tier Source Taxonomy”, `RESEARCH-INDEX.md`, or “Baton Pass Rule 1” as resolvable things here.
  - Marked: `[SOURCE REQUIRED]` — referenced by the source document but not present in this repo.

## Nugget 2 — Capability routing (how to think about tools/models)

### Nugget 2 — Candidate claim

- Route tasks to tools/models by **task type + quality requirement + cost constraint**, rather than using one model for everything.
- Treat “tooling exposure” patterns explicitly: the source describes exposing internal systems as an **MCP server** and/or an **OpenAI-compatible proxy**.

### Nugget 2 — Extract (paraphrased, faithful)

- The source describes a “Model‑Task Assignment Framework” with a simple routing rule and the idea of a router layer (it names “LiteLLM”).
- The source describes a “PCO” system shipped as a single container and exposed as both an MCP server and an OpenAI‑compatible HTTP proxy, emphasizing a quality gate (“Dual Classifier with Veto”).

### Nugget 2 — Workspace alignment notes

- We can reuse the **pattern** (explicit routing + clear interface boundary) without importing the whole stack.
- Marked `[SOURCE REQUIRED]`: “LiteLLM”, “PCO”, “Dual Classifier with Veto”, “Mem0”, and any claimed performance figures or ecosystem mappings referenced only inside the source doc.

## Nugget 3 — Minimal naming / registry discipline (hygiene lane)

### Nugget 3 — Candidate claim

- Enforce **machine-readable document metadata** (frontmatter) so artefacts can be retrieved, filtered, and audited without manual heroics.
- Use **stable identifiers** for processes (the source uses an atom ID scheme) to prevent name drift and ambiguity.

### Nugget 3 — Extract (paraphrased, faithful)

- The source specifies a “Document YAML Frontmatter Standard” and lists many required fields intended to make documents machine-searchable and consistently tagged.
- The source describes an atom ID format `AMP-{APQC#}-{SEQ}-{VERSION}` for uniquely identifying/versioning process atoms.
- The source references a file naming standard (`FILE-NAMING-CONVENTION-v1`) but does not include its content.

### Nugget 3 — Workspace alignment notes

- We should adopt **only the minimum useful subset** for this clean-room (avoid vault-era bloat).
- Marked `[SOURCE REQUIRED]`: “SKILL‑16”, `FILE-NAMING-CONVENTION-v1`, and APQC mapping specifics (referenced, not provided here).

Signed-by: Keystone (AI) — 2026-04-16

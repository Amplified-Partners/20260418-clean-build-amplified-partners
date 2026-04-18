---
title: Model-aware format selection
date: 2026-04-16
version: 1
status: active
tags: [format, model-selection, agent-communication, marginal-gains]
source: multi-model empirical studies 2024-2025
review: update when new format/model research emerges
---

<!-- markdownlint-disable-file MD013 -->

## Purpose

When the model receiving a handoff, baton pass, or structured prompt is known, use the empirically optimal format for that model.

**Decision hierarchy for format selection:**
1. Comprehension gain — primary. If format A produces materially better agent outcomes than format B, use A.
2. Compound value — primary. A small gain applied to every run compounds significantly.
3. Maintenance overhead — secondary.
4. Token cost — a factor, not the constraint. If a more verbose format produces better outcomes, use it.

Token cost is not the veto. The goal is the only constraint.

The principle is stable (`00_authority/PRINCIPLES.md` → receiver-native format). The model-specific mappings here are updated as research evolves.

## Current best evidence

Source: comparative empirical studies across GPT-4o, Claude, Gemini (2024–2025). `[CURRENT BEST EVIDENCE]`

| Model family | Optimal format for structured fields | Rationale |
|---|---|---|
| GPT-4 / GPT-4o and equivalents | Markdown | Most token-efficient; large models resilient to format variation |
| GPT-3.5 and smaller GPT variants | JSON | Empirically favoured for accuracy at this scale |
| Gemini family | YAML | Best accuracy across nested data |
| Claude family | YAML | Best cross-model accuracy; XML underperforms and costs more tokens |
| Unknown / model-agnostic | YAML frontmatter + structured Markdown body | Best-compromise default |
| Qwen (hive mind / resolver tier) | YAML | Machine retrieval priority; YAML parses cleanly |

## Default format for this workspace

```
YAML frontmatter  →  machine retrieval (Qwen, search, status queries)
Structured Markdown body  →  agent comprehension (explicit labelled fields, not prose)
Prose  →  only where structure cannot carry the meaning
```

This default is the model-agnostic safe choice. When the model is known, apply the table above.

## What matters more than format

Research finding: explicit field labelling and defined-done criteria matter more than format syntax. A well-labelled Markdown block outperforms poorly-labelled YAML. Structure of meaning beats structure of syntax.

For handoff documents specifically:
- Label every field explicitly
- State the specific blocker in one sentence (not a paragraph)
- Include a defined-done condition — what would make this unblocked?
- Separate working context (what happened) from forward context (what is needed)

## Review trigger

Update this document when:
- New multi-model format comparison research is published
- A model in active use changes its behaviour significantly
- A format consistently underperforms in practice (empirical signal beats theoretical mapping)

Previous research `[NON-AUTHORITATIVE]`: file an updated version at `90_archive/` when superseded.

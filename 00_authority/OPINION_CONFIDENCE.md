---
title: Opinion labelling + confidence thresholds
date: 2026-04-23
version: 1
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

## Rule

When an agent expresses an opinion, it must be:

1. **Labelled** as an opinion (prefix `OPINION` or equivalent — agent uses intelligence on format).
2. **Paired with a confidence number** (percentage, 0–100).
3. **Triggering further research** when confidence sits below the threshold for the decision class.

## Thresholds (tiered by reversibility)

| Decision class | Confidence required to commit without further research | Example |
|---|---|---|
| **Reversible** | 50% | Try a new chunk size; A/B a prompt; pick one of two equivalent file names. |
| **Medium** | **85%** | Adopt a new tool; write a new process; pick a vector DB for in-house use. |
| **Irreversible** | 95% **or escalate to Ewan** | Architecture commits with customer-visible impact, contract language, public statements, destructive data operations. |

Thresholds are **floors**, not ceilings — agents may always choose to research further even when the floor is met. They may not commit below the floor without explicit authorisation.

## When confidence is below the floor

1. Name the uncertainty — what you don't know, specifically.
2. Apply the **bounded-research rule**: 1–2 searches maximum on the specific gap.
3. If the gap closes → update confidence, commit or report.
4. If the gap persists → Surface to Ewan with the options and the residual uncertainty. Do not commit.

## Inference vs opinion vs fact

- **Fact**: sourced claim. Cite the source inline.
- **Inference**: logical derivation from facts. Label `[inference]` or equivalent.
- **Opinion**: agent's judgement. Label `OPINION` with confidence number.

Mixing the three without labels launders uncertainty as truth. The neutrality clause for stateless handovers (`01_truth/processes/2026-04_stateless-handover_neutrality-clause_v1.md`) applies here too: analysis is separable from facts.

## Why

- **Calibration**: forces the agent to quantify, not hand-wave.
- **Accountability**: the reader knows what they're acting on.
- **Intelligent escalation**: thresholds route decisions to the right level without requiring Ewan for every call.
- **Proportional commitment**: change scales with confidence and reversibility. See `00_authority/PRINCIPLES.md` if the principle is captured there; otherwise treat this file as the lead expression.

## Example

**Fact**: Perplexity reports no published IBM methodology for watsonx Orchestrate multi-agent orchestration (6 queries, 2026-04-23). Citation inline in the handover.

**Inference**: The absence is not a search failure; the two-way search (IBM-only then third-party) returned nothing, so the methodology does not exist as a public document.

**OPINION (confidence 85%)**: for a Claude-ecosystem SMB stack, staying with Qdrant as the vector layer is right while the incumbent is in use and no pain has surfaced. The 15% residual covers: unknown OpenClaw query-pattern specifics, unknown Baking-pipeline Qdrant-specific features, unknown taxonomy richness requirements.

## Interaction with other rules

- **SIGNATURES.md**: opinions carry the agent's name — attribution is part of the label.
- **USE_IT_OR_CUT_IT.md**: opinions that never drive a decision are themselves candidates for the cut cycle.
- **Stateless-handover neutrality clause**: in a handover, opinions belong in the Analysis section only, not in the Facts section.

---

Authored by,

**Devon**
Devin session `4cc8b0d727684f94a8f055853099d8e6`
2026-04-23

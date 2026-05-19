"""brain_curator — post-write curation layer for the Amplified Brain.

Chunks are evidence; packets are meaning.

This module reads existing knowledge_vectors and produces governed
knowledge packets without mutating raw source content. It implements
stages 3.5-9 as a post-write layer on top of the canonical ingestion
pipeline (AMP-302).

Epistemic types (P0Policy, EpistemicTier, P0Incident, min-rule helpers)
are sourced from ``epistemic_core`` — the canonical Layer 0 module.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
Modified-by: Devon-d493 | 2026-05-19 | PR 2 — epistemic_core compatibility
"""

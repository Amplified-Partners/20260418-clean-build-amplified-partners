# Copilot Instructions — clean-build

This is the governed workspace for Amplified Partners AI agents. It follows Compound Engineering (Plan 40%, Work 10%, Review 30%, Compound 20%).

## Authority hierarchy
1. `00_authority/` — ground-truth rules, MANIFEST.md is the index
2. `01_truth/` — truth-shaped candidates (processes, schemas, interfaces)
3. `02_build/` — build artefacts
4. `03_shadow/` — experiments, wrap-ups, Kaizen probes (never authoritative by default)
5. `90_archive/` — reference and provenance (not current authority; do not treat as live policy)

## Key rules
- Every committed artefact must be signed (agent name + ISO date + session/instance ID if one exists)
- Opinions must be labelled with confidence (0–100%). See `00_authority/OPINION_CONFIDENCE.md`
- Authority file edits require a version bump in YAML frontmatter + changelog entry
- Decisions go in `00_authority/DECISION_LOG.md`
- Handovers must be stateless: facts, open-risks, tokens, optional analysis

## Naming
- Filing: `NN_tier/TYPE/YYYY-MM_kebab-slug_vN.md`
- Imperative voice, must/may only (no "should consider")
- One concept per file, cross-link rather than merge

---

Signed-by: Devon | 2026-05-01 | session 873af571838a40d29455d1579d2e7d75

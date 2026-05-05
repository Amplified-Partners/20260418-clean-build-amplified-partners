---
title: API data engineering Cursor rules — canonical tree, mirror parity, zip
type: refactor
status: active
date: 2026-04-26
origin: inferred from PR diff (00-api-data-engineering-always.mdc) and docs/2026-04-23-amplified-partners-delegate-brief.md
---

# API data engineering Cursor rules — canonical tree, mirror parity, zip

## Overview

Keep **one** authoritative rules story for API data engineering work: the live Cursor rules under `.cursor/rules/api-data-engineering/` stay **identical** to the distributable mirror under `docs/revisions/_extracted_rules/cursor-rules-api-data-eng/`, optional **zip** stays current when you still ship that way, and cross-references (evidence pack, UK scope §F) stay valid. This plan does **not** invent new product behavior; it governs documentation and packaging discipline already implied by the delegate brief and onboarding doc.

---

## Problem Frame

Two on-disk copies of the same rules pack invite silent drift. The orchestration plan’s acceptance test already calls for a **silent** `diff` on `00-api-data-engineering-always.mdc` between trees; widening parity to the **whole** `api-data-engineering/` folder reduces surprise. The attached PR shows the kind of substantive edit (frontmatter, editorial bar, reference stack wording, evidence-pack path) that must land **once** and be **mirrored**, not half-applied.

---

## Requirements Trace

- R1. **Single story** — Any change to API data engineering rules appears in both `.cursor/…` and `_extracted_rules/…` (or documented exception list is empty).
- R2. **Zip hygiene** — If `docs/revisions/cursor-rules-api-data-eng.zip` remains in use, it is regenerated after meaningful rule edits and `docs/revisions/README.md` instructions stay accurate.
- R3. **Traceable references** — Links and filenames for the evidence pack (`docs/revisions/api-data-engineering-research.md`) and optional hardware scope (`docs/revisions/uk-accounting-apis-alpha-scope.md`) resolve from this repo.
- R4. **Delegate alignment** — Commands in `docs/2026-04-23-amplified-partners-delegate-brief.md` remain the verification path of record (or are updated in the same change set if paths change).

---

## Scope Boundaries

- **In scope:** Markdown rules (`.mdc`), pack `README.md`, zip regeneration, cross-doc references, one-line workflow note for “which tree is edited first.”
- **Out of scope:** Changing Hazel scripts, SSD backup units, or GitHub org bootstrap (see `docs/plans/2026-04-23-orchestration-milestone-ssd-backup-hazel-codex.md`).
- **Deferred to follow-up work:** Adding automated CI that fails on `diff` drift (optional; not required for this refactor plan).

---

## Context & Research

### Relevant code and patterns

- Authoritative Cursor path: `.cursor/rules/api-data-engineering/*.mdc` (15 files including `00-api-data-engineering-always.mdc`).
- Mirror path: `docs/revisions/_extracted_rules/cursor-rules-api-data-eng/.cursor/rules/api-data-engineering/*.mdc`.
- Onboarding: `docs/2026-04-23-amplified-partners-rules-onboarding-and-ship.md` describes mirror + zip intent.
- Zip: `docs/revisions/cursor-rules-api-data-eng.zip`; regeneration commands differ slightly between `docs/revisions/README.md` and the delegate brief — this plan resolves that ambiguity in **U4**.

### Institutional learnings

- `docs/solutions/` not present in this repo; no additional learnings file.

### External references

- None required for governance refactor; stack rows in `00-*` already point maintainers at vendor docs.

---

## Key Technical Decisions

- **Decision — Edit source:** Treat **`.cursor/rules/api-data-engineering/`** as canonical for day-to-day edits in this repo; **copy or sync into** `_extracted_rules/…` before merge (alternative: edit mirror first — pick one and record it in **U1**; do not leave both implied).
- **Decision — Editorial depth:** The open PR proposes a longer “radical honesty / transparency / …” block; the workspace currently uses a shorter “Editorial (keep it short)” section. **Resolve during U3** so both trees match the chosen tier; do not ship mixed voice between `00` and pack `README.md`.
- **Decision — `alwaysApply`:** Keep `alwaysApply: true` on `00-*` only if that matches how Cursor should load master rules in this workspace; if toggled, document why in **Open questions → resolved** during implementation.

---

## Open Questions

### Resolved during planning

- **Which zip command is canonical?** — Prefer the path spelled in `docs/revisions/README.md` after **U4** verifies which command produces the zip linked from that README; align delegate brief in the same unit if they differ.

### Deferred to implementation

- **CI gate for folder `diff`:** Optional follow-up once a test runner exists in repo.

---

## Implementation Units

- [ ] U1. **Document edit workflow (one paragraph)**

**Goal:** Remove ambiguity about which directory is edited first and how the mirror stays honest.

**Requirements:** R4

**Dependencies:** None

**Files:**
- Modify: `docs/2026-04-23-amplified-partners-rules-onboarding-and-ship.md`
- Modify: `docs/revisions/_extracted_rules/cursor-rules-api-data-eng/README.md` (Maintenance or intro subsection only)

**Approach:** Add a single explicit bullet: canonical path → mirror → optional zip. Link to delegate `diff -q` command.

**Test scenarios:**
- Happy path: A new reader can answer “which folder do I edit?” in under one minute using only those two docs.

**Verification:** Prose is present, non-contradictory, and references the `diff -q` paths from the delegate brief.

---

- [ ] U2. **Full folder parity (all `.mdc` files)**

**Goal:** Eliminate drift across the entire `api-data-engineering` rule set, not only `00-*`.

**Requirements:** R1

**Dependencies:** U1

**Files:**
- Modify: every file under `.cursor/rules/api-data-engineering/` and/or `docs/revisions/_extracted_rules/cursor-rules-api-data-eng/.cursor/rules/api-data-engineering/` as needed to make trees match

**Approach:** Run recursive `diff` (or file-by-file `diff -q`) between the two directories; reconcile until silent. Prefer copying **from** the canonical side chosen in U1.

**Test scenarios:**
- Happy path: `diff -qr` the two `api-data-engineering/` directories reports no differences.
- Edge case: If a file exists only on one side, delete or add to match the canonical set of 15 files.

**Verification:** Silent directory diff; spot-check one auto rule still has sensible `globs` frontmatter.

---

- [ ] U3. **`00-api-data-engineering-always.mdc` — content and cross-refs**

**Goal:** Land agreed editorial depth, stack table nuance, `01_truth/schemas` caveat, and evidence-pack pointer **identically** in both copies.

**Requirements:** R1, R3

**Dependencies:** U2 (may be folded into U2 if parity is done file-by-file starting with `00`)

**Files:**
- Modify: `.cursor/rules/api-data-engineering/00-api-data-engineering-always.mdc`
- Modify: `docs/revisions/_extracted_rules/cursor-rules-api-data-eng/.cursor/rules/api-data-engineering/00-api-data-engineering-always.mdc`

**Approach:** Choose long vs short editorial block; align with pack `README.md` “Editorial bar” language. Confirm `docs/revisions/api-data-engineering-research.md` exists or adjust pointer to “project’s canonical copy” wording.

**Test scenarios:**
- Happy path: `diff -q` on the two `00-*` paths is silent after edits.
- Integration: Open one rule in Cursor (manual) and confirm no frontmatter parse errors.

**Verification:** Silent `diff -q` on `00`; evidence path opens from repo root.

---

- [ ] U4. **Zip + README command alignment**

**Goal:** Regenerate distributable zip when policy says so; one documented command.

**Requirements:** R2, R4

**Dependencies:** U2, U3

**Files:**
- Modify: `docs/revisions/README.md`
- Modify: `docs/2026-04-23-amplified-partners-delegate-brief.md` (commands table only, if needed)
- Create/overwrite: `docs/revisions/cursor-rules-api-data-eng.zip` (binary artifact)

**Approach:** Run the chosen zip command from repo root or `docs/revisions` as documented; note approximate size and date in PR description (human), not in plan file.

**Test scenarios:**
- Happy path: Fresh zip unpacks to a tree containing `.cursor/rules/api-data-engineering/00-api-data-engineering-always.mdc` at the expected path.
- Error path: If `zip` is missing in environment, document fallback (e.g. “run on Mac with zip installed”) under README — **defer** only if truly blocked.

**Verification:** README command, when followed literally from a clean shell cwd, produces the linked zip path.

---

## System-Wide Impact

- **Interaction graph:** Cursor loads `.cursor/rules/`; humans may unpack zip elsewhere — parity prevents divergent behavior.
- **Unchanged invariants:** Orchestration plan Units A–C, E; Hazel dummy-run scripts; unrelated `docs/` narratives.

---

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Silent partial merge (only `00` fixed) | U2 requires full-directory diff |
| Zip command cwd confusion | U4 pins one cwd + relative paths in README |
| Editorial disagreement (long vs short block) | Resolve in PR discussion before U3 merge |

---

## Documentation / Operational Notes

- After merge, optionally add one line to `docs/plans/2026-04-23-orchestration-milestone-ssd-backup-hazel-codex.md` test scenario 3 only if verification commands moved.

---

## Sources & References

- **Origin:** Inferred from PR diff on `docs/revisions/_extracted_rules/cursor-rules-api-data-eng/.cursor/rules/api-data-engineering/00-api-data-engineering-always.mdc` and checklist in `docs/2026-04-23-amplified-partners-delegate-brief.md`
- Related: `docs/revisions/_extracted_rules/cursor-rules-api-data-eng/README.md`
- Related plan: `docs/plans/2026-04-23-orchestration-milestone-ssd-backup-hazel-codex.md`

---
Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd

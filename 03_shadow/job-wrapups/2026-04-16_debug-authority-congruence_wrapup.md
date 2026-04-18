---
title: Wrap-up — Debug authority congruence (remit filename + AGENTS indexing)
date: 2026-04-16
status: finished
---

### Resume instruction

Open `00_authority/MANIFEST.md`.

### Current state (facts vs inference)

- **Facts**:
  - The stop-hook “loop” root cause was “by design”: the `stop` hook fires every stop event; the hook now emits a **short pointer** (not the full checklist), and the full checklist lives in the SOP + always-on rule.
  - `00_authority/REMlT_PARTNER_CURSOR.md` existed with a visually confusing filename (`REMlT`), and was referenced by `MANIFEST.md` + `PARTNER_TRANSFER_INSTRUCTIONS.md`.
  - Root `AGENTS.md` existed and was referenced by authority docs (e.g. decision log), but was **not indexed** in `00_authority/MANIFEST.md`.
- **Inference**:
  - The `REMlT` filename is a likely source of “can’t find file / drift” failures, especially on stricter filesystems or when copying paths.
  - Not indexing root `AGENTS.md` creates an authority ambiguity because Cursor commonly surfaces it as the top-level partner instruction.

### Open risks + what would falsify the approach

- **Risk**: Other tools (outside this repo) hardcode `REMlT_PARTNER_CURSOR.md`.
  - **Falsify**: any runtime/tooling error referencing that exact filename. (Mitigation: kept old file as a redirect.)
- **Risk**: Adding `AGENTS.md` to the manifest increases the authoritative set.
  - **Falsify**: if the intended rule is “authority pack only under `00_authority/`”. (If so, move root `AGENTS.md` into `00_authority/` and make root a redirect instead.)

### Negative signals (repulsion)

- **Dead ends**:
  - Looked for runnable “code” under `02_build/` — it currently only contains `README.md`.
- **Anti-patterns**:
  - Letting files inside `00_authority/` exist without being indexed in `MANIFEST.md` (creates silent “non-authoritative” pockets).
- **Repulsion score (1–10)**: 3 — small but real “paper-cut” ambiguity; high likelihood of repetition.
- **Repulsion bands**: 1–3 noise; repetition makes it signal; 4–5 self-refine; 6–7 pause + quick evidence search; 8–10 redesign/remit territory
- **Cut / absolute stop?** no

### Artifacts touched (paths; no secrets)

- `00_authority/MANIFEST.md` (indexed `AGENTS.md`, `00_authority/AGENTS.md`, and normalized remit filename; bumped manifest version to 24 with changelog entry)
- `00_authority/PARTNER_TRANSFER_INSTRUCTIONS.md` (updated remit link)
- `00_authority/REMIT_PARTNER_CURSOR.md` (new canonical filename, same content)
- `00_authority/REMlT_PARTNER_CURSOR.md` (converted into a redirect stub)

### Tokens

- N/A — no new `[LOGIC TO BE CONFIRMED]` / `[SOURCE REQUIRED]` / `[DECISION REQUIRED]` introduced by these edits.

### Smallest next step (owner + bounded action + timebox, or escalation target)

- **Owner**: Partner A (Logic & Authority)
- **Next step**: decide whether root-level `AGENTS.md` should remain authoritative (indexed) or be relocated into `00_authority/` with root becoming a redirect.
- **Due time**: 15 minutes (single decision + one mechanical follow-up edit).

### Leverage score (0–9)

- **Score (0–9)**: 6
- **Reason (one line)**: Removed a likely recurring path/authority ambiguity and made enforcement inputs easier to follow without changing policy content.
- **One improvement to bake in**: add a lightweight “manifest drift check” process (e.g., grep for unindexed `00_authority/*` docs) as a periodic hygiene step.
- **What would move this one point up**: one deterministic check/process doc in `01_truth/processes/` for “authority pack drift detection” and indexing it as candidate authority.


---
status: active
created: 2026-04-23
author: Rowan
---

# Orchestration milestone — SSD, backup rhythm, Hazel, doc spine

## Problem frame

Unify **physical readiness** (external SSD, scheduled backup / “vault” product TBD), **desktop automation** (Hazel quarantine-first, parameters pre-set), and **one documentation spine** (the linked `docs/` story matches how the disk is actually laid out) without thrash, silent deletes, or “overnight takeover” energy for humans.

## Scope boundary

**In scope:** sequencing, checklists, doc pointers, delegate mechanical tasks, approval gates.  
**Out of scope:** purchasing hardware for Ewan, clicking Hazel FDA, choosing final backup vendor name (TBD in org docs).

## Requirements traceability

| Requirement | Source doc |
|-------------|------------|
| One canonical tree + inbox/sandbox/research | `docs/2026-04-23-amplified-partners-organization-proposal.md` |
| North star + collaborator tone | `docs/2026-04-23-amplified-partners-goal-and-iso-verification.md` |
| Parallel `EXCLUSIVE_ROOT` + log | `docs/2026-04-23-amplified-partners-parallel-agents-playbook.md` |
| Cross-Mac automation law | `docs/2026-04-23-amplified-partners-cross-mac-automation-guardrails.md` |
| Hazel params + approval line | `docs/2026-04-23-hazel-parameters-ewan-approval-sheet.md` |
| Mechanical delegate | `docs/2026-04-23-amplified-partners-delegate-brief.md` |
| Canonical GitHub org for build repos | This plan — Unit E; cross-ref org proposal when URL exists |

## Decisions (plan-time)

1. **One rulebook for every agent:** Cursor, Codex, and any other assistant **play by the same rules** (this plan + the linked docs). **No tool is the default owner** of the spine; use whichever session fits the next concrete step. **Spine** = the org / goal / playbook docs in `docs/` read as **one** aligned story. **How work happens:** Ewan may merge by hand with agent assist when he wants control; agents may **act when the path is clear** and **stop as soon as confidence drops**, then ask. **Pace and load:** the bar is **effective** work — **not** breakneck agent throughput (that invites errors and outruns the doc spine). **Bounded authority:** agents stay inside written rules and explicit permission; expand scope only when the goal requires it and confidence stays high. Agents are load-bearing **partners**, not a race.
2. **Backup before aggressive Hazel rules:** promotion from quarantine only after at least one successful restore test (stated in Hazel dummy-run pack).
3. **Git ship:** this folder is **not** yet a git repository — first “ship” sub-step is `git init` + remote + first commit when Ewan chooses; until then, zip + delegate report are the audit trail.
4. **Dedicated GitHub organisation (future-facing):** create a **new GitHub org** as the canonical home for repos that intentionally build toward **Amplified Partners** — separate from personal or legacy orgs for cleaner **billing, permissions, and mental boundary** (contractors, branch protection, one URL pattern). **Does not replace** local Hazel discipline or `~/AmplifiedPartners` layout; it is the **remote** source-of-truth layer. **Naming:** align org display name + slug with the chosen brand string (“Amplified” vs “Amplify”) and doc titles before creating, to avoid drift across URLs, disk, and narrative docs.

## Implementation units (sequenced)

### Unit A — Hardware and backup (human-led)

- Acquire SSD; decide single volume role (backup parent + optional quarantine parent per Hazel pack).
- Install/configure backup tool; run **one** restore drill; date-stamp evidence (screenshot or log path) in `docs/` if desired.

### Unit B — Hazel (Ewan + machine)

- Create quarantine folders per `docs/2026-04-23-hazel-parameters-ewan-approval-sheet.md`.
- Enable **one** rule; run `bash scripts/hazel-dummy-run-mac-air-1.sh`; compare before/after reports.

### Unit C — Spine pass (docs and disk in unison)

- Reconcile `docs/2026-04-23-amplified-partners-organization-proposal.md` with live `~/AmplifiedPartners` layout (flat repos vs proposed `repos/` subtree). Add **one short decision paragraph** (in the proposal or goal doc) so future readers are not guessing.

### Unit D — Repo hygiene (delegate or agent)

- Execute `docs/2026-04-23-amplified-partners-delegate-brief.md` checklist; attach one-screen report.

### Unit E — GitHub org bootstrap (human-led, when ready)

- Pick **display name + slug** (consistent with org proposal / goal doc wording).
- Create org; set baseline security (2FA for members, branch protection template on default branch when first repo exists).
- Add **first** remote for this research tree (or a named empty template repo) and document the canonical org URL in `docs/2026-04-23-amplified-partners-organization-proposal.md` or goal doc — **one line** so “two homes” confusion does not creep in.

## Test scenarios (acceptance)

1. After Unit B: no file in Trash from Hazel without explicit human rule; quarantine contains only expected patterns.
2. After Unit A: restore drill completes for a chosen test file.
3. After Unit D: `diff` on `00-api-data-engineering-always.mdc` silent between `.cursor` and `_extracted_rules` copies; zip date current if zip is used.

## Dependencies

- Unit B depends on A only if quarantine target lives on new volume (optional).
- Unit C can proceed in parallel with A/B whenever someone (Ewan or an agent session) is ready to do the reconcile pass.
- Unit E is independent of A/B but should follow **one** naming decision (Decision 4) so org URL and local tree language stay aligned; first `git remote` for this folder can land after Ewan picks org + repo name.

## Risks

- **TCC / FDA:** only Ewan approves Hazel Full Disk Access.
- **Non-git folder:** risk of losing history until Unit D includes `git init` — call out explicitly to Ewan.

## Retest date

Revisit assumptions **2026-05-23** or after SSD + first backup week completes.

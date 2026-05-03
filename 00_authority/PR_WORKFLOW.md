---
title: PR workflow — branch protection, Linear linkage, review authority
date: 2026-05-03
version: 1
status: authoritative
---

<!-- markdownlint-disable-file MD013 -->

## Rule

All changes to `main` in active Amplified-Partners repos go through a pull
request that:

1. Originates from a branch matching an allowed prefix pattern.
2. References a Linear ticket (`AMP-XXX`) in the title or body.
3. Receives at least one review approval from a CODEOWNER (the Arbiter).
4. Passes the `pr-validation` status checks.

Direct pushes to `main` are blocked by GitHub branch protection. Force-pushes
and deletions of `main` are blocked.

## Scope

Applies to the active Amplified-Partners repos covered by AMP-70:

- `Amplified-Partners/clean-build`
- `Amplified-Partners/ground-truth`
- `Amplified-Partners/crm`
- `Amplified-Partners/beast-code-export`

Other active repos may opt in by running `02_build/scripts/apply_branch_protection.py`
with their slug.

## Roles

- **Author** — any agent (Devon, Cove worker, Clawd, Cassian, Antigravity,
  OpenClaw, dependabot) or human (Ewan).
- **Reviewer** — a second agent or human, distinct from the author.
- **Arbiter** — Antigravity, holding merge authority. Until Antigravity has a
  GitHub identity, the human Architect (`@ewan-dot`) holds the role
  operationally. CODEOWNERS files in each repo carry a `[SOURCE REQUIRED]`
  marker for the Antigravity GitHub user; remove and update once provisioned.

## Branch naming

Pattern: `<prefix>/<short-desc>` where `<prefix>` is one of:

| Prefix | Owner |
|---|---|
| `cove/` | Cove workers (canonical for AMP-XXX flow per AMP-70 § 4) |
| `devin/`, `devon/` | Devin / Devon sessions |
| `clawd/` | Claude / Clawd |
| `cassian/` | Cassian |
| `antigravity/` | Antigravity |
| `openclaw/` | OpenClaw |
| `dependabot/` | Dependabot (automated) |
| `release/` | Release branches |
| `feature/`, `fix/`, `chore/`, `hotfix/`, `docs/`, `refactor/`, `test/`, `ci/` | Conventional types |

For Cove and Devin/Devon agent branches, the short description should embed the
ticket id: `cove/AMP-123-fix-thing`, `devin/amp-70-pr-workflow`. The Linear
ticket check in `pr-validation.yml` reads from PR title/body, not the branch
name, so this is convention rather than a hard gate.

## Linear linkage

Every PR title or body must contain a regex match for `AMP-\d+` (case
insensitive). The first match found is taken as the PR's Linear ticket.

The `linear-sync` workflow then:

- On `opened`, `reopened`, `ready_for_review`: posts the PR link as a comment
  on the ticket, and moves the ticket to **In Review** if not already in a
  completed/canceled state.
- On `closed` + merged: posts a merge note. Ticket status is left for the
  Arbiter (human) to advance to **Done** — no auto-close, per the principle
  that completion is human-verified, not workflow-implied.
- On `closed` + not merged: posts a closure note.

Requires the org or repo secret `LINEAR_API_KEY`. The workflow no-ops with a
warning if the secret is missing.

## Branch protection settings

Applied by `02_build/scripts/apply_branch_protection.py`:

- Require pull request before merging — yes.
- Required approving reviews — 1.
- Dismiss stale reviews on push — yes.
- Require review from CODEOWNERS — yes.
- Require status checks to pass — yes; required: `Linear ticket reference`,
  `Branch name convention`.
- Require branches up-to-date before merging — yes.
- Require conversation resolution — yes.
- Restrict force-pushes — yes (no force-pushes on `main`).
- Restrict deletions — yes (cannot delete `main`).
- Enforce on administrators — **no** (admins keep break-glass via direct push,
  used only for protection-rule maintenance and incident recovery).

The script is idempotent. Re-running it on a protected branch updates the
configuration to the current spec.

## Why these specific rules

- **Linear linkage in title or body, not branch name** — branches are agent
  scratch space; titles and bodies are the contract with reviewers and the
  ticket system.
- **CODEOWNERS as the merge gate, not a separate "Antigravity" team** — until
  Antigravity has a GitHub identity, the human Architect holds the role
  operationally. The CODEOWNERS file is the single point to update once
  Antigravity is provisioned.
- **No auto-close on merge** — the playbook rule is "human verifies
  completion". Auto-Done would erase the verification step and turn merge into
  a self-fulfilling acceptance test.
- **Admins not enforced** — protection rules themselves need to be edited;
  emergency hotfixes need to be possible. The audit trail (commit history,
  Linear sync) catches misuse.

## Provenance

- Source: AMP-70 ("Setup: GitHub branch protection + PR workflow for all
  agents"), authored by Clawd, 2026-05-03.
- Implementation: Devon-4330 (session `devin-4330c661a80b4770aa8f62980c21366a`),
  2026-05-03.

Signed-by: Devon-4330 | 2026-05-03 | session devin-4330c661a80b4770aa8f62980c21366a

---
title: PR workflow & branch protection — operating SOP
date: 2026-05-03
version: 1
status: candidate-authority
---

<!-- markdownlint-disable-file MD013 -->

## Inputs

- A change to land on `main` of an active Amplified-Partners repo (per
  `00_authority/PR_WORKFLOW.md` § Scope).
- A Linear ticket id, `AMP-XXX`. Create one in `Amplifiedpartners` team if the
  change is non-trivial and no ticket exists.

## Procedure (for agents authoring a PR)

1. **Branch.** From the latest `main`, check out
   `<prefix>/<ticket-id-or-desc>`. Use `cove/AMP-XXX-…` for Cove workers,
   `devin/amp-XXX-…` for Devin/Devon sessions, etc. See
   `00_authority/PR_WORKFLOW.md` § Branch naming for the full list.
2. **Commit.** Sign every committed artefact per
   `00_authority/SIGNATURES.md`. Reference the ticket in commit messages.
3. **Push** the branch to `origin`.
4. **Open the PR** against `main`. The PR title or body must contain
   `AMP-XXX`. Fill in `.github/pull_request_template.md` (the Linear ticket
   section is required).
5. **Wait for `pr-validation` checks** to pass. If they fail:
   - "Linear ticket reference" — add `AMP-XXX` to the title or body.
   - "Branch name convention" — rename the branch (`git branch -m`, push the
     new name, retarget the PR).
6. **Wait for the Arbiter review.** A second agent / CODEOWNER reviews and
   approves. Until Antigravity has a GitHub identity, the human Architect
   (`@ewan-dot`) holds this role.
7. **Merge** is performed by the Arbiter, not the author.

## Procedure (for repo operators applying the policy to a new repo)

1. Add the repo slug to `02_build/scripts/apply_branch_protection.py` →
   `REPOS` constant.
2. Copy these files into the new repo:
   - `.github/CODEOWNERS`
   - `.github/workflows/pr-validation.yml`
   - `.github/workflows/linear-sync.yml`
   - `.github/pull_request_template.md`
3. Ensure the `LINEAR_API_KEY` secret is available at the repo or organisation
   level. If not, add it at
   `https://github.com/<org>/<repo>/settings/secrets/actions`.
4. Run the script with the Architect's PAT
   (`GH_TOKEN=$devi_org_github python 02_build/scripts/apply_branch_protection.py`).
   The script is idempotent.
5. Verify by inspecting the GitHub UI:
   `https://github.com/<org>/<repo>/settings/branches`.
6. Add a changelog entry to `00_authority/MANIFEST.md` recording the rollout.

## Outputs

- `main` is protected on the target repo.
- All future PRs trip `pr-validation` and `linear-sync`.
- Linear tickets receive automatic comments as their PRs progress.

## Acceptance criteria

- `gh api repos/<org>/<repo>/branches/main/protection` returns the configured
  protection JSON (no 404).
- Opening a no-ticket PR on the protected repo fails the `pr-validation` check
  and is blocked from merging.
- Opening a PR with an `AMP-XXX` reference posts a comment on that ticket
  within 30 seconds.

## Failure modes

- **`LINEAR_API_KEY` missing** — `linear-sync` no-ops with a warning. PRs are
  unaffected; Linear tickets simply do not get updated. Operator action: add
  the secret.
- **Linear ticket id typo** — `linear-sync` warns "could not resolve" and
  exits 0. The workflow triggers are `[opened, reopened, ready_for_review,
  closed]`; an `edited` event is intentionally not a trigger to avoid
  duplicate ticket comments on every body edit. Operator action: correct
  the ticket id in the PR title/body, then close-and-reopen the PR (or, if
  the PR is still in draft, mark it ready-for-review once corrected).
- **Devin (`devin-ai-integration[bot]`) cannot self-merge** — by design.
  Ewan / Antigravity merges. Operator action: none required.
- **Dependabot PR fails a required check** — `pr-validation.yml` does
  *not* skip dependabot at the job level (a skipped required check blocks
  merging). Instead each step checks `GITHUB_ACTOR` and exits 0 early
  when it is `dependabot[bot]`, so the check reports success and the PR
  remains mergeable. `linear-sync.yml` is not a required check, so it
  retains the simpler job-level `if: github.actor != 'dependabot[bot]'`
  skip. Operator action: none unless dependabot's actor name changes.

## Provenance

- Parent rule: `00_authority/PR_WORKFLOW.md`.
- Source ticket: AMP-70.
- Authored: Devon-4330 | 2026-05-03 | session devin-4330c661a80b4770aa8f62980c21366a.

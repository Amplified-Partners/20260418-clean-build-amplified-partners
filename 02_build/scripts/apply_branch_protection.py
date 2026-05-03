#!/usr/bin/env python3
"""Apply the AMP-70 branch protection policy to active Amplified-Partners repos.

Idempotent. Re-running on a protected branch updates the protection rules to
the current spec.

Usage:
    GH_TOKEN=<admin-pat> python 02_build/scripts/apply_branch_protection.py
    GH_TOKEN=<admin-pat> python 02_build/scripts/apply_branch_protection.py --dry-run
    GH_TOKEN=<admin-pat> python 02_build/scripts/apply_branch_protection.py --repo Amplified-Partners/clean-build

The PAT must have admin access to the repos. The Architect's PAT
(`devi_org_github`) is the canonical token; org admins / Antigravity may also
hold equivalent tokens.

Authored by Devon-4330 | 2026-05-03 | session devin-4330c661a80b4770aa8f62980c21366a.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

# Active repos covered by AMP-70. Add new slugs as repos are promoted to active.
REPOS: list[str] = [
    "Amplified-Partners/clean-build",
    "Amplified-Partners/ground-truth",
    "Amplified-Partners/crm",
    "Amplified-Partners/beast-code-export",
]

BRANCH = "main"

# Required status check contexts. These names match the `name:` fields of jobs
# in `.github/workflows/pr-validation.yml`.
REQUIRED_CHECKS = [
    "Linear ticket reference",
    "Branch name convention",
]

PROTECTION_PAYLOAD: dict = {
    "required_status_checks": {
        "strict": True,
        "contexts": REQUIRED_CHECKS,
    },
    "enforce_admins": False,
    "required_pull_request_reviews": {
        "dismiss_stale_reviews": True,
        "require_code_owner_reviews": True,
        "required_approving_review_count": 1,
        "require_last_push_approval": False,
    },
    "restrictions": None,
    "allow_force_pushes": False,
    "allow_deletions": False,
    "required_conversation_resolution": True,
    "lock_branch": False,
    "allow_fork_syncing": False,
    "block_creations": False,
    "required_linear_history": False,
}


def _request(method: str, url: str, token: str, payload: dict | None = None) -> tuple[int, str]:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode()


def apply_protection(repo: str, token: str, dry_run: bool) -> bool:
    """Apply the protection payload to `<repo>/branches/<BRANCH>`. Returns True on success."""
    url = f"https://api.github.com/repos/{repo}/branches/{BRANCH}/protection"
    if dry_run:
        print(f"[dry-run] PUT {url}")
        print(f"[dry-run] payload: {json.dumps(PROTECTION_PAYLOAD, indent=2)}")
        return True
    status, body = _request("PUT", url, token, PROTECTION_PAYLOAD)
    if status in (200, 201):
        print(f"[ok] {repo}: protection applied ({status}).")
        return True
    print(f"[fail] {repo}: HTTP {status}: {body}", file=sys.stderr)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--repo",
        action="append",
        help="Limit to this repo (full slug, e.g. Amplified-Partners/clean-build). Repeatable.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the API call without executing it.",
    )
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token and not args.dry_run:
        print(
            "error: GH_TOKEN (or GITHUB_TOKEN) env var is required and must be a PAT with admin access.",
            file=sys.stderr,
        )
        return 2

    repos = args.repo or REPOS
    failures = 0
    for repo in repos:
        ok = apply_protection(repo, token or "", args.dry_run)
        if not ok:
            failures += 1
    if failures:
        print(f"\n{failures}/{len(repos)} repos failed.", file=sys.stderr)
        return 1
    print(f"\nAll {len(repos)} repos updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

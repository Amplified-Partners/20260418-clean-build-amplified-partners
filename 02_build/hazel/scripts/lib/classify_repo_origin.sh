#!/usr/bin/env bash
# classify_repo_origin.sh — find which org repo a path belongs to.
#
# Walks up from a file path looking for `.git/config` and parses
# `remote.origin.url` to determine the source repo. Used by the staging step
# to route SIGNAL_KEEP files into `~/_consolidated/code/<repo>/...`.
#
# Output:
#   ORG/repo\t<relative-path-within-repo>     (single line)
#
# If no repo is found, exits 1 with no output.
#
# Usage:
#   classify_repo_origin.sh /path/to/file
#
# Signed: Devon-fad5 | 2026-05-05 | AMP-83
set -euo pipefail

[[ $# -ge 1 ]] || { echo "usage: $0 <path>" >&2; exit 2; }
P="$1"
[[ -e "$P" ]] || { echo "no such path: $P" >&2; exit 2; }

# walk up
DIR="$(cd "$(dirname "$P")" && pwd)"
while [[ "$DIR" != "/" && "$DIR" != "$HOME" ]]; do
  if [[ -f "$DIR/.git/config" ]]; then
    URL=$(awk -F'= ' '/^\s*url = /{print $2; exit}' "$DIR/.git/config" 2>/dev/null || true)
    if [[ -n "$URL" ]]; then
      # strip trailing .git, embedded creds (defensive — we should never see these)
      URL_CLEAN=$(echo "$URL" | sed -E 's#https?://[^@]+@#https://#; s#\.git$##; s#git@github\.com:#https://github.com/#')
      SLUG=$(echo "$URL_CLEAN" | sed -E 's#https?://github\.com/##')
      REL="${P#$DIR/}"
      printf "%s\t%s\n" "$SLUG" "$REL"
      exit 0
    fi
  fi
  DIR="$(dirname "$DIR")"
done

exit 1

# Signed: Devon-fad5 | 2026-05-05

#!/usr/bin/env bash
# 04_promote.sh — Phase 4: push consolidated subtrees to the right org repos.
#
# Reads ~/_consolidated/ and a routes table (`routes.json`). For each subtree
# matching a route, it:
#   1. Clones the destination repo (or fast-forwards an existing local clone).
#   2. Creates a side branch `devon/amp-83-import-<ts>`.
#   3. Copies (rsync --ignore-existing) the subtree into the repo at the route's
#      target path.
#   4. Commits with a signed message and pushes the branch.
#   5. Opens a PR via `gh` (if installed) so Ewan reviews before merge.
#
# Anything in `~/_consolidated/unmapped/` is NOT pushed — Ewan must decide
# which repo (or new repo) it belongs to.
#
# Usage:
#   04_promote.sh                    # defaults
#   04_promote.sh --in ~/_hazel_work --consolidated ~/_consolidated --dry-run
#
# Requires: git, gh, rsync.  Auth via gh CLI must be configured (`gh auth status`).
#
# Signed: Devon-fad5 | 2026-05-05 | AMP-83
set -euo pipefail

IN="${HOME}/_hazel_work"
CONS="${HOME}/_consolidated"
DRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --in)           IN="$2"; shift 2 ;;
    --consolidated) CONS="$2"; shift 2 ;;
    --dry-run)      DRY=1; shift ;;
    -h|--help) grep '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

ROUTES="$IN/routes.json"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$IN/log/04_promote-$TS.log"
WORK="$IN/promote-work"

mkdir -p "$IN/log" "$WORK"
[[ -d "$CONS" ]] || { echo "consolidated dir missing: $CONS" >&2; exit 2; }

# Default routes table if user hasn't supplied one
if [[ ! -f "$ROUTES" ]]; then
  cat >"$ROUTES" <<'JSON'
{
  "routes": [
    { "src_glob": "code/clean-build/**",         "repo": "Amplified-Partners/clean-build",          "target": "imported-from-mac/" },
    { "src_glob": "code/vault/**",               "repo": "Amplified-Partners/vault",                "target": "imported-from-mac/" },
    { "src_glob": "code/crm/**",                 "repo": "Amplified-Partners/crm",                  "target": "imported-from-mac/" },
    { "src_glob": "code/openclaw/**",            "repo": "Amplified-Partners/openclaw",             "target": "imported-from-mac/" },
    { "src_glob": "code/<*>/**",                 "repo": "Amplified-Partners/<MATCH>",              "target": "imported-from-mac/" },
    { "src_glob": "notes/**",                    "repo": "Amplified-Partners/vault",                "target": "imported-from-mac/notes/" },
    { "src_glob": "transcripts/**",              "repo": "Amplified-Partners/corpus-raw",           "target": "imported-from-mac/transcripts/" },
    { "src_glob": "research/**",                 "repo": "Amplified-Partners/perplexity-research",  "target": "imported-from-mac/" },
    { "src_glob": "screenshots-with-signal/**",  "repo": "Amplified-Partners/corpus-raw",           "target": "imported-from-mac/screenshots/" }
  ],
  "unmapped": "DO_NOT_PUSH"
}
JSON
  echo "wrote default routes -> $ROUTES" | tee -a "$LOG"
fi

command -v git    >/dev/null || { echo "git required" >&2; exit 2; }
command -v rsync  >/dev/null || { echo "rsync required (brew install rsync)" >&2; exit 2; }
GH=$(command -v gh || true)

PY=$(command -v python3 || true)
[[ -z "$PY" ]] && { echo "python3 required" >&2; exit 2; }

# Build (src_subtree, repo, target) tuples that exist on disk.
PLAN_TSV="$IN/promote-plan-$TS.tsv"
"$PY" - "$ROUTES" "$CONS" >"$PLAN_TSV" <<'PY'
import sys, os, json, fnmatch
routes = json.load(open(sys.argv[1]))
cons = sys.argv[2]
for r in routes["routes"]:
    g = r["src_glob"]
    if "<*>" in g:
        # wildcard repo name: enumerate top-level dirs under code/
        prefix = g.split("<*>",1)[0].rstrip("/")
        base = os.path.join(cons, prefix)
        if not os.path.isdir(base): continue
        for entry in sorted(os.listdir(base)):
            sub = os.path.join(base, entry)
            if not os.path.isdir(sub): continue
            repo = r["repo"].replace("<MATCH>", entry)
            target = r["target"]
            print(f"{sub}\t{repo}\t{target}")
    else:
        prefix = g.rstrip("/**").rstrip("*").rstrip("/")
        sub = os.path.join(cons, prefix)
        if not os.path.exists(sub): continue
        print(f"{sub}\t{r['repo']}\t{r['target']}")
PY

if [[ ! -s "$PLAN_TSV" ]]; then
  echo "no promotable subtrees found under $CONS" | tee -a "$LOG"
  exit 0
fi

echo "promote plan ($PLAN_TSV):" | tee -a "$LOG"
column -t -s $'\t' "$PLAN_TSV" | tee -a "$LOG"

if [[ $DRY -eq 1 ]]; then
  echo "[dry-run] not pushing anything." | tee -a "$LOG"
  exit 0
fi

BRANCH="devon/amp-83-import-$TS"

while IFS=$'\t' read -r src repo target; do
  [[ -z "$src" ]] && continue
  echo "------------------------------------------------------------------" | tee -a "$LOG"
  echo "promote: $src  ->  $repo:$target  (branch: $BRANCH)" | tee -a "$LOG"
  CLONE="$WORK/${repo//\//__}"
  if [[ ! -d "$CLONE/.git" ]]; then
    git clone "https://github.com/$repo.git" "$CLONE" 2>&1 | tee -a "$LOG"
  fi
  git -C "$CLONE" fetch origin 2>&1 | tee -a "$LOG"
  DEFAULT_BRANCH=$(git -C "$CLONE" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || echo main)
  git -C "$CLONE" checkout -B "$BRANCH" "origin/$DEFAULT_BRANCH" 2>&1 | tee -a "$LOG"
  mkdir -p "$CLONE/$target"
  rsync -a --ignore-existing "$src/" "$CLONE/$target/" 2>&1 | tee -a "$LOG"
  if [[ -z "$(git -C "$CLONE" status --porcelain)" ]]; then
    echo "no changes for $repo — skipping commit" | tee -a "$LOG"
    continue
  fi
  git -C "$CLONE" add -A
  git -C "$CLONE" commit -m "AMP-83: import from Mac consolidation ($TS)

Imported subtree: $(basename "$src")
Source: ~/_consolidated/$(basename "$src")
Run by: Devon-fad5 — 2026-05-05 — devin-fad59f8cffd245618655e5b692895bbc" 2>&1 | tee -a "$LOG"
  git -C "$CLONE" push -u origin "$BRANCH" 2>&1 | tee -a "$LOG"
  if [[ -n "$GH" ]]; then
    "$GH" -R "$repo" pr create --title "AMP-83: import from Mac consolidation ($TS)" \
      --body "Automated import from Mac → GitHub consolidation. See parent ticket AMP-83." \
      --head "$BRANCH" --base "$DEFAULT_BRANCH" 2>&1 | tee -a "$LOG" || true
  else
    echo "gh not installed — open PR manually: https://github.com/$repo/pull/new/$BRANCH" | tee -a "$LOG"
  fi
done <"$PLAN_TSV"

echo "[$(date -u +%FT%TZ)] promote done" | tee -a "$LOG"

# Signed: Devon-fad5 | 2026-05-05

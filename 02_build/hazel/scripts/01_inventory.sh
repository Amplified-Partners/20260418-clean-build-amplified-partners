#!/usr/bin/env bash
# 01_inventory.sh — Phase 1: walk the source tree and write a manifest.
#
# Read-only. No file is modified. Output is JSON Lines (`manifest.jsonl`),
# one line per file, with the columns needed by 02_classify.sh:
#   { path, size, mtime, sha256, mime, is_protected }
#
# Usage:
#   01_inventory.sh                    # defaults: --root $HOME --out ~/_hazel_work
#   01_inventory.sh --root ~/Documents --out /tmp/inv
#
# Signed: Devon-fad5 | 2026-05-05 | AMP-83
set -euo pipefail

ROOT="${HOME}"
OUT="${HOME}/_hazel_work"
POLICY=""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)   ROOT="$2"; shift 2 ;;
    --out)    OUT="$2"; shift 2 ;;
    --policy) POLICY="$2"; shift 2 ;;
    -h|--help)
      grep '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

: "${POLICY:=$SCRIPT_DIR/../policy.yaml}"

mkdir -p "$OUT" "$OUT/log"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$OUT/log/01_inventory-$TS.log"
MANIFEST="$OUT/manifest.jsonl"

[[ -d "$ROOT" ]] || { echo "ROOT not a directory: $ROOT" >&2; exit 2; }

PY=$(command -v python3 || true)
[[ -z "$PY" ]] && { echo "python3 required (ships with macOS Big Sur+)" >&2; exit 2; }

echo "[$(date -u +%FT%TZ)] inventory start  root=$ROOT  out=$OUT" | tee -a "$LOG"

# Self-contained python — walks the tree itself (no shell `find` pipe). This
# is more portable across macOS / Linux and avoids stdin / heredoc collisions.
"$PY" - "$POLICY" "$ROOT" "$LOG" "$MANIFEST" <<'PY'
import sys, os, json, hashlib, fnmatch, mimetypes, stat as st_mod

policy_path  = sys.argv[1]
root         = sys.argv[2]
log_path     = sys.argv[3]
manifest_out = sys.argv[4]

# --- minimal protected-globs loader (no PyYAML on stock macOS python3) ---
def load_protected(p):
    out = []
    in_block = False
    with open(p) as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.startswith("protected_globs:"):
                in_block = True; continue
            if in_block:
                if line.startswith("  - "):
                    g = line[4:].strip().strip('"').strip("'")
                    out.append(os.path.expandvars(g))
                elif line and not line.startswith(" "):
                    in_block = False
    return out

protected = load_protected(policy_path)

def matches_protected(path):
    for g in protected:
        gnorm = g.replace("/**", "*")
        if fnmatch.fnmatch(path, gnorm) or fnmatch.fnmatch(path, g):
            return True
    return False

def sha256(p, max_bytes=64*1024*1024):
    """Hash up to max_bytes; for huge files we hash a prefix to keep Phase 1 fast."""
    h = hashlib.sha256()
    n = 0
    try:
        with open(p, "rb") as f:
            while True:
                chunk = f.read(1024*1024)
                if not chunk: break
                h.update(chunk); n += len(chunk)
                if n >= max_bytes: break
        return h.hexdigest(), n
    except (OSError, PermissionError):
        return None, 0

# Directories to skip during the walk for speed (still recorded if encountered
# directly via the manifest? — no, prune them at walk time; classify will treat
# anything under them as bloat anyway).
PRUNE_BASENAMES = {".Trash", "node_modules", "__pycache__", ".venv",
                   "venv", ".pytest_cache", ".mypy_cache", "DerivedData",
                   ".gradle", ".tox", "dist", "build", ".next"}
# `.git/objects` is huge binary blobs — never useful to scan.
# `.git/config`, `.git/hooks`, `.git/HEAD`, `.git/refs/**` ARE scanned because
# AMP-80 (the original PAT exposure) is precisely in `.git/config`.
PRUNE_PATH_TAILS = ("/Library/Caches", "/.git/objects", "/.git/lfs")

n_total = 0
n_skipped = 0
log = open(log_path, "a")
out = open(manifest_out, "w")

for dirpath, dirnames, filenames in os.walk(root, followlinks=False, onerror=lambda e: log.write(f"walk-err\t{e}\n")):
    # prune
    dirnames[:] = [d for d in dirnames if d not in PRUNE_BASENAMES]
    if any(dirpath.endswith(t) for t in PRUNE_PATH_TAILS):
        dirnames[:] = []
        continue

    for fn in filenames:
        path = os.path.join(dirpath, fn)
        n_total += 1
        try:
            st = os.lstat(path)
        except OSError as e:
            log.write(f"stat-fail\t{path}\t{e}\n"); n_skipped += 1; continue

        if not st_mod.S_ISREG(st.st_mode):
            n_skipped += 1; continue

        prot = matches_protected(path)
        sha, hashed = (None, 0) if prot else sha256(path)
        mime, _ = mimetypes.guess_type(path)

        rec = {
            "path": path,
            "size": st.st_size,
            "mtime": int(st.st_mtime),
            "sha256": sha,
            "hashed_bytes": hashed,
            "mime": mime,
            "is_protected": prot,
        }
        out.write(json.dumps(rec, ensure_ascii=False))
        out.write("\n")

out.close()
log.write(f"summary\ttotal={n_total}\tskipped={n_skipped}\n")
log.close()
sys.stderr.write(f"inventory: total={n_total} skipped={n_skipped}\n")
PY

echo "[$(date -u +%FT%TZ)] inventory done   manifest=$MANIFEST" | tee -a "$LOG"
wc -l "$MANIFEST" | tee -a "$LOG"

# Signed: Devon-fad5 | 2026-05-05

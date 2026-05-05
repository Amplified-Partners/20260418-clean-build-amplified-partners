#!/usr/bin/env bash
# secret_scan.sh — standalone scanner for the consolidated dump.
#
# Walks a directory tree and reports any file containing token / key patterns.
# Use case: post-Hazel sanity check on ~/_consolidated/ before Phase 4.
#
# Output is TSV: <path>\t<pattern_id>\t<match_prefix>***
# Exit code: 0 if clean, 1 if any matches found.
#
# Usage:
#   secret_scan.sh                       # scans ~/_consolidated/
#   secret_scan.sh --root ~/some/dir
#   secret_scan.sh --root ~/_consolidated --max-bytes 5242880
#
# Signed: Devon-fad5 | 2026-05-05 | AMP-83 / AMP-80
set -euo pipefail

ROOT="${HOME}/_consolidated"
MAX_BYTES=10485760

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)      ROOT="$2"; shift 2 ;;
    --max-bytes) MAX_BYTES="$2"; shift 2 ;;
    -h|--help)   grep '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

[[ -d "$ROOT" ]] || { echo "root not a directory: $ROOT" >&2; exit 2; }

PY=$(command -v python3 || true)
[[ -z "$PY" ]] && { echo "python3 required" >&2; exit 2; }

"$PY" - "$ROOT" "$MAX_BYTES" <<'PY'
import sys, os, re
root, max_bytes = sys.argv[1], int(sys.argv[2])

PATTERNS = [
    ("github_pat_classic",      re.compile(rb"ghp_[A-Za-z0-9]{20,}")),
    ("github_oauth",            re.compile(rb"gho_[A-Za-z0-9]{20,}")),
    ("github_u2s",              re.compile(rb"ghu_[A-Za-z0-9]{20,}")),
    ("github_s2s",              re.compile(rb"ghs_[A-Za-z0-9]{20,}")),
    ("github_pat_finegrained",  re.compile(rb"github_pat_[A-Za-z0-9_]{50,}")),
    ("openai_anthropic",        re.compile(rb"sk-[A-Za-z0-9_-]{20,}")),
    ("aws_access_key",          re.compile(rb"AKIA[0-9A-Z]{16}")),
    ("pem_private",             re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("slack",                   re.compile(rb"xox[bpoa]-[A-Za-z0-9-]{10,}")),
    ("huggingface",             re.compile(rb"hf_[A-Za-z0-9]{30,}")),
]

n_hits = 0
n_files = 0
for dirpath, dirnames, filenames in os.walk(root):
    # don't descend into binary asset dumps
    dirnames[:] = [d for d in dirnames if d not in (".git","node_modules","__pycache__")]
    for fn in filenames:
        path = os.path.join(dirpath, fn)
        try:
            sz = os.path.getsize(path)
        except OSError:
            continue
        if sz <= 0 or sz > max_bytes:
            continue
        n_files += 1
        try:
            with open(path, "rb") as f:
                data = f.read(max_bytes)
        except (OSError, PermissionError):
            continue
        for sid, rx in PATTERNS:
            m = rx.search(data)
            if m:
                tok = m.group(0).decode("utf-8", errors="replace")
                print(f"{path}\t{sid}\t{tok[:6]}***")
                n_hits += 1

sys.stderr.write(f"secret_scan: scanned={n_files} hits={n_hits}\n")
sys.exit(1 if n_hits else 0)
PY

# Signed: Devon-fad5 | 2026-05-05

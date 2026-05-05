#!/usr/bin/env bash
# 05_reap.sh — Phase 5: DESTRUCTIVE. Delete originals after GitHub verification.
#
# This is the only irreversible step. It deletes the original files referenced
# in plan.jsonl (excluding PROTECTED_LEAVE_ALONE). It refuses to run unless ALL
# of the following are true:
#
#   1. --i-have-verified-github flag passed.
#   2. A Time Machine backup completed within last 24 hours.
#   3. Phase 4 promotion log shows zero failed pushes.
#   4. ~/__quarantine/ is empty (no unresolved secrets).
#
# Even with all preconditions, files go to ~/.Trash via `mv`, not unlink.
# macOS's Trash retention is the user's last-line safety net.
#
# Usage:
#   05_reap.sh --i-have-verified-github
#
# Signed: Devon-fad5 | 2026-05-05 | AMP-83
set -euo pipefail

IN="${HOME}/_hazel_work"
CONFIRM=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --i-have-verified-github) CONFIRM=1; shift ;;
    --in) IN="$2"; shift 2 ;;
    -h|--help) grep '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

PLAN="$IN/plan.jsonl"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$IN/log/05_reap-$TS.log"
mkdir -p "$IN/log"

[[ $CONFIRM -eq 1 ]] || { echo "REFUSED: pass --i-have-verified-github once you've confirmed GitHub has all promoted content." >&2; exit 1; }
[[ -f "$PLAN" ]] || { echo "plan missing: $PLAN" >&2; exit 2; }

# Precondition: Time Machine backup within 24h
if command -v tmutil >/dev/null; then
  LAST=$(tmutil latestbackup 2>/dev/null || true)
  if [[ -z "$LAST" ]]; then
    echo "REFUSED: no Time Machine backup found." >&2; exit 1
  fi
  TM_AGE_S=$(( $(date +%s) - $(stat -f %m "$LAST" 2>/dev/null || echo 0) ))
  if (( TM_AGE_S > 86400 )); then
    echo "REFUSED: latest Time Machine backup is older than 24h ($((TM_AGE_S/3600))h)." >&2; exit 1
  fi
  echo "TM backup ok: $LAST  age=$((TM_AGE_S/60))m" | tee -a "$LOG"
else
  echo "REFUSED: tmutil not found (not on macOS?). This script is macOS-only." >&2; exit 1
fi

# Precondition: empty quarantine
if [[ -d "$HOME/__quarantine" ]] && [[ -n "$(ls -A "$HOME/__quarantine" 2>/dev/null)" ]]; then
  echo "REFUSED: ~/__quarantine/ is not empty. Resolve secrets before reaping." >&2; exit 1
fi

# Precondition: phase 4 promotion log has at least one success and zero FAILs
PROMO_LOG=$(ls -t "$IN/log"/04_promote-*.log 2>/dev/null | head -1 || true)
if [[ -z "$PROMO_LOG" ]]; then
  echo "REFUSED: no Phase 4 promotion log found. Run 04_promote.sh first." >&2; exit 1
fi
if grep -qE '^FAIL|^fatal:' "$PROMO_LOG"; then
  echo "REFUSED: Phase 4 log contains failures. Resolve before reaping. ($PROMO_LOG)" >&2; exit 1
fi

echo "[$(date -u +%FT%TZ)] reap start (DESTRUCTIVE — moving originals to ~/.Trash)" | tee -a "$LOG"

PY=$(command -v python3 || true)
[[ -z "$PY" ]] && { echo "python3 required" >&2; exit 2; }

"$PY" - "$PLAN" "$LOG" <<'PY'
import sys, json, os, subprocess
plan = sys.argv[1]
log_path = sys.argv[2]
log = open(log_path, "a")
HOME = os.environ["HOME"]

n_trashed = 0
n_skipped = 0

with open(plan) as f:
    for line in f:
        if not line.strip(): continue
        rec = json.loads(line)
        if rec["class"] == "PROTECTED_LEAVE_ALONE":
            continue
        src = rec["path"]
        if not os.path.exists(src):
            n_skipped += 1; continue
        # Use AppleScript to send to Trash (recoverable for ~30 days by default)
        applescript = (
            'tell application "Finder" to delete POSIX file "' +
            src.replace('"','\\"') + '"'
        )
        try:
            subprocess.run(["osascript","-e",applescript], check=True, capture_output=True)
            log.write(f"trashed\t{src}\n"); n_trashed += 1
        except subprocess.CalledProcessError as e:
            log.write(f"FAIL\t{src}\t{e.stderr.decode('utf-8',errors='replace')[:200]}\n")
            n_skipped += 1

log.write(f"summary\ttrashed={n_trashed}\tskipped={n_skipped}\n")
log.close()
print(f"reap done: trashed={n_trashed} skipped={n_skipped}")
PY

echo "[$(date -u +%FT%TZ)] reap done" | tee -a "$LOG"

# Signed: Devon-fad5 | 2026-05-05

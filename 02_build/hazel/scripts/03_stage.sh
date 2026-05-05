#!/usr/bin/env bash
# 03_stage.sh — Phase 3: enact the plan.
#
# Reads plan.jsonl. For each record:
#   SIGNAL_KEEP            -> copy   to ~/_consolidated/<route>/...
#   BLOAT_DROP             -> move   to ~/__trash_staging/...
#   AMBIGUOUS_REVIEW       -> move   to ~/__review/...
#   SECRET_QUARANTINE      -> move   to ~/__quarantine/... (and log)
#   PROTECTED_LEAVE_ALONE  -> skip
#
# Originals of SIGNAL_KEEP files are NOT moved here (they are copied). Phase 5
# is the only step that deletes from the original location.
#
# Idempotent: if the destination exists with the same sha256 prefix, the source
# is not re-copied/moved. Run as many times as needed.
#
# Usage:
#   03_stage.sh                       # defaults
#   03_stage.sh --in ~/_hazel_work --dry-run
#
# Signed: Devon-fad5 | 2026-05-05 | AMP-83
set -euo pipefail

IN="${HOME}/_hazel_work"
DRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --in)      IN="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) grep '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

PLAN="$IN/plan.jsonl"
[[ -f "$PLAN" ]] || { echo "plan missing: $PLAN  (run 02_classify.sh first)" >&2; exit 2; }
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$IN/log/03_stage-$TS.log"
mkdir -p "$IN/log" "$HOME/_consolidated" "$HOME/__trash_staging" "$HOME/__review" "$HOME/__quarantine"

echo "[$(date -u +%FT%TZ)] stage start  plan=$PLAN  dry=$DRY" | tee -a "$LOG"

PY=$(command -v python3 || true)
[[ -z "$PY" ]] && { echo "python3 required" >&2; exit 2; }

"$PY" - "$PLAN" "$LOG" "$DRY" <<'PY'
import sys, json, os, shutil, hashlib, re
plan = sys.argv[1]
log_path = sys.argv[2]
dry = bool(int(sys.argv[3]))

HOME = os.environ["HOME"]
ROUTES = {
    "SIGNAL_KEEP":       os.path.join(HOME, "_consolidated"),
    "BLOAT_DROP":        os.path.join(HOME, "__trash_staging"),
    "AMBIGUOUS_REVIEW":  os.path.join(HOME, "__review"),
    "SECRET_QUARANTINE": os.path.join(HOME, "__quarantine"),
}

def relpath_under_home(p):
    if p.startswith(HOME + "/"):
        return p[len(HOME)+1:]
    return p.lstrip("/")

def hash_prefix(p, n=64*1024):
    try:
        with open(p, "rb") as f:
            return hashlib.sha256(f.read(n)).hexdigest()
    except OSError:
        return None

n_done = {"SIGNAL_KEEP":0,"BLOAT_DROP":0,"AMBIGUOUS_REVIEW":0,"SECRET_QUARANTINE":0,"PROTECTED_LEAVE_ALONE":0}
n_skip = 0
log = open(log_path, "a")

with open(plan) as f:
    for line in f:
        if not line.strip(): continue
        rec = json.loads(line)
        cls = rec["class"]
        src = rec["path"]
        if cls == "PROTECTED_LEAVE_ALONE":
            n_done[cls] += 1; continue
        if not os.path.exists(src):
            log.write(f"skip-missing\t{src}\n"); n_skip += 1; continue

        rel = relpath_under_home(src)
        dest_root = ROUTES[cls]
        dest = os.path.join(dest_root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        if cls == "SECRET_QUARANTINE":
            # Logged by id+prefix only — never the secret itself
            secret_id = next((r for r in rec.get("reasons",[]) if r.startswith("secret:")), "secret:?")
            log.write(f"QUARANTINE\t{src}\t{secret_id}\n")

        if os.path.exists(dest):
            # idempotency: skip if hash matches
            if hash_prefix(src) == hash_prefix(dest):
                log.write(f"skip-existing\t{cls}\t{src}\n"); n_skip += 1; continue

        if dry:
            log.write(f"DRY\t{cls}\t{src}\t->\t{dest}\n")
            n_done[cls] += 1; continue

        try:
            if cls == "SIGNAL_KEEP":
                shutil.copy2(src, dest)
            else:
                shutil.move(src, dest)
            n_done[cls] += 1
        except Exception as e:
            log.write(f"FAIL\t{cls}\t{src}\t{e}\n"); n_skip += 1

for k,v in n_done.items():
    log.write(f"done\t{k}\t{v}\n")
log.write(f"skipped\t{n_skip}\n")
log.close()

print("\nStage summary:")
for k,v in n_done.items():
    print(f"  {k:24} {v}")
print(f"  skipped:                 {n_skip}")
PY

echo "[$(date -u +%FT%TZ)] stage done" | tee -a "$LOG"

# Signed: Devon-fad5 | 2026-05-05

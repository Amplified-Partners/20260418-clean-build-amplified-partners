#!/usr/bin/env bash
# 02_classify.sh — Phase 2: apply policy to manifest, produce a plan.
#
# Read-only. Reads manifest.jsonl (Phase 1) + policy.yaml; emits plan.jsonl
# with one record per file:
#   { path, class, action, route, confidence, reasons[] }
#
# Classes: PROTECTED_LEAVE_ALONE | SECRET_QUARANTINE | BLOAT_DROP
#        | SIGNAL_KEEP | AMBIGUOUS_REVIEW
#
# Usage:
#   02_classify.sh                       # defaults: --in ~/_hazel_work
#   02_classify.sh --in /tmp/inv --policy ./policy.yaml
#
# Signed: Devon-fad5 | 2026-05-05 | AMP-83
set -euo pipefail

IN="${HOME}/_hazel_work"
POLICY=""
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --in)     IN="$2"; shift 2 ;;
    --policy) POLICY="$2"; shift 2 ;;
    -h|--help)
      grep '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

: "${POLICY:=$SCRIPT_DIR/../policy.yaml}"

MANIFEST="$IN/manifest.jsonl"
PLAN="$IN/plan.jsonl"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$IN/log/02_classify-$TS.log"

[[ -f "$MANIFEST" ]] || { echo "manifest missing: $MANIFEST  (run 01_inventory.sh first)" >&2; exit 2; }
mkdir -p "$IN/log"

echo "[$(date -u +%FT%TZ)] classify start  manifest=$MANIFEST  policy=$POLICY" | tee -a "$LOG"

PY=$(command -v python3 || true)
[[ -z "$PY" ]] && { echo "python3 required" >&2; exit 2; }

"$PY" - "$POLICY" "$MANIFEST" "$LOG" "$SCRIPT_DIR/lib/secret_scan.py" >"$PLAN" <<'PY'
import sys, os, json, re, fnmatch, time, subprocess
policy_path = sys.argv[1]
manifest_path = sys.argv[2]
log_path = sys.argv[3]
secret_scan = sys.argv[4]  # path; used only as a hint; secret detection inlined here

# --- minimal YAML reader (no PyYAML on stock macOS python3) ---
def load_yaml(p):
    cfg = {}
    cur_key = None
    cur_list = None
    cur_obj_list = None
    cur_obj = None
    with open(p) as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if not line.startswith(" ") and ":" in line:
                key, _, rest = line.partition(":")
                key = key.strip(); rest = rest.strip()
                # strip inline comments
                if "#" in rest:
                    rest = rest.split("#", 1)[0].strip()
                if rest:
                    if rest.lower() in ("true","false"):
                        cfg[key] = (rest.lower() == "true")
                    else:
                        try: cfg[key] = int(rest)
                        except ValueError:
                            try: cfg[key] = float(rest)
                            except ValueError: cfg[key] = rest.strip('"').strip("'")
                    cur_key = None; cur_list = None; cur_obj_list = None
                else:
                    cur_key = key
                    cur_list = []
                    cur_obj_list = []
                    cfg[key] = cur_list
                continue
            if cur_key and line.startswith("  - "):
                # list item — could be scalar or "id: foo" start of obj
                tail = line[4:]
                if ":" in tail:
                    # obj item: start a new dict
                    k, _, v = tail.partition(":")
                    cur_obj = {k.strip(): v.strip().strip('"').strip("'")}
                    cur_obj_list.append(cur_obj)
                    if cfg[cur_key] is cur_list and cur_list and not isinstance(cur_list[0], dict):
                        # switch the storage to obj list
                        pass
                    cfg[cur_key] = cur_obj_list
                else:
                    val = tail.strip().strip('"').strip("'")
                    cur_list.append(os.path.expandvars(val))
                    cfg[cur_key] = cur_list
            elif cur_key and line.startswith("    ") and ":" in line and cur_obj is not None:
                k, _, v = line.strip().partition(":")
                cur_obj[k.strip()] = v.strip().strip('"').strip("'")
    return cfg

cfg = load_yaml(policy_path)

protected = cfg.get("protected_globs", []) or []
bloat_globs = cfg.get("bloat_globs", []) or []
signal_globs = cfg.get("signal_globs", []) or []
secret_patterns_raw = cfg.get("secret_patterns", []) or []
bloat_exts = set(cfg.get("bloat_extensions", []) or [])
signal_exts = set(cfg.get("signal_extensions", []) or [])
ambiguous_exts = set(cfg.get("ambiguous_extensions", []) or [])
secret_max = int(cfg.get("secret_scan_max_bytes", 10*1024*1024))
heuristics = {
    "ambiguous_to_bloat_age_days": 365,
    "min_confidence": 0.85,
}
# (heuristics may live as a nested key; we keep defaults sane)

# Pre-compile secret regex
secret_regex = []
for it in secret_patterns_raw:
    if isinstance(it, dict) and "regex" in it:
        try:
            secret_regex.append((it.get("id","sec"), re.compile(it["regex"].encode("utf-8"))))
        except re.error:
            pass

def matches_glob(path, globs):
    for g in globs:
        # crude `**` -> `*` for fnmatch
        gnorm = g.replace("/**", "*")
        if fnmatch.fnmatch(path, gnorm) or fnmatch.fnmatch(path, g):
            return True
    return False

def scan_secret(path, size):
    if size <= 0 or size > secret_max:
        return None
    try:
        with open(path, "rb") as f:
            data = f.read(secret_max)
    except (OSError, PermissionError):
        return None
    for sid, rx in secret_regex:
        m = rx.search(data)
        if m:
            tok = m.group(0).decode("utf-8", errors="replace")
            return f"{sid}:{tok[:6]}***"
    return None

def classify(rec):
    p = rec["path"]
    size = rec.get("size", 0)
    mtime = rec.get("mtime", 0)
    reasons = []

    if rec.get("is_protected"):
        return "PROTECTED_LEAVE_ALONE", "skip", None, 1.0, ["protected_glob"]

    # Secret scan first (terminal)
    sec = scan_secret(p, size)
    if sec:
        return "SECRET_QUARANTINE", "move", "$HOME/__quarantine/", 0.99, [f"secret:{sec}"]

    if matches_glob(p, protected):
        return "PROTECTED_LEAVE_ALONE", "skip", None, 1.0, ["protected_glob"]

    if matches_glob(p, bloat_globs):
        return "BLOAT_DROP", "move", "$HOME/__trash_staging/", 0.95, ["bloat_glob"]

    in_signal = matches_glob(p, signal_globs)

    _, ext = os.path.splitext(p)
    ext = ext.lower()

    if in_signal and ext in signal_exts:
        return "SIGNAL_KEEP", "copy", "$HOME/_consolidated/", 0.92, ["signal_glob","signal_ext"]

    if ext in bloat_exts:
        return "BLOAT_DROP", "move", "$HOME/__trash_staging/", 0.90, ["bloat_ext"]

    if in_signal and ext in ambiguous_exts:
        # if old, demote to bloat; if recent, keep as signal-low-confidence
        age_days = (time.time() - mtime) / 86400 if mtime else 0
        if age_days > 365:
            return "BLOAT_DROP", "move", "$HOME/__trash_staging/", 0.80, ["ambiguous_ext","old"]
        return "SIGNAL_KEEP", "copy", "$HOME/_consolidated/", 0.70, ["ambiguous_ext","recent","in_signal"]

    if in_signal and ext in signal_exts:
        return "SIGNAL_KEEP", "copy", "$HOME/_consolidated/", 0.92, ["signal_glob","signal_ext"]

    return "AMBIGUOUS_REVIEW", "move", "$HOME/__review/", 0.50, ["fallthrough"]

n = {"PROTECTED_LEAVE_ALONE":0,"SECRET_QUARANTINE":0,"BLOAT_DROP":0,"SIGNAL_KEEP":0,"AMBIGUOUS_REVIEW":0}
log = open(log_path, "a")

with open(manifest_path) as f:
    for line in f:
        if not line.strip(): continue
        rec = json.loads(line)
        cls, action, route, conf, reasons = classify(rec)
        n[cls] += 1
        out = {
            "path": rec["path"],
            "class": cls,
            "action": action,
            "route": route,
            "confidence": conf,
            "reasons": reasons,
            "size": rec.get("size", 0),
            "mtime": rec.get("mtime", 0),
            "sha256": rec.get("sha256"),
        }
        sys.stdout.write(json.dumps(out, ensure_ascii=False)); sys.stdout.write("\n")

for k,v in n.items():
    log.write(f"class\t{k}\t{v}\n")
log.close()
sys.stderr.write("classify: " + " ".join(f"{k}={v}" for k,v in n.items()) + "\n")
PY

echo "[$(date -u +%FT%TZ)] classify done   plan=$PLAN" | tee -a "$LOG"

# Quick top-line summary for Ewan
"$PY" - "$PLAN" <<'PY'
import sys, json, collections
n = collections.Counter()
size = collections.Counter()
with open(sys.argv[1]) as f:
    for line in f:
        rec = json.loads(line)
        n[rec["class"]] += 1
        size[rec["class"]] += rec.get("size", 0)
order = ["SIGNAL_KEEP","BLOAT_DROP","AMBIGUOUS_REVIEW","SECRET_QUARANTINE","PROTECTED_LEAVE_ALONE"]
print("\nClass                      Files       MiB")
for k in order:
    print(f"  {k:24} {n[k]:6}   {size[k]/1048576:8.1f}")
PY

# Signed: Devon-fad5 | 2026-05-05

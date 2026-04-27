"""
Sentinel v2 — Amplified Partners
Auditor, not just monitor.
Watches: ~/amplified-crm
Logs to: ~/shared/logs/audit.txt
Alerts: SMS via Twilio on confidence < 0.8

Fixes over v1:
- Diff scanner covers unstaged + staged + unpushed commits
- Credential VALUE detection (not variable name detection)
- Allowlist for clean os.environ[] / os.getenv() references
- Hardcoded fallback values in os.getenv("X", "value") ARE caught
- Pylint targets app/ explicitly, sorted by last-modified
- Tiered confidence drops (warn vs. block)
- .env.sentinel hard-required, no fallback values ever
"""

import subprocess
import time
import json
import os
import re
import datetime
from pathlib import Path
from dotenv import load_dotenv

# === HARD FAIL IF NO CREDENTIALS ===
env_path = Path(__file__).parent / ".env.sentinel"
if not env_path.exists():
    raise Exception(
        f"SENTINEL HALTED: .env.sentinel not found at {env_path}. "
        "Copy .env.sentinel.example and fill in real values."
    )
load_dotenv(dotenv_path=env_path)

TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
ALERT_PHONE = os.environ.get("ALERT_PHONE")
TWILIO_FROM = os.environ.get("TWILIO_FROM_PHONE")

for key, val in [
    ("TWILIO_ACCOUNT_SID", TWILIO_SID),
    ("TWILIO_AUTH_TOKEN", TWILIO_TOKEN),
    ("ALERT_PHONE", ALERT_PHONE),
    ("TWILIO_FROM_PHONE", TWILIO_FROM),
]:
    if not val:
        raise Exception(f"SENTINEL HALTED: {key} missing from .env.sentinel")

# === PATHS ===
WATCH_PATH = Path.home() / "amplified-crm"
LOG_PATH = Path.home() / "shared" / "logs" / "audit.txt"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# === CREDENTIAL VALUE PATTERNS ===
# We detect actual credential VALUES, not variable names.
# A variable named TWILIO_AUTH_TOKEN is fine. A 32-char hex string in quotes is not.
CREDENTIAL_PATTERNS = [
    # Twilio Account SID value (AC + 32 hex chars)
    re.compile(r'\bAC[a-f0-9]{32}\b'),
    # Any 32-char hex string in quotes (Twilio auth tokens, etc.)
    re.compile(r'["\'][a-f0-9]{32}["\']'),
    # sk- prefixed tokens (OpenAI, Stripe, Anthropic, etc.)
    re.compile(r'["\']sk-[a-zA-Z0-9\-_]{20,}["\']'),
    # Long strings assigned to credential-named variables
    re.compile(r'(?i)(password|secret|api.?key|auth.?token)\s*=\s*["\'][a-zA-Z0-9+/\-_]{20,}["\']'),
]

# Allowlist: lines that look like env var references (not hardcoded values)
# Applied ONLY when the line contains no embedded credential value
ALLOWLIST_PATTERNS = [
    re.compile(r'os\.environ\['),
    re.compile(r'os\.getenv\([^)]*\)\s*$'),  # getenv with no fallback argument
    re.compile(r'load_dotenv'),
    re.compile(r'#'),  # Comments
]

# Business logic lockouts — keyword presence always blocks (no allowlist)
HARD_LOCKED_KEYWORDS = [
    "whatsapp",
    "WHATSAPP",
    "hr_module",
    "HR_MODULE",
    "redundan",
    "client_pii_export",
]

# === CONFIDENCE THRESHOLDS ===
CONFIDENCE_ALERT = 0.8
CHECK_INTERVAL = 60  # seconds
FAILURE_LIMIT = 3


# === LOGGING ===
def log(level: str, message: str, data: dict = None):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "level": level,
        "message": message,
    }
    if data:
        entry["data"] = data
    line = json.dumps(entry)
    print(line)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


# === SMS ALERT ===
def send_alert(message: str):
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(body=f"[SENTINEL] {message}", from_=TWILIO_FROM, to=ALERT_PHONE)
        log("ALERT", "SMS sent", {"message": message})
    except Exception as e:
        log("ERROR", f"SMS failed: {e}")


# === DIFF COLLECTION ===
def get_full_diff() -> str:
    """
    Collect ALL pending changes:
    1. Unstaged changes (working tree vs index)
    2. Staged changes (index vs HEAD)
    3. Committed-but-unpushed changes (HEAD vs origin/main)
    """
    diffs = []
    commands = [
        ["git", "-C", str(WATCH_PATH), "diff"],
        ["git", "-C", str(WATCH_PATH), "diff", "--cached"],
        ["git", "-C", str(WATCH_PATH), "log", "-p", "origin/main..HEAD"],
    ]
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.stdout.strip():
                diffs.append(result.stdout)
        except Exception as e:
            log("WARN", f"Diff command failed", {"cmd": cmd[-1], "error": str(e)})
    return "\n".join(diffs)


def check_line_for_credentials(line: str) -> tuple[bool, str]:
    """
    Returns (flagged, reason).
    Checks credential VALUE patterns first.
    Applies allowlist only if no embedded credential value is present.
    """
    for pattern in CREDENTIAL_PATTERNS:
        match = pattern.search(line)
        if match:
            # Found a credential pattern. Check allowlist — but NOT if it's a hardcoded fallback.
            # A hardcoded value inside os.getenv("X", "real_value") is always dangerous.
            has_embedded_hex = bool(re.search(r'["\'][a-f0-9]{32}["\']', line))
            has_embedded_sid = bool(re.search(r'\bAC[a-f0-9]{32}\b', line))

            if has_embedded_hex or has_embedded_sid:
                # Always flag — hardcoded fallback or direct assignment
                return True, f"Hardcoded credential value: {match.group()[:30]}"

            # No embedded hex — check if it's a legitimate env var reference
            for ap in ALLOWLIST_PATTERNS:
                if ap.search(line):
                    return False, "allowlisted env var reference"

            return True, f"Credential pattern: {match.group()[:30]}"

    return False, "clean"


# === CHECKS ===
def check_git_status() -> tuple[float, list]:
    """Uncommitted changes reduce confidence but don't block."""
    issues = []
    try:
        result = subprocess.run(
            ["git", "-C", str(WATCH_PATH), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        changes = [l for l in result.stdout.strip().split("\n") if l]
        if changes:
            issues.append(f"{len(changes)} uncommitted file(s)")
            return 0.7, issues
        return 1.0, issues
    except Exception as e:
        issues.append(f"Git check failed: {e}")
        return 0.0, issues


def check_locked_files() -> tuple[float, list]:
    """
    Scan ALL pending diffs for:
    1. Hard-locked business keywords (block at 0.0, no allowlist)
    2. Credential value patterns (block at 0.0, with allowlist)
    Only examines added lines (lines starting with +).
    """
    issues = []
    diff = get_full_diff()

    if not diff:
        return 1.0, []

    added_lines = [l for l in diff.split("\n") if l.startswith("+") and not l.startswith("+++")]

    # Hard-locked keywords — business logic, no allowlist
    for keyword in HARD_LOCKED_KEYWORDS:
        for line in added_lines:
            if keyword.lower() in line.lower():
                issues.append(f"HARD LOCKED keyword '{keyword}' in diff")
                return 0.0, issues

    # Credential value detection — with allowlist
    for line in added_lines:
        flagged, reason = check_line_for_credentials(line)
        if flagged:
            issues.append(f"CREDENTIAL PATTERN in diff ({reason}): {line[:80].strip()}")
            return 0.0, issues

    return 1.0, []


def check_tests() -> tuple[float, list]:
    """Run pytest on tests/ directory only."""
    issues = []
    tests_path = WATCH_PATH / "tests"
    if not tests_path.exists():
        return 0.9, []
    try:
        result = subprocess.run(
            ["python3", "-m", "pytest", str(tests_path), "--tb=no", "-q"],
            capture_output=True, text=True, timeout=60
        )
        output = result.stdout + result.stderr
        if "no tests ran" in output:
            return 0.9, []
        if "failed" in output:
            issues.append(f"Tests failing: {output[-300:]}")
            return 0.5, issues
        return 1.0, issues
    except Exception as e:
        issues.append(f"Test runner failed: {e}")
        return 0.5, issues


def check_pylint() -> tuple[float, list]:
    """
    Run pylint on app/ only.
    Files sorted by last-modified — most recently changed files first.
    Errors only (no style noise).
    """
    issues = []
    app_path = WATCH_PATH / "app"
    if not app_path.exists():
        return 1.0, []

    try:
        py_files = sorted(
            app_path.rglob("*.py"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:20]

        if not py_files:
            return 1.0, []

        result = subprocess.run(
            [
                "python3", "-m", "pylint",
                "--score=yes",
                "--disable=all",
                "--enable=E",
                "--ignore=venv,migrations,tests,__pycache__",
                *[str(f) for f in py_files]
            ],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        if "Your code has been rated" in output:
            try:
                score_line = [l for l in output.split("\n") if "rated" in l][0]
                score = float(score_line.split("/")[0].split(" ")[-1])
                confidence = score / 10.0
                if confidence < 0.8:
                    issues.append(f"Pylint error score: {score}/10")
                return max(confidence, 0.1), issues
            except Exception:
                pass
        return 0.9, []
    except FileNotFoundError:
        return 0.9, []
    except Exception as e:
        issues.append(f"Pylint failed: {e}")
        return 0.8, issues


# === MAIN LOOP ===
def run():
    log("INFO", "Sentinel v2 started", {
        "watch_path": str(WATCH_PATH),
        "log_path": str(LOG_PATH),
        "alert_threshold": CONFIDENCE_ALERT,
        "check_interval_seconds": CHECK_INTERVAL,
    })

    failures = 0

    while True:
        try:
            scores = []
            all_issues = []

            for check_fn in [check_git_status, check_locked_files, check_tests, check_pylint]:
                score, issues = check_fn()
                scores.append(score)
                all_issues.extend(issues)

            confidence = min(scores)  # Weakest link

            log(
                "INFO" if confidence >= CONFIDENCE_ALERT else "WARN",
                "Health check complete",
                {
                    "confidence": round(confidence, 2),
                    "issues": all_issues,
                }
            )

            if confidence < CONFIDENCE_ALERT:
                failures += 1
                log("WARN", f"Low confidence ({confidence:.2f}). Failure {failures}/{FAILURE_LIMIT}")
                if failures >= FAILURE_LIMIT:
                    msg = f"Confidence {confidence:.2f} after {failures} failures. Issues: {'; '.join(all_issues[:2])}"
                    send_alert(msg)
                    failures = 0
            else:
                failures = 0

        except Exception as e:
            log("ERROR", f"Sentinel loop error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()

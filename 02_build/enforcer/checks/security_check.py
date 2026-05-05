# Authored by Claude (Haiku 4.5), 2026-03-11
# Merged into clean-build/02_build/enforcer/checks/ by Devon (Devin session devin-1bdaf31798874921940598bed17ca9e3), 2026-05-04 (AMP-77)
"""Security checks — container-aware."""

import os
import subprocess
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime, timezone


@dataclass
class SecurityCheckResult:
    name: str
    status: str
    message: str
    severity: str
    timestamp: str
    duration_ms: float
    details: Dict[str, Any]


async def check_security(fail2ban_enabled: bool = False) -> SecurityCheckResult:
    now = datetime.now(timezone.utc)
    issues = []
    checks = {}

    in_container = os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")

    if in_container:
        checks["environment"] = {"status": "container", "note": "Running in Docker"}
        if os.path.exists("/var/run/docker.sock"):
            checks["docker_socket"] = {"status": "accessible"}
        else:
            checks["docker_socket"] = {"status": "not_mounted"}
            issues.append("Docker socket not mounted")

        elapsed = (datetime.now(timezone.utc) - now).total_seconds() * 1000
        status = "warn" if issues else "pass"
        return SecurityCheckResult(
            name="security_check", status=status,
            message="Container environment — host security N/A" if not issues else "; ".join(issues),
            severity="info" if not issues else "warning",
            timestamp=now.isoformat(),
            duration_ms=elapsed,
            details={"in_container": True, "checks": checks}
        )

    # Host-level checks
    try:
        result = subprocess.run(["ufw", "status"], capture_output=True, text=True, timeout=5)
        if "active" in result.stdout.lower():
            checks["firewall"] = {"status": "active"}
        else:
            checks["firewall"] = {"status": "inactive"}
            issues.append("firewall inactive")
    except FileNotFoundError:
        checks["firewall"] = {"status": "not_installed"}
        issues.append("firewall: not_installed")
    except Exception as e:
        checks["firewall"] = {"status": "error", "error": str(e)}

    ssh_dir = os.path.expanduser("~/.ssh")
    auth_keys = os.path.join(ssh_dir, "authorized_keys")
    if os.path.exists(auth_keys):
        with open(auth_keys) as f:
            key_count = sum(1 for line in f if line.strip() and not line.startswith("#"))
        checks["ssh_auth"] = {"status": "configured", "key_count": key_count}
    else:
        checks["ssh_auth"] = {"status": "no_authorized_keys"}
        issues.append("No SSH keys configured")

    elapsed = (datetime.now(timezone.utc) - now).total_seconds() * 1000
    if issues:
        return SecurityCheckResult(
            name="security_check", status="warn",
            message=f"{len(issues)} note(s): {'; '.join(issues)}",
            severity="warning",
            timestamp=now.isoformat(),
            duration_ms=elapsed,
            details={"issues": issues, "checks": checks}
        )
    return SecurityCheckResult(
        name="security_check", status="pass",
        message="All security checks passed",
        severity="info",
        timestamp=now.isoformat(),
        duration_ms=elapsed,
        details={"checks": checks}
    )

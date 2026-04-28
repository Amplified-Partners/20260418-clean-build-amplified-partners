"""
The Optimizer (Kaizen) — Continuous Quality Daemon
===================================================
Runs every 10 minutes on Beast. Checks that everything is working
correctly — not just health, but quality and progress.

Named 'Optimizer' because it doesn't enforce — it helps us all do better.
Named 'Kaizen' (continuous improvement) for the container.

Checks:
  1. All Docker containers healthy (via Docker Engine API over socket)
  2. Openclaw agents responding (/health/deep)
  3. LiteLLM model gateway alive
  4. SearXNG search functional
  5. Disk/memory within bounds
  6. Logs findings — alerts if something's off
"""

import asyncio
import json
import os
import subprocess
import time
from datetime import datetime, timezone

import httpx

# --- Config ---
CHECK_INTERVAL = 600  # 10 minutes
OPENCLAW_URL = "http://openclaw-agents:8100"
LITELLM_URL = "http://litellm:4000"
SEARXNG_URL = "http://searxng:8080"
DOCKER_SOCKET = "/var/run/docker.sock"

# Thresholds
DISK_WARN_PERCENT = 85
MEMORY_WARN_PERCENT = 90

# Where to write status
STATUS_FILE = "/data/optimizer_status.json"
LOG_FILE = "/data/optimizer.log"


def log(level: str, msg: str, **kwargs):
    """Structured logging to file and stdout."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "msg": msg,
        **kwargs,
    }
    line = json.dumps(entry)
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# --- Checks ---

async def check_containers() -> dict:
    """Check all Docker containers via Docker Engine API (unix socket)."""
    try:
        transport = httpx.AsyncHTTPTransport(uds=DOCKER_SOCKET)
        async with httpx.AsyncClient(transport=transport, base_url="http://docker", timeout=10.0) as client:
            r = await client.get("/containers/json?all=true")
            containers_data = r.json()

            containers = {}
            unhealthy = []
            for c in containers_data:
                name = c.get("Names", ["/unknown"])[0].lstrip("/")
                state = c.get("State", "unknown")
                status = c.get("Status", "unknown")
                health = c.get("Status", "")
                is_healthy = state == "running" and "unhealthy" not in health.lower()
                containers[name] = {"state": state, "status": status, "healthy": is_healthy}
                if not is_healthy:
                    unhealthy.append(name)

            return {
                "check": "containers",
                "ok": len(unhealthy) == 0,
                "total": len(containers),
                "unhealthy": unhealthy,
            }
    except Exception as e:
        return {"check": "containers", "ok": False, "error": str(e)}


async def check_openclaw() -> dict:
    """Check openclaw-agents deep health."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{OPENCLAW_URL}/health/deep")
            data = r.json()
            return {
                "check": "openclaw",
                "ok": data.get("status") == "ok",
                "status": data.get("status"),
                "checks": data.get("checks", {}),
                "version": data.get("version"),
            }
    except Exception as e:
        return {"check": "openclaw", "ok": False, "error": str(e)}


async def check_litellm() -> dict:
    """Check LiteLLM is alive."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{LITELLM_URL}/health/liveliness")
            return {
                "check": "litellm",
                "ok": r.status_code == 200,
                "status_code": r.status_code,
            }
    except Exception as e:
        return {"check": "litellm", "ok": False, "error": str(e)}


async def check_searxng() -> dict:
    """Check SearXNG responds to a test query."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                f"{SEARXNG_URL}/search",
                params={"q": "test", "format": "json"},
            )
            data = r.json()
            return {
                "check": "searxng",
                "ok": r.status_code == 200 and len(data.get("results", [])) > 0,
                "result_count": len(data.get("results", [])),
            }
    except Exception as e:
        return {"check": "searxng", "ok": False, "error": str(e)}


def check_disk() -> dict:
    """Check disk usage."""
    try:
        result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True, text=True, timeout=5,
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            usage_pct = int(parts[4].rstrip("%"))
            return {
                "check": "disk",
                "ok": usage_pct < DISK_WARN_PERCENT,
                "usage_percent": usage_pct,
                "total": parts[1],
                "available": parts[3],
            }
    except Exception as e:
        return {"check": "disk", "ok": False, "error": str(e)}


def check_memory() -> dict:
    """Check memory usage."""
    try:
        result = subprocess.run(
            ["free", "-m"],
            capture_output=True, text=True, timeout=5,
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) >= 2:
            parts = lines[1].split()
            total = int(parts[1])
            used = int(parts[2])
            pct = round((used / total) * 100) if total > 0 else 0
            return {
                "check": "memory",
                "ok": pct < MEMORY_WARN_PERCENT,
                "usage_percent": pct,
                "total_mb": total,
                "used_mb": used,
            }
    except Exception as e:
        return {"check": "memory", "ok": False, "error": str(e)}


# --- Main Loop ---

async def run_all_checks() -> dict:
    """Run all checks and return a comprehensive report."""
    started = time.time()

    # Sync checks
    disk_result = check_disk()
    memory_result = check_memory()

    # Async checks (all concurrent)
    container_result, openclaw_result, litellm_result, searxng_result = await asyncio.gather(
        check_containers(),
        check_openclaw(),
        check_litellm(),
        check_searxng(),
    )

    checks = [
        container_result,
        openclaw_result,
        litellm_result,
        searxng_result,
        disk_result,
        memory_result,
    ]

    all_ok = all(c.get("ok", False) for c in checks)
    duration = round(time.time() - started, 2)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "ok" if all_ok else "degraded",
        "duration_seconds": duration,
        "checks": {c["check"]: c for c in checks},
        "issues": [c for c in checks if not c.get("ok", False)],
    }

    # Write status file
    try:
        os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
        with open(STATUS_FILE, "w") as f:
            json.dump(report, f, indent=2)
    except Exception as e:
        log("error", f"Failed to write status file: {e}")

    return report


async def optimizer_loop():
    """Main optimizer loop — runs forever."""
    log("info", "Optimizer (Kaizen) started", interval=CHECK_INTERVAL)

    # Run first check immediately
    report = await run_all_checks()
    if report["status"] == "ok":
        log("info", "Initial check: all systems green",
            duration=report["duration_seconds"],
            containers=report["checks"]["containers"].get("total", 0))
    else:
        issues = report["issues"]
        log("warn", f"Initial check: {len(issues)} issue(s)",
            issues=[i["check"] for i in issues])

    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        try:
            report = await run_all_checks()
            if report["status"] == "ok":
                log("info", "All checks passed",
                    duration=report["duration_seconds"],
                    containers=report["checks"]["containers"].get("total", 0))
            else:
                issues = report["issues"]
                log("warn", f"{len(issues)} check(s) failed",
                    issues=[i["check"] for i in issues],
                    details=issues)
        except Exception as e:
            log("error", f"Optimizer loop error: {e}")


if __name__ == "__main__":
    asyncio.run(optimizer_loop())

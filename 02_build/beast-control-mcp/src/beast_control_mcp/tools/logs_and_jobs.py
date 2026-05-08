"""Logs and jobs tools — systemd services, cron jobs, container logs, ingestion jobs.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import json
import subprocess

from .. import config
from ..audit import log_tool_call


def list_systemd_services() -> str:
    """List systemd services and their states."""
    log_tool_call("list_systemd_services", {})
    try:
        proc = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--all", "--no-pager", "--plain"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        lines = proc.stdout.strip().splitlines()
        services: list[dict] = []
        for line in lines[1:]:  # skip header
            parts = line.split(None, 4)
            if len(parts) >= 4:
                services.append(
                    {
                        "unit": parts[0],
                        "load": parts[1],
                        "active": parts[2],
                        "sub": parts[3],
                        "description": parts[4] if len(parts) > 4 else "",
                    }
                )
        return json.dumps(services, indent=2)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def list_cron_jobs() -> str:
    """List all cron jobs from crontab and /etc/cron.d/."""
    log_tool_call("list_cron_jobs", {})
    results: list[dict] = []
    # System crontab
    try:
        proc = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode == 0:
            for line in proc.stdout.strip().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    results.append({"source": "root_crontab", "entry": line})
    except (subprocess.TimeoutExpired, OSError):
        pass

    # /etc/cron.d/
    from pathlib import Path

    cron_d = Path("/etc/cron.d")
    if cron_d.exists():
        for f in sorted(cron_d.iterdir()):
            if f.is_file():
                try:
                    content = f.read_text(errors="replace")
                    for line in content.splitlines():
                        line = line.strip()
                        if line and not line.startswith("#"):
                            results.append({"source": str(f), "entry": line})
                except OSError:
                    continue

    # /etc/crontab
    crontab = Path("/etc/crontab")
    if crontab.exists():
        try:
            content = crontab.read_text(errors="replace")
            for line in content.splitlines():
                line = line.strip()
                if (
                    line
                    and not line.startswith("#")
                    and not line.startswith("SHELL")
                    and not line.startswith("PATH")
                ):
                    results.append({"source": "/etc/crontab", "entry": line})
        except OSError:
            pass

    return json.dumps(results, indent=2)


def list_recent_logs(service_or_path: str, lines: int = 200) -> str:
    """Retrieve recent log lines from journalctl or a log file.

    Args:
        service_or_path: Either a systemd service name or a file path under /var/log.
        lines: Number of lines to return (default 200, max 500).
    """
    lines = min(max(lines, 1), 500)
    log_tool_call("list_recent_logs", {"service_or_path": service_or_path, "lines": lines})

    # If it looks like a file path
    if service_or_path.startswith("/"):
        if not config.is_read_allowed(service_or_path):
            return json.dumps({"error": f"Path not in read allowlist: {service_or_path}"})
        try:
            proc = subprocess.run(
                ["tail", "-n", str(lines), service_or_path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return json.dumps(
                {"source": service_or_path, "lines": proc.stdout.splitlines()[-lines:]}
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            return json.dumps({"error": str(exc)})
    else:
        # Assume systemd service
        try:
            proc = subprocess.run(
                ["journalctl", "-u", service_or_path, "-n", str(lines), "--no-pager"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            return json.dumps(
                {"source": service_or_path, "lines": proc.stdout.splitlines()[-lines:]}
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            return json.dumps({"error": str(exc)})


def get_container_logs(name: str, lines: int = 200) -> str:
    """Retrieve recent logs from a Docker container.

    Args:
        name: Container name.
        lines: Number of lines (default 200, max 500).
    """
    lines = min(max(lines, 1), 500)
    log_tool_call("get_container_logs", {"name": name, "lines": lines})
    try:
        proc = subprocess.run(
            ["docker", "logs", "--tail", str(lines), name],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Docker logs can go to stdout or stderr
        output = proc.stdout + proc.stderr
        log_lines = output.strip().splitlines()[-lines:]
        return json.dumps({"container": name, "line_count": len(log_lines), "lines": log_lines})
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def list_ingestion_jobs() -> str:
    """List ingestion-related containers and their status."""
    log_tool_call("list_ingestion_jobs", {})
    try:
        proc = subprocess.run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                "name=ingestion",
                "--filter",
                "name=graphiti",
                "--filter",
                "name=labeller",
                "--filter",
                "name=harvester",
                "--filter",
                "name=extractor",
                "--format",
                '{"name":"{{.Names}}","status":"{{.Status}}","image":"{{.Image}}"}',
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        jobs: list[dict] = []
        for line in proc.stdout.strip().splitlines():
            if line.strip():
                try:
                    jobs.append(json.loads(line))
                except json.JSONDecodeError:
                    jobs.append({"raw": line})

        # Also check for ingestion progress files
        from pathlib import Path

        progress_dir = Path("/opt/amplified/vault-ingestion-progress")
        if progress_dir.exists():
            progress_files = sorted([f.name for f in progress_dir.iterdir() if f.is_file()])[:20]
            return json.dumps({"containers": jobs, "progress_files": progress_files}, indent=2)
        return json.dumps({"containers": jobs, "progress_files": []}, indent=2)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def get_ingestion_job(job_id: str) -> str:
    """Get details of a specific ingestion container or progress file.

    Args:
        job_id: Container name or progress filename.
    """
    log_tool_call("get_ingestion_job", {"job_id": job_id})
    # Try as container first
    try:
        proc = subprocess.run(
            ["docker", "inspect", job_id],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if proc.returncode == 0:
            data = json.loads(proc.stdout)
            if data:
                c = data[0]
                return json.dumps(
                    {
                        "type": "container",
                        "name": c.get("Name", "").lstrip("/"),
                        "state": c.get("State", {}),
                        "image": c.get("Config", {}).get("Image"),
                        "created": c.get("Created"),
                    },
                    indent=2,
                    default=str,
                )
    except (subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
        pass

    # Try as progress file
    from pathlib import Path

    progress_file = Path("/opt/amplified/vault-ingestion-progress") / job_id
    if progress_file.exists() and config.is_read_allowed(str(progress_file)):
        try:
            content = progress_file.read_text(errors="replace")[:10_000]
            return json.dumps({"type": "progress_file", "name": job_id, "content": content})
        except OSError as exc:
            return json.dumps({"error": str(exc)})

    return json.dumps({"error": f"Not found as container or progress file: {job_id}"})

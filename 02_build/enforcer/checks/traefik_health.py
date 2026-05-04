# Authored by Claude (Haiku 4.5), 2026-03-11
# Merged into clean-build/02_build/enforcer/checks/ by Devon (Devin session devin-1bdaf31798874921940598bed17ca9e3), 2026-05-04 (AMP-77)
"""Traefik reverse proxy health check."""

import socket
from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime, timezone

try:
    import httpx
except ImportError:
    httpx = None


@dataclass
class TraefikCheckResult:
    name: str
    status: str
    message: str
    severity: str
    timestamp: str
    duration_ms: float
    details: Dict[str, Any]


async def check_traefik(traefik_host: str = "traefik") -> TraefikCheckResult:
    now = datetime.now(timezone.utc)

    # Try multiple approaches to reach Traefik
    endpoints = [
        (f"http://{traefik_host}:8080/ping", "API ping"),
        (f"http://{traefik_host}:8080/api/overview", "API overview"),
        (f"http://{traefik_host}:80/", "HTTP port"),
    ]

    for url, desc in endpoints:
        try:
            if httpx:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    response = await client.get(url)
                    if response.status_code in (200, 204):
                        elapsed = (datetime.now(timezone.utc) - now).total_seconds() * 1000
                        return TraefikCheckResult(
                            name="traefik_health", status="pass",
                            message=f"Traefik responding ({desc})",
                            severity="info",
                            timestamp=now.isoformat(),
                            duration_ms=elapsed,
                            details={"url": url, "status_code": response.status_code}
                        )
        except Exception:
            continue

    # Fallback: TCP port check on 80 and 443
    for port in [80, 443, 8080]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((traefik_host, port))
            sock.close()
            if result == 0:
                elapsed = (datetime.now(timezone.utc) - now).total_seconds() * 1000
                return TraefikCheckResult(
                    name="traefik_health", status="pass",
                    message=f"Traefik port {port} reachable",
                    severity="info",
                    timestamp=now.isoformat(),
                    duration_ms=elapsed,
                    details={"method": "tcp", "port": port}
                )
        except:
            continue

    elapsed = (datetime.now(timezone.utc) - now).total_seconds() * 1000
    return TraefikCheckResult(
        name="traefik_health", status="fail",
        message="Traefik API not reachable (ports checked: 80, 443, 8080)",
        severity="critical",
        timestamp=now.isoformat(),
        duration_ms=elapsed,
        details={"error": "All connection attempts failed"}
    )

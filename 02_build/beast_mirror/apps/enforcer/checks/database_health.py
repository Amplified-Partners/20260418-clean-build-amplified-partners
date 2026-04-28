"""Database connectivity and health checks."""

import asyncio
import socket
from dataclasses import dataclass
from typing import Dict, Any, Tuple
from datetime import datetime, timezone

try:
    import redis
except ImportError:
    redis = None

try:
    import httpx
except ImportError:
    httpx = None


@dataclass
class DatabaseCheckResult:
    name: str
    status: str
    message: str
    severity: str
    timestamp: str
    duration_ms: float
    details: Dict[str, Any]


async def _check_redis(host: str, port: int) -> Tuple[bool, str]:
    if not redis:
        return False, "redis-py not installed"
    try:
        r = redis.Redis(host=host, port=port, socket_connect_timeout=2, socket_timeout=2, decode_responses=True)
        r.ping()
        return True, "OK"
    except Exception as e:
        return False, str(e)


async def _check_postgres(host: str, port: int) -> Tuple[bool, str]:
    """Check PostgreSQL via TCP socket (no password needed for health check)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return True, "OK (port reachable)"
        return False, f"port {port} unreachable"
    except Exception as e:
        return False, str(e)


async def _check_qdrant(host: str, port: int) -> Tuple[bool, str]:
    if not httpx:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0, "port check"
        except:
            return False, "port check failed"
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            # Try multiple endpoints
            for endpoint in ["/readyz", "/healthz", "/health", "/"]:
                try:
                    response = await client.get(f"http://{host}:{port}{endpoint}")
                    if response.status_code in (200, 204):
                        return True, f"OK ({endpoint})"
                except:
                    continue
            # Fallback: port check
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0, "port reachable"
    except Exception as e:
        return False, str(e)


async def _check_falkordb(host: str, port: int) -> Tuple[bool, str]:
    if not redis:
        return False, "redis-py not installed"
    try:
        r = redis.Redis(host=host, port=port, socket_connect_timeout=2, socket_timeout=2, decode_responses=True)
        r.ping()
        return True, "OK"
    except Exception as e:
        return False, str(e)


async def check_databases(
    falkordb_host: str, falkordb_port: int,
    postgres_host: str, postgres_port: int,
    redis_host: str, redis_port: int,
    qdrant_host: str, qdrant_port: int,
) -> DatabaseCheckResult:
    now = datetime.now(timezone.utc)
    checks = {
        "FalkorDB": _check_falkordb(falkordb_host, falkordb_port),
        "PostgreSQL": _check_postgres(postgres_host, postgres_port),
        "Redis": _check_redis(redis_host, redis_port),
        "Qdrant": _check_qdrant(qdrant_host, qdrant_port),
    }
    results = {}
    failed = []
    for name, check in checks.items():
        try:
            reachable, msg = await check
            results[name] = {"reachable": reachable, "message": msg}
            if not reachable:
                failed.append(f"{name}: {msg}")
        except Exception as e:
            results[name] = {"reachable": False, "message": str(e)}
            failed.append(f"{name}: {str(e)}")

    if failed:
        return DatabaseCheckResult(
            name="database_health", status="fail",
            message=f"{len(failed)} database(s) unreachable",
            severity="critical" if len(failed) >= 2 else "warning",
            timestamp=datetime.now(timezone.utc).isoformat(),
            duration_ms=(datetime.now(timezone.utc) - now).total_seconds() * 1000,
            details={"total_databases": len(results), "healthy": sum(1 for r in results.values() if r["reachable"]), "failures": failed, "details": results}
        )
    return DatabaseCheckResult(
        name="database_health", status="pass",
        message=f"All {len(results)} databases healthy",
        severity="info",
        timestamp=datetime.now(timezone.utc).isoformat(),
        duration_ms=(datetime.now(timezone.utc) - now).total_seconds() * 1000,
        details={"total_databases": len(results), "healthy": len(results), "details": results}
    )

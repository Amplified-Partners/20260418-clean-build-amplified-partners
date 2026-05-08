"""Beast inventory tools — Docker containers, networks, volumes, compose files, routes, ports.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .. import config
from ..audit import log_tool_call


def _docker_cmd(args: list[str], timeout: int = 30) -> str:
    """Run a docker CLI command and return stdout."""
    result = subprocess.run(
        ["docker", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        return json.dumps({"error": result.stderr.strip()})
    return result.stdout.strip()


def list_containers() -> str:
    """List all Docker containers (running and stopped) with name, status, image, and ports."""
    log_tool_call("list_containers", {})
    fmt = '{"name":"{{.Names}}","status":"{{.Status}}","image":"{{.Image}}","ports":"{{.Ports}}"}'
    raw = _docker_cmd(["ps", "-a", "--format", fmt])
    if raw.startswith('{"error"'):
        return raw
    lines = [line for line in raw.splitlines() if line.strip()]
    containers = []
    for line in lines:
        try:
            containers.append(json.loads(line))
        except json.JSONDecodeError:
            containers.append({"raw": line})
    return json.dumps(containers, indent=2)


def inspect_container(name: str) -> str:
    """Inspect a container — config, state, mounts, network, env var names (not values)."""
    log_tool_call("inspect_container", {"name": name})
    raw = _docker_cmd(["inspect", name])
    if raw.startswith('{"error"'):
        return raw
    try:
        data = json.loads(raw)
        if not data:
            return json.dumps({"error": f"Container '{name}' not found"})
        c = data[0]
        env_names = []
        for e in c.get("Config", {}).get("Env") or []:
            key = e.split("=", 1)[0]
            env_names.append(key)
        result = {
            "name": c.get("Name", "").lstrip("/"),
            "state": c.get("State", {}),
            "image": c.get("Config", {}).get("Image", ""),
            "cmd": c.get("Config", {}).get("Cmd"),
            "env_names": env_names,
            "mounts": [
                {
                    "type": m.get("Type"),
                    "source": m.get("Source"),
                    "destination": m.get("Destination"),
                    "rw": m.get("RW"),
                }
                for m in (c.get("Mounts") or [])
            ],
            "networks": list((c.get("NetworkSettings", {}).get("Networks") or {}).keys()),
            "ports": c.get("NetworkSettings", {}).get("Ports", {}),
            "labels": {
                k: v
                for k, v in (c.get("Config", {}).get("Labels") or {}).items()
                if k.startswith("traefik.") or k.startswith("com.docker.compose.")
            },
            "created": c.get("Created"),
            "restart_policy": c.get("HostConfig", {}).get("RestartPolicy", {}),
            "health": c.get("State", {}).get("Health", {}),
        }
        return json.dumps(result, indent=2, default=str)
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        return json.dumps({"error": f"Parse error: {exc}"})


def list_docker_networks() -> str:
    """List all Docker networks with connected container counts."""
    log_tool_call("list_docker_networks", {})
    fmt = '{"name":"{{.Name}}","driver":"{{.Driver}}","scope":"{{.Scope}}"}'
    raw = _docker_cmd(["network", "ls", "--format", fmt])
    if raw.startswith('{"error"'):
        return raw
    networks = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            net = json.loads(line)
            inspect_raw = _docker_cmd(
                ["network", "inspect", net["name"], "--format", "{{len .Containers}}"]
            )
            net["container_count"] = int(inspect_raw) if inspect_raw.isdigit() else 0
            networks.append(net)
        except (json.JSONDecodeError, ValueError):
            networks.append({"raw": line})
    return json.dumps(networks, indent=2)


def list_docker_volumes() -> str:
    """List all Docker volumes with size and mount point."""
    log_tool_call("list_docker_volumes", {})
    fmt = '{"name":"{{.Name}}","driver":"{{.Driver}}","mountpoint":"{{.Mountpoint}}"}'
    raw = _docker_cmd(["volume", "ls", "--format", fmt])
    if raw.startswith('{"error"'):
        return raw
    volumes = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            volumes.append(json.loads(line))
        except json.JSONDecodeError:
            volumes.append({"raw": line})
    return json.dumps(volumes, indent=2)


def list_compose_files() -> str:
    """Find all docker-compose files under known Beast paths."""
    log_tool_call("list_compose_files", {})
    results: list[dict] = []
    for root in config.COMPOSE_SEARCH_ROOTS:
        if not root.exists():
            continue
        try:
            proc = subprocess.run(
                [
                    "find",
                    str(root),
                    "-maxdepth",
                    "4",
                    "-name",
                    "docker-compose*.yml",
                    "-o",
                    "-name",
                    "compose*.yml",
                    "-o",
                    "-name",
                    "compose*.yaml",
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            for line in proc.stdout.strip().splitlines():
                if line.strip():
                    p = Path(line.strip())
                    results.append(
                        {
                            "path": str(p),
                            "size_bytes": p.stat().st_size if p.exists() else 0,
                        }
                    )
        except (subprocess.TimeoutExpired, OSError):
            continue
    return json.dumps(results, indent=2)


def read_compose_file(path: str) -> str:
    """Read the contents of a docker-compose file (must be under allowlisted paths)."""
    log_tool_call("read_compose_file", {"path": path})
    if not config.is_read_allowed(path):
        return json.dumps({"error": f"Path not in read allowlist: {path}"})
    p = Path(path)
    if not p.exists():
        return json.dumps({"error": f"File not found: {path}"})
    if not p.name.startswith(("docker-compose", "compose")):
        return json.dumps({"error": "Not a compose file"})
    try:
        content = p.read_text(errors="replace")
        if len(content) > 50_000:
            content = content[:50_000] + "\n... [truncated at 50KB]"
        return json.dumps({"path": path, "content": content})
    except OSError as exc:
        return json.dumps({"error": str(exc)})


def list_exposed_routes() -> str:
    """List Traefik-exposed routes by reading container labels."""
    log_tool_call("list_exposed_routes", {})
    raw = _docker_cmd(
        [
            "ps",
            "--filter",
            "label=traefik.enable=true",
            "--format",
            '{"name":"{{.Names}}","labels":"{{.Labels}}"}',
        ]
    )
    if raw.startswith('{"error"'):
        return raw
    routes: list[dict] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            c = json.loads(line)
            name = c["name"]
            inspect_raw = _docker_cmd(["inspect", name, "--format", "{{json .Config.Labels}}"])
            labels = json.loads(inspect_raw) if inspect_raw else {}
            route_info: dict = {"container": name, "rules": []}
            for k, v in labels.items():
                if "rule" in k.lower() and "traefik" in k.lower():
                    route_info["rules"].append({"label": k, "value": v})
                if "certresolver" in k.lower():
                    route_info["tls"] = True
                if "loadbalancer" in k.lower() and "port" in k.lower():
                    route_info["backend_port"] = v
            routes.append(route_info)
        except (json.JSONDecodeError, KeyError):
            continue
    return json.dumps(routes, indent=2)


def list_open_ports() -> str:
    """List all host-bound ports from running containers."""
    log_tool_call("list_open_ports", {})
    fmt = '{"name":"{{.Names}}","ports":"{{.Ports}}"}'
    raw = _docker_cmd(["ps", "--format", fmt])
    if raw.startswith('{"error"'):
        return raw
    port_map: list[dict] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            c = json.loads(line)
            if c.get("ports"):
                port_map.append({"container": c["name"], "ports": c["ports"]})
        except json.JSONDecodeError:
            continue
    return json.dumps(port_map, indent=2)

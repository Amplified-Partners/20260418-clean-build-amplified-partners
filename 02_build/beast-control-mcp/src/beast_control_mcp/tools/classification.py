"""Classification tools — classify services for simplification, beast_full_picture.

The key tool. For every service/container/repo/path, return keep/migrate/support/retire.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone

from ..audit import log_tool_call, write_audit_snapshot
from . import code_discovery, databases, filesystem, inventory, logs_and_jobs

# ---------------------------------------------------------------------------
# Known service classifications — manually curated baseline.
# If data is missing, return UNKNOWN. Do not classify by vibe.
# ---------------------------------------------------------------------------

_KNOWN_CLASSIFICATIONS: dict[str, dict] = {
    "falkordb": {
        "type": "container",
        "current_role": "FalkorDB graph database — stores business_knowledge graph (Graphiti)",
        "data_owned": ["business_knowledge graph", "graphiti episodic/entity nodes"],
        "classification": "MIGRATION_SOURCE",
        "reason": "Graph data migrates to Postgres + pgvector Brain",
        "migration_needed": True,
        "shutdown_risk": "medium",
        "next_action": "Export graph schema and data, map to Postgres tables",
    },
    "qdrant": {
        "type": "container",
        "current_role": "Qdrant vector database — stores amplified_knowledge embeddings",
        "data_owned": ["amplified_knowledge collection", "vault document embeddings"],
        "classification": "MIGRATION_SOURCE",
        "reason": "Vector embeddings migrate to pgvector in Postgres Brain",
        "migration_needed": True,
        "shutdown_risk": "medium",
        "next_action": "Export collection schemas and sample data, map to pgvector tables",
    },
    "postgres": {
        "type": "container",
        "current_role": "PostgreSQL 16 — amplified_main database",
        "data_owned": ["amplified_main database"],
        "classification": "KEEP_CORE",
        "reason": "Postgres is the target Brain — keep and extend with pgvector",
        "migration_needed": False,
        "shutdown_risk": "high",
        "next_action": "Add pgvector extension, create Brain schema",
    },
    "redis": {
        "type": "container",
        "current_role": "Redis cache and message broker",
        "data_owned": ["ephemeral cache"],
        "classification": "SUPPORTING_INFRA",
        "reason": "Cache layer — evaluate if still needed after simplification",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Audit what uses Redis; retire if only FalkorDB used it",
    },
    "litellm": {
        "type": "container",
        "current_role": "LLM model router with fallback chains",
        "data_owned": ["routing config", "virtual keys"],
        "classification": "KEEP_CORE",
        "reason": "Model routing is core infrastructure for all agents",
        "migration_needed": False,
        "shutdown_risk": "high",
        "next_action": "Verify API keys, clean up virtual key burn (AMP-143)",
    },
    "ollama": {
        "type": "container",
        "current_role": "Local LLM inference (Llama 3.1, Qwen3)",
        "data_owned": ["model weights"],
        "classification": "KEEP_CORE",
        "reason": "Local inference is core to the Four-Russian Stack",
        "migration_needed": False,
        "shutdown_risk": "medium",
        "next_action": "Verify model list matches what agents actually use",
    },
    "cove-temporal": {
        "type": "container",
        "current_role": "Temporal durable workflow engine",
        "data_owned": ["workflow history", "task queues"],
        "classification": "KEEP_CORE",
        "reason": "Durable execution is core to agent orchestration",
        "migration_needed": False,
        "shutdown_risk": "high",
        "next_action": "Fix gRPC probe failure (AMP-139)",
    },
    "traefik": {
        "type": "container",
        "current_role": "Reverse proxy and TLS termination",
        "data_owned": ["TLS certs", "routing rules"],
        "classification": "KEEP_CORE",
        "reason": "Edge routing required for all exposed services",
        "migration_needed": False,
        "shutdown_risk": "high",
        "next_action": "Fix dashboard unreachable (AMP-140)",
    },
    "amplified-knowledge-mcp": {
        "type": "container",
        "current_role": "MCP server for FalkorDB + Qdrant knowledge access",
        "data_owned": [],
        "classification": "MIGRATION_SOURCE",
        "reason": "Will be superseded by beast-control-mcp and Brain-backed tools",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Keep running until Brain migration complete, then retire",
    },
    "vault-graphiti": {
        "type": "container",
        "current_role": "Graphiti vault ingestion — populates FalkorDB from vault markdown",
        "data_owned": ["ingestion progress state"],
        "classification": "MIGRATION_SOURCE",
        "reason": "Ingestion target changes from FalkorDB to Postgres Brain",
        "migration_needed": True,
        "shutdown_risk": "low",
        "next_action": "Rebuild ingestion pipeline to target Postgres",
    },
    "amplified-crm": {
        "type": "container",
        "current_role": "CRM FastAPI backend (production build)",
        "data_owned": ["CRM database tables"],
        "classification": "KEEP_CORE",
        "reason": "Core revenue product",
        "migration_needed": False,
        "shutdown_risk": "high",
        "next_action": "Fix health check failure, deploy latest from GitHub",
    },
    "amplified-crm-dev": {
        "type": "container",
        "current_role": "CRM FastAPI backend (dev build)",
        "data_owned": [],
        "classification": "SUPPORTING_INFRA",
        "reason": "Dev instance for testing",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Evaluate if needed alongside production container",
    },
    "amplified-core": {
        "type": "container",
        "current_role": "Amplified Machine core API",
        "data_owned": ["machine state"],
        "classification": "KEEP_CORE",
        "reason": "Core API for content pipeline and Brain",
        "migration_needed": False,
        "shutdown_risk": "medium",
        "next_action": "Verify what endpoints are actively used",
    },
    "watchtower": {
        "type": "container",
        "current_role": "Auto-update Docker images",
        "data_owned": [],
        "classification": "SUPPORTING_INFRA",
        "reason": "Convenience tool, not business-critical",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Keep or retire based on update strategy preference",
    },
    "tailscale": {
        "type": "container",
        "current_role": "VPN mesh networking",
        "data_owned": [],
        "classification": "SUPPORTING_INFRA",
        "reason": "Network access layer — stuck in Created state (AMP-136)",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Fix or retire (AMP-136)",
    },
    "minio": {
        "type": "container",
        "current_role": "S3-compatible object storage",
        "data_owned": ["stored objects"],
        "classification": "SUPPORTING_INFRA",
        "reason": "Object storage — check what uses it",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Audit stored objects; migrate to Postgres LOBs or keep",
    },
    "langfuse": {
        "type": "container",
        "current_role": "LLM observability and tracing",
        "data_owned": ["trace data"],
        "classification": "SUPPORTING_INFRA",
        "reason": "Observability is valuable but not mission-critical",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Keep if actively used for Opik/tracing, retire if unused",
    },
    "clickhouse": {
        "type": "container",
        "current_role": "Columnar analytics database",
        "data_owned": ["analytics tables"],
        "classification": "RETIRE",
        "reason": "Analytics can move to Postgres; ClickHouse is overkill at current scale",
        "migration_needed": True,
        "shutdown_risk": "low",
        "next_action": "Check if any data exists; migrate to Postgres if so",
    },
    "searxng": {
        "type": "container",
        "current_role": "Self-hosted meta search engine",
        "data_owned": [],
        "classification": "SUPPORTING_INFRA",
        "reason": "APDS harvester dependency — evaluate usage",
        "migration_needed": False,
        "shutdown_risk": "low",
        "next_action": "Keep if APDS harvester uses it, retire otherwise",
    },
}


def classify_service_for_simplification(name: str) -> str:
    """Classify a service/container for simplification.

    Returns keep_core | migration_source | supporting_infra | retire | unknown.

    Args:
        name: Container name, service name, or path to classify.
    """
    log_tool_call("classify_service_for_simplification", {"name": name})
    # Check known classifications first
    key = name.lower().replace("-", "").replace("_", "")
    for known_name, classification in _KNOWN_CLASSIFICATIONS.items():
        known_key = known_name.lower().replace("-", "").replace("_", "")
        if key == known_key or known_name in name or name in known_name:
            result = {"name": name, **classification}
            # Enrich with live data
            try:
                proc = subprocess.run(
                    [
                        "docker",
                        "inspect",
                        name,
                        "--format",
                        '{"status":"{{.State.Status}}","running":"{{.State.Running}}"}',
                    ],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if proc.returncode == 0:
                    live = json.loads(proc.stdout.strip())
                    result["live_status"] = live
            except (subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
                pass
            return json.dumps(result, indent=2)

    # Unknown service — gather what we can
    result: dict = {
        "name": name,
        "type": "unknown",
        "current_role": "UNKNOWN — not in curated classification list",
        "data_owned": [],
        "depends_on": [],
        "used_by": [],
        "classification": "UNKNOWN",
        "reason": "No curated classification exists. Manual inspection required.",
        "migration_needed": False,
        "shutdown_risk": "unknown",
        "next_action": "Inspect manually and add to classification registry",
    }
    # Try to get container info
    try:
        proc = subprocess.run(
            [
                "docker",
                "inspect",
                name,
                "--format",
                '{"image":"{{.Config.Image}}","status":"{{.State.Status}}"}',
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if proc.returncode == 0:
            result["live_data"] = json.loads(proc.stdout.strip())
            result["type"] = "container"
    except (subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
        pass
    return json.dumps(result, indent=2)


def classify_all_services() -> str:
    """Classify all running and stopped containers for simplification."""
    log_tool_call("classify_all_services", {})
    try:
        proc = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        names = [n.strip() for n in proc.stdout.strip().splitlines() if n.strip()]
        classifications: list[dict] = []
        for name in names:
            c = json.loads(classify_service_for_simplification(name))
            classifications.append(c)
        # Summary counts
        summary = {
            "KEEP_CORE": 0,
            "MIGRATION_SOURCE": 0,
            "SUPPORTING_INFRA": 0,
            "RETIRE": 0,
            "UNKNOWN": 0,
        }
        for c in classifications:
            cat = c.get("classification", "UNKNOWN")
            summary[cat] = summary.get(cat, 0) + 1
        return json.dumps({"summary": summary, "services": classifications}, indent=2)
    except (subprocess.TimeoutExpired, OSError) as exc:
        return json.dumps({"error": str(exc)})


def beast_full_picture() -> str:
    """The full Beast picture in one call.

    Returns containers, databases, routes, volumes, repos, vault roots,
    raw dump roots, ingestion jobs, recent failures, and simplification map.

    Writes audit files to /opt/amplified/audits/<timestamp>/.
    """
    log_tool_call("beast_full_picture", {})
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    picture: dict = {}

    # Containers
    picture["containers"] = json.loads(inventory.list_containers())

    # Databases
    picture["databases"] = {
        "postgres": json.loads(databases.list_postgres_databases()),
        "qdrant": json.loads(databases.list_qdrant_collections()),
        "falkordb": json.loads(databases.list_falkordb_graphs()),
    }

    # Routes
    picture["routes"] = json.loads(inventory.list_exposed_routes())

    # Volumes
    picture["volumes"] = json.loads(inventory.list_docker_volumes())

    # Repos
    picture["repos"] = json.loads(code_discovery.list_repos())

    # Vault roots
    picture["vault_roots"] = json.loads(filesystem.list_vault_roots())

    # Raw dump roots
    picture["raw_dump_roots"] = json.loads(filesystem.list_raw_dump_roots())

    # Ingestion jobs
    picture["ingestion_jobs"] = json.loads(logs_and_jobs.list_ingestion_jobs())

    # Recent failures — containers that are exited or unhealthy
    failures: list[dict] = []
    for c in picture["containers"]:
        if isinstance(c, dict):
            status = c.get("status", "").lower()
            if "exited" in status or "unhealthy" in status or "dead" in status:
                failures.append({"name": c.get("name"), "status": c.get("status")})
    picture["recent_failures"] = failures

    # Simplification map
    picture["simplification_map"] = json.loads(classify_all_services())

    # Write audit files
    try:
        write_audit_snapshot(ts, "beast_full_picture.json", picture)
        write_audit_snapshot(ts, "containers.json", picture["containers"])
        write_audit_snapshot(ts, "databases.json", picture["databases"])
        write_audit_snapshot(ts, "routes.json", picture["routes"])
        write_audit_snapshot(ts, "volumes.json", picture["volumes"])
        write_audit_snapshot(ts, "repos.json", picture["repos"])
        write_audit_snapshot(ts, "simplification_map.json", picture["simplification_map"])

        # Generate summary.md
        summary_lines = [
            f"# Beast Full Picture — {ts}",
            "",
            f"## Containers: {len(picture['containers'])}",
            f"## Failures: {len(failures)}",
            "",
        ]
        for f in failures:
            summary_lines.append(f"- **{f['name']}**: {f['status']}")
        summary_lines.append("")
        summary_lines.append("## Simplification Summary")
        smap = picture["simplification_map"]
        if isinstance(smap, dict) and "summary" in smap:
            for cat, count in smap["summary"].items():
                summary_lines.append(f"- {cat}: {count}")
        summary_lines.append("")
        summary_lines.append("## Databases")
        pg = picture["databases"].get("postgres", {})
        if isinstance(pg, list):
            for db in pg:
                summary_lines.append(
                    f"- Postgres: {db.get('database', '?')} ({db.get('size_bytes', 0)} bytes)"
                )
        qdrant = picture["databases"].get("qdrant", {})
        if isinstance(qdrant, list):
            for col in qdrant:
                summary_lines.append(
                    f"- Qdrant: {col.get('name', '?')} ({col.get('points_count', 0)} points)"
                )
        elif isinstance(qdrant, dict) and "error" in qdrant:
            summary_lines.append(f"- Qdrant: {qdrant['error']}")
        falkor = picture["databases"].get("falkordb", {})
        if isinstance(falkor, list):
            for g in falkor:
                summary_lines.append(
                    f"- FalkorDB: {g.get('graph', '?')} ({g.get('node_count', '?')} nodes)"
                )
        elif isinstance(falkor, dict) and "error" in falkor:
            summary_lines.append(f"- FalkorDB: {falkor['error']}")

        write_audit_snapshot(ts, "summary.md", "\n".join(summary_lines))
        picture["audit_dir"] = f"/opt/amplified/audits/{ts}"
    except OSError as exc:
        picture["audit_error"] = str(exc)

    return json.dumps(picture, indent=2, default=str)

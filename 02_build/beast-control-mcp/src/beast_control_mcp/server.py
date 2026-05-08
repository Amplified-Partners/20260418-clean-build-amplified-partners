"""Beast Control MCP server — entrypoint.

The MCP is not the Brain.
The MCP is the torch we use to see the old Beast clearly enough to simplify it.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from . import config
from .tools import classification, code_discovery, databases, filesystem, inventory, logs_and_jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
_log = logging.getLogger("beast_control")

mcp = FastMCP(
    "Beast Control MCP",
    version="0.1.0",
    description=(
        "Allowlisted control surface for Beast (Hetzner M5). "
        "Inspect, classify, and safely audit the existing infrastructure "
        "so we can simplify it into the new Postgres + pgvector Brain."
    ),
)

# ===================================================================
# Inventory tools
# ===================================================================


@mcp.tool()
def list_containers() -> str:
    """List all Docker containers (running and stopped) with name, status, image, and ports."""
    return inventory.list_containers()


@mcp.tool()
def inspect_container(name: str) -> str:
    """Inspect a specific container — config, state, mounts, network, env var names (not values).

    Args:
        name: Container name to inspect.
    """
    return inventory.inspect_container(name)


@mcp.tool()
def list_docker_networks() -> str:
    """List all Docker networks with connected container counts."""
    return inventory.list_docker_networks()


@mcp.tool()
def list_docker_volumes() -> str:
    """List all Docker volumes with driver and mount point."""
    return inventory.list_docker_volumes()


@mcp.tool()
def list_compose_files() -> str:
    """Find all docker-compose files under known Beast paths."""
    return inventory.list_compose_files()


@mcp.tool()
def read_compose_file(path: str) -> str:
    """Read a docker-compose file (must be under allowlisted paths).

    Args:
        path: Full path to the compose file.
    """
    return inventory.read_compose_file(path)


@mcp.tool()
def list_exposed_routes() -> str:
    """List Traefik-exposed routes from container labels."""
    return inventory.list_exposed_routes()


@mcp.tool()
def list_open_ports() -> str:
    """List all host-bound ports from running containers."""
    return inventory.list_open_ports()


# ===================================================================
# Database tools
# ===================================================================


@mcp.tool()
def list_postgres_databases() -> str:
    """List all Postgres databases with sizes."""
    return databases.list_postgres_databases()


@mcp.tool()
def list_postgres_extensions(database: str) -> str:
    """List installed extensions for a Postgres database.

    Args:
        database: Database name.
    """
    return databases.list_postgres_extensions(database)


@mcp.tool()
def list_postgres_tables(database: str) -> str:
    """List all tables in a Postgres database with row count estimates and size.

    Args:
        database: Database name.
    """
    return databases.list_postgres_tables(database)


@mcp.tool()
def describe_postgres_table(database: str, table: str) -> str:
    """Describe columns, types, indexes, and constraints for a Postgres table.

    Args:
        database: Database name.
        table: Table name (optionally schema-qualified, e.g. 'public.users').
    """
    return databases.describe_postgres_table(database, table)


@mcp.tool()
def run_postgres_readonly_query(database: str, sql: str, limit: int = 100) -> str:
    """Run a read-only SQL query against Postgres. Only SELECT/WITH/EXPLAIN/SHOW allowed.

    Args:
        database: Database name.
        sql: SQL query (read-only only).
        limit: Max rows to return (default 100, max 500).
    """
    return databases.run_postgres_readonly_query(database, sql, limit)


@mcp.tool()
def list_qdrant_collections() -> str:
    """List Qdrant collections with point counts, vector dimensions, and status."""
    return databases.list_qdrant_collections()


@mcp.tool()
def sample_qdrant_collection(name: str, limit: int = 5) -> str:
    """Sample points from a Qdrant collection (payload only, no vectors).

    Args:
        name: Collection name.
        limit: Number of points to sample (default 5, max 20).
    """
    return databases.sample_qdrant_collection(name, limit)


@mcp.tool()
def list_falkordb_graphs() -> str:
    """List all graph keys in FalkorDB with node/edge counts."""
    return databases.list_falkordb_graphs()


@mcp.tool()
def sample_falkordb_schema(graph: str) -> str:
    """Sample the schema of a FalkorDB graph — node labels, edge types, property keys.

    Args:
        graph: Graph name (e.g. 'business_knowledge').
    """
    return databases.sample_falkordb_schema(graph)


# ===================================================================
# Filesystem tools
# ===================================================================


@mcp.tool()
def list_vault_roots() -> str:
    """List known vault directories with file counts."""
    return filesystem.list_vault_roots()


@mcp.tool()
def list_raw_dump_roots() -> str:
    """List known raw dump directories (Mac dumps, takeout extracts) with file counts."""
    return filesystem.list_raw_dump_roots()


@mcp.tool()
def list_ingestion_roots() -> str:
    """List known ingestion directories with file counts."""
    return filesystem.list_ingestion_roots()


@mcp.tool()
def list_recent_files(path: str, limit: int = 100) -> str:
    """List most recently modified files under a path, newest first.

    Args:
        path: Directory to scan (must be under read allowlist).
        limit: Max files to return (default 100, max 500).
    """
    return filesystem.list_recent_files(path, limit)


@mcp.tool()
def find_files(root: str, pattern: str, limit: int = 500) -> str:
    """Find files matching a glob pattern under a root path.

    Args:
        root: Directory to search (must be under read allowlist).
        pattern: Glob pattern (e.g. '*.py', '*.yml').
        limit: Max results (default 500).
    """
    return filesystem.find_files(root, pattern, limit)


@mcp.tool()
def hash_file(path: str) -> str:
    """Return the SHA-256 hash and size of a file.

    Args:
        path: File path (must be under read allowlist).
    """
    return filesystem.hash_file(path)


@mcp.tool()
def summarise_directory_counts(path: str) -> str:
    """Summarise a directory: file counts by extension, total size, subdirectories.

    Args:
        path: Directory to summarise (must be under read allowlist).
    """
    return filesystem.summarise_directory_counts(path)


@mcp.tool()
def list_secret_names() -> str:
    """List filenames in the secrets directory. Never returns file contents."""
    return filesystem.list_secret_names()


# ===================================================================
# Logs and jobs tools
# ===================================================================


@mcp.tool()
def list_systemd_services() -> str:
    """List systemd services and their states."""
    return logs_and_jobs.list_systemd_services()


@mcp.tool()
def list_cron_jobs() -> str:
    """List all cron jobs from crontab and /etc/cron.d/."""
    return logs_and_jobs.list_cron_jobs()


@mcp.tool()
def list_recent_logs(service_or_path: str, lines: int = 200) -> str:
    """Retrieve recent log lines from journalctl or a log file.

    Args:
        service_or_path: Systemd service name or file path under /var/log.
        lines: Number of lines (default 200, max 500).
    """
    return logs_and_jobs.list_recent_logs(service_or_path, lines)


@mcp.tool()
def get_container_logs(name: str, lines: int = 200) -> str:
    """Retrieve recent logs from a Docker container.

    Args:
        name: Container name.
        lines: Number of lines (default 200, max 500).
    """
    return logs_and_jobs.get_container_logs(name, lines)


@mcp.tool()
def list_ingestion_jobs() -> str:
    """List ingestion-related containers and progress files."""
    return logs_and_jobs.list_ingestion_jobs()


@mcp.tool()
def get_ingestion_job(job_id: str) -> str:
    """Get details of a specific ingestion container or progress file.

    Args:
        job_id: Container name or progress filename.
    """
    return logs_and_jobs.get_ingestion_job(job_id)


# ===================================================================
# Code / repo discovery tools
# ===================================================================


@mcp.tool()
def list_repos() -> str:
    """List all git repositories found under Beast paths."""
    return code_discovery.list_repos()


@mcp.tool()
def repo_status(path: str) -> str:
    """Get git status for a repository.

    Args:
        path: Path to the git repository.
    """
    return code_discovery.repo_status(path)


@mcp.tool()
def repo_recent_commits(path: str, limit: int = 20) -> str:
    """Get recent commits from a git repository.

    Args:
        path: Path to the git repository.
        limit: Number of commits (default 20, max 100).
    """
    return code_discovery.repo_recent_commits(path, limit)


@mcp.tool()
def repo_search(path: str, query: str, limit: int = 100) -> str:
    """Search for a string in a git repository.

    Args:
        path: Path to the git repository.
        query: Search string.
        limit: Max matching lines (default 100).
    """
    return code_discovery.repo_search(path, query, limit)


@mcp.tool()
def repo_find_files(path: str, pattern: str, limit: int = 100) -> str:
    """Find files matching a pattern in a git repository.

    Args:
        path: Path to the git repository.
        pattern: Glob pattern (e.g. '*.py').
        limit: Max files (default 100).
    """
    return code_discovery.repo_find_files(path, pattern, limit)


@mcp.tool()
def list_python_services() -> str:
    """Find all Python services on Beast (by main.py, app.py, pyproject.toml markers)."""
    return code_discovery.list_python_services()


@mcp.tool()
def list_fastapi_apps() -> str:
    """Find FastAPI applications by searching for FastAPI imports."""
    return code_discovery.list_fastapi_apps()


@mcp.tool()
def list_requirements() -> str:
    """Find all requirements.txt and pyproject.toml files on Beast."""
    return code_discovery.list_requirements()


# ===================================================================
# Classification tools
# ===================================================================


@mcp.tool()
def classify_service_for_simplification(name: str) -> str:
    """Classify a service/container for simplification.

    Returns KEEP_CORE, MIGRATION_SOURCE, SUPPORTING_INFRA, RETIRE, or UNKNOWN.

    Args:
        name: Container name, service name, or path.
    """
    return classification.classify_service_for_simplification(name)


@mcp.tool()
def classify_all_services() -> str:
    """Classify all containers for simplification.

    Returns summary + per-service classification.
    """
    return classification.classify_all_services()


@mcp.tool()
def beast_full_picture() -> str:
    """The full Beast picture in one call.

    Returns containers, databases, routes, volumes, repos, vault roots,
    raw dump roots, ingestion jobs, recent failures, and simplification map.

    Writes audit files to /opt/amplified/audits/<timestamp>/.
    """
    return classification.beast_full_picture()


# ===================================================================
# Entrypoint
# ===================================================================


def main() -> None:
    """Run the Beast Control MCP server."""
    _log.info(
        "Starting Beast Control MCP — transport=%s",
        config.TRANSPORT,
    )
    if config.TRANSPORT == "sse":
        mcp.run(transport="sse", host=config.SSE_HOST, port=config.SSE_PORT)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

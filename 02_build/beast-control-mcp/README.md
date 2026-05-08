# Beast Control MCP

Allowlisted MCP control surface for the Beast (Hetzner M5 server). Lets trusted agents
inspect, classify, and safely audit the existing Beast infrastructure so we can simplify
it into the new Postgres + pgvector Brain.

**The MCP is not the Brain. The MCP is the torch we use to see the old Beast clearly
enough to simplify it.**

## What it does

One command — `beast_full_picture()` — returns:

- **Containers**: all running/stopped Docker containers
- **Databases**: Postgres, FalkorDB, Qdrant state
- **Routes**: Traefik-exposed services
- **Volumes**: data ownership map
- **Repos**: code ownership map
- **Vaults**: raw/clean/archive paths
- **Jobs**: ingestion/cron/Temporal state
- **Logs**: recent failures
- **Classification**: keep / migrate / support / retire for every service

## Security model

- **No arbitrary shell.** Every tool is allowlisted.
- **No secret values.** `/opt/amplified/secrets` lists filenames only.
- **Read-only Postgres.** Only SELECT/WITH/EXPLAIN/SHOW allowed.
- **Filesystem allowlist.** Only reads from known Beast paths.
- **Every tool call logged** to `/opt/amplified/audits/tool_calls.jsonl`.
- **Audit snapshots** written to `/opt/amplified/audits/<timestamp>/`.
- **Auth token** required on SSE transport (set `BEAST_MCP_AUTH_TOKEN`).

## V1 tool count: 40+

### Inventory (8)
`list_containers`, `inspect_container`, `list_docker_networks`, `list_docker_volumes`,
`list_compose_files`, `read_compose_file`, `list_exposed_routes`, `list_open_ports`

### Databases (8)
`list_postgres_databases`, `list_postgres_extensions`, `list_postgres_tables`,
`describe_postgres_table`, `run_postgres_readonly_query`, `list_qdrant_collections`,
`sample_qdrant_collection`, `list_falkordb_graphs`, `sample_falkordb_schema`

### Filesystem (7)
`list_vault_roots`, `list_raw_dump_roots`, `list_ingestion_roots`, `list_recent_files`,
`find_files`, `hash_file`, `summarise_directory_counts`, `list_secret_names`

### Logs & Jobs (6)
`list_systemd_services`, `list_cron_jobs`, `list_recent_logs`, `get_container_logs`,
`list_ingestion_jobs`, `get_ingestion_job`

### Code Discovery (8)
`list_repos`, `repo_status`, `repo_recent_commits`, `repo_search`, `repo_find_files`,
`list_python_services`, `list_fastapi_apps`, `list_requirements`

### Classification (3)
`classify_service_for_simplification`, `classify_all_services`, `beast_full_picture`

## Run locally (stdio transport)

```bash
cd 02_build/beast-control-mcp
pip install -e .
BEAST_MCP_TRANSPORT=stdio beast-control-mcp
```

## Run on Beast (SSE transport via Docker)

```bash
cd /opt/amplified/apps/beast-control-mcp
# Set auth token
export BEAST_MCP_AUTH_TOKEN=<your-token>
docker compose up -d --build
```

The server will be available at `https://beast-control.beast.amplifiedpartners.ai/sse`
via Traefik.

## Connect from Perplexity Desktop

In Perplexity Desktop → Settings → Connectors → Add Connector → Advanced:

```json
{
  "command": "npx",
  "args": [
    "-y",
    "mcp-remote",
    "https://beast-control.beast.amplifiedpartners.ai/sse",
    "--transport",
    "http-only"
  ],
  "useBuiltInNode": true
}
```

## Connect from Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "beast-control": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://beast-control.beast.amplifiedpartners.ai/sse",
        "--transport",
        "http-only"
      ]
    }
  }
}
```

## Audit output

Every `beast_full_picture()` call writes:

```
/opt/amplified/audits/<timestamp>/
  beast_full_picture.json
  containers.json
  databases.json
  routes.json
  volumes.json
  repos.json
  simplification_map.json
  summary.md
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BEAST_MCP_TRANSPORT` | `sse` | Transport: `sse` or `stdio` |
| `BEAST_MCP_PORT` | `8400` | SSE listen port |
| `BEAST_MCP_HOST` | `0.0.0.0` | SSE listen host |
| `BEAST_MCP_AUTH_TOKEN` | (empty) | Bearer token for SSE auth |
| `POSTGRES_HOST` | `127.0.0.1` | Postgres host |
| `POSTGRES_PORT` | `5434` | Postgres port |
| `POSTGRES_USER` | `amplified` | Postgres user |
| `POSTGRES_PASSWORD` | (empty) | Postgres password |
| `FALKORDB_HOST` | `127.0.0.1` | FalkorDB host |
| `FALKORDB_PORT` | `6380` | FalkorDB port |
| `QDRANT_HOST` | `127.0.0.1` | Qdrant host |
| `QDRANT_PORT` | `6333` | Qdrant port |
| `AUDIT_DIR` | `/opt/amplified/audits` | Audit file directory |

---

*Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26*

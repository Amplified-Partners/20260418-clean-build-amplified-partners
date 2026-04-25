"""
PostgreSQL MCP Server — Amplified Partners
===========================================
Direct database access for agents: schema inspection, queries, migrations.
Runs against the Cove database on Beast.

Env vars:
    POSTGRES_DSN — postgresql://user:pass@host:port/dbname
"""

import os
import json
import logging
from enum import Enum
from typing import Any

import asyncpg
from pydantic import BaseModel, ConfigDict, Field, field_validator
from mcp.server.fastmcp import FastMCP

SERVICE_NAME = "postgresql"
DSN = os.getenv("POSTGRES_DSN", "postgresql://cove:cove@localhost:5432/cove")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [postgresql_mcp] %(message)s")
log = logging.getLogger("postgresql_mcp")

mcp = FastMCP(
    "postgresql_mcp",
    instructions=(
        "PostgreSQL connector for the Cove database. "
        "Supports schema inspection, read queries, and controlled writes. "
        "All tools prefixed with postgresql_."
    ),
)


class ResponseFormat(str, Enum):
    json = "json"
    markdown = "markdown"


_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None or _pool._closed:
        _pool = await asyncpg.create_pool(DSN, min_size=2, max_size=10)
    return _pool


# ─── Input Models ────────────────────────────────────────────────────────────

class QueryInput(BaseModel):
    model_config = ConfigDict(strict=True)
    sql: str = Field(description="SQL query to execute. SELECT only for read operations.")
    params: list[Any] = Field(default=[], description="Query parameters ($1, $2, etc.)")
    limit: int = Field(default=50, ge=1, le=500, description="Max rows to return")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)


class ListTablesInput(BaseModel):
    model_config = ConfigDict(strict=True)
    schema_name: str = Field(default="public", description="Database schema to list tables from")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)


class DescribeTableInput(BaseModel):
    model_config = ConfigDict(strict=True)
    table_name: str = Field(description="Table name to describe")
    schema_name: str = Field(default="public")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)


class ExecuteInput(BaseModel):
    """For INSERT/UPDATE/DELETE — requires explicit confirmation."""
    model_config = ConfigDict(strict=True)
    sql: str = Field(description="SQL statement to execute (INSERT, UPDATE, DELETE, DDL)")
    params: list[Any] = Field(default=[])
    confirm: bool = Field(default=False, description="Must be True to execute write operations")
    response_format: ResponseFormat = Field(default=ResponseFormat.markdown)


# ─── Tools ───────────────────────────────────────────────────────────────────

@mcp.tool(
    name="postgresql_query",
    description="Execute a read-only SQL query against the Cove database. Returns rows up to the limit.",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def query(input: QueryInput) -> str:
    pool = await get_pool()
    try:
        rows = await pool.fetch(f"{input.sql} LIMIT {input.limit}", *input.params)
    except Exception as e:
        return f"Error: {e}\nSuggestion: Check SQL syntax and table/column names. Use postgresql_list_tables to see available tables."

    if not rows:
        return "No rows returned." if input.response_format == ResponseFormat.markdown else json.dumps([])

    records = [dict(r) for r in rows]
    # Convert non-serializable types
    for r in records:
        for k, v in r.items():
            if hasattr(v, "isoformat"):
                r[k] = v.isoformat()
            elif isinstance(v, (bytes, bytearray)):
                r[k] = v.hex()

    if input.response_format == ResponseFormat.json:
        return json.dumps(records, indent=2, default=str)

    if not records:
        return "No results."

    cols = list(records[0].keys())
    lines = [f"## Query Results ({len(records)} rows)\n"]
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("| " + " | ".join("---" for _ in cols) + " |")
    for r in records[:30]:  # Cap markdown table at 30 rows for readability
        lines.append("| " + " | ".join(str(r.get(c, ""))[:50] for c in cols) + " |")
    if len(records) > 30:
        lines.append(f"\n*Showing 30 of {len(records)} rows. Use json format for full results.*")
    return "\n".join(lines)


@mcp.tool(
    name="postgresql_list_tables",
    description="List all tables in a database schema with row counts.",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def list_tables(input: ListTablesInput) -> str:
    pool = await get_pool()
    rows = await pool.fetch(
        """
        SELECT t.tablename,
               pg_stat_get_live_tuples(c.oid) as row_count
        FROM pg_tables t
        JOIN pg_class c ON c.relname = t.tablename
        WHERE t.schemaname = $1
        ORDER BY t.tablename
        """,
        input.schema_name,
    )

    tables = [{"name": r["tablename"], "rows": r["row_count"]} for r in rows]

    if input.response_format == ResponseFormat.json:
        return json.dumps(tables, indent=2)

    lines = [f"## Tables in `{input.schema_name}` ({len(tables)})\n"]
    lines.append("| Table | Rows |")
    lines.append("| --- | --- |")
    for t in tables:
        lines.append(f"| `{t['name']}` | {t['rows']:,} |")
    return "\n".join(lines)


@mcp.tool(
    name="postgresql_describe_table",
    description="Get column details for a table: names, types, nullable, defaults, constraints.",
    annotations={"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
)
async def describe_table(input: DescribeTableInput) -> str:
    pool = await get_pool()
    rows = await pool.fetch(
        """
        SELECT column_name, data_type, is_nullable, column_default,
               character_maximum_length
        FROM information_schema.columns
        WHERE table_schema = $1 AND table_name = $2
        ORDER BY ordinal_position
        """,
        input.schema_name,
        input.table_name,
    )

    if not rows:
        return f"Table `{input.schema_name}.{input.table_name}` not found. Use postgresql_list_tables to see available tables."

    cols = [
        {
            "name": r["column_name"],
            "type": r["data_type"],
            "nullable": r["is_nullable"] == "YES",
            "default": r["column_default"],
            "max_length": r["character_maximum_length"],
        }
        for r in rows
    ]

    if input.response_format == ResponseFormat.json:
        return json.dumps(cols, indent=2)

    lines = [f"## `{input.table_name}` ({len(cols)} columns)\n"]
    lines.append("| Column | Type | Nullable | Default |")
    lines.append("| --- | --- | --- | --- |")
    for c in cols:
        t = c["type"]
        if c["max_length"]:
            t += f"({c['max_length']})"
        lines.append(f"| `{c['name']}` | {t} | {'✓' if c['nullable'] else '✗'} | {c['default'] or '-'} |")
    return "\n".join(lines)


@mcp.tool(
    name="postgresql_execute",
    description=(
        "Execute a write SQL statement (INSERT, UPDATE, DELETE, DDL). "
        "Requires confirm=True as a safety gate. Returns affected row count."
    ),
    annotations={"readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": False},
)
async def execute(input: ExecuteInput) -> str:
    if not input.confirm:
        return (
            "Safety gate: set confirm=True to execute write operations.\n"
            f"Statement preview: {input.sql[:200]}"
        )

    pool = await get_pool()
    try:
        result = await pool.execute(input.sql, *input.params)
    except Exception as e:
        return f"Error: {e}\nSuggestion: Check SQL syntax, table existence, and constraint violations."

    if input.response_format == ResponseFormat.json:
        return json.dumps({"result": result, "status": "executed"})
    return f"Executed: {result}"


if __name__ == "__main__":
    mcp.run(transport="stdio")

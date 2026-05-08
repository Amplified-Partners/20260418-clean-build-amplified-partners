"""Database inspection tools — Postgres, Qdrant, FalkorDB.

Signed-by: Devon-f055 | 2026-05-07 | session devin-f055293582074f98b4c1ed6f77732b26
"""

from __future__ import annotations

import json
import logging

from .. import config
from ..audit import log_tool_call

_log = logging.getLogger("beast_control.databases")

# ---------------------------------------------------------------------------
# Postgres helpers
# ---------------------------------------------------------------------------

_PG_FORBIDDEN = frozenset(
    {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
        "COPY",
        "VACUUM",
        "REINDEX",
        "CLUSTER",
        "SET",
        "RESET",
        "DISCARD",
        "LOAD",
        "PREPARE",
        "EXECUTE",
        "DEALLOCATE",
        "LISTEN",
        "NOTIFY",
        "LOCK",
        "COMMENT",
        "SECURITY",
    }
)


def _pg_connect(database: str | None = None):
    """Return a psycopg2 connection to the given database."""
    import psycopg2

    return psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        dbname=database or config.POSTGRES_DEFAULT_DB,
        connect_timeout=10,
    )


def _is_readonly_sql(sql: str) -> bool:
    """Reject anything that is not a SELECT / WITH / EXPLAIN / SHOW."""
    stripped = sql.strip().rstrip(";").upper()
    first_word = stripped.split()[0] if stripped.split() else ""
    if first_word in _PG_FORBIDDEN:
        return False
    if first_word not in ("SELECT", "WITH", "EXPLAIN", "SHOW", "TABLE"):
        return False
    for kw in _PG_FORBIDDEN:
        if f" {kw} " in f" {stripped} ":
            return False
    return True


def list_postgres_databases() -> str:
    """List all Postgres databases."""
    log_tool_call("list_postgres_databases", {})
    try:
        conn = _pg_connect("postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            "SELECT datname, pg_database_size(datname) AS size_bytes"
            " FROM pg_database WHERE datistemplate = false ORDER BY datname"
        )
        rows = [{"database": r[0], "size_bytes": r[1]} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return json.dumps(rows, indent=2)
    except Exception as exc:
        return json.dumps({"error": str(exc)})


def list_postgres_extensions(database: str) -> str:
    """List installed extensions for a Postgres database."""
    log_tool_call("list_postgres_extensions", {"database": database})
    try:
        conn = _pg_connect(database)
        cur = conn.cursor()
        cur.execute("SELECT extname, extversion FROM pg_extension ORDER BY extname")
        rows = [{"extension": r[0], "version": r[1]} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return json.dumps(rows, indent=2)
    except Exception as exc:
        return json.dumps({"error": str(exc)})


def list_postgres_tables(database: str) -> str:
    """List all tables in a Postgres database with row count estimates and size."""
    log_tool_call("list_postgres_tables", {"database": database})
    try:
        conn = _pg_connect(database)
        cur = conn.cursor()
        cur.execute("""
            SELECT schemaname, tablename,
                   pg_total_relation_size(schemaname || '.' || tablename) AS size_bytes,
                   n_live_tup AS est_rows
            FROM pg_stat_user_tables
            ORDER BY schemaname, tablename
        """)
        rows = [
            {"schema": r[0], "table": r[1], "size_bytes": r[2], "est_rows": r[3]}
            for r in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return json.dumps(rows, indent=2)
    except Exception as exc:
        return json.dumps({"error": str(exc)})


def describe_postgres_table(database: str, table: str) -> str:
    """Describe columns, types, and constraints for a Postgres table."""
    log_tool_call("describe_postgres_table", {"database": database, "table": table})
    try:
        conn = _pg_connect(database)
        cur = conn.cursor()
        # Split schema.table if provided
        parts = table.split(".", 1)
        schema = parts[0] if len(parts) == 2 else "public"
        tbl = parts[1] if len(parts) == 2 else parts[0]
        cur.execute(
            """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position
        """,
            (schema, tbl),
        )
        columns = [
            {"column": r[0], "type": r[1], "nullable": r[2], "default": r[3]}
            for r in cur.fetchall()
        ]
        # Indexes
        cur.execute(
            """
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = %s AND tablename = %s
        """,
            (schema, tbl),
        )
        indexes = [{"name": r[0], "definition": r[1]} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return json.dumps(
            {"schema": schema, "table": tbl, "columns": columns, "indexes": indexes}, indent=2
        )
    except Exception as exc:
        return json.dumps({"error": str(exc)})


def run_postgres_readonly_query(database: str, sql: str, limit: int = 100) -> str:
    """Run a read-only SQL query against a Postgres database.

    Only SELECT, WITH, EXPLAIN, SHOW, and TABLE are allowed.
    Results capped at `limit` rows (max 500).
    """
    limit = min(max(limit, 1), config.PG_MAX_ROWS)
    log_tool_call(
        "run_postgres_readonly_query", {"database": database, "sql": sql[:200], "limit": limit}
    )
    if not _is_readonly_sql(sql):
        return json.dumps(
            {"error": "Only read-only queries (SELECT/WITH/EXPLAIN/SHOW/TABLE) are allowed."}
        )
    try:
        conn = _pg_connect(database)
        cur = conn.cursor()
        cur.execute(sql)
        if cur.description:
            columns = [d[0] for d in cur.description]
            rows = cur.fetchmany(limit)
            result = {"columns": columns, "rows": [list(r) for r in rows], "row_count": len(rows)}
        else:
            result = {"message": "Query executed, no rows returned."}
        cur.close()
        conn.close()
        return json.dumps(result, indent=2, default=str)
    except Exception as exc:
        return json.dumps({"error": str(exc)})


# ---------------------------------------------------------------------------
# Qdrant
# ---------------------------------------------------------------------------


def list_qdrant_collections() -> str:
    """List all Qdrant collections with point counts and vector dimensions."""
    log_tool_call("list_qdrant_collections", {})
    try:
        import httpx

        resp = httpx.get(
            f"http://{config.QDRANT_HOST}:{config.QDRANT_PORT}/collections", timeout=10
        )
        data = resp.json()
        collections = []
        for c in data.get("result", {}).get("collections", []):
            name = c.get("name", "")
            detail_resp = httpx.get(
                f"http://{config.QDRANT_HOST}:{config.QDRANT_PORT}/collections/{name}",
                timeout=10,
            )
            detail = detail_resp.json().get("result", {})
            collections.append(
                {
                    "name": name,
                    "points_count": detail.get("points_count", 0),
                    "vectors_count": detail.get("vectors_count", 0),
                    "status": detail.get("status", "unknown"),
                    "config": detail.get("config", {}).get("params", {}),
                }
            )
        return json.dumps(collections, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"Qdrant not reachable: {exc}"})


def sample_qdrant_collection(name: str, limit: int = 5) -> str:
    """Sample points from a Qdrant collection (payload only, no vectors)."""
    limit = min(max(limit, 1), 20)
    log_tool_call("sample_qdrant_collection", {"name": name, "limit": limit})
    try:
        import httpx

        resp = httpx.post(
            f"http://{config.QDRANT_HOST}:{config.QDRANT_PORT}/collections/{name}/points/scroll",
            json={"limit": limit, "with_payload": True, "with_vector": False},
            timeout=15,
        )
        data = resp.json()
        points = []
        for p in data.get("result", {}).get("points", []):
            points.append(
                {
                    "id": p.get("id"),
                    "payload": p.get("payload", {}),
                }
            )
        return json.dumps(
            {"collection": name, "sample_count": len(points), "points": points},
            indent=2,
            default=str,
        )
    except Exception as exc:
        return json.dumps({"error": f"Qdrant not reachable: {exc}"})


# ---------------------------------------------------------------------------
# FalkorDB
# ---------------------------------------------------------------------------


def _falkor_connect():
    """Return a Redis client pointed at FalkorDB."""
    import redis

    return redis.Redis(
        host=config.FALKORDB_HOST,
        port=config.FALKORDB_PORT,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=30,
    )


def list_falkordb_graphs() -> str:
    """List all graph keys in FalkorDB."""
    log_tool_call("list_falkordb_graphs", {})
    try:
        client = _falkor_connect()
        try:
            graphs = client.execute_command("GRAPH.LIST")
            names = [g if isinstance(g, str) else g.decode("utf-8") for g in graphs]
        except Exception:
            # Fallback: scan for graphdata keys
            names = []
            for key in client.scan_iter("*", count=1000):
                key_str = key if isinstance(key, str) else key.decode("utf-8")
                try:
                    t = client.type(key_str)
                    ts = t if isinstance(t, str) else t.decode("utf-8")
                    if ts == "graphdata":
                        names.append(key_str)
                except Exception:
                    continue
        result = []
        for name in names:
            try:
                info = client.execute_command(
                    "GRAPH.QUERY", name, "MATCH (n) RETURN count(n) AS node_count"
                )
                node_count = _extract_count(info)
            except Exception:
                node_count = "unknown"
            try:
                info = client.execute_command(
                    "GRAPH.QUERY", name, "MATCH ()-[r]->() RETURN count(r) AS edge_count"
                )
                edge_count = _extract_count(info)
            except Exception:
                edge_count = "unknown"
            result.append({"graph": name, "node_count": node_count, "edge_count": edge_count})
        client.close()
        return json.dumps(result, indent=2, default=str)
    except Exception as exc:
        return json.dumps({"error": f"FalkorDB not reachable: {exc}"})


def _extract_count(raw) -> int:
    """Extract a single count value from GRAPH.QUERY response."""
    if isinstance(raw, list) and len(raw) >= 2:
        rows = raw[1] if isinstance(raw[1], list) else []
        if rows and isinstance(rows[0], list):
            val = rows[0][0]
            if isinstance(val, list) and len(val) == 2:
                return int(val[1])
            return int(val)
    return 0


def sample_falkordb_schema(graph: str) -> str:
    """Sample the schema of a FalkorDB graph — node labels, edge types, property keys."""
    log_tool_call("sample_falkordb_schema", {"graph": graph})
    try:
        client = _falkor_connect()
        schema: dict = {"graph": graph, "node_labels": [], "edge_types": [], "sample_nodes": []}

        # Node labels
        try:
            raw = client.execute_command(
                "GRAPH.QUERY", graph, "MATCH (n) RETURN DISTINCT labels(n) AS lbl LIMIT 50"
            )
            if isinstance(raw, list) and len(raw) >= 2 and isinstance(raw[1], list):
                for row in raw[1]:
                    val = row[0] if isinstance(row, list) else row
                    if isinstance(val, list) and len(val) == 2:
                        val = val[1]
                    schema["node_labels"].append(str(val))
        except Exception as exc:
            schema["node_labels_error"] = str(exc)

        # Edge types
        try:
            raw = client.execute_command(
                "GRAPH.QUERY", graph, "MATCH ()-[r]->() RETURN DISTINCT type(r) AS t LIMIT 50"
            )
            if isinstance(raw, list) and len(raw) >= 2 and isinstance(raw[1], list):
                for row in raw[1]:
                    val = row[0] if isinstance(row, list) else row
                    if isinstance(val, list) and len(val) == 2:
                        val = val[1]
                    schema["edge_types"].append(str(val))
        except Exception as exc:
            schema["edge_types_error"] = str(exc)

        # Sample nodes with properties
        try:
            raw = client.execute_command("GRAPH.QUERY", graph, "MATCH (n) RETURN n LIMIT 5")
            if isinstance(raw, list) and len(raw) >= 2 and isinstance(raw[1], list):
                for row in raw[1]:
                    schema["sample_nodes"].append(str(row)[:500])
        except Exception as exc:
            schema["sample_nodes_error"] = str(exc)

        client.close()
        return json.dumps(schema, indent=2, default=str)
    except Exception as exc:
        return json.dumps({"error": f"FalkorDB not reachable: {exc}"})

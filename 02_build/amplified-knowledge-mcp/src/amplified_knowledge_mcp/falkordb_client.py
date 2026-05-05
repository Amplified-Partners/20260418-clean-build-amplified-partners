"""
FalkorDB client — wraps Redis wire protocol for Cypher graph queries.

FalkorDB knowledge graph built by Clawd (OpenClaw).

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b
"""

from __future__ import annotations

import json
import logging
from typing import Any

import redis

from .config import FALKORDB_HOST, FALKORDB_PORT

_log = logging.getLogger("amplified_mcp.falkordb")

_pool: redis.ConnectionPool | None = None


def _get_client() -> redis.Redis:
    global _pool
    if _pool is None:
        _pool = redis.ConnectionPool(
            host=FALKORDB_HOST,
            port=FALKORDB_PORT,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=30,
        )
    return redis.Redis(connection_pool=_pool)


def graph_query(graph_name: str, cypher: str) -> dict[str, Any]:
    """Execute a Cypher query against a FalkorDB graph and return structured results."""
    client = _get_client()
    _log.info("GRAPH.QUERY %s: %s", graph_name, cypher[:200])
    raw = client.execute_command("GRAPH.QUERY", graph_name, cypher)
    return _parse_result(raw)


def _parse_result(raw: Any) -> dict[str, Any]:
    """Parse FalkorDB GRAPH.QUERY response into a structured dict."""
    if not isinstance(raw, list) or len(raw) == 0:
        return {"columns": [], "rows": [], "stats": []}

    result: dict[str, Any] = {"columns": [], "rows": [], "stats": []}

    # FalkorDB returns: [header, [row, row, ...], stats]
    # or: [header, stats] when no rows
    # or: [stats] for write queries
    idx = 0

    # First element might be column headers
    if idx < len(raw) and isinstance(raw[idx], list) and all(
        isinstance(h, (list, str)) for h in raw[idx]
    ):
        headers = raw[idx]
        # Headers can be [column_type, column_name] pairs or plain strings
        columns = []
        for h in headers:
            if isinstance(h, list) and len(h) >= 2:
                columns.append(str(h[1]))
            else:
                columns.append(str(h))
        result["columns"] = columns
        idx += 1

    # Next element might be data rows
    if idx < len(raw) and isinstance(raw[idx], list):
        # Check if this looks like rows (list of lists) vs stats (list of strings)
        if raw[idx] and isinstance(raw[idx][0], list):
            rows = []
            for row in raw[idx]:
                parsed_row = []
                for cell in row:
                    parsed_row.append(_parse_cell(cell))
                rows.append(parsed_row)
            result["rows"] = rows
            idx += 1

    # Remaining elements are stats
    if idx < len(raw):
        stats_raw = raw[idx] if isinstance(raw[idx], list) else [raw[idx]]
        result["stats"] = [str(s) for s in stats_raw]

    return result


def _parse_cell(cell: Any) -> Any:
    """Parse an individual cell value from FalkorDB response."""
    if isinstance(cell, list):
        # Could be [type_code, value] from FalkorDB typed results
        if len(cell) == 2 and isinstance(cell[0], int):
            return _parse_cell(cell[1])
        # Could be a node or edge representation
        if len(cell) >= 3 and isinstance(cell[0], int):
            # Node: [id, [labels], [properties]]
            return _parse_node_or_edge(cell)
        return [_parse_cell(item) for item in cell]
    if isinstance(cell, bytes):
        return cell.decode("utf-8", errors="replace")
    return cell


def _parse_node_or_edge(data: list) -> dict[str, Any]:
    """Parse a FalkorDB node or edge into a readable dict."""
    result: dict[str, Any] = {"id": data[0]}
    if len(data) > 1 and isinstance(data[1], list):
        result["labels"] = [str(l) for l in data[1]]
    if len(data) > 2 and isinstance(data[2], list):
        props = {}
        for prop in data[2]:
            if isinstance(prop, list) and len(prop) >= 2:
                key = str(prop[0])
                val = _parse_cell(prop[1]) if len(prop) > 1 else None
                props[key] = val
        result["properties"] = props
    return result


def list_graphs() -> list[str]:
    """List all graph keys in FalkorDB."""
    client = _get_client()
    # FalkorDB graphs are stored as Redis keys; use GRAPH.LIST if available
    try:
        graphs = client.execute_command("GRAPH.LIST")
        if isinstance(graphs, list):
            return [g.decode("utf-8") if isinstance(g, bytes) else str(g) for g in graphs]
    except redis.exceptions.ResponseError:
        pass
    # Fallback: scan for graph keys
    result = []
    for key in client.scan_iter("*", count=1000):
        key_str = key if isinstance(key, str) else key.decode("utf-8")
        try:
            key_type = client.type(key_str)
            t = key_type if isinstance(key_type, str) else key_type.decode("utf-8")
            if t == "graphdata":
                result.append(key_str)
        except redis.exceptions.ResponseError:
            continue
    return result

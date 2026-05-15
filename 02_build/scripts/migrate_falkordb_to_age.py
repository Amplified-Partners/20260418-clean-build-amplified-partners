#!/usr/bin/env python3
"""
FalkorDB → Apache AGE Migration Script
========================================

Exports all nodes and relationships from FalkorDB (Redis-backed graph DB)
and imports them into PostgreSQL + Apache AGE within the amplified_brain database.

Target: Same PostgreSQL instance that already runs pgvector and relational tables.
Source: FalkorDB container at falkordb:6379 (legacy, read-only during migration).

Migration scope:
  - 4 graphs, ~9,000 nodes total
  - All relationships preserved
  - Node properties mapped to AGE vertex properties
  - Edge properties mapped to AGE edge properties

The Canonical Data Architecture is the law. One engine. Three capabilities.
No separate processes. — Ewan Bramley, 2026-05-08.

Usage:
  # Dry run (export only, no import):
  python migrate_falkordb_to_age.py --dry-run

  # Full migration:
  python migrate_falkordb_to_age.py

  # Verify after migration:
  python migrate_falkordb_to_age.py --verify-only

Environment variables:
  FALKORDB_HOST    FalkorDB host (default: falkordb)
  FALKORDB_PORT    FalkorDB port (default: 6379)
  PG_HOST          PostgreSQL host (default: cove-postgres)
  PG_PORT          PostgreSQL port (default: 5432)
  PG_DB            Database name (default: amplified_brain)
  PG_USER          PostgreSQL user (default: postgres)
  PG_PASSWORD      PostgreSQL password (required)

Signed-by: Devon-8da1 | 2026-05-15 | devin-8da1981ce177481da3fe1d2b40e7fade
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("migrate_falkordb_to_age")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FALKORDB_HOST = os.environ.get("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.environ.get("FALKORDB_PORT", "6379"))

PG_HOST = os.environ.get("PG_HOST", "cove-postgres")
PG_PORT = int(os.environ.get("PG_PORT", "5432"))
PG_DB = os.environ.get("PG_DB", "amplified_brain")
PG_USER = os.environ.get("PG_USER", "postgres")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "")

# Known FalkorDB graphs to migrate
KNOWN_GRAPHS = [
    "compound_design",
    "business_knowledge",
    "pudding_recipes",
    "entity_relationships",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class GraphNode:
    """A node extracted from FalkorDB."""
    node_id: int
    labels: list[str]
    properties: dict
    source_graph: str


@dataclass
class GraphEdge:
    """A relationship extracted from FalkorDB."""
    src_id: int
    dst_id: int
    relation_type: str
    properties: dict
    source_graph: str


@dataclass
class MigrationReport:
    """Tracks migration progress and results."""
    graphs_processed: int = 0
    nodes_exported: int = 0
    edges_exported: int = 0
    nodes_imported: int = 0
    edges_imported: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: str = ""
    completed_at: str = ""

    def summary(self) -> str:
        return (
            f"Migration report:\n"
            f"  Graphs processed: {self.graphs_processed}\n"
            f"  Nodes exported:   {self.nodes_exported}\n"
            f"  Nodes imported:   {self.nodes_imported}\n"
            f"  Edges exported:   {self.edges_exported}\n"
            f"  Edges imported:   {self.edges_imported}\n"
            f"  Errors:           {len(self.errors)}\n"
            f"  Started:          {self.started_at}\n"
            f"  Completed:        {self.completed_at}\n"
        )


# ---------------------------------------------------------------------------
# FalkorDB export
# ---------------------------------------------------------------------------

def connect_falkordb():
    """Connect to FalkorDB via redis-py."""
    try:
        import redis
    except ImportError:
        log.error("redis-py not installed. Run: pip install redis")
        sys.exit(1)
    return redis.Redis(host=FALKORDB_HOST, port=FALKORDB_PORT, decode_responses=True)


def discover_graphs(r) -> list[str]:
    """Discover available graphs in FalkorDB."""
    graphs = []
    for graph_name in KNOWN_GRAPHS:
        try:
            result = r.execute_command("GRAPH.QUERY", graph_name, "MATCH (n) RETURN count(n)")
            count = result[1][0][0] if result and len(result) > 1 else 0
            log.info(f"  Graph '{graph_name}': {count} nodes")
            graphs.append(graph_name)
        except Exception as e:
            log.warning(f"  Graph '{graph_name}' not found or empty: {e}")
    return graphs


def export_nodes(r, graph_name: str) -> list[GraphNode]:
    """Export all nodes from a FalkorDB graph."""
    nodes = []
    try:
        result = r.execute_command(
            "GRAPH.QUERY", graph_name,
            "MATCH (n) RETURN id(n), labels(n), properties(n)"
        )
        if result and len(result) > 1:
            for row in result[1]:
                node_id = row[0]
                labels = row[1] if isinstance(row[1], list) else [str(row[1])]
                props = row[2] if isinstance(row[2], dict) else {}
                nodes.append(GraphNode(
                    node_id=node_id,
                    labels=labels,
                    properties=props,
                    source_graph=graph_name,
                ))
    except Exception as e:
        log.error(f"Error exporting nodes from '{graph_name}': {e}")
    return nodes


def export_edges(r, graph_name: str) -> list[GraphEdge]:
    """Export all relationships from a FalkorDB graph."""
    edges = []
    try:
        result = r.execute_command(
            "GRAPH.QUERY", graph_name,
            "MATCH (a)-[r]->(b) RETURN id(a), id(b), type(r), properties(r)"
        )
        if result and len(result) > 1:
            for row in result[1]:
                edges.append(GraphEdge(
                    src_id=row[0],
                    dst_id=row[1],
                    relation_type=str(row[2]),
                    properties=row[3] if isinstance(row[3], dict) else {},
                    source_graph=graph_name,
                ))
    except Exception as e:
        log.error(f"Error exporting edges from '{graph_name}': {e}")
    return edges


# ---------------------------------------------------------------------------
# Apache AGE import
# ---------------------------------------------------------------------------

def connect_pg():
    """Connect to PostgreSQL."""
    try:
        import psycopg2
    except ImportError:
        log.error("psycopg2 not installed. Run: pip install psycopg2-binary")
        sys.exit(1)

    if not PG_PASSWORD:
        log.error("PG_PASSWORD environment variable is required")
        sys.exit(1)

    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )


def ensure_age_extension(conn):
    """Ensure Apache AGE extension is loaded."""
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS age")
        cur.execute("LOAD 'age'")
        cur.execute("SET search_path = ag_catalog, '$user', public")
    conn.commit()


def ensure_graph(conn, graph_name: str):
    """Create an AGE graph if it doesn't exist."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM ag_catalog.ag_graph WHERE name = %s",
            (graph_name,)
        )
        if cur.fetchone()[0] == 0:
            cur.execute(f"SELECT create_graph('{graph_name}')")
            log.info(f"  Created AGE graph: {graph_name}")
        else:
            log.info(f"  AGE graph exists: {graph_name}")
    conn.commit()


def escape_cypher_value(val) -> str:
    """Escape a value for openCypher property maps."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        return str(val)
    s = str(val).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{s}'"


def props_to_cypher(props: dict) -> str:
    """Convert a properties dict to openCypher map literal."""
    if not props:
        return "{}"
    pairs = [f"{k}: {escape_cypher_value(v)}" for k, v in props.items()]
    return "{" + ", ".join(pairs) + "}"


def import_nodes(conn, graph_name: str, nodes: list[GraphNode]) -> int:
    """Import nodes into an AGE graph. Returns count imported."""
    imported = 0
    with conn.cursor() as cur:
        for node in nodes:
            label = node.labels[0] if node.labels else "Entity"
            props = {**node.properties}
            props["_falkordb_id"] = node.node_id
            props["_migrated_from"] = "falkordb"
            props["_migrated_at"] = datetime.now(timezone.utc).isoformat()
            props["_source_graph"] = node.source_graph

            cypher = (
                f"SELECT * FROM cypher('{graph_name}', $$ "
                f"CREATE (n:{label} {props_to_cypher(props)}) "
                f"RETURN id(n) $$) AS (id agtype)"
            )
            try:
                cur.execute(cypher)
                imported += 1
            except Exception as e:
                log.error(f"Error importing node {node.node_id}: {e}")
                conn.rollback()
                continue
    conn.commit()
    return imported


def import_edges(conn, graph_name: str, edges: list[GraphEdge]) -> int:
    """Import edges into an AGE graph using FalkorDB ID mapping. Returns count imported."""
    imported = 0
    with conn.cursor() as cur:
        for edge in edges:
            props = {**edge.properties}
            props["_migrated_from"] = "falkordb"
            props["_migrated_at"] = datetime.now(timezone.utc).isoformat()

            cypher = (
                f"SELECT * FROM cypher('{graph_name}', $$ "
                f"MATCH (a {{_falkordb_id: {edge.src_id}}}), "
                f"      (b {{_falkordb_id: {edge.dst_id}}}) "
                f"CREATE (a)-[r:{edge.relation_type} {props_to_cypher(props)}]->(b) "
                f"RETURN id(r) $$) AS (id agtype)"
            )
            try:
                cur.execute(cypher)
                imported += 1
            except Exception as e:
                log.error(f"Error importing edge {edge.src_id}->{edge.dst_id}: {e}")
                conn.rollback()
                continue
    conn.commit()
    return imported


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_migration(conn, graph_name: str, expected_nodes: int, expected_edges: int) -> bool:
    """Verify node and edge counts in AGE match expected values."""
    with conn.cursor() as cur:
        cur.execute("LOAD 'age'")
        cur.execute("SET search_path = ag_catalog, '$user', public")

        cur.execute(
            f"SELECT * FROM cypher('{graph_name}', $$ "
            f"MATCH (n) RETURN count(n) $$) AS (cnt agtype)"
        )
        actual_nodes = int(cur.fetchone()[0])

        cur.execute(
            f"SELECT * FROM cypher('{graph_name}', $$ "
            f"MATCH ()-[r]->() RETURN count(r) $$) AS (cnt agtype)"
        )
        actual_edges = int(cur.fetchone()[0])

    log.info(f"  Verification for '{graph_name}':")
    log.info(f"    Nodes: expected={expected_nodes}, actual={actual_nodes}")
    log.info(f"    Edges: expected={expected_edges}, actual={actual_edges}")

    if actual_nodes < expected_nodes:
        log.warning(f"    ⚠ Node count mismatch: missing {expected_nodes - actual_nodes} nodes")
        return False
    if actual_edges < expected_edges:
        log.warning(f"    ⚠ Edge count mismatch: missing {expected_edges - actual_edges} edges")
        return False

    log.info(f"    ✓ Counts match or exceed expected values")
    return True


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def run_export(dry_run: bool = False) -> tuple[dict[str, list[GraphNode]], dict[str, list[GraphEdge]], MigrationReport]:
    """Phase 1: Export from FalkorDB."""
    report = MigrationReport(started_at=datetime.now(timezone.utc).isoformat())

    log.info("=" * 60)
    log.info("FalkorDB → Apache AGE Migration")
    log.info("=" * 60)
    log.info(f"FalkorDB: {FALKORDB_HOST}:{FALKORDB_PORT}")
    log.info(f"PostgreSQL: {PG_HOST}:{PG_PORT}/{PG_DB}")
    log.info(f"Dry run: {dry_run}")
    log.info("")

    log.info("Phase 1: Connecting to FalkorDB...")
    r = connect_falkordb()
    r.ping()
    log.info("  Connected.")

    log.info("Phase 2: Discovering graphs...")
    graphs = discover_graphs(r)
    if not graphs:
        log.warning("No graphs found in FalkorDB. Nothing to migrate.")
        return {}, {}, report

    all_nodes: dict[str, list[GraphNode]] = {}
    all_edges: dict[str, list[GraphEdge]] = {}

    for graph_name in graphs:
        log.info(f"\nPhase 3: Exporting '{graph_name}'...")
        nodes = export_nodes(r, graph_name)
        edges = export_edges(r, graph_name)
        all_nodes[graph_name] = nodes
        all_edges[graph_name] = edges
        report.nodes_exported += len(nodes)
        report.edges_exported += len(edges)
        report.graphs_processed += 1
        log.info(f"  Exported: {len(nodes)} nodes, {len(edges)} edges")

    # Write export ledger for audit
    export_ledger = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": f"falkordb://{FALKORDB_HOST}:{FALKORDB_PORT}",
        "graphs": {
            name: {"nodes": len(nodes), "edges": len(all_edges.get(name, []))}
            for name, nodes in all_nodes.items()
        },
        "total_nodes": report.nodes_exported,
        "total_edges": report.edges_exported,
        "signed_by": "Devon-8da1 | devin-8da1981ce177481da3fe1d2b40e7fade",
    }
    ledger_path = os.path.join(os.path.dirname(__file__), "falkordb_export_ledger.json")
    with open(ledger_path, "w") as f:
        json.dump(export_ledger, f, indent=2)
    log.info(f"\nExport ledger written to: {ledger_path}")

    return all_nodes, all_edges, report


def run_import(
    all_nodes: dict[str, list[GraphNode]],
    all_edges: dict[str, list[GraphEdge]],
    report: MigrationReport,
) -> MigrationReport:
    """Phase 2: Import into Apache AGE."""
    log.info("\nPhase 4: Connecting to PostgreSQL...")
    conn = connect_pg()
    log.info("  Connected.")

    log.info("Phase 5: Ensuring AGE extension...")
    ensure_age_extension(conn)

    for graph_name, nodes in all_nodes.items():
        edges = all_edges.get(graph_name, [])
        log.info(f"\nPhase 6: Importing '{graph_name}'...")

        ensure_graph(conn, graph_name)

        imported_nodes = import_nodes(conn, graph_name, nodes)
        report.nodes_imported += imported_nodes
        log.info(f"  Nodes imported: {imported_nodes}/{len(nodes)}")

        imported_edges = import_edges(conn, graph_name, edges)
        report.edges_imported += imported_edges
        log.info(f"  Edges imported: {imported_edges}/{len(edges)}")

    log.info("\nPhase 7: Verification...")
    all_ok = True
    for graph_name, nodes in all_nodes.items():
        edges = all_edges.get(graph_name, [])
        ok = verify_migration(conn, graph_name, len(nodes), len(edges))
        if not ok:
            all_ok = False
            report.errors.append(f"Verification failed for graph '{graph_name}'")

    conn.close()
    report.completed_at = datetime.now(timezone.utc).isoformat()

    log.info("\n" + "=" * 60)
    log.info(report.summary())
    if all_ok:
        log.info("Migration SUCCEEDED. All graphs verified.")
    else:
        log.warning("Migration completed with WARNINGS. Check errors above.")

    return report


def run_verify_only():
    """Verify existing AGE graphs without migrating."""
    log.info("Verification mode — checking AGE graphs only")
    conn = connect_pg()
    ensure_age_extension(conn)

    r = connect_falkordb()
    r.ping()

    for graph_name in KNOWN_GRAPHS:
        try:
            result = r.execute_command(
                "GRAPH.QUERY", graph_name,
                "MATCH (n) RETURN count(n)"
            )
            expected_nodes = result[1][0][0] if result and len(result) > 1 else 0
            result = r.execute_command(
                "GRAPH.QUERY", graph_name,
                "MATCH ()-[r]->() RETURN count(r)"
            )
            expected_edges = result[1][0][0] if result and len(result) > 1 else 0
            verify_migration(conn, graph_name, expected_nodes, expected_edges)
        except Exception as e:
            log.warning(f"Could not verify graph '{graph_name}': {e}")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Migrate FalkorDB graphs to Apache AGE")
    parser.add_argument("--dry-run", action="store_true", help="Export only, do not import")
    parser.add_argument("--verify-only", action="store_true", help="Verify AGE graphs without migrating")
    args = parser.parse_args()

    if args.verify_only:
        run_verify_only()
        return

    all_nodes, all_edges, report = run_export(dry_run=args.dry_run)

    if args.dry_run:
        log.info("\nDry run complete. No data was imported.")
        log.info(report.summary())
        return

    if not all_nodes:
        log.info("Nothing to import.")
        return

    report = run_import(all_nodes, all_edges, report)

    # Write final report
    report_path = os.path.join(os.path.dirname(__file__), "falkordb_migration_report.json")
    with open(report_path, "w") as f:
        json.dump({
            "graphs_processed": report.graphs_processed,
            "nodes_exported": report.nodes_exported,
            "nodes_imported": report.nodes_imported,
            "edges_exported": report.edges_exported,
            "edges_imported": report.edges_imported,
            "errors": report.errors,
            "started_at": report.started_at,
            "completed_at": report.completed_at,
            "signed_by": "Devon-8da1 | devin-8da1981ce177481da3fe1d2b40e7fade",
        }, f, indent=2)
    log.info(f"Report written to: {report_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Amplified Brain MCP Server
===========================
MCP-compatible HTTP server for the amplified_brain Postgres database.
Read-only by default. Write mode enabled via ALLOW_WRITES=true env var.

Devon-a704 | 2026-05-07 | Brain MCP server build
Devon-a81b | 2026-05-09 | Compound Design REST endpoints + AGE graph (AMP-280)
Devon-0de2 | 2026-05-11 | AMP-302 — write tools removed, read-only enforced

Write operations retired by AMP-302. All writes go through the canonical
ingestion pipeline (v0.3). This server is read-only regardless of ALLOW_WRITES.
"""

import os
import re
import json
import logging
from contextlib import asynccontextmanager
from typing import Optional

import asyncpg
from fastapi import FastAPI, Query, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("brain-mcp")

DB_HOST = os.environ.get("DB_HOST", "cove-postgres")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "amplified_brain")
DB_USER = os.environ.get("DB_USER", "brain_reader")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
# AMP-302: writes retired. This server is read-only regardless of env.
# Legacy env var preserved for backward compat but always evaluates False.
ALLOW_WRITES = False
SERVER_PORT = int(os.environ.get("SERVER_PORT", "8080"))

pool: asyncpg.Pool = None

WRITE_PREFIXES = ("INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "TRUNCATE", "GRANT", "REVOKE")

TOOLS = [
    {
        "name": "list_tables",
        "description": "List all tables in the amplified_brain database with row counts.",
        "inputSchema": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "describe_table",
        "description": "Show columns, types, and constraints for a specific table.",
        "inputSchema": {
            "type": "object",
            "properties": {"table_name": {"type": "string", "description": "Name of the table to describe"}},
            "required": ["table_name"]
        }
    },
    {
        "name": "search_knowledge",
        "description": "Semantic search across knowledge vectors. Returns matching content chunks with metadata.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query_text": {"type": "string", "description": "Search query text"},
                "limit": {"type": "integer", "description": "Max results (default 10)", "default": 10}
            },
            "required": ["query_text"]
        }
    },
    {
        "name": "get_entity",
        "description": "Look up an entity by name (fuzzy match). Returns entity details and relationships.",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Entity name to search for"}},
            "required": ["name"]
        }
    },
    {
        "name": "query_entities",
        "description": "List entities, optionally filtered by type.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "description": "Filter by entity type (optional)"},
                "limit": {"type": "integer", "description": "Max results (default 25)", "default": 25}
            },
            "required": []
        }
    },
    {
        "name": "query_relationships",
        "description": "Query relationships between entities.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "entity_name": {"type": "string", "description": "Filter by entity name (source or target)"},
                "relation_type": {"type": "string", "description": "Filter by relation type"},
                "limit": {"type": "integer", "description": "Max results (default 25)", "default": 25}
            },
            "required": []
        }
    },
    {
        "name": "get_episodes",
        "description": "List recent episodes (events/interactions) with optional text search.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "search": {"type": "string", "description": "Text search filter (optional)"},
                "limit": {"type": "integer", "description": "Max results (default 20)", "default": 20}
            },
            "required": []
        }
    },
    {
        "name": "run_query",
        "description": "Run a read-only SQL query against the database. SELECT only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "SQL SELECT query to execute"},
                "params": {"type": "array", "description": "Query parameters (optional)", "items": {}}
            },
            "required": ["sql"]
        }
    },
]

# AMP-302: Write tools removed. All writes go through the canonical pipeline.
WRITE_TOOLS = []


async def _init_age_connection(conn):
    """Per-connection init: load AGE extension and set search_path."""
    try:
        await conn.execute("LOAD 'age'")
        await conn.execute('SET search_path = ag_catalog, "$user", public')
    except Exception as e:
        logger.warning(f"AGE init skipped (extension may not be installed): {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    dsn = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    pool = await asyncpg.create_pool(dsn, min_size=2, max_size=10, init=_init_age_connection)
    logger.info(f"Connected to {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME} (writes={'enabled' if ALLOW_WRITES else 'disabled'})")
    yield
    await pool.close()


app = FastAPI(title="Amplified Brain MCP", lifespan=lifespan)

# MCP state
sessions = {}
msg_counter = 0


def next_id():
    global msg_counter
    msg_counter += 1
    return msg_counter


def all_tools():
    tools = list(TOOLS)
    if ALLOW_WRITES:
        tools.extend(WRITE_TOOLS)
    return tools


def make_result(id, result):
    return {"jsonrpc": "2.0", "id": id, "result": result}


def make_error(id, code, message):
    return {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}


async def handle_list_tables(args):
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT t.table_name, 
                   (xpath('/row/cnt/text()', xml_count))[1]::text::int as row_count
            FROM information_schema.tables t
            LEFT JOIN LATERAL (
                SELECT query_to_xml('SELECT count(*) as cnt FROM ' || quote_ident(t.table_name), false, true, '')
            ) x(xml_count) ON true
            WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name
        """)
        result = [{"table": r["table_name"], "rows": r["row_count"]} for r in rows]
        return [{"type": "text", "text": json.dumps(result, indent=2)}]


async def handle_describe_table(args):
    table_name = args.get("table_name", "")
    if not table_name.isidentifier():
        return [{"type": "text", "text": f"Invalid table name: {table_name}"}]
    async with pool.acquire() as conn:
        cols = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            ORDER BY ordinal_position
        """, table_name)
        if not cols:
            return [{"type": "text", "text": f"Table '{table_name}' not found"}]
        result = [{"column": c["column_name"], "type": c["data_type"], 
                    "nullable": c["is_nullable"], "default": c["column_default"]} for c in cols]
        return [{"type": "text", "text": json.dumps(result, indent=2)}]


async def handle_search_knowledge(args):
    query_text = args.get("query_text", "")
    limit = min(args.get("limit", 10), 100)
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, content, source, source_type, metadata, created_at::text
            FROM knowledge_vectors
            WHERE content ILIKE '%' || $1 || '%'
            ORDER BY created_at DESC
            LIMIT $2
        """, query_text, limit)
        result = [{"id": str(r["id"]), "content": r["content"][:500], "source": r["source"],
                    "source_type": r["source_type"], "metadata": json.loads(r["metadata"]) if r["metadata"] else None,
                    "created_at": r["created_at"]} for r in rows]
        return [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]


async def handle_get_entity(args):
    name = args.get("name", "")
    async with pool.acquire() as conn:
        entity = await conn.fetchrow("""
            SELECT id, name, entity_type, summary, properties, created_at::text, updated_at::text
            FROM entities WHERE name ILIKE '%' || $1 || '%' LIMIT 1
        """, name)
        if not entity:
            return [{"type": "text", "text": f"No entity found matching '{name}'"}]
        rels = await conn.fetch("""
            SELECT r.relation_type, r.summary, r.weight,
                   s.name as source_name, t.name as target_name
            FROM relationships r
            JOIN entities s ON r.source_id = s.id
            JOIN entities t ON r.target_id = t.id
            WHERE r.source_id = $1 OR r.target_id = $1
            LIMIT 50
        """, entity["id"])
        result = {
            "entity": {"id": str(entity["id"]), "name": entity["name"], "type": entity["entity_type"],
                        "summary": entity["summary"], "properties": json.loads(entity["properties"]) if entity["properties"] else None},
            "relationships": [{"type": r["relation_type"], "summary": r["summary"], "weight": float(r["weight"]) if r["weight"] else None,
                               "source": r["source_name"], "target": r["target_name"]} for r in rels]
        }
        return [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]


async def handle_query_entities(args):
    entity_type = args.get("entity_type")
    limit = min(args.get("limit", 25), 200)
    async with pool.acquire() as conn:
        if entity_type:
            rows = await conn.fetch("""
                SELECT id, name, entity_type, summary, created_at::text
                FROM entities WHERE entity_type ILIKE $1
                ORDER BY updated_at DESC LIMIT $2
            """, entity_type, limit)
        else:
            rows = await conn.fetch("""
                SELECT id, name, entity_type, summary, created_at::text
                FROM entities ORDER BY updated_at DESC LIMIT $1
            """, limit)
        result = [{"id": str(r["id"]), "name": r["name"], "type": r["entity_type"],
                    "summary": r["summary"], "created_at": r["created_at"]} for r in rows]
        return [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]


async def handle_query_relationships(args):
    entity_name = args.get("entity_name")
    relation_type = args.get("relation_type")
    limit = min(args.get("limit", 25), 200)
    async with pool.acquire() as conn:
        query = """
            SELECT r.relation_type, r.summary, r.weight,
                   s.name as source_name, t.name as target_name, r.created_at::text
            FROM relationships r
            JOIN entities s ON r.source_id = s.id
            JOIN entities t ON r.target_id = t.id
            WHERE 1=1
        """
        params = []
        idx = 1
        if entity_name:
            query += f" AND (s.name ILIKE '%' || ${idx} || '%' OR t.name ILIKE '%' || ${idx} || '%')"
            params.append(entity_name)
            idx += 1
        if relation_type:
            query += f" AND r.relation_type ILIKE ${idx}"
            params.append(relation_type)
            idx += 1
        query += f" ORDER BY r.created_at DESC LIMIT ${idx}"
        params.append(limit)
        rows = await conn.fetch(query, *params)
        result = [{"type": r["relation_type"], "summary": r["summary"], "weight": float(r["weight"]) if r["weight"] else None,
                    "source": r["source_name"], "target": r["target_name"], "created_at": r["created_at"]} for r in rows]
        return [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]


async def handle_get_episodes(args):
    search = args.get("search")
    limit = min(args.get("limit", 20), 100)
    async with pool.acquire() as conn:
        if search:
            rows = await conn.fetch("""
                SELECT id, name, content, source, created_at::text
                FROM episodes WHERE content ILIKE '%' || $1 || '%'
                ORDER BY created_at DESC LIMIT $2
            """, search, limit)
        else:
            rows = await conn.fetch("""
                SELECT id, name, content, source, created_at::text
                FROM episodes ORDER BY created_at DESC LIMIT $1
            """, limit)
        result = [{"id": str(r["id"]), "name": r["name"], "content": r["content"][:500],
                    "source": r["source"], "created_at": r["created_at"]} for r in rows]
        return [{"type": "text", "text": json.dumps(result, indent=2, default=str)}]


async def handle_run_query(args):
    sql = args.get("sql", "").strip()
    params = args.get("params", [])
    upper = sql.upper().lstrip()
    if any(upper.startswith(p) for p in WRITE_PREFIXES):
        return [{"type": "text", "text": "Error: Only SELECT queries allowed via run_query. Use run_write_query for writes."}]
    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(sql, *params)
            result = [dict(r) for r in rows]
            return [{"type": "text", "text": json.dumps(result[:100], indent=2, default=str)}]
        except Exception as e:
            return [{"type": "text", "text": f"Query error: {e}"}]


async def handle_insert_knowledge(args):
    if not ALLOW_WRITES:
        return [{"type": "text", "text": "Error: Write operations disabled on this endpoint."}]
    content = args["content"]
    source = args["source"]
    metadata = json.dumps(args.get("metadata", {}))
    embedding = args.get("embedding")
    async with pool.acquire() as conn:
        if embedding:
            vec_str = "[" + ",".join(str(f) for f in embedding) + "]"
            row = await conn.fetchrow("""
                INSERT INTO knowledge_vectors (content, source, embedding, metadata)
                VALUES ($1, $2, $3::vector, $4::jsonb)
                RETURNING id::text
            """, content, source, vec_str, metadata)
        else:
            row = await conn.fetchrow("""
                INSERT INTO knowledge_vectors (content, source, metadata)
                VALUES ($1, $2, $3::jsonb)
                RETURNING id::text
            """, content, source, metadata)
        return [{"type": "text", "text": json.dumps({"inserted": True, "id": row["id"]})}]


async def handle_insert_entity(args):
    if not ALLOW_WRITES:
        return [{"type": "text", "text": "Error: Write operations disabled on this endpoint."}]
    name = args["name"]
    entity_type = args["entity_type"]
    summary = args.get("summary", "")
    properties = json.dumps(args.get("properties", {}))
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT id FROM entities WHERE name = $1 AND entity_type = $2 LIMIT 1",
            name, entity_type)
        if existing:
            await conn.execute("""
                UPDATE entities SET summary = $1, properties = $2::jsonb, updated_at = now()
                WHERE id = $3
            """, summary, properties, existing["id"])
            return [{"type": "text", "text": json.dumps({"upserted": True, "id": str(existing["id"])})}]
        else:
            row = await conn.fetchrow("""
                INSERT INTO entities (name, entity_type, summary, properties)
                VALUES ($1, $2, $3, $4::jsonb)
                RETURNING id::text
            """, name, entity_type, summary, properties)
            return [{"type": "text", "text": json.dumps({"upserted": True, "id": row["id"]})}]


async def handle_insert_relationship(args):
    if not ALLOW_WRITES:
        return [{"type": "text", "text": "Error: Write operations disabled on this endpoint."}]
    source_name = args["source_name"]
    target_name = args["target_name"]
    relation_type = args["relation_type"]
    summary = args.get("summary", "")
    weight = args.get("weight", 1.0)
    async with pool.acquire() as conn:
        source = await conn.fetchrow("SELECT id FROM entities WHERE name = $1 LIMIT 1", source_name)
        target = await conn.fetchrow("SELECT id FROM entities WHERE name = $1 LIMIT 1", target_name)
        if not source:
            return [{"type": "text", "text": f"Source entity '{source_name}' not found"}]
        if not target:
            return [{"type": "text", "text": f"Target entity '{target_name}' not found"}]
        row = await conn.fetchrow("""
            INSERT INTO relationships (source_id, target_id, relation_type, summary, weight)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id::text
        """, source["id"], target["id"], relation_type, summary, weight)
        return [{"type": "text", "text": json.dumps({"inserted": True, "id": row["id"]})}]


async def handle_run_write_query(args):
    if not ALLOW_WRITES:
        return [{"type": "text", "text": "Error: Write operations disabled on this endpoint."}]
    sql = args.get("sql", "").strip()
    params = args.get("params", [])
    async with pool.acquire() as conn:
        try:
            result = await conn.execute(sql, *params)
            return [{"type": "text", "text": json.dumps({"executed": True, "result": result})}]
        except Exception as e:
            return [{"type": "text", "text": f"Write error: {e}"}]


HANDLERS = {
    "list_tables": handle_list_tables,
    "describe_table": handle_describe_table,
    "search_knowledge": handle_search_knowledge,
    "get_entity": handle_get_entity,
    "query_entities": handle_query_entities,
    "query_relationships": handle_query_relationships,
    "get_episodes": handle_get_episodes,
    "run_query": handle_run_query,
    # AMP-302: write handlers removed — canonical pipeline is the only write path
}


async def process_message(msg: dict) -> dict:
    method = msg.get("method", "")
    id = msg.get("id")
    params = msg.get("params", {})

    if method == "initialize":
        return make_result(id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {
                "name": "amplified-brain-mcp",
                "version": "1.0.0"
            }
        })
    elif method == "notifications/initialized":
        return None
    elif method == "tools/list":
        return make_result(id, {"tools": all_tools()})
    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        handler = HANDLERS.get(tool_name)
        if not handler:
            return make_error(id, -32602, f"Unknown tool: {tool_name}")
        try:
            content = await handler(arguments)
            return make_result(id, {"content": content, "isError": False})
        except Exception as e:
            logger.exception(f"Tool error: {tool_name}")
            return make_result(id, {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True})
    elif method == "ping":
        return make_result(id, {})
    else:
        return make_error(id, -32601, f"Method not found: {method}")


# --- HTTP Endpoints ---

@app.get("/health")
async def health():
    try:
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {"status": "ok", "server": "amplified-brain-mcp", "version": "1.0.0",
                "database": DB_NAME, "writes": ALLOW_WRITES}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=503)


@app.post("/mcp")
async def mcp_post(request: Request):
    """Streamable HTTP transport — POST JSON-RPC messages."""
    body = await request.json()
    if isinstance(body, list):
        results = []
        for msg in body:
            r = await process_message(msg)
            if r:
                results.append(r)
        return JSONResponse(results)
    else:
        result = await process_message(body)
        if result is None:
            return Response(status_code=204)
        return JSONResponse(result)


@app.get("/sse")
async def mcp_sse(request: Request):
    """SSE transport — for clients that prefer Server-Sent Events."""
    import asyncio
    import uuid
    session_id = str(uuid.uuid4())
    message_url = f"/sse/message?session={session_id}"
    sessions[session_id] = asyncio.Queue()

    async def event_generator():
        yield {"event": "endpoint", "data": message_url}
        queue = sessions[session_id]
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    msg = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield {"event": "message", "data": json.dumps(msg)}
                except asyncio.TimeoutError:
                    yield {"event": "ping", "data": ""}
        finally:
            sessions.pop(session_id, None)

    return EventSourceResponse(event_generator())


@app.post("/sse/message")
async def mcp_sse_message(request: Request):
    """SSE transport — receive client messages."""
    session_id = request.query_params.get("session")
    if not session_id or session_id not in sessions:
        return JSONResponse({"error": "Invalid session"}, status_code=400)
    body = await request.json()
    result = await process_message(body)
    if result:
        await sessions[session_id].put(result)
    return Response(status_code=202)


# ─── Compound Design REST Endpoints (AMP-280) ─────────────────────────────────
# POST endpoints require ALLOW_WRITES=true (writer :8091)
# GET endpoints work on both reader (:8090) and writer (:8091)


class ArtifactCreate(BaseModel):
    name: str
    artifact_type: str
    phase: str
    description: Optional[str] = None
    content: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    embedding: Optional[list[float]] = None
    source: Optional[str] = "plugin:compound-design"


class PatternCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    rationale: Optional[str] = None
    constraints: dict = Field(default_factory=dict)
    examples: list = Field(default_factory=list)
    embedding: Optional[list[float]] = None
    source: Optional[str] = "plugin:compound-design"


class ResearchCreate(BaseModel):
    title: str
    domain: str
    summary: str
    evidence: dict = Field(default_factory=dict)
    confidence: Optional[float] = None
    embedding: Optional[list[float]] = None
    source: Optional[str] = "plugin:compound-design"


class PuddingCreate(BaseModel):
    name: str
    bridge_a: str
    bridge_b: str
    mechanism: Optional[str] = None
    pudding_score: Optional[float] = None
    domain_distance: Optional[float] = None
    confidence_band: Optional[str] = None
    embedding: Optional[list[float]] = None
    source: Optional[str] = "plugin:compound-design"


class GraphEdgeCreate(BaseModel):
    source_id: str
    source_label: str  # 'Artifact' | 'Pattern' | 'Research' | 'Pudding' | 'Concept'
    target_id: str
    target_label: str
    edge_type: str     # 'INFORMS' | 'DERIVES_FROM' | 'CONTRADICTS' | 'BRIDGES_TO' | 'VALIDATED_BY'
    properties: dict = Field(default_factory=dict)


def _vec_literal(embedding: list[float]) -> str:
    return "[" + ",".join(str(f) for f in embedding) + "]"


_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)
_VALID_LABELS = {"Artifact", "Pattern", "Research", "Pudding", "Concept"}
_VALID_EDGES = {"INFORMS", "DERIVES_FROM", "CONTRADICTS", "BRIDGES_TO", "VALIDATED_BY"}


# ─── POST Endpoints (Writer) ──────────────────────────────────────────────────


@app.post("/design/artifacts")
async def create_artifact(body: ArtifactCreate):
    if not ALLOW_WRITES:
        return JSONResponse({"error": "Write operations disabled"}, status_code=403)
    async with pool.acquire() as conn:
        if body.embedding:
            row = await conn.fetchrow("""
                INSERT INTO design_artifacts (name, artifact_type, phase, description, content, tags, embedding, source)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7::vector, $8)
                RETURNING id::text, created_at::text
            """, body.name, body.artifact_type, body.phase, body.description,
                json.dumps(body.content), body.tags, _vec_literal(body.embedding), body.source)
        else:
            row = await conn.fetchrow("""
                INSERT INTO design_artifacts (name, artifact_type, phase, description, content, tags, source)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7)
                RETURNING id::text, created_at::text
            """, body.name, body.artifact_type, body.phase, body.description,
                json.dumps(body.content), body.tags, body.source)
        return {"id": row["id"], "created_at": row["created_at"]}


@app.post("/design/patterns")
async def create_pattern(body: PatternCreate):
    if not ALLOW_WRITES:
        return JSONResponse({"error": "Write operations disabled"}, status_code=403)
    async with pool.acquire() as conn:
        if body.embedding:
            row = await conn.fetchrow("""
                INSERT INTO design_patterns (name, category, description, rationale, constraints, examples, embedding, source)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb, $7::vector, $8)
                RETURNING id::text, created_at::text
            """, body.name, body.category, body.description, body.rationale,
                json.dumps(body.constraints), json.dumps(body.examples),
                _vec_literal(body.embedding), body.source)
        else:
            row = await conn.fetchrow("""
                INSERT INTO design_patterns (name, category, description, rationale, constraints, examples, source)
                VALUES ($1, $2, $3, $4, $5::jsonb, $6::jsonb, $7)
                RETURNING id::text, created_at::text
            """, body.name, body.category, body.description, body.rationale,
                json.dumps(body.constraints), json.dumps(body.examples), body.source)
        return {"id": row["id"], "created_at": row["created_at"]}


@app.post("/design/research")
async def create_research(body: ResearchCreate):
    if not ALLOW_WRITES:
        return JSONResponse({"error": "Write operations disabled"}, status_code=403)
    async with pool.acquire() as conn:
        if body.embedding:
            row = await conn.fetchrow("""
                INSERT INTO research_findings (title, domain, summary, evidence, confidence, embedding, source)
                VALUES ($1, $2, $3, $4::jsonb, $5, $6::vector, $7)
                RETURNING id::text, created_at::text
            """, body.title, body.domain, body.summary, json.dumps(body.evidence),
                body.confidence, _vec_literal(body.embedding), body.source)
        else:
            row = await conn.fetchrow("""
                INSERT INTO research_findings (title, domain, summary, evidence, confidence, source)
                VALUES ($1, $2, $3, $4::jsonb, $5, $6)
                RETURNING id::text, created_at::text
            """, body.title, body.domain, body.summary, json.dumps(body.evidence),
                body.confidence, body.source)
        return {"id": row["id"], "created_at": row["created_at"]}


@app.post("/design/pudding")
async def create_pudding(body: PuddingCreate):
    if not ALLOW_WRITES:
        return JSONResponse({"error": "Write operations disabled"}, status_code=403)
    async with pool.acquire() as conn:
        if body.embedding:
            row = await conn.fetchrow("""
                INSERT INTO pudding_concepts (name, bridge_a, bridge_b, mechanism, pudding_score,
                    domain_distance, confidence_band, embedding, source)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8::vector, $9)
                RETURNING id::text, created_at::text
            """, body.name, body.bridge_a, body.bridge_b, body.mechanism,
                body.pudding_score, body.domain_distance, body.confidence_band,
                _vec_literal(body.embedding), body.source)
        else:
            row = await conn.fetchrow("""
                INSERT INTO pudding_concepts (name, bridge_a, bridge_b, mechanism, pudding_score,
                    domain_distance, confidence_band, source)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id::text, created_at::text
            """, body.name, body.bridge_a, body.bridge_b, body.mechanism,
                body.pudding_score, body.domain_distance, body.confidence_band, body.source)
        return {"id": row["id"], "created_at": row["created_at"]}


@app.post("/design/graph/edge")
async def create_graph_edge(body: GraphEdgeCreate):
    if not ALLOW_WRITES:
        return JSONResponse({"error": "Write operations disabled"}, status_code=403)
    if body.source_label not in _VALID_LABELS or body.target_label not in _VALID_LABELS:
        return JSONResponse({"error": f"Invalid label. Valid: {_VALID_LABELS}"}, status_code=400)
    if body.edge_type not in _VALID_EDGES:
        return JSONResponse({"error": f"Invalid edge_type. Valid: {_VALID_EDGES}"}, status_code=400)
    if not _UUID_RE.match(body.source_id):
        return JSONResponse({"error": "source_id must be a valid UUID"}, status_code=400)
    if not _UUID_RE.match(body.target_id):
        return JSONResponse({"error": "target_id must be a valid UUID"}, status_code=400)
    props_str = json.dumps(body.properties).replace("'", "\\'") if body.properties else "{}"
    cypher = (
        f"SELECT * FROM cypher('compound_design', $$ "
        f"MATCH (a:{body.source_label} {{id: '{body.source_id}'}}), "
        f"(b:{body.target_label} {{id: '{body.target_id}'}}) "
        f"CREATE (a)-[e:{body.edge_type} {{properties: '{props_str}'}}]->(b) "
        f"RETURN e "
        f"$$) AS (e agtype)"
    )
    async with pool.acquire() as conn:
        try:
            await conn.execute(cypher)
            return {"created": True, "edge_type": body.edge_type,
                    "source": body.source_id, "target": body.target_id}
        except Exception as e:
            return JSONResponse({"error": f"Graph edge creation failed: {e}"}, status_code=500)


# ─── GET Endpoints (Reader) ───────────────────────────────────────────────────


@app.get("/design/recall")
async def design_recall(
    query_embedding: str = Query(None, description="JSON array of 384 floats"),
    phase: Optional[str] = Query(None),
    artifact_type: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
):
    """Semantic recall across design artifacts using pgvector cosine distance."""
    if not query_embedding:
        return JSONResponse({"error": "query_embedding required (JSON array of 384 floats)"}, status_code=400)
    try:
        vec = json.loads(query_embedding)
        if len(vec) != 384:
            return JSONResponse({"error": f"Embedding must be 384 dimensions, got {len(vec)}"}, status_code=400)
    except (json.JSONDecodeError, TypeError):
        return JSONResponse({"error": "query_embedding must be valid JSON array"}, status_code=400)
    vec_str = _vec_literal(vec)
    filters = []
    params = [vec_str, limit]
    idx = 3
    if phase:
        filters.append(f"phase = ${idx}")
        params.append(phase)
        idx += 1
    if artifact_type:
        filters.append(f"artifact_type = ${idx}")
        params.append(artifact_type)
        idx += 1
    where = (" AND " + " AND ".join(filters)) if filters else ""
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"""
            SELECT id::text, name, artifact_type, phase, description,
                   content::text, tags, source, created_at::text,
                   embedding <=> $1::vector AS distance
            FROM design_artifacts
            WHERE embedding IS NOT NULL{where}
            ORDER BY embedding <=> $1::vector
            LIMIT $2
        """, *params)
        results = [{"id": r["id"], "name": r["name"], "artifact_type": r["artifact_type"],
                    "phase": r["phase"], "description": r["description"],
                    "content": json.loads(r["content"]) if r["content"] else {},
                    "tags": r["tags"], "source": r["source"],
                    "distance": float(r["distance"]), "created_at": r["created_at"]} for r in rows]
        return {"results": results, "count": len(results)}


@app.get("/design/patterns")
async def list_patterns(
    category: Optional[str] = Query(None),
    limit: int = Query(25, ge=1, le=200),
):
    """List design patterns, optionally filtered by category."""
    async with pool.acquire() as conn:
        if category:
            rows = await conn.fetch("""
                SELECT id::text, name, category, description, rationale,
                       constraints::text, examples::text, source, created_at::text
                FROM design_patterns WHERE category = $1
                ORDER BY updated_at DESC LIMIT $2
            """, category, limit)
        else:
            rows = await conn.fetch("""
                SELECT id::text, name, category, description, rationale,
                       constraints::text, examples::text, source, created_at::text
                FROM design_patterns
                ORDER BY updated_at DESC LIMIT $1
            """, limit)
        results = [{"id": r["id"], "name": r["name"], "category": r["category"],
                    "description": r["description"], "rationale": r["rationale"],
                    "constraints": json.loads(r["constraints"]) if r["constraints"] else {},
                    "examples": json.loads(r["examples"]) if r["examples"] else [],
                    "source": r["source"], "created_at": r["created_at"]} for r in rows]
        return {"results": results, "count": len(results)}


@app.get("/design/research")
async def list_research(
    domain: Optional[str] = Query(None),
    limit: int = Query(25, ge=1, le=200),
):
    """List research findings, optionally filtered by domain."""
    async with pool.acquire() as conn:
        if domain:
            rows = await conn.fetch("""
                SELECT id::text, title, domain, summary, evidence::text,
                       confidence, source, created_at::text
                FROM research_findings WHERE domain = $1
                ORDER BY updated_at DESC LIMIT $2
            """, domain, limit)
        else:
            rows = await conn.fetch("""
                SELECT id::text, title, domain, summary, evidence::text,
                       confidence, source, created_at::text
                FROM research_findings
                ORDER BY updated_at DESC LIMIT $1
            """, limit)
        results = [{"id": r["id"], "title": r["title"], "domain": r["domain"],
                    "summary": r["summary"],
                    "evidence": json.loads(r["evidence"]) if r["evidence"] else {},
                    "confidence": float(r["confidence"]) if r["confidence"] else None,
                    "source": r["source"], "created_at": r["created_at"]} for r in rows]
        return {"results": results, "count": len(results)}


@app.get("/design/graph/traverse")
async def graph_traverse(
    start_id: str = Query(..., description="Starting node ID (UUID)"),
    start_label: str = Query(..., description="Starting node label (Artifact|Pattern|Research|Pudding|Concept)"),
    edge_type: Optional[str] = Query(None, description="Filter by edge type"),
    depth: int = Query(2, ge=1, le=5),
):
    """Traverse the compound_design graph from a starting node."""
    if start_label not in _VALID_LABELS:
        return JSONResponse({"error": f"Invalid start_label. Valid: {_VALID_LABELS}"}, status_code=400)
    if not _UUID_RE.match(start_id):
        return JSONResponse({"error": "start_id must be a valid UUID"}, status_code=400)
    if edge_type and edge_type not in _VALID_EDGES:
        return JSONResponse({"error": f"Invalid edge_type. Valid: {_VALID_EDGES}"}, status_code=400)
    edge_filter = f":{edge_type}" if edge_type else ""
    cypher = (
        f"SELECT * FROM cypher('compound_design', $$ "
        f"MATCH (a:{start_label} {{id: '{start_id}'}})-[e{edge_filter}*1..{depth}]->(b) "
        f"RETURN b, e "
        f"$$) AS (node agtype, edges agtype)"
    )
    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(cypher)
            results = [{"node": str(r["node"]), "edges": str(r["edges"])} for r in rows]
            return {"results": results, "count": len(results), "start": start_id, "depth": depth}
        except Exception as e:
            return JSONResponse({"error": f"Graph traversal failed: {e}"}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting Amplified Brain MCP server on port {SERVER_PORT}")
    logger.info(f"Database: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    logger.info(f"Write access: {'ENABLED' if ALLOW_WRITES else 'DISABLED'}")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT, log_level="info")

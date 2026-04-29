"""
Amplified Knowledge MCP Server — tiered access to FalkorDB + Qdrant.

Three tiers:
  - Tier 1 (READONLY):   query, search, browse. Cannot write.
  - Tier 2 (READWRITE):  Tier 1 + ingest, update, tag, flag. Cannot delete.
  - Tier 3 (ADMIN):      Tier 1 + 2 + archive, promote, audit log.

FalkorDB knowledge graph and Qdrant vector embeddings built by Clawd (OpenClaw).

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from . import audit, config, embedder, falkordb_client, qdrant_client, security

# ---------------------------------------------------------------------------
# Server setup
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "Amplified Knowledge",
    instructions=(
        "Tiered MCP server for Amplified Partners knowledge systems. "
        f"Current tier: {config.TIER.value}. "
        "FalkorDB (graph) + Qdrant (vectors). "
        "Knowledge graph and embeddings built by Clawd (OpenClaw)."
    ),
)

audit.setup_logging()


# ===================================================================
# TIER 1 — READ-ONLY (always available)
# ===================================================================


@mcp.tool()
def query_graph(graph_name: str, cypher_query: str) -> str:
    """Run a read-only Cypher query against a FalkorDB graph.

    Available graphs: business_knowledge, amplified, amplified_brain, amplified_graph.
    Only read operations (MATCH, RETURN, CALL, etc.) are permitted.
    Write operations (CREATE, SET, DELETE, MERGE, REMOVE) are rejected.

    Args:
        graph_name: Name of the FalkorDB graph to query.
        cypher_query: A valid read-only Cypher query string.
    """
    error = security.validate_cypher(cypher_query, config.TIER)
    if error:
        audit.log_operation("query_graph:REJECTED", graph_name, error)
        return json.dumps({"error": error})

    audit.log_operation("query_graph", graph_name, cypher_query[:200])
    result = falkordb_client.graph_query(graph_name, cypher_query)
    return json.dumps(result, default=str)


@mcp.tool()
def search_knowledge(query_text: str, limit: int = 5) -> str:
    """Semantic search across the amplified_knowledge Qdrant collection (57,434 embedded chunks).

    Embeds the query using all-MiniLM-L6-v2 (384-dim) and returns the most
    semantically similar document chunks with metadata (file_path, category,
    text, chunk_index).

    Args:
        query_text: Natural language search query.
        limit: Maximum number of results to return (default 5, max 20).
    """
    limit = min(max(limit, 1), 20)
    audit.log_operation("search_knowledge", "amplified_knowledge", query_text[:200])

    vector = embedder.embed_text(query_text)
    results = qdrant_client.search_vectors(
        collection="amplified_knowledge",
        query_vector=vector,
        limit=limit,
    )
    return json.dumps(results, default=str)


@mcp.tool()
def get_document(document_title: str) -> str:
    """Retrieve a specific Document node from the business_knowledge graph by title.

    Returns full document properties: filepath, title, filename, category,
    source, date, word_count, preview, ingested_at.

    Args:
        document_title: Title (or partial title) of the document to find.
    """
    audit.log_operation("get_document", "business_knowledge", document_title)

    cypher = (
        "MATCH (d:Document) "
        "WHERE toLower(d.title) CONTAINS toLower($title) "
        "RETURN d LIMIT 5"
    )
    # FalkorDB doesn't support $params in GRAPH.QUERY the same way;
    # use string interpolation with sanitised input.
    safe_title = document_title.replace("'", "\\'")
    cypher = (
        f"MATCH (d:Document) "
        f"WHERE toLower(d.title) CONTAINS toLower('{safe_title}') "
        f"RETURN d LIMIT 5"
    )
    result = falkordb_client.graph_query("business_knowledge", cypher)
    return json.dumps(result, default=str)


@mcp.tool()
def list_entities(category: str = "") -> str:
    """Browse Entity nodes in the business_knowledge graph.

    Args:
        category: Optional category filter. If empty, returns all entities (limited to 50).
    """
    audit.log_operation("list_entities", "business_knowledge", category)

    if category:
        safe_cat = category.replace("'", "\\'")
        cypher = (
            f"MATCH (e:Entity)-[:BELONGS_TO]->(c:Category) "
            f"WHERE toLower(c.name) CONTAINS toLower('{safe_cat}') "
            f"RETURN e.name, labels(e) LIMIT 50"
        )
    else:
        cypher = "MATCH (e:Entity) RETURN e.name, labels(e) LIMIT 50"

    result = falkordb_client.graph_query("business_knowledge", cypher)
    return json.dumps(result, default=str)


@mcp.tool()
def search_principles(keyword: str) -> str:
    """Find canonical principle documents by keyword.

    Searches both the FalkorDB graph (Document nodes in principles-related
    categories) and Qdrant semantic search for principle-related content.

    Args:
        keyword: Keyword or phrase to search for in principles.
    """
    audit.log_operation("search_principles", "business_knowledge+qdrant", keyword)

    # Graph search
    safe_kw = keyword.replace("'", "\\'")
    cypher = (
        f"MATCH (d:Document) "
        f"WHERE (toLower(d.title) CONTAINS toLower('{safe_kw}') "
        f"OR toLower(d.category) CONTAINS 'principle') "
        f"AND (toLower(d.title) CONTAINS toLower('{safe_kw}') "
        f"OR toLower(d.preview) CONTAINS toLower('{safe_kw}')) "
        f"RETURN d.title, d.category, d.preview, d.date LIMIT 10"
    )
    graph_results = falkordb_client.graph_query("business_knowledge", cypher)

    # Semantic search
    vector = embedder.embed_text(f"principle: {keyword}")
    semantic_results = qdrant_client.search_vectors(
        collection="amplified_knowledge",
        query_vector=vector,
        limit=5,
        category_filter="15-principles-library",
    )

    return json.dumps(
        {"graph_results": graph_results, "semantic_results": semantic_results},
        default=str,
    )


@mcp.tool()
def get_chronology(topic: str) -> str:
    """Return documents mentioning a topic, ordered by date.

    Shows the evolution of thinking on a topic over time.

    Args:
        topic: Topic to trace chronologically.
    """
    audit.log_operation("get_chronology", "business_knowledge", topic)

    safe_topic = topic.replace("'", "\\'")
    cypher = (
        f"MATCH (d:Document) "
        f"WHERE toLower(d.title) CONTAINS toLower('{safe_topic}') "
        f"OR toLower(d.preview) CONTAINS toLower('{safe_topic}') "
        f"RETURN d.title, d.date, d.category, d.preview "
        f"ORDER BY d.date ASC LIMIT 30"
    )
    result = falkordb_client.graph_query("business_knowledge", cypher)
    return json.dumps(result, default=str)


@mcp.tool()
def list_collections() -> str:
    """List available Qdrant collections and their stats.

    Returns collection name, point count, vector dimensions, and status.
    """
    audit.log_operation("list_collections", "qdrant", "")
    result = qdrant_client.list_collections()
    return json.dumps(result, default=str)


@mcp.tool()
def filter_by_category(category: str, limit: int = 10) -> str:
    """Browse Qdrant points filtered by vault category.

    Categories include: 01-business-strategy, 02-technical-architecture,
    04-products, 06-brand-and-marketing, 13-monologue-transcripts,
    14-voice-captures, 15-principles-library, and more.

    Args:
        category: Vault category to filter by (e.g. "01-business-strategy").
        limit: Maximum number of results (default 10, max 50).
    """
    limit = min(max(limit, 1), 50)
    audit.log_operation("filter_by_category", "amplified_knowledge", category)

    result = qdrant_client.scroll_points(
        collection="amplified_knowledge",
        limit=limit,
        category_filter=category,
    )
    return json.dumps(result, default=str)


# ===================================================================
# TIER 2 — READ-WRITE (available when TIER=readwrite or admin)
# ===================================================================

if config.TIER in (config.Tier.READWRITE, config.Tier.ADMIN):

    @mcp.tool()
    def ingest_document(content: str, title: str, category: str, source: str = "") -> str:
        """Add a new document to both FalkorDB (as Document node) and Qdrant (as embedded chunks).

        Creates a Document node in business_knowledge graph and embeds the content
        into the amplified_knowledge Qdrant collection.

        Args:
            content: Full document text content.
            title: Document title.
            category: Vault category (e.g. "01-business-strategy").
            source: Source attribution (e.g. "ewan-dictation", "devon-research").
        """
        audit.log_operation("ingest_document", "business_knowledge+qdrant", title)

        now = datetime.now(timezone.utc).isoformat()
        safe_title = title.replace("'", "\\'")
        safe_category = category.replace("'", "\\'")
        safe_source = source.replace("'", "\\'")
        preview = content[:200].replace("'", "\\'")
        word_count = len(content.split())

        # Create Document node in FalkorDB
        cypher = (
            f"CREATE (d:Document {{"
            f"title: '{safe_title}', "
            f"category: '{safe_category}', "
            f"source: '{safe_source}', "
            f"date: '{now}', "
            f"word_count: {word_count}, "
            f"preview: '{preview}', "
            f"ingested_at: '{now}'"
            f"}}) RETURN d"
        )
        graph_result = falkordb_client.graph_query("business_knowledge", cypher)

        # Chunk and embed into Qdrant
        chunks = _chunk_text(content, chunk_size=500, overlap=50)
        vectors = embedder.embed_texts(chunks)

        from qdrant_client.models import PointStruct

        points = []
        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "text": chunk,
                        "category": category,
                        "filename": f"{title}.md",
                        "file_path": f"/vault/{category}/{title}.md",
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "vertical": category,
                        "extension": ".md",
                    },
                )
            )
        if points:
            qdrant_client.upsert_points("amplified_knowledge", points)

        return json.dumps({
            "status": "ingested",
            "title": title,
            "chunks_created": len(chunks),
            "graph_result": graph_result,
        }, default=str)

    @mcp.tool()
    def update_status(document_title: str, status: str) -> str:
        """Mark a document as canonical / superseded / candidate / scratch.

        Args:
            document_title: Title of the document to update.
            status: New status — one of: canonical, superseded, candidate, scratch.
        """
        valid_statuses = {"canonical", "superseded", "candidate", "scratch"}
        if status not in valid_statuses:
            return json.dumps({"error": f"Invalid status. Must be one of: {valid_statuses}"})

        audit.log_operation("update_status", "business_knowledge", f"{document_title} -> {status}")

        safe_title = document_title.replace("'", "\\'")
        safe_status = status.replace("'", "\\'")
        cypher = (
            f"MATCH (d:Document) "
            f"WHERE toLower(d.title) CONTAINS toLower('{safe_title}') "
            f"SET d.status = '{safe_status}' "
            f"RETURN d.title, d.status"
        )
        result = falkordb_client.graph_query("business_knowledge", cypher)
        return json.dumps(result, default=str)

    @mcp.tool()
    def tag_entity(document_title: str, entity_name: str) -> str:
        """Create an entity link in FalkorDB between a document and an entity.

        If the entity doesn't exist, creates it. Then creates a MENTIONS
        relationship from the document to the entity.

        Args:
            document_title: Title of the document.
            entity_name: Name of the entity to link.
        """
        audit.log_operation("tag_entity", "business_knowledge", f"{document_title} -> {entity_name}")

        safe_title = document_title.replace("'", "\\'")
        safe_entity = entity_name.replace("'", "\\'")
        cypher = (
            f"MATCH (d:Document) "
            f"WHERE toLower(d.title) CONTAINS toLower('{safe_title}') "
            f"WITH d LIMIT 1 "
            f"MERGE (e:Entity {{name: '{safe_entity}'}}) "
            f"MERGE (d)-[:MENTIONS]->(e) "
            f"RETURN d.title, e.name"
        )
        result = falkordb_client.graph_query("business_knowledge", cypher)
        return json.dumps(result, default=str)

    @mcp.tool()
    def flag_stale(document_title: str, reason: str) -> str:
        """Flag a document for human review.

        Sets a 'flagged' property with the reason and timestamp.

        Args:
            document_title: Title of the document to flag.
            reason: Reason for flagging (e.g. "outdated", "contradicts newer doc").
        """
        audit.log_operation("flag_stale", "business_knowledge", f"{document_title}: {reason}")

        now = datetime.now(timezone.utc).isoformat()
        safe_title = document_title.replace("'", "\\'")
        safe_reason = reason.replace("'", "\\'")
        cypher = (
            f"MATCH (d:Document) "
            f"WHERE toLower(d.title) CONTAINS toLower('{safe_title}') "
            f"SET d.flagged = '{safe_reason}', d.flagged_at = '{now}' "
            f"RETURN d.title, d.flagged, d.flagged_at"
        )
        result = falkordb_client.graph_query("business_knowledge", cypher)
        return json.dumps(result, default=str)


# ===================================================================
# TIER 3 — ADMIN (available only when TIER=admin)
# ===================================================================

if config.TIER == config.Tier.ADMIN:

    @mcp.tool()
    def archive_document(document_title: str, reason: str) -> str:
        """Archive a document — sets status to 'superseded' with reason and timestamp.

        Args:
            document_title: Title of the document to archive.
            reason: Reason for archiving.
        """
        audit.log_operation("archive_document", "business_knowledge", f"{document_title}: {reason}")

        now = datetime.now(timezone.utc).isoformat()
        safe_title = document_title.replace("'", "\\'")
        safe_reason = reason.replace("'", "\\'")
        cypher = (
            f"MATCH (d:Document) "
            f"WHERE toLower(d.title) CONTAINS toLower('{safe_title}') "
            f"SET d.status = 'superseded', "
            f"d.archived_reason = '{safe_reason}', "
            f"d.archived_at = '{now}' "
            f"RETURN d.title, d.status, d.archived_reason, d.archived_at"
        )
        result = falkordb_client.graph_query("business_knowledge", cypher)
        return json.dumps(result, default=str)

    @mcp.tool()
    def promote_document(document_title: str) -> str:
        """Promote a document from candidate to canonical status.

        Args:
            document_title: Title of the document to promote.
        """
        audit.log_operation("promote_document", "business_knowledge", document_title)

        now = datetime.now(timezone.utc).isoformat()
        safe_title = document_title.replace("'", "\\'")
        cypher = (
            f"MATCH (d:Document) "
            f"WHERE toLower(d.title) CONTAINS toLower('{safe_title}') "
            f"AND d.status = 'candidate' "
            f"SET d.status = 'canonical', d.promoted_at = '{now}' "
            f"RETURN d.title, d.status, d.promoted_at"
        )
        result = falkordb_client.graph_query("business_knowledge", cypher)
        return json.dumps(result, default=str)

    @mcp.tool()
    def audit_log(limit: int = 50) -> str:
        """Retrieve recent operations from the audit log.

        Args:
            limit: Number of recent entries to return (default 50, max 200).
        """
        limit = min(max(limit, 1), 200)
        audit.log_operation("audit_log", "audit", f"limit={limit}")
        entries = audit.get_recent_entries(limit)
        return json.dumps(entries, default=str)


# ===================================================================
# Helpers
# ===================================================================


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks by word count."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks if chunks else [text]


# ===================================================================
# Entrypoint
# ===================================================================


def main() -> None:
    """Run the MCP server."""
    import logging

    logging.getLogger("amplified_mcp").info(
        "Starting Amplified Knowledge MCP server — tier=%s agent=%s session=%s",
        config.TIER.value,
        config.AGENT_NAME,
        config.SESSION_ID,
    )
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

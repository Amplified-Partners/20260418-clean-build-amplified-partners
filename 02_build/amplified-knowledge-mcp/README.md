# Amplified Knowledge MCP Server

Tiered MCP server exposing Amplified Partners' knowledge systems (FalkorDB graph + Qdrant vectors) to AI agents via the Model Context Protocol.

**FalkorDB knowledge graph and Qdrant vector embeddings built by Clawd (OpenClaw).**

## Architecture

```
┌──────────────────────────────┐
│   AI Agent (Claude, etc.)    │
│   connects via MCP stdio     │
└──────────┬───────────────────┘
           │
┌──────────▼───────────────────┐
│  amplified-knowledge-mcp     │
│  ┌─────────┐  ┌───────────┐ │
│  │ Tier    │  │ Embedding │ │
│  │ Enforce │  │ Pipeline  │ │
│  └────┬────┘  └─────┬─────┘ │
│       │              │       │
│  ┌────▼────┐  ┌─────▼─────┐ │
│  │FalkorDB │  │  Qdrant   │ │
│  │ Client  │  │  Client   │ │
│  └────┬────┘  └─────┬─────┘ │
└───────┼─────────────┼───────┘
        │             │
   ┌────▼────┐  ┌─────▼─────┐
   │FalkorDB │  │  Qdrant   │
   │ :6379   │  │  :6333    │
   └─────────┘  └───────────┘
```

## Tiers

| Tier | Env Value | Capabilities |
|------|-----------|-------------|
| **1 — Read-only** | `readonly` | Query graphs, semantic search, browse documents/entities |
| **2 — Read-write** | `readwrite` | Tier 1 + ingest documents, update status, tag entities, flag stale |
| **3 — Admin** | `admin` | Tier 1+2 + archive, promote, audit log |

## Tools

### Tier 1 (Read-only)
- `query_graph(graph_name, cypher_query)` — read-only Cypher against FalkorDB
- `search_knowledge(query_text, limit)` — semantic search (384-dim, all-MiniLM-L6-v2)
- `get_document(document_title)` — retrieve a document node by title
- `list_entities(category)` — browse entity nodes
- `search_principles(keyword)` — find principle documents (graph + semantic)
- `get_chronology(topic)` — trace topic evolution over time
- `list_collections()` — Qdrant collection stats
- `filter_by_category(category, limit)` — browse by vault category

### Tier 2 (Read-write)
- `ingest_document(content, title, category, source)` — add to both FalkorDB + Qdrant
- `update_status(document_title, status)` — canonical / superseded / candidate / scratch
- `tag_entity(document_title, entity_name)` — create entity links
- `flag_stale(document_title, reason)` — flag for human review

### Tier 3 (Admin)
- `archive_document(document_title, reason)` — move to superseded with reason
- `promote_document(document_title)` — candidate → canonical
- `audit_log(limit)` — recent operations log

## Deployment

```bash
# On the Beast (amplified-core), from this directory:
docker compose up -d

# Or with a specific tier:
TIER=readwrite AGENT_NAME=devon SESSION_ID=abc123 docker compose up -d
```

## Configuration

All via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `TIER` | `readonly` | Access tier: readonly, readwrite, admin |
| `FALKORDB_HOST` | `falkordb` | FalkorDB container hostname |
| `FALKORDB_PORT` | `6379` | FalkorDB port |
| `QDRANT_HOST` | `qdrant` | Qdrant container hostname |
| `QDRANT_PORT` | `6333` | Qdrant HTTP port |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model |
| `LOG_DIR` | `/var/log/amplified-mcp` | Audit log directory |
| `AGENT_NAME` | `unknown` | Calling agent identity |
| `SESSION_ID` | `unset` | Session identifier |

## Security

- **Tier 1**: All Cypher is validated — CREATE, SET, DELETE, MERGE, REMOVE rejected
- **Tier 2**: Destructive operations (DELETE, DROP, DETACH) rejected
- **Tier 3**: Full access except raw data destruction
- All operations are audit-logged with agent, timestamp, session, and operation details

## Audit

Every operation is logged to:
- stderr (structured JSON)
- `/var/log/amplified-mcp/audit.jsonl` (persistent JSONL)

Use the `audit_log` tool (Tier 3) to query recent entries.

---

Signed-by: Devon | 2026-04-29 | devin-60ae27b157c3459d90abd0c80734513b

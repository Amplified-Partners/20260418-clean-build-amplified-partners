# Vault Monitor Report — 2026-03-20 R28

## 1. Local Output (Claude Code)
- **_working/**: 27 monitor reports today (r2–r27). Latest: r27 at 04:53 UTC.
- **_master-docs/**: Empty — no new documents.

## 2. FalkorDB Ingestion
- **Process**: NOT RUNNING (completed)
- **Status**: Log says "Done! Your Business Brain is being built."
- **Log lines**: 8,545
- **Successes**: 11
- **Errors**: 293 (mostly "Query timed out" on business-knowledge-foundation.md)
- **⚠️ FLAG**: High error count (293) vs low success count (11). The ingestion run appears to have completed but with significant failures. Most errors are FalkorDB query timeouts.

## 3. Porch Status
- **Incoming queue**: EMPTY — nothing waiting to process.

## 4. Vault Health
| Store | Metric | Value |
|-------|--------|-------|
| Qdrant | Points | **57,434** |
| Qdrant | Status | **green** |
| FalkorDB | Nodes | **4,973** |

## 5. Infrastructure
| Container | Status |
|-----------|--------|
| qdrant | Up 8 days |
| falkordb | Up 4 days |
| litellm | Up 37 hours |
| langfuse | Up 37 hours |
| searxng | Up 37 hours |
| ollama | Up 13 hours |

**⚠️ NOTE**: Qdrant port 6333 is NOT mapped to localhost — only accessible via Docker network (172.18.0.7:6333). This may cause issues for scripts expecting localhost access.

## Flags
1. **Ingestion error rate is high** — 293 errors vs 11 successes. Needs investigation.
2. **Qdrant not on localhost** — port binding missing from Docker config.

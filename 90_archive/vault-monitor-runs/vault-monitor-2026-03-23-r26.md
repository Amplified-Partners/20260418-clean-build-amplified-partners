# Vault Monitor — 2026-03-23 06:02 UTC (Run 26)

## 1. Claude Code Output
- **_working/**: 25 vault-monitor reports today (r1–r25). Latest: r25 at 05:42 UTC.
- **_master-docs/**: Empty. No new master docs.

## 2. FalkorDB Ingestion
- **Process**: NOT RUNNING. Ingestion completed.
- **Status**: Finished. "Done! Your Business Brain is being built."
- **Errors**: 293 errors in r3 log.
- **Error types**: Mostly `RediSearch: Syntax error at offset near "amplified"` and `Query timed out`.
- **Last failed files**: SESSION-2026-02-14-BUSINESS-BRAIN.md, businessfactory-a-plus-plan.md, businessfactory-complete-critique.md, business-knowledge-foundation.md.

## 3. Porch Status
- **Incoming**: EMPTY. No files waiting.
- Porch watcher not triggered (nothing to process).

## 4. Vault Health
| Component | Status | Count |
|-----------|--------|-------|
| **FalkorDB** | UP | **4,973 nodes** |
| **Qdrant** | ⚠️ DOWN | Not responding (container up 11 days, API unreachable) |

## ⚠️ FLAGS
1. **Qdrant API unreachable** — Container running but port 6333 not responding. Needs investigation. Possible OOM or internal crash.
2. **293 ingestion errors** — Persistent issue with RediSearch syntax errors on "amplified" keyword and query timeouts. These files were not ingested into the graph.

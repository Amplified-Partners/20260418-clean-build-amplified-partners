# Vault Monitor — 2026-03-22 14:35 UTC (r119)

## 1. Local Files
- **_working/**: 10+ monitor reports today (r109–r118). Latest: r118 at 14:12. No other new files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **Process**: NOT running (completed)
- **Result**: 120 success, 32 failed (152 total)
- **Errors**: 293 error lines in log. Last failure: `business-knowledge-foundation.md` — FalkorDB query timed out
- **Status**: Ingestion finished. Log says "Done! Your Business Brain is being built."

## 3. Porch
- **Incoming**: Empty. Nothing queued.

## 4. Vault Health
| Store | Count | Status |
|-------|-------|--------|
| Qdrant (amplified_knowledge) | **57,434 points** | GREEN |
| FalkorDB (business_knowledge) | **4,973 nodes** | OK |

**Qdrant collections**: person_profiles, amplified_knowledge, content_embeddings, knowledge_base

## Flags
- ⚠️ **32 failed ingestions** — mostly query timeouts. `business-knowledge-foundation.md` was the last to fail. May want to retry these with longer timeout or smaller batch size.
- ⚠️ **Qdrant port not exposed to host** — container running (10 days uptime) but `localhost:6333` unreachable from host. Only accessible via container network IP (172.18.0.7). Docker port mapping may have been dropped. Not blocking anything currently but worth noting.
- ✅ No new files on porch. Pipeline idle.

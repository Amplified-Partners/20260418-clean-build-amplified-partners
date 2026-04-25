# Vault Monitor — 2026-03-23 R5 (~12:45 UTC)

## 1. Local Files
- **_working/**: 4 monitor reports today (r1–r4), plus execution log. No new non-monitor files.
- **_master-docs/**: Empty. No new files.

## 2. FalkorDB Ingestion
- **Process**: NOT running (completed)
- **Status**: "Done! Your Business Brain is being built."
- **Errors**: 293 (Failed/Error/timed out entries in log)
- **Note**: Ingestion finished. 293 errors need review — same count as prior runs, no new activity.

## 3. Porch
- **Incoming**: Empty. Nothing queued.

## 4. Vault Health
| Store | Count | Status |
|-------|-------|--------|
| Qdrant (amplified_knowledge) | **57,434** points | OK (container IP only, not bound to localhost) |
| FalkorDB (business_knowledge) | **4,973** nodes | OK |

## Flags
- ⚠️ **Qdrant not port-mapped to localhost** — container is up (11 days) but only accessible via internal IP (172.18.0.7:6333). Not bound to host port 6333. This may affect any services expecting localhost access.
- ⚠️ **293 ingestion errors** — stable count, but should be reviewed to confirm they're all known/acceptable failures.

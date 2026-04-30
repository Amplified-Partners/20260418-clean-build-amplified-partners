# Vault Monitor — 2026-03-22 ~15:00 UTC (r121)

## 1. Local Files
- **_working/**: 120 monitor reports (r1–r120). Latest: r120 at 14:42. No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2–4. Beast (FalkorDB / Porch / Vault Health)
- **SSH FAILED**: `Connection refused` on port 22 to 135.181.161.131. Tried both key files (claude-code-beast-key, claude-code-beast-key-2). Beast SSH is unreachable from this sandbox.
- **Last known state (from r120, ~18 min ago)**:
  - Ingestion: COMPLETED (120 success / 32 failed / 293 error lines)
  - Porch: Empty
  - Qdrant: 57,434 points
  - FalkorDB: 4,973 nodes

## Flags
- 🔴 **Beast SSH unreachable** — Connection refused (persistent across recent runs). Likely sandbox network restriction — not a Beast-side issue since earlier runs today connected fine.
- ⚠️ **32 failed ingestions** still unresolved. Retry recommended when SSH access restored.
- ✅ No changes to local output files since last check.

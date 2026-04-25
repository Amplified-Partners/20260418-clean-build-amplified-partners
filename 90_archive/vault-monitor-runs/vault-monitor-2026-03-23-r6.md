# Vault Monitor — 2026-03-23 R6 (~12:55 UTC)

## 1. Local Files
- **_working/**: 5 monitor reports today (r1–r5). No new non-monitor files.
- **_master-docs/**: Empty. No changes.

## 2. FalkorDB Ingestion
- **UNABLE TO CHECK** — Beast (135.181.161.131) SSH connection refused on port 22, timed out on 2222/22222.
- Last known (R5): Ingestion complete, 293 errors in log, process not running.

## 3. Porch
- **UNABLE TO CHECK** — Beast unreachable (see above).

## 4. Vault Health
- **UNABLE TO CHECK** — Qdrant and FalkorDB both on Beast, which is unreachable.
- Last known (R5): Qdrant 57,434 points, FalkorDB 4,973 nodes.

## Flags
- 🔴 **Beast unreachable** — SSH connection refused on all attempted ports (22, 2222, 22222). Server may be down, SSH service stopped, or firewall change. This is a new issue since R5 which connected successfully. Needs investigation.
- ⚠️ Carrying forward: 293 ingestion errors still unreviewed.
- ⚠️ Carrying forward: Qdrant not port-mapped to localhost on Beast.

# Vault Monitor — 2026-03-23 r1 (10:42 UTC)

## 1. Claude Code Output
- **_working/**: 150 monitor reports from yesterday (Mar 22). This is first check today. No other new files.
- **_master-docs/**: Directory does not exist.

## 2. FalkorDB Ingestion
- **Beast SSH**: REFUSED — host pings fine (0.4ms avg) but port 22 is closed.
- **Process/Log/Errors**: Cannot check — SSH down.
- Last known state (r150): Ingestion complete, 293 errors (static), 4,973 nodes.

## 3. Porch
- Cannot check — SSH down.
- Last known state (r150): 0 incoming files.

## 4. Vault Health
- **Qdrant**: Cannot check — SSH down. Last known: 57,434 points, green.
- **FalkorDB**: Cannot check — SSH down. Last known: 4,973 nodes.

## Flags
- **🔴 Beast SSH DOWN** — Host responds to ping but SSH (port 22) is refusing connections. This was also seen around r145 yesterday before recovering at r150. Possible sshd crash or restart needed.
- All last-known values were stable as of 23:22 UTC yesterday.

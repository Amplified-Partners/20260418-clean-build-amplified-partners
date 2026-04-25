# Vault Monitor — 2026-03-22 r129 (17:32 UTC)

## 1. Claude Code Output
- **_working/**: Monitor reports only (r1–r128). No new non-monitor files.
- **_master-docs/**: Empty.

## 2. FalkorDB Ingestion
- **Status**: UNABLE TO CHECK — Beast SSH down (Connection refused on port 22).
- **Last known (r128)**: COMPLETED. 4,973 nodes. 293 historical errors.

## 3. Porch
- **Status**: UNABLE TO CHECK — Beast unreachable.

## 4. Vault Health
- **Qdrant**: UNABLE TO CHECK — Beast unreachable.
- **FalkorDB**: UNABLE TO CHECK — Beast unreachable.
- **Last known (r128)**: Qdrant 57,434 points, FalkorDB 4,973 nodes.

## Flags
- **ALERT: Beast SSH down AGAIN.** Connection refused on port 22 (135.181.161.131). Both SSH keys tried. This is the same class of outage as r108–r118. Was resolved at r128 but has recurred.
- Recommend checking Hetzner console or out-of-band access to verify Beast is up and sshd is running.

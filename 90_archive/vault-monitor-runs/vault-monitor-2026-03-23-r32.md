# Vault Monitor — 2026-03-23 07:43 UTC (Run 32)

## 1. Claude Code Output
- **_working/**: 31 vault-monitor reports today (r1–r31). No non-monitor files produced.
- **_master-docs/**: Empty.

## 2. FalkorDB Ingestion
- **SSH**: ❌ CONNECTION REFUSED — Beast (135.181.161.131:22) still unreachable. SSH key missing from this sandbox AND port 22 refusing connections.
- **Last known good (r9/r26)**: Ingestion complete. 293 historic errors in r3 log. 4,973 FalkorDB nodes.

## 3. Porch Status
- **SSH**: ❌ Cannot reach Beast.
- **Last known good**: Porch incoming empty.

## 4. Vault Health
- **SSH**: ❌ Cannot check remotely.
- **Last known good (r9)**: Qdrant 57,434 points (was healthy on container IP 172.18.0.7:6333, not bound to localhost). FalkorDB 4,973 nodes.

## 🚨 FLAGS
1. **Beast SSH down — PERSISTENT** — Connection refused since ~r27 (05:52 UTC), now 110+ min. Needs manual check via Hetzner console or direct Mac terminal SSH. Possible causes: SSH daemon crash, firewall change, server reboot.
2. **Qdrant localhost binding** — Known issue: port 6333 not bound to host. Works on container network only.
3. **ch-pipeline container** — Was UNHEALTHY as of r9 (9+ days). Cannot re-verify.
4. **293 ingestion errors** — Historic/unchanged. Not new.

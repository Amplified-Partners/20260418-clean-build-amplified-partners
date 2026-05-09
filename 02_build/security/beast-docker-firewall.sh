#!/usr/bin/env bash
# beast-docker-firewall.sh — Persistent DOCKER-USER iptables rules for Beast
# Prevents Docker from bypassing UFW by filtering in the DOCKER-USER chain.
#
# Usage:
#   sudo bash beast-docker-firewall.sh          # Apply rules
#   sudo bash beast-docker-firewall.sh --save   # Apply + persist across reboots
#
# The DOCKER-USER chain is evaluated BEFORE Docker's own DOCKER chain,
# so rules here take precedence over Docker's port-forwarding rules.
#
# Devon-7ac0 | 2026-05-09 | AMP-289
# ────────────────────────────────────────────────────────────────────

set -euo pipefail

# Beast external NIC — verify with: ip route show default
EXT_IFACE="enp193s0f0np0"

# Tailscale interface (created when tailscale is authenticated)
TS_IFACE="tailscale0"

echo "[*] Flushing DOCKER-USER chain..."
iptables -F DOCKER-USER

echo "[*] Applying DOCKER-USER rules..."

# 1. Allow established/related connections (return traffic for existing sessions)
iptables -A DOCKER-USER -m state --state RELATED,ESTABLISHED -j ACCEPT

# 2. Allow Traefik HTTP/HTTPS from external interface (public-facing by design)
iptables -A DOCKER-USER -i "$EXT_IFACE" -p tcp -m multiport --dports 80,443 -j RETURN

# 3. Allow all traffic from Tailscale interface (trusted private mesh)
iptables -A DOCKER-USER -i "$TS_IFACE" -j RETURN

# 4. Drop everything else from the external interface
#    This is the critical rule — prevents Docker's port-forwarding from
#    exposing internal services (Postgres, Cove API, etc.) to the internet,
#    even if a compose file binds to 0.0.0.0.
iptables -A DOCKER-USER -i "$EXT_IFACE" -j DROP

# 5. Allow all other traffic (Docker bridge-to-bridge, loopback, etc.)
iptables -A DOCKER-USER -j RETURN

echo "[*] DOCKER-USER chain rules applied:"
iptables -L DOCKER-USER -n -v --line-numbers

# Persist if requested
if [[ "${1:-}" == "--save" ]]; then
    if command -v netfilter-persistent &>/dev/null; then
        netfilter-persistent save
        echo "[*] Rules saved via netfilter-persistent."
    elif command -v iptables-save &>/dev/null; then
        iptables-save > /etc/iptables/rules.v4 2>/dev/null || \
            iptables-save > /etc/iptables.rules
        echo "[*] Rules saved to /etc/iptables/rules.v4"
    else
        echo "[!] No persistence tool found. Install iptables-persistent:"
        echo "    apt-get install -y iptables-persistent"
    fi
fi

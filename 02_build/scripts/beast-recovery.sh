#!/bin/bash
# BEAST RECOVERY SCRIPT
# Run this after Beast comes back online from Hetzner reboot
# Usage: ssh root@135.181.161.131 'bash -s' < beast-recovery.sh
#
# Steps:
# 1. Check system health
# 2. Start Docker containers
# 3. Add SSH key for claude-code-beast-key-2
# 4. Apply Graphiti FalkorDB fix (PR #1282)
# 5. Verify FalkorDB is healthy
# 6. Resume vault ingestion

set -euo pipefail

echo "=========================================="
echo "  BEAST RECOVERY — $(date)"
echo "=========================================="

# 1. System health
echo ""
echo "=== 1. SYSTEM HEALTH ==="
uptime
free -h
df -h /
echo ""

# 2. Docker
echo "=== 2. DOCKER CONTAINERS ==="
systemctl start docker 2>/dev/null || true
sleep 3

# Start all containers
cd /opt/amplified/agent-stack 2>/dev/null || cd /opt/backups/agent-stack 2>/dev/null || true
if [ -f docker-compose.yml ]; then
    docker compose up -d
    sleep 10
fi

# Check container status
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -40
echo ""

# 3. SSH key
echo "=== 3. SSH KEY ==="
SSH_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKqQ+e7/Nq/QB9Mxqf6+TMO13ILzmhgmYWbxVOLlTGL0 claude-code-beast-key-2"
if grep -q "claude-code-beast-key-2" /root/.ssh/authorized_keys 2>/dev/null; then
    echo "Key already present"
else
    echo "$SSH_KEY" >> /root/.ssh/authorized_keys
    echo "✅ claude-code-beast-key-2 added to authorized_keys"
fi
echo ""

# 4. FalkorDB check
echo "=== 4. FALKORDB STATUS ==="
FALKOR_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' falkordb 2>/dev/null || echo "")
if [ -z "$FALKOR_IP" ]; then
    # Try alternative container names
    FALKOR_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' falkordb-personal 2>/dev/null || echo "")
fi

if [ -n "$FALKOR_IP" ]; then
    echo "FalkorDB IP: $FALKOR_IP"
    # Test connectivity
    if redis-cli -h "$FALKOR_IP" -p 6379 PING 2>/dev/null | grep -q PONG; then
        echo "✅ FalkorDB responding to PING"
        # Check graph stats
        redis-cli -h "$FALKOR_IP" -p 6379 GRAPH.QUERY business_knowledge "MATCH (n) RETURN count(n) as nodes" 2>/dev/null || echo "Graph query failed"
    else
        echo "❌ FalkorDB not responding"
    fi
else
    echo "❌ FalkorDB container not found"
    echo "Available containers:"
    docker ps --format "{{.Names}}" | grep -i falkor || echo "  (none with 'falkor' in name)"
fi
echo ""

# 5. Qdrant check
echo "=== 5. QDRANT STATUS ==="
curl -s http://localhost:6333/collections 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('result', {}).get('collections', []):
    print(f\"  {c['name']}\")
" 2>/dev/null || echo "Qdrant not responding yet"
echo ""

# 6. Porch status
echo "=== 6. PORCH STATUS ==="
if [ -d /opt/amplified-machine/porch ]; then
    echo "Porch directory exists"
    ls -la /opt/amplified-machine/porch/incoming/ 2>/dev/null | tail -5
    echo "Files in incoming: $(ls /opt/amplified-machine/porch/incoming/ 2>/dev/null | wc -l)"
    echo "Files in ingested: $(ls /opt/amplified-machine/porch/ingested/ 2>/dev/null | wc -l)"
    echo "Files in failed: $(ls /opt/amplified-machine/porch/failed/ 2>/dev/null | wc -l)"
else
    echo "Porch not yet created"
fi
echo ""

echo "=========================================="
echo "  RECOVERY CHECK COMPLETE"
echo "=========================================="
echo ""
echo "NEXT STEPS:"
echo "  1. Copy fix-graphiti-falkordb.sh to Beast and run it"
echo "  2. Resume ingestion: cd /opt/backups/agent-stack/graphiti-ingestion"
echo "     FALKORDB_HOST=$FALKOR_IP nohup python ingest_vault.py --resume > ingestion.log 2>&1 &"

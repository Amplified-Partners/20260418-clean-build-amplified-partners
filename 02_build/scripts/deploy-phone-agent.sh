#!/bin/bash
# ============================================================
# Deploy xAI Phone Agent to Beast — ONE COMMAND
# Run this from your Mac Mini terminal
# ============================================================
set -e

BEAST="root@beast.amplifiedpartners.ai"
REMOTE_DIR="/opt/xai-phone-agent"
LOCAL_DIR="$HOME/Downloads/xai-phone-agent"
XAI_KEY="REDACTED_XAI_API_KEY"  # Secret redacted by Devon during consolidation — do not commit real keys

echo "=== Deploying xAI Phone Agent to Beast ==="
echo ""

# 1. Create remote directory
echo "[1/5] Creating directory on Beast..."
ssh "$BEAST" "mkdir -p $REMOTE_DIR"

# 2. Copy files
echo "[2/5] Copying files to Beast..."
scp "$LOCAL_DIR/server.py" "$BEAST:$REMOTE_DIR/"
scp "$LOCAL_DIR/requirements.txt" "$BEAST:$REMOTE_DIR/"
scp "$LOCAL_DIR/Dockerfile" "$BEAST:$REMOTE_DIR/"
scp "$LOCAL_DIR/docker-compose.yml" "$BEAST:$REMOTE_DIR/"

# 3. Create .env on Beast
echo "[3/5] Writing .env..."
ssh "$BEAST" "cat > $REMOTE_DIR/.env << 'EOF'
XAI_API_KEY=$XAI_KEY
GROK_VOICE=Ara
LOG_LEVEL=INFO
EOF"

# 4. Check amplified-net network exists (Traefik's network)
echo "[4/5] Checking Docker network..."
ssh "$BEAST" "docker network inspect amplified-net >/dev/null 2>&1 || echo 'WARNING: amplified-net not found — Traefik may not route to this container'"

# 5. Build and start
echo "[5/5] Building and starting container..."
ssh "$BEAST" "cd $REMOTE_DIR && docker compose up -d --build"

echo ""
echo "=== Checking health... ==="
sleep 3
HEALTH=$(ssh "$BEAST" "curl -s http://localhost:8080/health" 2>/dev/null || echo "waiting...")
echo "Health check: $HEALTH"

echo ""
echo "============================================"
echo "  DEPLOYED!"
echo "============================================"
echo ""
echo "Service running at: https://phone.beast.amplifiedpartners.ai"
echo ""
echo "NOW DO THIS IN TWILIO:"
echo "  1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/incoming"
echo "  2. Click on +44 191 743 3558"
echo "  3. Under 'Voice Configuration' → 'A Call Comes In'"
echo "  4. Change the webhook URL from the VAPI one to:"
echo ""
echo "     https://phone.beast.amplifiedpartners.ai/incoming-call"
echo ""
echo "  5. Method: POST"
echo "  6. Click SAVE"
echo ""
echo "Then call 0191 743 3558 and talk to Grok."
echo "Logs: ssh $BEAST 'docker logs -f xai-phone-agent'"

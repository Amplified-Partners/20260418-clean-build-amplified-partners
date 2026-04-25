#!/bin/bash
# Deploy Voice Agent to Beast
# Run from your Mac: bash deploy-voice.sh

set -e

BEAST="root@beast.amplifiedpartners.ai"
REMOTE_DIR="/opt/amplified-voice-agent"

echo "=== Deploying Voice Agent to Beast ==="

# 1. Create directory on Beast
echo "Creating remote directory..."
ssh $BEAST "mkdir -p $REMOTE_DIR"

# 2. Copy files to Beast
echo "Copying files..."
scp voice_agent.py $BEAST:$REMOTE_DIR/
scp Dockerfile.voice $BEAST:$REMOTE_DIR/
scp docker-compose.voice.yml $BEAST:$REMOTE_DIR/docker-compose.yml
scp requirements-voice.txt $BEAST:$REMOTE_DIR/
scp .env $BEAST:$REMOTE_DIR/

# 3. Build and start on Beast
echo "Building and starting container..."
ssh $BEAST "cd $REMOTE_DIR && docker compose build && docker compose up -d"

# 4. Check health
echo "Waiting for startup..."
sleep 5
ssh $BEAST "curl -s http://localhost:8080/health | python3 -m json.tool"

echo ""
echo "=== Voice Agent Deployed! ==="
echo "URL: https://voice.beast.amplifiedpartners.ai"
echo "Health: https://voice.beast.amplifiedpartners.ai/health"
echo ""
echo "Now configure Twilio webhook:"
echo "  Phone: +441917433558"
echo "  Webhook URL: https://voice.beast.amplifiedpartners.ai/incoming-call"
echo "  Method: POST"

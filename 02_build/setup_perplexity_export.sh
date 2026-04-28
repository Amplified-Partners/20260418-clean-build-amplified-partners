#!/usr/bin/env bash
# Setup and run script for simwai/perplexity-ai-export on Beast (Hetzner AX162-R)
# Prepared by Antigravity
# Attribution: https://github.com/simwai/perplexity-ai-export

set -e

REPO_DIR="perplexity-ai-export"
REPO_URL="https://github.com/simwai/perplexity-ai-export.git"

echo "[*] Preparing Perplexity AI Export for the Beast..."

# 1. Clone or update the repository
if [ ! -d "$REPO_DIR" ]; then
    echo "[*] Cloning repository..."
    git clone "$REPO_URL"
else
    echo "[*] Repository already exists. Pulling latest..."
    cd "$REPO_DIR"
    git pull
    cd ..
fi

cd "$REPO_DIR"

# 2. Install Node dependencies (Requires Node 20)
echo "[*] Installing npm dependencies..."
npm install

# 3. Install Playwright Chromium (Headless browser for extraction)
echo "[*] Installing Playwright Chromium..."
npx playwright install chromium

# 4. Pull required Ollama models
# NOTE: The Beast runs Ollama behind Traefik. OLLAMA_HOST may need setting if not executed inside the Beast's environment natively.
echo "[*] Pulling Ollama models (nomic-embed-text, deepseek-r1)..."
ollama pull nomic-embed-text || echo "[!] Failed to pull nomic-embed-text. Verify Ollama is accessible."
ollama pull deepseek-r1 || echo "[!] Failed to pull deepseek-r1. Verify Ollama is accessible."

# 5. Environment configuration
if [ ! -f ".env" ]; then
    echo "[*] Setting up .env configuration..."
    cp .env.example .env
    
    # Force enable vector search for RAG capabilities
    if ! grep -q "ENABLE_VECTOR_SEARCH=" .env; then
        echo "ENABLE_VECTOR_SEARCH=true" >> .env
    else
        # Mac and Linux sed compatible replacement
        sed -i.bak 's/ENABLE_VECTOR_SEARCH=.*/ENABLE_VECTOR_SEARCH=true/g' .env && rm -f .env.bak
    fi
    
    echo "[!] IMPORTANT: Adjust OLLAMA_URL in .env if the Beast's Ollama is routed differently (e.g. via Traefik instead of localhost:11434)."
fi

echo ""
echo "[*] Beast preparation complete."
echo "[*] To fire off the extraction, run:"
echo "cd $REPO_DIR && npm run dev"

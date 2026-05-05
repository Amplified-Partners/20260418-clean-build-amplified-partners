---
title: "Qdrant Vector Database Setup"
id: "qdrant_setup"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Qdrant Vector Database Setup

## Overview

Qdrant stores cached research data with semantic embeddings for fast retrieval. This guide covers local development, Railway deployment, and Qdrant Cloud production setup.

## Option 1: Local Development (Docker)

### Quick Start

```bash
# Run Qdrant in Docker
docker run -p 6333:6333 qdrant/qdrant

# Verify it's running
curl http://localhost:6333/dashboard
```

### With Docker Compose (Recommended)

Create `docker-compose.qdrant.yml`:

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_data:/qdrant/storage
    restart: unless-stopped

networks:
  default:
    name: cover-ai-network
```

Start with:

```bash
docker-compose -f docker-compose.qdrant.yml up -d
```

### Verify Connection

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
print(client.get_collections())
# Expected output: CollectionsResponse(collections=[])
```

---

## Option 2: Railway Deployment

### Add Qdrant to Railway

```bash
# Navigate to project directory
cd cover-ai-railway

# Add Qdrant using Railway CLI
railway add

# Select "Qdrant" from the template list
# Railway will automatically create the service and set environment variables
```

### Set Environment Variables

Railway automatically sets `QDRANT_URL`. Verify:

```bash
railway variables

# Should show: QDRANT_URL=https://your-service.up.railway.app
```

### Manual Configuration (if needed)

```bash
railway variables set QDRANT_URL=${{Qdrant.QDRANT_URL}}
```

### Connect from Application

Update `.env`:

```bash
QDRANT_URL=https://your-qdrant-service.up.railway.app
```

---

## Option 3: Qdrant Cloud (Production)

### Sign Up

1. Go to https://cloud.qdrant.io
2. Create account (free tier available)
3. Verify email

### Create Cluster

1. Click "Create Cluster"
2. Choose:
   - **Tier**: Free (for testing) or paid (production)
   - **Region**: Choose closest to your users (e.g., London for UK)
   - **Cloud Provider**: AWS, GCP, or Azure
3. Click "Create Cluster"
4. Wait 2-5 minutes for provisioning

### Get Connection Details

Once cluster is ready:

1. Click "Connect" button
2. Copy the API URL (e.g., `https://xyz-1234.us-east-1-0.aws.cloud.qdrant.io`)
3. Generate an API key (Settings → API Keys → Create Key)

### Set Environment Variables

```bash
# In Railway
railway variables set QDRANT_URL=https://your-cluster.qdrant.io
railway variables set QDRANT_API_KEY=your-api-key-here
```

### Update Application Code

In `workers/research_worker.py`, update Qdrant initialization:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
```

---

## Testing Connection

### Python Test Script

Create `test_qdrant_connection.py`:

```python
import os
from qdrant_client import QdrantClient

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Initialize client
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")  # Optional for local
)

# Test connection
try:
    collections = qdrant.get_collections()
    print(f"✅ Connected to Qdrant")
    print(f"   Collections: {len(collections.collections)}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run:

```bash
python test_qdrant_connection.py
```

### API Test

```bash
curl -X GET "http://localhost:6333/collections"

# Expected response:
# {"status":"ok","result":{"collections":[]}}
```

---

## Tenant Collection Naming

Each tenant gets their own Qdrant collection with isolated data:

| Tenant ID | Collection Name |
|-----------|-----------------|
| `abc-123` | `tenant_abc_123` |
| `xyz-789` | `tenant_xyz_789` |

Collections are auto-created when first research is stored.

---

## Collection Settings

Default configuration for tenant collections:

```python
from qdrant_client.models import Distance, VectorParams

VectorParams(
    size=384,           # Embedding dimension (sentence-transformers)
    distance=Distance.COSINE  # Best for semantic similarity
)
```

### Why These Settings?

- **384 dimensions**: Optimal for `all-MiniLM-L6-v2` embeddings
- **Cosine distance**: Measures semantic similarity, best for research caching
- **Auto-creation**: Collections created per tenant for data isolation

---

## Troubleshooting

### Connection Refused

```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Check logs
docker logs qdrant

# Restart if needed
docker restart qdrant
```

### Authentication Failed

```bash
# Verify API key is set correctly
echo $QDRANT_API_KEY

# Check for extra spaces or newlines in .env
cat .env | grep QDRANT
```

### Collection Not Found

```python
# List all collections
collections = client.get_collections()
print([c.name for c in collections.collections])
```

### Timeout Errors

```bash
# Increase timeout in environment
export QDRANT_TIMEOUT=30
```

---

## Cost Estimation

| Deployment | Cost |
|------------|------|
| Local (Docker) | Free |
| Railway | Free tier available |
| Qdrant Cloud Free | 1GB storage, limited queries |
| Qdrant Cloud Pro | ~$25/month for production |

---

## Next Steps

After setup:

1. ✅ Test connection with `test_qdrant_connection.py`
2. ✅ Run first research job to auto-create tenant collection
3. ✅ Verify data is stored in Qdrant dashboard
4. ✅ Set up monitoring alerts for cluster health

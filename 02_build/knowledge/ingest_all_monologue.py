#!/usr/bin/env python3
"""
Ingest ALL Monologue transcripts (2,126 total) into vault + Qdrant
"""

import json
from pathlib import Path
from datetime import datetime
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
import hashlib
import warnings
warnings.filterwarnings('ignore')

# Configuration
MONOLOGUE_JSON = Path("/Users/ewanbramley/Library/Containers/com.zeitalabs.jottleai/Data/Documents/transcription_history.json")
VAULT_PATH = Path("/Users/ewanbramley/Manual Library/real-vault/transcripts/monologue-full")
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_API_KEY = "amplified-qdrant-2026"
COLLECTION_NAME = "ewan_transcripts"

print("🦞 Processing ALL 2,126 Monologue Transcripts")
print("="*70)

# Initialize
print("🔧 Loading Monologue history...")
with open(MONOLOGUE_JSON, 'r') as f:
    data = json.load(f)

transcripts = data.get('history', [])
print(f"✓ Found {len(transcripts)} total transcripts")

# Create vault directory
VAULT_PATH.mkdir(parents=True, exist_ok=True)
print(f"✓ Vault ready at {VAULT_PATH}")

# Initialize Qdrant + embedding
print("🔧 Initializing Qdrant + FastEmbed...")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, prefer_grpc=False, https=False)
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
print("✓ Ready to ingest")

def generate_id(text: str) -> str:
    """Generate stable ID from text"""
    return hashlib.md5(text.encode()).hexdigest()

# Process all transcripts
print(f"\n📂 Processing {len(transcripts)} transcripts...")
print("="*70)

vault_created = 0
vectors_created = 0
errors = []
batch_points = []

for i, entry in enumerate(transcripts, 1):
    try:
        # Extract data
        text = entry.get('text', entry.get('rawText', ''))
        if not text or not text.strip():
            continue
        
        # Parse timestamp
        ts = entry.get('timestamp', '')
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            date_str = dt.strftime('%Y-%m-%d')
            time_str = dt.strftime('%H%M')
            timestamp = ts
        except:
            date_str = 'unknown'
            time_str = f"{i:04d}"
            timestamp = 'unknown'
        
        source_type = entry.get('sourceType', 'dictation')
        source_id = entry.get('sourceIdentifier', 'unknown')
        
        # Get context
        context = entry.get('dictateContext', {})
        if isinstance(context, dict):
            window_title = context.get('windowTitle', '')
        else:
            window_title = str(context) if context else ''
        
        # Create vault file
        filename = f"monologue-{date_str}-{time_str}-{i:04d}.md"
        filepath = VAULT_PATH / filename
        
        frontmatter = f"""---
type: transcript
source: monologue
date: {date_str}
timestamp: {timestamp}
source_type: {source_type}
source_identifier: "{source_id}"
window_title: "{window_title}"
word_count: {len(text.split())}
tags: [voice-memo, transcription, ewan, monologue-full]
---

# Monologue Transcript — {date_str}

**Source:** {source_type}  
**Context:** {window_title if window_title else 'N/A'}  
**Timestamp:** {timestamp}

---

{text}
"""
        
        filepath.write_text(frontmatter, encoding='utf-8')
        vault_created += 1
        
        # Generate embedding
        vector = list(embedding_model.embed([text[:2000]]))[0].tolist()
        
        # Create point
        point_id = generate_id(f"{filename}-{i}")
        payload = {
            "text": text,
            "filename": filename,
            "filepath": f"monologue-full/{filename}",
            "type": "transcript",
            "source": "monologue",
            "date": date_str,
            "timestamp": timestamp,
            "source_type": source_type,
            "source_identifier": source_id,
            "window_title": window_title,
            "word_count": len(text.split()),
            "tags": ["voice-memo", "transcription", "ewan", "monologue-full"]
        }
        
        from qdrant_client.models import PointStruct
        batch_points.append(PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        ))
        vectors_created += 1
        
        # Batch upload every 50 points
        if len(batch_points) >= 50:
            qdrant.upsert(collection_name=COLLECTION_NAME, points=batch_points)
            batch_points = []
            print(f"[{i}/{len(transcripts)}] Processed {vault_created} files, {vectors_created} vectors ingested...")
        
    except Exception as e:
        errors.append(f"Transcript {i}: {str(e)}")
        if len(errors) <= 5:
            print(f"✗ Error on transcript {i}: {e}")

# Upload remaining points
if batch_points:
    qdrant.upsert(collection_name=COLLECTION_NAME, points=batch_points)
    print(f"[{len(transcripts)}/{len(transcripts)}] Final batch uploaded...")

# Summary
print("\n" + "="*70)
print("✅ COMPLETE!")
print("="*70)
print(f"  Vault files created: {vault_created}")
print(f"  Vectors ingested: {vectors_created}")
print(f"  Errors: {len(errors)}")
if errors:
    print(f"\n  First few errors:")
    for err in errors[:5]:
        print(f"    {err}")

# Verify Qdrant count
count = qdrant.count(collection_name=COLLECTION_NAME)
print(f"\n✓ Total vectors in Qdrant: {count.count}")
print("="*70)
print("\n🔥 ALL 2,126 TRANSCRIPTS READY FOR PUDDING QUERIES!")

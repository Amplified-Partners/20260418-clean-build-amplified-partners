#!/usr/bin/env python3
"""
Transcript Ingestion into Qdrant
Implements the Pudding Technique (Swanson's ABC model)
"""

import frontmatter
from pathlib import Path
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib
import sys
from datetime import datetime

# Configuration
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_API_KEY = "amplified-qdrant-2026"
COLLECTION_NAME = "ewan_transcripts"

# Initialize clients (using Qdrant's built-in FastEmbed)
print("🔧 Initializing clients...")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY, prefer_grpc=False, https=False)

# We'll use Qdrant's built-in embedding model (no external API needed)
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # Fast, free, good quality

def create_collection():
    """Create Qdrant collection for transcripts"""
    try:
        # Check if collection exists
        collections = qdrant.get_collections().collections
        if any(c.name == COLLECTION_NAME for c in collections):
            print(f"✓ Collection '{COLLECTION_NAME}' already exists")
            return
        
        # Create new collection
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,  # BAAI/bge-small-en-v1.5 dimension
                distance=Distance.COSINE
            )
        )
        print(f"✓ Created collection '{COLLECTION_NAME}'")
    except Exception as e:
        print(f"✗ Error creating collection: {e}")
        sys.exit(1)

def generate_embedding(text: str, model) -> list:
    """Generate embedding using FastEmbed"""
    try:
        # Use FastEmbed's embed method
        embeddings = list(model.embed([text[:2000]]))  # Truncate for performance
        return embeddings[0].tolist()
    except Exception as e:
        print(f"✗ Error generating embedding: {e}")
        return None

def generate_id(filepath: str) -> str:
    """Generate stable ID from filepath"""
    return hashlib.md5(str(filepath).encode()).hexdigest()

def ingest_transcripts(vault_path: str, embedding_model):
    """Ingest all transcripts from vault into Qdrant"""
    vault = Path(vault_path).expanduser()
    
    if not vault.exists():
        print(f"✗ Vault path not found: {vault}")
        sys.exit(1)
    
    # Find all markdown files
    transcript_files = list(vault.rglob("*.md"))
    # Exclude INDEX and PUDDING-TECHNIQUE files
    transcript_files = [f for f in transcript_files if f.stem not in ['INDEX', 'PUDDING-TECHNIQUE-RESEARCH']]
    
    print(f"📂 Found {len(transcript_files)} transcripts")
    
    points = []
    errors = []
    
    for i, md_file in enumerate(transcript_files, 1):
        try:
            # Read file content
            content = md_file.read_text(encoding='utf-8')
            
            # Extract content after second ---
            parts = content.split('---', 2)
            if len(parts) < 3:
                print(f"⊘ Skipping malformed: {md_file.name}")
                continue
            
            frontmatter_text = parts[1]
            main_content = parts[2].strip()
            
            # Skip if no content
            if not main_content:
                print(f"⊘ Skipping empty: {md_file.name}")
                continue
            
            # Parse frontmatter manually
            metadata = {}
            for line in frontmatter_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"')
            
            # Generate embedding
            print(f"[{i}/{len(transcript_files)}] Embedding {md_file.name}...", end=" ")
            vector = generate_embedding(main_content, embedding_model)
            
            if vector is None:
                errors.append(md_file.name)
                print("✗ Failed")
                continue
            
            # Create point
            point_id = generate_id(str(md_file))
            payload = {
                "text": main_content,
                "filename": md_file.name,
                "filepath": str(md_file.relative_to(vault)),
                **metadata  # All frontmatter fields
            }
            
            points.append(PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            ))
            
            print("✓")
            
            # Batch upload every 10 points
            if len(points) >= 10:
                qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
                points = []
            
        except Exception as e:
            errors.append(f"{md_file.name}: {str(e)}")
            print(f"✗ Error: {e}")
    
    # Upload remaining points
    if points:
        qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    
    # Summary
    print("\n" + "="*60)
    print(f"✓ Ingestion complete!")
    print(f"  - Processed: {len(transcript_files)} files")
    print(f"  - Errors: {len(errors)}")
    if errors:
        print(f"  - Failed files: {errors[:5]}")
    print("="*60)

def main():
    print("🦞 Pudding Technique: Transcript Ingestion")
    print("="*60)
    
    # Step 1: Create collection
    create_collection()
    
    # Step 2: Initialize embedding model
    print("🔧 Loading embedding model (FastEmbed)...")
    from fastembed import TextEmbedding
    embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL)
    print("✓ Model loaded")
    
    # Step 3: Ingest transcripts
    vault_path = "~/Manual Library/real-vault/transcripts"
    ingest_transcripts(vault_path, embedding_model)
    
    print("\n✓ Ready for pudding queries! 🎉")

if __name__ == "__main__":
    main()

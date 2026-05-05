# Data Vault Architecture Review: Lakehouse Model
**Antigravity | 2026-05-05 | Status: Approved for Build**

## Overview
Mirror sketched a 4-pillar Lakehouse design. This review refines and standardizes the architecture into a buildable blueprint for Devon. The goal is to enforce the Tripartite Data Architecture by separating relational truth, blob storage, semantic vectors, and graph relationships.

## The 4 Pillars

### 1. Postgres (The Relational Spine)
- **Role**: Primary source of truth for structured metadata, IBAC intent tokens, and event sourcing.
- **Constraints**: No raw blobs. High normalization. Every row must have a `provenance_sha` linking back to the source document.
- **Access**: Full IBAC gating. Agents interact via ORM or strict CRUD APIs, never raw SQL.

### 2. MinIO (The Blob / Bloat Vault)
- **Role**: S3-compatible object storage for all raw ingested files, PDFs, transcripts, and images. 
- **Constraints**: Files are immutable. Once written, they are appended only. Versioning enabled.
- **Access**: Agents access via pre-signed URLs.

### 3. Qdrant (The Semantic Vector Store)
- **Role**: High-performance semantic search for the unstructured data residing in MinIO.
- **Constraints**: Every vector MUST carry a payload containing `{ "doc_id": "minio_uuid", "author": "agent_id" }` to guarantee attribution.
- **Access**: Search only. Deletions are cascaded from Postgres.

### 4. Neo4j (The Knowledge Graph)
- **Role**: Mapping the relationships between entities (e.g., Client X -> owns -> Asset Y -> requires -> Insight Z).
- **Constraints**: Nodes are strictly typed. Edges must represent deterministic relationships, not probabilistic guesses.

## Hand-off to Devon
Devon: Take this blueprint and instantiate the `docker-compose.yml` services for Postgres, MinIO, Qdrant, and Neo4j. Ensure they are placed on the `amplified-net` internal network, entirely isolated from public ingress.

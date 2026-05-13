# Step 8: pgvectorscale Install — PG15 Build Test First

AMP-331 | Devon-0178 | 2026-05-13

## Current State

- pgvectorscale is **not installed** on cove-postgres
- pgvector 0.8.2 is installed and working (163,554 vectors, HNSW)
- At current scale (163K vectors × 384-dim), HNSW is comfortable
- The crossover where DiskANN (StreamingDiskANN) adds value is ~2–5M vectors

## Decision: Defer Install (OPINION 88%)

pgvectorscale adds zero overhead when unused, but the install requires building
from source against the timescaledb-ha image which has a custom PG15 layout.
The risk-benefit ratio doesn't justify it at 163K vectors.

**Install when:** approaching 1M vectors, or during the PG15→PG16 upgrade (which
will use a fresh image and can include pgvectorscale in the base build).

## Install Procedure (when ready)

### Prerequisites

- PG15 development headers available in the container
- Rust toolchain (pgvectorscale is written in Rust via pgrx)
- `pgvector` 0.7.0+ already installed ✓

### Option A: Build from source inside the container

```bash
# Enter the container as root
docker exec -u root -it cove-postgres bash

# Install build dependencies
apt-get update && apt-get install -y \
  build-essential \
  pkg-config \
  libssl-dev \
  postgresql-server-dev-15 \
  curl

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source "$HOME/.cargo/env"

# Install cargo-pgrx (must match pgvectorscale's expected version)
# Check pgvectorscale's Cargo.toml for the pinned pgrx version
cargo install cargo-pgrx --version 0.12.9 --locked

# Initialize pgrx for PG15
cargo pgrx init --pg15=$(which pg_config)

# Clone and build pgvectorscale
cd /tmp
git clone --depth 1 --branch 0.9.0 https://github.com/timescale/pgvectorscale.git
cd pgvectorscale/pgvectorscale

# Build and install
cargo pgrx install --release --pg-config=$(which pg_config)

# Verify the extension is available
psql -U cove -d amplified_brain -c "SELECT * FROM pg_available_extensions WHERE name = 'vectorscale'"
```

### Option B: Use Timescale's pre-built packages (preferred if available)

The `timescaledb-ha` image may include pgvectorscale in newer tags. Check:

```bash
# Check if a newer image tag includes pgvectorscale
docker pull timescale/timescaledb-ha:pg15-latest
docker run --rm timescale/timescaledb-ha:pg15-latest \
  psql -U postgres -c "SELECT * FROM pg_available_extensions WHERE name = 'vectorscale'"
```

If available, update the docker-compose to use the newer image tag. This is
cleaner than building from source.

### Post-install (either option)

```sql
-- Create the extension (does NOT require restart)
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;

-- Verify
SELECT extname, extversion FROM pg_extension WHERE extname = 'vectorscale';

-- At this point, you can create StreamingDiskANN indexes:
-- CREATE INDEX idx_kv_diskann ON knowledge_vectors
--   USING diskann (embedding halfvec_cosine_ops)
--   WITH (num_neighbors = 50);
--
-- But do NOT create this index until you have 2M+ vectors.
-- Below that threshold, HNSW outperforms DiskANN on latency.
```

### Rollback

```sql
DROP EXTENSION IF EXISTS vectorscale;
-- The .so file remains on disk but is harmless if the extension is dropped.
-- Remove build artifacts: rm -rf /tmp/pgvectorscale
```

## Capacity Reference

Beast hardware: 256 GB RAM, 96 threads, 1.4 TB free disk.

| Vectors | Dimensions | Index Type | Index Size | Build Time | Query p99 |
|---------|------------|------------|------------|------------|-----------|
| 163K | 384 | HNSW | ~244 MB | ~2 min | <5 ms |
| 1M | 384 | HNSW | ~1.5 GB | ~15 min | <10 ms |
| 1M | 1536 | HNSW | ~6 GB | ~60 min | <15 ms |
| 5M | 1536 | HNSW | ~30 GB | ~5 hr | <50 ms |
| 5M | 1536 | DiskANN | ~10 GB | ~2 hr | <20 ms |
| 10M | 1536 | DiskANN | ~20 GB | ~4 hr | <30 ms |

Sources: pgvector benchmarks (2025), pgvectorscale release notes v0.8.0–v0.9.0.
Numbers are estimates scaled from published benchmarks — actual Beast performance
will vary. Benchmark before migrating production indexes.

---

*Devon-0178 | 2026-05-13 | session devin-01787ef6cd57476aacdb0f1dfe10b069*

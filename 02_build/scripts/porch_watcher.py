#!/usr/bin/env python3
"""
Porch Watcher — Deterministic file ingestion pipeline for Amplified Partners
============================================================================

Watches /opt/amplified-machine/porch/incoming/ for new files.
Labels them with PUDDING taxonomy, then ingests into Qdrant.
FalkorDB ingestion runs separately (via the existing graphiti ingestion script).

Flow: incoming/ → label → Qdrant embed → labeled/ (success) or failed/ (error)

Run as: python3 porch_watcher.py          (single pass)
        python3 porch_watcher.py --watch   (continuous, checks every 60s)
        python3 porch_watcher.py --dry-run (label only, don't ingest)
"""

import json
import os
import shutil
import sys
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

# Import the PUDDING labeler
sys.path.insert(0, str(Path(__file__).parent))
from pudding_labeler import label_document

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PORCH_DIR = Path("/opt/amplified-machine/porch")
INCOMING_DIR = PORCH_DIR / "incoming"
LABELED_DIR = PORCH_DIR / "labeled"
INGESTED_DIR = PORCH_DIR / "ingested"
FAILED_DIR = PORCH_DIR / "failed"
LABELS_LOG = PORCH_DIR / "labels_log.jsonl"
WATCHER_LOG = PORCH_DIR / "watcher_log.jsonl"

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "amplified_knowledge")

# Supported file types
SUPPORTED_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}


def log_event(event: dict):
    """Append event to JSONL log."""
    event["timestamp"] = datetime.now().isoformat()
    with open(WATCHER_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")


def file_hash(filepath: Path) -> str:
    """SHA-256 hash of file content for dedup."""
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def embed_and_store(filepath: Path, label: dict, dry_run: bool = False) -> bool:
    """Embed document and store in Qdrant."""
    if dry_run:
        print(f"  [DRY RUN] Would embed: {filepath.name}")
        return True

    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import PointStruct
        import requests

        content = filepath.read_text(encoding="utf-8", errors="replace")

        # Use Ollama for embeddings (same as existing vault ingestion)
        try:
            resp = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": "nomic-embed-text", "prompt": content[:8000]},
                timeout=30,
            )
            resp.raise_for_status()
            vector = resp.json()["embedding"]
        except Exception as e:
            print(f"  [WARN] Ollama embedding failed: {e}")
            print(f"  [WARN] File will be labeled but not embedded")
            return False

        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

        # Build payload with PUDDING label
        payload = {
            "filename": filepath.name,
            "content": content[:10000],  # Truncate for storage
            "pudding_label": label.get("pudding_label", ""),
            "pudding_what": label.get("what", ""),
            "pudding_how": label.get("how", ""),
            "pudding_scale": label.get("scale", ""),
            "pudding_time": label.get("time", ""),
            "pudding_patterns": label.get("patterns", []),
            "word_count": label.get("word_count", 0),
            "source": "porch",
            "ingested_at": datetime.now().isoformat(),
            "file_hash": file_hash(filepath),
        }

        # Generate a deterministic ID from the file hash
        point_id = int(hashlib.md5(filepath.name.encode()).hexdigest()[:16], 16)

        client.upsert(
            collection_name=QDRANT_COLLECTION,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)],
        )

        print(f"  [QDRANT] Embedded: {filepath.name} → {len(vector)}d vector")
        return True

    except ImportError:
        print(f"  [WARN] qdrant-client not installed. Label only, no embedding.")
        return False
    except Exception as e:
        print(f"  [ERROR] Qdrant ingestion failed: {e}")
        return False


def process_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single file through the porch pipeline."""
    print(f"\n{'='*50}")
    print(f"Processing: {filepath.name}")

    # Step 1: Label with PUDDING
    label = label_document(str(filepath))
    if "error" in label:
        print(f"  [ERROR] Labeling failed: {label['error']}")
        shutil.move(str(filepath), str(FAILED_DIR / filepath.name))
        log_event({"event": "label_failed", "file": filepath.name, "error": label["error"]})
        return False

    print(f"  [PUDDING] {label['pudding_label']}")
    print(f"    WHAT:  [{label['what']}] {label['what_desc']}")
    print(f"    HOW:   [{label['how']}] {label['how_desc']}")
    print(f"    SCALE: [{label['scale']}] {label['scale_desc']}")
    print(f"    TIME:  [{label['time']}] {label['time_desc']}")
    if label.get("patterns"):
        print(f"    PATTERNS: {', '.join(label['patterns'])}")

    # Log the label
    with open(LABELS_LOG, "a") as f:
        f.write(json.dumps(label) + "\n")

    # Step 2: Embed in Qdrant
    embedded = embed_and_store(filepath, label, dry_run=dry_run)

    # Step 3: Move to appropriate directory
    if dry_run:
        dest = LABELED_DIR / filepath.name
    elif embedded:
        dest = INGESTED_DIR / filepath.name
    else:
        dest = LABELED_DIR / filepath.name  # Labeled but not embedded — still progress

    if not dry_run:
        shutil.move(str(filepath), str(dest))
        print(f"  [MOVED] → {dest.parent.name}/{dest.name}")

    log_event({
        "event": "file_processed",
        "file": filepath.name,
        "label": label.get("pudding_label", ""),
        "embedded": embedded,
        "destination": str(dest.parent.name),
    })

    return True


def scan_incoming(dry_run: bool = False) -> int:
    """Scan incoming directory and process all files."""
    files = [f for f in INCOMING_DIR.iterdir() if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS]

    if not files:
        return 0

    print(f"\n{'#'*60}")
    print(f"  PORCH WATCHER — {len(files)} files in incoming")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}")

    processed = 0
    for filepath in sorted(files):
        try:
            if process_file(filepath, dry_run=dry_run):
                processed += 1
        except Exception as e:
            print(f"  [FATAL] {filepath.name}: {e}")
            try:
                shutil.move(str(filepath), str(FAILED_DIR / filepath.name))
            except Exception:
                pass
            log_event({"event": "fatal_error", "file": filepath.name, "error": str(e)})

    print(f"\nProcessed: {processed}/{len(files)}")
    return processed


def watch_mode(dry_run: bool = False, interval: int = 60):
    """Continuous watch mode — check every interval seconds."""
    print(f"Porch Watcher running in watch mode (every {interval}s)")
    print(f"Watching: {INCOMING_DIR}")
    print(f"Press Ctrl+C to stop\n")

    while True:
        count = scan_incoming(dry_run=dry_run)
        if count > 0:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Processed {count} files. Waiting...")
        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Porch Watcher — PUDDING labeling pipeline")
    parser.add_argument("--watch", action="store_true", help="Continuous watch mode")
    parser.add_argument("--dry-run", action="store_true", help="Label only, don't ingest or move")
    parser.add_argument("--interval", type=int, default=60, help="Watch interval in seconds (default: 60)")
    args = parser.parse_args()

    # Ensure directories exist
    for d in [INCOMING_DIR, LABELED_DIR, INGESTED_DIR, FAILED_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    if args.watch:
        watch_mode(dry_run=args.dry_run, interval=args.interval)
    else:
        scan_incoming(dry_run=args.dry_run)

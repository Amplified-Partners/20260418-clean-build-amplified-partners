#!/usr/bin/env python3
import os
import hashlib
from pathlib import Path

KNOWLEDGE_ROOT = Path("/Users/ewansair/Vaults/Ewan")

def dedupe():
    seen_hashes = set()
    duplicates_removed = 0
    total_scanned = 0

    for root, _, files in os.walk(KNOWLEDGE_ROOT):
        for file in files:
            if file.endswith(('.md', '.txt', '.jsonl', '.json')):
                file_path = Path(root) / file
                total_scanned += 1
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    file_hash = hashlib.sha256(content).hexdigest()
                    
                    if file_hash in seen_hashes:
                        os.remove(file_path)
                        duplicates_removed += 1
                    else:
                        seen_hashes.add(file_hash)
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")

    print(f"Scanned: {total_scanned}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Unique files remaining: {len(seen_hashes)}")

if __name__ == '__main__':
    dedupe()

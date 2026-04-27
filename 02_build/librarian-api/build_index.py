#!/usr/bin/env python3
"""
Librarian Index Builder
=======================
Crawls the knowledge base directory and builds a high-speed SQLite FTS5 index.
"""

import sqlite3
from pathlib import Path
import os

SCRIPT_DIR = Path(__file__).parent
LIBRARIAN_DB = SCRIPT_DIR / "librarian.db"
KNOWLEDGE_ROOT = Path("/Users/ewansair/Vaults/Ewan")

def build_index():
    print(f"Building FTS Index for: {KNOWLEDGE_ROOT}")
    
    if LIBRARIAN_DB.exists():
        LIBRARIAN_DB.unlink()
        print("Removed old index.")

    conn = sqlite3.connect(str(LIBRARIAN_DB))
    cursor = conn.cursor()

    # Create the virtual table for full-text search
    cursor.execute('''
        CREATE VIRTUAL TABLE atoms_fts USING fts5(
            path, 
            content
        )
    ''')
    
    # Create a standard table to hold actual data
    cursor.execute('''
        CREATE TABLE atoms (
            path TEXT PRIMARY KEY,
            content TEXT
        )
    ''')

    count = 0
    # Walk through the knowledge root and index all markdown files
    for root, _, files in os.walk(KNOWLEDGE_ROOT):
        for file in files:
            if file.endswith(('.md', '.txt', '.jsonl', '.json')):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Insert into both standard and FTS tables
                    cursor.execute('INSERT INTO atoms (path, content) VALUES (?, ?)', (str(file_path), content))
                    cursor.execute('INSERT INTO atoms_fts (rowid, path, content) VALUES (last_insert_rowid(), ?, ?)', (str(file_path), content))
                    
                    count += 1
                except Exception as e:
                    print(f"Failed to read {file_path}: {e}")

    conn.commit()
    conn.close()
    print(f"Successfully indexed {count} markdown atoms.")

if __name__ == "__main__":
    build_index()

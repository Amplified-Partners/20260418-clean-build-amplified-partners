#!/usr/bin/env python3
"""
Librarian API - Expose knowledge base search via REST API
Enables Perplexity and other tools to query your 41,000+ atoms
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from pathlib import Path
from datetime import datetime
import os

# Configuration
# Use relative path for Railway deployment
SCRIPT_DIR = Path(__file__).parent
LIBRARIAN_DB = SCRIPT_DIR / "librarian.db"
KNOWLEDGE_ROOT = Path("/Users/ewanbramley/Knowledge")
ATOMS_DIR = KNOWLEDGE_ROOT / "02-atoms"

# Initialize FastAPI
app = FastAPI(
    title="Librarian API",
    description="Search API for Ewan's Second Brain (41,000+ atoms)",
    version="1.0.0"
)

# Enable CORS for Perplexity and other clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class SearchResult(BaseModel):
    file_path: str
    content: str
    score: float
    file_name: str
    directory: str

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_found: int
    search_time_ms: float

class AtomResponse(BaseModel):
    atom_id: str
    content: str
    file_path: str
    exists: bool

class StatsResponse(BaseModel):
    total_atoms: int
    total_size_mb: float
    last_updated: str
    directories: dict

# Helper functions
def get_db_connection():
    """Get SQLite database connection"""
    if not LIBRARIAN_DB.exists():
        raise HTTPException(status_code=500, detail="Librarian database not found")
    return sqlite3.connect(str(LIBRARIAN_DB))

def format_content(content: str, max_length: int = 500) -> str:
    """Format content for display"""
    if len(content) <= max_length:
        return content
    return content[:max_length] + "..."

# API Endpoints

@app.get("/")
async def root():
    """API root - health check"""
    return {
        "status": "healthy",
        "service": "Librarian API",
        "version": "1.0.0",
        "knowledge_base": "Ewan's Second Brain",
        "total_atoms": count_atoms()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/search", response_model=SearchResponse)
async def search_knowledge(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results to return"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum relevance score")
):
    """
    Search the knowledge base using full-text search
    
    Returns relevant atoms ranked by relevance score
    """
    start_time = datetime.now()
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if FTS table exists, if not use simple search
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='atoms_fts'
        """)
        
        has_fts = cursor.fetchone() is not None
        
        if has_fts:
            # Use full-text search with JOIN to get path
            cursor.execute("""
                SELECT a.path, a.content, atoms_fts.rank
                FROM atoms_fts
                JOIN atoms a ON atoms_fts.rowid = a.rowid
                WHERE atoms_fts MATCH ?
                ORDER BY atoms_fts.rank
                LIMIT ?
            """, (query, limit))
        else:
            # Fallback to LIKE search
            cursor.execute("""
                SELECT path, content,
                       (LENGTH(content) - LENGTH(REPLACE(LOWER(content), LOWER(?), ''))) / LENGTH(?) as score
                FROM atoms
                WHERE LOWER(content) LIKE LOWER(?)
                ORDER BY score DESC
                LIMIT ?
            """, (query, query, f"%{query}%", limit))
        
        results = cursor.fetchall()
        conn.close()
        
        # Format results
        search_results = []
        for row in results:
            file_path = Path(row[0])
            search_results.append(SearchResult(
                file_path=str(file_path),
                content=format_content(row[1]),
                score=abs(float(row[2])) if row[2] else 0.0,
                file_name=file_path.name,
                directory=str(file_path.parent)
            ))
        
        # Filter by minimum score
        search_results = [r for r in search_results if r.score >= min_score]
        
        end_time = datetime.now()
        search_time = (end_time - start_time).total_seconds() * 1000
        
        return SearchResponse(
            query=query,
            results=search_results,
            total_found=len(search_results),
            search_time_ms=round(search_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/atom/{atom_id}", response_model=AtomResponse)
async def get_atom(atom_id: str):
    """
    Retrieve a specific atom by ID
    
    Atom ID is the filename without extension
    """
    atom_path = ATOMS_DIR / f"{atom_id}.md"
    
    if not atom_path.exists():
        return AtomResponse(
            atom_id=atom_id,
            content="",
            file_path=str(atom_path),
            exists=False
        )
    
    try:
        with open(atom_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return AtomResponse(
            atom_id=atom_id,
            content=content,
            file_path=str(atom_path),
            exists=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading atom: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get knowledge base statistics"""
    try:
        total_atoms = count_atoms()
        total_size = sum(f.stat().st_size for ext in ("*.md", "*.txt", "*.jsonl", "*.json") for f in KNOWLEDGE_ROOT.rglob(ext))
        total_size_mb = total_size / (1024 * 1024)
        
        # Count atoms by directory
        directories = {}
        for ext in ("*.md", "*.txt", "*.jsonl", "*.json"):
            for md_file in KNOWLEDGE_ROOT.rglob(ext):
                dir_name = md_file.parent.name
                directories[dir_name] = directories.get(dir_name, 0) + 1
        
        return StatsResponse(
            total_atoms=total_atoms,
            total_size_mb=round(total_size_mb, 2),
            last_updated=datetime.now().isoformat(),
            directories=directories
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

@app.get("/recent")
async def get_recent_atoms(limit: int = Query(10, ge=1, le=100)):
    """Get recently modified atoms"""
    try:
        atoms = []
        for md_file in KNOWLEDGE_ROOT.rglob("*.md"):
            stat = md_file.stat()
            atoms.append({
                "file_path": str(md_file),
                "file_name": md_file.name,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size": stat.st_size
            })
        
        # Sort by modification time
        atoms.sort(key=lambda x: x["modified"], reverse=True)
        
        return {
            "recent_atoms": atoms[:limit],
            "total_found": len(atoms)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def count_atoms() -> int:
    """Count total atoms in knowledge base"""
    return sum(1 for ext in ("*.md", "*.txt", "*.jsonl", "*.json") for _ in KNOWLEDGE_ROOT.rglob(ext))

# Run server
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║              LIBRARIAN API STARTING                      ║
╠══════════════════════════════════════════════════════════╣
║  Knowledge Base: {KNOWLEDGE_ROOT}
║  Total Atoms: {count_atoms()}
║  Port: {port}
║  Docs: http://localhost:{port}/docs
╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
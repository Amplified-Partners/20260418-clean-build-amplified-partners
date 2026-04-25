"""
Amplified Command Centre — FastAPI Backend
Proxies Beast voice pipeline, serves local task/promise data,
and reports Docker container status.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional, List
import httpx
import asyncio
import subprocess
import json
import search_db
from search_watcher import watcher_loop

app = FastAPI(title="Amplified Command Centre API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:3001"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BEAST_VOICE_URL = "https://voice.beast.amplifiedpartners.ai"
SEARXNG_URL = "https://search.beast.amplifiedpartners.ai"
HTTP_TIMEOUT = 10.0

# ── Models ────────────────────────────────────────────

Status = Literal["PENDING", "KEPT", "MISSED"]
TaskStatus = Literal["TODO", "IN_PROGRESS", "DONE", "BLOCKED", "NEEDS_DETAILS"]
TaskType = Literal["COMM", "WRITING", "R_AND_D", "ADMIN"]
Priority = Literal["HIGH", "MEDIUM", "LOW"]
SessionStatus = Literal["ACTIVE", "PAUSED", "DONE"]


class Promise(BaseModel):
    id: str
    description: str
    origin_event_id: Optional[str] = None
    due_at: datetime
    status: Status
    resolved_at: Optional[datetime] = None


class Task(BaseModel):
    id: str
    title: str
    description: str
    origin_event_id: Optional[str] = None
    session_id: Optional[str] = None
    type: TaskType
    status: TaskStatus
    priority: Priority
    due_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    promise_id: Optional[str] = None


class Session(BaseModel):
    id: str
    focus_title: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: SessionStatus
    tasks_created: List[str] = []
    events: List[str] = []


# ── Seed Data (local, will move to Beast PostgreSQL later) ──

PROMISES = [
    Promise(id="1", description="Call Dave back about Jesmond pilot",
            due_at=datetime(2026, 3, 10, 9, 0), status="KEPT",
            resolved_at=datetime(2026, 3, 10, 9, 5)),
    Promise(id="2", description="Write Pudding follow-up article",
            due_at=datetime(2026, 3, 11, 18, 0), status="MISSED",
            resolved_at=datetime(2026, 3, 12, 10, 0)),
    Promise(id="3", description="Email plumber trialist about weather feature",
            due_at=datetime(2026, 3, 15, 12, 0), status="PENDING"),
    Promise(id="4", description="Send Tyrone the Docker compose config",
            due_at=datetime(2026, 3, 8, 14, 0), status="KEPT",
            resolved_at=datetime(2026, 3, 8, 13, 30)),
    Promise(id="5", description="Review OpenClaw cron schedule",
            due_at=datetime(2026, 3, 9, 10, 0), status="KEPT",
            resolved_at=datetime(2026, 3, 9, 9, 45)),
    Promise(id="6", description="Draft HeyGen demo script for trades vertical",
            due_at=datetime(2026, 3, 12, 16, 0), status="PENDING"),
]

TASKS = [
    Task(id="task-1", title="Finalise command centre V1 layout",
         description="Review and approve the 5-panel layout with Antigravity.",
         type="ADMIN", status="IN_PROGRESS", priority="HIGH",
         due_at=datetime(2026, 3, 12, 17, 0),
         created_at=datetime(2026, 3, 12, 9, 0), updated_at=datetime(2026, 3, 12, 11, 0)),
    Task(id="task-2", title="Email Dave about Jesmond pilot",
         description="From voice at 11:32: 'I need to email Dave about the Jesmond pilot.'",
         origin_event_id="event-1", session_id="session-1",
         type="COMM", status="TODO", priority="HIGH",
         due_at=datetime(2026, 3, 12, 16, 0),
         created_at=datetime(2026, 3, 12, 11, 32), updated_at=datetime(2026, 3, 12, 11, 32)),
    Task(id="task-3", title="Write Pudding Logic blog post draft",
         description="Cross-industry insight piece: F1 pit-stop timing applied to accounting audits.",
         type="WRITING", status="TODO", priority="MEDIUM",
         due_at=datetime(2026, 3, 13, 12, 0),
         created_at=datetime(2026, 3, 12, 10, 15), updated_at=datetime(2026, 3, 12, 10, 15)),
    Task(id="task-4", title="Check Beast Qdrant indexing status",
         description="Verify the 1.2M word Pudding Vault is fully indexed on Hetzner.",
         type="R_AND_D", status="TODO", priority="LOW",
         due_at=datetime(2026, 3, 14, 10, 0),
         created_at=datetime(2026, 3, 11, 14, 0), updated_at=datetime(2026, 3, 11, 14, 0)),
]

CURRENT_SESSION = Session(
    id="session-1", focus_title="Command Centre V1 build",
    started_at=datetime(2026, 3, 12, 11, 30), status="ACTIVE",
    tasks_created=["task-1", "task-2"], events=["event-1", "event-2"],
)


# ══════════════════════════════════════════════════════
# LOCAL ENDPOINTS (tasks, promises, sessions)
# ══════════════════════════════════════════════════════

@app.get("/api/promises", response_model=List[Promise])
def list_promises():
    return PROMISES

@app.get("/api/tasks", response_model=List[Task])
def list_tasks():
    return TASKS

@app.get("/api/sessions/current", response_model=Session)
def get_current_session():
    return CURRENT_SESSION


# ══════════════════════════════════════════════════════
# BEAST PROXY (voice pipeline on Hetzner)
# ══════════════════════════════════════════════════════

@app.get("/api/beast/stats")
async def beast_stats():
    """Proxy to Beast voice pipeline stats."""
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            r = await client.get(f"{BEAST_VOICE_URL}/api/stats")
            return r.json()
    except Exception:
        return {"error": "upstream unavailable", "source": "beast_voice_pipeline"}


@app.get("/api/beast/transcripts")
async def beast_transcripts():
    """Proxy to Beast voice pipeline transcripts."""
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            r = await client.get(f"{BEAST_VOICE_URL}/api/transcripts")
            return r.json()
    except Exception:
        return {"error": "upstream unavailable", "source": "beast_voice_pipeline"}


@app.get("/api/beast/briefings")
async def beast_briefings():
    """Proxy to Beast voice pipeline briefings."""
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            r = await client.get(f"{BEAST_VOICE_URL}/api/briefings")
            return r.json()
    except Exception:
        return {"error": "upstream unavailable", "source": "beast_voice_pipeline"}


# ════════════════════════════════════════════════════════
# MONITORING (Enforcer, Kaizen, FalkorDB)
# ════════════════════════════════════════════════════════

@app.get("/api/enforcer/health")
async def enforcer_health():
    """Get Enforcer health status from Beast via SSH (internal network only)."""
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            ["ssh", "-o", "ConnectTimeout=5", "root@beast.amplifiedpartners.ai",
             "docker exec enforcer python -c 'import httpx; r = httpx.get(\"http://localhost:8000/health/detailed\"); print(r.text)'"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        return {"overall_health": "unknown", "error": result.stderr[:200] if result.stderr else "no output"}
    except Exception:
        return {"overall_health": "error", "error": "connection failed"}


@app.get("/api/kaizen/health")
async def kaizen_health():
    """Get Kaizen optimizer health from Beast via SSH."""
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            ["ssh", "-o", "ConnectTimeout=5", "root@beast.amplifiedpartners.ai",
             "docker exec kaizen-optimizer python -c 'import httpx; r = httpx.get(\"http://localhost:8080/health/detailed\"); print(r.text)'"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        return {"overall_health": "unknown", "error": result.stderr[:200] if result.stderr else "no output"}
    except Exception:
        return {"overall_health": "error", "error": "connection failed"}


@app.get("/api/graphiti/stats")
async def graphiti_stats():
    """Get FalkorDB Business Brain graph stats from local OrbStack."""
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            ["/Users/amplifiedpartners/agent-stack/graphiti-ingestion/.venv/bin/python3", "-c", """
import json
from falkordb import FalkorDB
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('amplified_brain')
stats = {}
for label, query in [
    ('documents', 'MATCH (d:Document) RETURN count(d)'),
    ('categories', 'MATCH (c:Category) RETURN count(c)'),
    ('entities', 'MATCH (n) WHERE NOT n:Document AND NOT n:Category AND NOT n:AIMemory AND NOT n:AISession AND NOT n:AIRegistry RETURN count(n)'),
    ('relationships', 'MATCH ()-[r]->() RETURN count(r)'),
    ('ai_memories', 'MATCH (m:AIMemory) RETURN count(m)'),
    ('cross_references', 'MATCH ()-[r:CROSS_REFERENCES]->() RETURN count(r)'),
]:
    try:
        r = graph.query(query)
        stats[label] = r.result_set[0][0]
    except:
        stats[label] = 0
print(json.dumps(stats))
"""],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        return {"error": result.stderr[:200] if result.stderr else "no output"}
    except Exception:
        return {"error": "graph query failed"}


# ════════════════════════════════════════════════════════
# SEARCH INTELLIGENCE (SearXNG + persistence + watched searches)
# ════════════════════════════════════════════════════════

@app.get("/api/search")
async def search(q: str, categories: str = "general", page: int = 1):
    """Search via SearXNG and auto-save results."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(
                f"{SEARXNG_URL}/search",
                params={"q": q, "format": "json", "categories": categories, "pageno": page},
            )
            data = r.json()
            results = []
            for item in data.get("results", [])[:15]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "engine": item.get("engine", ""),
                })
            total = len(data.get("results", []))

            # Auto-save every search
            search_id = search_db.save_search(q, categories, results, total)

            return {
                "query": q,
                "results": results,
                "total": total,
                "categories": categories,
                "search_id": search_id,
                "is_watched": search_db.is_watched(q),
            }
    except Exception:
        return {"error": "search unavailable", "query": q, "results": []}


@app.get("/api/searches")
async def list_searches(limit: int = 30):
    """List recent searches."""
    return {"searches": search_db.get_recent_searches(limit)}


@app.get("/api/searches/watched")
async def list_watched():
    """List all watched searches."""
    return {"watched": search_db.get_watched_searches()}


@app.get("/api/searches/{search_id}")
async def get_search(search_id: int):
    """Get a single search with full results."""
    result = search_db.get_search_by_id(search_id)
    if result:
        return result
    return {"error": "Search not found"}


@app.post("/api/searches/watch")
async def watch(query: str, categories: str = "general", schedule: str = "daily"):
    """Start watching a search query."""
    record = search_db.watch_search(query, categories, schedule)
    return {"status": "watching", "watch": record}


@app.delete("/api/searches/watch")
async def unwatch(query: str):
    """Stop watching a search query."""
    removed = search_db.unwatch_search(query)
    return {"status": "unwatched" if removed else "not_found"}


@app.get("/api/searches/diffs")
async def get_diffs(query: str, limit: int = 10):
    """Get diff history for a watched search."""
    return {"diffs": search_db.get_diffs_for_query(query, limit)}


@app.post("/api/searches/seen")
async def mark_seen(query: str):
    """Mark a watched search's changes as seen."""
    search_db.clear_changes(query)
    return {"status": "cleared"}



# ══════════════════════════════════════════════════════

def _get_local_containers() -> list:
    """Get local Docker container status via CLI (OrbStack or Docker Desktop)."""
    import os
    try:
        # OrbStack uses a custom socket path
        env = os.environ.copy()
        orbstack_sock = os.path.expanduser("~/.orbstack/run/docker.sock")
        if os.path.exists(orbstack_sock):
            env["DOCKER_HOST"] = f"unix://{orbstack_sock}"

        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}|{{.Status}}|{{.Image}}|{{.Ports}}"],
            capture_output=True, text=True, timeout=5, env=env,
        )
        if result.returncode != 0:
            return []
        containers = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 3:
                name = parts[0]
                status_str = parts[1]
                image = parts[2]
                # Determine health
                if "healthy" in status_str.lower():
                    health = "healthy"
                elif "unhealthy" in status_str.lower():
                    health = "unhealthy"
                else:
                    health = "running"
                containers.append({
                    "name": name,
                    "status": status_str,
                    "image": image,
                    "health": health,
                    "location": "mac",
                })
        return containers
    except Exception:
        return []


def _get_beast_containers_via_ssh() -> list:
    """Get Beast container status via SSH."""
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no",
             "root@beast.amplifiedpartners.ai",
             "docker ps --format '{{.Names}}|{{.Status}}|{{.Image}}'"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return []
        containers = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 3:
                name = parts[0]
                status_str = parts[1]
                image = parts[2]
                if "healthy" in status_str.lower():
                    health = "healthy"
                elif "unhealthy" in status_str.lower():
                    health = "unhealthy"
                else:
                    health = "running"
                containers.append({
                    "name": name,
                    "status": status_str,
                    "image": image,
                    "health": health,
                    "location": "beast",
                })
        return containers
    except Exception:
        return []


@app.get("/api/infra/containers")
async def infra_containers():
    """Get container status from both Mac and Beast."""
    loop = asyncio.get_event_loop()
    # Run both in thread pool to avoid blocking
    local_future = loop.run_in_executor(None, _get_local_containers)
    beast_future = loop.run_in_executor(None, _get_beast_containers_via_ssh)
    local, beast = await asyncio.gather(local_future, beast_future)
    return {
        "mac": local,
        "beast": beast,
        "mac_count": len(local),
        "beast_count": len(beast),
        "total": len(local) + len(beast),
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/infra/containers/mac")
async def infra_mac_containers():
    """Get Mac-local container status only (fast, no SSH)."""
    loop = asyncio.get_event_loop()
    containers = await loop.run_in_executor(None, _get_local_containers)
    return {"containers": containers, "count": len(containers)}


# ══════════════════════════════════════════════════════
# HEALTH
# ══════════════════════════════════════════════════════

@app.get("/api/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# ══════════════════════════════════════════════════════
# STARTUP — Background tasks
# ══════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    """Start the search watcher background task."""
    asyncio.create_task(watcher_loop())

"""
Event Log API Routes - Query and manage logged events
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from prisma import Prisma
from src.db.client import get_prisma
from src.services.event_log import get_event_log_service

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
async def list_events(
    source: Optional[str] = None,
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    since: Optional[str] = None,
    limit: int = 100,
    db: Prisma = Depends(get_prisma),
):
    """List events with optional filters."""
    service = get_event_log_service(db)
    events = await service.list(
        source=source,
        event_type=event_type,
        status=status,
        client_id=client_id,
        since=since,
        limit=min(limit, 500),
    )
    return {"events": events, "total": len(events)}


@router.get("/stats")
async def get_event_stats(db: Prisma = Depends(get_prisma)):
    """Get event statistics."""
    service = get_event_log_service(db)
    return await service.get_stats()


@router.get("/{event_id}")
async def get_event(event_id: str, db: Prisma = Depends(get_prisma)):
    """Get event details including full payload."""
    service = get_event_log_service(db)
    event = await service.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{event_id}/retry")
async def retry_event(event_id: str, db: Prisma = Depends(get_prisma)):
    """Retry processing a failed event."""
    service = get_event_log_service(db)
    success = await service.retry(event_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Cannot retry this event (not failed or not found)"
        )
    return {"message": "Event queued for retry", "event_id": event_id}


@router.post("/cleanup")
async def cleanup_old_events(days: int = 30, db: Prisma = Depends(get_prisma)):
    """Delete events older than N days (admin)."""
    service = get_event_log_service(db)
    deleted = await service.cleanup_old_events(days)
    return {"message": f"Deleted {deleted} old events", "days": days}

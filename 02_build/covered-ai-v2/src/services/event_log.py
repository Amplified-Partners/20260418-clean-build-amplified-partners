"""
Event Log Service - Centralized event logging and retrieval

Features:
- Log all webhook events to database
- Link events to entities (client, call, invoice, etc.)
- Query and filter events
- Retry failed event processing
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum

from prisma import Prisma


class EventSource(str, Enum):
    VAPI = "vapi"
    TWILIO = "twilio"
    STRIPE = "stripe"
    RESEND = "resend"
    MANUAL = "manual"


class EventStatus(str, Enum):
    RECEIVED = "received"
    PROCESSED = "processed"
    FAILED = "failed"


class EventLogService:
    def __init__(self, db: Prisma):
        self.db = db

    async def log(
        self,
        source: EventSource,
        event_type: str,
        payload: Dict[str, Any],
        client_id: Optional[str] = None,
        call_id: Optional[str] = None,
        invoice_id: Optional[str] = None,
        porting_id: Optional[str] = None,
        demo_number_id: Optional[str] = None,
    ) -> str:
        """Log an incoming event. Returns event ID."""
        event = await self.db.eventlog.create(
            data={
                "source": source.value,
                "eventType": event_type,
                "status": EventStatus.RECEIVED.value,
                "payload": payload,
                "clientId": client_id,
                "callId": call_id,
                "invoiceId": invoice_id,
                "portingId": porting_id,
                "demoNumberId": demo_number_id,
            }
        )
        return event.id

    async def mark_processed(
        self,
        event_id: str,
        response: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Mark event as successfully processed."""
        await self.db.eventlog.update(
            where={"id": event_id},
            data={
                "status": EventStatus.PROCESSED.value,
                "response": response,
                "processedAt": datetime.utcnow(),
            }
        )

    async def mark_failed(
        self,
        event_id: str,
        error: str,
    ) -> None:
        """Mark event as failed."""
        await self.db.eventlog.update(
            where={"id": event_id},
            data={
                "status": EventStatus.FAILED.value,
                "error": error,
                "processedAt": datetime.utcnow(),
            }
        )

    async def get(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get event by ID."""
        event = await self.db.eventlog.find_unique(where={"id": event_id})
        if not event:
            return None
        return self._serialize_event(event)

    async def list(
        self,
        source: Optional[str] = None,
        event_type: Optional[str] = None,
        status: Optional[str] = None,
        client_id: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """List events with filters."""
        where: Dict[str, Any] = {}

        if source:
            where["source"] = source
        if event_type:
            where["eventType"] = event_type
        if status:
            where["status"] = status
        if client_id:
            where["clientId"] = client_id
        if since:
            where["createdAt"] = {"gte": datetime.fromisoformat(since.replace("Z", "+00:00"))}

        events = await self.db.eventlog.find_many(
            where=where,
            order={"createdAt": "desc"},
            take=limit,
        )

        return [self._serialize_event(e) for e in events]

    async def get_stats(self) -> Dict[str, Any]:
        """Get event statistics."""
        # Count by source
        by_source: Dict[str, int] = {}
        for source in EventSource:
            count = await self.db.eventlog.count(where={"source": source.value})
            if count > 0:
                by_source[source.value] = count

        # Count by status
        by_status: Dict[str, int] = {}
        for status in EventStatus:
            count = await self.db.eventlog.count(where={"status": status.value})
            if count > 0:
                by_status[status.value] = count

        total = await self.db.eventlog.count()

        return {
            "total": total,
            "by_source": by_source,
            "by_status": by_status,
        }

    async def retry(self, event_id: str) -> bool:
        """Retry processing a failed event."""
        event = await self.db.eventlog.find_unique(where={"id": event_id})
        if not event or event.status != EventStatus.FAILED.value:
            return False

        # Reset status
        await self.db.eventlog.update(
            where={"id": event_id},
            data={
                "status": EventStatus.RECEIVED.value,
                "error": None,
                "processedAt": None,
            }
        )

        # TODO: Re-trigger processing based on source/event_type
        # This would call the appropriate handler based on event.source

        return True

    async def cleanup_old_events(self, days: int = 30) -> int:
        """Delete events older than N days. Run periodically."""
        cutoff = datetime.utcnow() - timedelta(days=days)

        result = await self.db.eventlog.delete_many(
            where={"createdAt": {"lt": cutoff}}
        )

        return result

    def _serialize_event(self, event) -> Dict[str, Any]:
        """Convert Prisma event to dict."""
        return {
            "id": event.id,
            "source": event.source,
            "event_type": event.eventType,
            "status": event.status,
            "payload": event.payload,
            "response": event.response,
            "error": event.error,
            "client_id": event.clientId,
            "call_id": event.callId,
            "invoice_id": event.invoiceId,
            "porting_id": event.portingId,
            "demo_number_id": event.demoNumberId,
            "created_at": event.createdAt.isoformat() if event.createdAt else None,
            "processed_at": event.processedAt.isoformat() if event.processedAt else None,
        }


def get_event_log_service(db: Prisma) -> EventLogService:
    """Factory function for dependency injection."""
    return EventLogService(db)

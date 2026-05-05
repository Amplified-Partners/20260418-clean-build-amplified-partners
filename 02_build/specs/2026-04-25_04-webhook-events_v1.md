---
title: "Module 4: Webhook Receiver + Event Log"
id: "04-webhook-events"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 4: Webhook Receiver + Event Log

## Overview
Centralized webhook handling for Vapi, Twilio, Stripe, Resend. Log all events for debugging.

## Files to Create

### 1. src/services/event_log.py

```python
"""
Event Log Service - Centralized event logging and retrieval

Features:
- Log all webhook events
- Link events to entities (client, call, invoice, etc.)
- Query and filter events
- Retry failed event processing
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
import uuid


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
    def __init__(self):
        self.events: Dict[str, Dict[str, Any]] = {}  # Replace with DB
    
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
        event_id = str(uuid.uuid4())[:12]
        
        self.events[event_id] = {
            "id": event_id,
            "source": source.value,
            "event_type": event_type,
            "status": EventStatus.RECEIVED.value,
            "payload": payload,
            "response": None,
            "error": None,
            "client_id": client_id,
            "call_id": call_id,
            "invoice_id": invoice_id,
            "porting_id": porting_id,
            "demo_number_id": demo_number_id,
            "created_at": datetime.utcnow().isoformat(),
            "processed_at": None,
        }
        
        return event_id
    
    async def mark_processed(
        self,
        event_id: str,
        response: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Mark event as successfully processed."""
        if event_id in self.events:
            self.events[event_id]["status"] = EventStatus.PROCESSED.value
            self.events[event_id]["response"] = response
            self.events[event_id]["processed_at"] = datetime.utcnow().isoformat()
    
    async def mark_failed(
        self,
        event_id: str,
        error: str,
    ) -> None:
        """Mark event as failed."""
        if event_id in self.events:
            self.events[event_id]["status"] = EventStatus.FAILED.value
            self.events[event_id]["error"] = error
            self.events[event_id]["processed_at"] = datetime.utcnow().isoformat()
    
    async def get(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get event by ID."""
        return self.events.get(event_id)
    
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
        events = list(self.events.values())
        
        if source:
            events = [e for e in events if e["source"] == source]
        if event_type:
            events = [e for e in events if e["event_type"] == event_type]
        if status:
            events = [e for e in events if e["status"] == status]
        if client_id:
            events = [e for e in events if e["client_id"] == client_id]
        if since:
            events = [e for e in events if e["created_at"] >= since]
        
        return sorted(events, key=lambda x: x["created_at"], reverse=True)[:limit]
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get event statistics."""
        events = list(self.events.values())
        
        by_source = {}
        by_status = {}
        
        for e in events:
            source = e["source"]
            status = e["status"]
            
            by_source[source] = by_source.get(source, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total": len(events),
            "by_source": by_source,
            "by_status": by_status,
        }
    
    async def retry(self, event_id: str) -> bool:
        """Retry processing a failed event."""
        event = self.events.get(event_id)
        if not event or event["status"] != EventStatus.FAILED.value:
            return False
        
        # Reset status
        event["status"] = EventStatus.RECEIVED.value
        event["error"] = None
        event["processed_at"] = None
        
        # TODO: Re-trigger processing based on source/event_type
        # This would call the appropriate handler based on event["source"]
        
        return True
    
    async def cleanup_old_events(self, days: int = 30) -> int:
        """Delete events older than N days. Run periodically."""
        from datetime import timedelta
        
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        to_delete = [
            eid for eid, e in self.events.items()
            if e["created_at"] < cutoff
        ]
        
        for eid in to_delete:
            del self.events[eid]
        
        return len(to_delete)


event_log_service = EventLogService()
```

### 2. src/api/routes/webhooks_v2.py

```python
"""
Centralized Webhook Receiver

All external webhooks come through here, get logged, and routed to handlers.
"""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import hmac
import hashlib
import os

from src.services.event_log import event_log_service, EventSource

router = APIRouter(tags=["webhooks-v2"])

VAPI_WEBHOOK_SECRET = os.getenv("VAPI_WEBHOOK_SECRET", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")


def verify_vapi_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify Vapi webhook signature."""
    if not secret:
        return True  # Skip if no secret configured
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/v2/vapi")
async def vapi_webhook(
    request: Request,
    x_vapi_signature: Optional[str] = Header(None),
    client_id: Optional[str] = None,
):
    """Handle Vapi webhooks."""
    body = await request.body()
    payload = await request.json()
    
    # Verify signature
    if VAPI_WEBHOOK_SECRET and x_vapi_signature:
        if not verify_vapi_signature(body, x_vapi_signature, VAPI_WEBHOOK_SECRET):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Extract event type
    message = payload.get("message", {})
    event_type = message.get("type", "unknown")
    
    # Log event
    event_id = await event_log_service.log(
        source=EventSource.VAPI,
        event_type=event_type,
        payload=payload,
        client_id=client_id,
    )
    
    try:
        result = None
        
        if event_type == "end-of-call-report":
            result = await handle_vapi_end_of_call(payload, client_id)
        elif event_type == "assistant-request":
            result = await handle_vapi_assistant_request(payload, client_id)
        elif event_type == "status-update":
            result = await handle_vapi_status_update(payload, client_id)
        elif event_type == "transcript":
            result = await handle_vapi_transcript(payload, client_id)
        
        await event_log_service.mark_processed(event_id, result)
        return {"status": "ok", "event_id": event_id, "result": result}
        
    except Exception as e:
        await event_log_service.mark_failed(event_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))


async def handle_vapi_end_of_call(payload: dict, client_id: Optional[str]) -> dict:
    """Process end-of-call report from Vapi."""
    message = payload.get("message", {})
    call_data = message.get("call", {})
    
    # Extract call details
    call_id = call_data.get("id")
    phone_number = call_data.get("customer", {}).get("number")
    duration = call_data.get("duration")
    
    # Extract transcript
    transcript = message.get("transcript", "")
    summary = message.get("summary", "")
    
    # Extract analysis/structured data
    analysis = message.get("analysis", {})
    
    # TODO: Save to database, create lead, notify client
    
    return {
        "call_id": call_id,
        "phone_number": phone_number,
        "duration": duration,
        "has_transcript": bool(transcript),
        "has_summary": bool(summary),
    }


async def handle_vapi_assistant_request(payload: dict, client_id: Optional[str]) -> dict:
    """Handle assistant request - return dynamic config."""
    # TODO: Look up client config and return custom assistant settings
    return {"action": "default"}


async def handle_vapi_status_update(payload: dict, client_id: Optional[str]) -> dict:
    """Handle call status updates."""
    return {"action": "logged"}


async def handle_vapi_transcript(payload: dict, client_id: Optional[str]) -> dict:
    """Handle real-time transcript updates."""
    return {"action": "logged"}


@router.post("/v2/twilio/voice")
async def twilio_voice_webhook(request: Request, client_id: Optional[str] = None):
    """Handle Twilio voice webhooks."""
    form_data = await request.form()
    payload = dict(form_data)
    
    event_type = payload.get("CallStatus", "unknown")
    
    event_id = await event_log_service.log(
        source=EventSource.TWILIO,
        event_type=f"voice.{event_type}",
        payload=payload,
        client_id=client_id,
        call_id=payload.get("CallSid"),
    )
    
    try:
        # Handle different call statuses
        if event_type == "completed":
            pass  # Call finished
        elif event_type == "busy":
            pass  # Line was busy
        elif event_type == "no-answer":
            pass  # No answer
        elif event_type == "failed":
            pass  # Call failed
        
        await event_log_service.mark_processed(event_id)
        return {"status": "ok"}
        
    except Exception as e:
        await event_log_service.mark_failed(event_id, str(e))
        raise


@router.post("/v2/twilio/sms")
async def twilio_sms_webhook(request: Request, client_id: Optional[str] = None):
    """Handle Twilio SMS webhooks."""
    form_data = await request.form()
    payload = dict(form_data)
    
    event_id = await event_log_service.log(
        source=EventSource.TWILIO,
        event_type="sms.received",
        payload=payload,
        client_id=client_id,
    )
    
    try:
        from_number = payload.get("From")
        to_number = payload.get("To")
        body = payload.get("Body")
        
        # TODO: Process inbound SMS
        # - Match to client by to_number
        # - Create notification
        # - Auto-reply if configured
        
        await event_log_service.mark_processed(event_id)
        return {"status": "ok"}
        
    except Exception as e:
        await event_log_service.mark_failed(event_id, str(e))
        raise


@router.post("/v2/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None),
):
    """Handle Stripe webhooks."""
    body = await request.body()
    payload = await request.json()
    
    # TODO: Verify Stripe signature
    # stripe.Webhook.construct_event(body, stripe_signature, STRIPE_WEBHOOK_SECRET)
    
    event_type = payload.get("type", "unknown")
    data = payload.get("data", {}).get("object", {})
    
    event_id = await event_log_service.log(
        source=EventSource.STRIPE,
        event_type=event_type,
        payload=payload,
    )
    
    try:
        if event_type == "payment_intent.succeeded":
            # Mark invoice as paid
            invoice_id = data.get("metadata", {}).get("invoice_id")
            if invoice_id:
                # TODO: Update invoice status
                pass
        
        elif event_type == "customer.subscription.created":
            # Handle new subscription
            pass
        
        elif event_type == "customer.subscription.updated":
            # Handle subscription changes
            pass
        
        elif event_type == "customer.subscription.deleted":
            # Handle cancellation
            pass
        
        elif event_type == "invoice.payment_failed":
            # Handle failed payment
            pass
        
        await event_log_service.mark_processed(event_id)
        return {"status": "ok"}
        
    except Exception as e:
        await event_log_service.mark_failed(event_id, str(e))
        raise


@router.post("/v2/resend")
async def resend_webhook(request: Request):
    """Handle Resend webhooks."""
    payload = await request.json()
    
    event_type = payload.get("type", "unknown")
    
    event_id = await event_log_service.log(
        source=EventSource.RESEND,
        event_type=event_type,
        payload=payload,
    )
    
    try:
        data = payload.get("data", {})
        email_id = data.get("email_id")
        
        if event_type == "email.delivered":
            pass  # Email delivered
        elif event_type == "email.opened":
            pass  # Email opened
        elif event_type == "email.clicked":
            pass  # Link clicked
        elif event_type == "email.bounced":
            # Handle bounce - maybe update contact status
            pass
        elif event_type == "email.complained":
            # Handle spam complaint - unsubscribe
            pass
        
        await event_log_service.mark_processed(event_id)
        return {"status": "ok"}
        
    except Exception as e:
        await event_log_service.mark_failed(event_id, str(e))
        raise


@router.post("/v2/demo-call")
async def demo_call_webhook(request: Request, demo_id: str):
    """Handle calls to demo numbers."""
    payload = await request.json()
    
    event_id = await event_log_service.log(
        source=EventSource.VAPI,
        event_type="demo_call",
        payload=payload,
        demo_number_id=demo_id,
    )
    
    try:
        # Record the call on the demo number
        from src.services.demo_numbers import demo_number_service
        await demo_number_service.record_call(demo_id, payload)
        
        await event_log_service.mark_processed(event_id)
        return {"status": "ok"}
        
    except Exception as e:
        await event_log_service.mark_failed(event_id, str(e))
        raise
```

### 3. src/api/routes/events.py

```python
"""
Event Log API Routes - Query and manage logged events
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, List

from src.services.event_log import event_log_service

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
async def list_events(
    source: Optional[str] = None,
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    client_id: Optional[str] = None,
    since: Optional[str] = None,
    limit: int = 100,
):
    """List events with optional filters."""
    events = await event_log_service.list(
        source=source,
        event_type=event_type,
        status=status,
        client_id=client_id,
        since=since,
        limit=min(limit, 500),
    )
    return {"events": events, "total": len(events)}


@router.get("/stats")
async def get_event_stats():
    """Get event statistics."""
    return await event_log_service.get_stats()


@router.get("/{event_id}")
async def get_event(event_id: str):
    """Get event details including full payload."""
    event = await event_log_service.get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{event_id}/retry")
async def retry_event(event_id: str):
    """Retry processing a failed event."""
    success = await event_log_service.retry(event_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot retry this event (not failed or not found)")
    return {"message": "Event queued for retry", "event_id": event_id}


@router.post("/cleanup")
async def cleanup_old_events(days: int = 30):
    """Delete events older than N days (admin)."""
    deleted = await event_log_service.cleanup_old_events(days)
    return {"message": f"Deleted {deleted} old events", "days": days}
```

### 4. Add to src/api/main.py

```python
from src.api.routes import webhooks_v2, events

# Replace or add alongside existing webhooks
app.include_router(webhooks_v2.router, prefix="/api/v1/webhooks", tags=["webhooks"])
app.include_router(events.router, prefix="/api/v1", tags=["events"])
```

### 5. Add to frontend/src/lib/api.ts

```typescript
export const eventsApi = {
  list: (params?: { source?: string; status?: string; client_id?: string; limit?: number }) => {
    const searchParams = new URLSearchParams();
    if (params?.source) searchParams.append("source", params.source);
    if (params?.status) searchParams.append("status", params.status);
    if (params?.client_id) searchParams.append("client_id", params.client_id);
    if (params?.limit) searchParams.append("limit", params.limit.toString());
    return fetchApi<{ events: EventLogItem[]; total: number }>(`/events?${searchParams}`);
  },
  
  get: (id: string) =>
    fetchApi<EventLogItem>(`/events/${id}`),
  
  retry: (id: string) =>
    fetchApi<{ message: string }>(`/events/${id}/retry`, { method: "POST" }),
  
  stats: () =>
    fetchApi<EventStats>("/events/stats"),
};

export interface EventLogItem {
  id: string;
  source: string;
  event_type: string;
  status: string;
  payload: any;
  response: any | null;
  error: string | null;
  client_id: string | null;
  call_id: string | null;
  invoice_id: string | null;
  created_at: string;
  processed_at: string | null;
}

export interface EventStats {
  total: number;
  by_source: Record<string, number>;
  by_status: Record<string, number>;
}
```

## Database Schema (add to prisma/schema.prisma)

```prisma
model EventLog {
  id            String    @id @default(cuid())
  source        String    // vapi, twilio, stripe, resend
  eventType     String
  status        String    @default("received") // received, processed, failed
  payload       Json
  response      Json?
  error         String?
  clientId      String?
  callId        String?
  invoiceId     String?
  portingId     String?
  demoNumberId  String?
  createdAt     DateTime  @default(now())
  processedAt   DateTime?
  
  @@index([source])
  @@index([status])
  @@index([clientId])
  @@index([createdAt])
}
```

## Scheduled Job for Cleanup

Create trigger-jobs/cleanup-events.ts:

```typescript
import { schedules } from "@trigger.dev/sdk/v3";

export const cleanupOldEvents = schedules.task({
  id: "cleanup-old-events",
  cron: "0 3 * * *", // Daily at 3am
  run: async () => {
    const response = await fetch(
      `${process.env.API_URL}/api/v1/events/cleanup?days=30`,
      { method: "POST" }
    );
    return await response.json();
  },
});
```

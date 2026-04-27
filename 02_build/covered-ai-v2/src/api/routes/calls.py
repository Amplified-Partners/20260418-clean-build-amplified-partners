"""
Calls Routes - Call history and management (calls are stored as leads)

In Covered AI, incoming calls are processed by Vapi and stored as Lead records.
This routes module provides a calls-focused interface to that data.
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from enum import Enum

from src.db.client import get_prisma

router = APIRouter()


class CallStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    callback_scheduled = "callback_scheduled"
    booked = "booked"
    dismissed = "dismissed"


class CallUpdate(BaseModel):
    status: Optional[CallStatus] = None
    notes: Optional[str] = None


def call_to_response(lead) -> dict:
    """Convert Prisma lead to call response dict."""
    # Determine call status based on lead status
    call_status = "new"
    if lead.status == "booked":
        call_status = "booked"
    elif lead.status == "dismissed":
        call_status = "dismissed"
    elif lead.status in ["contacted", "nurturing", "qualified"]:
        call_status = "contacted"

    return {
        "id": lead.id,
        "client_id": lead.clientId,
        "customer_id": lead.customerId,
        "call_id": lead.callId,
        "caller_phone": lead.callerPhone,
        "customer_name": lead.customerName,
        "duration": lead.callDuration,
        "recording_url": lead.recordingUrl,
        "transcript": lead.transcript,
        "summary": lead.summary,
        "address": lead.address,
        "postcode": lead.postcode,
        "job_type": lead.jobType,
        "urgency": lead.urgency,
        "status": call_status,
        "lead_status": lead.status,
        "created_at": lead.createdAt,
        "customer": {
            "id": lead.customer.id,
            "name": lead.customer.name,
            "phone": lead.customer.phone,
            "email": lead.customer.email,
        } if lead.customer else None,
        "job": {
            "id": lead.job.id,
            "title": lead.job.title,
            "status": lead.job.status,
            "scheduled_date": lead.job.scheduledDate,
        } if hasattr(lead, 'job') and lead.job else None,
    }


@router.get("")
async def list_calls(
    client_id: str,
    status: Optional[str] = None,
    urgency: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List calls (leads) for a client with filters."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    where = {"clientId": client_id}

    # Filter by urgency
    if urgency:
        where["urgency"] = urgency

    # Filter by date range
    if date_from:
        where["createdAt"] = where.get("createdAt", {})
        where["createdAt"]["gte"] = date_from
    if date_to:
        where["createdAt"] = where.get("createdAt", {})
        where["createdAt"]["lte"] = date_to

    # Filter by status (map call status to lead status)
    if status:
        status_map = {
            "new": ["new"],
            "contacted": ["contacted", "nurturing", "qualified"],
            "booked": ["booked", "converted"],
            "dismissed": ["dismissed", "lost"],
        }
        lead_statuses = status_map.get(status, [status])
        where["status"] = {"in": lead_statuses}

    # Search
    if search:
        where["OR"] = [
            {"customerName": {"contains": search, "mode": "insensitive"}},
            {"callerPhone": {"contains": search}},
            {"summary": {"contains": search, "mode": "insensitive"}},
            {"jobType": {"contains": search, "mode": "insensitive"}},
        ]

    leads = await db.lead.find_many(
        where=where,
        include={"customer": True, "job": True},
        order={"createdAt": "desc"},
        take=limit,
        skip=offset,
    )

    total = await db.lead.count(where=where)

    return {
        "calls": [call_to_response(lead) for lead in leads],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(leads) < total,
    }


@router.get("/today")
async def get_today_calls(client_id: str, db=Depends(get_prisma)):
    """Get today's calls summary."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # Get today's leads
    leads = await db.lead.find_many(
        where={
            "clientId": client_id,
            "createdAt": {"gte": today_start}
        },
        include={"customer": True},
        order={"createdAt": "desc"},
    )

    # Calculate stats
    total = len(leads)
    emergencies = sum(1 for l in leads if l.urgency == "emergency")
    urgent = sum(1 for l in leads if l.urgency == "urgent")
    routine = sum(1 for l in leads if l.urgency == "routine")

    new_count = sum(1 for l in leads if l.status == "new")
    booked_count = sum(1 for l in leads if l.status == "booked")

    return {
        "date": today_start.date().isoformat(),
        "total": total,
        "emergencies": emergencies,
        "urgent": urgent,
        "routine": routine,
        "new": new_count,
        "booked": booked_count,
        "calls": [call_to_response(lead) for lead in leads[:10]],  # First 10
    }


@router.get("/stats")
async def get_call_stats(
    client_id: str,
    days: int = 7,
    db=Depends(get_prisma)
):
    """Get call statistics for a period."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    start_date = datetime.utcnow() - timedelta(days=days)

    # Get all leads in period
    leads = await db.lead.find_many(
        where={
            "clientId": client_id,
            "createdAt": {"gte": start_date}
        }
    )

    total = len(leads)
    emergencies = sum(1 for l in leads if l.urgency == "emergency")
    urgent = sum(1 for l in leads if l.urgency == "urgent")
    routine = sum(1 for l in leads if l.urgency == "routine")

    booked = sum(1 for l in leads if l.status in ["booked", "converted"])
    dismissed = sum(1 for l in leads if l.status in ["dismissed", "lost"])

    conversion_rate = (booked / total * 100) if total > 0 else 0

    # Average call duration (for calls with duration)
    calls_with_duration = [l.callDuration for l in leads if l.callDuration]
    avg_duration = sum(calls_with_duration) / len(calls_with_duration) if calls_with_duration else 0

    # Calls by day
    calls_by_day = {}
    for lead in leads:
        day = lead.createdAt.date().isoformat()
        calls_by_day[day] = calls_by_day.get(day, 0) + 1

    return {
        "period_days": days,
        "total_calls": total,
        "urgency_breakdown": {
            "emergency": emergencies,
            "urgent": urgent,
            "routine": routine,
        },
        "outcome_breakdown": {
            "booked": booked,
            "dismissed": dismissed,
            "in_progress": total - booked - dismissed,
        },
        "conversion_rate": round(conversion_rate, 1),
        "avg_duration_seconds": round(avg_duration),
        "calls_by_day": calls_by_day,
    }


@router.get("/{call_id}")
async def get_call(client_id: str, call_id: str, db=Depends(get_prisma)):
    """Get call (lead) by ID with full details."""
    lead = await db.lead.find_unique(
        where={"id": call_id},
        include={
            "customer": True,
            "job": True,
            "nurtureSequence": True,
            "notifications": {
                "order_by": {"createdAt": "desc"},
                "take": 10,
            }
        }
    )

    if not lead or lead.clientId != client_id:
        raise HTTPException(status_code=404, detail="Call not found")

    response = call_to_response(lead)

    # Add nurture sequence info if present
    if lead.nurtureSequence:
        response["nurture_sequence"] = {
            "id": lead.nurtureSequence.id,
            "current_touch": lead.nurtureSequence.currentTouch,
            "status": lead.nurtureSequence.status,
            "next_touch_at": lead.nurtureSequence.nextTouchAt,
        }

    # Add notification history
    response["notifications"] = [
        {
            "id": n.id,
            "type": n.type,
            "channel": n.channel,
            "status": n.status,
            "sent_at": n.sentAt,
        }
        for n in (lead.notifications or [])
    ]

    return response


@router.patch("/{call_id}")
async def update_call(
    client_id: str,
    call_id: str,
    update: CallUpdate,
    db=Depends(get_prisma)
):
    """Update call status or add notes."""
    lead = await db.lead.find_unique(where={"id": call_id})

    if not lead or lead.clientId != client_id:
        raise HTTPException(status_code=404, detail="Call not found")

    data = {}

    if update.status:
        # Map call status to lead status
        status_map = {
            "new": "new",
            "contacted": "contacted",
            "callback_scheduled": "contacted",
            "booked": "booked",
            "dismissed": "dismissed",
        }
        lead_status = status_map.get(update.status.value, update.status.value)
        data["status"] = lead_status

        # Set timestamps based on status
        if lead_status == "booked":
            data["bookedAt"] = datetime.utcnow()
        elif lead_status == "dismissed":
            data["dismissedAt"] = datetime.utcnow()

    # Notes can be added to summary field
    # We don't have a separate notes field, but we can append to summary
    # Or we could use the dismiss_reason field creatively

    if data:
        lead = await db.lead.update(
            where={"id": call_id},
            data=data,
            include={"customer": True}
        )

    return {"id": call_id, "message": "Call updated", **call_to_response(lead)}


@router.post("/{call_id}/create-job")
async def create_job_from_call(
    client_id: str,
    call_id: str,
    scheduled_date: datetime,
    scheduled_time: Optional[str] = None,
    quoted_amount: Optional[float] = None,
    db=Depends(get_prisma)
):
    """Create a job from a call (lead)."""
    lead = await db.lead.find_unique(
        where={"id": call_id},
        include={"customer": True, "job": True}
    )

    if not lead or lead.clientId != client_id:
        raise HTTPException(status_code=404, detail="Call not found")

    if lead.job:
        raise HTTPException(
            status_code=400,
            detail=f"Job {lead.job.id} already exists for this call"
        )

    if not lead.customerId:
        raise HTTPException(
            status_code=400,
            detail="Call has no linked customer"
        )

    # Create job
    job = await db.job.create(
        data={
            "clientId": client_id,
            "customerId": lead.customerId,
            "leadId": lead.id,
            "title": lead.jobType or "New Job",
            "description": lead.summary,
            "address": lead.address or "",
            "postcode": lead.postcode,
            "scheduledDate": scheduled_date,
            "scheduledTime": scheduled_time,
            "quotedAmount": quoted_amount,
            "status": "scheduled",
        },
        include={"customer": True}
    )

    # Update lead status
    await db.lead.update(
        where={"id": call_id},
        data={
            "status": "booked",
            "bookedAt": datetime.utcnow(),
        }
    )

    # Stop nurture sequence if active
    if lead.nurtureSequence:
        await db.nurturesequence.update(
            where={"id": lead.nurtureSequence.id},
            data={
                "status": "stopped",
                "stoppedAt": datetime.utcnow(),
                "stopReason": "job_booked",
            }
        )

    return {
        "message": "Job created from call",
        "job": {
            "id": job.id,
            "title": job.title,
            "scheduled_date": job.scheduledDate,
            "scheduled_time": job.scheduledTime,
            "status": job.status,
            "customer": {
                "id": job.customer.id,
                "name": job.customer.name,
            } if job.customer else None,
        }
    }


@router.post("/{call_id}/dismiss")
async def dismiss_call(
    client_id: str,
    call_id: str,
    reason: Optional[str] = None,
    db=Depends(get_prisma)
):
    """Dismiss a call (mark lead as dismissed)."""
    lead = await db.lead.find_unique(where={"id": call_id})

    if not lead or lead.clientId != client_id:
        raise HTTPException(status_code=404, detail="Call not found")

    # Update lead
    await db.lead.update(
        where={"id": call_id},
        data={
            "status": "dismissed",
            "dismissedAt": datetime.utcnow(),
            "dismissReason": reason,
        }
    )

    # Stop nurture sequence if active
    if lead.nurtureSequenceId:
        sequence = await db.nurturesequence.find_unique(
            where={"id": lead.nurtureSequenceId}
        )
        if sequence and sequence.status == "active":
            await db.nurturesequence.update(
                where={"id": sequence.id},
                data={
                    "status": "stopped",
                    "stoppedAt": datetime.utcnow(),
                    "stopReason": reason or "dismissed",
                }
            )

    return {
        "id": call_id,
        "status": "dismissed",
        "reason": reason,
        "message": "Call dismissed",
    }

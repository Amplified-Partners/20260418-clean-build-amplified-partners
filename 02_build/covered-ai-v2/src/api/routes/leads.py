"""
Leads Routes - Lead management for a client
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from src.db.client import get_prisma
from src.db import queries
from src.services.lead_service import LeadService

router = APIRouter()


class LeadStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    nurturing = "nurturing"
    qualified = "qualified"
    booked = "booked"
    converted = "converted"
    dismissed = "dismissed"
    lost = "lost"


class LeadAction(str, Enum):
    book = "book"
    dismiss = "dismiss"
    callback = "callback"
    convert = "convert"
    pause_nurture = "pause_nurture"
    resume_nurture = "resume_nurture"


class ActionRequest(BaseModel):
    action: LeadAction
    reason: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    scheduled_time: Optional[str] = None
    quoted_amount: Optional[float] = None
    notes: Optional[str] = None


def lead_to_response(lead) -> dict:
    """Convert Prisma lead to response dict."""
    return {
        "id": lead.id,
        "client_id": lead.clientId,
        "customer_id": lead.customerId,
        "caller_phone": lead.callerPhone,
        "customer_name": lead.customerName,
        "address": lead.address,
        "postcode": lead.postcode,
        "job_type": lead.jobType,
        "urgency": lead.urgency,
        "status": lead.status,
        "summary": lead.summary,
        "transcript": lead.transcript,
        "recording_url": lead.recordingUrl,
        "created_at": lead.createdAt,
        "customer": {
            "id": lead.customer.id,
            "name": lead.customer.name,
            "phone": lead.customer.phone,
            "email": lead.customer.email
        } if lead.customer else None,
        "nurture_sequence": {
            "id": lead.nurtureSequence.id,
            "current_touch": lead.nurtureSequence.currentTouch,
            "status": lead.nurtureSequence.status
        } if lead.nurtureSequence else None
    }


@router.get("")
async def list_leads(
    client_id: str,
    status: Optional[LeadStatus] = None,
    urgency: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List leads for a client."""
    # Verify client exists
    client = await queries.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    leads, total = await queries.list_leads(
        db,
        client_id=client_id,
        status=status.value if status else None,
        urgency=urgency,
        limit=limit,
        offset=offset
    )

    return {
        "leads": [lead_to_response(lead) for lead in leads],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{lead_id}")
async def get_lead(client_id: str, lead_id: str, db=Depends(get_prisma)):
    """Get lead by ID."""
    lead = await queries.get_lead_by_id(db, lead_id)

    if not lead or lead.clientId != client_id:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead_to_response(lead)


@router.post("/{lead_id}/action")
async def take_action(
    client_id: str,
    lead_id: str,
    request: ActionRequest,
    db=Depends(get_prisma)
):
    """
    Take action on a lead.

    Actions:
    - book: Convert to job
    - dismiss: Mark as not interested
    - callback: Schedule follow-up
    - convert: Mark as converted (completed)
    - pause_nurture: Stop nurture sequence
    - resume_nurture: Restart nurture sequence
    """
    # Verify lead exists and belongs to client
    lead = await queries.get_lead_by_id(db, lead_id)
    if not lead or lead.clientId != client_id:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead_service = LeadService(db)
    action = request.action

    if action == LeadAction.book:
        if not request.scheduled_date:
            raise HTTPException(
                status_code=400,
                detail="scheduled_date required for booking"
            )

        result = await lead_service.book_lead(
            lead_id=lead_id,
            scheduled_date=request.scheduled_date.isoformat(),
            scheduled_time=request.scheduled_time,
            quoted_amount=request.quoted_amount
        )
        return {"message": "Job created", **result}

    elif action == LeadAction.dismiss:
        await lead_service.dismiss_lead(lead_id, request.reason)
        return {"message": "Lead dismissed", "reason": request.reason}

    elif action == LeadAction.callback:
        # Update lead status to indicate callback needed
        await queries.update_lead_status(db, lead_id, "contacted")
        return {
            "message": "Callback scheduled",
            "scheduled": request.scheduled_date,
            "notes": request.notes
        }

    elif action == LeadAction.convert:
        await queries.update_lead_status(db, lead_id, "converted")
        await queries.stop_nurture_sequence(db, lead_id, "lead_converted")
        return {"message": "Lead converted"}

    elif action == LeadAction.pause_nurture:
        success = await lead_service.pause_nurture(lead_id)
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Could not pause nurture sequence"
            )
        return {"message": "Nurture paused"}

    elif action == LeadAction.resume_nurture:
        success = await lead_service.resume_nurture(lead_id)
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Could not resume nurture sequence"
            )
        return {"message": "Nurture resumed"}

    return {"message": "Action completed"}

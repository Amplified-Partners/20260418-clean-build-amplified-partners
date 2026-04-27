"""
Nurture Sequence API routes - Email drip campaigns for leads
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from src.services.nurture_sequences import (
    SequenceType,
    add_to_sequence,
    stop_sequence,
    get_lead,
    list_leads,
    get_sequence_schedule,
    send_sequence_email,
    SEQUENCES,
    TEMPLATES,
)

router = APIRouter(prefix="/nurture", tags=["nurture"])


class AddToSequenceRequest(BaseModel):
    email: EmailStr
    first_name: str
    sequence_type: str  # demo_followup, cold_intro, reengagement
    vertical: Optional[str] = "business"
    avg_job_value: Optional[int] = 200
    metadata: Optional[dict] = None


class AddToSequenceResponse(BaseModel):
    lead_id: str
    email: str
    sequence_type: str
    schedule: List[dict]
    message: str


class LeadResponse(BaseModel):
    id: str
    email: str
    first_name: str
    sequence_type: str
    vertical: str
    status: str
    current_step: int
    emails_sent: List[dict]
    created_at: str


class SendEmailRequest(BaseModel):
    email: EmailStr
    template: str
    first_name: str
    vertical: Optional[str] = "business"
    avg_job_value: Optional[int] = 200


@router.post("/add", response_model=AddToSequenceResponse)
async def add_lead_to_sequence(request: AddToSequenceRequest):
    """
    Add a lead to an email nurture sequence.
    
    Sequence types:
    - demo_followup: After a demo call
    - cold_intro: Cold outreach
    - reengagement: Re-engage dormant leads
    """
    # Validate sequence type
    try:
        seq_type = SequenceType(request.sequence_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sequence type. Must be one of: {[s.value for s in SequenceType]}"
        )
    
    # Add to sequence
    lead_id = add_to_sequence(
        email=request.email,
        first_name=request.first_name,
        sequence_type=seq_type,
        vertical=request.vertical,
        avg_job_value=request.avg_job_value,
        metadata=request.metadata,
    )
    
    # Get schedule
    schedule = get_sequence_schedule(seq_type)
    
    return AddToSequenceResponse(
        lead_id=lead_id,
        email=request.email,
        sequence_type=request.sequence_type,
        schedule=schedule,
        message=f"Lead added to {request.sequence_type} sequence. First email sent.",
    )


@router.get("/leads", response_model=List[LeadResponse])
async def get_all_leads(status: Optional[str] = None):
    """List all leads in nurture sequences."""
    leads = list_leads(status=status)
    
    return [
        LeadResponse(
            id=lead["id"],
            email=lead["email"],
            first_name=lead["first_name"],
            sequence_type=lead["sequence_type"],
            vertical=lead["vertical"],
            status=lead["status"],
            current_step=lead["current_step"],
            emails_sent=lead["emails_sent"],
            created_at=lead["created_at"],
        )
        for lead in leads
    ]


@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead_by_id(lead_id: str):
    """Get a specific lead by ID."""
    lead = get_lead(lead_id)
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return LeadResponse(
        id=lead["id"],
        email=lead["email"],
        first_name=lead["first_name"],
        sequence_type=lead["sequence_type"],
        vertical=lead["vertical"],
        status=lead["status"],
        current_step=lead["current_step"],
        emails_sent=lead["emails_sent"],
        created_at=lead["created_at"],
    )


@router.post("/leads/{lead_id}/stop")
async def stop_lead_sequence(lead_id: str, reason: str = "manual"):
    """Stop a nurture sequence for a lead."""
    success = stop_sequence(lead_id, reason)
    
    if not success:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return {"message": "Sequence stopped", "lead_id": lead_id, "reason": reason}


@router.get("/sequences")
async def list_sequences():
    """List all available nurture sequences."""
    return {
        seq_type.value: {
            "name": seq_type.value.replace("_", " ").title(),
            "emails": len(SEQUENCES[seq_type]),
            "schedule": get_sequence_schedule(seq_type),
        }
        for seq_type in SequenceType
    }


@router.get("/templates")
async def list_templates():
    """List all available email templates."""
    return {
        key: {"subject": template["subject"]}
        for key, template in TEMPLATES.items()
    }


@router.post("/send")
async def send_single_email(request: SendEmailRequest):
    """Send a single email using a template (not part of sequence)."""
    if request.template not in TEMPLATES:
        raise HTTPException(
            status_code=400,
            detail=f"Template not found. Available: {list(TEMPLATES.keys())}"
        )
    
    success = send_sequence_email(
        to_email=request.email,
        template_key=request.template,
        first_name=request.first_name,
        vertical=request.vertical,
        avg_job_value=request.avg_job_value,
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
    return {
        "message": "Email sent",
        "email": request.email,
        "template": request.template,
    }


@router.post("/preview")
async def preview_template(request: SendEmailRequest):
    """Preview a rendered email template without sending."""
    if request.template not in TEMPLATES:
        raise HTTPException(
            status_code=400,
            detail=f"Template not found. Available: {list(TEMPLATES.keys())}"
        )
    
    from src.services.nurture_sequences import render_template
    
    subject, body = render_template(
        template_key=request.template,
        first_name=request.first_name,
        vertical=request.vertical,
        avg_job_value=request.avg_job_value,
    )
    
    return {
        "template": request.template,
        "subject": subject,
        "body": body,
    }

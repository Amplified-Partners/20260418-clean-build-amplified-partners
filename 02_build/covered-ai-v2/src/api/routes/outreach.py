"""
Cold Outreach API Routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import Response, RedirectResponse
from pydantic import BaseModel
from typing import Optional, List

from src.db.client import get_prisma
from src.services.cold_outreach import get_cold_outreach_service, TEMPLATES

router = APIRouter()


class CreateCampaignRequest(BaseModel):
    name: str
    subject: str
    template: str
    vertical: Optional[str] = None


class CampaignResponse(BaseModel):
    id: str
    name: str
    status: str
    subject: str
    template: str
    vertical: Optional[str]
    total_leads: int
    sent: int
    opened: int
    clicked: int
    replied: int
    converted: int
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]


class LeadResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: Optional[str]
    business_name: Optional[str]
    phone: Optional[str]
    vertical: Optional[str]
    status: str
    sent_at: Optional[str]
    opened_at: Optional[str]
    clicked_at: Optional[str]
    replied_at: Optional[str]


@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(request: CreateCampaignRequest, db=Depends(get_prisma)):
    """Create a new outreach campaign."""
    if request.template not in TEMPLATES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid template. Available: {list(TEMPLATES.keys())}"
        )

    service = get_cold_outreach_service(db)
    result = await service.create_campaign(
        name=request.name,
        subject=request.subject,
        template=request.template,
        vertical=request.vertical,
    )
    return result


@router.get("/campaigns", response_model=List[CampaignResponse])
async def list_campaigns(db=Depends(get_prisma)):
    """List all campaigns."""
    service = get_cold_outreach_service(db)
    return await service.list_campaigns()


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str, db=Depends(get_prisma)):
    """Get campaign details."""
    service = get_cold_outreach_service(db)
    result = await service.get_campaign(campaign_id)
    if not result:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return result


@router.get("/campaigns/{campaign_id}/leads", response_model=List[LeadResponse])
async def get_campaign_leads(campaign_id: str, db=Depends(get_prisma)):
    """Get leads for a campaign."""
    service = get_cold_outreach_service(db)
    return await service.get_campaign_leads(campaign_id)


@router.post("/campaigns/{campaign_id}/upload")
async def upload_leads(campaign_id: str, file: UploadFile = File(...), db=Depends(get_prisma)):
    """Upload CSV of leads."""
    content = await file.read()
    service = get_cold_outreach_service(db)
    try:
        result = await service.upload_leads(campaign_id, content.decode())
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/campaigns/{campaign_id}/start")
async def start_campaign(campaign_id: str, db=Depends(get_prisma)):
    """Start campaign."""
    service = get_cold_outreach_service(db)
    try:
        await service.start_campaign(campaign_id)
        return {"message": "Campaign started"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/campaigns/{campaign_id}/pause")
async def pause_campaign(campaign_id: str, db=Depends(get_prisma)):
    """Pause campaign."""
    service = get_cold_outreach_service(db)
    try:
        await service.pause_campaign(campaign_id)
        return {"message": "Campaign paused"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/campaigns/{campaign_id}/export")
async def export_campaign(campaign_id: str, db=Depends(get_prisma)):
    """Export results as CSV."""
    service = get_cold_outreach_service(db)
    csv_content = await service.export_results(campaign_id)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=campaign-{campaign_id}.csv"}
    )


@router.post("/process-queue")
async def process_queue(limit: int = 50, db=Depends(get_prisma)):
    """Manually trigger queue processing (admin)."""
    service = get_cold_outreach_service(db)
    sent = await service.process_queue(limit)
    return {"message": f"Sent {sent} emails", "sent": sent}


@router.get("/templates")
async def list_templates():
    """List available email templates."""
    return {key: {"subject": t["subject"]} for key, t in TEMPLATES.items()}


# Tracking endpoints
@router.get("/track/open")
async def track_open(lead_id: str, db=Depends(get_prisma)):
    """Track email open (1x1 pixel)."""
    service = get_cold_outreach_service(db)
    await service.track_open(lead_id)
    # Return 1x1 transparent GIF
    gif_bytes = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return Response(content=gif_bytes, media_type="image/gif")


@router.get("/track/click")
async def track_click(lead_id: str, url: str, db=Depends(get_prisma)):
    """Track click and redirect."""
    service = get_cold_outreach_service(db)
    await service.track_click(lead_id, url)
    return RedirectResponse(url=url)


@router.post("/leads/{lead_id}/replied")
async def mark_replied(lead_id: str, db=Depends(get_prisma)):
    """Mark lead as replied (manual)."""
    service = get_cold_outreach_service(db)
    await service.track_reply(lead_id)
    return {"message": "Marked as replied"}


@router.post("/leads/{lead_id}/converted")
async def mark_converted(lead_id: str, db=Depends(get_prisma)):
    """Mark lead as converted."""
    service = get_cold_outreach_service(db)
    await service.mark_converted(lead_id)
    return {"message": "Marked as converted"}

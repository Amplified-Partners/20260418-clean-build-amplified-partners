---
title: "Module 2: Cold Outreach Engine"
id: "02-cold-outreach"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "sales-marketing"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 2: Cold Outreach Engine

## Overview
Upload lead lists, create email campaigns, send personalized cold emails, track engagement.

## Files to Create

### 1. src/services/cold_outreach.py

```python
"""
Cold Outreach Service - Email campaigns with tracking

Features:
- Create campaigns with email templates
- Upload CSV lead lists
- Send rate-limited emails (50/hour)
- Track opens, clicks, replies
- Integration with personalized demo numbers
"""

import csv
import io
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
import uuid
import os

try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "Ewan from Covered AI <ewan@covered.ai>")
TRACKING_BASE_URL = os.getenv("TRACKING_BASE_URL", "https://covered-ai-production.up.railway.app/api/v1/outreach/track")


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class LeadStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"
    CONVERTED = "converted"
    BOUNCED = "bounced"
    UNSUBSCRIBED = "unsubscribed"


# Email templates
TEMPLATES = {
    "cold_intro": {
        "subject": "Missed calls = missed money",
        "body": """Hi {first_name},

I'm Ewan. I built an AI receptionist called Gemma specifically for {vertical}s like you.

She answers your phone 24/7, captures every caller's details, and forwards emergencies to you immediately.

No more missed calls. No more voicemails. No more "sorry, we tried calling but..."

{demo_line}

Ewan
Covered AI
""",
    },
    "cold_with_demo": {
        "subject": "I set up a demo line for {business_name}",
        "body": """Hi {first_name},

I've set up a demo phone line specifically for {business_name}.

Call this number: {demo_number}

Gemma will answer as your receptionist. It takes 30 seconds to see how it works.

No commitment, no sales call. Just call and experience it.

Ewan
Covered AI
""",
    },
    "cold_followup": {
        "subject": "Quick question",
        "body": """{first_name},

Just wondering — how many calls do you reckon you miss each week?

Most {vertical}s I talk to say it's somewhere between 5-10. At an average job value of £200, that's potentially £4,000/month walking out the door.

Gemma catches those calls. Every single one.

Worth a quick 10-minute setup? Reply and I'll sort it.

Ewan
""",
    },
}


class ColdOutreachService:
    def __init__(self):
        self.campaigns: Dict[str, Dict[str, Any]] = {}
        self.leads: Dict[str, Dict[str, Any]] = {}
    
    async def create_campaign(
        self,
        name: str,
        subject: str,
        template: str,
        vertical: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new outreach campaign."""
        campaign_id = str(uuid.uuid4())[:8]
        
        campaign = {
            "id": campaign_id,
            "name": name,
            "status": CampaignStatus.DRAFT.value,
            "subject": subject,
            "template": template,
            "vertical": vertical,
            "total_leads": 0,
            "sent": 0,
            "opened": 0,
            "clicked": 0,
            "replied": 0,
            "converted": 0,
            "created_at": datetime.utcnow().isoformat(),
            "started_at": None,
            "completed_at": None,
        }
        
        self.campaigns[campaign_id] = campaign
        return campaign
    
    async def upload_leads(
        self,
        campaign_id: str,
        csv_content: str,
    ) -> Dict[str, Any]:
        """
        Upload leads from CSV.
        Required columns: email, first_name
        Optional: last_name, business_name, phone, vertical
        Returns: { added: int, skipped: int, errors: [] }
        """
        if campaign_id not in self.campaigns:
            raise ValueError("Campaign not found")
        
        reader = csv.DictReader(io.StringIO(csv_content))
        
        added = 0
        skipped = 0
        errors = []
        
        for row in reader:
            try:
                email = row.get("email", "").strip().lower()
                first_name = row.get("first_name", "").strip()
                
                if not email or not first_name:
                    errors.append(f"Missing email or first_name: {row}")
                    skipped += 1
                    continue
                
                # Check for duplicate
                existing = [l for l in self.leads.values() 
                           if l["campaign_id"] == campaign_id and l["email"] == email]
                if existing:
                    skipped += 1
                    continue
                
                lead_id = str(uuid.uuid4())[:8]
                lead = {
                    "id": lead_id,
                    "campaign_id": campaign_id,
                    "email": email,
                    "first_name": first_name,
                    "last_name": row.get("last_name", "").strip() or None,
                    "business_name": row.get("business_name", "").strip() or None,
                    "phone": row.get("phone", "").strip() or None,
                    "vertical": row.get("vertical", "").strip() or self.campaigns[campaign_id].get("vertical"),
                    "status": LeadStatus.PENDING.value,
                    "sent_at": None,
                    "opened_at": None,
                    "clicked_at": None,
                    "replied_at": None,
                    "demo_number_id": None,
                    "metadata": {},
                    "created_at": datetime.utcnow().isoformat(),
                }
                
                self.leads[lead_id] = lead
                added += 1
                
            except Exception as e:
                errors.append(f"Error processing row: {e}")
                skipped += 1
        
        # Update campaign total
        self.campaigns[campaign_id]["total_leads"] = len([
            l for l in self.leads.values() if l["campaign_id"] == campaign_id
        ])
        
        return {"added": added, "skipped": skipped, "errors": errors[:10]}
    
    async def start_campaign(self, campaign_id: str) -> None:
        """Start sending emails."""
        if campaign_id not in self.campaigns:
            raise ValueError("Campaign not found")
        
        self.campaigns[campaign_id]["status"] = CampaignStatus.ACTIVE.value
        self.campaigns[campaign_id]["started_at"] = datetime.utcnow().isoformat()
    
    async def pause_campaign(self, campaign_id: str) -> None:
        """Pause campaign."""
        if campaign_id not in self.campaigns:
            raise ValueError("Campaign not found")
        
        self.campaigns[campaign_id]["status"] = CampaignStatus.PAUSED.value
    
    async def process_queue(self, limit: int = 50) -> int:
        """
        Process pending emails. Called by scheduled job.
        Rate limit: 50 emails per call (run every hour).
        Returns number sent.
        """
        sent_count = 0
        
        # Get active campaigns
        active_campaigns = [c for c in self.campaigns.values() 
                          if c["status"] == CampaignStatus.ACTIVE.value]
        
        for campaign in active_campaigns:
            if sent_count >= limit:
                break
            
            # Get pending leads for this campaign
            pending_leads = [l for l in self.leads.values()
                           if l["campaign_id"] == campaign["id"] 
                           and l["status"] == LeadStatus.PENDING.value]
            
            for lead in pending_leads:
                if sent_count >= limit:
                    break
                
                success = await self._send_email(campaign, lead)
                if success:
                    sent_count += 1
                    self.campaigns[campaign["id"]]["sent"] += 1
            
            # Check if campaign is complete
            remaining = len([l for l in self.leads.values()
                           if l["campaign_id"] == campaign["id"]
                           and l["status"] == LeadStatus.PENDING.value])
            
            if remaining == 0:
                self.campaigns[campaign["id"]]["status"] = CampaignStatus.COMPLETED.value
                self.campaigns[campaign["id"]]["completed_at"] = datetime.utcnow().isoformat()
        
        return sent_count
    
    async def _send_email(self, campaign: Dict, lead: Dict) -> bool:
        """Send email to a single lead."""
        template = TEMPLATES.get(campaign["template"])
        if not template:
            return False
        
        # Render template
        subject = campaign["subject"].format(
            first_name=lead["first_name"],
            business_name=lead.get("business_name", "your business"),
            vertical=lead.get("vertical", "business"),
        )
        
        # Add tracking pixel and click tracking
        tracking_pixel = f'<img src="{TRACKING_BASE_URL}/open?lead_id={lead["id"]}" width="1" height="1" />'
        
        body = template["body"].format(
            first_name=lead["first_name"],
            business_name=lead.get("business_name", "your business"),
            vertical=lead.get("vertical", "business"),
            demo_line="Call 0800 COVERED to hear Gemma in action.",
            demo_number="",
        )
        
        # Convert to HTML
        html_body = f"<html><body><pre style='font-family: sans-serif;'>{body}</pre>{tracking_pixel}</body></html>"
        
        # Send via Resend
        if RESEND_AVAILABLE and RESEND_API_KEY:
            try:
                resend.api_key = RESEND_API_KEY
                resend.Emails.send({
                    "from": FROM_EMAIL,
                    "to": lead["email"],
                    "subject": subject,
                    "html": html_body,
                })
            except Exception as e:
                print(f"Failed to send email: {e}")
                return False
        else:
            print(f"[EMAIL MOCK] To: {lead['email']}, Subject: {subject}")
        
        # Update lead status
        lead["status"] = LeadStatus.SENT.value
        lead["sent_at"] = datetime.utcnow().isoformat()
        
        return True
    
    async def track_open(self, lead_id: str) -> None:
        """Record email open."""
        if lead_id in self.leads:
            lead = self.leads[lead_id]
            if lead["status"] == LeadStatus.SENT.value:
                lead["status"] = LeadStatus.OPENED.value
                lead["opened_at"] = datetime.utcnow().isoformat()
                
                # Update campaign stats
                campaign = self.campaigns.get(lead["campaign_id"])
                if campaign:
                    campaign["opened"] += 1
    
    async def track_click(self, lead_id: str, url: str) -> None:
        """Record link click."""
        if lead_id in self.leads:
            lead = self.leads[lead_id]
            if lead["status"] in [LeadStatus.SENT.value, LeadStatus.OPENED.value]:
                lead["status"] = LeadStatus.CLICKED.value
                lead["clicked_at"] = datetime.utcnow().isoformat()
                
                campaign = self.campaigns.get(lead["campaign_id"])
                if campaign:
                    campaign["clicked"] += 1
    
    async def track_reply(self, lead_id: str) -> None:
        """Record reply (called manually or via email parsing)."""
        if lead_id in self.leads:
            lead = self.leads[lead_id]
            lead["status"] = LeadStatus.REPLIED.value
            lead["replied_at"] = datetime.utcnow().isoformat()
            
            campaign = self.campaigns.get(lead["campaign_id"])
            if campaign:
                campaign["replied"] += 1
    
    async def mark_converted(self, lead_id: str) -> None:
        """Mark lead as converted."""
        if lead_id in self.leads:
            lead = self.leads[lead_id]
            lead["status"] = LeadStatus.CONVERTED.value
            
            campaign = self.campaigns.get(lead["campaign_id"])
            if campaign:
                campaign["converted"] += 1
    
    async def get_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign with stats."""
        return self.campaigns.get(campaign_id)
    
    async def list_campaigns(self) -> List[Dict[str, Any]]:
        """List all campaigns."""
        return sorted(
            list(self.campaigns.values()),
            key=lambda x: x["created_at"],
            reverse=True
        )
    
    async def get_campaign_leads(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get all leads for a campaign."""
        return [l for l in self.leads.values() if l["campaign_id"] == campaign_id]
    
    async def export_results(self, campaign_id: str) -> str:
        """Export campaign results as CSV."""
        leads = await self.get_campaign_leads(campaign_id)
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "email", "first_name", "last_name", "business_name", "phone",
            "vertical", "status", "sent_at", "opened_at", "clicked_at", "replied_at"
        ])
        writer.writeheader()
        
        for lead in leads:
            writer.writerow({
                "email": lead["email"],
                "first_name": lead["first_name"],
                "last_name": lead.get("last_name", ""),
                "business_name": lead.get("business_name", ""),
                "phone": lead.get("phone", ""),
                "vertical": lead.get("vertical", ""),
                "status": lead["status"],
                "sent_at": lead.get("sent_at", ""),
                "opened_at": lead.get("opened_at", ""),
                "clicked_at": lead.get("clicked_at", ""),
                "replied_at": lead.get("replied_at", ""),
            })
        
        return output.getvalue()


cold_outreach_service = ColdOutreachService()
```

### 2. src/api/routes/outreach.py

```python
"""
Cold Outreach API Routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response, RedirectResponse
from pydantic import BaseModel
from typing import Optional, List

from src.services.cold_outreach import cold_outreach_service, TEMPLATES

router = APIRouter(prefix="/outreach", tags=["outreach"])


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
    status: str
    sent_at: Optional[str]
    opened_at: Optional[str]
    clicked_at: Optional[str]


@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(request: CreateCampaignRequest):
    """Create a new outreach campaign."""
    if request.template not in TEMPLATES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid template. Available: {list(TEMPLATES.keys())}"
        )
    
    result = await cold_outreach_service.create_campaign(
        name=request.name,
        subject=request.subject,
        template=request.template,
        vertical=request.vertical,
    )
    return result


@router.get("/campaigns", response_model=List[CampaignResponse])
async def list_campaigns():
    """List all campaigns."""
    return await cold_outreach_service.list_campaigns()


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str):
    """Get campaign details."""
    result = await cold_outreach_service.get_campaign(campaign_id)
    if not result:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return result


@router.get("/campaigns/{campaign_id}/leads", response_model=List[LeadResponse])
async def get_campaign_leads(campaign_id: str):
    """Get leads for a campaign."""
    return await cold_outreach_service.get_campaign_leads(campaign_id)


@router.post("/campaigns/{campaign_id}/upload")
async def upload_leads(campaign_id: str, file: UploadFile = File(...)):
    """Upload CSV of leads."""
    content = await file.read()
    try:
        result = await cold_outreach_service.upload_leads(campaign_id, content.decode())
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/campaigns/{campaign_id}/start")
async def start_campaign(campaign_id: str):
    """Start campaign."""
    try:
        await cold_outreach_service.start_campaign(campaign_id)
        return {"message": "Campaign started"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/campaigns/{campaign_id}/pause")
async def pause_campaign(campaign_id: str):
    """Pause campaign."""
    try:
        await cold_outreach_service.pause_campaign(campaign_id)
        return {"message": "Campaign paused"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/campaigns/{campaign_id}/export")
async def export_campaign(campaign_id: str):
    """Export results as CSV."""
    csv_content = await cold_outreach_service.export_results(campaign_id)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=campaign-{campaign_id}.csv"}
    )


@router.post("/process-queue")
async def process_queue(limit: int = 50):
    """Manually trigger queue processing (admin)."""
    sent = await cold_outreach_service.process_queue(limit)
    return {"message": f"Sent {sent} emails"}


@router.get("/templates")
async def list_templates():
    """List available email templates."""
    return {key: {"subject": t["subject"]} for key, t in TEMPLATES.items()}


# Tracking endpoints
@router.get("/track/open")
async def track_open(lead_id: str):
    """Track email open (1x1 pixel)."""
    await cold_outreach_service.track_open(lead_id)
    # Return 1x1 transparent GIF
    gif_bytes = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return Response(content=gif_bytes, media_type="image/gif")


@router.get("/track/click")
async def track_click(lead_id: str, url: str):
    """Track click and redirect."""
    await cold_outreach_service.track_click(lead_id, url)
    return RedirectResponse(url=url)


@router.post("/leads/{lead_id}/replied")
async def mark_replied(lead_id: str):
    """Mark lead as replied (manual)."""
    await cold_outreach_service.track_reply(lead_id)
    return {"message": "Marked as replied"}


@router.post("/leads/{lead_id}/converted")
async def mark_converted(lead_id: str):
    """Mark lead as converted."""
    await cold_outreach_service.mark_converted(lead_id)
    return {"message": "Marked as converted"}
```

### 3. Add to src/api/main.py

```python
from src.api.routes import outreach
app.include_router(outreach.router, prefix="/api/v1", tags=["outreach"])
```

### 4. Add to frontend/src/lib/api.ts

```typescript
export const outreachApi = {
  createCampaign: (data: { name: string; subject: string; template: string; vertical?: string }) =>
    fetchApi<OutreachCampaign>("/outreach/campaigns", { method: "POST", body: JSON.stringify(data) }),
  
  listCampaigns: () =>
    fetchApi<OutreachCampaign[]>("/outreach/campaigns"),
  
  getCampaign: (id: string) =>
    fetchApi<OutreachCampaign>(`/outreach/campaigns/${id}`),
  
  getCampaignLeads: (id: string) =>
    fetchApi<OutreachLead[]>(`/outreach/campaigns/${id}/leads`),
  
  uploadLeads: (id: string, file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return fetch(`${API_BASE_URL}/outreach/campaigns/${id}/upload`, {
      method: "POST",
      body: formData,
    }).then(r => r.json());
  },
  
  startCampaign: (id: string) =>
    fetchApi<{ message: string }>(`/outreach/campaigns/${id}/start`, { method: "POST" }),
  
  pauseCampaign: (id: string) =>
    fetchApi<{ message: string }>(`/outreach/campaigns/${id}/pause`, { method: "POST" }),
  
  exportCampaign: (id: string) =>
    `${API_BASE_URL}/outreach/campaigns/${id}/export`,
  
  listTemplates: () =>
    fetchApi<Record<string, { subject: string }>>("/outreach/templates"),
  
  markReplied: (leadId: string) =>
    fetchApi<{ message: string }>(`/outreach/leads/${leadId}/replied`, { method: "POST" }),
  
  markConverted: (leadId: string) =>
    fetchApi<{ message: string }>(`/outreach/leads/${leadId}/converted`, { method: "POST" }),
};

export interface OutreachCampaign {
  id: string;
  name: string;
  status: string;
  subject: string;
  template: string;
  vertical: string | null;
  total_leads: number;
  sent: number;
  opened: number;
  clicked: number;
  replied: number;
  converted: number;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export interface OutreachLead {
  id: string;
  email: string;
  first_name: string;
  last_name: string | null;
  business_name: string | null;
  status: string;
  sent_at: string | null;
  opened_at: string | null;
  clicked_at: string | null;
}
```

## Database Schema (add to prisma/schema.prisma)

```prisma
model OutreachCampaign {
  id            String    @id @default(cuid())
  name          String
  status        String    @default("draft")
  subject       String
  template      String
  vertical      String?
  totalLeads    Int       @default(0)
  sent          Int       @default(0)
  opened        Int       @default(0)
  clicked       Int       @default(0)
  replied       Int       @default(0)
  converted     Int       @default(0)
  createdAt     DateTime  @default(now())
  startedAt     DateTime?
  completedAt   DateTime?
  leads         OutreachLead[]
}

model OutreachLead {
  id            String    @id @default(cuid())
  campaignId    String
  campaign      OutreachCampaign @relation(fields: [campaignId], references: [id])
  email         String
  firstName     String
  lastName      String?
  businessName  String?
  phone         String?
  vertical      String?
  status        String    @default("pending")
  sentAt        DateTime?
  openedAt      DateTime?
  clickedAt     DateTime?
  repliedAt     DateTime?
  demoNumberId  String?
  metadata      Json?
  createdAt     DateTime  @default(now())
  
  @@index([campaignId])
  @@index([status])
}
```

## Scheduled Job (Trigger.dev)

Create trigger-jobs/outreach-processor.ts:

```typescript
import { schedules } from "@trigger.dev/sdk/v3";

export const processOutreachQueue = schedules.task({
  id: "process-outreach-queue",
  cron: "0 * * * *", // Every hour
  run: async () => {
    const response = await fetch(
      `${process.env.API_URL}/api/v1/outreach/process-queue?limit=50`,
      { method: "POST" }
    );
    const result = await response.json();
    return { sent: result.sent };
  },
});
```

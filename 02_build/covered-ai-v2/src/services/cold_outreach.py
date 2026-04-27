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
import os

from prisma import Prisma

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
    def __init__(self, db: Prisma):
        self.db = db

    async def create_campaign(
        self,
        name: str,
        subject: str,
        template: str,
        vertical: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new outreach campaign."""
        campaign = await self.db.outreachcampaign.create(
            data={
                "name": name,
                "subject": subject,
                "template": template,
                "vertical": vertical,
                "status": CampaignStatus.DRAFT.value,
                "totalLeads": 0,
                "sent": 0,
                "opened": 0,
                "clicked": 0,
                "replied": 0,
                "converted": 0,
            }
        )

        return self._format_campaign(campaign)

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
        campaign = await self.db.outreachcampaign.find_unique(where={"id": campaign_id})
        if not campaign:
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
                existing = await self.db.outreachlead.find_first(
                    where={
                        "campaignId": campaign_id,
                        "email": email,
                    }
                )
                if existing:
                    skipped += 1
                    continue

                await self.db.outreachlead.create(
                    data={
                        "campaignId": campaign_id,
                        "email": email,
                        "firstName": first_name,
                        "lastName": row.get("last_name", "").strip() or None,
                        "businessName": row.get("business_name", "").strip() or None,
                        "phone": row.get("phone", "").strip() or None,
                        "vertical": row.get("vertical", "").strip() or campaign.vertical,
                        "status": LeadStatus.PENDING.value,
                    }
                )
                added += 1

            except Exception as e:
                errors.append(f"Error processing row: {e}")
                skipped += 1

        # Update campaign total
        total_leads = await self.db.outreachlead.count(where={"campaignId": campaign_id})
        await self.db.outreachcampaign.update(
            where={"id": campaign_id},
            data={"totalLeads": total_leads}
        )

        return {"added": added, "skipped": skipped, "errors": errors[:10]}

    async def start_campaign(self, campaign_id: str) -> None:
        """Start sending emails."""
        campaign = await self.db.outreachcampaign.find_unique(where={"id": campaign_id})
        if not campaign:
            raise ValueError("Campaign not found")

        await self.db.outreachcampaign.update(
            where={"id": campaign_id},
            data={
                "status": CampaignStatus.ACTIVE.value,
                "startedAt": datetime.utcnow(),
            }
        )

    async def pause_campaign(self, campaign_id: str) -> None:
        """Pause campaign."""
        campaign = await self.db.outreachcampaign.find_unique(where={"id": campaign_id})
        if not campaign:
            raise ValueError("Campaign not found")

        await self.db.outreachcampaign.update(
            where={"id": campaign_id},
            data={"status": CampaignStatus.PAUSED.value}
        )

    async def process_queue(self, limit: int = 50) -> int:
        """
        Process pending emails. Called by scheduled job.
        Rate limit: 50 emails per call (run every hour).
        Returns number sent.
        """
        sent_count = 0

        # Get active campaigns
        active_campaigns = await self.db.outreachcampaign.find_many(
            where={"status": CampaignStatus.ACTIVE.value}
        )

        for campaign in active_campaigns:
            if sent_count >= limit:
                break

            # Get pending leads for this campaign
            pending_leads = await self.db.outreachlead.find_many(
                where={
                    "campaignId": campaign.id,
                    "status": LeadStatus.PENDING.value,
                },
                take=limit - sent_count,
            )

            for lead in pending_leads:
                if sent_count >= limit:
                    break

                success = await self._send_email(campaign, lead)
                if success:
                    sent_count += 1
                    await self.db.outreachcampaign.update(
                        where={"id": campaign.id},
                        data={"sent": {"increment": 1}}
                    )

            # Check if campaign is complete
            remaining = await self.db.outreachlead.count(
                where={
                    "campaignId": campaign.id,
                    "status": LeadStatus.PENDING.value,
                }
            )

            if remaining == 0:
                await self.db.outreachcampaign.update(
                    where={"id": campaign.id},
                    data={
                        "status": CampaignStatus.COMPLETED.value,
                        "completedAt": datetime.utcnow(),
                    }
                )

        return sent_count

    async def _send_email(self, campaign, lead) -> bool:
        """Send email to a single lead."""
        template = TEMPLATES.get(campaign.template)
        if not template:
            return False

        # Render template
        subject = campaign.subject.format(
            first_name=lead.firstName,
            business_name=lead.businessName or "your business",
            vertical=lead.vertical or "business",
        )

        # Add tracking pixel and click tracking
        tracking_pixel = f'<img src="{TRACKING_BASE_URL}/open?lead_id={lead.id}" width="1" height="1" />'

        body = template["body"].format(
            first_name=lead.firstName,
            business_name=lead.businessName or "your business",
            vertical=lead.vertical or "business",
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
                    "to": lead.email,
                    "subject": subject,
                    "html": html_body,
                })
            except Exception as e:
                print(f"Failed to send email: {e}")
                return False
        else:
            print(f"[EMAIL MOCK] To: {lead.email}, Subject: {subject}")

        # Update lead status
        await self.db.outreachlead.update(
            where={"id": lead.id},
            data={
                "status": LeadStatus.SENT.value,
                "sentAt": datetime.utcnow(),
            }
        )

        return True

    async def track_open(self, lead_id: str) -> None:
        """Record email open."""
        lead = await self.db.outreachlead.find_unique(where={"id": lead_id})
        if lead and lead.status == LeadStatus.SENT.value:
            await self.db.outreachlead.update(
                where={"id": lead_id},
                data={
                    "status": LeadStatus.OPENED.value,
                    "openedAt": datetime.utcnow(),
                }
            )

            # Update campaign stats
            await self.db.outreachcampaign.update(
                where={"id": lead.campaignId},
                data={"opened": {"increment": 1}}
            )

    async def track_click(self, lead_id: str, url: str) -> None:
        """Record link click."""
        lead = await self.db.outreachlead.find_unique(where={"id": lead_id})
        if lead and lead.status in [LeadStatus.SENT.value, LeadStatus.OPENED.value]:
            await self.db.outreachlead.update(
                where={"id": lead_id},
                data={
                    "status": LeadStatus.CLICKED.value,
                    "clickedAt": datetime.utcnow(),
                }
            )

            await self.db.outreachcampaign.update(
                where={"id": lead.campaignId},
                data={"clicked": {"increment": 1}}
            )

    async def track_reply(self, lead_id: str) -> None:
        """Record reply (called manually or via email parsing)."""
        lead = await self.db.outreachlead.find_unique(where={"id": lead_id})
        if lead:
            await self.db.outreachlead.update(
                where={"id": lead_id},
                data={
                    "status": LeadStatus.REPLIED.value,
                    "repliedAt": datetime.utcnow(),
                }
            )

            await self.db.outreachcampaign.update(
                where={"id": lead.campaignId},
                data={"replied": {"increment": 1}}
            )

    async def mark_converted(self, lead_id: str) -> None:
        """Mark lead as converted."""
        lead = await self.db.outreachlead.find_unique(where={"id": lead_id})
        if lead:
            await self.db.outreachlead.update(
                where={"id": lead_id},
                data={"status": LeadStatus.CONVERTED.value}
            )

            await self.db.outreachcampaign.update(
                where={"id": lead.campaignId},
                data={"converted": {"increment": 1}}
            )

    async def get_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign with stats."""
        campaign = await self.db.outreachcampaign.find_unique(where={"id": campaign_id})
        if not campaign:
            return None
        return self._format_campaign(campaign)

    async def list_campaigns(self) -> List[Dict[str, Any]]:
        """List all campaigns."""
        campaigns = await self.db.outreachcampaign.find_many(
            order_by={"createdAt": "desc"}
        )
        return [self._format_campaign(c) for c in campaigns]

    async def get_campaign_leads(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get all leads for a campaign."""
        leads = await self.db.outreachlead.find_many(
            where={"campaignId": campaign_id},
            order_by={"createdAt": "desc"}
        )
        return [self._format_lead(l) for l in leads]

    async def export_results(self, campaign_id: str) -> str:
        """Export campaign results as CSV."""
        leads = await self.db.outreachlead.find_many(where={"campaignId": campaign_id})

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "email", "first_name", "last_name", "business_name", "phone",
            "vertical", "status", "sent_at", "opened_at", "clicked_at", "replied_at"
        ])
        writer.writeheader()

        for lead in leads:
            writer.writerow({
                "email": lead.email,
                "first_name": lead.firstName,
                "last_name": lead.lastName or "",
                "business_name": lead.businessName or "",
                "phone": lead.phone or "",
                "vertical": lead.vertical or "",
                "status": lead.status,
                "sent_at": lead.sentAt.isoformat() if lead.sentAt else "",
                "opened_at": lead.openedAt.isoformat() if lead.openedAt else "",
                "clicked_at": lead.clickedAt.isoformat() if lead.clickedAt else "",
                "replied_at": lead.repliedAt.isoformat() if lead.repliedAt else "",
            })

        return output.getvalue()

    def _format_campaign(self, campaign) -> Dict[str, Any]:
        """Format campaign for API response."""
        return {
            "id": campaign.id,
            "name": campaign.name,
            "status": campaign.status,
            "subject": campaign.subject,
            "template": campaign.template,
            "vertical": campaign.vertical,
            "total_leads": campaign.totalLeads,
            "sent": campaign.sent,
            "opened": campaign.opened,
            "clicked": campaign.clicked,
            "replied": campaign.replied,
            "converted": campaign.converted,
            "created_at": campaign.createdAt.isoformat(),
            "started_at": campaign.startedAt.isoformat() if campaign.startedAt else None,
            "completed_at": campaign.completedAt.isoformat() if campaign.completedAt else None,
        }

    def _format_lead(self, lead) -> Dict[str, Any]:
        """Format lead for API response."""
        return {
            "id": lead.id,
            "email": lead.email,
            "first_name": lead.firstName,
            "last_name": lead.lastName,
            "business_name": lead.businessName,
            "phone": lead.phone,
            "vertical": lead.vertical,
            "status": lead.status,
            "sent_at": lead.sentAt.isoformat() if lead.sentAt else None,
            "opened_at": lead.openedAt.isoformat() if lead.openedAt else None,
            "clicked_at": lead.clickedAt.isoformat() if lead.clickedAt else None,
            "replied_at": lead.repliedAt.isoformat() if lead.repliedAt else None,
        }


# Helper function to get service instance
def get_cold_outreach_service(db: Prisma) -> ColdOutreachService:
    return ColdOutreachService(db)

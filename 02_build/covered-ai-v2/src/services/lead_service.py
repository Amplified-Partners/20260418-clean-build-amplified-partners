"""
Lead Service

Business logic for lead management, including creation from calls
and triggering the nurture sequence.
"""

import os
import httpx
from typing import Optional, Dict, Any
from prisma import Prisma
from prisma.models import Lead, Client, Customer

from src.db import queries


class LeadService:
    """Service for managing leads."""

    def __init__(self, db: Prisma):
        self.db = db
        self.trigger_secret_key = os.getenv("TRIGGER_API_KEY")
        self.trigger_project_ref = "proj_mzlahtbhkhkroxbcabis"

    async def create_from_call(
        self,
        client: Client,
        caller_phone: str,
        call_id: Optional[str] = None,
        call_duration: Optional[int] = None,
        recording_url: Optional[str] = None,
        transcript: Optional[str] = None,
        summary: Optional[str] = None,
        customer_name: Optional[str] = None,
        address: Optional[str] = None,
        postcode: Optional[str] = None,
        job_type: Optional[str] = None,
        urgency: str = "routine"
    ) -> Lead:
        """
        Create a lead from a completed phone call.

        Flow:
        1. Find or create customer
        2. Create lead record
        3. Create nurture sequence
        4. Return lead with all associations
        """
        # 1. Find or create customer
        customer = await queries.find_or_create_customer(
            db=self.db,
            client_id=client.id,
            phone=caller_phone,
            name=customer_name or "Unknown",
            address=address,
            postcode=postcode
        )

        # 2. Create lead
        lead = await queries.create_lead(
            db=self.db,
            data={
                "clientId": client.id,
                "customerId": customer.id,
                "callerPhone": caller_phone,
                "callId": call_id,
                "callDuration": call_duration,
                "recordingUrl": recording_url,
                "transcript": transcript,
                "summary": summary,
                "customerName": customer_name,
                "address": address,
                "postcode": postcode,
                "jobType": job_type,
                "urgency": urgency,
                "status": "new"
            }
        )

        # 3. Create nurture sequence
        await queries.create_nurture_sequence(self.db, lead.id)

        # Reload lead with all associations
        lead = await queries.get_lead_by_id(self.db, lead.id)

        return lead

    async def trigger_nurture_sequence(self, lead: Lead, client: Client) -> bool:
        """
        Trigger the lead nurture sequence via Trigger.dev v4 API.

        Returns True if triggered successfully.
        """
        if not self.trigger_secret_key:
            print("⚠️ TRIGGER_API_KEY not set, skipping nurture trigger")
            return False

        try:
            # Trigger.dev v4 uses the tasks API
            async with httpx.AsyncClient() as http:
                response = await http.post(
                    f"https://api.trigger.dev/api/v1/tasks/lead-nurture-sequence/trigger",
                    headers={
                        "Authorization": f"Bearer {self.trigger_secret_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "payload": {
                            "lead": {
                                "id": lead.id,
                                "clientId": lead.clientId,
                                "customerName": lead.customerName,
                                "email": lead.customer.email if lead.customer else None,
                                "phone": lead.callerPhone,
                                "jobType": lead.jobType,
                                "urgency": lead.urgency,
                                "vertical": client.vertical
                            },
                            "client": {
                                "id": client.id,
                                "businessName": client.businessName,
                                "ownerName": client.ownerName,
                                "vertical": client.vertical
                            }
                        }
                    },
                    timeout=10.0
                )

                if response.status_code in (200, 201, 202):
                    print(f"🌱 Nurture sequence triggered for lead {lead.id}")
                    return True
                else:
                    print(f"❌ Failed to trigger nurture: {response.status_code} - {response.text}")
                    return False

        except Exception as e:
            print(f"❌ Error triggering nurture sequence: {e}")
            return False

    async def book_lead(
        self,
        lead_id: str,
        scheduled_date: str,
        scheduled_time: Optional[str] = None,
        quoted_amount: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Book a lead - create a job and update lead status.
        """
        lead = await queries.get_lead_by_id(self.db, lead_id)

        if not lead:
            raise ValueError(f"Lead {lead_id} not found")

        if not lead.customer:
            raise ValueError(f"Lead {lead_id} has no associated customer")

        # Create job
        from datetime import datetime
        job = await queries.create_job(
            db=self.db,
            data={
                "clientId": lead.clientId,
                "customerId": lead.customer.id,
                "leadId": lead.id,
                "title": lead.jobType or "Service Call",
                "description": lead.summary,
                "jobType": lead.jobType,
                "address": lead.address or lead.customer.address or "TBD",
                "postcode": lead.postcode or lead.customer.postcode,
                "scheduledDate": datetime.fromisoformat(scheduled_date),
                "scheduledTime": scheduled_time,
                "quotedAmount": quoted_amount,
                "status": "scheduled"
            }
        )

        # Update lead status
        await queries.update_lead_status(self.db, lead_id, "booked")

        # Stop nurture sequence
        await queries.stop_nurture_sequence(self.db, lead_id, "lead_booked")

        return {
            "lead_id": lead_id,
            "job_id": job.id,
            "status": "booked"
        }

    async def dismiss_lead(
        self,
        lead_id: str,
        reason: Optional[str] = None
    ) -> Lead:
        """Dismiss a lead."""
        lead = await queries.update_lead_status(
            self.db, lead_id, "dismissed", reason
        )

        # Stop nurture sequence
        await queries.stop_nurture_sequence(
            self.db, lead_id, f"dismissed: {reason or 'no reason provided'}"
        )

        return lead

    async def pause_nurture(self, lead_id: str) -> bool:
        """Pause the nurture sequence for a lead."""
        lead = await queries.get_lead_by_id(self.db, lead_id)

        if not lead or not lead.nurtureSequence:
            return False

        await self.db.nurturesequence.update(
            where={"id": lead.nurtureSequence.id},
            data={"status": "paused"}
        )

        return True

    async def resume_nurture(self, lead_id: str) -> bool:
        """Resume the nurture sequence for a lead."""
        lead = await queries.get_lead_by_id(self.db, lead_id)

        if not lead or not lead.nurtureSequence:
            return False

        if lead.nurtureSequence.status != "paused":
            return False

        await self.db.nurturesequence.update(
            where={"id": lead.nurtureSequence.id},
            data={"status": "active"}
        )

        # Re-trigger nurture sequence
        client = await queries.get_client_by_id(self.db, lead.clientId)
        if client:
            await self.trigger_nurture_sequence(lead, client)

        return True

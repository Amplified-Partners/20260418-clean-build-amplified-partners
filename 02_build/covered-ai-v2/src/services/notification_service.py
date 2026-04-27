"""
Notification Service

Send notifications via email, SMS, and WhatsApp.
Logs all notifications to the database for audit trail.
"""

import os
from typing import Optional, Dict, Any
from prisma import Prisma
import httpx
import resend

from src.db import queries


class NotificationService:
    """Service for sending notifications across channels."""

    def __init__(self, db: Prisma):
        self.db = db

        # Resend setup
        resend_api_key = os.getenv("RESEND_API_KEY")
        if resend_api_key:
            resend.api_key = resend_api_key
        self.resend_from = os.getenv("RESEND_FROM_EMAIL", "Covered AI <noreply@covered.ai>")

        # Twilio setup
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
        self.twilio_whatsapp = os.getenv("TWILIO_WHATSAPP_NUMBER")

    def _format_uk_phone(self, phone: str) -> str:
        """Format phone number to E.164 format."""
        cleaned = "".join(c for c in phone if c.isdigit() or c == "+")

        if cleaned.startswith("44"):
            return f"+{cleaned}"
        elif cleaned.startswith("0"):
            return f"+44{cleaned[1:]}"
        elif not cleaned.startswith("+"):
            return f"+44{cleaned}"

        return cleaned

    async def send_email(
        self,
        client_id: str,
        to: str,
        subject: str,
        html: str,
        lead_id: Optional[str] = None,
        job_id: Optional[str] = None,
        notification_type: str = "email"
    ) -> Dict[str, Any]:
        """
        Send an email and log it.

        Returns dict with success status and notification ID.
        """
        # Create notification record
        notification = await queries.create_notification(
            db=self.db,
            data={
                "clientId": client_id,
                "leadId": lead_id,
                "jobId": job_id,
                "type": notification_type,
                "channel": "email",
                "recipient": to,
                "subject": subject,
                "message": html,
                "status": "pending"
            }
        )

        try:
            # Send via Resend
            result = resend.Emails.send({
                "from": self.resend_from,
                "to": [to],
                "subject": subject,
                "html": html
            })

            # Update status
            await queries.update_notification_status(
                self.db, notification.id, "sent"
            )

            return {
                "success": True,
                "notification_id": notification.id,
                "external_id": result.get("id")
            }

        except Exception as e:
            await queries.update_notification_status(
                self.db, notification.id, "failed", str(e)
            )
            return {
                "success": False,
                "notification_id": notification.id,
                "error": str(e)
            }

    async def send_sms(
        self,
        client_id: str,
        to: str,
        message: str,
        lead_id: Optional[str] = None,
        job_id: Optional[str] = None,
        notification_type: str = "sms"
    ) -> Dict[str, Any]:
        """Send an SMS and log it."""
        formatted_to = self._format_uk_phone(to)

        # Create notification record
        notification = await queries.create_notification(
            db=self.db,
            data={
                "clientId": client_id,
                "leadId": lead_id,
                "jobId": job_id,
                "type": notification_type,
                "channel": "sms",
                "recipient": formatted_to,
                "message": message,
                "status": "pending"
            }
        )

        if not self.twilio_sid or not self.twilio_token:
            await queries.update_notification_status(
                self.db, notification.id, "failed", "Twilio not configured"
            )
            return {
                "success": False,
                "notification_id": notification.id,
                "error": "Twilio not configured"
            }

        try:
            async with httpx.AsyncClient() as http:
                response = await http.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json",
                    auth=(self.twilio_sid, self.twilio_token),
                    data={
                        "To": formatted_to,
                        "From": self.twilio_phone,
                        "Body": message
                    },
                    timeout=10.0
                )

                if response.status_code == 201:
                    result = response.json()
                    await queries.update_notification_status(
                        self.db, notification.id, "sent"
                    )
                    return {
                        "success": True,
                        "notification_id": notification.id,
                        "external_id": result.get("sid")
                    }
                else:
                    error = response.text
                    await queries.update_notification_status(
                        self.db, notification.id, "failed", error
                    )
                    return {
                        "success": False,
                        "notification_id": notification.id,
                        "error": error
                    }

        except Exception as e:
            await queries.update_notification_status(
                self.db, notification.id, "failed", str(e)
            )
            return {
                "success": False,
                "notification_id": notification.id,
                "error": str(e)
            }

    async def send_whatsapp(
        self,
        client_id: str,
        to: str,
        message: str,
        lead_id: Optional[str] = None,
        job_id: Optional[str] = None,
        notification_type: str = "whatsapp"
    ) -> Dict[str, Any]:
        """Send a WhatsApp message and log it."""
        formatted_to = self._format_uk_phone(to)
        whatsapp_to = f"whatsapp:{formatted_to}"
        whatsapp_from = self.twilio_whatsapp or f"whatsapp:{self.twilio_phone}"

        # Create notification record
        notification = await queries.create_notification(
            db=self.db,
            data={
                "clientId": client_id,
                "leadId": lead_id,
                "jobId": job_id,
                "type": notification_type,
                "channel": "whatsapp",
                "recipient": formatted_to,
                "message": message,
                "status": "pending"
            }
        )

        if not self.twilio_sid or not self.twilio_token:
            await queries.update_notification_status(
                self.db, notification.id, "failed", "Twilio not configured"
            )
            return {
                "success": False,
                "notification_id": notification.id,
                "error": "Twilio not configured"
            }

        try:
            async with httpx.AsyncClient() as http:
                response = await http.post(
                    f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json",
                    auth=(self.twilio_sid, self.twilio_token),
                    data={
                        "To": whatsapp_to,
                        "From": whatsapp_from,
                        "Body": message
                    },
                    timeout=10.0
                )

                if response.status_code == 201:
                    result = response.json()
                    await queries.update_notification_status(
                        self.db, notification.id, "sent"
                    )
                    return {
                        "success": True,
                        "notification_id": notification.id,
                        "external_id": result.get("sid")
                    }
                else:
                    error = response.text
                    await queries.update_notification_status(
                        self.db, notification.id, "failed", error
                    )
                    return {
                        "success": False,
                        "notification_id": notification.id,
                        "error": error
                    }

        except Exception as e:
            await queries.update_notification_status(
                self.db, notification.id, "failed", str(e)
            )
            return {
                "success": False,
                "notification_id": notification.id,
                "error": str(e)
            }

    async def notify_owner(
        self,
        client_id: str,
        lead_id: str,
        message: str,
        subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Notify the business owner about a new lead.
        Sends via their preferred channel(s).
        """
        from src.db import queries as db_queries

        client = await db_queries.get_client_by_id(self.db, client_id)
        if not client:
            return {"success": False, "error": "Client not found"}

        results = []

        # Send email if enabled
        if client.notifyViaEmail and client.notificationEmail:
            result = await self.send_email(
                client_id=client_id,
                to=client.notificationEmail,
                subject=subject or "New Lead Alert",
                html=f"<p>{message}</p>",
                lead_id=lead_id,
                notification_type="owner_notification"
            )
            results.append({"channel": "email", **result})

        # Send WhatsApp if enabled
        if client.notifyViaWhatsapp and client.notificationPhone:
            result = await self.send_whatsapp(
                client_id=client_id,
                to=client.notificationPhone,
                message=message,
                lead_id=lead_id,
                notification_type="owner_notification"
            )
            results.append({"channel": "whatsapp", **result})

        # Send SMS if enabled
        if client.notifyViaSms and client.notificationPhone:
            result = await self.send_sms(
                client_id=client_id,
                to=client.notificationPhone,
                message=message,
                lead_id=lead_id,
                notification_type="owner_notification"
            )
            results.append({"channel": "sms", **result})

        return {
            "success": any(r.get("success") for r in results),
            "notifications": results
        }

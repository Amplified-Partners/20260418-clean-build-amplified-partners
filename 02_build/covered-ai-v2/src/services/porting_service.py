"""
Porting Service - Handles the full number porting workflow

Integrates:
- LOA PDF generation
- Email notifications
- Status tracking
- Twilio porting API (when ready)
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid

from src.services.loa_generator import generate_loa_pdf


class PortingService:
    """Service for managing number porting requests."""
    
    # Status flow
    STATUSES = {
        "pending": "Request received, awaiting processing",
        "loa_generated": "LOA document generated",
        "submitted": "Submitted to carrier",
        "in_progress": "Port in progress with carrier",
        "scheduled": "Port scheduled for specific date",
        "completed": "Port completed successfully",
        "failed": "Port failed - action required",
        "cancelled": "Port cancelled by user",
    }
    
    def __init__(self):
        # In-memory storage - replace with database
        self.requests: Dict[str, Dict[str, Any]] = {}
    
    async def create_request(
        self,
        client_id: str,
        number_to_port: str,
        current_provider: str,
        account_number: str,
        account_holder_name: str,
        billing_postcode: str,
        authorized_signature: str,
        business_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new porting request and trigger the workflow.
        """
        request_id = f"PORT-{uuid.uuid4().hex[:8].upper()}"
        clean_number = ''.join(filter(str.isdigit, number_to_port))
        submitted_at = datetime.utcnow()
        estimated_completion = submitted_at + timedelta(days=10)
        
        # Create request record
        request = {
            "id": request_id,
            "client_id": client_id,
            "number_to_port": number_to_port,
            "clean_number": clean_number,
            "current_provider": current_provider,
            "account_number": account_number,
            "account_holder_name": account_holder_name,
            "billing_postcode": billing_postcode.upper(),
            "authorized_signature": authorized_signature,
            "business_name": business_name,
            "email": email,
            "status": "pending",
            "status_history": [
                {"status": "pending", "timestamp": submitted_at.isoformat(), "note": "Request created"}
            ],
            "submitted_at": submitted_at.isoformat(),
            "estimated_completion": estimated_completion.strftime("%Y-%m-%d"),
            "scheduled_port_date": None,
            "completed_at": None,
            "loa_pdf_url": None,
            "twilio_port_order_sid": None,
            "notes": [],
        }
        
        self.requests[request_id] = request
        
        # Generate LOA PDF
        loa_pdf = await self.generate_loa(request_id)
        
        # Send confirmation email
        if email:
            await self.send_confirmation_email(request_id)
        
        return request
    
    async def generate_loa(self, request_id: str) -> bytes:
        """Generate LOA PDF for a porting request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        pdf_bytes = generate_loa_pdf(
            number_to_port=request["number_to_port"],
            current_provider=request["current_provider"],
            account_number=request["account_number"],
            account_holder_name=request["account_holder_name"],
            billing_postcode=request["billing_postcode"],
            authorized_signature=request["authorized_signature"],
            business_name=request.get("business_name"),
            request_id=request_id,
        )
        
        # TODO: Upload to S3/storage and save URL
        # For now, we'll store the bytes temporarily
        
        self._update_status(request_id, "loa_generated", "LOA document generated")
        
        return pdf_bytes
    
    async def send_confirmation_email(self, request_id: str) -> bool:
        """Send confirmation email to customer."""
        request = self.requests.get(request_id)
        if not request or not request.get("email"):
            return False
        
        # TODO: Integrate with Resend
        # For now, log the action
        self._add_note(request_id, f"Confirmation email queued for {request['email']}")
        
        return True
    
    async def submit_to_twilio(self, request_id: str) -> Optional[str]:
        """
        Submit porting request to Twilio.
        
        Returns Twilio Port Order SID if successful.
        """
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        # TODO: Implement Twilio Porting API
        # https://www.twilio.com/docs/phone-numbers/porting-phone-numbers
        
        # For now, simulate submission
        self._update_status(request_id, "submitted", "Submitted to carrier via Twilio")
        
        return None  # Would return Twilio Port Order SID
    
    async def check_status(self, request_id: str) -> Dict[str, Any]:
        """Check and update status from Twilio."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        # TODO: Check Twilio API for status updates
        
        return {
            "id": request_id,
            "status": request["status"],
            "status_description": self.STATUSES.get(request["status"], "Unknown"),
            "estimated_completion": request["estimated_completion"],
            "scheduled_port_date": request.get("scheduled_port_date"),
        }
    
    async def complete_port(self, request_id: str) -> Dict[str, Any]:
        """Mark port as completed."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        request["completed_at"] = datetime.utcnow().isoformat()
        self._update_status(request_id, "completed", "Number successfully ported")
        
        # TODO: Send completion email
        # TODO: Update Vapi assistant with new number
        # TODO: Update client record
        
        return request
    
    async def cancel_port(self, request_id: str, reason: str) -> Dict[str, Any]:
        """Cancel a porting request."""
        request = self.requests.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")
        
        if request["status"] == "completed":
            raise ValueError("Cannot cancel a completed port")
        
        self._update_status(request_id, "cancelled", f"Cancelled: {reason}")
        
        return request
    
    def get_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get a porting request by ID."""
        return self.requests.get(request_id)
    
    def list_requests(
        self,
        client_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list:
        """List porting requests with optional filters."""
        requests = list(self.requests.values())
        
        if client_id:
            requests = [r for r in requests if r["client_id"] == client_id]
        
        if status:
            requests = [r for r in requests if r["status"] == status]
        
        return sorted(requests, key=lambda x: x["submitted_at"], reverse=True)
    
    def _update_status(self, request_id: str, status: str, note: str):
        """Update request status and add to history."""
        request = self.requests.get(request_id)
        if request:
            request["status"] = status
            request["status_history"].append({
                "status": status,
                "timestamp": datetime.utcnow().isoformat(),
                "note": note,
            })
    
    def _add_note(self, request_id: str, note: str):
        """Add a note to the request."""
        request = self.requests.get(request_id)
        if request:
            request["notes"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "note": note,
            })


# Singleton instance
porting_service = PortingService()

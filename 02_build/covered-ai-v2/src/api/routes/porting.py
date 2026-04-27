"""
Porting API routes - Handle number porting requests
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import io

from src.services.porting_service import porting_service
from src.services.loa_generator import generate_loa_pdf

router = APIRouter(prefix="/porting", tags=["porting"])


class PortingRequest(BaseModel):
    number_to_port: str
    current_provider: str
    account_number: str
    account_holder_name: str
    billing_postcode: str
    authorized_signature: str
    business_name: Optional[str] = None
    email: Optional[str] = None


class PortingResponse(BaseModel):
    id: str
    status: str
    number_to_port: str
    current_provider: str
    submitted_at: str
    estimated_completion: str
    message: str


class PortingStatus(BaseModel):
    id: str
    number_to_port: str
    current_provider: str
    status: str
    status_description: str
    submitted_at: str
    estimated_completion: Optional[str]
    scheduled_port_date: Optional[str]
    completed_at: Optional[str]
    status_history: List[dict]


class PortingListItem(BaseModel):
    id: str
    number_to_port: str
    current_provider: str
    status: str
    submitted_at: str
    estimated_completion: Optional[str]


@router.post("/request", response_model=PortingResponse)
async def create_porting_request(request: PortingRequest):
    """
    Submit a new number porting request.
    
    This endpoint:
    1. Validates the request data
    2. Creates a porting request record
    3. Generates LOA PDF
    4. Sends confirmation email
    """
    # Clean phone number
    clean_number = ''.join(filter(str.isdigit, request.number_to_port))
    
    # Basic validation
    if len(clean_number) < 10:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    
    if not request.account_number:
        raise HTTPException(status_code=400, detail="Account number is required")
    
    if not request.authorized_signature:
        raise HTTPException(status_code=400, detail="Authorization signature is required")
    
    # Create porting request via service
    result = await porting_service.create_request(
        client_id="temp",  # TODO: Get from auth
        number_to_port=request.number_to_port,
        current_provider=request.current_provider,
        account_number=request.account_number,
        account_holder_name=request.account_holder_name,
        billing_postcode=request.billing_postcode,
        authorized_signature=request.authorized_signature,
        business_name=request.business_name,
        email=request.email,
    )
    
    return PortingResponse(
        id=result["id"],
        status=result["status"],
        number_to_port=result["number_to_port"],
        current_provider=result["current_provider"],
        submitted_at=result["submitted_at"],
        estimated_completion=result["estimated_completion"],
        message="Porting request submitted successfully. LOA generated. We'll begin processing immediately."
    )


@router.get("/status/{request_id}", response_model=PortingStatus)
async def get_porting_status(request_id: str):
    """Get the status of a porting request."""
    request = porting_service.get_request(request_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Porting request not found")
    
    return PortingStatus(
        id=request["id"],
        number_to_port=request["number_to_port"],
        current_provider=request["current_provider"],
        status=request["status"],
        status_description=porting_service.STATUSES.get(request["status"], "Unknown"),
        submitted_at=request["submitted_at"],
        estimated_completion=request["estimated_completion"],
        scheduled_port_date=request.get("scheduled_port_date"),
        completed_at=request.get("completed_at"),
        status_history=request["status_history"],
    )


@router.get("/requests", response_model=List[PortingListItem])
async def list_porting_requests(
    status: Optional[str] = None,
):
    """List all porting requests (admin endpoint)."""
    requests = porting_service.list_requests(status=status)
    
    return [
        PortingListItem(
            id=r["id"],
            number_to_port=r["number_to_port"],
            current_provider=r["current_provider"],
            status=r["status"],
            submitted_at=r["submitted_at"],
            estimated_completion=r["estimated_completion"],
        )
        for r in requests
    ]


@router.get("/loa/{request_id}")
async def download_loa(request_id: str):
    """Download the LOA PDF for a porting request."""
    request = porting_service.get_request(request_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Porting request not found")
    
    # Generate PDF
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
    
    # Return as downloadable PDF
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=LOA-{request_id}.pdf"
        }
    )


@router.post("/submit/{request_id}")
async def submit_to_carrier(request_id: str):
    """Submit porting request to carrier (admin endpoint)."""
    request = porting_service.get_request(request_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Porting request not found")
    
    if request["status"] not in ["pending", "loa_generated"]:
        raise HTTPException(status_code=400, detail="Request already submitted or completed")
    
    await porting_service.submit_to_twilio(request_id)
    
    return {"message": "Request submitted to carrier", "id": request_id}


@router.post("/complete/{request_id}")
async def complete_port(request_id: str):
    """Mark porting request as completed (admin endpoint)."""
    request = porting_service.get_request(request_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Porting request not found")
    
    result = await porting_service.complete_port(request_id)
    
    return {"message": "Port completed successfully", "id": request_id}


@router.post("/cancel/{request_id}")
async def cancel_port(request_id: str, reason: str = "Cancelled by user"):
    """Cancel a porting request."""
    request = porting_service.get_request(request_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Porting request not found")
    
    try:
        await porting_service.cancel_port(request_id, reason)
        return {"message": "Port cancelled", "id": request_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

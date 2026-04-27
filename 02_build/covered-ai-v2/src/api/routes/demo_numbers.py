"""
Demo Numbers API Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from src.db.client import get_prisma
from src.services.demo_numbers import get_demo_number_service

router = APIRouter()


class ProvisionRequest(BaseModel):
    business_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    vertical: Optional[str] = None


class DemoNumberResponse(BaseModel):
    id: str
    phone_number: str
    phone_number_display: str
    business_name: str
    contact_name: Optional[str]
    contact_email: Optional[str]
    vertical: Optional[str]
    vapi_assistant_id: Optional[str]
    status: str
    call_count: int
    last_called_at: Optional[str]
    created_at: str
    expires_at: str
    converted_at: Optional[str]
    client_id: Optional[str]


class ExtendRequest(BaseModel):
    days: int = 7


class ConvertRequest(BaseModel):
    client_id: str


@router.post("/provision", response_model=DemoNumberResponse)
async def provision_demo_number(request: ProvisionRequest, db=Depends(get_prisma)):
    """Provision a new personalized demo number."""
    service = get_demo_number_service(db)

    try:
        result = await service.provision(
            business_name=request.business_name,
            contact_name=request.contact_name,
            contact_email=request.contact_email,
            vertical=request.vertical,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[DemoNumberResponse])
async def list_demo_numbers(status: Optional[str] = None, db=Depends(get_prisma)):
    """List all demo numbers."""
    service = get_demo_number_service(db)
    return await service.list(status=status)


@router.get("/{demo_id}", response_model=DemoNumberResponse)
async def get_demo_number(demo_id: str, db=Depends(get_prisma)):
    """Get demo number details."""
    service = get_demo_number_service(db)
    result = await service.get(demo_id)
    if not result:
        raise HTTPException(status_code=404, detail="Demo number not found")
    return result


@router.post("/{demo_id}/extend")
async def extend_demo_number(demo_id: str, request: ExtendRequest, db=Depends(get_prisma)):
    """Extend demo number expiry."""
    service = get_demo_number_service(db)
    try:
        result = await service.extend(demo_id, request.days)
        return {"message": f"Extended by {request.days} days", "expires_at": result["expires_at"]}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{demo_id}/convert")
async def convert_demo_number(demo_id: str, request: ConvertRequest, db=Depends(get_prisma)):
    """Mark demo as converted."""
    service = get_demo_number_service(db)
    try:
        await service.convert(demo_id, request.client_id)
        return {"message": "Marked as converted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{demo_id}")
async def release_demo_number(demo_id: str, db=Depends(get_prisma)):
    """Release demo number."""
    service = get_demo_number_service(db)
    try:
        await service.release(demo_id)
        return {"message": "Number released"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/expire")
async def expire_old_numbers(db=Depends(get_prisma)):
    """Manually trigger expiry of old numbers (admin)."""
    service = get_demo_number_service(db)
    count = await service.expire_old_numbers()
    return {"message": f"Expired {count} numbers"}

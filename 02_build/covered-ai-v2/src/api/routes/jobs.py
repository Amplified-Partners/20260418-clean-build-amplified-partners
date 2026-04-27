"""
Jobs Routes - Job management for a client
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from src.db.client import get_prisma
from src.db import queries

router = APIRouter()


class JobStatus(str, Enum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class JobCreate(BaseModel):
    customer_id: str
    lead_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    job_type: Optional[str] = None
    address: str
    postcode: Optional[str] = None
    scheduled_date: datetime
    scheduled_time: Optional[str] = None
    estimated_duration: Optional[int] = None
    quoted_amount: Optional[float] = None


class JobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    scheduled_date: Optional[datetime] = None
    scheduled_time: Optional[str] = None
    final_amount: Optional[float] = None
    notes: Optional[str] = None


def job_to_response(job) -> dict:
    """Convert Prisma job to response dict."""
    return {
        "id": job.id,
        "client_id": job.clientId,
        "customer_id": job.customerId,
        "lead_id": job.leadId,
        "title": job.title,
        "description": job.description,
        "job_type": job.jobType,
        "address": job.address,
        "postcode": job.postcode,
        "scheduled_date": job.scheduledDate,
        "scheduled_time": job.scheduledTime,
        "estimated_duration": job.estimatedDuration,
        "quoted_amount": float(job.quotedAmount) if job.quotedAmount else None,
        "final_amount": float(job.finalAmount) if job.finalAmount else None,
        "status": job.status,
        "created_at": job.createdAt,
        "completed_at": job.completedAt,
        "customer": {
            "id": job.customer.id,
            "name": job.customer.name,
            "phone": job.customer.phone,
            "email": job.customer.email
        } if job.customer else None
    }


@router.get("")
async def list_jobs(
    client_id: str,
    status: Optional[JobStatus] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List jobs for a client."""
    client = await queries.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    jobs, total = await queries.list_jobs(
        db,
        client_id=client_id,
        status=status.value if status else None,
        limit=limit,
        offset=offset
    )

    return {
        "jobs": [job_to_response(job) for job in jobs],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("")
async def create_job(client_id: str, job: JobCreate, db=Depends(get_prisma)):
    """Create a new job."""
    client = await queries.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    new_job = await queries.create_job(
        db,
        data={
            "clientId": client_id,
            "customerId": job.customer_id,
            "leadId": job.lead_id,
            "title": job.title,
            "description": job.description,
            "jobType": job.job_type,
            "address": job.address,
            "postcode": job.postcode,
            "scheduledDate": job.scheduled_date,
            "scheduledTime": job.scheduled_time,
            "estimatedDuration": job.estimated_duration,
            "quotedAmount": job.quoted_amount,
            "status": "scheduled"
        }
    )

    return {
        "id": new_job.id,
        "message": "Job created",
        **job_to_response(new_job)
    }


@router.get("/{job_id}")
async def get_job(client_id: str, job_id: str, db=Depends(get_prisma)):
    """Get job by ID."""
    job = await queries.get_job_by_id(db, job_id)

    if not job or job.clientId != client_id:
        raise HTTPException(status_code=404, detail="Job not found")

    return job_to_response(job)


@router.patch("/{job_id}")
async def update_job(
    client_id: str,
    job_id: str,
    update: JobUpdate,
    db=Depends(get_prisma)
):
    """Update job status."""
    job = await queries.get_job_by_id(db, job_id)
    if not job or job.clientId != client_id:
        raise HTTPException(status_code=404, detail="Job not found")

    # Build update data
    if update.status:
        job = await queries.update_job_status(
            db,
            job_id,
            update.status.value,
            final_amount=update.final_amount
        )

        if update.status == JobStatus.completed:
            # Log for review request trigger
            print(f"Job {job_id} completed - review request will be triggered")
            # TODO: Trigger review-request job via Trigger.dev

    return {"id": job_id, "message": "Job updated", **job_to_response(job)}


@router.post("/{job_id}/complete")
async def complete_job(
    client_id: str,
    job_id: str,
    final_amount: Optional[float] = None,
    db=Depends(get_prisma)
):
    """
    Mark job as completed.

    This triggers:
    1. Job status update
    2. Review request (after 2 hour delay)
    """
    job = await queries.get_job_by_id(db, job_id)
    if not job or job.clientId != client_id:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update job status
    job = await queries.update_job_status(
        db, job_id, "completed", final_amount=final_amount
    )

    # TODO: Trigger review-request job via Trigger.dev
    print(f"Job {job_id} completed - queuing review request")

    return {
        "id": job_id,
        "status": "completed",
        "final_amount": final_amount,
        "review_request_scheduled": True,
    }

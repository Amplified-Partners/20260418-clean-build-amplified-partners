"""
Content Engine API Router

Mounts at /content/ in app/main.py.

Endpoints:
  POST /content/atomise              — Submit pillar content, get variants back + Telegram review
  GET  /content/jobs                 — List all content jobs
  GET  /content/jobs/{job_id}        — Job details + variants
  GET  /content/variants/{id}        — Single variant
  POST /content/variants/{id}/approve — Manual approve (fallback if Telegram is down)
  POST /content/variants/{id}/reject  — Manual reject
  GET  /content/analytics            — Engagement data
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.content.atomiser import atomise
from app.content.models_orm import ContentAnalyticsORM, ContentJobORM, ContentVariantORM
from app.content.prospect_research import router as prospect_router
from app.content.telegram_gate import send_job_variants_for_review
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content", tags=["Content Engine"])

# Mount prospect research sub-router
router.include_router(prospect_router)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class AtomiseRequest(BaseModel):
    pillar_text: str = Field(..., min_length=50, description="The source content to atomise")
    title: Optional[str] = Field(None, description="Optional label for this job")
    source: str = Field("manual", description="Source type: manual, voice_transcript, substack_draft")
    send_to_telegram: bool = Field(True, description="Send variants to Telegram for review immediately")


class VariantOut(BaseModel):
    id: int
    platform: str
    content: str
    review_status: str
    publish_status: str
    scheduled_for: Optional[datetime]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class JobOut(BaseModel):
    id: int
    title: Optional[str]
    source: str
    status: str
    created_at: datetime
    variants: list[VariantOut] = []

    class Config:
        from_attributes = True


class AtomiseResponse(BaseModel):
    job_id: int
    variants_created: int
    platforms: list[str]
    message: str


class AnalyticsOut(BaseModel):
    id: int
    variant_id: int
    platform: str
    published_at: Optional[datetime]
    likes: int
    shares: int
    comments: int
    clicks: int
    impressions: int
    platform_post_id: Optional[str]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/atomise", response_model=AtomiseResponse)
async def atomise_content(
    request: AtomiseRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Submit pillar content for atomisation.

    Creates a ContentJob, runs Claude to generate 5 platform variants,
    stores them in the DB, and sends them to Telegram for Ewan's review.

    The Telegram review is fire-and-forget (background task) so this endpoint
    returns immediately once variants are stored.
    """
    # 1. Create job
    job = ContentJobORM(
        title=request.title,
        pillar_text=request.pillar_text,
        source=request.source,
        status="atomising",
    )
    db.add(job)
    await db.flush()  # Get job.id without full commit
    job_id = job.id

    # 2. Run atomiser
    try:
        variants = await atomise(request.pillar_text, title=request.title)
    except Exception as e:
        job.status = "failed"
        await db.commit()
        logger.error("Atomise failed for job %d: %s", job_id, e)
        raise HTTPException(status_code=500, detail=f"Atomisation failed: {e}")

    # 3. Store variants
    variant_ids = []
    for v in variants:
        orm_variant = ContentVariantORM(
            job_id=job_id,
            platform=v.platform,
            content=v.content,
            metadata_=v.metadata,
            review_status="pending",
            publish_status="not_scheduled",
        )
        db.add(orm_variant)
        await db.flush()
        variant_ids.append(orm_variant.id)

    job.status = "review"
    await db.commit()

    platforms = [v.platform for v in variants]
    logger.info("Job %d: atomised %d variants (%s)", job_id, len(variants), ", ".join(platforms))

    # 4. Send to Telegram in background (non-blocking)
    if request.send_to_telegram:
        background_tasks.add_task(send_job_variants_for_review, job_id)

    return AtomiseResponse(
        job_id=job_id,
        variants_created=len(variants),
        platforms=platforms,
        message=(
            f"Created {len(variants)} variants. "
            + ("Sending to Telegram for review." if request.send_to_telegram else "Review via API.")
        ),
    )


@router.get("/jobs", response_model=list[JobOut])
async def list_jobs(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List recent content jobs."""
    result = await db.execute(
        select(ContentJobORM)
        .options(selectinload(ContentJobORM.variants))
        .order_by(ContentJobORM.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/jobs/{job_id}", response_model=JobOut)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    """Get a content job with all its variants."""
    result = await db.execute(
        select(ContentJobORM)
        .options(selectinload(ContentJobORM.variants))
        .where(ContentJobORM.id == job_id)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/variants/{variant_id}", response_model=VariantOut)
async def get_variant(variant_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single content variant."""
    variant = await db.get(ContentVariantORM, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant


@router.post("/variants/{variant_id}/approve")
async def approve_variant(variant_id: int, db: AsyncSession = Depends(get_db)):
    """
    Manually approve a variant (fallback if Telegram is unavailable).
    Prefer Telegram review — this is the escape hatch.
    """
    variant = await db.get(ContentVariantORM, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    variant.review_status = "approved"
    variant.publish_status = "queued"
    await db.commit()
    return {"status": "approved", "variant_id": variant_id, "platform": variant.platform}


@router.post("/variants/{variant_id}/reject")
async def reject_variant(
    variant_id: int,
    reason: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Reject a variant."""
    variant = await db.get(ContentVariantORM, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    variant.review_status = "rejected"
    variant.reject_reason = reason or "Rejected via API"
    await db.commit()
    return {"status": "rejected", "variant_id": variant_id}


@router.get("/analytics", response_model=list[AnalyticsOut])
async def get_analytics(
    limit: int = 50,
    platform: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get content analytics, optionally filtered by platform."""
    query = select(ContentAnalyticsORM).order_by(ContentAnalyticsORM.published_at.desc()).limit(limit)
    if platform:
        query = query.where(ContentAnalyticsORM.platform == platform)
    result = await db.execute(query)
    return result.scalars().all()

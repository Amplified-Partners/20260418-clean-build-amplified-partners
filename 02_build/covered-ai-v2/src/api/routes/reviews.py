"""
Reviews Routes - Review management and request tracking
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta

from src.db.client import get_prisma

router = APIRouter()


class ReviewCreate(BaseModel):
    job_id: Optional[str] = None
    customer_id: Optional[str] = None
    platform: str = "google"
    rating: int
    review_text: Optional[str] = None
    reviewer_name: Optional[str] = None
    external_id: Optional[str] = None
    external_url: Optional[str] = None


class ReviewRequestCreate(BaseModel):
    job_id: str
    customer_email: str


def review_to_response(review) -> dict:
    """Convert Prisma review to response dict."""
    return {
        "id": review.id,
        "client_id": review.clientId,
        "job_id": review.jobId,
        "customer_id": review.customerId,
        "platform": review.platform,
        "rating": review.rating,
        "review_text": review.reviewText,
        "reviewer_name": review.reviewerName,
        "external_id": review.externalId,
        "external_url": review.externalUrl,
        "request_sent_at": review.requestSentAt,
        "received_at": review.receivedAt,
        "response_text": review.responseText,
        "responded_at": review.respondedAt,
        "created_at": review.createdAt,
    }


@router.get("")
async def list_reviews(
    client_id: str,
    platform: Optional[str] = None,
    rating_min: Optional[int] = None,
    rating_max: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List reviews for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    where = {"clientId": client_id}

    if platform:
        where["platform"] = platform

    if rating_min is not None or rating_max is not None:
        where["rating"] = {}
        if rating_min is not None:
            where["rating"]["gte"] = rating_min
        if rating_max is not None:
            where["rating"]["lte"] = rating_max

    reviews = await db.review.find_many(
        where=where,
        order={"createdAt": "desc"},
        take=limit,
        skip=offset,
    )

    total = await db.review.count(where=where)

    return {
        "reviews": [review_to_response(r) for r in reviews],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(reviews) < total,
    }


@router.get("/stats")
async def get_review_stats(
    client_id: str,
    days: int = 30,
    db=Depends(get_prisma)
):
    """Get review statistics for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    start_date = datetime.utcnow() - timedelta(days=days)

    # Get all reviews
    all_reviews = await db.review.find_many(where={"clientId": client_id})

    # Get reviews in period
    period_reviews = await db.review.find_many(
        where={
            "clientId": client_id,
            "createdAt": {"gte": start_date}
        }
    )

    # Calculate stats
    total_reviews = len(all_reviews)
    period_reviews_count = len(period_reviews)

    # Average rating (all time)
    avg_rating = sum(r.rating for r in all_reviews) / total_reviews if total_reviews > 0 else 0

    # Rating distribution
    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in all_reviews:
        if 1 <= r.rating <= 5:
            rating_dist[r.rating] += 1

    # Platform breakdown
    platform_counts = {}
    for r in all_reviews:
        platform_counts[r.platform] = platform_counts.get(r.platform, 0) + 1

    # 5-star count (period)
    five_star_period = sum(1 for r in period_reviews if r.rating == 5)

    # Get pending review requests (jobs completed without reviews)
    jobs_needing_reviews = await db.job.count(
        where={
            "clientId": client_id,
            "status": "completed",
            "reviewRequested": False,
        }
    )

    return {
        "period_days": days,
        "total_reviews": total_reviews,
        "period_reviews": period_reviews_count,
        "average_rating": round(avg_rating, 2),
        "rating_distribution": rating_dist,
        "platform_breakdown": platform_counts,
        "five_star_period": five_star_period,
        "jobs_needing_reviews": jobs_needing_reviews,
        "google_place_id": client.googlePlaceId,
    }


@router.get("/{review_id}")
async def get_review(client_id: str, review_id: str, db=Depends(get_prisma)):
    """Get review by ID."""
    review = await db.review.find_unique(where={"id": review_id})

    if not review or review.clientId != client_id:
        raise HTTPException(status_code=404, detail="Review not found")

    return review_to_response(review)


@router.post("")
async def create_review(
    client_id: str,
    review: ReviewCreate,
    db=Depends(get_prisma)
):
    """Create a new review (typically from webhook or manual entry)."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")

    new_review = await db.review.create(
        data={
            "clientId": client_id,
            "jobId": review.job_id,
            "customerId": review.customer_id,
            "platform": review.platform,
            "rating": review.rating,
            "reviewText": review.review_text,
            "reviewerName": review.reviewer_name,
            "externalId": review.external_id,
            "externalUrl": review.external_url,
            "receivedAt": datetime.utcnow(),
        }
    )

    # Update job if linked
    if review.job_id:
        await db.job.update(
            where={"id": review.job_id},
            data={
                "reviewReceived": True,
                "reviewRating": review.rating,
            }
        )

    return {
        "id": new_review.id,
        "message": "Review created",
        **review_to_response(new_review)
    }


@router.post("/request")
async def request_review(
    client_id: str,
    request: ReviewRequestCreate,
    db=Depends(get_prisma)
):
    """Manually request a review for a job."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get job
    job = await db.job.find_unique(
        where={"id": request.job_id},
        include={"customer": True}
    )

    if not job or job.clientId != client_id:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Can only request reviews for completed jobs"
        )

    if not client.googlePlaceId:
        raise HTTPException(
            status_code=400,
            detail="Client has no Google Place ID configured"
        )

    # Create review record to track the request
    review = await db.review.create(
        data={
            "clientId": client_id,
            "jobId": job.id,
            "customerId": job.customerId,
            "platform": "google",
            "rating": 0,  # 0 indicates pending
            "requestSentAt": datetime.utcnow(),
            "reviewerName": job.customer.name if job.customer else None,
        }
    )

    # Update job
    await db.job.update(
        where={"id": job.id},
        data={
            "reviewRequested": True,
            "reviewRequestedAt": datetime.utcnow(),
        }
    )

    # TODO: Trigger review-request job via Trigger.dev
    print(f"Review request queued for job {job.id} to {request.customer_email}")

    review_link = f"https://search.google.com/local/writereview?placeid={client.googlePlaceId}"

    return {
        "id": review.id,
        "job_id": job.id,
        "message": "Review request queued",
        "email": request.customer_email,
        "review_link": review_link,
    }


@router.post("/{review_id}/respond")
async def respond_to_review(
    client_id: str,
    review_id: str,
    response_text: str,
    db=Depends(get_prisma)
):
    """Add a response to a review."""
    review = await db.review.find_unique(where={"id": review_id})

    if not review or review.clientId != client_id:
        raise HTTPException(status_code=404, detail="Review not found")

    updated = await db.review.update(
        where={"id": review_id},
        data={
            "responseText": response_text,
            "respondedAt": datetime.utcnow(),
        }
    )

    return {
        "id": review_id,
        "message": "Response added",
        "response_text": response_text,
        "responded_at": updated.respondedAt,
    }


@router.get("/pending-requests")
async def get_pending_review_requests(
    client_id: str,
    limit: int = 20,
    db=Depends(get_prisma)
):
    """Get jobs that should have review requests sent."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get completed jobs without review requests
    jobs = await db.job.find_many(
        where={
            "clientId": client_id,
            "status": "completed",
            "reviewRequested": False,
        },
        include={"customer": True},
        order={"completedAt": "desc"},
        take=limit,
    )

    return {
        "pending_count": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "completed_at": job.completedAt,
                "customer": {
                    "id": job.customer.id,
                    "name": job.customer.name,
                    "email": job.customer.email,
                } if job.customer else None,
            }
            for job in jobs
        ],
        "google_place_id": client.googlePlaceId,
    }

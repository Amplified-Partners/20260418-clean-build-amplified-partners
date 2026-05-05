---
title: "Module 10: Google Reviews Integration"
id: "10-google-reviews"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 10: Google Reviews Integration

## Overview
Automatically request reviews from happy customers, monitor review responses, and display reviews on client websites.

## Expert Panel Input

**Reputation Expert**: Reviews are the #1 trust signal for local businesses. Automate the ask at the right moment.

**Timing Expert**: Ask for reviews 24-48 hours after service completion. Not immediately (feels pushy), not later (they forget).

**Response Expert**: Respond to every review within 24 hours. Thank positives, address negatives professionally.

---

## Features

### 1. Review Request Automation
- Trigger after successful job completion
- SMS + email request with direct link
- Follow-up if no review after 3 days
- Smart timing based on job type

### 2. Review Monitoring
- Pull reviews from Google Places API
- Alert on new reviews
- Alert on negative reviews (priority)
- Track review velocity

### 3. Review Display
- Embed reviews on client websites
- Schema markup for rich snippets
- Filter/curate displayed reviews

---

## Files to Create

### 1. src/services/reviews/manager.py

```python
"""
Google Reviews Manager

Handles review requests, monitoring, and display.
"""

import os
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import httpx

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")


class ReviewRequestStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    CLICKED = "clicked"
    COMPLETED = "completed"
    EXPIRED = "expired"


@dataclass
class ReviewRequest:
    id: str
    client_id: str
    customer_name: str
    customer_phone: str
    customer_email: Optional[str]
    job_type: str
    job_completed_at: datetime
    status: ReviewRequestStatus
    sent_at: Optional[datetime]
    clicked_at: Optional[datetime]
    completed_at: Optional[datetime]
    review_id: Optional[str]


@dataclass
class GoogleReview:
    review_id: str
    author_name: str
    rating: int
    text: str
    time: datetime
    profile_photo_url: Optional[str]
    response: Optional[str]
    response_time: Optional[datetime]


class ReviewsManager:
    """
    Manages Google Reviews for clients.
    """
    
    def __init__(self):
        self.http = httpx.AsyncClient(timeout=30.0)
    
    async def create_review_request(
        self,
        client_id: str,
        customer_name: str,
        customer_phone: str,
        customer_email: Optional[str],
        job_type: str,
        job_completed_at: datetime,
        delay_hours: int = 24,
    ) -> ReviewRequest:
        """
        Create a review request to be sent after delay.
        """
        import uuid
        
        request = ReviewRequest(
            id=str(uuid.uuid4()),
            client_id=client_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            job_type=job_type,
            job_completed_at=job_completed_at,
            status=ReviewRequestStatus.PENDING,
            sent_at=None,
            clicked_at=None,
            completed_at=None,
            review_id=None,
        )
        
        # Store in database
        # TODO: Implement database storage
        
        return request
    
    async def send_review_request(
        self,
        request: ReviewRequest,
        google_place_id: str,
        business_name: str,
    ) -> bool:
        """
        Send SMS and email asking for a review.
        """
        review_link = f"https://search.google.com/local/writereview?placeid={google_place_id}"
        tracking_link = f"https://covered.ai/r/{request.id}"  # Redirects to review_link
        
        # Send SMS
        sms_sent = await self._send_sms(
            to=request.customer_phone,
            message=f"Hi {request.customer_name.split()[0]}, thanks for choosing {business_name}! "
                    f"If you were happy with our service, we'd really appreciate a quick review: {tracking_link}"
        )
        
        # Send email if available
        email_sent = False
        if request.customer_email:
            email_sent = await self._send_review_email(
                to=request.customer_email,
                customer_name=request.customer_name,
                business_name=business_name,
                review_link=tracking_link,
            )
        
        if sms_sent or email_sent:
            request.status = ReviewRequestStatus.SENT
            request.sent_at = datetime.utcnow()
            return True
        
        return False
    
    async def _send_sms(self, to: str, message: str) -> bool:
        """Send SMS via Twilio."""
        # TODO: Implement Twilio SMS
        print(f"SMS to {to}: {message}")
        return True
    
    async def _send_review_email(
        self,
        to: str,
        customer_name: str,
        business_name: str,
        review_link: str,
    ) -> bool:
        """Send review request email."""
        html = f"""
        <div style="font-family: sans-serif; max-width: 500px; margin: 0 auto;">
            <h2>Thanks for choosing {business_name}!</h2>
            <p>Hi {customer_name.split()[0]},</p>
            <p>We hope you were happy with our service. If you have a moment, 
            we'd really appreciate a quick review on Google.</p>
            <p style="text-align: center; margin: 30px 0;">
                <a href="{review_link}" 
                   style="background: #4285f4; color: white; padding: 15px 30px; 
                          text-decoration: none; border-radius: 8px; font-weight: bold;">
                    Leave a Review ⭐
                </a>
            </p>
            <p>It only takes 30 seconds and really helps us out.</p>
            <p>Thank you!</p>
        </div>
        """
        
        response = await self.http.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": f"{business_name} <reviews@covered.ai>",
                "to": to,
                "subject": f"How was your experience with {business_name}?",
                "html": html,
            }
        )
        
        return response.status_code == 200
    
    async def fetch_google_reviews(
        self,
        place_id: str,
        max_results: int = 50,
    ) -> List[GoogleReview]:
        """
        Fetch reviews from Google Places API.
        """
        response = await self.http.get(
            "https://maps.googleapis.com/maps/api/place/details/json",
            params={
                "place_id": place_id,
                "fields": "reviews",
                "key": GOOGLE_PLACES_API_KEY,
            }
        )
        
        data = response.json()
        reviews = []
        
        for r in data.get("result", {}).get("reviews", []):
            reviews.append(GoogleReview(
                review_id=str(hash(r.get("time", 0))),  # Google doesn't provide IDs
                author_name=r.get("author_name", "Anonymous"),
                rating=r.get("rating", 5),
                text=r.get("text", ""),
                time=datetime.fromtimestamp(r.get("time", 0)),
                profile_photo_url=r.get("profile_photo_url"),
                response=None,  # Owner responses not in basic API
                response_time=None,
            ))
        
        return reviews[:max_results]
    
    async def get_review_stats(self, place_id: str) -> Dict[str, Any]:
        """
        Get review statistics for a place.
        """
        response = await self.http.get(
            "https://maps.googleapis.com/maps/api/place/details/json",
            params={
                "place_id": place_id,
                "fields": "rating,user_ratings_total",
                "key": GOOGLE_PLACES_API_KEY,
            }
        )
        
        data = response.json().get("result", {})
        
        return {
            "average_rating": data.get("rating", 0),
            "total_reviews": data.get("user_ratings_total", 0),
        }
    
    def generate_review_schema(
        self,
        reviews: List[GoogleReview],
        business_name: str,
        place_id: str,
    ) -> Dict[str, Any]:
        """
        Generate Schema.org markup for reviews.
        """
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        
        return {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": business_name,
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": round(avg_rating, 1),
                "reviewCount": len(reviews),
                "bestRating": 5,
                "worstRating": 1,
            },
            "review": [
                {
                    "@type": "Review",
                    "author": {
                        "@type": "Person",
                        "name": r.author_name,
                    },
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": r.rating,
                    },
                    "reviewBody": r.text,
                    "datePublished": r.time.isoformat(),
                }
                for r in reviews[:10]  # Limit for schema
            ]
        }


# Singleton
reviews_manager = ReviewsManager()
```

### 2. src/api/routes/reviews.py

```python
"""
Reviews API Routes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from src.services.reviews.manager import reviews_manager, ReviewRequestStatus

router = APIRouter(prefix="/reviews", tags=["reviews"])


class CreateReviewRequestInput(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    job_type: str
    delay_hours: int = 24


class ReviewRequestResponse(BaseModel):
    id: str
    status: str
    sent_at: Optional[str] = None


@router.post("/request/{client_id}")
async def create_review_request(
    client_id: str,
    input: CreateReviewRequestInput,
    background_tasks: BackgroundTasks,
):
    """Create a review request for a customer."""
    request = await reviews_manager.create_review_request(
        client_id=client_id,
        customer_name=input.customer_name,
        customer_phone=input.customer_phone,
        customer_email=input.customer_email,
        job_type=input.job_type,
        job_completed_at=datetime.utcnow(),
        delay_hours=input.delay_hours,
    )
    
    return {
        "id": request.id,
        "status": request.status.value,
        "scheduled_for": (datetime.utcnow()).isoformat(),
    }


@router.get("/fetch/{place_id}")
async def fetch_reviews(place_id: str, limit: int = 20):
    """Fetch reviews from Google."""
    reviews = await reviews_manager.fetch_google_reviews(place_id, limit)
    
    return {
        "reviews": [
            {
                "author": r.author_name,
                "rating": r.rating,
                "text": r.text,
                "time": r.time.isoformat(),
                "photo": r.profile_photo_url,
            }
            for r in reviews
        ],
        "count": len(reviews),
    }


@router.get("/stats/{place_id}")
async def get_review_stats(place_id: str):
    """Get review statistics."""
    return await reviews_manager.get_review_stats(place_id)


@router.get("/schema/{place_id}")
async def get_review_schema(place_id: str, business_name: str):
    """Get Schema.org markup for reviews."""
    reviews = await reviews_manager.fetch_google_reviews(place_id, 10)
    schema = reviews_manager.generate_review_schema(reviews, business_name, place_id)
    return schema


@router.get("/track/{request_id}")
async def track_review_click(request_id: str):
    """Track when someone clicks a review link."""
    # TODO: Update request status and redirect
    return {"redirect": "https://google.com/maps"}


@router.post("/process-pending")
async def process_pending_requests():
    """Process pending review requests (scheduled job)."""
    # TODO: Implement batch processing
    return {"processed": 0}
```

---

## Scheduled Jobs

### Trigger.dev job for review requests

```typescript
// src/trigger/review-requests.ts
import { schedules } from "@trigger.dev/sdk/v3";

export const processReviewRequests = schedules.task({
  id: "process-review-requests",
  cron: "0 10 * * *", // Daily at 10am
  run: async () => {
    const response = await fetch(
      `${process.env.API_URL}/api/v1/reviews/process-pending`,
      { method: "POST" }
    );
    return response.json();
  },
});
```

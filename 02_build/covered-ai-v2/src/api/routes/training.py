"""
Training Routes - Video tracking, events, help, and support chat
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone
from prisma import Json

from src.db.client import get_prisma

router = APIRouter()


# =============================================================================
# VIDEO TRACKING
# =============================================================================

class VideoWatchRequest(BaseModel):
    clientId: str
    videoId: str
    trigger: Optional[str] = None
    location: Optional[str] = None


class VideoProgressUpdateRequest(BaseModel):
    watchedSeconds: int
    completed: Optional[bool] = False


# Video content definitions (matches frontend)
VIDEO_CONTENT = {
    "welcome": {"duration": 60, "type": "ONBOARDING"},
    "quick_tour": {"duration": 90, "type": "ONBOARDING"},
    "phone_setup": {"duration": 45, "type": "ONBOARDING"},
    "meet_gemma": {"duration": 60, "type": "ONBOARDING"},
    "calls_dashboard": {"duration": 90, "type": "FEATURE_TRAINING"},
    "creating_invoices": {"duration": 120, "type": "FEATURE_TRAINING"},
    "invoice_chasing": {"duration": 90, "type": "FEATURE_TRAINING"},
    "review_requests": {"duration": 60, "type": "FEATURE_TRAINING"},
    "attention_items": {"duration": 75, "type": "FEATURE_TRAINING"},
    "first_call_success": {"duration": 30, "type": "CELEBRATION"},
    "first_invoice_paid": {"duration": 30, "type": "CELEBRATION"},
    "week_1_complete": {"duration": 45, "type": "CELEBRATION"},
    "forwarding_not_working": {"duration": 90, "type": "TROUBLESHOOTING"},
}


@router.post("/videos/watch")
async def start_video_watch(
    request: VideoWatchRequest,
    db=Depends(get_prisma)
):
    """Start tracking a video watch session."""
    video_info = VIDEO_CONTENT.get(request.videoId)
    if not video_info:
        raise HTTPException(status_code=404, detail="Video not found")

    watch = await db.videowatch.create(
        data={
            "clientId": request.clientId,
            "videoId": request.videoId,
            "videoType": video_info["type"],
            "totalSeconds": video_info["duration"],
            "trigger": request.trigger,
            "location": request.location
        }
    )

    return {"watchId": watch.id}


@router.patch("/videos/watch/{watch_id}")
async def update_video_progress(
    watch_id: str,
    update: VideoProgressUpdateRequest,
    db=Depends(get_prisma)
):
    """Update video watch progress."""
    watch = await db.videowatch.find_unique(where={"id": watch_id})

    if not watch:
        raise HTTPException(status_code=404, detail="Watch session not found")

    percent_watched = (update.watchedSeconds / watch.totalSeconds) * 100

    updated = await db.videowatch.update(
        where={"id": watch_id},
        data={
            "watchedSeconds": update.watchedSeconds,
            "percentWatched": percent_watched,
            "completedAt": datetime.now(timezone.utc) if update.completed or percent_watched >= 90 else None
        }
    )

    return {
        "id": updated.id,
        "watchedSeconds": updated.watchedSeconds,
        "percentWatched": updated.percentWatched,
        "completed": updated.completedAt is not None
    }


@router.get("/videos/history/{client_id}")
async def get_video_history(
    client_id: str,
    db=Depends(get_prisma)
):
    """Get client's video watch history."""
    watches = await db.videowatch.find_many(
        where={"clientId": client_id},
        order={"startedAt": "desc"},
        take=50
    )

    return {
        "watches": [
            {
                "id": w.id,
                "videoId": w.videoId,
                "videoType": w.videoType,
                "startedAt": w.startedAt,
                "completedAt": w.completedAt,
                "percentWatched": w.percentWatched
            }
            for w in watches
        ]
    }


# =============================================================================
# BEHAVIORAL EVENTS
# =============================================================================

class BehavioralEventRequest(BaseModel):
    clientId: str
    eventType: str
    eventData: Optional[dict] = None
    sessionId: Optional[str] = None
    deviceType: Optional[str] = None


@router.post("/events")
async def log_event(
    request: BehavioralEventRequest,
    db=Depends(get_prisma)
):
    """Log a behavioral event."""
    event = await db.behavioralevent.create(
        data={
            "client": {"connect": {"id": request.clientId}},
            "eventType": request.eventType,
            "eventData": Json(request.eventData or {}),
            "sessionId": request.sessionId,
            "deviceType": request.deviceType
        }
    )

    # Check for trigger conditions that update onboarding progress
    await check_trigger_conditions(db, request.clientId, request.eventType, request.eventData)

    return {"eventId": event.id}


async def check_trigger_conditions(db, client_id: str, event_type: str, event_data: dict):
    """Update onboarding progress based on events. Single query, batched updates."""

    # Only fetch if this is a triggering event type
    triggering_events = {"invoice_sent", "call_received", "review_request_sent"}
    if event_type not in triggering_events:
        return

    # Single fetch for all conditions
    progress = await db.onboardingprogress.find_unique(where={"clientId": client_id})
    if not progress:
        return

    # Build update data based on event type
    update_data = {}
    now = datetime.now(timezone.utc)

    if event_type == "invoice_sent" and not progress.firstInvoiceSent:
        update_data["firstInvoiceSent"] = True
        update_data["firstInvoiceSentAt"] = now

    elif event_type == "call_received" and event_data and event_data.get("isReal") and not progress.firstRealCall:
        update_data["firstRealCall"] = True
        update_data["firstRealCallAt"] = now
        update_data["currentStage"] = "ACTIVATION"

    elif event_type == "review_request_sent" and not progress.firstReviewRequest:
        update_data["firstReviewRequest"] = True
        update_data["firstReviewRequestAt"] = now

    # Single update if there are changes
    if update_data:
        await db.onboardingprogress.update(
            where={"clientId": client_id},
            data=update_data
        )


# =============================================================================
# HELP SEARCH
# =============================================================================

# Help articles (simple in-memory for now)
HELP_ARTICLES = [
    {
        "id": "how-covered-works",
        "title": "How Covered Works",
        "snippet": "An overview of how Gemma answers your calls and manages enquiries.",
        "category": "getting-started",
        "type": "article",
        "videoId": "welcome",
        "keywords": ["how", "works", "gemma", "calls", "overview", "introduction"]
    },
    {
        "id": "phone-setup",
        "title": "Setting Up Your Phone",
        "snippet": "How to configure call forwarding and your Covered number.",
        "category": "getting-started",
        "type": "article",
        "videoId": "phone_setup",
        "keywords": ["phone", "setup", "forwarding", "number", "configure", "mobile"]
    },
    {
        "id": "understanding-calls",
        "title": "Understanding Your Calls Dashboard",
        "snippet": "How to view, filter, and act on calls in your dashboard.",
        "category": "calls",
        "type": "article",
        "videoId": "calls_dashboard",
        "keywords": ["calls", "dashboard", "filter", "transcript", "recording", "action"]
    },
    {
        "id": "calls-not-coming-through",
        "title": "Calls Not Coming Through",
        "snippet": "Troubleshooting when calls aren't reaching your phone.",
        "category": "troubleshooting",
        "type": "article",
        "videoId": "forwarding_not_working",
        "keywords": ["calls", "not", "coming", "through", "forwarding", "troubleshoot", "problem", "issue"]
    },
    {
        "id": "creating-invoices",
        "title": "Creating Invoices",
        "snippet": "Step-by-step guide to creating and sending invoices.",
        "category": "invoices",
        "type": "article",
        "videoId": "creating_invoices",
        "keywords": ["invoice", "create", "send", "bill", "payment", "customer"]
    },
    {
        "id": "invoice-reminders",
        "title": "Automatic Invoice Reminders",
        "snippet": "How the invoice chasing system works.",
        "category": "invoices",
        "type": "article",
        "videoId": "invoice_chasing",
        "keywords": ["invoice", "reminder", "chasing", "automatic", "overdue", "payment"]
    },
    {
        "id": "review-requests",
        "title": "Getting More Reviews",
        "snippet": "How automatic review requests work.",
        "category": "reviews",
        "type": "article",
        "videoId": "review_requests",
        "keywords": ["review", "google", "rating", "star", "feedback", "reputation"]
    },
]


def search_articles(query: str) -> list:
    """Simple keyword-based search."""
    query_lower = query.lower()
    query_words = query_lower.split()

    results = []
    for article in HELP_ARTICLES:
        score = 0

        # Title match (highest weight)
        if query_lower in article["title"].lower():
            score += 10

        # Keyword match
        for keyword in article.get("keywords", []):
            for word in query_words:
                if keyword in word or word in keyword:
                    score += 5

        # Snippet match
        if query_lower in article["snippet"].lower():
            score += 3

        if score > 0:
            results.append({**article, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:10]


@router.get("/help/search")
async def search_help(q: str):
    """Search help articles."""
    if not q or len(q) < 2:
        return {"results": []}

    results = search_articles(q)

    return {
        "query": q,
        "results": [
            {
                "id": r["id"],
                "title": r["title"],
                "snippet": r["snippet"],
                "type": r["type"],
                "category": r["category"],
                "videoId": r.get("videoId")
            }
            for r in results
        ]
    }


@router.get("/help/articles")
async def list_help_articles(category: Optional[str] = None):
    """List all help articles, optionally filtered by category."""
    articles = HELP_ARTICLES

    if category:
        articles = [a for a in articles if a["category"] == category]

    return {
        "articles": articles,
        "total": len(articles)
    }


@router.get("/help/articles/{article_id}")
async def get_help_article(article_id: str):
    """Get a specific help article."""
    for article in HELP_ARTICLES:
        if article["id"] == article_id:
            return article

    raise HTTPException(status_code=404, detail="Article not found")


# =============================================================================
# SUPPORT CHAT
# =============================================================================

class ChatMessageRequest(BaseModel):
    clientId: str
    message: str
    chatId: Optional[str] = None


@router.post("/support/chat")
async def send_chat_message(
    request: ChatMessageRequest,
    db=Depends(get_prisma)
):
    """Send a message in support chat."""
    # Get or create chat session
    chat = None
    if request.chatId:
        chat = await db.supportchat.find_unique(where={"id": request.chatId})

    if not chat:
        chat = await db.supportchat.create(
            data={
                "client": {"connect": {"id": request.clientId}},
                "messages": Json([]),
                "status": "ACTIVE"
            }
        )

    # Get existing messages
    messages = chat.messages if isinstance(chat.messages, list) else []

    # Add user message
    messages.append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    # Generate AI response (simple rule-based for now, can integrate Claude later)
    ai_response = generate_support_response(request.message)

    # Add AI response to messages
    messages.append({
        "role": "assistant",
        "content": ai_response["content"],
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    # Determine if needs escalation
    needs_escalation = ai_response.get("needs_escalation", False)

    # Update chat
    await db.supportchat.update(
        where={"id": chat.id},
        data={
            "messages": Json(messages),
            "status": "WAITING_HUMAN" if needs_escalation else "ACTIVE",
            "escalatedAt": datetime.now(timezone.utc) if needs_escalation else None
        }
    )

    return {
        "chatId": chat.id,
        "response": {
            "role": "assistant",
            "content": ai_response["content"],
            "actions": ai_response.get("actions", [])
        },
        "needsEscalation": needs_escalation
    }


def generate_support_response(message: str) -> dict:
    """Generate a simple rule-based support response."""
    message_lower = message.lower()

    # Forwarding issues
    if any(word in message_lower for word in ["forwarding", "calls not coming", "not working", "can't receive"]):
        return {
            "content": """I can help with call forwarding issues! Here are some things to check:

1. **Settings** - Go to Settings > Phone and verify your forwarding number is correct (including country code +44)

2. **Your phone** - Make sure Do Not Disturb is off and you're not blocking unknown numbers

3. **Test it** - Try calling your Covered number from a different phone

If you're still having trouble, let me know and I can escalate this to our support team.""",
            "actions": [
                {"type": "link", "label": "Go to Settings", "url": "/settings"}
            ]
        }

    # Invoice questions
    if any(word in message_lower for word in ["invoice", "payment", "paid", "overdue"]):
        return {
            "content": """I can help with invoices! Here are some common questions:

- **Create an invoice** - Go to Invoices > New Invoice, or create one directly from a call record
- **Chase an overdue invoice** - Reminders are sent automatically, but you can send one manually from the invoice page
- **Mark as paid** - Open the invoice and click "Mark as Paid"

Need help with something specific?""",
            "actions": [
                {"type": "link", "label": "Go to Invoices", "url": "/invoices"}
            ]
        }

    # Review questions
    if any(word in message_lower for word in ["review", "google", "rating"]):
        return {
            "content": """I can help with reviews!

Review requests are sent automatically when you mark a job as complete. Make sure your Google Business Profile is connected in Settings > Reviews.

To manually send a review request, go to the completed job and click "Request Review".""",
            "actions": [
                {"type": "link", "label": "Go to Reviews", "url": "/reviews"}
            ]
        }

    # Dashboard/general
    if any(word in message_lower for word in ["dashboard", "how", "start", "begin"]):
        return {
            "content": """Welcome to Covered! Here's a quick overview:

- **Calls** - Every call Gemma handles appears here with transcripts and recordings
- **Invoices** - Create and send invoices, track payments
- **Customers** - Your customer database
- **Reviews** - Manage your Google reviews

What would you like to know more about?"""
        }

    # Default response
    return {
        "content": """Thanks for your message! I'm here to help with:

- Call and phone setup issues
- Invoices and payments
- Reviews and reputation
- Dashboard and features

Could you tell me more about what you need help with? If this is urgent, I can connect you with our support team.""",
        "needs_escalation": "urgent" in message_lower or "help" in message_lower and "please" in message_lower
    }


@router.get("/support/chat/{chat_id}")
async def get_chat_history(
    chat_id: str,
    db=Depends(get_prisma)
):
    """Get chat history."""
    chat = await db.supportchat.find_unique(where={"id": chat_id})

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return {
        "chatId": chat.id,
        "messages": chat.messages,
        "status": chat.status,
        "createdAt": chat.createdAt
    }


@router.post("/support/chat/{chat_id}/resolve")
async def resolve_chat(
    chat_id: str,
    resolution: Optional[str] = None,
    db=Depends(get_prisma)
):
    """Mark a chat as resolved."""
    await db.supportchat.update(
        where={"id": chat_id},
        data={
            "status": "RESOLVED",
            "resolvedAt": datetime.now(timezone.utc),
            "resolution": resolution,
            "wasResolved": True
        }
    )

    return {"message": "Chat resolved"}

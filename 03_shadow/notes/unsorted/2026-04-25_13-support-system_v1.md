---
title: "Module 13: Support & Help System"
id: "13-support-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Module 13: Support & Help System

## Overview
Customer support ticketing, help documentation, and self-service troubleshooting for clients.

## Expert Panel Input

**Support Expert**: 80% of support queries are the same 10 questions. Answer them before they're asked.

**Self-Service Expert**: Make forwarding setup foolproof. One wrong digit = no calls = unhappy customer.

**Documentation Expert**: Visual guides, not walls of text. Show, don't tell.

---

## Features

### 1. Help Center
- Searchable knowledge base
- Visual setup guides
- Video tutorials
- FAQ by topic

### 2. Support Tickets
- Create/track tickets
- Priority levels
- Auto-responses for common issues
- Escalation rules

### 3. Self-Service Tools
- Forwarding code generator
- Test your line tool
- Connection checker
- Status page

---

## Files to Create

### 1. src/services/support/help_center.py

```python
"""
Help Center - Knowledge base and support tools
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ArticleCategory(str, Enum):
    SETUP = "setup"
    CALLS = "calls"
    BILLING = "billing"
    FEATURES = "features"
    TROUBLESHOOTING = "troubleshooting"


@dataclass
class HelpArticle:
    id: str
    title: str
    slug: str
    category: ArticleCategory
    content: str  # Markdown
    video_url: Optional[str]
    views: int = 0
    helpful_yes: int = 0
    helpful_no: int = 0


# Pre-written help articles
HELP_ARTICLES = [
    HelpArticle(
        id="setup-forwarding",
        title="How to forward your calls to Covered",
        slug="forward-calls",
        category=ArticleCategory.SETUP,
        content="""
# How to Forward Your Calls to Covered

Setting up call forwarding takes about 30 seconds. Here's how:

## Step 1: Find your Covered number

Your dedicated Covered number is shown on your dashboard. It looks like: **+44 XXXX XXXXXX**

## Step 2: Enable forwarding on your phone

### From an iPhone:
1. Open **Settings**
2. Tap **Phone**
3. Tap **Call Forwarding**
4. Toggle it **ON**
5. Enter your Covered number

### From an Android:
1. Open **Phone** app
2. Tap **⋮** (menu)
3. Tap **Settings** → **Calls** → **Call Forwarding**
4. Enter your Covered number

### From a landline:
Dial this code from your landline:
```
*21*[your-covered-number]#
```

To disable forwarding later:
```
#21#
```

## Step 3: Test it!

Call your normal number from another phone. Gemma should answer!

## Troubleshooting

**Calls aren't forwarding?**
- Check you entered the full number including country code (+44)
- Make sure call forwarding is enabled (not just "forward when busy")
- Some networks need 24 hours to activate

**Need help?** Contact us and we'll walk you through it.
""",
        video_url="https://youtube.com/watch?v=xxxxx",
    ),
    HelpArticle(
        id="test-line",
        title="How to test your Covered line",
        slug="test-line",
        category=ArticleCategory.SETUP,
        content="""
# Testing Your Covered Line

Want to hear how Gemma answers your calls? Here's how to test:

## Option 1: Call your Covered number directly

1. Use a different phone (or a friend's phone)
2. Call your Covered number directly
3. Gemma will answer as your business

## Option 2: Call your forwarded number

If you've set up forwarding:
1. Call your main business number
2. The call should forward to Covered
3. Gemma answers

## What to listen for

✅ Gemma greets with your business name
✅ She sounds natural and friendly
✅ She asks appropriate questions
✅ You receive a notification after the call

## Common issues

**Gemma says the wrong business name?**
→ Update your business name in Settings

**No answer at all?**
→ Check your forwarding is set up correctly

**Gemma sounds robotic?**
→ Check your internet connection (she streams over the web)
""",
        video_url=None,
    ),
    HelpArticle(
        id="emergency-keywords",
        title="Setting up emergency call handling",
        slug="emergency-keywords",
        category=ArticleCategory.FEATURES,
        content="""
# Emergency Call Handling

Gemma can detect urgent calls and forward them to you immediately.

## How it works

1. You define "emergency keywords" (e.g., flood, burst, gas leak)
2. When a caller mentions these words, Gemma flags it as urgent
3. The call can be forwarded to your mobile immediately
4. You get a priority notification

## Setting up keywords

1. Go to **Dashboard** → **Settings**
2. Find **Emergency Keywords**
3. Enter words separated by commas
4. Click **Save**

## Recommended keywords by trade

**Plumbers:** flood, burst, leak, no water, gas, emergency
**Electricians:** no power, sparking, burning smell, emergency
**HVAC:** no heating, frozen, gas smell
**General:** urgent, emergency, asap

## Forwarding options

You can choose what happens with urgent calls:
- **Forward immediately** - Call goes straight to your mobile
- **Priority notification** - Get an urgent SMS/email
- **Both** - Forward AND notify

## Tips

- Don't add too many keywords (false positives)
- Test with a friend to make sure it works
- Keep your forwarding number up to date
""",
        video_url=None,
    ),
    HelpArticle(
        id="view-calls",
        title="Viewing your call history",
        slug="view-calls",
        category=ArticleCategory.CALLS,
        content="""
# Viewing Your Call History

See every call Gemma has handled for you.

## Accessing call history

1. Log in to your **Dashboard**
2. Click **Calls** in the sidebar
3. See all calls, newest first

## What you can see

For each call:
- **Caller number** and name (if captured)
- **Date and time**
- **Duration**
- **Outcome** (lead, enquiry, spam, etc.)
- **Summary** - What the call was about
- **Recording** - Listen to the full call
- **Transcript** - Read what was said

## Filtering calls

Use the filters to find specific calls:
- **All calls** - Everything
- **Leads** - Calls where someone wanted a callback
- **Missed** - Calls that weren't answered (rare)
- **By date** - Specific time periods

## Exporting data

Click **Export** to download your call data as CSV.
""",
        video_url=None,
    ),
    HelpArticle(
        id="billing",
        title="Understanding your bill",
        slug="billing",
        category=ArticleCategory.BILLING,
        content="""
# Understanding Your Bill

Simple pricing, no surprises.

## Your subscription

**Covered Pro: £297/month + VAT**

This includes:
- Unlimited calls
- 24/7 availability
- Call recordings
- Lead capture
- Dashboard access
- Email/SMS notifications

## Billing cycle

- Billed monthly on your signup date
- Payment by card (Visa, Mastercard, Amex)
- VAT added for UK businesses

## Invoices

View and download invoices:
1. Go to **Dashboard** → **Settings** → **Billing**
2. Click **View Invoices**
3. Download any invoice as PDF

## Updating payment

1. Go to **Settings** → **Billing**
2. Click **Update Payment Method**
3. Enter new card details

## Cancellation

You can cancel anytime:
1. Go to **Settings** → **Billing**
2. Click **Cancel Subscription**
3. Service continues until end of billing period

No cancellation fees. No contracts.
""",
        video_url=None,
    ),
]


class HelpCenter:
    """
    Knowledge base and help system.
    """
    
    def __init__(self):
        self.articles = {a.id: a for a in HELP_ARTICLES}
    
    def get_article(self, id_or_slug: str) -> Optional[HelpArticle]:
        """Get article by ID or slug."""
        # Try ID first
        if id_or_slug in self.articles:
            return self.articles[id_or_slug]
        
        # Try slug
        for article in self.articles.values():
            if article.slug == id_or_slug:
                return article
        
        return None
    
    def search(self, query: str) -> List[HelpArticle]:
        """Search articles by title and content."""
        query_lower = query.lower()
        results = []
        
        for article in self.articles.values():
            if (query_lower in article.title.lower() or
                query_lower in article.content.lower()):
                results.append(article)
        
        return results
    
    def list_by_category(self, category: ArticleCategory) -> List[HelpArticle]:
        """List articles in a category."""
        return [
            a for a in self.articles.values()
            if a.category == category
        ]
    
    def get_popular(self, limit: int = 5) -> List[HelpArticle]:
        """Get most viewed articles."""
        sorted_articles = sorted(
            self.articles.values(),
            key=lambda a: a.views,
            reverse=True
        )
        return sorted_articles[:limit]
    
    def record_view(self, article_id: str):
        """Record an article view."""
        if article_id in self.articles:
            self.articles[article_id].views += 1
    
    def record_feedback(self, article_id: str, helpful: bool):
        """Record article feedback."""
        if article_id in self.articles:
            if helpful:
                self.articles[article_id].helpful_yes += 1
            else:
                self.articles[article_id].helpful_no += 1


# Forwarding code generator
FORWARDING_CODES = {
    "ee": {"enable": "*21*{number}#", "disable": "#21#"},
    "vodafone": {"enable": "*21*{number}#", "disable": "#21#"},
    "o2": {"enable": "*21*{number}#", "disable": "#21#"},
    "three": {"enable": "*21*{number}#", "disable": "#21#"},
    "bt": {"enable": "*21*{number}#", "disable": "#21#"},
    "sky": {"enable": "*21*{number}#", "disable": "#21#"},
    "virgin": {"enable": "*21*{number}#", "disable": "#21#"},
    "default": {"enable": "*21*{number}#", "disable": "#21#"},
}


def generate_forwarding_code(
    covered_number: str,
    network: str = "default",
) -> Dict[str, str]:
    """Generate forwarding codes for a network."""
    codes = FORWARDING_CODES.get(network.lower(), FORWARDING_CODES["default"])
    
    # Format number (remove spaces, ensure +44)
    clean_number = covered_number.replace(" ", "").replace("-", "")
    if clean_number.startswith("0"):
        clean_number = "+44" + clean_number[1:]
    
    return {
        "enable": codes["enable"].format(number=clean_number),
        "disable": codes["disable"],
        "number": clean_number,
        "network": network,
    }


# Singleton
help_center = HelpCenter()
```

### 2. src/services/support/tickets.py

```python
"""
Support Ticket System
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketCategory(str, Enum):
    SETUP = "setup"
    CALLS = "calls"
    BILLING = "billing"
    TECHNICAL = "technical"
    FEATURE_REQUEST = "feature_request"
    OTHER = "other"


@dataclass
class TicketMessage:
    id: str
    author: str  # "client" or "support"
    author_name: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SupportTicket:
    id: str
    client_id: str
    client_name: str
    client_email: str
    subject: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    messages: List[TicketMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    assigned_to: Optional[str] = None


# Auto-responses for common issues
AUTO_RESPONSES = {
    "forwarding": """
Hi! It sounds like you're having trouble with call forwarding.

Here are the most common fixes:
1. Make sure you entered the full number including +44
2. Check that forwarding is set to "all calls" not just "when busy"
3. Some networks take up to 24 hours to activate

If you're still stuck, reply to this message and we'll help!
""",
    "no_calls": """
Hi! If you're not seeing calls come through:

1. First, test your line by calling your Covered number directly
2. Check your forwarding is set up correctly (dial *#21# to check status)
3. Make sure Gemma status shows "Active" on your dashboard

If the test call works but regular calls don't, the issue is likely with forwarding setup.
""",
    "billing": """
Hi! For billing questions:

- View invoices: Dashboard → Settings → Billing
- Update payment: Dashboard → Settings → Billing → Update Payment
- Cancel: Dashboard → Settings → Billing → Cancel Subscription

No cancellation fees, and your service continues until the end of your billing period.
""",
}


class TicketSystem:
    """
    Support ticket management.
    """
    
    def __init__(self):
        self.tickets: Dict[str, SupportTicket] = {}
    
    async def create_ticket(
        self,
        client_id: str,
        client_name: str,
        client_email: str,
        subject: str,
        message: str,
        category: TicketCategory = TicketCategory.OTHER,
    ) -> SupportTicket:
        """Create a new support ticket."""
        # Determine priority based on keywords
        priority = self._detect_priority(subject, message)
        
        ticket = SupportTicket(
            id=f"TICKET-{uuid.uuid4().hex[:8].upper()}",
            client_id=client_id,
            client_name=client_name,
            client_email=client_email,
            subject=subject,
            category=category,
            priority=priority,
            status=TicketStatus.OPEN,
            messages=[
                TicketMessage(
                    id=str(uuid.uuid4()),
                    author="client",
                    author_name=client_name,
                    content=message,
                )
            ],
        )
        
        self.tickets[ticket.id] = ticket
        
        # Check for auto-response
        auto_response = self._get_auto_response(subject, message)
        if auto_response:
            ticket.messages.append(TicketMessage(
                id=str(uuid.uuid4()),
                author="support",
                author_name="Covered Support",
                content=auto_response,
            ))
            ticket.status = TicketStatus.WAITING_CUSTOMER
        
        return ticket
    
    def _detect_priority(self, subject: str, message: str) -> TicketPriority:
        """Detect priority from content."""
        text = f"{subject} {message}".lower()
        
        if any(word in text for word in ["urgent", "emergency", "down", "broken", "not working"]):
            return TicketPriority.URGENT
        elif any(word in text for word in ["asap", "important", "billing", "payment"]):
            return TicketPriority.HIGH
        elif any(word in text for word in ["question", "how do i", "help"]):
            return TicketPriority.MEDIUM
        else:
            return TicketPriority.LOW
    
    def _get_auto_response(self, subject: str, message: str) -> Optional[str]:
        """Get auto-response if applicable."""
        text = f"{subject} {message}".lower()
        
        if any(word in text for word in ["forward", "forwarding", "divert"]):
            return AUTO_RESPONSES["forwarding"]
        elif any(word in text for word in ["no calls", "not receiving", "calls not"]):
            return AUTO_RESPONSES["no_calls"]
        elif any(word in text for word in ["bill", "invoice", "payment", "cancel"]):
            return AUTO_RESPONSES["billing"]
        
        return None
    
    async def add_message(
        self,
        ticket_id: str,
        author: str,
        author_name: str,
        content: str,
    ) -> Optional[TicketMessage]:
        """Add a message to a ticket."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None
        
        message = TicketMessage(
            id=str(uuid.uuid4()),
            author=author,
            author_name=author_name,
            content=content,
        )
        
        ticket.messages.append(message)
        ticket.updated_at = datetime.utcnow()
        
        # Update status
        if author == "support":
            ticket.status = TicketStatus.WAITING_CUSTOMER
        elif author == "client":
            if ticket.status == TicketStatus.WAITING_CUSTOMER:
                ticket.status = TicketStatus.OPEN
        
        return message
    
    async def resolve_ticket(self, ticket_id: str) -> bool:
        """Mark ticket as resolved."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return False
        
        ticket.status = TicketStatus.RESOLVED
        ticket.resolved_at = datetime.utcnow()
        ticket.updated_at = datetime.utcnow()
        return True
    
    async def get_client_tickets(self, client_id: str) -> List[SupportTicket]:
        """Get all tickets for a client."""
        return [
            t for t in self.tickets.values()
            if t.client_id == client_id
        ]
    
    async def get_open_tickets(self) -> List[SupportTicket]:
        """Get all open tickets (for admin)."""
        return [
            t for t in self.tickets.values()
            if t.status not in [TicketStatus.RESOLVED, TicketStatus.CLOSED]
        ]


# Singleton
ticket_system = TicketSystem()
```

### 3. src/api/routes/support.py

```python
"""
Support API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from src.services.support.help_center import (
    help_center,
    generate_forwarding_code,
    ArticleCategory,
)
from src.services.support.tickets import (
    ticket_system,
    TicketCategory,
)

router = APIRouter(prefix="/support", tags=["support"])


# Help Center routes

@router.get("/articles")
async def list_articles(category: Optional[str] = None):
    """List help articles."""
    if category:
        try:
            cat = ArticleCategory(category)
            articles = help_center.list_by_category(cat)
        except ValueError:
            articles = []
    else:
        articles = list(help_center.articles.values())
    
    return {
        "articles": [
            {
                "id": a.id,
                "title": a.title,
                "slug": a.slug,
                "category": a.category.value,
                "has_video": bool(a.video_url),
            }
            for a in articles
        ]
    }


@router.get("/articles/{id_or_slug}")
async def get_article(id_or_slug: str):
    """Get a specific article."""
    article = help_center.get_article(id_or_slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    help_center.record_view(article.id)
    
    return {
        "id": article.id,
        "title": article.title,
        "category": article.category.value,
        "content": article.content,
        "video_url": article.video_url,
    }


@router.get("/articles/search")
async def search_articles(q: str):
    """Search help articles."""
    results = help_center.search(q)
    return {
        "query": q,
        "results": [
            {
                "id": a.id,
                "title": a.title,
                "slug": a.slug,
            }
            for a in results
        ]
    }


@router.post("/articles/{article_id}/feedback")
async def article_feedback(article_id: str, helpful: bool):
    """Record article feedback."""
    help_center.record_feedback(article_id, helpful)
    return {"recorded": True}


# Forwarding code generator

@router.get("/forwarding-code")
async def get_forwarding_code(
    covered_number: str,
    network: str = "default",
):
    """Generate forwarding codes."""
    return generate_forwarding_code(covered_number, network)


# Ticket routes

class CreateTicketInput(BaseModel):
    subject: str
    message: str
    category: str = "other"


class AddMessageInput(BaseModel):
    content: str


@router.post("/tickets")
async def create_ticket(
    input: CreateTicketInput,
    client_id: str = "test-client",  # TODO: Get from auth
    client_name: str = "Test User",
    client_email: str = "test@example.com",
):
    """Create a support ticket."""
    try:
        category = TicketCategory(input.category)
    except ValueError:
        category = TicketCategory.OTHER
    
    ticket = await ticket_system.create_ticket(
        client_id=client_id,
        client_name=client_name,
        client_email=client_email,
        subject=input.subject,
        message=input.message,
        category=category,
    )
    
    return {
        "id": ticket.id,
        "status": ticket.status.value,
        "has_auto_response": len(ticket.messages) > 1,
    }


@router.get("/tickets")
async def list_tickets(client_id: str = "test-client"):
    """List tickets for a client."""
    tickets = await ticket_system.get_client_tickets(client_id)
    
    return {
        "tickets": [
            {
                "id": t.id,
                "subject": t.subject,
                "status": t.status.value,
                "priority": t.priority.value,
                "created_at": t.created_at.isoformat(),
                "message_count": len(t.messages),
            }
            for t in sorted(tickets, key=lambda x: x.updated_at, reverse=True)
        ]
    }


@router.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Get ticket details."""
    ticket = ticket_system.tickets.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {
        "id": ticket.id,
        "subject": ticket.subject,
        "status": ticket.status.value,
        "priority": ticket.priority.value,
        "category": ticket.category.value,
        "created_at": ticket.created_at.isoformat(),
        "messages": [
            {
                "author": m.author,
                "author_name": m.author_name,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in ticket.messages
        ]
    }


@router.post("/tickets/{ticket_id}/messages")
async def add_ticket_message(
    ticket_id: str,
    input: AddMessageInput,
    client_name: str = "Test User",
):
    """Add a message to a ticket."""
    message = await ticket_system.add_message(
        ticket_id=ticket_id,
        author="client",
        author_name=client_name,
        content=input.content,
    )
    
    if not message:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {"message_id": message.id}


@router.post("/tickets/{ticket_id}/resolve")
async def resolve_ticket(ticket_id: str):
    """Mark ticket as resolved."""
    success = await ticket_system.resolve_ticket(ticket_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {"status": "resolved"}
```

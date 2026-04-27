"""
Common Database Queries

Reusable query functions for leads, clients, jobs, etc.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from prisma import Prisma
from prisma.models import Lead, Client, Customer, Job, NurtureSequence, Notification


async def get_client_by_id(db: Prisma, client_id: str) -> Optional[Client]:
    """Get a client by ID."""
    return await db.client.find_unique(where={"id": client_id})


async def get_client_by_covered_number(db: Prisma, phone: str) -> Optional[Client]:
    """Get a client by their Covered phone number."""
    return await db.client.find_first(where={"coveredNumber": phone})


async def list_clients(
    db: Prisma,
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None
) -> tuple[List[Client], int]:
    """List all clients with pagination."""
    where = {}
    if status:
        where["subscriptionStatus"] = status

    clients = await db.client.find_many(
        where=where,
        take=limit,
        skip=offset,
        order={"createdAt": "desc"}
    )
    total = await db.client.count(where=where)
    return clients, total


async def create_client(db: Prisma, data: Dict[str, Any]) -> Client:
    """Create a new client."""
    return await db.client.create(data=data)


async def update_client(db: Prisma, client_id: str, data: Dict[str, Any]) -> Client:
    """Update a client."""
    return await db.client.update(
        where={"id": client_id},
        data=data
    )


async def find_or_create_customer(
    db: Prisma,
    client_id: str,
    phone: str,
    name: str,
    email: Optional[str] = None,
    address: Optional[str] = None,
    postcode: Optional[str] = None
) -> Customer:
    """Find existing customer by phone or create new one."""
    # Try to find existing
    customer = await db.customer.find_first(
        where={
            "clientId": client_id,
            "phone": phone
        }
    )

    if customer:
        return customer

    # Create new customer
    return await db.customer.create(
        data={
            "clientId": client_id,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "postcode": postcode,
            "source": "phone_call"
        }
    )


async def create_lead(db: Prisma, data: Dict[str, Any]) -> Lead:
    """Create a new lead."""
    return await db.lead.create(
        data=data,
        include={"client": True, "customer": True}
    )


async def get_lead_by_id(db: Prisma, lead_id: str) -> Optional[Lead]:
    """Get a lead by ID with full details."""
    return await db.lead.find_unique(
        where={"id": lead_id},
        include={
            "client": True,
            "customer": True,
            "nurtureSequence": True,
            "notifications": {
                "order_by": {"createdAt": "desc"},
                "take": 10
            }
        }
    )


async def list_leads(
    db: Prisma,
    client_id: str,
    status: Optional[str] = None,
    urgency: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> tuple[List[Lead], int]:
    """List leads for a client with filters."""
    where: Dict[str, Any] = {"clientId": client_id}

    if status:
        where["status"] = status
    if urgency:
        where["urgency"] = urgency

    leads = await db.lead.find_many(
        where=where,
        include={"customer": True, "nurtureSequence": True},
        take=limit,
        skip=offset,
        order={"createdAt": "desc"}
    )
    total = await db.lead.count(where=where)
    return leads, total


async def update_lead_status(
    db: Prisma,
    lead_id: str,
    status: str,
    dismiss_reason: Optional[str] = None
) -> Lead:
    """Update lead status with appropriate timestamp."""
    data: Dict[str, Any] = {"status": status}

    if status == "booked":
        data["bookedAt"] = datetime.utcnow()
    elif status == "converted":
        data["convertedAt"] = datetime.utcnow()
    elif status == "dismissed":
        data["dismissedAt"] = datetime.utcnow()
        data["dismissReason"] = dismiss_reason
    elif status == "qualified":
        data["qualifiedAt"] = datetime.utcnow()

    return await db.lead.update(
        where={"id": lead_id},
        data=data
    )


async def create_nurture_sequence(db: Prisma, lead_id: str) -> NurtureSequence:
    """Create a nurture sequence for a lead."""
    sequence = await db.nurturesequence.create(
        data={
            "leadId": lead_id,
            "currentTouch": 0,
            "status": "active",
            "nextTouchAt": datetime.utcnow(),
            "nextTouchNumber": 1
        }
    )

    # Link to lead
    await db.lead.update(
        where={"id": lead_id},
        data={
            "nurtureSequenceId": sequence.id,
            "status": "nurturing"
        }
    )

    return sequence


async def update_nurture_progress(
    db: Prisma,
    lead_id: str,
    touch_number: int
) -> Optional[NurtureSequence]:
    """Record a nurture touch as sent."""
    lead = await db.lead.find_unique(
        where={"id": lead_id},
        include={"nurtureSequence": True}
    )

    if not lead or not lead.nurtureSequence:
        return None

    # Build update data
    touch_field = f"touch{touch_number}SentAt"
    data: Dict[str, Any] = {
        "currentTouch": touch_number,
        touch_field: datetime.utcnow()
    }

    # Set next touch or complete
    if touch_number >= 12:
        data["status"] = "completed"
        data["completedAt"] = datetime.utcnow()
        data["nextTouchAt"] = None
        data["nextTouchNumber"] = None
    else:
        data["nextTouchNumber"] = touch_number + 1

    return await db.nurturesequence.update(
        where={"id": lead.nurtureSequence.id},
        data=data
    )


async def stop_nurture_sequence(
    db: Prisma,
    lead_id: str,
    reason: str
) -> Optional[NurtureSequence]:
    """Stop a nurture sequence."""
    lead = await db.lead.find_unique(
        where={"id": lead_id},
        include={"nurtureSequence": True}
    )

    if not lead or not lead.nurtureSequence:
        return None

    return await db.nurturesequence.update(
        where={"id": lead.nurtureSequence.id},
        data={
            "status": "stopped",
            "stoppedAt": datetime.utcnow(),
            "stopReason": reason,
            "nextTouchAt": None,
            "nextTouchNumber": None
        }
    )


async def create_job(db: Prisma, data: Dict[str, Any]) -> Job:
    """Create a new job."""
    return await db.job.create(
        data=data,
        include={"customer": True, "lead": True}
    )


async def get_job_by_id(db: Prisma, job_id: str) -> Optional[Job]:
    """Get a job by ID."""
    return await db.job.find_unique(
        where={"id": job_id},
        include={"customer": True, "client": True, "lead": True}
    )


async def list_jobs(
    db: Prisma,
    client_id: str,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> tuple[List[Job], int]:
    """List jobs for a client."""
    where: Dict[str, Any] = {"clientId": client_id}

    if status:
        where["status"] = status

    jobs = await db.job.find_many(
        where=where,
        include={"customer": True},
        take=limit,
        skip=offset,
        order={"scheduledDate": "desc"}
    )
    total = await db.job.count(where=where)
    return jobs, total


async def update_job_status(
    db: Prisma,
    job_id: str,
    status: str,
    final_amount: Optional[float] = None
) -> Job:
    """Update job status."""
    data: Dict[str, Any] = {"status": status}

    if status == "completed":
        data["completedAt"] = datetime.utcnow()
    elif status == "cancelled":
        data["cancelledAt"] = datetime.utcnow()
    elif status == "in_progress":
        data["startedAt"] = datetime.utcnow()
    elif status == "confirmed":
        data["confirmedAt"] = datetime.utcnow()

    if final_amount is not None:
        data["finalAmount"] = final_amount

    return await db.job.update(
        where={"id": job_id},
        data=data,
        include={"customer": True, "client": True}
    )


async def create_notification(db: Prisma, data: Dict[str, Any]) -> Notification:
    """Create a notification record."""
    return await db.notification.create(data=data)


async def update_notification_status(
    db: Prisma,
    notification_id: str,
    status: str,
    error: Optional[str] = None
) -> Notification:
    """Update notification delivery status."""
    data: Dict[str, Any] = {"status": status}

    if status == "sent":
        data["sentAt"] = datetime.utcnow()
    elif status == "delivered":
        data["deliveredAt"] = datetime.utcnow()
    elif status == "failed":
        data["failedAt"] = datetime.utcnow()
        data["error"] = error

    return await db.notification.update(
        where={"id": notification_id},
        data=data
    )


async def get_dashboard_stats(db: Prisma, client_id: str) -> Dict[str, Any]:
    """Get dashboard statistics for a client."""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Run queries in parallel-ish (Prisma doesn't support true parallel in Python yet)
    leads_today = await db.lead.count(
        where={"clientId": client_id, "createdAt": {"gte": today_start}}
    )
    leads_this_week = await db.lead.count(
        where={"clientId": client_id, "createdAt": {"gte": week_start}}
    )
    leads_this_month = await db.lead.count(
        where={"clientId": client_id, "createdAt": {"gte": month_start}}
    )
    converted_leads = await db.lead.count(
        where={
            "clientId": client_id,
            "createdAt": {"gte": month_start},
            "status": {"in": ["booked", "converted"]}
        }
    )
    jobs_scheduled = await db.job.count(
        where={
            "clientId": client_id,
            "status": "scheduled",
            "scheduledDate": {"gte": now}
        }
    )
    jobs_completed = await db.job.count(
        where={
            "clientId": client_id,
            "status": "completed",
            "completedAt": {"gte": month_start}
        }
    )

    # Calculate revenue
    completed_jobs = await db.job.find_many(
        where={
            "clientId": client_id,
            "status": "completed",
            "completedAt": {"gte": month_start}
        }
    )
    revenue = sum(
        float(job.finalAmount) if job.finalAmount else 0
        for job in completed_jobs
    )

    conversion_rate = (converted_leads / leads_this_month * 100) if leads_this_month > 0 else 0

    return {
        "leadsToday": leads_today,
        "leadsThisWeek": leads_this_week,
        "leadsThisMonth": leads_this_month,
        "conversionRate": round(conversion_rate, 1),
        "jobsScheduled": jobs_scheduled,
        "jobsCompleted": jobs_completed,
        "revenueThisMonth": revenue
    }

"""
Dashboard Routes - Single API call returning all dashboard data
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, date
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from src.db.client import get_prisma

router = APIRouter()

# Vertical-aware terminology
TERMINOLOGY = {
    "trades": {"customer": "customer", "customers": "customers"},
    "vet": {"customer": "client", "customers": "clients"},
    "dental": {"customer": "patient", "customers": "patients"},
    "aesthetics": {"customer": "client", "customers": "clients"},
    "salon": {"customer": "client", "customers": "clients"},
    "physio": {"customer": "patient", "customers": "patients"},
    "optometry": {"customer": "patient", "customers": "patients"},
    "auto": {"customer": "customer", "customers": "customers"},
    "legal": {"customer": "client", "customers": "clients"},
    "accountant": {"customer": "client", "customers": "clients"},
    "fitness": {"customer": "member", "customers": "members"},
}


def get_greeting() -> str:
    """Get time-appropriate greeting."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def get_terminology(vertical: str) -> Dict[str, str]:
    """Get vertical-specific terminology."""
    return TERMINOLOGY.get(vertical, TERMINOLOGY["trades"])


def calculate_cash_health_percent(
    collected: float, outstanding: float, overdue: float
) -> int:
    """Calculate cash health as percentage (for traffic light system)."""
    total = collected + outstanding
    if total == 0:
        return 100  # No invoices = healthy
    # Health = (collected / (collected + outstanding)) * 100
    # Penalize overdue more heavily
    health = (collected / total) * 100
    # Reduce health by overdue ratio
    if outstanding > 0:
        overdue_ratio = overdue / outstanding
        health = health * (1 - (overdue_ratio * 0.3))  # 30% penalty for overdue
    return max(0, min(100, int(health)))


def attention_item_to_response(item) -> dict:
    """Convert Prisma attention item to response dict."""
    return {
        "id": item.id,
        "item_type": item.itemType,
        "item_id": item.itemId,
        "priority": item.priority,
        "category": item.category,
        "title": item.title,
        "subtitle": item.subtitle,
        "action_type": item.actionType,
        "action_label": item.actionLabel,
        "action_data": item.actionData,
        "created_at": item.createdAt,
    }


@router.get("/{client_id}")
async def get_dashboard(client_id: str, db=Depends(get_prisma)):
    """
    Get complete dashboard data in a single API call.

    Returns:
    - client info with greeting
    - needs_attention items (priority-sorted)
    - today_stats (calls, revenue, reviews with trends)
    - cash_health (collected, outstanding, overdue, health %)
    - customer_snapshot (total, repeat rate, LTV, LTV:CAC)
    - terminology (vertical-aware customer/client/patient labels)
    """
    # Get client
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get terminology for this vertical
    terms = get_terminology(client.vertical)

    # Get pre-calculated stats
    stats = await db.dashboardstats.find_unique(where={"clientId": client_id})

    # Get attention items (unresolved, sorted by priority)
    attention_items = await db.attentionitem.find_many(
        where={"clientId": client_id, "resolved": False},
        order={"priority": "desc"},
        take=10,
    )

    # Get cash metrics
    cash_metrics = await db.clientcashmetrics.find_unique(where={"clientId": client_id})

    # Get unit economics
    unit_economics = await db.clientuniteconomics.find_unique(
        where={"clientId": client_id}
    )

    # Calculate cash health percentage
    cash_health_percent = 100
    if cash_metrics:
        cash_health_percent = calculate_cash_health_percent(
            float(cash_metrics.collectedThisMonth),
            float(cash_metrics.totalOutstanding),
            float(cash_metrics.totalOverdue),
        )

    # Calculate 30-day forecast (simple: current outstanding that's not overdue)
    forecast_30_day = 0
    if cash_metrics:
        forecast_30_day = float(cash_metrics.totalOutstanding) - float(
            cash_metrics.totalOverdue
        )

    # Build response
    response = {
        "client": {
            "id": client.id,
            "business_name": client.businessName,
            "owner_name": client.ownerName,
            "vertical": client.vertical,
            "greeting": f"{get_greeting()}, {client.ownerName}",
        },
        "terminology": terms,
        "needs_attention": [attention_item_to_response(item) for item in attention_items],
        "attention_count": len(attention_items),
        "today_stats": {
            "calls_today": stats.callsToday if stats else 0,
            "calls_today_trend": stats.callsTodayTrend if stats else 0,
            "revenue_this_week": float(stats.revenueThisWeek) if stats else 0,
            "revenue_this_week_trend": stats.revenueThisWeekTrend if stats else 0,
            "reviews_this_week": stats.reviewsThisWeek if stats else 0,
            "reviews_this_week_trend": stats.reviewsThisWeekTrend if stats else 0,
        },
        "cash_health": {
            "collected_this_month": float(cash_metrics.collectedThisMonth) if cash_metrics else 0,
            "total_outstanding": float(cash_metrics.totalOutstanding) if cash_metrics else 0,
            "total_overdue": float(cash_metrics.totalOverdue) if cash_metrics else 0,
            "health_percent": cash_health_percent,
            "health_status": (
                "green" if cash_health_percent >= 80 else
                "yellow" if cash_health_percent >= 60 else
                "red"
            ),
            "average_dso": cash_metrics.averageDSO if cash_metrics else 0,
            "forecast_30_day": forecast_30_day,
        },
        "customer_snapshot": {
            "total_customers": unit_economics.totalCustomers if unit_economics else 0,
            "repeat_customers": unit_economics.repeatCustomers if unit_economics else 0,
            "repeat_rate": float(unit_economics.repeatRate) if unit_economics else 0,
            "customer_ltv": float(unit_economics.customerLTV) if unit_economics else 0,
            "avg_cac": float(unit_economics.avgCAC) if unit_economics else 0,
            "ltv_cac_ratio": float(unit_economics.ltvCacRatio) if unit_economics else 0,
            "ltv_cac_trend": unit_economics.ltvCacTrend if unit_economics else "stable",
            "insight": generate_customer_insight(unit_economics, terms),
        },
        "all_time": {
            "calls_answered": stats.totalCallsAnswered if stats else 0,
            "leads_captured": stats.totalLeadsCaptured if stats else 0,
            "jobs_booked": stats.totalJobsBooked if stats else 0,
            "total_revenue": float(stats.totalRevenue) if stats else 0,
            "time_saved_hours": stats.totalTimeSavedHrs if stats else 0,
        },
        "calculated_at": stats.calculatedAt if stats else None,
    }

    return response


def generate_customer_insight(unit_economics, terms: Dict[str, str]) -> str:
    """Generate insight text based on unit economics."""
    if not unit_economics:
        return f"Start tracking {terms['customers']} to see insights"

    ltv_cac = float(unit_economics.ltvCacRatio) if unit_economics.ltvCacRatio else 0
    repeat_rate = float(unit_economics.repeatRate) if unit_economics.repeatRate else 0
    trend = unit_economics.ltvCacTrend

    if ltv_cac >= 3:
        return f"Excellent! Each {terms['customer']} is worth {ltv_cac:.1f}x their acquisition cost"
    elif ltv_cac >= 1:
        if trend == "up":
            return f"Getting better! Your LTV:CAC is improving"
        return f"Your {terms['customers']} are worth {ltv_cac:.1f}x acquisition cost - aim for 3x"
    elif ltv_cac > 0:
        return f"Focus on retention - {terms['customers']} cost more to acquire than they spend"
    else:
        return f"Add marketing spend and {terms['customer']} data to calculate LTV:CAC"


@router.post("/{client_id}/attention/{item_id}/resolve")
async def resolve_attention_item(
    client_id: str,
    item_id: str,
    db=Depends(get_prisma)
):
    """Mark an attention item as resolved."""
    item = await db.attentionitem.find_unique(where={"id": item_id})
    if not item or item.clientId != client_id:
        raise HTTPException(status_code=404, detail="Attention item not found")

    await db.attentionitem.update(
        where={"id": item_id},
        data={"resolved": True, "resolvedAt": datetime.utcnow()},
    )

    return {"message": "Item resolved", "id": item_id}


@router.delete("/{client_id}/attention/{item_id}")
async def delete_attention_item(
    client_id: str,
    item_id: str,
    db=Depends(get_prisma)
):
    """Delete an attention item."""
    item = await db.attentionitem.find_unique(where={"id": item_id})
    if not item or item.clientId != client_id:
        raise HTTPException(status_code=404, detail="Attention item not found")

    await db.attentionitem.delete(where={"id": item_id})

    return {"message": "Item deleted", "id": item_id}


# =============================================================================
# ATTENTION ITEM CREATION (for Trigger.dev jobs)
# =============================================================================

from pydantic import BaseModel

class AttentionItemCreate(BaseModel):
    item_type: str
    item_id: str
    priority: int = 50
    category: str
    title: str
    subtitle: Optional[str] = None
    action_type: str
    action_label: str
    action_data: Optional[dict] = None


@router.post("/{client_id}/attention")
async def create_attention_item(
    client_id: str,
    item: AttentionItemCreate,
    db=Depends(get_prisma)
):
    """Create or update an attention item (upsert by item_type + item_id)."""
    # Check if item already exists
    existing = await db.attentionitem.find_first(
        where={
            "clientId": client_id,
            "itemType": item.item_type,
            "itemId": item.item_id,
            "resolved": False,
        }
    )

    if existing:
        # Update existing
        updated = await db.attentionitem.update(
            where={"id": existing.id},
            data={
                "priority": item.priority,
                "category": item.category,
                "title": item.title,
                "subtitle": item.subtitle,
                "actionType": item.action_type,
                "actionLabel": item.action_label,
                "actionData": item.action_data,
            },
        )
        return {"id": updated.id, "action": "updated"}

    # Create new
    created = await db.attentionitem.create(
        data={
            "clientId": client_id,
            "itemType": item.item_type,
            "itemId": item.item_id,
            "priority": item.priority,
            "category": item.category,
            "title": item.title,
            "subtitle": item.subtitle,
            "actionType": item.action_type,
            "actionLabel": item.action_label,
            "actionData": item.action_data,
        }
    )

    return {"id": created.id, "action": "created"}


@router.post("/{client_id}/attention/clear-old")
async def clear_old_attention_items(
    client_id: str,
    db=Depends(get_prisma)
):
    """Clear resolved attention items older than 24 hours."""
    cutoff = datetime.utcnow() - timedelta(hours=24)

    result = await db.attentionitem.delete_many(
        where={
            "clientId": client_id,
            "resolved": True,
            "resolvedAt": {"lt": cutoff},
        }
    )

    return {"deleted": result}


# =============================================================================
# STATS UPDATE (for Trigger.dev jobs)
# =============================================================================

class DashboardStatsUpdate(BaseModel):
    calls_today: int = 0
    calls_today_trend: int = 0
    revenue_this_week: float = 0
    revenue_this_week_trend: int = 0
    reviews_this_week: int = 0
    reviews_this_week_trend: int = 0
    total_calls_answered: int = 0
    total_leads_captured: int = 0
    total_jobs_booked: int = 0
    total_revenue: float = 0
    total_time_saved_hrs: int = 0


@router.put("/{client_id}/stats")
async def update_dashboard_stats(
    client_id: str,
    stats: DashboardStatsUpdate,
    db=Depends(get_prisma)
):
    """Update or create dashboard stats for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Upsert stats
    updated = await db.dashboardstats.upsert(
        where={"clientId": client_id},
        data={
            "create": {
                "clientId": client_id,
                "callsToday": stats.calls_today,
                "callsTodayTrend": stats.calls_today_trend,
                "revenueThisWeek": Decimal(str(stats.revenue_this_week)),
                "revenueThisWeekTrend": stats.revenue_this_week_trend,
                "reviewsThisWeek": stats.reviews_this_week,
                "reviewsThisWeekTrend": stats.reviews_this_week_trend,
                "totalCallsAnswered": stats.total_calls_answered,
                "totalLeadsCaptured": stats.total_leads_captured,
                "totalJobsBooked": stats.total_jobs_booked,
                "totalRevenue": Decimal(str(stats.total_revenue)),
                "totalTimeSavedHrs": stats.total_time_saved_hrs,
                "calculatedAt": datetime.utcnow(),
            },
            "update": {
                "callsToday": stats.calls_today,
                "callsTodayTrend": stats.calls_today_trend,
                "revenueThisWeek": Decimal(str(stats.revenue_this_week)),
                "revenueThisWeekTrend": stats.revenue_this_week_trend,
                "reviewsThisWeek": stats.reviews_this_week,
                "reviewsThisWeekTrend": stats.reviews_this_week_trend,
                "totalCallsAnswered": stats.total_calls_answered,
                "totalLeadsCaptured": stats.total_leads_captured,
                "totalJobsBooked": stats.total_jobs_booked,
                "totalRevenue": Decimal(str(stats.total_revenue)),
                "totalTimeSavedHrs": stats.total_time_saved_hrs,
                "calculatedAt": datetime.utcnow(),
            },
        }
    )

    return {
        "client_id": client_id,
        "message": "Stats updated",
        "calculated_at": updated.calculatedAt,
    }


# =============================================================================
# FINANCIAL DASHBOARD ENDPOINTS (Phase 5)
# =============================================================================

@router.get("/{client_id}/financial-summary")
async def get_financial_summary(client_id: str, db=Depends(get_prisma)):
    """
    Get financial summary: total billed, collected, outstanding, overdue.
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get all invoices for this client
    invoices = await db.invoice.find_many(
        where={"clientId": client_id},
    )

    total_billed = sum(float(inv.amount) for inv in invoices)
    total_collected = sum(
        float(inv.amount) for inv in invoices if inv.status == "PAID"
    )
    total_outstanding = sum(
        float(inv.amount) for inv in invoices if inv.status in ["SENT", "REMINDED", "OVERDUE"]
    )
    total_overdue = sum(
        float(inv.amount) for inv in invoices if inv.status == "OVERDUE"
    )

    overdue_count = len([inv for inv in invoices if inv.status == "OVERDUE"])

    # Calculate collection rate
    collection_rate = (total_collected / total_billed * 100) if total_billed > 0 else 0

    return {
        "client_id": client_id,
        "total_billed": round(total_billed, 2),
        "total_collected": round(total_collected, 2),
        "total_outstanding": round(total_outstanding, 2),
        "total_overdue": round(total_overdue, 2),
        "overdue_count": overdue_count,
        "collection_rate": round(collection_rate, 1),
        "invoice_count": len(invoices),
    }


@router.get("/{client_id}/revenue-trend")
async def get_revenue_trend(
    client_id: str,
    months: int = Query(default=6, ge=1, le=12),
    db=Depends(get_prisma)
):
    """
    Get revenue trend for the last N months.
    Returns monthly totals for billed and collected.
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Calculate date range
    today = date.today()
    start_date = today - relativedelta(months=months - 1)
    start_date = date(start_date.year, start_date.month, 1)  # First of month

    # Get invoices created in this period
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "createdAt": {"gte": datetime.combine(start_date, datetime.min.time())},
        },
    )

    # Group by month
    monthly_data = {}
    for i in range(months):
        month_date = today - relativedelta(months=months - 1 - i)
        month_key = month_date.strftime("%Y-%m")
        monthly_data[month_key] = {
            "month": month_date.strftime("%b %Y"),
            "billed": 0,
            "collected": 0,
        }

    for inv in invoices:
        month_key = inv.createdAt.strftime("%Y-%m")
        if month_key in monthly_data:
            monthly_data[month_key]["billed"] += float(inv.amount)
            if inv.status == "PAID":
                monthly_data[month_key]["collected"] += float(inv.amount)

    # Calculate trend (compare last month to previous)
    data_list = list(monthly_data.values())
    trend = 0
    if len(data_list) >= 2:
        last_month = data_list[-1]["billed"]
        prev_month = data_list[-2]["billed"]
        if prev_month > 0:
            trend = round(((last_month - prev_month) / prev_month) * 100, 1)

    return {
        "client_id": client_id,
        "months": months,
        "data": data_list,
        "trend_percent": trend,
        "trend_direction": "up" if trend > 0 else "down" if trend < 0 else "stable",
    }


@router.get("/{client_id}/payment-forecast")
async def get_payment_forecast(
    client_id: str,
    days: int = Query(default=30, ge=7, le=90),
    db=Depends(get_prisma)
):
    """
    Get payment forecast for the next N days.
    Based on invoice due dates.
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    today = date.today()
    end_date = today + timedelta(days=days)

    # Get outstanding invoices with due dates in range
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "status": {"in": ["SENT", "REMINDED"]},
            "dueDate": {
                "gte": datetime.combine(today, datetime.min.time()),
                "lte": datetime.combine(end_date, datetime.max.time()),
            },
        },
        order={"dueDate": "asc"},
    )

    # Group by week
    weekly_data = []
    for week_num in range((days // 7) + 1):
        week_start = today + timedelta(days=week_num * 7)
        week_end = week_start + timedelta(days=6)
        week_invoices = [
            inv for inv in invoices
            if week_start <= inv.dueDate.date() <= week_end
        ]
        weekly_data.append({
            "week": f"Week {week_num + 1}",
            "start_date": week_start.isoformat(),
            "end_date": week_end.isoformat(),
            "expected_amount": round(sum(float(inv.amount) for inv in week_invoices), 2),
            "invoice_count": len(week_invoices),
        })

    total_expected = sum(week["expected_amount"] for week in weekly_data)

    return {
        "client_id": client_id,
        "days": days,
        "total_expected": round(total_expected, 2),
        "weeks": weekly_data,
    }


@router.get("/{client_id}/outstanding-invoices")
async def get_outstanding_invoices(
    client_id: str,
    limit: int = Query(default=5, ge=1, le=20),
    db=Depends(get_prisma)
):
    """
    Get outstanding invoices sorted by priority (overdue first, then by amount).
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get outstanding invoices
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "status": {"in": ["SENT", "REMINDED", "OVERDUE"]},
        },
        order=[{"status": "desc"}, {"dueDate": "asc"}],
        take=limit,
    )

    today = date.today()
    result = []
    for inv in invoices:
        days_until_due = (inv.dueDate.date() - today).days if inv.dueDate else 0

        # Determine urgency
        if inv.status == "OVERDUE":
            urgency = "overdue"
        elif days_until_due <= 3:
            urgency = "due_soon"
        else:
            urgency = "pending"

        result.append({
            "id": inv.id,
            "invoice_number": inv.invoiceNumber,
            "customer_name": inv.customerName,
            "amount": float(inv.amount),
            "due_date": inv.dueDate.isoformat() if inv.dueDate else None,
            "days_until_due": days_until_due,
            "status": inv.status,
            "urgency": urgency,
            "reminder1_sent": inv.reminder1SentAt is not None,
            "reminder2_sent": inv.reminder2SentAt is not None,
            "final_notice_sent": inv.finalNoticeSentAt is not None,
        })

    total_outstanding = sum(inv["amount"] for inv in result)

    return {
        "client_id": client_id,
        "invoices": result,
        "total_outstanding": round(total_outstanding, 2),
        "count": len(result),
    }

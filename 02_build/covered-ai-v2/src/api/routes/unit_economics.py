"""
Unit Economics Routes - LTV:CAC tracking and metrics
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from src.db.client import get_prisma

router = APIRouter()


class MarketingSpendCreate(BaseModel):
    month: str  # "2025-01"
    amount: float
    source: Optional[str] = None  # "google_ads", "facebook", "flyers", "covered_ai", "other"
    notes: Optional[str] = None


class UnitEconomicsUpdate(BaseModel):
    total_customers: int
    repeat_customers: int
    repeat_rate: float
    avg_job_value: float
    avg_jobs_per_customer: float
    customer_ltv: float
    total_marketing_spend: float
    new_customers_this_month: int
    avg_cac: float
    ltv_cac_ratio: float
    ltv_cac_last_month: float
    ltv_cac_trend: str


class AddJobRevenueRequest(BaseModel):
    revenue: float
    completed_at: Optional[datetime] = None


def unit_economics_to_response(metrics) -> dict:
    """Convert Prisma unit economics to response dict."""
    return {
        "client_id": metrics.clientId,
        "total_customers": metrics.totalCustomers,
        "repeat_customers": metrics.repeatCustomers,
        "repeat_rate": float(metrics.repeatRate),
        "avg_job_value": float(metrics.avgJobValue),
        "avg_jobs_per_customer": float(metrics.avgJobsPerCustomer),
        "customer_ltv": float(metrics.customerLTV),
        "total_marketing_spend": float(metrics.totalMarketingSpend),
        "new_customers_this_month": metrics.newCustomersThisMonth,
        "avg_cac": float(metrics.avgCAC),
        "ltv_cac_ratio": float(metrics.ltvCacRatio),
        "ltv_cac_last_month": float(metrics.ltvCacLastMonth),
        "ltv_cac_trend": metrics.ltvCacTrend,
        "calculated_at": metrics.calculatedAt,
    }


def customer_to_response(customer) -> dict:
    """Convert Prisma customer to response dict."""
    return {
        "id": customer.id,
        "client_id": customer.clientId,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "total_jobs": customer.totalJobs,
        "total_revenue": float(customer.totalRevenue) if customer.totalRevenue else 0,
        "first_job_date": customer.firstJobDate,
        "last_job_date": customer.lastJobDate,
        "acquisition_source": customer.acquisitionSource,
    }


# =============================================================================
# UNIT ECONOMICS ROUTES
# =============================================================================

@router.get("/clients/{client_id}")
async def get_unit_economics(client_id: str, db=Depends(get_prisma)):
    """Get unit economics metrics for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    metrics = await db.clientuniteconomics.find_unique(
        where={"clientId": client_id}
    )

    if not metrics:
        # Return default metrics
        return {
            "client_id": client_id,
            "total_customers": 0,
            "repeat_customers": 0,
            "repeat_rate": 0,
            "avg_job_value": 0,
            "avg_jobs_per_customer": 1,
            "customer_ltv": 0,
            "total_marketing_spend": 0,
            "new_customers_this_month": 0,
            "avg_cac": 0,
            "ltv_cac_ratio": 0,
            "ltv_cac_last_month": 0,
            "ltv_cac_trend": "stable",
            "calculated_at": None,
        }

    return unit_economics_to_response(metrics)


@router.put("/clients/{client_id}")
async def update_unit_economics(
    client_id: str,
    metrics: UnitEconomicsUpdate,
    db=Depends(get_prisma)
):
    """Update unit economics metrics for a client (called by scheduled job)."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Upsert metrics
    updated = await db.clientuniteconomics.upsert(
        where={"clientId": client_id},
        data={
            "create": {
                "clientId": client_id,
                "totalCustomers": metrics.total_customers,
                "repeatCustomers": metrics.repeat_customers,
                "repeatRate": Decimal(str(metrics.repeat_rate)),
                "avgJobValue": Decimal(str(metrics.avg_job_value)),
                "avgJobsPerCustomer": Decimal(str(metrics.avg_jobs_per_customer)),
                "customerLTV": Decimal(str(metrics.customer_ltv)),
                "totalMarketingSpend": Decimal(str(metrics.total_marketing_spend)),
                "newCustomersThisMonth": metrics.new_customers_this_month,
                "avgCAC": Decimal(str(metrics.avg_cac)),
                "ltvCacRatio": Decimal(str(metrics.ltv_cac_ratio)),
                "ltvCacLastMonth": Decimal(str(metrics.ltv_cac_last_month)),
                "ltvCacTrend": metrics.ltv_cac_trend,
                "calculatedAt": datetime.utcnow(),
            },
            "update": {
                "totalCustomers": metrics.total_customers,
                "repeatCustomers": metrics.repeat_customers,
                "repeatRate": Decimal(str(metrics.repeat_rate)),
                "avgJobValue": Decimal(str(metrics.avg_job_value)),
                "avgJobsPerCustomer": Decimal(str(metrics.avg_jobs_per_customer)),
                "customerLTV": Decimal(str(metrics.customer_ltv)),
                "totalMarketingSpend": Decimal(str(metrics.total_marketing_spend)),
                "newCustomersThisMonth": metrics.new_customers_this_month,
                "avgCAC": Decimal(str(metrics.avg_cac)),
                "ltvCacRatio": Decimal(str(metrics.ltv_cac_ratio)),
                "ltvCacLastMonth": Decimal(str(metrics.ltv_cac_last_month)),
                "ltvCacTrend": metrics.ltv_cac_trend,
                "calculatedAt": datetime.utcnow(),
            }
        }
    )

    return {
        "client_id": client_id,
        "message": "Unit economics updated",
        "calculated_at": updated.calculatedAt,
    }


# =============================================================================
# CUSTOMER DATA FOR CALCULATIONS
# =============================================================================

@router.get("/clients/{client_id}/customers")
async def get_customers_for_ltv(client_id: str, db=Depends(get_prisma)):
    """Get all customers with LTV data for a client."""
    customers = await db.customer.find_many(
        where={"clientId": client_id},
        order={"totalRevenue": "desc"},
    )

    return {
        "customers": [customer_to_response(c) for c in customers],
        "total": len(customers),
    }


@router.get("/clients/{client_id}/completed-jobs")
async def get_completed_jobs_for_ltv(client_id: str, db=Depends(get_prisma)):
    """Get all completed jobs for LTV calculations."""
    jobs = await db.job.find_many(
        where={
            "clientId": client_id,
            "status": "completed",
        },
        order={"completedAt": "desc"},
    )

    return {
        "jobs": [
            {
                "id": j.id,
                "client_id": j.clientId,
                "customer_id": j.customerId,
                "final_amount": float(j.finalAmount) if j.finalAmount else None,
                "quoted_amount": float(j.quotedAmount) if j.quotedAmount else None,
                "completed_at": j.completedAt,
            }
            for j in jobs
        ],
        "total": len(jobs),
    }


# =============================================================================
# MARKETING SPEND ROUTES
# =============================================================================

@router.get("/clients/{client_id}/marketing-spend")
async def get_marketing_spend(
    client_id: str,
    month: Optional[str] = None,
    db=Depends(get_prisma)
):
    """Get marketing spend records for a client."""
    where = {"clientId": client_id}
    if month:
        where["month"] = month

    spend = await db.marketingspend.find_many(
        where=where,
        order={"month": "desc"},
    )

    return {
        "spend": [
            {
                "id": s.id,
                "month": s.month,
                "amount": float(s.amount),
                "source": s.source,
                "notes": s.notes,
                "created_at": s.createdAt,
            }
            for s in spend
        ],
        "total": len(spend),
    }


@router.post("/clients/{client_id}/marketing-spend")
async def add_marketing_spend(
    client_id: str,
    spend: MarketingSpendCreate,
    db=Depends(get_prisma)
):
    """Add marketing spend for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Upsert (update if exists for same month/source)
    created = await db.marketingspend.upsert(
        where={
            "clientId_month_source": {
                "clientId": client_id,
                "month": spend.month,
                "source": spend.source or "other",
            }
        },
        data={
            "create": {
                "clientId": client_id,
                "month": spend.month,
                "amount": Decimal(str(spend.amount)),
                "source": spend.source or "other",
                "notes": spend.notes,
            },
            "update": {
                "amount": Decimal(str(spend.amount)),
                "notes": spend.notes,
            }
        }
    )

    return {
        "id": created.id,
        "message": "Marketing spend added",
        "month": spend.month,
        "amount": float(created.amount),
    }


@router.delete("/clients/{client_id}/marketing-spend/{spend_id}")
async def delete_marketing_spend(
    client_id: str,
    spend_id: str,
    db=Depends(get_prisma)
):
    """Delete a marketing spend record."""
    spend = await db.marketingspend.find_unique(where={"id": spend_id})

    if not spend or spend.clientId != client_id:
        raise HTTPException(status_code=404, detail="Marketing spend not found")

    await db.marketingspend.delete(where={"id": spend_id})

    return {"message": "Marketing spend deleted"}


# =============================================================================
# CUSTOMER LTV UPDATE
# =============================================================================

@router.post("/customers/{customer_id}/add-job-revenue")
async def add_job_revenue_to_customer(
    customer_id: str,
    request: AddJobRevenueRequest,
    db=Depends(get_prisma)
):
    """Add job revenue to customer's LTV tracking."""
    customer = await db.customer.find_unique(where={"id": customer_id})

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    completed_at = request.completed_at or datetime.utcnow()

    # Update customer stats
    update_data = {
        "totalJobs": customer.totalJobs + 1,
        "totalRevenue": float(customer.totalRevenue or 0) + request.revenue,
        "lastJobDate": completed_at,
    }

    # Set first job date if not set
    if not customer.firstJobDate:
        update_data["firstJobDate"] = completed_at

    updated = await db.customer.update(
        where={"id": customer_id},
        data=update_data,
    )

    return {
        "customer_id": customer_id,
        "total_jobs": updated.totalJobs,
        "total_revenue": float(updated.totalRevenue),
        "message": "Customer LTV updated",
    }


# =============================================================================
# DASHBOARD SUMMARY
# =============================================================================

@router.get("/clients/{client_id}/dashboard")
async def get_ltv_cac_dashboard(client_id: str, db=Depends(get_prisma)):
    """Get a comprehensive LTV:CAC dashboard for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get unit economics
    metrics = await db.clientuniteconomics.find_unique(
        where={"clientId": client_id}
    )

    # Get top customers by LTV
    top_customers = await db.customer.find_many(
        where={"clientId": client_id},
        order={"totalRevenue": "desc"},
        take=5,
    )

    # Get recent marketing spend
    recent_spend = await db.marketingspend.find_many(
        where={"clientId": client_id},
        order={"month": "desc"},
        take=6,
    )

    # Get customer acquisition by source
    customers_by_source = await db.customer.group_by(
        by=["acquisitionSource"],
        where={"clientId": client_id},
        count=True,
    )

    return {
        "metrics": unit_economics_to_response(metrics) if metrics else None,
        "top_customers": [customer_to_response(c) for c in top_customers],
        "recent_marketing_spend": [
            {
                "month": s.month,
                "amount": float(s.amount),
                "source": s.source,
            }
            for s in recent_spend
        ],
        "customers_by_source": [
            {
                "source": item.get("acquisitionSource") or "unknown",
                "count": item.get("_count", {}).get("_all", 0) if isinstance(item.get("_count"), dict) else item.get("_count", 0),
            }
            for item in customers_by_source
        ],
        "insights": generate_insights(metrics) if metrics else [],
    }


def generate_insights(metrics) -> List[dict]:
    """Generate actionable insights from unit economics."""
    insights = []

    ltv_cac = float(metrics.ltvCacRatio) if metrics else 0
    repeat_rate = float(metrics.repeatRate) if metrics else 0

    # LTV:CAC ratio insights
    if ltv_cac < 1:
        insights.append({
            "type": "warning",
            "title": "LTV:CAC Below 1",
            "message": "You're spending more to acquire customers than they're worth. Focus on increasing job values or reducing marketing spend.",
        })
    elif ltv_cac < 3:
        insights.append({
            "type": "info",
            "title": "Room for Growth",
            "message": "Your LTV:CAC is healthy but could be better. A ratio of 3:1 or higher is ideal.",
        })
    elif ltv_cac >= 3:
        insights.append({
            "type": "success",
            "title": "Healthy LTV:CAC",
            "message": "Great job! Your customer value significantly exceeds acquisition cost.",
        })

    # Repeat rate insights
    if repeat_rate < 0.2:
        insights.append({
            "type": "warning",
            "title": "Low Repeat Rate",
            "message": "Only {:.0%} of customers return. Consider follow-up campaigns or loyalty programs.".format(repeat_rate),
        })
    elif repeat_rate >= 0.4:
        insights.append({
            "type": "success",
            "title": "Strong Retention",
            "message": "{:.0%} of customers are repeat buyers. Your service quality is paying off!".format(repeat_rate),
        })

    # Trend insights
    if metrics and metrics.ltvCacTrend == "up":
        insights.append({
            "type": "success",
            "title": "Improving Trend",
            "message": "Your LTV:CAC ratio is trending upward. Keep up the good work!",
        })
    elif metrics and metrics.ltvCacTrend == "down":
        insights.append({
            "type": "warning",
            "title": "Declining Trend",
            "message": "Your LTV:CAC ratio is declining. Review recent marketing spend and customer retention.",
        })

    return insights

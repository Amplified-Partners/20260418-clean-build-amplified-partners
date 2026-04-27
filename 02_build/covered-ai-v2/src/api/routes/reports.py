"""
Reports Routes - Financial reports and exports
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from typing import Optional
from datetime import datetime, timedelta, date
from decimal import Decimal
from dateutil.relativedelta import relativedelta
import csv
import io

from src.db.client import get_prisma

router = APIRouter()


@router.get("/{client_id}/cash-flow")
async def get_cash_flow_report(
    client_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db=Depends(get_prisma)
):
    """
    Get cash flow report for date range.
    Defaults to current month.
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Parse dates (default to current month)
    today = date.today()
    if start_date:
        start = datetime.fromisoformat(start_date)
    else:
        start = datetime(today.year, today.month, 1)

    if end_date:
        end = datetime.fromisoformat(end_date)
    else:
        end = datetime.now()

    # Get invoices in range
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "createdAt": {"gte": start, "lte": end},
        },
        order={"createdAt": "asc"},
    )

    # Calculate totals
    total_invoiced = sum(float(inv.amount) for inv in invoices)
    total_collected = sum(
        float(inv.amount) for inv in invoices if inv.status == "PAID"
    )
    total_outstanding = sum(
        float(inv.amount) for inv in invoices if inv.status in ["SENT", "REMINDED", "OVERDUE"]
    )
    total_cancelled = sum(
        float(inv.amount) for inv in invoices if inv.status == "CANCELLED"
    )

    # Daily breakdown
    daily_data = {}
    current = start.date()
    while current <= end.date():
        date_key = current.isoformat()
        daily_data[date_key] = {"invoiced": 0, "collected": 0}
        current += timedelta(days=1)

    for inv in invoices:
        date_key = inv.createdAt.date().isoformat()
        if date_key in daily_data:
            daily_data[date_key]["invoiced"] += float(inv.amount)
            if inv.status == "PAID":
                daily_data[date_key]["collected"] += float(inv.amount)

    # Invoice summary by status
    status_breakdown = {}
    for inv in invoices:
        status = inv.status
        if status not in status_breakdown:
            status_breakdown[status] = {"count": 0, "amount": 0}
        status_breakdown[status]["count"] += 1
        status_breakdown[status]["amount"] += float(inv.amount)

    return {
        "client_id": client_id,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "summary": {
            "total_invoiced": round(total_invoiced, 2),
            "total_collected": round(total_collected, 2),
            "total_outstanding": round(total_outstanding, 2),
            "total_cancelled": round(total_cancelled, 2),
            "collection_rate": round(
                (total_collected / total_invoiced * 100) if total_invoiced > 0 else 0, 1
            ),
            "invoice_count": len(invoices),
        },
        "status_breakdown": status_breakdown,
        "daily_data": [
            {"date": k, "invoiced": round(v["invoiced"], 2), "collected": round(v["collected"], 2)}
            for k, v in daily_data.items()
        ],
    }


@router.get("/{client_id}/cash-flow/export")
async def export_cash_flow_csv(
    client_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db=Depends(get_prisma)
):
    """
    Export cash flow report as CSV.
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Parse dates
    today = date.today()
    if start_date:
        start = datetime.fromisoformat(start_date)
    else:
        start = datetime(today.year, today.month, 1)

    if end_date:
        end = datetime.fromisoformat(end_date)
    else:
        end = datetime.now()

    # Get invoices
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "createdAt": {"gte": start, "lte": end},
        },
        order={"createdAt": "asc"},
    )

    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Invoice Number",
        "Customer Name",
        "Customer Email",
        "Amount",
        "VAT",
        "Total",
        "Status",
        "Created Date",
        "Due Date",
        "Paid Date",
    ])

    # Data rows
    vat_rate = 0.20
    for inv in invoices:
        amount = float(inv.amount)
        vat = amount * vat_rate
        total = amount + vat
        writer.writerow([
            inv.invoiceNumber,
            inv.customerName,
            inv.customerEmail,
            f"{amount:.2f}",
            f"{vat:.2f}",
            f"{total:.2f}",
            inv.status,
            inv.createdAt.strftime("%Y-%m-%d"),
            inv.dueDate.strftime("%Y-%m-%d") if inv.dueDate else "",
            inv.paidAt.strftime("%Y-%m-%d") if inv.paidAt else "",
        ])

    output.seek(0)

    filename = f"cash-flow-{start.strftime('%Y%m%d')}-{end.strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/{client_id}/vat")
async def get_vat_report(
    client_id: str,
    quarter: Optional[int] = None,
    year: Optional[int] = None,
    db=Depends(get_prisma)
):
    """
    Get VAT report for a quarter.
    Defaults to current quarter.
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Determine quarter dates
    today = date.today()
    if year is None:
        year = today.year
    if quarter is None:
        quarter = (today.month - 1) // 3 + 1

    # Quarter start/end dates
    quarter_start_month = (quarter - 1) * 3 + 1
    start = datetime(year, quarter_start_month, 1)
    end = start + relativedelta(months=3) - timedelta(days=1)
    end = datetime.combine(end.date(), datetime.max.time())

    # Get paid invoices in this quarter
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "status": "PAID",
            "paidAt": {"gte": start, "lte": end},
        },
        order={"paidAt": "asc"},
    )

    # Calculate VAT
    vat_rate = 0.20
    total_net = sum(float(inv.amount) for inv in invoices)
    total_vat = total_net * vat_rate
    total_gross = total_net + total_vat

    # Monthly breakdown
    monthly_breakdown = {}
    for month_offset in range(3):
        month_date = start + relativedelta(months=month_offset)
        month_key = month_date.strftime("%b %Y")
        monthly_breakdown[month_key] = {"net": 0, "vat": 0, "gross": 0}

    for inv in invoices:
        if inv.paidAt:
            month_key = inv.paidAt.strftime("%b %Y")
            if month_key in monthly_breakdown:
                amount = float(inv.amount)
                monthly_breakdown[month_key]["net"] += amount
                monthly_breakdown[month_key]["vat"] += amount * vat_rate
                monthly_breakdown[month_key]["gross"] += amount * (1 + vat_rate)

    return {
        "client_id": client_id,
        "quarter": quarter,
        "year": year,
        "period": f"Q{quarter} {year}",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "summary": {
            "total_net": round(total_net, 2),
            "vat_rate": vat_rate,
            "total_vat": round(total_vat, 2),
            "total_gross": round(total_gross, 2),
            "invoice_count": len(invoices),
        },
        "monthly_breakdown": [
            {
                "month": k,
                "net": round(v["net"], 2),
                "vat": round(v["vat"], 2),
                "gross": round(v["gross"], 2),
            }
            for k, v in monthly_breakdown.items()
        ],
        "vat_number": client.vatNumber,
    }


@router.get("/{client_id}/vat/export")
async def export_vat_csv(
    client_id: str,
    quarter: Optional[int] = None,
    year: Optional[int] = None,
    db=Depends(get_prisma)
):
    """
    Export VAT report as CSV.
    """
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Determine quarter dates
    today = date.today()
    if year is None:
        year = today.year
    if quarter is None:
        quarter = (today.month - 1) // 3 + 1

    quarter_start_month = (quarter - 1) * 3 + 1
    start = datetime(year, quarter_start_month, 1)
    end = start + relativedelta(months=3) - timedelta(days=1)
    end = datetime.combine(end.date(), datetime.max.time())

    # Get paid invoices
    invoices = await db.invoice.find_many(
        where={
            "clientId": client_id,
            "status": "PAID",
            "paidAt": {"gte": start, "lte": end},
        },
        order={"paidAt": "asc"},
    )

    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)

    vat_rate = 0.20

    # Header
    writer.writerow([
        "Invoice Number",
        "Customer Name",
        "Date Paid",
        "Net Amount",
        "VAT Rate",
        "VAT Amount",
        "Gross Amount",
    ])

    # Data rows
    for inv in invoices:
        amount = float(inv.amount)
        vat = amount * vat_rate
        gross = amount + vat
        writer.writerow([
            inv.invoiceNumber,
            inv.customerName,
            inv.paidAt.strftime("%Y-%m-%d") if inv.paidAt else "",
            f"{amount:.2f}",
            f"{vat_rate * 100:.0f}%",
            f"{vat:.2f}",
            f"{gross:.2f}",
        ])

    # Totals row
    total_net = sum(float(inv.amount) for inv in invoices)
    total_vat = total_net * vat_rate
    total_gross = total_net + total_vat
    writer.writerow([])
    writer.writerow([
        "TOTAL",
        "",
        "",
        f"{total_net:.2f}",
        "",
        f"{total_vat:.2f}",
        f"{total_gross:.2f}",
    ])

    output.seek(0)

    filename = f"vat-report-Q{quarter}-{year}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

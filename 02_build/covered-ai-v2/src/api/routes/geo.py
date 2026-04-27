"""
GEO Routes - Generative Engine Optimization for local SEO
Handles GEO page management, FAQ generation, and AI citation tracking.
"""
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json
import re

from src.db.client import get_prisma

router = APIRouter()


# Pydantic models
class GeoPageCreate(BaseModel):
    postcode: str
    area: Optional[str] = None
    service: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    content: Optional[str] = None
    status: str = "DRAFT"


class GeoPageUpdate(BaseModel):
    title: Optional[str] = None
    meta_description: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    schema_markup: Optional[dict] = None


class GeoFaqCreate(BaseModel):
    question: str
    answer: str
    source_type: str = "manual"  # manual, ai_generated, customer_query


class AiCitationCreate(BaseModel):
    source: str  # chatgpt, perplexity, gemini, claude
    query: str
    position: Optional[int] = None
    url: Optional[str] = None
    snippet: Optional[str] = None
    was_mentioned: bool = False


class GeneratePageRequest(BaseModel):
    postcode: str
    service: str
    area: Optional[str] = None
    include_faqs: bool = True
    num_faqs: int = 5


# Helper functions
def geo_page_to_response(page) -> dict:
    """Convert Prisma GeoPage to response dict."""
    return {
        "id": page.id,
        "client_id": page.clientId,
        "slug": page.slug,
        "postcode": page.postcode,
        "area": page.area,
        "service": page.service,
        "title": page.title,
        "meta_description": page.metaDescription,
        "content": page.content,
        "schema_markup": page.schemaMarkup,
        "status": page.status,
        "views": page.views,
        "leads_generated": page.leadsGenerated,
        "created_at": page.createdAt,
        "updated_at": page.updatedAt,
        "published_at": page.publishedAt,
    }


def geo_faq_to_response(faq) -> dict:
    """Convert Prisma GeoFaq to response dict."""
    return {
        "id": faq.id,
        "page_id": faq.pageId,
        "client_id": faq.clientId,
        "question": faq.question,
        "answer": faq.answer,
        "source_type": faq.sourceType,
        "ai_query": faq.aiQuery,
        "created_at": faq.createdAt,
    }


def ai_citation_to_response(citation) -> dict:
    """Convert Prisma AiCitation to response dict."""
    return {
        "id": citation.id,
        "client_id": citation.clientId,
        "source": citation.source,
        "query": citation.query,
        "position": citation.position,
        "url": citation.url,
        "snippet": citation.snippet,
        "was_mentioned": citation.wasMentioned,
        "checked_at": citation.checkedAt,
        "created_at": citation.createdAt,
    }


def generate_slug(postcode: str, service: str, area: Optional[str] = None) -> str:
    """Generate URL-friendly slug from postcode and service."""
    base = f"{service}-{postcode}"
    if area:
        base = f"{service}-{area}"
    # Remove special characters, lowercase, replace spaces with dashes
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', base.lower())
    slug = re.sub(r'\s+', '-', slug)
    return slug


def generate_schema_markup(page_data: dict, client_data: dict) -> dict:
    """Generate JSON-LD schema markup for a GEO page."""
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": client_data.get("businessName", ""),
        "description": page_data.get("meta_description", ""),
        "areaServed": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "postalCode": page_data.get("postcode", ""),
                "addressLocality": page_data.get("area", ""),
                "addressCountry": "GB"
            }
        },
        "serviceType": page_data.get("service", ""),
        "url": f"https://{client_data.get('businessName', '').lower().replace(' ', '')}.covered.ai/{page_data.get('slug', '')}",
    }


def generate_page_content(postcode: str, service: str, area: str, business_name: str, vertical: str) -> str:
    """Generate SEO-optimized page content. In production, this would call an AI API."""
    # Template-based generation for now
    area_name = area or postcode

    content = f"""# {service.title()} Services in {area_name}

Looking for professional {service.lower()} services in {area_name}? {business_name} provides reliable, high-quality {service.lower()} services throughout the {postcode} area.

## Why Choose {business_name}?

- **Local Expertise**: We know the {area_name} area inside out
- **Fast Response**: Same-day service available for urgent needs
- **Trusted Professionals**: Fully qualified and insured team
- **Fair Pricing**: Transparent quotes with no hidden fees

## Our {service.title()} Services

We offer a comprehensive range of {service.lower()} services in {area_name}:

- Emergency callouts and repairs
- Routine maintenance and servicing
- New installations
- Upgrades and replacements
- Free quotes and assessments

## Service Area

We cover all of {postcode} and surrounding areas including {area_name}. Whether you're in the town centre or the outskirts, we can help.

## Get in Touch

Ready to book or need a quote? Give us a call or fill out our enquiry form. We aim to respond within 15 minutes during business hours.

**Covering {postcode} | {area_name} | Available 24/7 for Emergencies**
"""
    return content


def generate_page_title(service: str, area: str, postcode: str, business_name: str) -> str:
    """Generate SEO-optimized page title."""
    area_name = area or postcode
    return f"{service.title()} in {area_name} | {business_name} | {postcode}"


def generate_meta_description(service: str, area: str, postcode: str, business_name: str) -> str:
    """Generate SEO-optimized meta description."""
    area_name = area or postcode
    return f"Professional {service.lower()} services in {area_name} ({postcode}). {business_name} offers reliable, affordable {service.lower()} with fast response times. Call now for a free quote!"


def generate_faqs(service: str, area: str, postcode: str, business_name: str, num_faqs: int = 5) -> List[dict]:
    """Generate common FAQs for the service and area."""
    area_name = area or postcode

    faq_templates = [
        {
            "question": f"How quickly can you provide {service.lower()} services in {area_name}?",
            "answer": f"We typically respond within 2 hours for standard requests and offer same-day emergency service throughout {postcode}."
        },
        {
            "question": f"How much does {service.lower()} cost in {area_name}?",
            "answer": f"Prices vary depending on the specific job. We offer free, no-obligation quotes and transparent pricing with no hidden fees."
        },
        {
            "question": f"Are your {service.lower()} professionals qualified and insured?",
            "answer": f"Yes, all our team members are fully qualified, certified, and comprehensively insured for your peace of mind."
        },
        {
            "question": f"Do you offer emergency {service.lower()} services in {postcode}?",
            "answer": f"Yes, we provide 24/7 emergency callout services throughout {area_name} and the wider {postcode} area."
        },
        {
            "question": f"What areas do you cover near {area_name}?",
            "answer": f"We cover all of {postcode} and surrounding postcodes. Contact us to confirm we service your specific location."
        },
        {
            "question": f"Can I get a free quote for {service.lower()}?",
            "answer": f"Absolutely! We provide free, no-obligation quotes for all {service.lower()} work. Call us or fill in our online form."
        },
        {
            "question": f"What payment methods do you accept?",
            "answer": f"We accept cash, card payments, and bank transfer. Payment is typically due upon completion of work."
        },
    ]

    return faq_templates[:num_faqs]


# Routes
@router.get("/pages")
async def list_geo_pages(
    client_id: str,
    status: Optional[str] = None,
    service: Optional[str] = None,
    postcode: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List GEO pages for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    where = {"clientId": client_id}

    if status:
        where["status"] = status
    if service:
        where["service"] = {"contains": service, "mode": "insensitive"}
    if postcode:
        where["postcode"] = {"contains": postcode, "mode": "insensitive"}

    pages = await db.geopage.find_many(
        where=where,
        order={"createdAt": "desc"},
        take=limit,
        skip=offset,
    )

    total = await db.geopage.count(where=where)

    return {
        "pages": [geo_page_to_response(p) for p in pages],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(pages) < total,
    }


@router.get("/pages/stats")
async def get_geo_stats(
    client_id: str,
    db=Depends(get_prisma)
):
    """Get GEO page statistics for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Count pages by status
    total_pages = await db.geopage.count(where={"clientId": client_id})
    published_pages = await db.geopage.count(where={"clientId": client_id, "status": "PUBLISHED"})
    draft_pages = await db.geopage.count(where={"clientId": client_id, "status": "DRAFT"})

    # Get total views and leads
    pages = await db.geopage.find_many(where={"clientId": client_id})
    total_views = sum(p.views for p in pages)
    total_leads = sum(p.leadsGenerated for p in pages)

    # Get citation stats
    total_citations = await db.aicitation.count(where={"clientId": client_id})
    mentioned_citations = await db.aicitation.count(where={"clientId": client_id, "wasMentioned": True})

    # Get FAQ count
    total_faqs = await db.geofaq.count(where={"clientId": client_id})

    # Get unique services and postcodes
    unique_services = len(set(p.service for p in pages))
    unique_postcodes = len(set(p.postcode for p in pages))

    return {
        "total_pages": total_pages,
        "published_pages": published_pages,
        "draft_pages": draft_pages,
        "total_views": total_views,
        "total_leads": total_leads,
        "total_faqs": total_faqs,
        "total_citations": total_citations,
        "mentioned_citations": mentioned_citations,
        "unique_services": unique_services,
        "unique_postcodes": unique_postcodes,
        "mention_rate": round(mentioned_citations / total_citations * 100, 1) if total_citations > 0 else 0,
    }


@router.get("/pages/{page_id}")
async def get_geo_page(
    client_id: str,
    page_id: str,
    db=Depends(get_prisma)
):
    """Get a single GEO page with its FAQs."""
    page = await db.geopage.find_unique(
        where={"id": page_id},
        include={"faqs": True}
    )

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    response = geo_page_to_response(page)
    response["faqs"] = [geo_faq_to_response(f) for f in page.faqs] if page.faqs else []

    return response


@router.post("/pages")
async def create_geo_page(
    client_id: str,
    page_data: GeoPageCreate,
    db=Depends(get_prisma)
):
    """Create a new GEO page."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Generate slug
    slug = generate_slug(page_data.postcode, page_data.service, page_data.area)

    # Check if slug already exists for this client
    existing = await db.geopage.find_first(
        where={"clientId": client_id, "slug": slug}
    )
    if existing:
        raise HTTPException(status_code=400, detail=f"Page with slug '{slug}' already exists")

    # Generate content if not provided
    title = page_data.title or generate_page_title(
        page_data.service, page_data.area, page_data.postcode, client.businessName
    )
    meta_description = page_data.meta_description or generate_meta_description(
        page_data.service, page_data.area, page_data.postcode, client.businessName
    )
    content = page_data.content or generate_page_content(
        page_data.postcode, page_data.service, page_data.area or page_data.postcode,
        client.businessName, client.vertical or "trades"
    )

    # Generate schema markup
    schema_data = {
        "postcode": page_data.postcode,
        "area": page_data.area,
        "service": page_data.service,
        "slug": slug,
        "meta_description": meta_description,
    }
    client_data = {
        "businessName": client.businessName,
    }
    schema_markup = generate_schema_markup(schema_data, client_data)

    page = await db.geopage.create(
        data={
            "clientId": client_id,
            "slug": slug,
            "postcode": page_data.postcode,
            "area": page_data.area,
            "service": page_data.service,
            "title": title,
            "metaDescription": meta_description,
            "content": content,
            "schemaMarkup": json.dumps(schema_markup),
            "status": page_data.status,
        }
    )

    return {
        "id": page.id,
        "message": "GEO page created",
        **geo_page_to_response(page)
    }


@router.post("/pages/generate")
async def generate_geo_page(
    client_id: str,
    request: GeneratePageRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_prisma)
):
    """Generate a complete GEO page with AI content and FAQs."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Generate slug
    slug = generate_slug(request.postcode, request.service, request.area)

    # Check if slug already exists
    existing = await db.geopage.find_first(
        where={"clientId": client_id, "slug": slug}
    )
    if existing:
        raise HTTPException(status_code=400, detail=f"Page with slug '{slug}' already exists")

    # Generate all content
    area_name = request.area or request.postcode
    title = generate_page_title(request.service, area_name, request.postcode, client.businessName)
    meta_description = generate_meta_description(request.service, area_name, request.postcode, client.businessName)
    content = generate_page_content(
        request.postcode, request.service, area_name,
        client.businessName, client.vertical or "trades"
    )

    # Generate schema markup
    schema_data = {
        "postcode": request.postcode,
        "area": request.area,
        "service": request.service,
        "slug": slug,
        "meta_description": meta_description,
    }
    client_data = {"businessName": client.businessName}
    schema_markup = generate_schema_markup(schema_data, client_data)

    # Create the page
    page = await db.geopage.create(
        data={
            "clientId": client_id,
            "slug": slug,
            "postcode": request.postcode,
            "area": request.area,
            "service": request.service,
            "title": title,
            "metaDescription": meta_description,
            "content": content,
            "schemaMarkup": json.dumps(schema_markup),
            "status": "DRAFT",
        }
    )

    # Generate and create FAQs
    faqs_created = []
    if request.include_faqs:
        faq_data = generate_faqs(
            request.service, area_name, request.postcode,
            client.businessName, request.num_faqs
        )

        for faq in faq_data:
            created_faq = await db.geofaq.create(
                data={
                    "pageId": page.id,
                    "clientId": client_id,
                    "question": faq["question"],
                    "answer": faq["answer"],
                    "sourceType": "ai_generated",
                }
            )
            faqs_created.append(geo_faq_to_response(created_faq))

    response = geo_page_to_response(page)
    response["faqs"] = faqs_created

    return {
        "id": page.id,
        "message": "GEO page generated successfully",
        **response
    }


@router.patch("/pages/{page_id}")
async def update_geo_page(
    client_id: str,
    page_id: str,
    page_data: GeoPageUpdate,
    db=Depends(get_prisma)
):
    """Update a GEO page."""
    page = await db.geopage.find_unique(where={"id": page_id})

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    update_data = {}

    if page_data.title is not None:
        update_data["title"] = page_data.title
    if page_data.meta_description is not None:
        update_data["metaDescription"] = page_data.meta_description
    if page_data.content is not None:
        update_data["content"] = page_data.content
    if page_data.schema_markup is not None:
        update_data["schemaMarkup"] = json.dumps(page_data.schema_markup)
    if page_data.status is not None:
        update_data["status"] = page_data.status
        if page_data.status == "PUBLISHED" and not page.publishedAt:
            update_data["publishedAt"] = datetime.utcnow()

    updated = await db.geopage.update(
        where={"id": page_id},
        data=update_data
    )

    return {
        "id": page_id,
        "message": "GEO page updated",
        **geo_page_to_response(updated)
    }


@router.delete("/pages/{page_id}")
async def delete_geo_page(
    client_id: str,
    page_id: str,
    db=Depends(get_prisma)
):
    """Delete a GEO page and its FAQs."""
    page = await db.geopage.find_unique(where={"id": page_id})

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    # Delete FAQs first
    await db.geofaq.delete_many(where={"pageId": page_id})

    # Delete the page
    await db.geopage.delete(where={"id": page_id})

    return {"message": "GEO page deleted", "id": page_id}


@router.post("/pages/{page_id}/publish")
async def publish_geo_page(
    client_id: str,
    page_id: str,
    db=Depends(get_prisma)
):
    """Publish a GEO page."""
    page = await db.geopage.find_unique(where={"id": page_id})

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    updated = await db.geopage.update(
        where={"id": page_id},
        data={
            "status": "PUBLISHED",
            "publishedAt": datetime.utcnow(),
        }
    )

    return {
        "id": page_id,
        "message": "GEO page published",
        "status": "PUBLISHED",
        "published_at": updated.publishedAt,
    }


@router.post("/pages/{page_id}/track-view")
async def track_page_view(
    client_id: str,
    page_id: str,
    db=Depends(get_prisma)
):
    """Track a view on a GEO page."""
    page = await db.geopage.find_unique(where={"id": page_id})

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    await db.geopage.update(
        where={"id": page_id},
        data={"views": {"increment": 1}}
    )

    return {"message": "View tracked", "views": page.views + 1}


@router.post("/pages/{page_id}/track-lead")
async def track_page_lead(
    client_id: str,
    page_id: str,
    db=Depends(get_prisma)
):
    """Track a lead generated from a GEO page."""
    page = await db.geopage.find_unique(where={"id": page_id})

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    await db.geopage.update(
        where={"id": page_id},
        data={"leadsGenerated": {"increment": 1}}
    )

    return {"message": "Lead tracked", "leads_generated": page.leadsGenerated + 1}


# FAQ Routes
@router.get("/pages/{page_id}/faqs")
async def list_page_faqs(
    client_id: str,
    page_id: str,
    db=Depends(get_prisma)
):
    """List FAQs for a GEO page."""
    page = await db.geopage.find_unique(where={"id": page_id})

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    faqs = await db.geofaq.find_many(
        where={"pageId": page_id},
        order={"createdAt": "asc"}
    )

    return {
        "page_id": page_id,
        "faqs": [geo_faq_to_response(f) for f in faqs],
        "total": len(faqs),
    }


@router.post("/pages/{page_id}/faqs")
async def add_page_faq(
    client_id: str,
    page_id: str,
    faq_data: GeoFaqCreate,
    db=Depends(get_prisma)
):
    """Add a FAQ to a GEO page."""
    page = await db.geopage.find_unique(where={"id": page_id})

    if not page or page.clientId != client_id:
        raise HTTPException(status_code=404, detail="GEO page not found")

    faq = await db.geofaq.create(
        data={
            "pageId": page_id,
            "clientId": client_id,
            "question": faq_data.question,
            "answer": faq_data.answer,
            "sourceType": faq_data.source_type,
        }
    )

    return {
        "id": faq.id,
        "message": "FAQ added",
        **geo_faq_to_response(faq)
    }


@router.delete("/pages/{page_id}/faqs/{faq_id}")
async def delete_page_faq(
    client_id: str,
    page_id: str,
    faq_id: str,
    db=Depends(get_prisma)
):
    """Delete a FAQ from a GEO page."""
    faq = await db.geofaq.find_unique(where={"id": faq_id})

    if not faq or faq.clientId != client_id or faq.pageId != page_id:
        raise HTTPException(status_code=404, detail="FAQ not found")

    await db.geofaq.delete(where={"id": faq_id})

    return {"message": "FAQ deleted", "id": faq_id}


# AI Citation Routes
@router.get("/citations")
async def list_citations(
    client_id: str,
    source: Optional[str] = None,
    mentioned_only: bool = False,
    limit: int = 50,
    offset: int = 0,
    db=Depends(get_prisma)
):
    """List AI citations for a client."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    where = {"clientId": client_id}

    if source:
        where["source"] = source
    if mentioned_only:
        where["wasMentioned"] = True

    citations = await db.aicitation.find_many(
        where=where,
        order={"checkedAt": "desc"},
        take=limit,
        skip=offset,
    )

    total = await db.aicitation.count(where=where)

    return {
        "citations": [ai_citation_to_response(c) for c in citations],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(citations) < total,
    }


@router.post("/citations")
async def create_citation(
    client_id: str,
    citation_data: AiCitationCreate,
    db=Depends(get_prisma)
):
    """Record an AI citation check."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    citation = await db.aicitation.create(
        data={
            "clientId": client_id,
            "source": citation_data.source,
            "query": citation_data.query,
            "position": citation_data.position,
            "url": citation_data.url,
            "snippet": citation_data.snippet,
            "wasMentioned": citation_data.was_mentioned,
            "checkedAt": datetime.utcnow(),
        }
    )

    return {
        "id": citation.id,
        "message": "Citation recorded",
        **ai_citation_to_response(citation)
    }


@router.get("/citations/stats")
async def get_citation_stats(
    client_id: str,
    db=Depends(get_prisma)
):
    """Get AI citation statistics."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    citations = await db.aicitation.find_many(where={"clientId": client_id})

    # Calculate stats by source
    source_stats = {}
    for citation in citations:
        if citation.source not in source_stats:
            source_stats[citation.source] = {"total": 0, "mentioned": 0}
        source_stats[citation.source]["total"] += 1
        if citation.wasMentioned:
            source_stats[citation.source]["mentioned"] += 1

    # Calculate mention rates
    for source in source_stats:
        total = source_stats[source]["total"]
        mentioned = source_stats[source]["mentioned"]
        source_stats[source]["mention_rate"] = round(mentioned / total * 100, 1) if total > 0 else 0

    total_citations = len(citations)
    total_mentioned = sum(1 for c in citations if c.wasMentioned)

    return {
        "total_citations": total_citations,
        "total_mentioned": total_mentioned,
        "overall_mention_rate": round(total_mentioned / total_citations * 100, 1) if total_citations > 0 else 0,
        "by_source": source_stats,
    }


# Bulk Operations
@router.post("/pages/bulk-generate")
async def bulk_generate_pages(
    client_id: str,
    postcodes: List[str],
    services: List[str],
    include_faqs: bool = True,
    db=Depends(get_prisma)
):
    """Bulk generate GEO pages for multiple postcodes and services."""
    client = await db.client.find_unique(where={"id": client_id})
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    if len(postcodes) * len(services) > 50:
        raise HTTPException(
            status_code=400,
            detail="Maximum 50 pages can be generated at once"
        )

    created_pages = []
    skipped = []

    for postcode in postcodes:
        for service in services:
            slug = generate_slug(postcode, service)

            # Check if exists
            existing = await db.geopage.find_first(
                where={"clientId": client_id, "slug": slug}
            )
            if existing:
                skipped.append({"postcode": postcode, "service": service, "reason": "already_exists"})
                continue

            # Generate content
            title = generate_page_title(service, None, postcode, client.businessName)
            meta_description = generate_meta_description(service, None, postcode, client.businessName)
            content = generate_page_content(
                postcode, service, postcode,
                client.businessName, client.vertical or "trades"
            )

            schema_data = {
                "postcode": postcode,
                "area": None,
                "service": service,
                "slug": slug,
                "meta_description": meta_description,
            }
            schema_markup = generate_schema_markup(schema_data, {"businessName": client.businessName})

            # Create page
            page = await db.geopage.create(
                data={
                    "clientId": client_id,
                    "slug": slug,
                    "postcode": postcode,
                    "service": service,
                    "title": title,
                    "metaDescription": meta_description,
                    "content": content,
                    "schemaMarkup": json.dumps(schema_markup),
                    "status": "DRAFT",
                }
            )

            # Generate FAQs
            if include_faqs:
                faq_data = generate_faqs(service, postcode, postcode, client.businessName, 5)
                for faq in faq_data:
                    await db.geofaq.create(
                        data={
                            "pageId": page.id,
                            "clientId": client_id,
                            "question": faq["question"],
                            "answer": faq["answer"],
                            "sourceType": "ai_generated",
                        }
                    )

            created_pages.append({
                "id": page.id,
                "slug": slug,
                "postcode": postcode,
                "service": service,
            })

    return {
        "message": f"Bulk generation complete",
        "created": len(created_pages),
        "skipped": len(skipped),
        "pages": created_pages,
        "skipped_details": skipped,
    }


# ============================================================================
# PUBLIC ROUTES (No authentication required)
# ============================================================================

@router.get("/public/{slug}")
async def get_public_geo_page(
    slug: str,
    db=Depends(get_prisma)
):
    """Get a published GEO page by slug (public endpoint)."""
    page = await db.geopage.find_first(
        where={"slug": slug, "status": "PUBLISHED"},
        include={"faqs": True}
    )

    if not page:
        raise HTTPException(status_code=404, detail="Page not found")

    # Get client info for business details
    client = await db.client.find_unique(where={"id": page.clientId})
    if not client:
        raise HTTPException(status_code=404, detail="Business not found")

    # Increment view count in background
    await db.geopage.update(
        where={"id": page.id},
        data={
            "views": {"increment": 1},
            "lastViewedAt": datetime.utcnow(),
        }
    )

    # Build public response
    return {
        "id": page.id,
        "slug": page.slug,
        "title": page.title,
        "meta_description": page.metaDescription,
        "content": page.content,
        "postcode": page.postcode,
        "area": page.area,
        "service": page.service,
        "schema_markup": json.loads(page.schemaMarkup) if page.schemaMarkup else None,
        "faqs": [
            {
                "question": faq.question,
                "answer": faq.answer,
            }
            for faq in (page.faqs or [])
        ],
        "business": {
            "name": client.businessName,
            "phone": client.coveredNumber or client.phone,
            "email": client.email,
            "vertical": client.vertical,
        },
        "published_at": page.publishedAt,
    }


@router.get("/public/business/{business_slug}")
async def list_business_geo_pages(
    business_slug: str,
    limit: int = 20,
    db=Depends(get_prisma)
):
    """List all published GEO pages for a business (by business name slug)."""
    # First find the client by slugified business name
    clients = await db.client.find_many()
    client = None
    for c in clients:
        if generate_slug("", c.businessName, None).replace("-", "") == business_slug.replace("-", ""):
            client = c
            break

    if not client:
        raise HTTPException(status_code=404, detail="Business not found")

    pages = await db.geopage.find_many(
        where={"clientId": client.id, "status": "PUBLISHED"},
        order={"createdAt": "desc"},
        take=limit,
    )

    return {
        "business": {
            "name": client.businessName,
            "vertical": client.vertical,
        },
        "pages": [
            {
                "id": p.id,
                "slug": p.slug,
                "title": p.title,
                "postcode": p.postcode,
                "area": p.area,
                "service": p.service,
            }
            for p in pages
        ],
        "total": len(pages),
    }

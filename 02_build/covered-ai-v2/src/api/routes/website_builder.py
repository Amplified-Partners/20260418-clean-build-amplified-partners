"""
Website Builder API Routes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

from src.services.website_builder.engine import (
    website_builder,
    ClientInput,
    Vertical,
)

router = APIRouter(prefix="/website-builder", tags=["website-builder"])


class WebsiteRequest(BaseModel):
    business_name: str
    vertical: str
    location: str
    phone: str
    email: EmailStr
    tagline: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    staff_photos: List[str] = []
    services: List[str] = []
    existing_website: Optional[str] = None


class WebsiteStatusResponse(BaseModel):
    client_id: str
    status: str
    pages: List[str] = []
    deploy_url: Optional[str] = None
    message: Optional[str] = None


class PagePreviewResponse(BaseModel):
    html: str


class VerticalsResponse(BaseModel):
    verticals: List[str]
    default: str


class ColorPreset(BaseModel):
    primary: str
    name: str


class ColorPresetsResponse(BaseModel):
    presets: Dict[str, ColorPreset]


# Store generation results (in production, use Redis or database)
generation_results: Dict[str, Any] = {}
generation_status: Dict[str, str] = {}


@router.post("/generate/{client_id}", response_model=WebsiteStatusResponse)
async def generate_website(
    client_id: str,
    request: WebsiteRequest,
    background_tasks: BackgroundTasks,
):
    """
    Generate a complete website for a client.
    Runs in background, poll /status for completion.
    """
    try:
        vertical = Vertical(request.vertical)
    except ValueError:
        vertical = Vertical.OTHER

    input_data = ClientInput(
        business_name=request.business_name,
        vertical=vertical,
        location=request.location,
        phone=request.phone,
        email=request.email,
        tagline=request.tagline,
        description=request.description,
        logo_url=request.logo_url,
        primary_color=request.primary_color,
        staff_photos=request.staff_photos,
        services=request.services,
        existing_website=request.existing_website,
    )

    async def run_generation():
        try:
            generation_status[client_id] = "generating"
            result = await website_builder.generate(client_id, input_data)
            generation_results[client_id] = result
            generation_status[client_id] = "completed"
        except Exception as e:
            generation_status[client_id] = f"failed: {str(e)}"

    generation_status[client_id] = "queued"
    background_tasks.add_task(run_generation)

    return WebsiteStatusResponse(
        client_id=client_id,
        status="generating",
        message="Website generation started. Poll /status for completion.",
    )


@router.get("/status/{client_id}", response_model=WebsiteStatusResponse)
async def get_generation_status(client_id: str):
    """Check website generation status."""
    status = generation_status.get(client_id, "not_found")

    if client_id in generation_results:
        result = generation_results[client_id]
        return WebsiteStatusResponse(
            client_id=client_id,
            status="completed",
            pages=list(result.pages.keys()),
            deploy_url=result.deploy_url,
        )

    if status.startswith("failed"):
        return WebsiteStatusResponse(
            client_id=client_id,
            status="failed",
            message=status,
        )

    return WebsiteStatusResponse(
        client_id=client_id,
        status=status,
    )


@router.get("/preview/{client_id}/{page}", response_model=PagePreviewResponse)
async def preview_page(client_id: str, page: str):
    """Preview a generated page."""
    if client_id not in generation_results:
        raise HTTPException(status_code=404, detail="Website not found")

    result = generation_results[client_id]

    if page not in result.pages:
        raise HTTPException(status_code=404, detail="Page not found")

    return PagePreviewResponse(html=result.pages[page])


@router.get("/pages/{client_id}")
async def list_pages(client_id: str):
    """List all generated pages for a client."""
    if client_id not in generation_results:
        raise HTTPException(status_code=404, detail="Website not found")

    result = generation_results[client_id]

    return {
        "client_id": client_id,
        "pages": list(result.pages.keys()),
        "sitemap": result.sitemap,
        "robots_txt": result.robots_txt,
    }


@router.get("/schema/{client_id}")
async def get_schema_markup(client_id: str):
    """Get the schema.org markup for a generated website."""
    if client_id not in generation_results:
        raise HTTPException(status_code=404, detail="Website not found")

    result = generation_results[client_id]

    return {
        "client_id": client_id,
        "schema_markup": result.schema_markup,
        "llm_context": result.llm_context,
    }


@router.get("/verticals", response_model=VerticalsResponse)
async def list_verticals():
    """List available business verticals."""
    return VerticalsResponse(
        verticals=[v.value for v in Vertical],
        default=Vertical.OTHER.value,
    )


@router.get("/color-presets", response_model=ColorPresetsResponse)
async def get_color_presets():
    """Get color presets for each vertical."""
    return ColorPresetsResponse(
        presets={
            "plumber": ColorPreset(primary="#2563eb", name="Professional Blue"),
            "electrician": ColorPreset(primary="#f59e0b", name="Safety Amber"),
            "salon": ColorPreset(primary="#ec4899", name="Elegant Pink"),
            "vet": ColorPreset(primary="#10b981", name="Calming Green"),
            "dental": ColorPreset(primary="#06b6d4", name="Clean Cyan"),
            "physio": ColorPreset(primary="#8b5cf6", name="Healing Purple"),
            "trades": ColorPreset(primary="#f97316", name="Bold Orange"),
            "other": ColorPreset(primary="#2563eb", name="Professional Blue"),
        }
    )


@router.delete("/cache/{client_id}")
async def clear_cache(client_id: str):
    """Clear cached website for a client (allows regeneration)."""
    if client_id in generation_results:
        del generation_results[client_id]
    if client_id in generation_status:
        del generation_status[client_id]

    return {"message": f"Cache cleared for client {client_id}"}

"""
Photo Studio API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from src.services.photo_studio.processor import (
    photo_processor,
    image_generator,
    OutputFormat,
)

router = APIRouter(prefix="/photo-studio", tags=["photo-studio"])


class ProcessHeadshotRequest(BaseModel):
    photo_url: str
    brand_color: Optional[str] = None
    output_format: str = "web"


class ProcessTeamRequest(BaseModel):
    photo_urls: List[str]
    brand_color: Optional[str] = None


class GenerateHeroRequest(BaseModel):
    vertical: str
    location: str
    style: str = "professional"


class GenerateStaffRequest(BaseModel):
    gender: str = "neutral"
    role: str = "professional"
    style: str = "friendly"


class GenerateServiceRequest(BaseModel):
    service_name: str
    vertical: str


class ProcessedPhotoResponse(BaseModel):
    original_url: str
    processed_url: str
    thumbnail_url: str
    width: int
    height: int
    processing_applied: List[str]


class GeneratedPhotoResponse(BaseModel):
    url: str
    prompt: str
    width: int
    height: int


@router.post("/process/headshot", response_model=ProcessedPhotoResponse)
async def process_headshot(request: ProcessHeadshotRequest):
    """Process a single headshot photo."""
    try:
        output_format = OutputFormat(request.output_format)
    except ValueError:
        output_format = OutputFormat.WEB

    try:
        result = await photo_processor.process_headshot(
            photo_url=request.photo_url,
            brand_color=request.brand_color,
            output_format=output_format,
        )

        return ProcessedPhotoResponse(
            original_url=result.original_url,
            processed_url=result.processed_url,
            thumbnail_url=result.thumbnail_url,
            width=result.width,
            height=result.height,
            processing_applied=result.processing_applied,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process photo: {str(e)}")


@router.post("/process/team")
async def process_team_photos(request: ProcessTeamRequest):
    """Process multiple team photos with consistent styling."""
    results = await photo_processor.process_team_photos(
        photo_urls=request.photo_urls,
        brand_color=request.brand_color,
    )

    return {
        "processed": len(results),
        "photos": [
            {
                "original_url": r.original_url,
                "processed_url": r.processed_url,
                "thumbnail_url": r.thumbnail_url,
            }
            for r in results
        ]
    }


@router.post("/generate/hero", response_model=GeneratedPhotoResponse)
async def generate_hero_image(request: GenerateHeroRequest):
    """Generate a hero image for the business."""
    result = await image_generator.generate_hero_image(
        vertical=request.vertical,
        location=request.location,
        style=request.style,
    )

    return GeneratedPhotoResponse(
        url=result.url,
        prompt=result.prompt,
        width=result.width,
        height=result.height,
    )


@router.post("/generate/staff", response_model=GeneratedPhotoResponse)
async def generate_staff_placeholder(request: GenerateStaffRequest):
    """Generate a placeholder staff photo."""
    result = await image_generator.generate_staff_placeholder(
        gender=request.gender,
        role=request.role,
        style=request.style,
    )

    return GeneratedPhotoResponse(
        url=result.url,
        prompt=result.prompt,
        width=result.width,
        height=result.height,
    )


@router.post("/generate/service", response_model=GeneratedPhotoResponse)
async def generate_service_image(request: GenerateServiceRequest):
    """Generate an image for a specific service."""
    result = await image_generator.generate_service_image(
        service_name=request.service_name,
        vertical=request.vertical,
    )

    return GeneratedPhotoResponse(
        url=result.url,
        prompt=result.prompt,
        width=result.width,
        height=result.height,
    )


@router.get("/formats")
async def list_output_formats():
    """List available output formats."""
    return {
        "formats": [
            {"id": "web", "size": "800x800", "use": "Website display"},
            {"id": "social", "size": "1200x1200", "use": "Social media"},
            {"id": "thumbnail", "size": "200x200", "use": "Previews"},
            {"id": "print", "size": "2400x2400", "use": "Print materials"},
        ]
    }


@router.get("/verticals")
async def list_verticals():
    """List verticals with available hero image presets."""
    return {
        "verticals": [
            {"id": "plumber", "name": "Plumber", "has_hero_preset": True},
            {"id": "electrician", "name": "Electrician", "has_hero_preset": True},
            {"id": "salon", "name": "Salon", "has_hero_preset": True},
            {"id": "vet", "name": "Veterinarian", "has_hero_preset": True},
            {"id": "dental", "name": "Dental", "has_hero_preset": True},
            {"id": "physio", "name": "Physiotherapist", "has_hero_preset": True},
            {"id": "trades", "name": "General Trades", "has_hero_preset": False},
            {"id": "other", "name": "Other", "has_hero_preset": False},
        ]
    }

"""
AI Photo Studio - Process and generate professional photos

Uses:
- Replicate API for face enhancement and background removal
- OpenAI DALL-E 3 for image generation
- PIL for image manipulation
"""

import os
import io
import base64
import asyncio
import uuid
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum
import httpx
from PIL import Image

REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")


class PhotoType(str, Enum):
    HEADSHOT = "headshot"
    TEAM = "team"
    ACTION = "action"
    SERVICE = "service"
    HERO = "hero"


class OutputFormat(str, Enum):
    WEB = "web"  # 800x800, optimized
    SOCIAL = "social"  # 1200x1200
    THUMBNAIL = "thumbnail"  # 200x200
    PRINT = "print"  # 2400x2400, high quality


@dataclass
class ProcessedPhoto:
    original_url: str
    processed_url: str
    thumbnail_url: str
    format: OutputFormat
    width: int
    height: int
    file_size: int
    processing_applied: List[str]


@dataclass
class GeneratedPhoto:
    prompt: str
    url: str
    width: int
    height: int


class PhotoProcessor:
    """
    Process photos with AI enhancement.
    """

    def __init__(self):
        self.http = httpx.AsyncClient(timeout=120.0)

    async def process_headshot(
        self,
        photo_url: str,
        brand_color: Optional[str] = None,
        output_format: OutputFormat = OutputFormat.WEB,
    ) -> ProcessedPhoto:
        """
        Process a staff headshot photo.

        Steps:
        1. Download original
        2. Remove background
        3. Enhance face (subtle)
        4. Add brand-colored background
        5. Crop to headshot frame
        6. Resize for output format
        """
        processing_applied = []

        # Download original
        original_image = await self._download_image(photo_url)

        # Remove background
        no_bg_image = await self._remove_background(original_image)
        processing_applied.append("background_removed")

        # Enhance face
        enhanced_image = await self._enhance_face(no_bg_image)
        processing_applied.append("face_enhanced")

        # Add background color
        bg_color = brand_color or "#f3f4f6"  # Light gray default
        with_bg = self._add_solid_background(enhanced_image, bg_color)
        processing_applied.append(f"background_color:{bg_color}")

        # Crop to headshot
        cropped = self._crop_to_headshot(with_bg)
        processing_applied.append("cropped_headshot")

        # Resize for format
        final = self._resize_for_format(cropped, output_format)
        processing_applied.append(f"resized:{output_format.value}")

        # Upload and get URLs
        processed_url = await self._upload_image(final, "processed")
        thumbnail = self._resize_for_format(final, OutputFormat.THUMBNAIL)
        thumbnail_url = await self._upload_image(thumbnail, "thumbnail")

        return ProcessedPhoto(
            original_url=photo_url,
            processed_url=processed_url,
            thumbnail_url=thumbnail_url,
            format=output_format,
            width=final.width,
            height=final.height,
            file_size=self._get_file_size(final),
            processing_applied=processing_applied,
        )

    async def process_team_photos(
        self,
        photo_urls: List[str],
        brand_color: Optional[str] = None,
    ) -> List[ProcessedPhoto]:
        """
        Process multiple team photos with consistent styling.
        """
        results = []
        for url in photo_urls:
            try:
                processed = await self.process_headshot(url, brand_color)
                results.append(processed)
            except Exception as e:
                print(f"Failed to process {url}: {e}")
                # Continue with others

        return results

    async def _download_image(self, url: str) -> Image.Image:
        """Download image from URL."""
        response = await self.http.get(url)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))

    async def _remove_background(self, image: Image.Image) -> Image.Image:
        """Remove background using remove.bg API or Replicate."""
        if REMOVE_BG_API_KEY:
            # Use remove.bg API
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            response = await self.http.post(
                "https://api.remove.bg/v1.0/removebg",
                headers={"X-Api-Key": REMOVE_BG_API_KEY},
                files={"image_file": img_bytes},
                data={"size": "auto"},
            )
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))

        elif REPLICATE_API_KEY:
            # Use Replicate background removal model
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()

            response = await self.http.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {REPLICATE_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "version": "fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003",  # rembg model
                    "input": {
                        "image": f"data:image/png;base64,{img_base64}"
                    }
                }
            )
            response.raise_for_status()

            # Poll for result
            prediction = response.json()
            result_url = await self._wait_for_replicate(prediction["id"])

            return await self._download_image(result_url)

        else:
            # Return original if no API available
            return image

    async def _enhance_face(self, image: Image.Image) -> Image.Image:
        """Enhance face using AI (subtle improvements)."""
        if not REPLICATE_API_KEY:
            return image

        try:
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()

            response = await self.http.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {REPLICATE_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "version": "9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",  # GFPGAN
                    "input": {
                        "img": f"data:image/png;base64,{img_base64}",
                        "scale": 2,
                        "version": "v1.4",
                    }
                }
            )
            response.raise_for_status()

            prediction = response.json()
            result_url = await self._wait_for_replicate(prediction["id"])

            return await self._download_image(result_url)
        except Exception:
            # Return original if enhancement fails
            return image

    async def _wait_for_replicate(self, prediction_id: str, max_wait: int = 60) -> str:
        """Wait for Replicate prediction to complete."""
        for _ in range(max_wait):
            response = await self.http.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers={"Authorization": f"Token {REPLICATE_API_KEY}"},
            )
            result = response.json()

            if result["status"] == "succeeded":
                return result["output"]
            elif result["status"] == "failed":
                raise Exception(f"Replicate prediction failed: {result.get('error')}")

            await asyncio.sleep(1)

        raise Exception("Replicate prediction timed out")

    def _add_solid_background(self, image: Image.Image, color: str) -> Image.Image:
        """Add solid color background to transparent image."""
        # Parse hex color
        if color.startswith('#'):
            color = color[1:]
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        # Create background
        bg = Image.new('RGBA', image.size, (r, g, b, 255))

        # Composite
        if image.mode == 'RGBA':
            bg.paste(image, (0, 0), image)
        else:
            bg.paste(image, (0, 0))

        return bg.convert('RGB')

    def _crop_to_headshot(self, image: Image.Image) -> Image.Image:
        """Crop image to professional headshot framing."""
        width, height = image.size

        # Detect face center (simplified - assumes centered)
        # In production, use face detection

        # Aim for 3:4 aspect ratio (portrait)
        target_ratio = 3 / 4
        current_ratio = width / height

        if current_ratio > target_ratio:
            # Too wide - crop sides
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            image = image.crop((left, 0, left + new_width, height))
        else:
            # Too tall - crop top/bottom (keep more top for headroom)
            new_height = int(width / target_ratio)
            top = int((height - new_height) * 0.3)  # Keep more top
            image = image.crop((0, top, width, top + new_height))

        return image

    def _resize_for_format(self, image: Image.Image, format: OutputFormat) -> Image.Image:
        """Resize image for output format."""
        sizes = {
            OutputFormat.WEB: (800, 800),
            OutputFormat.SOCIAL: (1200, 1200),
            OutputFormat.THUMBNAIL: (200, 200),
            OutputFormat.PRINT: (2400, 2400),
        }

        target_size = sizes[format]

        # Make a copy to avoid modifying original
        img_copy = image.copy()

        # Maintain aspect ratio, fit within bounds
        img_copy.thumbnail(target_size, Image.Resampling.LANCZOS)

        return img_copy

    async def _upload_image(self, image: Image.Image, prefix: str) -> str:
        """Upload image and return URL."""
        # TODO: Implement upload to S3/Cloudflare/etc.
        # For now, return a placeholder
        return f"https://covered-ai-assets.s3.amazonaws.com/{prefix}_{uuid.uuid4().hex[:8]}.jpg"

    def _get_file_size(self, image: Image.Image) -> int:
        """Get image file size in bytes."""
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG', quality=85)
        return img_bytes.tell()


class ImageGenerator:
    """
    Generate images using AI.
    """

    def __init__(self):
        self.http = httpx.AsyncClient(timeout=60.0)

    async def generate_hero_image(
        self,
        vertical: str,
        location: str,
        style: str = "professional",
    ) -> GeneratedPhoto:
        """Generate a hero image for the business."""
        prompts = {
            "plumber": f"Professional plumber working on pipes in a modern kitchen, friendly smile, UK home setting, natural lighting, high quality photo",
            "electrician": f"Professional electrician checking electrical panel, safety gear, focused work, modern UK home, professional photography",
            "salon": f"Beautiful modern hair salon interior, styling chairs, warm lighting, professional atmosphere, UK high street",
            "vet": f"Friendly veterinarian with a happy dog in a clean modern clinic, warm caring atmosphere, professional photo",
            "dental": f"Modern dental clinic interior, clean white aesthetic, professional equipment, welcoming atmosphere",
            "physio": f"Professional physiotherapist helping patient with exercise, modern clinic, caring professional atmosphere",
        }

        prompt = prompts.get(vertical, f"Professional {vertical} at work, friendly, trustworthy, UK setting")

        if not OPENAI_API_KEY:
            # Return placeholder if no API key
            return GeneratedPhoto(
                prompt=prompt,
                url="https://via.placeholder.com/1792x1024/2563eb/ffffff?text=Hero+Image",
                width=1792,
                height=1024,
            )

        try:
            response = await self.http.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1792x1024",
                    "quality": "standard",
                }
            )
            response.raise_for_status()

            result = response.json()
            image_url = result["data"][0]["url"]

            return GeneratedPhoto(
                prompt=prompt,
                url=image_url,
                width=1792,
                height=1024,
            )
        except Exception:
            return GeneratedPhoto(
                prompt=prompt,
                url="https://via.placeholder.com/1792x1024/2563eb/ffffff?text=Hero+Image",
                width=1792,
                height=1024,
            )

    async def generate_staff_placeholder(
        self,
        gender: str = "neutral",
        role: str = "professional",
        style: str = "friendly",
    ) -> GeneratedPhoto:
        """Generate a placeholder staff photo."""
        prompt = f"Professional headshot of a friendly {gender} {role}, neutral background, warm lighting, trustworthy appearance, UK professional"

        if not OPENAI_API_KEY:
            return GeneratedPhoto(
                prompt=prompt,
                url="https://via.placeholder.com/1024x1024/f3f4f6/374151?text=Staff+Photo",
                width=1024,
                height=1024,
            )

        try:
            response = await self.http.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024",
                    "quality": "standard",
                }
            )
            response.raise_for_status()

            result = response.json()
            image_url = result["data"][0]["url"]

            return GeneratedPhoto(
                prompt=prompt,
                url=image_url,
                width=1024,
                height=1024,
            )
        except Exception:
            return GeneratedPhoto(
                prompt=prompt,
                url="https://via.placeholder.com/1024x1024/f3f4f6/374151?text=Staff+Photo",
                width=1024,
                height=1024,
            )

    async def generate_service_image(
        self,
        service_name: str,
        vertical: str,
    ) -> GeneratedPhoto:
        """Generate an image for a specific service."""
        prompt = f"Professional photo illustrating {service_name} service by a {vertical}, clean modern setting, UK, high quality"

        if not OPENAI_API_KEY:
            return GeneratedPhoto(
                prompt=prompt,
                url="https://via.placeholder.com/1792x1024/10b981/ffffff?text=Service+Image",
                width=1792,
                height=1024,
            )

        try:
            response = await self.http.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1792x1024",
                    "quality": "standard",
                }
            )
            response.raise_for_status()

            result = response.json()
            image_url = result["data"][0]["url"]

            return GeneratedPhoto(
                prompt=prompt,
                url=image_url,
                width=1792,
                height=1024,
            )
        except Exception:
            return GeneratedPhoto(
                prompt=prompt,
                url="https://via.placeholder.com/1792x1024/10b981/ffffff?text=Service+Image",
                width=1792,
                height=1024,
            )


# Singleton instances
photo_processor = PhotoProcessor()
image_generator = ImageGenerator()

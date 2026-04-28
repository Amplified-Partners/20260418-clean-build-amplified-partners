"""
HeyGen video integration.
Generates talking-head avatar videos from scripts.
Used for social media clips, educational content, client onboarding.
"""
import os
import logging
import asyncio
from dataclasses import dataclass
from typing import Optional
import httpx

logger = logging.getLogger("marketing.heygen")

HEYGEN_API = "https://api.heygen.com"


@dataclass
class VideoRequest:
    script: str
    title: str
    avatar_id: str = ""
    voice_id: str = ""
    background: str = "default"
    aspect_ratio: str = "16:9"  # 16:9, 9:16 (TikTok/Reels), 1:1
    max_duration_seconds: int = 90


@dataclass
class VideoResult:
    video_id: str
    status: str  # "pending", "processing", "completed", "failed"
    url: str = ""
    thumbnail_url: str = ""
    duration_seconds: float = 0.0
    error: str = ""


class HeyGenClient:
    """HeyGen API client for avatar video generation."""

    def __init__(self):
        self.api_key = os.environ.get("HEYGEN_API_KEY", "")
        if not self.api_key:
            logger.warning("HEYGEN_API_KEY not set — video generation will be simulated")
        self._client = httpx.AsyncClient(
            base_url=HEYGEN_API,
            headers={"X-Api-Key": self.api_key, "Content-Type": "application/json"},
            timeout=60.0,
        )

    async def generate(self, req: VideoRequest) -> VideoResult:
        """Submit a video generation request."""
        if not self.api_key:
            logger.info(f"[DRY RUN] HeyGen video: {req.title} ({len(req.script.split())} words)")
            return VideoResult(video_id="dry-run", status="simulated")

        # Word count check — HeyGen charges per minute
        word_count = len(req.script.split())
        estimated_seconds = word_count * 0.5  # ~120wpm speaking pace
        if estimated_seconds > req.max_duration_seconds:
            logger.warning(f"Script too long ({estimated_seconds:.0f}s > {req.max_duration_seconds}s) — truncating")
            words = req.script.split()[:int(req.max_duration_seconds * 2)]
            req.script = " ".join(words)

        payload = {
            "video_inputs": [{
                "character": {
                    "type": "avatar",
                    "avatar_id": req.avatar_id or os.environ.get("HEYGEN_AVATAR_ID", ""),
                    "avatar_style": "normal",
                },
                "voice": {
                    "type": "text",
                    "input_text": req.script,
                    "voice_id": req.voice_id or os.environ.get("HEYGEN_VOICE_ID", ""),
                },
                "background": {"type": "color", "value": "#111111"},
            }],
            "aspect_ratio": req.aspect_ratio,
            "title": req.title,
        }

        try:
            resp = await self._client.post("/v2/video/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
            video_id = data.get("data", {}).get("video_id", "")
            logger.info(f"HeyGen job submitted: {video_id}")
            return VideoResult(video_id=video_id, status="pending")
        except Exception as e:
            logger.error(f"HeyGen generate failed: {e}")
            return VideoResult(video_id="", status="failed", error=str(e))

    async def check_status(self, video_id: str) -> VideoResult:
        """Poll video status."""
        if not self.api_key or video_id in ("dry-run", ""):
            return VideoResult(video_id=video_id, status="simulated")

        try:
            resp = await self._client.get(f"/v1/video_status.get?video_id={video_id}")
            resp.raise_for_status()
            data = resp.json().get("data", {})
            return VideoResult(
                video_id=video_id,
                status=data.get("status", "unknown"),
                url=data.get("video_url", ""),
                thumbnail_url=data.get("thumbnail_url", ""),
                duration_seconds=data.get("duration", 0.0),
            )
        except Exception as e:
            logger.error(f"HeyGen status check failed: {e}")
            return VideoResult(video_id=video_id, status="error", error=str(e))

    async def wait_for_completion(self, video_id: str, timeout_seconds: int = 300) -> VideoResult:
        """Poll until video is ready or timeout."""
        start = asyncio.get_event_loop().time()
        while True:
            result = await self.check_status(video_id)
            if result.status in ("completed", "failed", "simulated"):
                return result
            elapsed = asyncio.get_event_loop().time() - start
            if elapsed > timeout_seconds:
                return VideoResult(video_id=video_id, status="timeout",
                                   error=f"Timed out after {timeout_seconds}s")
            logger.info(f"HeyGen {video_id}: {result.status} ({elapsed:.0f}s)")
            await asyncio.sleep(15)

    async def close(self):
        await self._client.aclose()


class VideoScriptGenerator:
    """
    Generates video scripts from content using LLM.
    Converts blog/social content into natural spoken-word scripts.
    """

    def __init__(self, litellm_url: str, litellm_key: str):
        self.litellm_url = litellm_url
        self.litellm_key = litellm_key

    async def generate_script(
        self,
        content: str,
        style: str = "heygen",  # heygen (60-90s) or synthesia (2-5min)
        brand_voice: str = "friendly_professional",
    ) -> str:
        """Generate a natural spoken-word video script from written content."""
        durations = {"heygen": "60-90 seconds", "synthesia": "2-3 minutes"}
        word_counts = {"heygen": "120-180 words", "synthesia": "300-450 words"}

        prompt = f"""Convert this written content into a natural spoken-word video script.

CONTENT:
{content}

REQUIREMENTS:
- Duration: {durations[style]}
- Word count: {word_counts[style]}
- Style: Natural, conversational spoken English — NOT written English
- Short sentences. Breathing room. Natural pauses marked with [PAUSE]
- No reading-aloud-of-text feel — this should sound like someone talking
- Brand voice: {brand_voice}
- Start with a hook that grabs attention in the first 3 seconds
- End with a clear, single call to action

FORMAT: Return the script only — no stage directions, no headers, just the words to be spoken.
Add [PAUSE] where natural breaks occur.
"""

        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(
                f"{self.litellm_url}/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.litellm_key}"},
                json={
                    "model": "claude-sonnet-4",
                    "messages": [
                        {"role": "system", "content": "You write natural spoken-word video scripts. Output only the script."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 600,
                },
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()

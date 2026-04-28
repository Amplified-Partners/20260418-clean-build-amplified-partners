"""
Marketing Engine — Publishing Agent
Schedules and publishes content to platforms.

Runs at scheduled intervals on The Beast, after content agent.
Handles platform-specific formatting, rate limiting, and engagement tracking.
"""

import asyncio
import httpx
import yaml
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger("marketing.publishing")


@dataclass
class PublishResult:
    """Outcome of a publishing attempt."""
    client_id: str
    platform: str
    content_type: str
    status: str          # "published", "scheduled", "failed", "held_for_review"
    post_id: str = ""    # Platform post ID if published
    scheduled_time: str = ""
    error: str = ""
    engagement: dict = field(default_factory=dict)  # Filled later by metrics
    published_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class PublishingAgent:
    """
    Publishes approved content to social platforms and GMB.

    Flow:
    1. Receive approved content from content agent
    2. Check posting cadence (don't flood)
    3. Format for each platform
    4. Publish or schedule via platform APIs
    5. Log results to Langfuse for tracking
    6. Store published content in PostgreSQL

    Phase 1 (current): Write content to output files for manual review
    Phase 2: Direct API integration with platforms
    """

    def __init__(self, config_path: str = "/app/config/engine_config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        self.limits = self.config.get("limits", {})
        self.schedule = self.config.get("schedule", {}).get("publishing", {})

    def check_cadence(self, client_id: str, platform: str, recent_posts: list[dict]) -> bool:
        """Check if we're within posting limits."""
        max_per_day = self.limits.get("max_posts_per_day", 5)
        min_hours = self.limits.get("min_hours_between_posts", 2)

        today = datetime.utcnow().date()
        today_posts = [
            p for p in recent_posts
            if p.get("platform") == platform
            and datetime.fromisoformat(p.get("published_at", "")).date() == today
        ]

        if len(today_posts) >= max_per_day:
            logger.warning(f"{client_id}/{platform}: Hit daily limit ({max_per_day})")
            return False

        if today_posts:
            last_post_time = max(
                datetime.fromisoformat(p["published_at"]) for p in today_posts
            )
            hours_since = (datetime.utcnow() - last_post_time).total_seconds() / 3600
            if hours_since < min_hours:
                logger.info(f"{client_id}/{platform}: Too soon ({hours_since:.1f}h < {min_hours}h)")
                return False

        return True

    def format_for_platform(self, body: str, platform: str, hashtags: list[str] = None) -> str:
        """Apply platform-specific formatting."""
        hashtags = hashtags or []

        if platform == "twitter":
            # Trim to 280 chars, append hashtags if they fit
            tag_str = " ".join(f"#{t}" for t in hashtags[:2])
            max_body = 280 - len(tag_str) - 1
            if len(body) > max_body:
                body = body[:max_body - 3] + "..."
            return f"{body} {tag_str}".strip()

        elif platform == "instagram":
            # Instagram: body + line break + hashtags block
            tag_str = " ".join(f"#{t}" for t in hashtags[:self.limits.get("max_hashtags", 5)])
            return f"{body}\n\n.\n.\n.\n{tag_str}"

        elif platform == "facebook":
            # Facebook: body + hashtags inline
            tag_str = " ".join(f"#{t}" for t in hashtags[:3])
            return f"{body}\n\n{tag_str}" if tag_str else body

        elif platform == "gmb":
            # GMB: Plain text, no hashtags, max 1500 chars
            return body[:1500]

        elif platform == "linkedin":
            # LinkedIn: Professional, hashtags at end
            tag_str = " ".join(f"#{t}" for t in hashtags[:3])
            return f"{body}\n\n{tag_str}" if tag_str else body

        return body

    def get_next_slot(self, platform: str) -> Optional[str]:
        """Get the next available posting time for a platform."""
        schedule_str = self.schedule.get(platform, "")
        if not schedule_str:
            return None

        now = datetime.utcnow()
        hours = [int(h.split(":")[0]) if ":" in str(h) else int(h)
                 for h in str(schedule_str).split(",")]

        for hour in sorted(hours):
            slot = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if slot > now:
                return slot.isoformat()

        # All slots passed today — schedule for first slot tomorrow
        tomorrow = now + timedelta(days=1)
        first_hour = min(hours)
        return tomorrow.replace(hour=first_hour, minute=0, second=0, microsecond=0).isoformat()

    async def write_to_output(self, client_id: str, content_piece, formatted_body: str) -> str:
        """
        Phase 1: Write content to output directory for manual review.
        Phase 2 will replace this with direct API publishing.
        """
        output_dir = Path(f"/app/outputs/clients/{client_id}")
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{content_piece.platform}_{content_piece.content_type}_{timestamp}.json"

        output = {
            "client_id": client_id,
            "platform": content_piece.platform,
            "content_type": content_piece.content_type,
            "title": content_piece.title,
            "body": formatted_body,
            "original_body": content_piece.body,
            "hashtags": content_piece.hashtags,
            "media_suggestions": content_piece.media_suggestions,
            "quality_score": content_piece.quality_score,
            "status": content_piece.status,
            "created_at": content_piece.created_at,
            "metadata": content_piece.metadata,
        }

        output_path = output_dir / filename
        with open(output_path, "w") as f:
            json.dump(output, f, indent=2)

        logger.info(f"  Written to {output_path}")
        return str(output_path)

    async def publish_piece(self, content_piece, client_config: dict, recent_posts: list[dict]) -> PublishResult:
        """Publish or schedule a single content piece."""
        client_id = client_config["client"]["id"]
        platform = content_piece.platform

        # Check if content is approved
        if content_piece.status != "approved":
            return PublishResult(
                client_id=client_id,
                platform=platform,
                content_type=content_piece.content_type,
                status="held_for_review",
                error=f"Quality score {content_piece.quality_score:.1f} below threshold",
            )

        # Check cadence
        if not self.check_cadence(client_id, platform, recent_posts):
            next_slot = self.get_next_slot(platform)
            return PublishResult(
                client_id=client_id,
                platform=platform,
                content_type=content_piece.content_type,
                status="scheduled",
                scheduled_time=next_slot or "",
            )

        # Format for platform
        formatted = self.format_for_platform(
            content_piece.body,
            platform,
            content_piece.hashtags,
        )

        # Phase 1: Write to file for manual review
        output_path = await self.write_to_output(client_id, content_piece, formatted)

        return PublishResult(
            client_id=client_id,
            platform=platform,
            content_type=content_piece.content_type,
            status="published",  # Phase 1: "published" means written to output
            post_id=output_path,
        )

    async def run(self, client_id: str, content_pieces: list) -> list[PublishResult]:
        """Publish all approved content for a client."""
        client_path = Path(f"/app/config/clients/{client_id}.yaml")
        with open(client_path) as f:
            client_config = yaml.safe_load(f)

        logger.info(f"Publishing {len(content_pieces)} pieces for {client_id}")

        # TODO: Load recent posts from PostgreSQL
        recent_posts: list[dict] = []

        results = []
        for piece in content_pieces:
            result = await self.publish_piece(piece, client_config, recent_posts)
            results.append(result)
            logger.info(f"  {piece.platform}: {result.status}")

        published = sum(1 for r in results if r.status == "published")
        scheduled = sum(1 for r in results if r.status == "scheduled")
        held = sum(1 for r in results if r.status == "held_for_review")

        logger.info(
            f"Publishing complete: {published} published, "
            f"{scheduled} scheduled, {held} held for review"
        )

        return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Integration test would chain: research → content → publishing
    print("Publishing agent ready. Run via orchestrator.")

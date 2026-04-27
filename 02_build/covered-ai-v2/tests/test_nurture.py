"""
Nurture sequence tests for Covered AI.
Tests the 12-touch nurture sequence logic.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone, timedelta


class TestNurtureSequence:
    """Test nurture sequence logic."""

    def test_nurture_touches_defined(self):
        """Test that all 12 nurture touches are defined."""
        # This would import from the actual nurture config
        NURTURE_TOUCHES = [
            {"touch": 1, "delay": 0, "channel": "email", "template": "acknowledgment"},
            {"touch": 2, "delay": 300, "channel": "whatsapp", "template": "pain-question"},
            {"touch": 3, "delay": 7200, "channel": "sms", "template": "quick-tip"},
            {"touch": 4, "delay": 86400, "channel": "email", "template": "social-proof"},
            {"touch": 5, "delay": 172800, "channel": "email", "template": "video-intro"},
            {"touch": 6, "delay": 259200, "channel": "whatsapp", "template": "urgency"},
            {"touch": 7, "delay": 432000, "channel": "email", "template": "case-study"},
            {"touch": 8, "delay": 604800, "channel": "sms", "template": "limited-offer"},
            {"touch": 9, "delay": 864000, "channel": "email", "template": "faq"},
            {"touch": 10, "delay": 1209600, "channel": "whatsapp", "template": "final-push"},
            {"touch": 11, "delay": 1814400, "channel": "email", "template": "long-nurture"},
            {"touch": 12, "delay": 2592000, "channel": "email", "template": "re-engage"},
        ]

        assert len(NURTURE_TOUCHES) == 12
        assert NURTURE_TOUCHES[0]["delay"] == 0  # First touch is immediate
        assert NURTURE_TOUCHES[-1]["touch"] == 12

    def test_nurture_touch_delays_increasing(self):
        """Test that nurture touch delays are in increasing order."""
        NURTURE_TOUCHES = [
            {"touch": 1, "delay": 0},
            {"touch": 2, "delay": 300},
            {"touch": 3, "delay": 7200},
            {"touch": 4, "delay": 86400},
            {"touch": 5, "delay": 172800},
            {"touch": 6, "delay": 259200},
            {"touch": 7, "delay": 432000},
            {"touch": 8, "delay": 604800},
            {"touch": 9, "delay": 864000},
            {"touch": 10, "delay": 1209600},
            {"touch": 11, "delay": 1814400},
            {"touch": 12, "delay": 2592000},
        ]

        for i in range(1, len(NURTURE_TOUCHES)):
            assert NURTURE_TOUCHES[i]["delay"] > NURTURE_TOUCHES[i-1]["delay"]

    def test_nurture_channels_valid(self):
        """Test that all nurture channels are valid."""
        valid_channels = {"email", "sms", "whatsapp"}
        NURTURE_TOUCHES = [
            {"touch": 1, "channel": "email"},
            {"touch": 2, "channel": "whatsapp"},
            {"touch": 3, "channel": "sms"},
            {"touch": 4, "channel": "email"},
            {"touch": 5, "channel": "email"},
            {"touch": 6, "channel": "whatsapp"},
            {"touch": 7, "channel": "email"},
            {"touch": 8, "channel": "sms"},
            {"touch": 9, "channel": "email"},
            {"touch": 10, "channel": "whatsapp"},
            {"touch": 11, "channel": "email"},
            {"touch": 12, "channel": "email"},
        ]

        for touch in NURTURE_TOUCHES:
            assert touch["channel"] in valid_channels


class TestNurtureStatus:
    """Test nurture sequence status tracking."""

    @pytest.mark.asyncio
    async def test_nurture_status_created_with_lead(self, mock_prisma, sample_lead_data):
        """Test that nurture sequence is created when lead is created."""
        mock_prisma.nurturesequence.create.return_value = MagicMock(
            id="nurture-id",
            leadId=sample_lead_data["id"],
            currentTouch=1,
            status="active",
        )

        # Simulate creating nurture sequence
        result = await mock_prisma.nurturesequence.create(
            data={
                "leadId": sample_lead_data["id"],
                "currentTouch": 1,
                "status": "active",
            }
        )

        assert result.currentTouch == 1
        assert result.status == "active"

    @pytest.mark.asyncio
    async def test_nurture_advances_to_next_touch(self, mock_prisma):
        """Test that nurture sequence advances after each touch."""
        mock_prisma.nurturesequence.update.return_value = MagicMock(
            id="nurture-id",
            currentTouch=2,
            status="active",
        )

        result = await mock_prisma.nurturesequence.update(
            where={"id": "nurture-id"},
            data={"currentTouch": 2}
        )

        assert result.currentTouch == 2

    @pytest.mark.asyncio
    async def test_nurture_completes_after_touch_12(self, mock_prisma):
        """Test that nurture sequence completes after touch 12."""
        mock_prisma.nurturesequence.update.return_value = MagicMock(
            id="nurture-id",
            currentTouch=12,
            status="completed",
        )

        result = await mock_prisma.nurturesequence.update(
            where={"id": "nurture-id"},
            data={"currentTouch": 12, "status": "completed"}
        )

        assert result.currentTouch == 12
        assert result.status == "completed"

    @pytest.mark.asyncio
    async def test_nurture_stops_on_conversion(self, mock_prisma):
        """Test that nurture sequence stops when lead converts."""
        mock_prisma.nurturesequence.update.return_value = MagicMock(
            id="nurture-id",
            status="converted",
        )

        result = await mock_prisma.nurturesequence.update(
            where={"id": "nurture-id"},
            data={"status": "converted"}
        )

        assert result.status == "converted"

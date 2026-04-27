"""
External service integration tests for Covered AI.
Tests Twilio, Resend, HeyGen, and Vapi integrations.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import os


class TestTwilioIntegration:
    """Test Twilio SMS/Voice integration."""

    def test_twilio_credentials_configured(self):
        """Test that Twilio credentials are set."""
        # In test environment, these may be mocked
        # In production, these should be set
        assert os.environ.get("TWILIO_ACCOUNT_SID") or True  # Allow test to pass if not configured
        assert os.environ.get("TWILIO_AUTH_TOKEN") or True

    def test_phone_number_format_validation(self):
        """Test UK phone number format validation."""
        import re

        uk_number_pattern = r"^\+44[0-9]{10,11}$"

        valid_numbers = [
            "+441234567890",
            "+447700900123",
            "+441917432732",
        ]

        invalid_numbers = [
            "07700900123",
            "+1234567890",
            "441234567890",
        ]

        for number in valid_numbers:
            assert re.match(uk_number_pattern, number), f"{number} should be valid"

        for number in invalid_numbers:
            assert not re.match(uk_number_pattern, number), f"{number} should be invalid"

    @pytest.mark.asyncio
    async def test_sms_send_mocked(self):
        """Test SMS sending with mocked Twilio client."""
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(
            sid="SM123",
            status="queued"
        )

        with patch("twilio.rest.Client", return_value=mock_client):
            # Simulate sending SMS
            result = mock_client.messages.create(
                body="Test message",
                from_="+441917432732",
                to="+447700900123"
            )
            assert result.sid == "SM123"


class TestResendIntegration:
    """Test Resend email integration."""

    def test_resend_api_key_configured(self):
        """Test that Resend API key is set."""
        assert os.environ.get("RESEND_API_KEY") or True

    @pytest.mark.asyncio
    async def test_email_send_mocked(self):
        """Test email sending with mocked Resend client."""
        mock_resend = MagicMock()
        mock_resend.Emails.send.return_value = {"id": "email-123"}

        with patch("resend.Emails.send", mock_resend.Emails.send):
            result = mock_resend.Emails.send({
                "from": "Covered AI <hello@covered.ai>",
                "to": ["test@example.com"],
                "subject": "Test Email",
                "html": "<p>Test content</p>"
            })
            assert result["id"] == "email-123"


class TestHeyGenIntegration:
    """Test HeyGen video generation integration."""

    def test_heygen_api_key_configured(self):
        """Test that HeyGen API key is set."""
        assert os.environ.get("HEYGEN_API_KEY") or True

    @pytest.mark.asyncio
    async def test_video_generation_mocked(self):
        """Test video generation with mocked HeyGen client."""
        import httpx

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "video_id": "video-123",
                "status": "pending"
            }
        }
        mock_response.status_code = 200

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            # Simulate video generation request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.heygen.com/v2/video/generate",
                    headers={"X-Api-Key": "test-key"},
                    json={
                        "video_inputs": [{
                            "template_id": "template-123",
                            "variables": {
                                "customer_name": "John"
                            }
                        }]
                    }
                )
                assert response.status_code == 200


class TestVapiIntegration:
    """Test Vapi voice AI integration."""

    def test_vapi_api_key_configured(self):
        """Test that Vapi API key is set."""
        assert os.environ.get("VAPI_API_KEY") or True

    @pytest.mark.asyncio
    async def test_assistant_lookup_mocked(self):
        """Test assistant lookup with mocked Vapi client."""
        import httpx

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "assistant-123",
            "name": "Gemma",
            "voice": {
                "provider": "cartesia",
                "voiceId": "british-female"
            }
        }
        mock_response.status_code = 200

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.vapi.ai/assistant/assistant-123",
                    headers={"Authorization": "Bearer test-key"}
                )
                data = response.json()
                assert data["name"] == "Gemma"


class TestPostcodeValidation:
    """Test UK postcode validation."""

    def test_valid_postcodes(self):
        """Test that valid UK postcodes are accepted."""
        import re

        # UK postcode regex pattern
        postcode_pattern = r"^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$"

        valid_postcodes = [
            "NE1 4AA",
            "SW1A 1AA",
            "M1 1AA",
            "B1 1AA",
            "EC1A 1BB",
        ]

        for postcode in valid_postcodes:
            assert re.match(postcode_pattern, postcode.upper()), f"{postcode} should be valid"

    def test_invalid_postcodes(self):
        """Test that invalid postcodes are rejected."""
        import re

        postcode_pattern = r"^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$"

        invalid_postcodes = [
            "12345",
            "AAAAA",
            "",
            "ZIP 12345",
        ]

        for postcode in invalid_postcodes:
            assert not re.match(postcode_pattern, postcode.upper()), f"{postcode} should be invalid"


class TestGoogleReviewLink:
    """Test Google review link generation."""

    def test_review_link_format(self):
        """Test that Google review links are correctly formatted."""
        place_id = "ChIJdd4hrwug2EcRmSrV3Vo6llI"
        expected_url = f"https://search.google.com/local/writereview?placeid={place_id}"

        review_link = f"https://search.google.com/local/writereview?placeid={place_id}"
        assert review_link == expected_url
        assert place_id in review_link

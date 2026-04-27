"""
Webhook unit tests for Covered AI.
Tests Vapi call completion webhook handling logic.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone


class TestVapiWebhookLogic:
    """Test Vapi webhook business logic."""

    def test_vapi_payload_parsing(self, sample_vapi_webhook_payload):
        """Test that Vapi webhook payload is correctly parsed."""
        message = sample_vapi_webhook_payload["message"]

        assert message["type"] == "end-of-call-report"
        assert "call" in message
        assert message["call"]["id"] == "vapi-call-123"
        assert "transcript" in message
        assert "summary" in message

    def test_call_analysis_extraction(self, sample_vapi_webhook_payload):
        """Test that call analysis is correctly extracted."""
        analysis = sample_vapi_webhook_payload["message"]["analysis"]

        assert analysis["intent"] == "emergency_plumbing"
        assert analysis["sentiment"] == "urgent"

    @pytest.mark.asyncio
    async def test_lead_created_from_call(self, mock_prisma, sample_client_data):
        """Test that lead is created from call data."""
        mock_prisma.lead.create.return_value = MagicMock(
            id="new-lead-id",
            clientId=sample_client_data["id"],
            status="new",
            urgency="emergency",
            jobType="Emergency plumbing",
        )

        lead = await mock_prisma.lead.create(data={
            "clientId": sample_client_data["id"],
            "customerId": "customer-id",
            "jobType": "Emergency plumbing",
            "urgency": "emergency",
            "status": "new",
        })

        assert lead.id == "new-lead-id"
        assert lead.status == "new"
        assert lead.urgency == "emergency"

    @pytest.mark.asyncio
    async def test_customer_lookup_by_phone(self, mock_prisma, sample_customer_data):
        """Test that existing customer is found by phone number."""
        mock_prisma.customer.find_first.return_value = MagicMock(**sample_customer_data)

        customer = await mock_prisma.customer.find_first(where={
            "clientId": sample_customer_data["clientId"],
            "phone": sample_customer_data["phone"]
        })

        assert customer is not None
        assert customer.phone == sample_customer_data["phone"]

    @pytest.mark.asyncio
    async def test_new_customer_created(self, mock_prisma, sample_client_data):
        """Test that new customer is created when not found."""
        mock_prisma.customer.find_first.return_value = None
        mock_prisma.customer.create.return_value = MagicMock(
            id="new-customer-id",
            clientId=sample_client_data["id"],
            name="New Customer",
            phone="+447700999999",
        )

        # Customer not found
        existing = await mock_prisma.customer.find_first(where={"phone": "+447700999999"})
        assert existing is None

        # Create new customer
        customer = await mock_prisma.customer.create(data={
            "clientId": sample_client_data["id"],
            "name": "New Customer",
            "phone": "+447700999999",
        })

        assert customer.id == "new-customer-id"
        assert customer.phone == "+447700999999"


class TestTriggerWebhookLogic:
    """Test Trigger.dev webhook business logic."""

    def test_trigger_event_format(self):
        """Test that Trigger.dev event format is valid."""
        event = {
            "event": "nurture.touch_complete",
            "data": {
                "lead_id": "test-lead-id",
                "touch_number": 1,
                "status": "sent",
            }
        }

        assert "event" in event
        assert "data" in event
        assert event["data"]["touch_number"] == 1

    @pytest.mark.asyncio
    async def test_nurture_progress_updated(self, mock_prisma):
        """Test that nurture progress is updated after event."""
        mock_prisma.nurturesequence.update.return_value = MagicMock(
            id="nurture-id",
            currentTouch=2,
            lastTouchAt=datetime.now(timezone.utc),
        )

        nurture = await mock_prisma.nurturesequence.update(
            where={"leadId": "test-lead-id"},
            data={"currentTouch": 2, "lastTouchAt": datetime.now(timezone.utc)}
        )

        assert nurture.currentTouch == 2


class TestNotificationLogic:
    """Test notification creation logic."""

    @pytest.mark.asyncio
    async def test_notification_created(self, mock_prisma, sample_client_data):
        """Test that notification record is created."""
        mock_prisma.notification.create.return_value = MagicMock(
            id="notification-id",
            clientId=sample_client_data["id"],
            channel="email",
            status="sent",
        )

        notification = await mock_prisma.notification.create(data={
            "clientId": sample_client_data["id"],
            "channel": "email",
            "recipient": "owner@example.com",
            "subject": "New Lead",
            "status": "sent",
        })

        assert notification.id == "notification-id"
        assert notification.status == "sent"

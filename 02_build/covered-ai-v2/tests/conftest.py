"""
Pytest configuration and fixtures for integration tests.
"""
import os
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock, AsyncMock

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = os.environ.get("DATABASE_URL", "postgresql://test:test@localhost:5432/covered_test")


def create_mock_record(**kwargs):
    """Create a mock record with attributes from kwargs."""
    record = MagicMock()
    for key, value in kwargs.items():
        setattr(record, key, value)
    return record


@pytest.fixture
def mock_prisma():
    """Mock Prisma client for unit tests."""
    mock = MagicMock()
    mock.connect = AsyncMock()
    mock.disconnect = AsyncMock()

    # Mock User model
    mock.user = MagicMock()
    mock.user.find_unique = AsyncMock(return_value=None)
    mock.user.find_first = AsyncMock(return_value=None)
    mock.user.find_many = AsyncMock(return_value=[])
    mock.user.create = AsyncMock()
    mock.user.update = AsyncMock()

    # Mock Session model
    mock.session = MagicMock()
    mock.session.find_unique = AsyncMock(return_value=None)
    mock.session.create = AsyncMock()
    mock.session.delete = AsyncMock()
    mock.session.delete_many = AsyncMock()

    # Mock OnboardingSession model
    mock.onboardingsession = MagicMock()
    mock.onboardingsession.find_unique = AsyncMock(return_value=None)
    mock.onboardingsession.create = AsyncMock()
    mock.onboardingsession.update = AsyncMock()

    # Mock Client model
    mock.client = MagicMock()
    mock.client.find_unique = AsyncMock(return_value=None)
    mock.client.find_first = AsyncMock(return_value=None)
    mock.client.find_many = AsyncMock(return_value=[])
    mock.client.create = AsyncMock()
    mock.client.update = AsyncMock()
    mock.client.delete = AsyncMock()

    # Mock Lead model
    mock.lead = MagicMock()
    mock.lead.find_unique = AsyncMock(return_value=None)
    mock.lead.find_many = AsyncMock(return_value=[])
    mock.lead.create = AsyncMock()
    mock.lead.update = AsyncMock()
    mock.lead.count = AsyncMock(return_value=0)

    # Mock Customer model
    mock.customer = MagicMock()
    mock.customer.find_unique = AsyncMock(return_value=None)
    mock.customer.find_first = AsyncMock(return_value=None)
    mock.customer.find_many = AsyncMock(return_value=[])
    mock.customer.create = AsyncMock()
    mock.customer.update = AsyncMock()
    mock.customer.count = AsyncMock(return_value=0)

    # Mock Job model
    mock.job = MagicMock()
    mock.job.find_unique = AsyncMock(return_value=None)
    mock.job.find_many = AsyncMock(return_value=[])
    mock.job.create = AsyncMock()
    mock.job.update = AsyncMock()
    mock.job.count = AsyncMock(return_value=0)

    # Mock NurtureSequence model
    mock.nurturesequence = MagicMock()
    mock.nurturesequence.find_unique = AsyncMock(return_value=None)
    mock.nurturesequence.create = AsyncMock()
    mock.nurturesequence.update = AsyncMock()

    # Mock Notification model
    mock.notification = MagicMock()
    mock.notification.create = AsyncMock()
    mock.notification.find_many = AsyncMock(return_value=[])

    return mock


@pytest.fixture
def sample_client_data():
    """Sample client data for tests."""
    return {
        "id": "test-client-id",
        "businessName": "Test Plumbing",
        "ownerName": "John Test",
        "phone": "+447700000000",
        "email": "test@example.com",
        "coveredNumber": "+441917432732",
        "vertical": "trades",
        "subscriptionPlan": "starter",
        "subscriptionStatus": "active",
        "notificationEmail": "test@example.com",
    }


@pytest.fixture
def sample_lead_data():
    """Sample lead data for tests."""
    return {
        "id": "test-lead-id",
        "clientId": "test-client-id",
        "customerId": "test-customer-id",
        "callId": "test-call-id",
        "jobType": "Emergency plumbing",
        "description": "Burst pipe in kitchen",
        "urgency": "emergency",
        "status": "new",
        "value": 250.0,
    }


@pytest.fixture
def sample_vapi_webhook_payload():
    """Sample Vapi webhook payload for call completion."""
    return {
        "message": {
            "type": "end-of-call-report",
            "call": {
                "id": "vapi-call-123",
                "phoneNumberId": "pn_123",
                "status": "ended",
            },
            "recordingUrl": "https://example.com/recording.mp3",
            "transcript": "Gemma: Hello, Test Plumbing, Gemma speaking. How can I help? Caller: Hi, I have a burst pipe.",
            "summary": "Emergency call about burst pipe in kitchen.",
            "analysis": {
                "intent": "emergency_plumbing",
                "sentiment": "urgent",
            },
        }
    }


@pytest.fixture
def sample_customer_data():
    """Sample customer data for tests."""
    return {
        "id": "test-customer-id",
        "clientId": "test-client-id",
        "name": "Jane Customer",
        "phone": "+447700111111",
        "email": "jane@example.com",
        "address": "123 Test Street",
        "postcode": "NE1 4AA",
    }


@pytest.fixture
def sample_job_data():
    """Sample job data for tests."""
    return {
        "id": "test-job-id",
        "clientId": "test-client-id",
        "customerId": "test-customer-id",
        "leadId": "test-lead-id",
        "title": "Emergency pipe repair",
        "description": "Fix burst pipe in kitchen",
        "status": "scheduled",
        "scheduledDate": "2025-11-28T10:00:00Z",
        "estimatedValue": 250.0,
    }

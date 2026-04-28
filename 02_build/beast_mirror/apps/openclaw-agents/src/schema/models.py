"""
API Request/Response Schemas
=============================
Thin Pydantic models. Keep these minimal — they're the contract
between the API and any future frontend or orchestrator.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Role(str, Enum):
    human = "human"
    ai = "ai"
    system = "system"
    tool = "tool"


class ChatMessage(BaseModel):
    role: Role
    content: str
    name: str | None = None
    tool_calls: list[dict[str, Any]] | None = None


class ChatRequest(BaseModel):
    """What comes in from a client."""
    message: str
    thread_id: str | None = None  # None = new conversation
    agent_id: str = "test"       # Which agent to route to
    model: str | None = None      # Override default model


class ChatResponse(BaseModel):
    """What goes back for a non-streaming invoke."""
    message: str
    thread_id: str
    agent_id: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class StreamEvent(BaseModel):
    """Single SSE event payload."""
    event: str  # "token", "message", "error", "done"
    data: str
    thread_id: str | None = None


class AgentInfo(BaseModel):
    """Describes a registered agent."""
    agent_id: str
    description: str
    tools: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str  # "ok" or "degraded"
    version: str
    timestamp: datetime
    checks: dict[str, str] = Field(default_factory=dict)

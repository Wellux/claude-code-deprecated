"""Pydantic request/response models for the FastAPI layer."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CompleteRequest(BaseModel):
    prompt: str
    system: str | None = None
    model: str | None = None          # None = auto-route
    max_tokens: int = Field(default=4096, ge=1, le=200000)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    stream: bool = False
    auto_route: bool = True           # use routing system to pick model


class CompleteResponse(BaseModel):
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    stop_reason: str
    routed_by: str | None = None      # routing reason if auto_route=True


class RouteRequest(BaseModel):
    task: str
    content_type: str | None = None   # hint for memory router


class RouteResponse(BaseModel):
    model: str
    model_reason: str
    skill: str | None
    skill_confidence: float | None
    agent: str
    agent_reason: str
    memory_tier: str
    memory_destination: str
    plan_size: str
    plan_mode: str
    subtasks: list[dict]


class ChatMessage(BaseModel):
    role: str   # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)
    system: str | None = None
    model: str | None = None
    max_tokens: int = Field(default=4096, ge=1, le=200000)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)


class ChatResponse(BaseModel):
    message: ChatMessage
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class HealthResponse(BaseModel):
    status: str
    version: str
    models_available: list[str]
    uptime_s: float | None = None

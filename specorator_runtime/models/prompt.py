from datetime import datetime, UTC
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str


class Prompt(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    request_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    messages: list[Message]
    parameters: dict[str, Any] = Field(default_factory=dict)

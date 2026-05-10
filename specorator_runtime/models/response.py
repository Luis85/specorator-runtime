from datetime import datetime, UTC
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    BLOCKED = "blocked"


class Response(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    request_id: UUID
    prompt_id: UUID
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    content: str
    status: ResponseStatus = ResponseStatus.SUCCESS
    metadata: dict[str, Any] = Field(default_factory=dict)

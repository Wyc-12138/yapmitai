from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    data: T
    msg: str = "success"
    traceId: str


class ToggleRequest(BaseModel):
    enabled: bool


class Pagination(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class AgentCallRequest(BaseModel):
    params: dict[str, Any] = Field(default_factory=dict)

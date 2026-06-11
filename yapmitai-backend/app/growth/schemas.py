from typing import Any

from pydantic import BaseModel, Field, model_validator


class TaskStartRequest(BaseModel):
    prompt: str | None = None
    product: str | None = None
    market: str | None = None
    target_customer: str | None = None
    budget: str | None = None

    @model_validator(mode="after")
    def validate_input(self) -> "TaskStartRequest":
        has_prompt = bool(self.prompt and self.prompt.strip())
        has_fields = bool(self.product and self.market)
        if not has_prompt and not has_fields:
            raise ValueError("请提供 prompt 一句话需求，或同时提供 product 与 market")
        return self


class AgentInput(BaseModel):
    task_id: str = ""
    product: str = ""
    market: str = ""
    target_customer: str = ""
    budget: str = ""


class AgentOutput(BaseModel):
    agent_name: str
    status: str = "success"
    result: dict[str, Any] = Field(default_factory=dict)

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
        if not (self.prompt and self.prompt.strip()) and not (self.product and self.market):
            raise ValueError("请提供一句话需求，或同时提供产品与目标市场")
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

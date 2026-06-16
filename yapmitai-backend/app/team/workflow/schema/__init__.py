from pydantic import BaseModel, Field


class WorkflowTaskCreate(BaseModel):
    team_id: int
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    enabled: bool = True


class WorkflowTaskUpdate(BaseModel):
    team_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    enabled: bool | None = None


class WorkflowOrderUpdate(BaseModel):
    agent_ids: list[int] = Field(min_length=1)


class WorkflowRunCreate(BaseModel):
    prompt: str = Field(min_length=1, max_length=5000)

from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    enabled: bool = True
    agent_ids: list[int] = Field(default_factory=list)


class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    enabled: bool | None = None
    agent_ids: list[int] | None = None

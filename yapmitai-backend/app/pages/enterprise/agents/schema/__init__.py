from datetime import datetime

from pydantic import BaseModel, Field


class AgentTaskCreate(BaseModel):
    description: str = Field(min_length=2, max_length=2000)
    deadline: datetime | None = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class AgentToggle(BaseModel):
    enabled: bool


class GlobalToggle(BaseModel):
    enabled: bool


class AgentKnowledgeBaseUpdate(BaseModel):
    knowledge_base_ids: list[str] = Field(default_factory=list)

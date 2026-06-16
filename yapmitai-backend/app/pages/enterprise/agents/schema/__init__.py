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


class AgentCreate(BaseModel):
    code: str = Field(min_length=2, max_length=80, pattern=r"^[a-z0-9-]+$")
    name: str = Field(min_length=2, max_length=100)
    name_en: str | None = Field(default=None, max_length=150)
    description: str | None = None
    avatar: str | None = Field(default=None, max_length=500)
    chat_model_config_id: int | None = None
    system_prompt: str = Field(default="", max_length=10000)
    category: str = Field(min_length=1, max_length=50)
    status: str = Field(default="standby", pattern="^(working|standby|offline)$")
    enabled: bool = True
    today_done: int = Field(default=0, ge=0)
    month_kpi: int = Field(default=0, ge=0, le=100)


class AgentUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=2, max_length=80, pattern=r"^[a-z0-9-]+$")
    name: str | None = Field(default=None, min_length=2, max_length=100)
    name_en: str | None = Field(default=None, max_length=150)
    description: str | None = None
    avatar: str | None = Field(default=None, max_length=500)
    chat_model_config_id: int | None = None
    system_prompt: str | None = Field(default=None, max_length=10000)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    status: str | None = Field(default=None, pattern="^(working|standby|offline)$")
    enabled: bool | None = None
    today_done: int | None = Field(default=None, ge=0)
    month_kpi: int | None = Field(default=None, ge=0, le=100)

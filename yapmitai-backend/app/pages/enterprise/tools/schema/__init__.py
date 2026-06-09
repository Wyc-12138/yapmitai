from typing import Any

from pydantic import BaseModel, Field


class ToolCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    name_en: str | None = Field(default=None, max_length=150)
    code: str = Field(min_length=2, max_length=80)
    category: str = Field(min_length=1, max_length=50)
    description: str | None = None
    icon: str | None = Field(default=None, max_length=100)
    model_config_id: int | None = None
    prompt_template: str = Field(min_length=1)
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    enabled: bool = True
    is_system: bool = False
    sort_order: int = 0


class ToolUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    name_en: str | None = Field(default=None, max_length=150)
    code: str | None = Field(default=None, min_length=2, max_length=80)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    icon: str | None = Field(default=None, max_length=100)
    model_config_id: int | None = None
    prompt_template: str | None = Field(default=None, min_length=1)
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    enabled: bool | None = None
    is_system: bool | None = None
    sort_order: int | None = None


class ToolToggle(BaseModel):
    enabled: bool


class ToolRun(BaseModel):
    task: str = Field(min_length=1, max_length=2000)
    model_config_id: int | None = None

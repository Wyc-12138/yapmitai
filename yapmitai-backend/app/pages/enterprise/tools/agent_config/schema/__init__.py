from pydantic import BaseModel, Field, HttpUrl


class GatewayConfigUpdate(BaseModel):
    gateway_url: HttpUrl
    timeout_seconds: int = Field(default=30, ge=1, le=120)
    global_enabled: bool = True


class ModuleConfigUpdate(BaseModel):
    source: str = Field(pattern="^(external|native|disabled)$")
    settings: dict = Field(default_factory=dict)

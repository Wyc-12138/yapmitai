from pydantic import BaseModel, Field


class LeadSearchRequest(BaseModel):
    industry: str
    region: str
    keywords: list[str] = Field(default_factory=list)
    limit: int = Field(default=20, ge=1, le=100)


class CallTaskRequest(BaseModel):
    contacts: list[str] = Field(min_length=1)
    script_template: str
    consentFlag: bool

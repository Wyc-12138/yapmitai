from pydantic import BaseModel, Field


class AllianceMemberCreate(BaseModel):
    name: str = Field(min_length=2)
    enterprise_type: str
    ai_level: str = "L1"

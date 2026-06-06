from pydantic import BaseModel, Field


class KnowledgeQuery(BaseModel):
    query: str = Field(min_length=2, max_length=2000)
    limit: int = Field(default=5, ge=1, le=20)


class KnowledgeSyncRequest(BaseModel):
    sources: list[str] = Field(default_factory=lambda: ["external", "system"])

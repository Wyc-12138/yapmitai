from pydantic import BaseModel, Field


class KnowledgeQuery(BaseModel):
    query: str = Field(min_length=2, max_length=2000)
    limit: int = Field(default=5, ge=1, le=20)
    answer_model: str | None = None
    knowledge_base_id: str | None = None
    conversation_id: str | None = None


class KnowledgeSyncRequest(BaseModel):
    sources: list[str] = Field(default_factory=lambda: ["external", "system"])


class LocalKnowledgeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    knowledge_type: str = Field(pattern="^(text|image)$")
    description: str = Field(min_length=2, max_length=500)


class LocalKnowledgeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=2, max_length=500)


class KnowledgeModelConfigUpdate(BaseModel):
    embedding_model: str
    answer_model: str
    knowledge_base_id: str


class KnowledgeModelTest(BaseModel):
    knowledge_base_id: str
    text: str = Field(default="悦普 AI 本地知识库模型连接测试", min_length=2, max_length=500)

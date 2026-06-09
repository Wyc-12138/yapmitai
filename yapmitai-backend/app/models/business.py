from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    avatar: Mapped[str | None] = mapped_column(String(500))
    chat_model_config_id: Mapped[int | None] = mapped_column(
        ForeignKey("model_configs.id", ondelete="SET NULL"), nullable=True, index=True
    )
    system_prompt: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[str] = mapped_column(String(30), index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    today_done: Mapped[int] = mapped_column(Integer, default=0)
    month_kpi: Mapped[int] = mapped_column(Integer, default=0)
    chat_model_config: Mapped["ModelConfig | None"] = relationship(
        foreign_keys=[chat_model_config_id]
    )


class ModelConfig(Base):
    __tablename__ = "model_configs"
    __table_args__ = (
        CheckConstraint(
            "model_type IN ('chat', 'embedding')",
            name="ck_model_configs_type",
        ),
        CheckConstraint(
            "(model_type = 'chat' AND context_window_tokens IS NOT NULL "
            "AND max_output_tokens IS NOT NULL) OR "
            "(model_type = 'embedding' AND dimension IS NOT NULL "
            "AND max_input_tokens IS NOT NULL)",
            name="ck_model_configs_type_fields",
        ),
        UniqueConstraint(
            "provider_code",
            "model_code",
            "model_type",
            name="uq_model_configs_provider_model_type",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider_code: Mapped[str] = mapped_column(String(50), index=True)
    provider_name: Mapped[str] = mapped_column(String(100))
    model_code: Mapped[str] = mapped_column(String(100), index=True)
    display_name: Mapped[str] = mapped_column(String(100))
    model_type: Mapped[str] = mapped_column(String(20), index=True)
    api_base_url: Mapped[str] = mapped_column(String(500))
    api_key_encrypted: Mapped[str] = mapped_column(Text, default="")
    api_key_last4: Mapped[str | None] = mapped_column(String(10), nullable=True)
    dimension: Mapped[int | None] = mapped_column(Integer)
    max_input_tokens: Mapped[int | None] = mapped_column(Integer)
    context_window_tokens: Mapped[int | None] = mapped_column(Integer)
    max_output_tokens: Mapped[int | None] = mapped_column(Integer)
    default_temperature: Mapped[float | None] = mapped_column(Float)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    remark: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    knowledge_type: Mapped[str] = mapped_column(String(20), default="text")
    status: Mapped[str] = mapped_column(String(30), default="ready", index=True)
    embedding_model_config_id: Mapped[int | None] = mapped_column(
        ForeignKey("model_configs.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    documents: Mapped[list["KnowledgeDocument"]] = relationship(
        back_populates="knowledge_base", cascade="all, delete-orphan", passive_deletes=True
    )
    embedding_model_config: Mapped[ModelConfig | None] = relationship(
        foreign_keys=[embedding_model_config_id]
    )


class AiTool(Base):
    __tablename__ = "ai_tools"
    __table_args__ = (
        UniqueConstraint("code", name="uq_ai_tools_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    name_en: Mapped[str | None] = mapped_column(String(150))
    code: Mapped[str] = mapped_column(String(80), index=True)
    category: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    icon: Mapped[str | None] = mapped_column(String(100))
    model_config_id: Mapped[int | None] = mapped_column(
        ForeignKey("model_configs.id", ondelete="SET NULL"), nullable=True, index=True
    )
    prompt_template: Mapped[str] = mapped_column(Text)
    input_schema: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    output_schema: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    call_count: Mapped[int] = mapped_column(Integer, default=0)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    model_config: Mapped[ModelConfig | None] = relationship(foreign_keys=[model_config_id])
    run_records: Mapped[list["SkillRunRecord"]] = relationship(
        back_populates="skill", cascade="all, delete-orphan", passive_deletes=True
    )


class SkillRunRecord(Base):
    __tablename__ = "skill_run_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("ai_tools.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(150))
    target: Mapped[str | None] = mapped_column(String(200))
    suggested_action: Mapped[str | None] = mapped_column(Text)
    deliverables: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    skill: Mapped[AiTool] = relationship(back_populates="run_records")


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    knowledge_base_id: Mapped[str] = mapped_column(
        ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True
    )
    filename: Mapped[str] = mapped_column(String(500))
    storage_path: Mapped[str] = mapped_column(String(1000))
    content_type: Mapped[str] = mapped_column(String(150))
    size: Mapped[int] = mapped_column(Integer)
    processing_status: Mapped[str] = mapped_column(String(30), default="processing", index=True)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    knowledge_base: Mapped[KnowledgeBase] = relationship(back_populates="documents")


class AgentKnowledgeBase(Base):
    __tablename__ = "agent_knowledge_bases"
    __table_args__ = (UniqueConstraint("agent_id", "knowledge_base_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), index=True)
    knowledge_base_id: Mapped[str] = mapped_column(
        ForeignKey("knowledge_bases.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    agent_id: Mapped[int | None] = mapped_column(
        ForeignKey("agents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan", passive_deletes=True
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(30), index=True)
    content: Mapped[str] = mapped_column(Text)
    model: Mapped[str | None] = mapped_column(String(150))
    sources: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    conversation: Mapped[Conversation] = relationship(back_populates="messages")

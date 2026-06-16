from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class GrowthTask(Base):
    __tablename__ = "growth_tasks"

    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    prompt: Mapped[str] = mapped_column(Text, default="")
    product: Mapped[str] = mapped_column(String(300), default="")
    market: Mapped[str] = mapped_column(String(300), default="")
    target_customer: Mapped[str] = mapped_column(String(500), default="")
    budget: Mapped[str] = mapped_column(String(200), default="")
    status: Mapped[str] = mapped_column(String(40), index=True, default="pending")
    current_step: Mapped[str] = mapped_column(String(40), default="")
    context: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    agent_outputs: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    pdf_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"
    __table_args__ = {"comment": "工作流任务：每个任务绑定一个AI团队"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("ai_teams.id", ondelete="RESTRICT"), index=True
    )
    name: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    status: Mapped[str] = mapped_column(String(30), default="draft", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class WorkflowTaskAgent(Base):
    __tablename__ = "workflow_task_agents"
    __table_args__ = (
        UniqueConstraint("task_id", "agent_id", name="uq_workflow_task_agents"),
        {"comment": "工作流任务员工：保存团队员工的执行顺序与实时状态"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_tasks.id", ondelete="CASCADE"), index=True
    )
    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id", ondelete="RESTRICT"), index=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, index=True)
    run_status: Mapped[str] = mapped_column(String(30), default="idle", index=True)
    output: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    __table_args__ = {"comment": "工作流运行记录：保存一次顺序执行与最终PDF报告"}

    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    task_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_tasks.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(30), default="running", index=True)
    current_agent_id: Mapped[int | None] = mapped_column(Integer)
    prompt: Mapped[str] = mapped_column(Text)
    report_data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    pdf_path: Mapped[str | None] = mapped_column(String(1000))
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

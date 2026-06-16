from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.models.base import Base

# 多对多中间表
ai_team_agent_table = Table(
    "ai_team_agents",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("team_id", Integer, ForeignKey("ai_teams.id", ondelete="CASCADE"), nullable=False),
    Column("agent_id", Integer, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), default=datetime.utcnow, nullable=False)
)
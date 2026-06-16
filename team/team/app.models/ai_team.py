# from sqlalchemy import Column, Integer, String, Text, TINYINT, DateTime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from app.models.ai_team_agent import ai_team_agent_table


class AiTeam(Base):
    __tablename__ = "ai_teams"
    __table_args__ = {"comment": "AI团队"}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="团队主键")
    name = Column(String(100), nullable=False, unique=True, comment="团队名称")
    description = Column(Text, nullable=True, comment="团队描述")
    enabled = Column(Boolean, default=True, nullable=False, comment="是否启用")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")

    agents = relationship(
        "Agent",
        secondary=ai_team_agent_table,
        lazy="selectin"
    )
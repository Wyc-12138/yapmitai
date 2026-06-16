from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# 基础模型（公共字段）
class AiTeamBase(BaseModel):
    name: str = Field(..., max_length=100, description="团队名称")
    description: Optional[str] = Field(None, description="团队描述")
    enabled: int = Field(1, ge=0, le=1, description="是否启用 0-禁用 1-启用")

# 创建团队 入参
class AiTeamCreate(AiTeamBase):
    pass

# 编辑团队 入参
class AiTeamUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    enabled: Optional[int] = Field(None, ge=0, le=1)

# 团队列表/详情 出参
class AiTeamResponse(AiTeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # 支持ORM对象直接转模型

# 团队+下属AI员工 组合响应（详情页使用）
class AiTeamWithAgents(AiTeamResponse):
    agent_ids: List[int] = Field([], description="团队内AI员工ID列表")
    agent_names: List[str] = Field([], description="团队内AI员工名称列表")

# 绑定/解绑AI员工 入参
class TeamBindAgent(BaseModel):
    agent_ids: List[int] = Field(..., description="要绑定的AI员工ID数组")
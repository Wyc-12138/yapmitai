from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
from app.models.ai_team import AiTeam
from app.models import Agent
from app.pages.enterprise.team_temp.schema import AiTeamCreate, AiTeamUpdate, TeamBindAgent


# 1. 创建团队
async def create_team(db: AsyncSession, data: AiTeamCreate) -> AiTeam:
    team = AiTeam(**data.dict())
    db.add(team)
    await db.commit()
    await db.refresh(team)
    return team

# 2. 查询所有团队（列表）
async def get_team_list(db: AsyncSession) -> List[AiTeam]:
    stmt = select(AiTeam).order_by(AiTeam.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())

# 3. 查询单个团队（含下属AI员工）
async def get_team_detail(db: AsyncSession, team_id: int) -> Optional[AiTeam]:
    stmt = select(AiTeam).where(AiTeam.id == team_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 4. 更新团队
async def update_team(db: AsyncSession, team_id: int, data: AiTeamUpdate) -> Optional[AiTeam]:
    team = await get_team_detail(db, team_id)
    if not team:
        return None
    for k, v in data.dict(exclude_unset=True).items():
        setattr(team, k, v)
    await db.commit()
    await db.refresh(team)
    return team

# 5. 删除团队
async def delete_team(db: AsyncSession, team_id: int) -> bool:
    team = await get_team_detail(db, team_id)
    if not team:
        return False
    await db.delete(team)
    await db.commit()
    return True

# 6. 给团队绑定AI员工（覆盖式绑定）
async def bind_team_agents(db: AsyncSession, team_id: int, agent_ids: List[int]) -> bool:
    team = await get_team_detail(db, team_id)
    if not team:
        return False
    # 清空原有关联
    team.agents.clear()
    # 批量添加新员工
    stmt = select(Agent).where(Agent.id.in_(agent_ids))
    agents = (await db.execute(stmt)).scalars().all()
    team.agents = agents
    await db.commit()
    return True
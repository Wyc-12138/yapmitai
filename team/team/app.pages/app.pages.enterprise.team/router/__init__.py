from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.core.responses import success, failure
from app.pages.enterprise.team_temp import service, schema

router = APIRouter(prefix="/team", tags=["AI团队管理"])
DBDep = Depends(get_db)

# 1. 创建团队
@router.post("/")
async def create_team(
    data: schema.AiTeamCreate,
    db: AsyncSession = DBDep
):
    team = await service.create_team(db, data)
    return success(data=team)

# 2. 获取团队列表
@router.get("/")
async def get_team_list(db: AsyncSession = DBDep):
    teams = await service.get_team_list(db)
    return success(data=teams)

# 3. 获取团队详情（含成员）
@router.get("/{team_id}")
async def get_team_detail(team_id: int, db: AsyncSession = DBDep):
    team = await service.get_team_detail(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="团队不存在")
    # 组装成员信息
    resp = schema.AiTeamWithAgents.from_orm(team)
    resp.agent_ids = [a.id for a in team.agents]
    resp.agent_names = [a.name for a in team.agents]
    return success(data=resp)

# 4. 编辑团队
@router.put("/{team_id}")
async def update_team(
    team_id: int,
    data: schema.AiTeamUpdate,
    db: AsyncSession = DBDep
):
    team = await service.update_team(db, team_id, data)
    if not team:
        raise HTTPException(status_code=404, detail="团队不存在")
    return success(data=team)

# 5. 删除团队
@router.delete("/{team_id}")
async def delete_team(team_id: int, db: AsyncSession = DBDep):
    ok = await service.delete_team(db, team_id)
    if not ok:
        raise HTTPException(status_code=404, detail="团队不存在")
    return success(msg="删除成功")

# 6. 团队绑定AI员工
@router.post("/{team_id}/bind-agents")
async def bind_agents(
    team_id: int,
    data: schema.TeamBindAgent,
    db: AsyncSession = DBDep
):
    ok = await service.bind_team_agents(db, team_id, data.agent_ids)
    if not ok:
        raise HTTPException(status_code=404, detail="团队不存在")
    return success(msg="成员绑定成功")
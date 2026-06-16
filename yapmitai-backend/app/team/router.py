from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.database import get_db
from app.team import service
from app.team.schema import TeamCreate, TeamUpdate

router = APIRouter(prefix="/teams", tags=["AI团队管理"])


@router.get("")
async def list_teams(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_teams(db))


@router.get("/agent-options")
async def list_agent_options(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_agent_options(db))


@router.get("/summary")
async def get_summary(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.team_summary(db))


@router.post("")
async def create_team(
    payload: TeamCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        return success(await service.create_team(db, payload.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/{team_id}")
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    team = await service.get_team(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="团队不存在")
    return success(team)


@router.patch("/{team_id}")
async def update_team(
    team_id: int, payload: TeamUpdate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        team = await service.update_team(
            db, team_id, payload.model_dump(exclude_unset=True)
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not team:
        raise HTTPException(status_code=404, detail="团队不存在")
    return success(team)


@router.delete("/{team_id}")
async def delete_team(team_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    if not await service.delete_team(db, team_id):
        raise HTTPException(status_code=404, detail="团队不存在")
    return success({"deleted": True, "id": team_id})

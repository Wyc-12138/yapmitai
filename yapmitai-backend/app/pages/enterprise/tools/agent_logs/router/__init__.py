from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.postgres import get_db
from .. import service

router = APIRouter(tags=["logs-and-stats"])


@router.get("/logs")
async def get_logs(
    status: str | None = None,
    module: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return success(await service.list_logs(db, status, module))


@router.get("/stats/overview")
async def stats_overview(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.stats(db))


@router.get("/stats/trend")
async def stats_trend(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.trend(db))


@router.get("/stats/distribution")
async def stats_distribution(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.distribution(db))

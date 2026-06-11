from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.db.database import get_db
from .. import service
from ..schema import PolicyQuestion

router = APIRouter(prefix="/government", tags=["government-dashboard"])


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.get_dashboard(db))


@router.post("/policy-question")
async def policy_question(
    payload: PolicyQuestion, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.answer_policy(db, payload.question))

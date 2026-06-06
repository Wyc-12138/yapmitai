from fastapi import APIRouter

from app.core.responses import success
from app.schemas.government import PolicyQuestion
from app.services import government

router = APIRouter(prefix="/government", tags=["government-dashboard"])


@router.get("/dashboard")
async def dashboard() -> dict:
    return success(government.get_dashboard())


@router.post("/policy-question")
async def policy_question(payload: PolicyQuestion) -> dict:
    return success(government.answer_policy(payload.question))

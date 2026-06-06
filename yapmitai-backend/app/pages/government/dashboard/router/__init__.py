from fastapi import APIRouter

from app.core.responses import success
from .. import service
from ..schema import PolicyQuestion

router = APIRouter(prefix="/government", tags=["government-dashboard"])


@router.get("/dashboard")
async def dashboard() -> dict:
    return success(service.get_dashboard())


@router.post("/policy-question")
async def policy_question(payload: PolicyQuestion) -> dict:
    return success(service.answer_policy(payload.question))

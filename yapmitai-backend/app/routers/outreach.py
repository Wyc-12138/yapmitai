from fastapi import APIRouter

from app.core.exceptions import InvalidParameterError
from app.core.responses import success
from app.schemas.outreach import CallTaskRequest, LeadSearchRequest
from app.services import outreach

router = APIRouter(prefix="/outreach", tags=["outreach-agent"])


@router.post("/leads")
async def search_leads(payload: LeadSearchRequest) -> dict:
    return success(await outreach.search_leads(payload.model_dump()))


@router.post("/calls")
async def create_call_task(payload: CallTaskRequest) -> dict:
    if not payload.consentFlag:
        raise InvalidParameterError("consentFlag must be true for outbound calls")
    return success(await outreach.create_call_task(payload.model_dump()))

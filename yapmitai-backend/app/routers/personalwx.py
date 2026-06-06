from fastapi import APIRouter

from app.core.responses import success
from app.schemas.personalwx import PersonalWxMessage
from app.services import personalwx

router = APIRouter(prefix="/personalwx", tags=["personalwx-agent"])


@router.post("/webhook")
async def personalwx_webhook(payload: PersonalWxMessage) -> dict:
    return success(await personalwx.reply(payload.model_dump()))

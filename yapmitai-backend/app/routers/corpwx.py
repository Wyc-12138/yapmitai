from fastapi import APIRouter

from app.core.responses import success
from app.schemas.corpwx import CorpWxMessage
from app.services import corpwx

router = APIRouter(prefix="/corpwx", tags=["corpwx-agent"])


@router.post("/webhook")
async def corpwx_webhook(payload: CorpWxMessage) -> dict:
    return success(await corpwx.reply(payload.model_dump()))

from fastapi import APIRouter

from app.core.responses import success

from ..schema import TranslationBatchRequest
from ..service import translate_batch

router = APIRouter(prefix="/translations", tags=["translations"])


@router.post("/batch")
async def translate_page_text(payload: TranslationBatchRequest) -> dict:
    return success({"translations": await translate_batch(payload.texts)})

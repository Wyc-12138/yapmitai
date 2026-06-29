from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidParameterError
from app.core.responses import success
from app.db.database import get_db
from app.pages.enterprise.inquiry import service
from app.pages.enterprise.inquiry.schema import InquiryAnalyzeRequest, InquiryDeleteRequest

router = APIRouter(prefix="/inquiry", tags=["inquiry-ai"])


@router.post("/analyze")
async def analyze_inquiry(
    payload: InquiryAnalyzeRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    if not payload.inquiry_text.strip():
        raise InvalidParameterError("inquiry_text cannot be empty")
    return success(
        await service.analyze_inquiry(
            db,
            payload.inquiry_text,
            payload.source,
            payload.sample_label,
        )
    )


@router.get("/history")
async def list_history(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_inquiry_history(db))


@router.get("/history/{record_id}")
async def get_history_item(record_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    record = await service.get_inquiry_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Inquiry record not found")
    return success(record)


@router.delete("/history/{record_id}")
async def delete_history_item(record_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    deleted = await service.delete_inquiry_record(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inquiry record not found")
    return success({"id": record_id})


@router.post("/history/delete")
async def delete_history_items(
    payload: InquiryDeleteRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return success(await service.delete_inquiry_records(db, payload.ids))

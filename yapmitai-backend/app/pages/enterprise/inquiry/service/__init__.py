from uuid import uuid4

from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InquiryRecord, ModelConfig
from app.pages.enterprise.inquiry.workflow import InquiryWorkflow


def _serialize_record(record: InquiryRecord) -> dict:
    return {
        "id": record.id,
        "inquiryText": record.inquiry_text,
        "source": record.source,
        "sampleLabel": record.sample_label,
        "status": record.status,
        "steps": record.steps or [],
        "summary": record.summary or {},
        "errorMessage": record.error_message,
        "createdAt": record.created_at.isoformat() if record.created_at else None,
    }


async def _get_default_chat_config(db: AsyncSession) -> ModelConfig | None:
    result = await db.scalars(
        select(ModelConfig)
        .where(ModelConfig.model_type == "chat", ModelConfig.enabled.is_(True))
        .order_by(ModelConfig.is_default.desc(), ModelConfig.id.asc())
        .limit(1)
    )
    return result.first()


async def analyze_inquiry(
    db: AsyncSession,
    inquiry_text: str,
    source: str,
    sample_label: str | None = None,
) -> dict:
    model_config = await _get_default_chat_config(db)
    workflow = InquiryWorkflow(model_config)
    workflow_result = await workflow.run(inquiry_text.strip(), source)

    record_id = f"inq-{uuid4().hex[:12]}"
    record = InquiryRecord(
        id=record_id,
        inquiry_text=inquiry_text.strip(),
        source=source,
        sample_label=sample_label,
        status=workflow_result.get("status", "error"),
        steps=workflow_result.get("steps", []),
        summary=workflow_result.get("summary", {}),
        error_message=workflow_result.get("error"),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    payload = _serialize_record(record)
    payload["inquiry"] = workflow_result.get("inquiry")
    if workflow_result.get("error"):
        payload["error"] = workflow_result["error"]
    return payload


async def list_inquiry_history(db: AsyncSession, limit: int = 50) -> dict:
    rows = (
        await db.scalars(
            select(InquiryRecord)
            .order_by(desc(InquiryRecord.created_at))
            .limit(limit)
        )
    ).all()
    items = [_serialize_record(row) for row in rows]
    return {"items": items, "total": len(items)}


async def get_inquiry_record(db: AsyncSession, record_id: str) -> dict | None:
    record = await db.get(InquiryRecord, record_id)
    if not record:
        return None
    return _serialize_record(record)


async def delete_inquiry_record(db: AsyncSession, record_id: str) -> bool:
    record = await db.get(InquiryRecord, record_id)
    if not record:
        return False
    await db.delete(record)
    await db.commit()
    return True


async def delete_inquiry_records(db: AsyncSession, record_ids: list[str]) -> dict:
    unique_ids = list(dict.fromkeys(record_ids))
    if not unique_ids:
        return {"deleted": 0, "ids": []}

    rows = (
        await db.scalars(select(InquiryRecord).where(InquiryRecord.id.in_(unique_ids)))
    ).all()
    deleted_ids = [row.id for row in rows]
    if deleted_ids:
        await db.execute(delete(InquiryRecord).where(InquiryRecord.id.in_(deleted_ids)))
        await db.commit()
    return {"deleted": len(deleted_ids), "ids": deleted_ids}

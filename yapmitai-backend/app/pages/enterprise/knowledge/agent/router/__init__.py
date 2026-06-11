from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.responses import success
from app.core.exceptions import InvalidParameterError
from app.db.database import get_db
from .. import service
from ..schema import (
    KnowledgeQuery,
    LocalKnowledgeCreate,
    LocalKnowledgeUpdate,
    KnowledgeModelConfigUpdate,
    KnowledgeModelTest,
)

router = APIRouter(prefix="/knowledge", tags=["knowledge-agent"])


@router.get("/status")
async def status(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.status(db))


@router.post("/query")
async def query(payload: KnowledgeQuery, db: AsyncSession = Depends(get_db)) -> dict:
    return success(
        await service.query(
            db,
            payload.query,
            payload.limit,
            payload.answer_model,
            payload.knowledge_base_id,
            payload.conversation_id,
        )
    )


@router.get("/model-config")
async def get_model_config(
    knowledge_base_id: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return success(await service.get_model_config(db, knowledge_base_id))


@router.get("/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db)) -> dict:
    return success(await service.list_conversations(db))


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str, db: AsyncSession = Depends(get_db)
) -> dict:
    conversation = await service.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return success(conversation)


@router.put("/model-config")
async def update_model_config(
    payload: KnowledgeModelConfigUpdate, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        config = await service.update_model_config(
            db,
            payload.knowledge_base_id,
            payload.embedding_model,
            payload.answer_model,
        )
    except ValueError as exc:
        raise InvalidParameterError(str(exc)) from exc
    return success(config)


@router.post("/model-test")
async def test_models(
    payload: KnowledgeModelTest, db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        result = await service.test_models(
            db, payload.knowledge_base_id, payload.text
        )
    except ValueError as exc:
        raise InvalidParameterError(str(exc)) from exc
    return success(result)


@router.get("/local-libraries")
async def list_local_libraries(
    keyword: str | None = None,
    knowledge_type: str | None = Query(default=None, pattern="^(text|image)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> dict:
    return success(
        await service.list_local_libraries(
            db,
            keyword=keyword,
            knowledge_type=knowledge_type,
            page=page,
            page_size=page_size,
        )
    )


@router.post("/local-libraries")
async def create_local_library(
    payload: LocalKnowledgeCreate, db: AsyncSession = Depends(get_db)
) -> dict:
    return success(await service.create_local_library(db, payload.model_dump()))


@router.get("/local-libraries/{library_id}")
async def get_local_library(
    library_id: str, db: AsyncSession = Depends(get_db)
) -> dict:
    library = await service.get_local_library(db, library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Local knowledge library not found")
    return success(library)


@router.patch("/local-libraries/{library_id}")
async def update_local_library(
    library_id: str,
    payload: LocalKnowledgeUpdate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    library = await service.update_local_library(
        db,
        library_id,
        payload.model_dump(exclude_none=True),
    )
    if not library:
        raise HTTPException(status_code=404, detail="Local knowledge library not found")
    return success(library)


@router.delete("/local-libraries/{library_id}")
async def delete_local_library(
    library_id: str, db: AsyncSession = Depends(get_db)
) -> dict:
    if not await service.delete_local_library(db, library_id):
        raise HTTPException(status_code=404, detail="Local knowledge library not found")
    return success({"deleted": True, "libraryId": library_id})


@router.post("/local-libraries/{library_id}/collections")
async def upload_collection(
    library_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> dict:
    content = await file.read()
    collection = await service.add_document(
        db=db,
        library_id=library_id,
        filename=file.filename or "unnamed",
        content_type=file.content_type,
        content=content,
    )
    if not collection:
        raise HTTPException(status_code=404, detail="Local knowledge library not found")
    return success(collection)

from fastapi import APIRouter, HTTPException

from app.core.responses import success
from app.schemas.knowledge import KnowledgeQuery, KnowledgeSyncRequest
from app.services import knowledge

router = APIRouter(prefix="/knowledge", tags=["knowledge-agent"])


@router.post("/sync")
async def sync(payload: KnowledgeSyncRequest) -> dict:
    return success(knowledge.start_sync(payload.sources))


@router.get("/sync/{task_id}")
async def sync_status(task_id: str) -> dict:
    result = knowledge.sync_status(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sync task not found")
    return success(result)


@router.get("/status")
async def status() -> dict:
    return success(knowledge.status())


@router.post("/query")
async def query(payload: KnowledgeQuery) -> dict:
    return success(knowledge.query(payload.query, payload.limit))

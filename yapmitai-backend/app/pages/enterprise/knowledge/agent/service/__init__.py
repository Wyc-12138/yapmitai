from uuid import uuid4

SYNC_TASKS: dict[str, dict] = {}


def start_sync(sources: list[str]) -> dict:
    task_id = str(uuid4())
    SYNC_TASKS[task_id] = {"taskId": task_id, "progress": 100, "status": "completed", "sources": sources}
    return SYNC_TASKS[task_id]


def sync_status(task_id: str) -> dict | None:
    return SYNC_TASKS.get(task_id)


def status() -> dict:
    return {"count": 1284, "lastSyncAt": "2 minutes ago", "status": "ready"}


def query(text: str, limit: int) -> dict:
    return {
        "query": text,
        "results": [
            {"content": "海南自贸港企业所得税优惠政策示例内容", "score": 0.94, "source": "external-vector"},
            {"content": "品牌出海补贴申报流程示例内容", "score": 0.87, "source": "system-keyword"},
        ][:limit],
    }

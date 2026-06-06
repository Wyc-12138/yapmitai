from app.middleware.call_logging import CALL_LOG_STORE


def list_logs(status: str | None = None, module: str | None = None) -> list[dict]:
    items = CALL_LOG_STORE
    if status:
        items = [item for item in items if item["status"] == status]
    if module:
        items = [item for item in items if module in item["path"]]
    return items


def stats() -> dict:
    total = len(CALL_LOG_STORE)
    successful = sum(item["status"] == "success" for item in CALL_LOG_STORE)
    average = round(sum(item["latency_ms"] for item in CALL_LOG_STORE) / total) if total else 0
    return {
        "calls": total,
        "successRate": round(successful / total * 100, 2) if total else 100,
        "averageLatencyMs": average,
        "cost": 0,
    }

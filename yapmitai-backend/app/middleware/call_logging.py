import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


@dataclass
class CallLog:
    request_at: str
    response_at: str
    path: str
    method: str
    status: str
    latency_ms: int


CALL_LOG_STORE: list[dict] = []


class CallLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        started_at = datetime.now(UTC)
        started = time.perf_counter()
        response = await call_next(request)
        latency_ms = round((time.perf_counter() - started) * 1000)
        if "/api/v1/" in request.url.path:
            item = CallLog(
                request_at=started_at.isoformat(),
                response_at=datetime.now(UTC).isoformat(),
                path=request.url.path,
                method=request.method,
                status="success" if response.status_code < 400 else "failed",
                latency_ms=latency_ms,
            )
            CALL_LOG_STORE.insert(0, asdict(item))
            del CALL_LOG_STORE[200:]
        response.headers["X-Trace-Latency-Ms"] = str(latency_ms)
        return response

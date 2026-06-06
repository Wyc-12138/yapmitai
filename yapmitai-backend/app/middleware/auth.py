from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.core.responses import failure


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        protected_prefix = get_settings().api_v1_prefix
        if request.url.path.startswith(protected_prefix):
            supplied_key = request.headers.get("X-API-Key")
            if supplied_key != get_settings().api_key:
                return JSONResponse(
                    status_code=401,
                    content=failure(401, "Unauthorized: invalid X-API-Key"),
                )
        return await call_next(request)

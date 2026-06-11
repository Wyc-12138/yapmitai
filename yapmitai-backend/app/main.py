from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.core.responses import failure, success
from app.middleware.auth import ApiKeyMiddleware
from app.middleware.call_logging import CallLoggingMiddleware
from app.growth.router import router as growth_router
from app.pages import api_router
from app.db.postgres import init_database

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_database()
    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="YAPMITAI Demo 2.0 Agent Gateway backend",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CallLoggingMiddleware)
app.add_middleware(ApiKeyMiddleware)
app.include_router(api_router, prefix=settings.api_v1_prefix)
app.include_router(growth_router)


@app.exception_handler(AppError)
async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=failure(exc.code, exc.message),
    )


@app.exception_handler(StarletteHTTPException)
async def handle_http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=failure(exc.status_code, str(exc.detail)),
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=failure(4003, "Invalid request parameters", exc.errors()),
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=failure(5000, f"Internal server error: {exc}"),
    )


@app.get("/health", tags=["system"])
async def health() -> dict:
    return success(
        {
            "status": "healthy",
            "environment": settings.app_env,
            "gateway": settings.agent_gateway_url,
        }
    )

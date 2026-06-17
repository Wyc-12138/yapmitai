"""Demo media schemas — text-to-image / text-to-video request/response."""

from pydantic import BaseModel, Field


class TextToImageRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)
    size: str = Field(default="1024x1024", max_length=20)
    style: str = Field(default="natural", max_length=50)
    quantity: int = Field(default=1, ge=1, le=4)


class TextToImageResponse(BaseModel):
    url: str
    filename: str
    size: str
    prompt: str


class TextToVideoRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)
    ratio: str = Field(default="16:9", max_length=10)
    duration: int = Field(default=5, ge=3, le=30)
    style: str = Field(default="cinematic", max_length=50)


class TextToVideoResponse(BaseModel):
    task_id: str
    status: str  # pending | running | completed | failed


class VideoStatusResponse(BaseModel):
    task_id: str
    status: str  # pending | running | completed | failed
    url: str | None = None
    filename: str | None = None
    error: str | None = None

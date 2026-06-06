from pydantic import BaseModel, Field


class ImageCreateRequest(BaseModel):
    prompt: str = Field(min_length=2, max_length=2000)
    style: str = "commercial"
    size: str = "1024x1024"
    quality: str = "standard"


class VideoCreateRequest(BaseModel):
    prompt: str = Field(min_length=2, max_length=2000)
    duration: int = Field(default=15, ge=5, le=60)
    resolution: str = "1080p"
    language: str = "zh-CN"

from pydantic import BaseModel, Field


class InquiryAnalyzeRequest(BaseModel):
    inquiry_text: str = Field(min_length=1)
    source: str = "WhatsApp"
    sample_label: str | None = None


class InquiryDeleteRequest(BaseModel):
    ids: list[str] = Field(min_length=1)

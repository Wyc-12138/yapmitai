from pydantic import BaseModel


class TalentAssistantRequest(BaseModel):
    assistant: str
    prompt: str

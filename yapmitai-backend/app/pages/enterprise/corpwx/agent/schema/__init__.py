from pydantic import BaseModel


class CorpWxMessage(BaseModel):
    contact_id: str
    department: str
    content: str
    takeover_mode: str = "managed"

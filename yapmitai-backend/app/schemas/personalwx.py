from pydantic import BaseModel


class PersonalWxMessage(BaseModel):
    contact_id: str
    content: str
    takeover_mode: str = "assisted"

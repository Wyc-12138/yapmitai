from pydantic import BaseModel


class ToolToggle(BaseModel):
    enabled: bool

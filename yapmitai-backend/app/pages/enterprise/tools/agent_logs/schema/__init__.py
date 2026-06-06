from pydantic import BaseModel


class LogFilter(BaseModel):
    module: str | None = None
    status: str | None = None

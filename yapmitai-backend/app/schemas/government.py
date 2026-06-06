from pydantic import BaseModel


class PolicyQuestion(BaseModel):
    question: str

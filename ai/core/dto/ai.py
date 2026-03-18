from pydantic import BaseModel


class AiResponse(BaseModel):
    text: str
    usage: int

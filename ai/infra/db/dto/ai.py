from __future__ import annotations

from pydantic import BaseModel


class AiModel(BaseModel):
    id: int = 1
    name: str
    ai_types: int
    price: str


class AiType(BaseModel):
    id: int = 1
    name: str

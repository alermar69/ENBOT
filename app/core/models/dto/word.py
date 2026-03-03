from __future__ import annotations

from pydantic import BaseModel


class Word(BaseModel):
    en: str
    ru: str | None = None
    trans: str | None = None
    ru_full: str | None = None
    audio_id: str | None = None
    image_id: str | None = None

    # def to_orm(self) -> Base:
    #     return WordModel(**self.model_dump())

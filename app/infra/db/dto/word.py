from __future__ import annotations

from pydantic import BaseModel


class Word(BaseModel):
    id: int = 1
    en: str
    ru: str | None = None
    trans: str | None = None
    trans_full: str | None = None
    ru_full: str | None = None
    audio_id: str | None = None
    image_id: str | None = None


class WordsUsers(BaseModel):
    id: int = 1
    word_id: int
    user_id: int
    stage: int = 1

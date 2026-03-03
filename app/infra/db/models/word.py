from core.models import dto
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    en: Mapped[str] = mapped_column(String(50), nullable=False)
    ru: Mapped[str] = mapped_column(String(50), nullable=True)
    trans: Mapped[str] = mapped_column(String(50), nullable=True)
    ru_full: Mapped[str] = mapped_column(Text, nullable=True)
    audio_id = mapped_column(Text, nullable=True)
    image_id = mapped_column(Text, nullable=True)

    def to_dto(self) -> dto.Word:
        return dto.Word.model_validate(self, from_attributes=True)


class WordsUsers(Base):
    __tablename__ = "words_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    stage: Mapped[int]

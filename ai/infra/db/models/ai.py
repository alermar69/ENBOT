from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AiType(Base):
    __tablename__ = "ai_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class AiModel(Base):
    __tablename__ = "ai_models"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    ai_types: Mapped[int] = mapped_column(ForeignKey("ai_types.id"))
    price: Mapped[str] = mapped_column(String(25))

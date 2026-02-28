from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import dto
from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )
    tg_id: Mapped[int] = mapped_column(
        BigInteger, index=True, unique=True, nullable=False
    )
    lang: Mapped[str] = mapped_column(Text, default="en", nullable=False)
    first_name: Mapped[str] = mapped_column(String(15), nullable=False)
    last_name: Mapped[str] = mapped_column(String(15), nullable=True)
    username = mapped_column(Text, nullable=True)
    hashed_password = mapped_column(Text, nullable=True)
    is_bot = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        rez = (
            f"<User "
            f"id={self.id} "
            f"tg_id={self.tg_id} "
            f"name={self.first_name} {self.last_name} "
        )
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"

    def to_dto(self) -> dto.User:
        return dto.User(
            db_id=self.id,
            tg_id=self.tg_id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            is_bot=self.is_bot,
        )

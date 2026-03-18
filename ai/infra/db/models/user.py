from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

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
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True, nullable=False)
    lang: Mapped[str] = mapped_column(Text, default="en", nullable=False)
    first_name: Mapped[str] = mapped_column(String(15), nullable=False)
    last_name: Mapped[str] = mapped_column(String(15), nullable=True)
    username = mapped_column(Text, nullable=True)
    hashed_password = mapped_column(Text, nullable=True)
    is_bot = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        rez = f"<User id={self.id} tg_id={self.tg_id} name={self.first_name} {self.last_name} "
        if self.username:
            rez += f"username=@{self.username}"
        return rez + ">"

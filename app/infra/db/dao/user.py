import typing
from datetime import datetime, tzinfo
from typing import Sequence

from infra.db.models.user import User
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db import dto
from .base import BaseDAO
from .mappers.mappers import UserDataMapper


class UserDao(BaseDAO[User, UserDataMapper]):
    def __init__(
        self, session: AsyncSession, clock: typing.Callable[[tzinfo], datetime] = datetime.now
    ) -> None:
        super().__init__(User, UserDataMapper, session, clock=clock)

    async def get_by_username_with_password(self, username: str) -> dto.UserWithCreds:
        user: dto.User = await self.get_one(username=username)
        return user.add_password(user.hashed_password)

    async def set_password(self, user: dto.User, hashed_password: str):
        assert user.db_id
        db_user = await self._get_by_id(user.db_id)
        db_user.hashed_password = hashed_password

    async def get_page(self, offset: int, limit: int) -> Sequence[dto.User]:
        result: ScalarResult[User] = await self.session.scalars(
            select(User).offset(offset).limit(limit)
        )
        return [user.to_dto() for user in result.all()]

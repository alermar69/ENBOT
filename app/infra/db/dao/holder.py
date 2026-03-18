import typing
from datetime import datetime, tzinfo

from infra.db.dao.user import UserDao
from infra.db.dao.word import WordDao, WordsUsersDao
from sqlalchemy.ext.asyncio import AsyncSession


class HolderDao:
    def __init__(
        self,
        session: AsyncSession,
        clock: typing.Callable[[tzinfo], datetime] = datetime.now,
    ) -> None:
        self.session = session
        self.clock = clock
        self.user = UserDao(self.session, clock=clock)
        self.word = WordDao(self.session, clock=clock)
        self.word_users = WordsUsersDao(self.session, clock=clock)

    async def commit(self):
        await self.session.commit()

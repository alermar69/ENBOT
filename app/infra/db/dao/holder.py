import typing
from datetime import datetime, tzinfo


from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.dao.user import UserDao


class HolderDao:
    def __init__(
        self,
        session: AsyncSession,
        clock: typing.Callable[[tzinfo], datetime] = datetime.now,
    ) -> None:
        self.session = session
        self.clock = clock
        self.user = UserDao(self.session, clock=clock)


    async def commit(self):
        await self.session.commit()


    # @property
    # def team_creator(self) -> TeamCreator:
    #     return TeamCreatorImpl(dao=self)

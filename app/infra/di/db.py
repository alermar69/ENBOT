from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from infra.db.dao.holder import HolderDao
from infra.db.factory import create_engine, create_session_maker


class DbProvider(Provider):
    scope = Scope.APP

    def __init__(self):
        super().__init__()

    @provide
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine = create_engine()
        yield engine
        await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, pool: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session


class DAOProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_dao(
        self, session: AsyncSession
    ) -> HolderDao:
        return HolderDao(session=session)


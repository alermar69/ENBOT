import logging
import os
from typing import Iterable

from dishka import Provider, Scope, provide
from infra.db.dao.holder import HolderDao
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer

logger = logging.getLogger(__name__)


class TestDbProvider(Provider):
    scope = Scope.APP

    @provide
    def get_db_config(self) -> Iterable[PostgresContainer]:
        postgres = PostgresContainer("postgres:16.1")
        if os.name == "nt":  # TODO workaround from testcontainers/testcontainers-python#108
            postgres.get_container_host_ip = lambda: "localhost"
        try:
            postgres.start()
            postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
            logger.info("postgres url %s", postgres_url_)
            yield postgres
        finally:
            postgres.stop()

    @provide(scope=Scope.REQUEST)
    async def get_dao(
        self,
        session: AsyncSession,
    ) -> HolderDao:
        return HolderDao(session=session)

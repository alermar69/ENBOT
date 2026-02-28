import logging

from core.config import settings

# from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)


def create_pool() -> async_sessionmaker[AsyncSession]:
    engine = create_engine()
    return create_session_maker(engine)


def create_engine() -> AsyncEngine:
    return create_async_engine(url=settings.db.async_url, echo=settings.db.sqla.echo)


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )
    return pool


# def create_redis(config: RedisConfig) -> Redis:
#     logger.info("created redis for %s", config)
#     return Redis(host=config.url, port=config.port, db=config.db)

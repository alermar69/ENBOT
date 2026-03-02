import logging

import pytest
import pytest_asyncio
from aiogram import Bot, Dispatcher
from aiogram_dialog.api.protocols import MessageManagerProtocol
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from core.config import settings, struct_logs
from core.config.settings import CONFIG_DIR
from dataclass_factory import Factory
from dishka import AsyncContainer, Provider, Scope, make_async_container
from infra.db.dao.holder import HolderDao
from infra.di import DbProvider, DpProvider, NatsProvider
from tests.fixtures.db_provider import TestDbProvider
from tests.mocks.bot import MockBotProvider, MockMessageManagerProvider

logger = logging.getLogger(__name__)

struct_logs.startup(settings.structlog)


@pytest_asyncio.fixture(scope="session")
async def dishka():
    mock_provider = Provider(scope=Scope.APP)
    # mock_provider.provide(GameLogWriterMock, provides=GameLogWriter)
    container = make_async_container(
        TestDbProvider(),
        DbProvider(),
        NatsProvider(),
        DpProvider(),
        MockBotProvider(),
        MockMessageManagerProvider(),
        mock_provider,
    )
    yield container
    await container.close()


@pytest_asyncio.fixture(scope="session")
async def dcf(dishka: AsyncContainer) -> Factory:
    return await dishka.get(Factory)


@pytest_asyncio.fixture
async def dishka_request(dishka: AsyncContainer):
    async with dishka() as request_container:
        yield request_container


@pytest_asyncio.fixture
async def dao(dishka_request: AsyncContainer) -> HolderDao:
    dao_ = await dishka_request.get(HolderDao)
    await clear_data(dao_)
    return dao_


@pytest_asyncio.fixture
async def check_dao(dishka: AsyncContainer):
    async with dishka() as request_container:
        yield await request_container.get(HolderDao)


async def clear_data(dao: HolderDao):
    await dao.user.delete_all()
    await dao.commit()


@pytest_asyncio.fixture(scope="session")
async def message_manager(dishka: AsyncContainer) -> MessageManagerProtocol:
    return await dishka.get(MessageManagerProtocol)


@pytest_asyncio.fixture(scope="session")
async def dp(dishka: AsyncContainer) -> Dispatcher:
    return await dishka.get(Dispatcher)


@pytest_asyncio.fixture
async def bot(dishka: AsyncContainer) -> Bot:
    return await dishka.get(Bot)


@pytest_asyncio.fixture(scope="session")
async def alembic_config(dishka: AsyncContainer) -> AlembicConfig:
    alembic_cfg = AlembicConfig(str(CONFIG_DIR.parent / "alembic.ini"))
    alembic_cfg.set_main_option(
        "script_location",
        str(CONFIG_DIR.parent / "app" / "infra" / "db" / "alembic"),
    )
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        settings.db.async_url.render_as_string(hide_password=False),
    )
    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config: AlembicConfig):
    upgrade(alembic_config, "head")

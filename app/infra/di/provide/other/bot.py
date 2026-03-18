from typing import AsyncIterable

import orjson
import structlog
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Chat, TelegramObject, User
from aiogram_dialog import BgManagerFactory, setup_dialogs
from aiogram_dialog.api.protocols import MessageManagerProtocol
from aiogram_dialog.manager.message_manager import MessageManager
from aiogram_dialog.widgets.text import setup_jinja
from bot.handling.dialogs import router as dialogs_router
from bot.handling.handlers import get_user_router, start_router
from bot.handling.middlewares import LoggingMiddleware, TrackAllUsersMiddleware
from bot.handling.middlewares.init_middleware import InitMiddleware
from bot.handling.middlewares.translator import TranslatorRunnerMiddleware
from bot.nats_storage import NATSFSMStorage
from core.config import settings
from dishka import AsyncContainer, Provider, Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData, setup_dishka
from faststream.nats import NatsBroker

logger = structlog.get_logger(__name__)


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self) -> AsyncIterable[Bot]:
        async with Bot(
            token=settings.bot.token.get_secret_value(),
            session=settings.bot.create_session(),
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML,
                allow_sending_without_reply=True,
            ),
        ) as bot:
            setup_jinja(bot)
            yield bot

    @provide(scope=Scope.REQUEST)
    async def get_user(self, obj: TelegramObject) -> User:
        return obj.from_user

    @provide(scope=Scope.REQUEST)
    async def get_chat(
        self,
        middleware_data: AiogramMiddlewareData,
    ) -> Chat | None:
        return middleware_data.get("event_chat")


class DpProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_dispatcher(
        self,
        dishka: AsyncContainer,
        nc: NatsBroker,
    ) -> Dispatcher:
        kv_states = await nc.key_value(settings.bot.fsm.states_bucket, declare=False)
        kv_data = await nc.key_value(settings.bot.fsm.data_bucket, declare=False)
        if settings.MODE == "TEST":
            dp = Dispatcher(storage=MemoryStorage())
        else:
            dp = Dispatcher(
                storage=NATSFSMStorage(
                    kv_states, kv_data, serializer=orjson.dumps, deserializer=orjson.loads
                ),
            )

        setup_dialogs(dp)
        dp.update.middleware(LoggingMiddleware())
        t = TranslatorRunnerMiddleware()
        dp.message.middleware(t)
        dp.callback_query.middleware(t)
        dp.message.middleware(TrackAllUsersMiddleware())
        dp.update.middleware(InitMiddleware())

        dp.include_routers(start_router, get_user_router, dialogs_router)
        setup_dishka(container=dishka, router=dp)
        return dp


class DialogManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_manager(self) -> MessageManagerProtocol:
        return MessageManager()

    @provide
    async def get_background_router(
        self,
        message_manager: MessageManagerProtocol,
        dp: Dispatcher,
    ) -> BgManagerFactory:
        bg_manager = setup_dialogs(dp, message_manager=message_manager)
        return bg_manager

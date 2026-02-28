import logging
from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

# from aiogram.fsm.storage.redis import (
#     DefaultKeyBuilder,
#     RedisEventIsolation,
#     RedisStorage,
# )
from aiogram.types import TelegramObject
from aiogram_dialog.api.protocols import MessageManagerProtocol
from aiogram_dialog.manager.message_manager import MessageManager
from dishka import (
    STRICT_VALIDATION,
    AnyOf,
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from dishka.integrations.aiogram import AiogramMiddlewareData, setup_dishka
from infra.di import get_providers

logger = logging.getLogger(__name__)


def create_dishka() -> AsyncContainer:
    container = make_async_container(*get_bot_providers())
    return container


def get_bot_providers() -> list[Provider]:
    return [
        *get_providers(),
        DialogManagerProvider(),
    ]


class DialogManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_manager(self) -> MessageManagerProtocol:
        return MessageManager()


def resolve_update_types(dp: Dispatcher) -> list[str]:
    return dp.resolve_used_update_types(skip_events={"aiogd_update"})

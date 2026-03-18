from typing import Protocol, cast

from aiogram import types
from bot.utils.data import SHMiddlewareData
from dishka import (
    Provider,
    Scope,
    from_context,
    provide,
)
from dishka.integrations.aiogram import AiogramMiddlewareData, AiogramProvider
from infra.db import dto
from infra.db.dao.holder import HolderDao

from .bot import BotProvider, DialogManagerProvider, DpProvider

__all__ = [
    "BotProvider",
    "DialogManagerProvider",
    "DpProvider",
    "get_providers",
]


def get_providers():
    return [
        AiogramProvider(),
        BotProvider(),
        DpProvider(),
        DialogManagerProvider(),
        BotIdpProvider(),
    ]


class IdentityProvider(Protocol):
    async def get_user(self) -> dto.User | None:
        raise NotImplementedError


class TgBotIdentityProvider(IdentityProvider):
    def __init__(
        self,
        *,
        # event: TelegramObject,
        dao: HolderDao,
        aiogram_data: AiogramMiddlewareData,
    ) -> None:
        # self.event = event
        self.dao = dao
        self.aiogram_data = aiogram_data

    async def get_user(self) -> dto.User | None:
        data = cast(SHMiddlewareData, self.aiogram_data)
        user_tg: types.User | None
        if user_tg := data.get("event_from_user", None):
            user = await self.dao.user.get_by_tg_id(user_tg.id)
        else:
            user = None
        return user


class BotIdpProvider(Provider):
    scope = Scope.REQUEST
    # event = from_context(TelegramObject)
    aiogram_data = from_context(AiogramMiddlewareData)
    bot_idp = provide(TgBotIdentityProvider)

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.utils.data import SHMiddlewareData
from faststream.nats import NatsBroker
from infra.db.dao.holder import HolderDao


class InitMiddleware(BaseMiddleware):
    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: SHMiddlewareData,
    ) -> Any:
        dishka = data["dishka_container"]
        data["dao"] = await dishka.get(HolderDao)
        data["nats"] = await dishka.get(NatsBroker)
        result = await handler(event, data)  # type: ignore[arg-type]
        return result

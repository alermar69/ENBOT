from typing import Awaitable

import structlog
from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs
from bot.handling.filters import ChatType, ChatTypeFilter
from bot.handling.handlers import get_user_router, start_router
from bot.handling.middlewares import (
    TranslatorRunnerMiddleware,
)
from bot.handling.middlewares.logging import LoggingMiddleware

logger = structlog.getLogger("schema")


async def assemble(dispatcher_factory: Awaitable[Dispatcher]) -> Dispatcher:
    dp = await dispatcher_factory
    setup_dialogs(dp)
    dp.update.middleware(LoggingMiddleware())
    t = TranslatorRunnerMiddleware()
    dp.message.middleware(t)
    dp.callback_query.middleware(t)
    dp.update.filter(ChatTypeFilter(ChatType.private))
    dp.include_routers(start_router, get_user_router)
    return dp

import structlog
from aiogram import Dispatcher
from aiogram_dialog.api.protocols import BgManagerFactory, MessageManagerProtocol

from . import base, errors
from .get_user import get_user_router
from .start import start_router

__all__ = ["start_router", "get_user_router"]


# logger = structlog.get_logger(__name__)
#
#
# def setup_handlers(
#     dp: Dispatcher, message_manager: MessageManagerProtocol
# ) -> BgManagerFactory:
#     # errors.setup(dp, bot_config.log_chat)
#     dp.include_router(base.setup())
#
#     bg_manager_factory = dialogs.setup(dp, message_manager)
#
#     logger.debug("handlers configured successfully")
#     return bg_manager_factory

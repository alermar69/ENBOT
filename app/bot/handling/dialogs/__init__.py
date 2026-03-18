__all__ = [
    "router",
    "words",
]

from aiogram import Router

from .schedules.dialogs import dialog as words

# from .base_commands import router as base_commands_router
# from .user_commands import router as user_commands_router
from .sentence.dialogs import dialog as sentence

router = Router(name=__name__)

router.include_routers(
    sentence,
    words,
)

import logging

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from bot.handling.views.commands import (
    ABOUT_COMMAND,
    CANCEL_COMMAND,
    CHAT_TYPE_COMMAND,
    HELP_COMMAND,
    HELP_USER,
)
from core.models import dto

logger = logging.getLogger(__name__)


async def cancel_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logger.info("Cancelling state %s", current_state)
    # Cancel state and inform user about it
    await state.clear()
    # And remove keyboard (just in case)
    await message.reply(
        "Диалог прекращён, данные удалены", reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
    )


async def cmd_about(message: Message, user: dto.User):
    logger.info("User %s read about in %s", user.tg_id)
    await message.reply("Разработчик бота - @bomzheg\n")


async def cmd_help(message: Message):
    await message.reply(HELP_USER)


async def chat_type_cmd_supergroup(message: Message):
    await message.reply(
        "Группа имеет тип supergroup, "
        "ты можешь создать команду в этом чате, отправив /create_team",
    )


async def chat_type_cmd_group(message: Message):
    await message.reply(
        "Группа имеет тип group, "
        "чтобы создать команду в этом чате - преобразуй группу в супергруппу"
        "https://telegra.ph/Preobrazovanie-gruppy-v-supergruppu-08-25",
    )


def setup() -> Router:
    router = Router(name=__name__)

    router.message.register(cmd_help, Command(HELP_COMMAND))
    router.message.register(cmd_about, Command(commands=ABOUT_COMMAND))
    router.message.register(cmd_about, Command(commands="developer_info"))
    router.message.register(
        chat_type_cmd_group, Command(commands=CHAT_TYPE_COMMAND), F.chat.type == ChatType.GROUP
    )

    router.message.register(
        chat_type_cmd_supergroup,
        Command(commands=CHAT_TYPE_COMMAND),
        F.chat.type == ChatType.SUPERGROUP,
    )
    router.message.register(
        cancel_state, Command(commands=CANCEL_COMMAND), F.chat.type != ChatType.PRIVATE
    )
    return router

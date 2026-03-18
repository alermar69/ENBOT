from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from bot.handling.states.en_text_translate import EnTextTranslateSG
from bot.utils.read_en_file import read_text
from faststream import FastStream
from infra.db.dao.holder import HolderDao
from infra.db.dto import User
from sqlalchemy.exc import NoResultFound
from structlog import get_logger

start_router = Router()

logger = get_logger(__name__)

dialog_manager_gl: DialogManager | None = None


@start_router.message(CommandStart())
async def handler(
    msg: Message,
    dialog_manager: DialogManager,
    dao: HolderDao,
    app_faststream: FastStream,
):
    app_faststream.context.set_global("dialog_manager", dialog_manager)
    await logger.info(msg.from_user)
    try:
        user = await dao.user.get_one(tg_id=msg.from_user.id)
    except NoResultFound:
        user = await dao.user.add(User.from_aiogram(msg.from_user))
        await dao.commit()

    ls_txt = read_text("en_text.txt")

    await dialog_manager.start(
        EnTextTranslateSG.show_text_en,
        mode=StartMode.RESET_STACK,
        data={
            "ls_text_en": ls_txt,
            "user": user.model_dump(),
        },
    )

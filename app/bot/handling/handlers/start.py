from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from bot.handling.states.en_text_translate import EnTextTranslateSG
from bot.utils.read_en_file import read_text
from core.models.dto import User
from fluentogram import TranslatorRunner
from infra.db.dao.holder import HolderDao
from sqlalchemy.exc import NoResultFound
from structlog import get_logger

start_router = Router()

logger = get_logger(__name__)

# @start_router.message(Command("start"))
# async def handler(msg: Message, dialog_manager: DialogManager, i18n: TranslatorRunner):
#     await dialog_manager.start(Watermark.enter_text, mode=StartMode.RESET_STACK)


@start_router.message(CommandStart())
async def handler(
    msg: Message,
    dialog_manager: DialogManager,
    dao: HolderDao,
    i18n: TranslatorRunner,
    state: FSMContext,
):
    # await msg.answer("Привет!")
    try:
        user = await dao.user.get_by_tg_id(msg.from_user.id)
    except NoResultFound:
        user = await dao.user.upsert_user(User.from_aiogram(msg.from_user))
        await dao.commit()

    ls_txt = read_text("en_text.txt")
    # await state.update_data(ls_text_en=ls_txt)
    await dialog_manager.start(
        EnTextTranslateSG.show_text_en,
        mode=StartMode.RESET_STACK,
        data={"ls_text_en": ls_txt},
    )

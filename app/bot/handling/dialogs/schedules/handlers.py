from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from bot.handling.states.en_text_translate import WordsScheduleSG
from dishka.integrations.aiogram_dialog import FromDishka, inject
from infra.db import dto
from infra.db.dao.holder import HolderDao
from structlog import get_logger

logger = get_logger(__name__)


async def select_word(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    n_word = int(item_id) // 3
    n_attr = int(item_id) % 3
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["n_word"] = n_word
    data["n_attr"] = n_attr
    if n_attr == 0:
        await manager.switch_to(WordsScheduleSG.stage)
    elif n_attr == 1:
        await manager.switch_to(WordsScheduleSG.full_ru)
    elif n_attr == 2:
        await manager.switch_to(WordsScheduleSG.full_trans)


async def on_off_word_ru(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    is_show_ru = dialog_manager.dialog_data.get("is_show_ru")
    dialog_manager.dialog_data.update(is_show_ru=not is_show_ru)


@inject
async def select_stage(
    c: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    item_id: str,
    dao: FromDishka[HolderDao],
):
    await c.answer()
    word: dto.Word = dto.Word.model_validate(dialog_manager.dialog_data.get("word"))
    word_users: dto.WordsUsers = dto.WordsUsers.model_validate(
        dialog_manager.dialog_data.get("word_users"),
    )
    word_users.stage = int(item_id)
    await logger.info(item_id)

    n_word: int = int(dialog_manager.dialog_data.get("n_word"))
    n_attr: int = int(dialog_manager.dialog_data.get("n_attr"))
    words_stage: list[tuple[dto.Word, dto.WordsUsers]] = dialog_manager.start_data.get(
        "words_stage"
    )
    word_users1: dict = words_stage[n_word][1]
    word_users1["stage"] = item_id
    dialog_manager.start_data.update(words_stage=words_stage)

    await dao.word_users.edit(data=word_users, id=word_users.id)
    await dao.commit()

    await dialog_manager.switch_to(WordsScheduleSG.words_en)

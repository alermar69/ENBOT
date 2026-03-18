from aiogram import Bot
from aiogram.types import Chat, User
from aiogram_dialog import BgManagerFactory, DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import ManagedRadio
from bot.handling.states.en_text_translate import WordsScheduleSG
from core.config import settings
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.nats import NatsRouter
from infra.db import dto
from infra.db.dao.holder import HolderDao
from structlog import get_logger

logger = get_logger(__name__)

router = NatsRouter()


@router.subscriber("en.shedule")
@inject
async def handle(
    msg: str,
    dao: FromDishka[HolderDao],
    bot: FromDishka[Bot],
    bg_factory: FromDishka[BgManagerFactory],
):
    await logger.info(msg)

    user = await dao.user.get_one(tg_id=settings.tg_id)

    words_stage: list[tuple[dto.Word, dto.WordsUsers]] = await dao.word.get_random_words(
        user_id=user.id, word_count=30
    )

    words_stage = [(word.model_dump(), stage.model_dump()) for word, stage in words_stage]

    manager = bg_factory.bg(
        bot=bot,
        user_id=user.tg_id,
        chat_id=user.tg_id,
        stack_id="",
        load=True,
    )
    await manager.start(
        WordsScheduleSG.words_en,
        data={
            "words_stage": words_stage,
        },
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


async def get_words(
    dialog_manager: DialogManager,
    **kwargs,
):
    words_stage: list[tuple[dto.Word, dto.WordsUsers]] = dialog_manager.start_data.get(
        "words_stage"
    )
    is_show_ru = dialog_manager.dialog_data.get("is_show_ru")
    ls = []
    for word, word_users in words_stage:
        word: dto.Word = dto.Word.model_validate(word)
        word_users: dto.WordsUsers = dto.WordsUsers.model_validate(word_users)
        stage = word_users.stage

        word_en = word.en

        if stage == 2:
            word_en = f"◦  {word.en}"
        if stage == 3:
            word_en = f"!  {word.en}"

        ls.append(word_en)
        if is_show_ru:
            ls.append(word.ru)
        else:
            ls.append("...")
        ls.append(word.trans)

    words_en_ru = list(enumerate(ls))

    if is_show_ru:
        text_btn_show_ru = "Скрыть перевод"
    else:
        text_btn_show_ru = "Показать перевод"

    return {
        "words": words_en_ru,
        "text_btn_show_ru": text_btn_show_ru,
    }


async def get_word_full(
    dialog_manager: DialogManager,
    **kwargs,
):
    n_word: int = int(dialog_manager.dialog_data.get("n_word"))
    n_attr: int = int(dialog_manager.dialog_data.get("n_attr"))
    words_stage: list[tuple[dto.Word, dto.WordsUsers]] = dialog_manager.start_data.get(
        "words_stage"
    )
    word: dto.Word = dto.Word.model_validate(words_stage[n_word][0])

    if n_attr == 1:
        txt = word.ru_full
    elif n_attr == 2:
        txt = word.trans_full
    else:
        txt = word.en

    return {
        "txt": txt,
    }


async def get_word_stage(
    dialog_manager: DialogManager,
    **kwargs,
):
    n_word: int = int(dialog_manager.dialog_data.get("n_word"))
    n_attr: int = int(dialog_manager.dialog_data.get("n_attr"))
    words_stage: list[tuple[dto.Word, dto.WordsUsers]] = dialog_manager.start_data.get(
        "words_stage"
    )
    word: dto.Word = dto.Word.model_validate(words_stage[n_word][0])
    word_users: dto.WordsUsers = dto.WordsUsers.model_validate(words_stage[n_word][1])
    stage: int = word_users.stage

    dialog_manager.dialog_data.update(word=word.model_dump())
    dialog_manager.dialog_data.update(word_users=word_users.model_dump())
    # word: dto.Word = dto.Word.model_validate(dialog_manager.start_data["words"][n_word])

    radio: ManagedRadio = dialog_manager.find("radio_stage")
    await radio.set_checked(str(stage))

    stages = [
        ("1     🔴", "1"),
        ("2     🟡", "2"),
        ("3     🟢", "3"),
    ]

    word_en = f"🔴  {word.en}"
    if stage == 2:
        word_en = f"🟡  {word.en}"
    if stage == 3:
        word_en = f"🟢  {word.en}"

    if n_attr == 0:
        txt = word_en
    elif n_attr == 1:
        txt = word.ru_full
    elif n_attr == 2:
        txt = word.trans_full
    else:
        txt = word.en

    return {
        "txt": txt,
        "stages": stages,
    }

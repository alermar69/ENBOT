import typing

from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedMultiselect
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.nats import NatsBroker, NatsRouter
from infra.db import dto
from infra.db.dao.holder import HolderDao
from pydantic import BaseModel
from structlog import get_logger

logger = get_logger(__name__)

router = NatsRouter()


class MessageIn(BaseModel):
    text_en: str


class MessageOut(BaseModel):
    text_ru: str
    words: dict[str, str]


class WordsIn(BaseModel):
    words_en: list[str]
    user_id: int


class WordOut(BaseModel):
    word_ru_full: str
    trans: str
    trans_full: str


class WordsOut(BaseModel):
    words_en: dict[str, WordOut] = {}


@router.subscriber("en.is_words")
@inject
async def handle(
    user_id: int,
    nc: FromDishka[NatsBroker],
    dao: FromDishka[HolderDao],
) -> None:
    await logger.info(user_id)
    user = await dao.user.get_one(tg_id=user_id)
    await logger.info(user)
    if True:
        kv = await nc.key_value(bucket="enru")
        resp_obj = await kv.get(key="words")
        resp_obj = resp_obj.value.decode("utf-8")
        await logger.info(resp_obj)
        words_full: WordsOut = WordsOut.model_validate_json(resp_obj)
        await logger.info(words_full)

        words_en_ru = await kv.get(key="words_en_ru")
        words_en_ru = eval(words_en_ru.value.decode("utf-8"))
        await logger.info(words_en_ru)

        words = [
            dto.Word(
                en=word_en,
                ru=word_ru,
                trans=words_full.words_en.get(word_en).trans,
                ru_full=words_full.words_en.get(word_en).word_ru_full,
                trans_full=words_full.words_en.get(word_en).trans_full,
            )
            for word_en, word_ru in words_en_ru
        ]
        words = await dao.word.add_bulk(words)

        await logger.info(words)

        words_users = [dto.WordsUsers(user_id=user.id, word_id=word.id) for word in words]
        words_users = await dao.word_users.add_bulk(words_users)
        await dao.commit()


async def get_sentence(
    dialog_manager: DialogManager,
    nats: NatsBroker,
    event_from_user: User,
    **kwargs,
):

    ls_text: list[str] = dialog_manager.start_data.get("ls_text_en")
    user: dto.User = dto.User.model_validate(dialog_manager.start_data.get("user"))
    text: str = ls_text.pop()
    dialog_manager.dialog_data.update(text=text)
    dialog_manager.dialog_data.update(ls_text_en=ls_text)
    dialog_manager.dialog_data.update({"is_words": False})
    dialog_manager.dialog_data.update({"resp_sentence": False})

    multiselect = typing.cast("ManagedMultiselect", dialog_manager.find("multi_topics"))
    words_id: list[int] = multiselect.get_checked()
    if words_id:
        words_en = dialog_manager.dialog_data.get("words_en")
        words_en_ru = [words_en.get(str(word_id)) for word_id in words_id]

        kv = await nats.key_value(bucket="enru")
        await kv.put(key="words_en_ru", value=str(words_en_ru).encode("utf-8"))

        publisher = router.publisher("en.words")
        words_en1 = [word_en for word_en, word_ru in words_en_ru]
        await publisher.publish(
            WordsIn(
                words_en=words_en1,
                user_id=event_from_user.id,
            ).model_dump()
        )
        await logger.info(WordsIn(words_en=words_en1, user_id=event_from_user.id).model_dump())

        await multiselect.reset_checked()

    return {
        "text": text,
    }


async def get_words(
    dialog_manager: DialogManager,
    nats: NatsBroker,
    **kwargs,
):
    logger = get_logger(__name__)
    text = dialog_manager.dialog_data.get("text")

    kv = await nats.key_value(bucket="enru")
    resp_sentence = await kv.get(key="resp_sentence")
    resp_sentence = resp_sentence.value.decode("utf-8")
    await logger.info(resp_sentence)
    resp_obj = await kv.get(key="resp_obj")
    resp_obj = resp_obj.value.decode("utf-8")
    msg: MessageOut = MessageOut.model_validate_json(resp_obj)
    resp = await kv.get(key="resp")
    if resp == "on":
        pass

    words_en_ru_ls = [f"{word_en} - {word_ru}" for word_en, word_ru in msg.words.items()]
    words_en_ru = list(enumerate(words_en_ru_ls))
    words_en = {}
    for index, (word_en, word_ru) in enumerate(msg.words.items()):
        words_en[str(index)] = [word_en, word_ru]
    await logger.info(words_en_ru)
    await logger.info(msg)
    dialog_manager.dialog_data.update(words_en=words_en)

    is_show_words = dialog_manager.dialog_data.get("is_show_words")
    if is_show_words:
        text_btn_show_words = "Показать\nслова"
    else:
        text_btn_show_words = "Скрыть\nслова"

    is_show_translate = dialog_manager.dialog_data.get("is_show_translate")
    if is_show_translate:
        text_btn_show_translate = "Скрыть\nперевод"
    else:
        text_btn_show_translate = "Показать\nперевод"

    return {
        "words_en_ru": words_en_ru,
        "text": text,
        "text_translate": msg.text_ru,
        "text_btn_show_words": text_btn_show_words,
        "text_btn_show_translate": text_btn_show_translate,
        "is_show_words": not is_show_words,
        "is_show_translate": is_show_translate,
    }

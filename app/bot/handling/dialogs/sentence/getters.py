from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from dishka import AsyncContainer
from dishka.integrations.aiogram_dialog import FromDishka, inject

# from dishka.integrations.faststream import inject
from faststream import Context, ContextRepo, Logger
from faststream.nats import NatsBroker, NatsRouter
from fluentogram import TranslatorRunner
from infra.db.dao.holder import HolderDao

# from main import dishka
# from main import get_nc
from pydantic import BaseModel
from structlog import get_logger

logger = get_logger(__name__)

router = NatsRouter()


class MessageIn(BaseModel):
    text_en: str


class MessageOut(BaseModel):
    text_ru: str
    words: dict[str, str]


# @router.subscriber("en.translate.response")
# @inject
# async def response_en(
#     msg: MessageOut,
#     nc: FromDishka[NatsBroker],
#     # logger1: Logger,
#     # msg: MessageOut, logger1: Logger, nc: FromDishka[NatsBroker]
# ) -> None:
#     logger.info(msg)
#     # nc = await dishka.get(NatsBroker)
#     # nc = await get_nc()
#     # nc = NatsBroker("nats://localhost:4222")
#     kv = await nc.key_value(bucket="enru")
#     await kv.put(key="resp_sentence", value=msg.text_ru.encode("utf-8"))
#     await kv.put(key="resp_obj", value=msg.model_dump_json().encode("utf-8"))
#     await kv.put(key="resp", value=b"on")


async def get_sentence(
    dialog_manager: DialogManager, i18n: TranslatorRunner, state: FSMContext, **kwargs
):
    # await logger.debug("main page getter called")

    ls_text: list[str] = dialog_manager.start_data.get("ls_text_en")
    text: str = ls_text.pop()
    dialog_manager.dialog_data.update(text=text)
    dialog_manager.dialog_data.update(ls_text_en=ls_text)
    dialog_manager.dialog_data.update({"is_words": False})

    publisher = router.publisher("en.translate")
    await publisher.publish(MessageIn(text_en=text).model_dump())
    dialog_manager.dialog_data.update({"resp_sentence": False})

    return {
        "text": text,
    }


# @inject
async def get_words(
    dialog_manager: DialogManager,
    nats: NatsBroker,
    dao: HolderDao,
    # dishka_container: AsyncContainer,
    # nc: FromDishka[NatsBroker],
    # i18n: TranslatorRunner,
    # state: FSMContext,
    **kwargs,
):

    # nc = await dishka_container.get(NatsBroker)
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

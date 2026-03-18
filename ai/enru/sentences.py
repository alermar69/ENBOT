import re

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream import Logger
from faststream.nats import NatsBroker, NatsRouter
from mistral_ai.gen.text import gpt_text
from pydantic import BaseModel

from enru.words import safe_kv_put

router = NatsRouter()


class MessageIn(BaseModel):
    text_en: str


class MessageOut(BaseModel):
    text_ru: str
    words: dict[str, str]


@router.subscriber("en.translate")
@inject
async def handle(msg: MessageIn, logger: Logger, nc: FromDishka[NatsBroker]) -> None:
    s1 = f"{msg.text_en}\nпереведи на русский"
    res1 = gpt_text(s1, model="mistral-small-latest")
    # logger.info(res.text)

    s1 = f"""{msg.text_en}
Выбери из этого предложения основные слова и отобрази их в виде dict python, 
где key-английское слово, value - перевод на русский"""

    res2 = gpt_text(s1, model="mistral-small-latest")
    words_str = re.findall(r"\{.*?}", res2.text, re.DOTALL)[0]
    words: dict[str, str] = eval(words_str)
    logger.info(words)

    msg = MessageOut(text_ru=res1.text, words=words)

    kv = await nc.key_value(bucket="enru")
    await safe_kv_put(kv, key="resp_sentence", value=msg.text_ru.encode("utf-8"))
    await safe_kv_put(kv, key="resp_obj", value=msg.model_dump_json().encode("utf-8"))
    await safe_kv_put(kv, key="resp", value=b"on")

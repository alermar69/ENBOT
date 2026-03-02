import asyncio
import re

from faststream import FastStream, Logger
from faststream.nats import NatsBroker
from pydantic import BaseModel

from core.config import settings
from mistral_ai.gen.text import gpt_text

# from enru.translate import router

broker = NatsBroker(settings.nats.url)


class MessageIn(BaseModel):
    text_en: str


class MessageOut(BaseModel):
    text_ru: str
    words: dict[str, str]


@broker.subscriber("en.translate")
# @router.publisher("en.translate.response")
async def handle(msg: MessageIn, logger: Logger) -> None:
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

    kv = await broker.key_value(bucket="enru")
    # kv = await broker.key_value(bucket="enru", declare=False)
    await kv.put(key="resp_sentence", value=msg.text_ru.encode("utf-8"))
    await kv.put(key="resp_obj", value=msg.model_dump_json().encode("utf-8"))
    await kv.put(key="resp", value=b"on")

    # return MessageOut(text_ru=res1.text, words=words)


async def main():

    # broker.include_router(router)
    app = FastStream(broker)
    await app.run()  # blocking method


if __name__ == "__main__":
    asyncio.run(main())

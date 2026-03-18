import re

from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream import Logger
from faststream.nats import NatsBroker, NatsRouter
from mistral_ai.gen.text import gpt_text
from nats.errors import TimeoutError
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def safe_kv_put(kv, key, value):
    try:
        await kv.put(key=key, value=value)
    except TimeoutError as e:
        print(f"Timeout occurred: {e}. Retrying...")
        raise


router = NatsRouter()


class TmpOut(BaseModel):
    name: str


class WordsIn(BaseModel):
    words_en: list[str]
    user_id: int


class WordOut(BaseModel):
    word_ru_full: str
    trans: str
    trans_full: str


class WordsOut(BaseModel):
    words_en: dict[str, WordOut] = {}


@router.subscriber("en.words")
@router.publisher("en.is_words")
@inject
async def handle(msg: WordsIn, logger: Logger, nc: FromDishka[NatsBroker]) -> int:
    s1 = f"{', '.join(msg.words_en)}\nотобрази их в виде dict python, где key-английское слово, value - транскрипция"
    res1 = gpt_text(s1, model="mistral-small-latest")
    words_str = re.findall(r"\{.*?}", res1.text, re.DOTALL)[0]
    words_trans: dict[str, str] = eval(words_str)
    words_out = WordsOut()

    for word_en, trans in words_trans.items():
        if word_en in msg.words_en:
            s1 = f"{word_en}\nпереведи на русский"
            res1 = gpt_text(s1, model="mistral-small-latest")
            word_ru_full = res1.text

            s1 = f"{word_en}\nнапиши транскрипцию"
            res1 = gpt_text(s1, model="mistral-small-latest")
            trans_full = res1.text

            word_out = WordOut(
                trans=trans,
                word_ru_full=word_ru_full,
                trans_full=trans_full,
            )
            words_out.words_en[word_en] = word_out

    kv = await nc.key_value(bucket="enru")
    await safe_kv_put(kv, key="words", value=words_out.model_dump_json().encode("utf-8"))
    logger.info(words_out)
    return msg.user_id


class WordOut1(BaseModel):
    word_ru: str
    word_ru_full: str
    trans: str
    trans_full: str


class WordsOut1(BaseModel):
    words_en: dict[str, WordOut1] = {}


@router.subscriber("en.words1")
@router.publisher("en.is_words1")
@inject
async def handle1(msg: WordsIn, logger: Logger, nc: FromDishka[NatsBroker]) -> int:
    s1 = f"""{msg.words_en}
    Отобрази их в виде dict python, 
    где key-английское слово, value - перевод на русский"""

    res2 = gpt_text(s1, model="mistral-small-latest")
    words_str = re.findall(r"\{.*?}", res2.text, re.DOTALL)[0]
    words: dict[str, str] = eval(words_str)

    s1 = f"{', '.join(msg.words_en)}\nотобрази их в виде dict python, где key-английское слово, value - транскрипция"
    res1 = gpt_text(s1, model="mistral-small-latest")
    words_str = re.findall(r"\{.*?}", res1.text, re.DOTALL)[0]
    words_trans: dict[str, str] = eval(words_str)
    words_out = WordsOut1()

    for word_en, trans in words_trans.items():
        if word_en in msg.words_en:
            s1 = f"{word_en}\nпереведи на русский"
            res1 = gpt_text(s1, model="mistral-small-latest")
            word_ru_full = res1.text

            s1 = f"{word_en}\nнапиши транскрипцию"
            res1 = gpt_text(s1, model="mistral-small-latest")
            trans_full = res1.text

            word_out = WordOut1(
                trans=trans,
                word_ru_full=word_ru_full,
                word_ru=words.get(word_en),
                trans_full=trans_full,
            )
            words_out.words_en[word_en] = word_out

    kv = await nc.key_value(bucket="enru")
    await safe_kv_put(kv, key="words1", value=words_out.model_dump_json().encode("utf-8"))
    # logger.info(words_out)
    return msg.user_id

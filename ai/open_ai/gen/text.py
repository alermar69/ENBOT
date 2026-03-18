import asyncio

from core.config import settings
from core.dto.ai import AiResponse
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionUserMessageParam


async def gpt_text(req: str, model: str) -> AiResponse | None:
    # client = AsyncOpenAI(api_key=settings.openai.token)

    async with AsyncOpenAI(api_key=settings.openai.token) as client:
        res = await client.chat.completions.create(
            messages=[ChatCompletionUserMessageParam(content=req, role="user")],
            model=model,
        )

    if res is not None:
        return AiResponse(
            text=res.choices[0].message.content,
            usage=res.usage.total_tokens,
        )
    return None


# asyncio.run(gpt_text("embed - переводи на русский язык", "gpt-3.5-turbo"))

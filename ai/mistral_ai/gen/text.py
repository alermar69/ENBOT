from time import sleep

from mistralai import Mistral

from core.config import settings
from core.DTO import AiResponse


def gpt_text(req: str, model: str) -> AiResponse | None:
    for i in range(10):
        try:
            with Mistral(
                api_key=settings.mistral.token,
            ) as mistral:
                res = mistral.chat.complete(
                    model=model,  # "mistral-small-latest"
                    messages=[
                        {
                            "content": req,
                            "role": "user",
                        },
                    ],
                    stream=False,
                )

                break
        except Exception as e:
            sleep(1)
    if res:
        return AiResponse(
            text=res.choices[0].message.content,
            usage=res.usage.total_tokens,
        )
    return None

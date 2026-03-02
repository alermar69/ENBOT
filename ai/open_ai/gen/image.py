import base64

import aiofiles
import aiohttp
from openai import AsyncOpenAI

from core.config import settings


async def gpt_image(req: str, model: str):
    async with AsyncOpenAI(api_key=settings.openai.token) as client:
        response = await client.images.generate(
            model=model,  # "dall-e-3"
            prompt=req,
            n=1,
            size="1024x1024",
            quality="standard",
        )
        return {
            "response": response.data[0].url,
            "usage": 1,
        }


async def encode_image(image_path: str):
    async with aiofiles.open(image_path, "rb") as image_file:
        return base64.b64encode(await image_file.read()).decode("utf-8")


async def gpt_vision(req: str, model: str, file: str):
    base64_image = await encode_image(file)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.openai.token}",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }
    if req is not None:
        payload["messages"][0]["content"].append(
            {
                "type": "text",
                "text": req,
            },
        )

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        ) as resp:
            completion = await resp.json()
            return {
                "response": completion["choices"][0]["message"]["content"],
                "usage": completion["usage"]["total_tokens"],
            }

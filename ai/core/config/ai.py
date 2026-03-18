from pydantic import BaseModel


class OpenAiConfig(BaseModel):
    token: str = ""


class MistralAiConfig(BaseModel):
    token: str = ""

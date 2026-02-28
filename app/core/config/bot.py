from enum import Enum

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from pydantic import BaseModel, SecretStr


class BotApiType(Enum):
    official = "official"
    local = "local"


class BotApiConfig(BaseModel):
    # type: BotApiType = BotApiType.local
    type: BotApiType = BotApiType.official
    botapi_url: str | None = None
    botapi_file_url: str | None = None

    @property
    def is_local(self) -> bool:
        return self.type == BotApiType.local

    def create_server(self) -> TelegramAPIServer:
        if self.type != BotApiType.local:
            raise RuntimeError("can create only local botapi server")
        return TelegramAPIServer(
            base=f"{self.botapi_url}/bot{{token}}/{{method}}",
            file=f"{self.botapi_file_url}{{path}}",
        )


class FSMConfig(BaseModel):
    data_bucket: str = "fsm_data_aiogram"
    states_bucket: str = "fsm_states_aiogram"

    class Config:
        extras = "allow"


class BotConfig(BaseModel):
    token: SecretStr = ""
    fsm: FSMConfig = FSMConfig()
    bot_api: BotApiConfig = BotApiConfig()

    def create_session(self) -> AiohttpSession | None:
        if self.bot_api.is_local:
            return AiohttpSession(api=self.bot_api.create_server())
        return None

    class Config:
        extras = "allow"

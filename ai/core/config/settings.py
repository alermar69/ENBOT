from pathlib import Path
from typing import Literal

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from core.config.ai import MistralAiConfig, OpenAiConfig
from core.config.database import DatabaseConfig
from core.config.logging import LoggingConfig
from core.config.nats import NatsConfig
from core.config.struct_logs.config import StructLogConfig

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent
ENVS_DIR = CONFIG_DIR / "envs"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            ENVS_DIR / ".env.template",
            ENVS_DIR / ".env",
            CONFIG_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"] = "LOCAL"

    logging: LoggingConfig = LoggingConfig()
    structlog: StructLogConfig = StructLogConfig()
    db: DatabaseConfig
    nats: NatsConfig = NatsConfig()
    openai: OpenAiConfig = OpenAiConfig()
    mistral: MistralAiConfig = MistralAiConfig()


settings = Settings()

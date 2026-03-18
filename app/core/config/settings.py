from pathlib import Path
from typing import Literal

from core.config.api import ApiPrefix, GunicornConfig, RunConfig
from core.config.bot import BotConfig, FSMConfig
from core.config.cache import CacheConfig
from core.config.database import DatabaseConfig
from core.config.logging import LoggingConfig
from core.config.nats import NatsConfig
from core.config.redis import RedisConfig
from core.config.struct_logs.config import StructLogConfig
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent
ENVS_DIR = CONFIG_DIR / "envs"
YAML_DIR = CONFIG_DIR / "yaml"


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
        yaml_config_section="app",
        yaml_file=(
            YAML_DIR / "default.yaml",
            YAML_DIR / "local.yaml",
        ),
    )

    tg_id: int

    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    bot: BotConfig = BotConfig()
    fsm: FSMConfig = FSMConfig()
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    structlog: StructLogConfig = StructLogConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()
    nats: NatsConfig = NatsConfig()

    # @classmethod
    # def settings_customise_sources(
    #         cls,
    #         settings_cls: type[BaseSettings],
    #         init_settings: PydanticBaseSettingsSource,
    #         env_settings: PydanticBaseSettingsSource,
    #         dotenv_settings: PydanticBaseSettingsSource,
    #         file_secret_settings: PydanticBaseSettingsSource,
    # ) -> tuple[PydanticBaseSettingsSource, ...]:
    #     return (
    #         init_settings,
    #         env_settings,
    #         dotenv_settings,
    #         # file_secret_settings,
    #         #
    #         YamlConfigSettingsSource(
    #             settings_cls,
    #             deep_merge=True, # pydantic > 2.12.0 required
    #         ),
    #     )


settings = Settings()

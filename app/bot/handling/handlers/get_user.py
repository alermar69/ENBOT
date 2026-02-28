from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluentogram import TranslatorRunner
from infra.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession

# from config import Config


get_user_router = Router()


@get_user_router.message(Command("get_info"))
async def get_user_handler(msg: Message, i18n: TranslatorRunner, db: AsyncSession):
    user = await db.get(User, msg.from_user.id)
    await msg.answer(i18n.db_get_user(user=user))


# @get_user_router.message(Command("get_test"))
# async def get_user_handler(msg: Message, i18n: TranslatorRunner, db: AsyncSession):
#     settings = Dynaconf(
#         envvar_prefix="APP_CONF",
#         settings_files=["settings.toml", ".secrets.toml"],
#     )
#     app_config: Config = Config.model_validate(settings.as_dict())
#     url = app_config.db.uri
#     x1 = 1

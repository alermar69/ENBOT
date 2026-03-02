import asyncio
import sys
from asyncio import CancelledError
from pathlib import Path

import core.config.struct_logs
import dishka_faststream
import structlog
from aiogram import Bot, Dispatcher
from bot.main_factory import create_dishka, resolve_update_types
from core.config import settings, struct_logs
from faststream import FastStream
from faststream.nats import NatsBroker
from infra.di.utils import warm_up
from infra.I18N import i18n_factory

sys.path.append(str(Path(__file__).parent))

dishka = create_dishka()


async def main():
    logger = structlog.get_logger(__name__)
    struct_logs.startup(settings.structlog)
    await logger.info(settings.nats.server)
    await logger.info("App is starting, configs parsed successfully")

    dp = await dishka.get(Dispatcher)
    bot = await dishka.get(Bot)
    nc = await dishka.get(NatsBroker)

    app = FastStream(nc)
    dishka_faststream.setup_dishka(container=dishka, app=app, auto_inject=True)

    # setup_dishka(container=dishka, broker=nc)

    try:
        # await app.run()
        await warm_up(dishka)
        # await bot.delete_webhook()
        # await dp.start_polling(bot, allowed_updates=resolve_update_types(dp))
        await dp.start_polling(
            bot,
            _translator_hub=i18n_factory(),
            allowed_updates=resolve_update_types(dp),
        )
    except CancelledError:
        await logger.info("Bot stopped")
    except KeyboardInterrupt:
        await logger.info("Bot stopped")
    finally:
        await logger.info("stopped")
        await dishka.close()
        await app.stop()
        await nc.stop()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()

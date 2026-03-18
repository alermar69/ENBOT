import asyncio
from asyncio import CancelledError
from pathlib import Path

import structlog
import sys
from aiogram import Bot, Dispatcher
from faststream import FastStream
from faststream.nats import NatsBroker

from core.config import settings, struct_logs
from infra.I18N import i18n_factory
from infra.di.main_factory import resolve_update_types
from infra.di.utils import warm_up

sys.path.append(str(Path(__file__).parent))

from infra.di.main_factory import dishka


async def main():
    logger = structlog.get_logger(__name__)
    struct_logs.startup(settings.structlog)
    await logger.info("App is starting, configs parsed successfully")

    dp = await dishka.get(Dispatcher)
    bot = await dishka.get(Bot)
    nc = await dishka.get(NatsBroker)
    app_faststream = await dishka.get(FastStream)

    try:
        await warm_up(dishka)
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
        await app_faststream.stop()
        await nc.stop()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()

import asyncio
from asyncio import CancelledError

import structlog
from faststream import FastStream
from faststream.nats import NatsBroker
from infra.di.main_factory import create_dishka
from infra.di.utils import warm_up

dishka = create_dishka()


async def main():

    logger = await dishka.get(structlog.BoundLogger)
    nc = await dishka.get(NatsBroker)
    app_faststream = await dishka.get(FastStream)

    try:
        await warm_up(dishka)
        await app_faststream.run()
    except CancelledError:
        await logger.info("Bot stopped")
    except KeyboardInterrupt:
        await logger.info("Bot stopped")
    finally:
        await logger.info("stopped")
        await dishka.close()
        await app_faststream.stop()
        await nc.stop()


if __name__ == "__main__":
    asyncio.run(main())

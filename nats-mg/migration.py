import asyncio

import nats
import structlog
from config import settings
from nats.js.api import KeyValueConfig
from nats.js.errors import BucketNotFoundError


async def main():
    logger = structlog.get_logger(__name__)
    structlog.configure(processors=[structlog.dev.ConsoleRenderer(colors=True)])
    nc = await nats.connect(settings.nats.url)
    js = nc.jetstream()
    logger.debug("NATS connection established")
    # FSM buckets
    kv_name = "fsm_data_aiogram"
    try:
        kv = await js.key_value(kv_name)
    except BucketNotFoundError as e:
        await js.create_key_value(KeyValueConfig(kv_name))

    kv_name = "fsm_states_aiogram"
    try:
        kv = await js.key_value(kv_name)
    except BucketNotFoundError as e:
        await js.create_key_value(KeyValueConfig(kv_name))

    # EnRu
    kv_name = "enru"
    try:
        kv = await js.key_value(kv_name)
    except BucketNotFoundError as e:
        await js.create_key_value(KeyValueConfig(kv_name))

    logger.debug("NATS Buckets created")


if __name__ == "__main__":
    asyncio.run(main())

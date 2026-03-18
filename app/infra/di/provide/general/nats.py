import structlog
from bot.handling.dialogs.schedules.getters import router as router_nc_words
from bot.handling.dialogs.sentence.getters import router as router_nc_sentences
from core.config import settings
from dishka import Provider, Scope, provide
from faststream.nats import NatsBroker


class NatsProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_broker(
        self,
        logger: structlog.BoundLogger,
    ) -> NatsBroker:
        await logger.info("NatsBroker starting", url=settings.nats.url)
        nc = NatsBroker(settings.nats.url)
        nc.include_router(router_nc_sentences)
        nc.include_router(router_nc_words)
        await nc.start()
        return nc

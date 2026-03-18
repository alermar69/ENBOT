import structlog
from core.config import settings
from dishka import AsyncContainer, Provider, Scope, provide
from enru import router as router_enru
from faststream.nats import NatsBroker


class NatsProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_broker(
        self,
        logger: structlog.BoundLogger,
    ) -> NatsBroker:
        await logger.info("NatsBroker starting", url=settings.nats.url)
        nc = NatsBroker(
            settings.nats.url,
            connect_timeout=10,
            max_reconnect_attempts=5,
            reconnect_time_wait=2,
        )
        nc.include_router(router_enru)
        await nc.start()
        return nc

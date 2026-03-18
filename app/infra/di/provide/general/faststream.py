import structlog
from dishka import AsyncContainer, Provider, Scope, provide
from dishka.integrations.faststream import (
    setup_dishka,
)
from faststream import FastStream
from faststream.nats import NatsBroker


class FastStreamAppProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_app(
        self,
        dishka: AsyncContainer,
        nc: NatsBroker,
        logger: structlog.BoundLogger,
    ) -> FastStream:
        app = FastStream(nc)
        setup_dishka(container=dishka, app=app, auto_inject=True)
        await app.start()
        await logger.info("FastStream created")
        return app

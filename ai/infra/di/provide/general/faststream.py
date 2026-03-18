import dishka_faststream
import structlog
from dishka import AsyncContainer, Provider, Scope, provide
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
        dishka_faststream.setup_dishka(container=dishka, app=app, auto_inject=True)
        await logger.info("FastStream created")
        return app

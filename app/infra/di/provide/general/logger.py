import structlog
from dishka import AsyncContainer, Provider, Scope, provide


class LoggerProvider(Provider):
    scope = Scope.APP

    @provide
    async def create_logger(
        self,
    ) -> structlog.BoundLogger:
        logger: structlog.BoundLogger = structlog.get_logger(__name__)
        return logger

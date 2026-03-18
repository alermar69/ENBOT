import typing
from datetime import datetime, tzinfo

from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.models.ai import AiModel, AiType

from .base import BaseDAO
from .mappers.mappers import AiModelDataMapper, AiTypeDataMapper


class AiModelDao(BaseDAO[AiModel, AiModelDataMapper]):
    def __init__(
        self, session: AsyncSession, clock: typing.Callable[[tzinfo], datetime] = datetime.now
    ) -> None:
        super().__init__(AiModel, AiModelDataMapper, session, clock=clock)


class AiTypeDao(BaseDAO[AiType, AiTypeDataMapper]):
    def __init__(
        self, session: AsyncSession, clock: typing.Callable[[tzinfo], datetime] = datetime.now
    ) -> None:
        super().__init__(AiType, AiTypeDataMapper, session, clock=clock)

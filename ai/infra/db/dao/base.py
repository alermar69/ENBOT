import typing
from collections.abc import Sequence
from datetime import datetime, tzinfo
from typing import Generic, TypeVar

from asyncpg import UniqueViolationError
from infra.db.dao.mappers.base import DataMapper
from infra.db.models.base import Base
from pydantic import BaseModel
from sqlalchemy import ScalarResult, delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption
from structlog import get_logger

logger = get_logger(__name__)

Model_co = TypeVar("Model_co", bound=Base, covariant=True, contravariant=False)
Mapper_co = TypeVar("Mapper_co", bound=DataMapper, covariant=True, contravariant=False)
Dto_co = TypeVar("Dto_co", bound=BaseModel, covariant=True, contravariant=False)


class BaseDAO(Generic[Model_co, Mapper_co]):
    def __init__(
        self,
        model: type[Model_co],
        mapper: type[DataMapper],
        session: AsyncSession,
        clock: typing.Callable[[tzinfo], datetime] = datetime.now,
    ) -> None:
        self.model = model
        self.mapper = mapper
        self.session = session
        self.clock = clock

    async def get_filtered(self, *filter, **filter_by) -> list[Dto_co]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.to_dto(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> list[Dto_co]:
        return await self.get_filtered()

    async def get_one(self, **filter_by) -> Dto_co:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return self.mapper.to_dto(model)
        except NoResultFound:
            pass
            # raise ObjectNotFoundException

    async def get_page(self, offset: int, limit: int) -> Sequence[Dto_co]:
        result: ScalarResult[Model_co] = await self.session.scalars(
            select(self.model).offset(offset).limit(limit)
        )
        return [self.mapper.to_dto(model) for model in result.all()]

    async def add(self, data: Dto_co) -> Dto_co:
        try:
            add_data_stmt = (
                insert(self.model).values(**data.model_dump(exclude={"id"})).returning(self.model)
            )
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.to_dto(model)
        except IntegrityError as ex:
            await logger.exception("Не удалось добавить данные в БД, входные данные=%s", data)
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                # raise ObjectAlreadyExistsException from ex
                pass
            else:
                await logger.exception(
                    "Незнакомая ошибка: не удалось добавить данные в БД, входные данные=%s", data
                )
                raise ex

    async def add_bulk(self, data: Sequence[Dto_co]) -> list[Dto_co]:
        add_data_stmt = (
            insert(self.model)
            .values([item.model_dump(exclude={"id"}) for item in data])
            .returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        models = result.scalars().all()
        return [self.mapper.to_dto(model) for model in models]

    async def edit(self, data: Dto_co, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def delete_all(self):
        await self.session.execute(delete(self.model))

    async def _get_all(self, options: Sequence[ORMOption] = ()) -> Sequence[Model_co]:
        result: ScalarResult[Model_co] = await self.session.scalars(
            select(self.model).options(*options)
        )
        return result.all()

    async def _get_by_id(
        self, id_: int, options: Sequence[ORMOption] | None = None, populate_existing: bool = False
    ) -> Model_co:
        result = await self.session.get(
            self.model, id_, options=options, populate_existing=populate_existing
        )
        if result is None:
            raise NoResultFound
        return result

    def _save(self, obj: Base):
        self.session.add(obj)

    async def _delete(self, obj: Base):
        await self.session.delete(obj)

    async def count(self):
        result = await self.session.execute(select(func.count(self.model.id)))
        return result.scalar_one()

    async def commit(self):
        await self.session.commit()

    async def _flush(self, *objects: Base):
        await self.session.flush(objects)

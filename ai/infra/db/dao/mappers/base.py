from typing import Type, TypeVar

from infra.db.models.base import Base
from pydantic import BaseModel
from sqlalchemy import Row, RowMapping

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: Type[Base]
    schema: Type[SchemaType]

    @classmethod
    def to_dto(cls, data: Base | dict | Row | RowMapping) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def to_orm(cls, data: BaseModel) -> Base:
        return cls.db_model(**data.model_dump())

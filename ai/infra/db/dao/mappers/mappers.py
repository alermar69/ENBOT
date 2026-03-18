from infra.db import dto
from infra.db.dao.mappers.base import DataMapper
from infra.db.models.ai import AiModel, AiType
from infra.db.models.user import User


class UserDataMapper(DataMapper):
    db_model = User
    schema = dto.User


class AiModelDataMapper(DataMapper):
    db_model = AiModel
    schema = dto.AiModel


class AiTypeDataMapper(DataMapper):
    db_model = AiType
    schema = dto.AiType

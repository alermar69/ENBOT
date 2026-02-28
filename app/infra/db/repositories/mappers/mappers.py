from infra.db.models import User
from infra.db.repositories.mappers.base import DataMapper
from infra.db.schemas.users import User as UserSchema


class UserDataMapper(DataMapper):
    db_model = User
    schema = UserSchema

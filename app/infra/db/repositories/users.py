from infra.db.models import User
from infra.db.repositories.base import BaseRepository
from infra.db.repositories.mappers.mappers import UserDataMapper
from pydantic import EmailStr
from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = User
    mapper = UserDataMapper

from infra.db import dto
from infra.db.dao.mappers.base import DataMapper
from infra.db.models import User
from infra.db.models.word import Word, WordsUsers


class UserDataMapper(DataMapper):
    db_model = User
    schema = dto.User


class WordDataMapper(DataMapper):
    db_model = Word
    schema = dto.Word


class WordsUsersDataMapper(DataMapper):
    db_model = WordsUsers
    schema = dto.WordsUsers

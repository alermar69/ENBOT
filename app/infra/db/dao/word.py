import typing
from datetime import datetime, tzinfo

from infra.db import dto
from infra.db.models.word import Word, WordsUsers
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from .mappers.mappers import WordDataMapper, WordsUsersDataMapper


class WordDao(BaseDAO[Word, WordDataMapper]):
    def __init__(
        self, session: AsyncSession, clock: typing.Callable[[tzinfo], datetime] = datetime.now
    ) -> None:
        super().__init__(Word, WordDataMapper, session, clock=clock)

    async def get_random_words(
        self, user_id: int, word_count: int = 10
    ) -> list[tuple[dto.Word, dto.WordsUsers]]:
        query = (
            select(Word, WordsUsers)
            .join(WordsUsers, Word.id == WordsUsers.word_id)
            .where(WordsUsers.user_id == user_id)
            .order_by(func.random())
            .limit(word_count)
        )
        result = await self.session.execute(query)
        res = result.all()
        return [
            (self.mapper.to_dto(word), WordsUsersDataMapper.to_dto(word_users))
            for word, word_users in res
        ]


class WordsUsersDao(BaseDAO[WordsUsers, WordsUsersDataMapper]):
    def __init__(
        self, session: AsyncSession, clock: typing.Callable[[tzinfo], datetime] = datetime.now
    ) -> None:
        super().__init__(WordsUsers, WordsUsersDataMapper, session, clock=clock)

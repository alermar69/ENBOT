# Sample test

from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Chat, Message, Update, User
from tests.mocks.mocked_aiogram import MockedBot

# from core.utils.datetime_utils import tz_utc


@pytest.mark.asyncio
async def test_cmd_start(dp: Dispatcher, bot: MockedBot):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/start",
        date=datetime.now(),
        # message_id=1, chat=chat, from_user=user, text="/start", date=datetime.now(tz=tz_utc)
    )

    result = await dp.feed_update(bot, Update(message=message, update_id=1))
    assert result is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)

    # text = dialog_manager.dialog_data.get("text")
    # assert outgoing_message.text == text

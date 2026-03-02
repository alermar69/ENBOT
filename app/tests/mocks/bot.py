from aiogram import Bot
from aiogram_dialog.api.protocols import MessageManagerProtocol
from aiogram_dialog.test_tools import MockMessageManager
from core.config import settings, struct_logs
from dishka import Provider, Scope, provide
from tests.mocks.mocked_aiogram import MockedBot

# from tests.aiogram_tests import MockedBot


class MockMessageManagerProvider(Provider):
    scope = Scope.APP

    @provide
    def get_manager(self) -> MessageManagerProtocol:
        return MockMessageManager()


class MockBotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self) -> Bot:
        # struct_logs.startup(settings.structlog)
        bot = MockedBot(token=settings.bot.token.get_secret_value())
        return bot

from dishka.integrations.aiogram import AiogramProvider
from dishka_faststream import FastStreamProvider
from infra.di.bot import BotProvider, DpProvider, NatsProvider
from infra.di.db import DAOProvider, DbProvider


def get_providers():
    return [
        DbProvider(),
        DAOProvider(),
        BotProvider(),
        NatsProvider(),
        DpProvider(),
        AiogramProvider(),
        FastStreamProvider(),
    ]

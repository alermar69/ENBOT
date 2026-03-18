from dishka_faststream import FastStreamProvider

from .db import DAOProvider, DbProvider
from .faststream import FastStreamAppProvider
from .logger import LoggerProvider
from .nats import NatsProvider

__all__ = [
    "DAOProvider",
    "DbProvider",
    "FastStreamAppProvider",
    "LoggerProvider",
    "NatsProvider",
    "get_providers",
]


def get_providers():
    return [
        LoggerProvider(),
        NatsProvider(),
        FastStreamAppProvider(),
        FastStreamProvider(),
        DbProvider(),
        DAOProvider(),
    ]

from dishka import (
    AsyncContainer,
    Provider,
    make_async_container,
)

from infra.di import get_providers


def create_dishka() -> AsyncContainer:
    container = make_async_container(*get_all_providers())
    return container


def get_all_providers() -> list[Provider]:
    return [
        *get_providers(),
    ]

from aiogram import Bot, Dispatcher
from dishka import (
    AsyncContainer,
    Provider,
    make_async_container,
)


def create_dishka() -> AsyncContainer:
    container = make_async_container(*get_all_providers())
    return container


def get_all_providers() -> list[Provider]:
    from infra.di.provide import get_providers

    return [
        *get_providers(),
    ]


def resolve_update_types(dp: Dispatcher) -> list[str]:
    return dp.resolve_used_update_types(skip_events={"aiogd_update"})


dishka = create_dishka()

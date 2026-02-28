from aiogram.dispatcher.middlewares.data import MiddlewareData
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Context, Stack
from aiogram_dialog.api.protocols import BgManagerFactory
from aiogram_dialog.context.storage import StorageProxy
from core.models import dto
from dishka import AsyncContainer
from faststream.nats import NatsBroker
from infra.db.dao.holder import HolderDao


class DialogMiddlewareData(MiddlewareData, total=False):
    dialog_manager: DialogManager
    aiogd_storage_proxy: StorageProxy
    aiogd_stack: Stack
    aiogd_context: Context


class SHMiddlewareData(DialogMiddlewareData, total=False):
    dishka_container: AsyncContainer
    dao: HolderDao
    nats: NatsBroker
    user: dto.User | None
    bg_manager_factory: BgManagerFactory

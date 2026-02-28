from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedMultiselect


async def next_text(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.done()


async def on_off_words(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    is_show_words = dialog_manager.dialog_data.get("is_show_words")
    dialog_manager.dialog_data.update(is_show_words=not is_show_words)


async def on_off_translate(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    is_show_translate = dialog_manager.dialog_data.get("is_show_translate")
    dialog_manager.dialog_data.update(is_show_translate=not is_show_translate)


# Хэндлер, обрабатывающий нажатие кнопки в виджете `Checkbox`
async def words_filled(
    callback: CallbackQuery, checkbox: ManagedMultiselect, *args, **kwargs
):
    print(checkbox.get_checked())

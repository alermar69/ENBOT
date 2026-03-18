import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Radio,
    ScrollingGroup,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format, Jinja

from bot.handling.states.en_text_translate import WordsScheduleSG
from .getters import get_word_full, get_word_stage, get_words
from .handlers import (
    on_off_word_ru,
    select_stage,
    select_word,
)

dialog = Dialog(
    Window(
        Jinja("<u>Список игр твоего авторства</u>"),
        ScrollingGroup(
            Select(
                Format("{item[1]}"),
                id="en",
                item_id_getter=lambda x: x[0],
                items="words",
                on_click=select_word,
            ),
            id="my_games_sg",
            width=3,
            height=10,
        ),
        Button(
            Format("📜{text_btn_show_ru}"),
            id="translate_words",
            on_click=on_off_word_ru,
        ),
        Cancel(Const("Выход"), id="text"),
        state=WordsScheduleSG.words_en,
        getter=get_words,
    ),
    Window(
        Format("{txt}"),
        Radio(
            checked_text=Format("🔘    {item[0]}"),
            unchecked_text=Format("⚪️    {item[0]}"),
            id="radio_stage",
            item_id_getter=operator.itemgetter(1),
            items="stages",
            on_click=select_stage,
        ),
        Back(Const("🔙Назад")),
        state=WordsScheduleSG.stage,
        getter=get_word_stage,
    ),
    Window(
        Format("{txt}"),
        Back(Const("🔙Назад")),
        state=WordsScheduleSG.full_en,
        getter=get_word_full,
    ),
    Window(
        Format("{txt}"),
        SwitchTo(
            Const("🔙Назад"),
            id="back_ru",
            state=WordsScheduleSG.words_en,
        ),
        state=WordsScheduleSG.full_ru,
        getter=get_word_full,
    ),
    Window(
        Format("{txt}"),
        SwitchTo(
            Const("🔙Назад"),
            id="back_trans",
            state=WordsScheduleSG.words_en,
        ),
        state=WordsScheduleSG.full_trans,
        getter=get_word_full,
    ),
)

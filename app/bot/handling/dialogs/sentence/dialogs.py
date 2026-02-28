import operator

from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Multiselect,
    Next,
    Row,
    ScrollingGroup,
    Select,
    SwitchInlineQuery,
)
from aiogram_dialog.widgets.text import Const, Format, Jinja, Multi

from ...states.en_text_translate import EnTextTranslateSG
from .getters import get_sentence, get_words
from .handlers import on_off_translate, on_off_words, words_filled

dialog = Dialog(
    Window(
        Jinja("Выбрана игра: <b>Перевод предложения</b>"),
        Format("{text}"),
        Next(Const("Переводы слов"), id="translate_words"),
        Button(Const("Следующее предложение"), id="text"),
        state=EnTextTranslateSG.show_text_en,
        getter=get_sentence,
    ),
    Window(
        Format("{text}"),
        Format("\n{text_translate}", when="is_show_translate"),
        Column(
            Multiselect(
                checked_text=Format("[✔️] {item[1]}"),
                unchecked_text=Format("[  ] {item[1]}"),
                id="multi_topics",
                item_id_getter=operator.itemgetter(0),
                items="words_en_ru",
                on_state_changed=words_filled,
                on_click=words_filled,
                when="is_show_words",
            ),
        ),
        Row(
            Button(
                Format("{text_btn_show_words}"),
                id="show_words",
                on_click=on_off_words,
            ),
            Button(
                Format("{text_btn_show_translate}"),
                id="is_show_translate",
                on_click=on_off_translate,
            ),
            Back(Const("Следующее предложение"), id="text_next"),
        ),
        state=EnTextTranslateSG.show_words_en_ru,
        getter=get_words,
    ),
)

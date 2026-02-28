from aiogram.fsm.state import State, StatesGroup


class EnTextTranslateSG(StatesGroup):
    start = State()
    show_text_en = State()
    show_words_en_ru = State()

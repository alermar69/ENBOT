from aiogram.fsm.state import State, StatesGroup


class EnTextTranslateSG(StatesGroup):
    start = State()
    show_text_en = State()
    show_words_en_ru = State()


class WordsScheduleSG(StatesGroup):
    start = State()
    words_en = State()
    words_en_ru = State()
    stage = State()
    full_en = State()
    full_ru = State()
    full_trans = State()

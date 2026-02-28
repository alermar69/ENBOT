from pathlib import Path

from core.config.settings import CONFIG_DIR


def read_text(name_file: str = "en_text.txt") -> list[str]:
    file_path = CONFIG_DIR.parent / name_file
    txt = file_path.read_text()
    txt = txt.replace("\n", " ")
    ls_txt = txt.split(". ")
    ls_txt.reverse()
    return ls_txt

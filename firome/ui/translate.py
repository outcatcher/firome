import json
import locale
from os import path


def _locale_name():
    sys_locale = locale.getlocale()[0]  # this is tuple

    if sys_locale in ["Russian_Russia", "ru_RU"]:
        return "ru_RU"

    return "en_US"


class Translator:
    def __init__(self, filename: str):
        filename = filename.format(_locale_name())

        tr_path = path.abspath(path.join(path.dirname(__file__), filename))
        with open(tr_path, "rb") as file:
            self.translations = json.load(file)

    def translate(self, key: str) -> str:
        return self.translations.get(key, str(key))

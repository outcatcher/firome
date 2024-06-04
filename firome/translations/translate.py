import locale
from configparser import ConfigParser
from os import path


def _locale_name():
    sys_locale = locale.getlocale()[0]  # this is tuple

    if sys_locale in ["Russian_Russia", "ru_RU"]:
        return "ru_RU"

    return "en_US"


class Translator:
    """Translator handling translations to language detected from system"""
    def __init__(self, domain: str):
        tr_path = path.abspath(path.join(path.dirname(__file__), "assets", domain + ".ini"))

        cfg = ConfigParser()
        cfg.read(tr_path)
        self.translations = cfg[_locale_name()]

    def translate(self, key: str) -> str:
        return self.translations.get(key, str(key))

import locale
from configparser import ConfigParser
from pathlib import Path


def _locale_name():
    sys_locale = locale.getlocale()[0]  # this is tuple

    if sys_locale in ["Russian_Russia", "ru_RU"]:
        return "ru_RU"

    return "en_US"


class Translator:
    """Translator handling translations to language detected from system."""

    def __init__(self, domain: str):
        tr_path = (Path(__file__).parent / "assets" / domain).with_suffix(".ini").resolve()

        cfg = ConfigParser()
        cfg.read(tr_path, encoding="utf-8")
        self.translations = cfg[_locale_name()]

    def translate(self, key: str) -> str:
        """Выполняет перевод по ключу."""
        return self.translations.get(key, str(key))

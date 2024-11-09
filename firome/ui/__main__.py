import argparse
import logging
import sys

from PySide6.QtWidgets import QApplication

from firome import __version__
from firome.logger import LOGGER
from firome.ui.main import MainWindow

app = QApplication(sys.argv)

parser = argparse.ArgumentParser(
    description="Combines GPX file with training data with GPX file with position data based on the distance",
)
parser.add_argument("--debug", action="store_true", help="Enable debug logging")
parser.add_argument("--version", action="store_true", help="Print app version")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.version:
        print(__version__) # noqa: T201  # не для дебага
        sys.exit(0)

    if args.debug:
        LOGGER.setLevel(logging.DEBUG)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec())

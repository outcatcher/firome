import sys

from PySide6.QtWidgets import QApplication

from firome.ui.main import MainWindow

app = QApplication(sys.argv)

if __name__ == '__main__':
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec())

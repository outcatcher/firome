import time

from PySide6.QtWidgets import *

from firome.export.tcx import export_as_tcx
from firome.merge import merge
from firome.ui.main_ui import Ui_MainWindow  # TODO: load directly from .ui file


class MainWindow(QMainWindow):

    def on_select_activity_click(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.ExistingFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter("FIT (*.fit)")
        if dialog.exec_():
            self.ui.inputActivitySelect.setText(dialog.selectedFiles()[0])

    def on_select_route_click(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.ExistingFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter("Route files (*.gpx)")
        if dialog.exec_():
            self.ui.inputRouteSelect.setText(dialog.selectedFiles()[0])

    def on_submit(self):
        points = merge(self.ui.inputRouteSelect.text(), self.ui.inputActivitySelect.text())

        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.AnyFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptSave)
        dialog.setDefaultSuffix("tcx")
        dialog.selectFile(f"{int(time.time())}.tcx")

        if dialog.exec_():
            export_as_tcx(points, dialog.selectedFiles()[0])

    def _reset_input(self):
        self.ui.inputRouteSelect.setText("")
        self.ui.inputActivitySelect.setText("")

    def on_cancel(self):
        self._reset_input()

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self.on_submit)
        self.ui.buttonBox.rejected.connect(self.on_cancel)

        self.ui.buttonRouteSelect.clicked.connect(self.on_select_route_click)
        self.ui.buttonActivitySelect.clicked.connect(self.on_select_activity_click)

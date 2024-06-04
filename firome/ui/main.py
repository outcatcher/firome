import time

from PySide6.QtCore import QRunnable, Slot, QThreadPool, Signal, QObject
from PySide6.QtWidgets import QMainWindow, QFileDialog, QSlider, QCheckBox, QLabel

from .main_ui import Ui_MainWindow
from ..classes.export import list_export_fields, ExportFields
from ..classes.points import DataPoint
from ..codecs.tcx import export_as_tcx
from ..merge import merge
from ..translations.translate import Translator

_precision_positions = (0.5, 1.0, 2.0, 3.0, 4.0, 5.0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # gettext seems bit too complex
        self._translator = Translator("ui")

        self._export_fields = ExportFields()

        self._threadpool = QThreadPool()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self.on_submit)
        self.ui.buttonBox.rejected.connect(self.on_cancel)

        self.ui.buttonRouteSelect.clicked.connect(self.on_select_route_click)
        self.ui.buttonActivitySelect.clicked.connect(self.on_select_activity_click)

        self._init_precision_slider()

        self._checkbox_values = self._init_checkboxes()

        self._translate_static()

    def tr(self, msg, *_):
        return self._translator.translate(msg)

    def on_select_activity_click(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.ExistingFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter(self.tr("nameFilterActivity") + " (*.fit *.fit.zip)")
        if dialog.exec_():
            self.ui.inputActivitySelect.setText(dialog.selectedFiles()[0])

    def on_select_route_click(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.ExistingFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter(self.tr("nameFilterRoute") + " (*.gpx)")
        if dialog.exec_():
            self.ui.inputRouteSelect.setText(dialog.selectedFiles()[0])

    def on_submit(self):
        worker = MergeWorker(self.ui.inputRouteSelect.text(), self.ui.inputActivitySelect.text(), self.precision)
        worker.signals.result.connect(self._on_finish_merge)

        self.ui.buttonBox.blockSignals(True)
        self.ui.buttonBox.setEnabled(False)

        self._threadpool.start(worker)

    def _on_finish_merge(self, points: list[DataPoint]):
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.AnyFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptSave)
        dialog.setDefaultSuffix("tcx")
        dialog.selectFile(f"{int(time.time())}.tcx")

        if dialog.exec_():
            checkbox_dict = {k: v.isChecked() for k, v in self._checkbox_values.items()}

            export_as_tcx(points, dialog.selectedFiles()[0], ExportFields(**checkbox_dict))

        self._reset_input()
        self.ui.buttonBox.blockSignals(False)
        self.ui.buttonBox.setEnabled(True)

    def _reset_input(self):
        self.ui.inputRouteSelect.setText("")
        self.ui.inputActivitySelect.setText("")
        self.ui.horizontalSlider.setSliderPosition(1)

    def on_cancel(self):
        self._reset_input()

    def _init_precision_slider(self):
        slider = self.ui.horizontalSlider
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        slider.setRange(0, len(_precision_positions) - 1)
        slider.setTickInterval(1)
        slider.setPageStep(1)
        slider.setSliderPosition(1)
        slider.setTracking(True)

        self._update_precision_value()

        slider.valueChanged.connect(self._update_precision_value)

    def _init_checkboxes(self) -> dict[str, QCheckBox]:
        checkbox_values = {}

        layout = self.ui.checkboxLayout

        layout.addWidget(QLabel(self.tr("labelSelectExportedList")))

        for field in list_export_fields():
            checkbox = QCheckBox(self.tr(field), self)
            checkbox.stateChanged.connect(lambda v: self._set_export_field(field, bool(v)))
            checkbox.setChecked(True)

            layout.addWidget(checkbox)

            checkbox_values[field] = checkbox

        return checkbox_values

    def _set_export_field(self, name: str, value: bool):
        setattr(self._export_fields, name, value)

    @property
    def precision(self) -> float:
        return _precision_positions[self.ui.horizontalSlider.sliderPosition()]

    def _update_precision_value(self):
        self.ui.precisionValue.setText(str(self.precision))

    def _translate_static(self):
        self.ui.buttonRouteSelect.setText(self.tr("btnRouteSelect"))
        self.ui.buttonActivitySelect.setText(self.tr("btnActivitySelect"))
        self.ui.precisionLabel.setText(self.tr("lblPrecision"))

        for button in self.ui.buttonBox.buttons():
            button.setText(self.tr(button.text()))


class WorkerSignals(QObject):
    result = Signal(list)


class MergeWorker(QRunnable):
    """Worker thread"""

    def __init__(self, route_path: str, recording_path: str, precision: float):
        super().__init__()

        self.args = (route_path, recording_path, precision)
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        result = merge(*self.args)
        self.signals.result.emit(result)

import time
from pathlib import Path

from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QCheckBox, QFileDialog, QLabel, QMainWindow, QSlider

from .. import __version__
from ..classes.export import ExportFields
from ..classes.points import DataPoint, PositionPoint
from ..codecs.tcx import export_as_tcx
from ..i18n import Translator
from .main_ui import Ui_MainWindow
from .main_workers import LoadActivityWorker, LoadRouteWorker, MergeWorker

_precision_positions = (0.5, 1.0, 2.0, 3.0, 4.0, 5.0)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self._route_points = []
        self._activity_points = []

        # gettext seems bit too complex
        self._translator = Translator("ui")

        self._export_fields = ExportFields()

        self._threadpool = QThreadPool()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f"Firome {__version__}")

        self.ui.buttonBox.accepted.connect(self._on_submit)
        self.ui.buttonBox.rejected.connect(self._on_cancel)

        self.ui.buttonRouteSelect.clicked.connect(self._on_select_route_click)
        self.ui.buttonActivitySelect.clicked.connect(self._on_select_activity_click)

        self._init_precision_slider()

        self._checkbox_values = self._init_checkboxes()

        self._translate_static()

    def t(self, msg, *_):
        """Translate given message."""
        return self._translator.translate(msg)

    def _on_select_activity_click(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.ExistingFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter(self.t("nameFilterActivity") + " (*.fit *.fit.zip)")
        if dialog.exec_():
            self.ui.inputActivitySelect.setText(dialog.selectedFiles()[0])
            self._on_activity_select()

    def _on_select_route_click(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.FileMode.ExistingFile)
        dialog.setAcceptMode(dialog.AcceptMode.AcceptOpen)
        dialog.setNameFilter(self.t("nameFilterRoute") + " (*.gpx)")
        if dialog.exec_():
            self.ui.inputRouteSelect.setText(dialog.selectedFiles()[0])
            self._on_route_select()

    def _block_buttons(self):
        self.ui.buttonBox.blockSignals(True) #noqa:FBT003 # boolead is the only argument
        self.ui.buttonBox.setEnabled(False)

    def _unblock_buttons(self):
        self.ui.buttonBox.blockSignals(False) #noqa:FBT003 # boolead is the only argument
        self.ui.buttonBox.setEnabled(True)

    def _on_route_select(self):
        worker = LoadRouteWorker(Path(self.ui.inputRouteSelect.text()), self._precision)
        worker.signals.result.connect(self._on_load_route)

        self._block_buttons()

        self._threadpool.start(worker)

    def _on_load_route(self, positions: list[PositionPoint]):
        self.ui.labelRouteLen.setText(self._len_to_test(positions[-1].distance))
        self._route_points = positions

        self._unblock_buttons()

    def _on_activity_select(self):
        worker = LoadActivityWorker(Path(self.ui.inputActivitySelect.text()))
        worker.signals.result.connect(self._on_load_activity)

        self._block_buttons()

        self._threadpool.start(worker)

    def _on_load_activity(self, points: list[DataPoint]):
        self.ui.labelActivityLen.setText(self._len_to_test(points[-1].distance))
        self._activity_points = points

        self._unblock_buttons()

    def _on_submit(self):
        worker = MergeWorker(self._route_points, self._activity_points, self._precision)
        worker.signals.result.connect(self._on_finish_merge)

        self._block_buttons()

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
        self._unblock_buttons()

    def _reset_input(self):
        self.ui.inputRouteSelect.setText("")
        self.ui.inputActivitySelect.setText("")

        self.ui.horizontalSlider.setSliderPosition(1)

        self.ui.labelRouteLen.setText(self._len_to_test(0))
        self.ui.labelActivityLen.setText(self._len_to_test(0))

    def _len_to_test(self, length_meters: float):
        km = int(length_meters / 1000)
        m = round(length_meters % 1000)

        parts = []

        if km > 0:
            parts.append(f"{km}{self.t('km')}")

        if m > 0 or km == 0:
            parts.append(f"{m}{self.t('m')}")

        return " ".join(parts)

    def _on_cancel(self):
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

        layout.addWidget(QLabel(self.t("labelSelectExportedList")))

        for field in ExportFields.list_fields():
            checkbox = QCheckBox(self.t(field), self)
            checkbox.stateChanged.connect(self._handle_set_export_field)
            checkbox.setChecked(True)

            layout.addWidget(checkbox)

            checkbox_values[field] = checkbox

        return checkbox_values

    def _handle_set_export_field(self, name: str):
        def _set_export_field(value):
            setattr(self._export_fields, name, bool(value))

        return _set_export_field

    @property
    def _precision(self) -> float:
        return _precision_positions[self.ui.horizontalSlider.sliderPosition()]

    def _update_precision_value(self):
        self.ui.precisionValue.setText(str(self._precision))

        if len(self._route_points) > 0:
            # update distance with updated precision
            self._on_route_select()

    def _translate_static(self):
        self.ui.buttonRouteSelect.setText(self.t("btnRouteSelect"))
        self.ui.buttonActivitySelect.setText(self.t("btnActivitySelect"))
        self.ui.precisionLabel.setText(self.t("lblPrecision"))

        for button in self.ui.buttonBox.buttons():
            button.setText(self.t(button.text()))

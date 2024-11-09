from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from ..classes.points import DataPoint, PositionPoint
from ..codecs.fit import parse_fit
from ..codecs.gpx import interpolate, parse_gpx
from ..merge import merge


class WorkerSignals(QObject):
    """Signals supported by worker."""

    result = Signal(list)


class LoadRouteWorker(QRunnable):
    """Loading and interpolating route."""

    def __init__(self, route_path: str, precision: float):
        super().__init__()

        self.args = (route_path, precision)
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Execute route loading and interpolation."""
        route_path, precision = self.args
        result = interpolate(parse_gpx(route_path), precision)

        self.signals.result.emit(result)


class LoadActivityWorker(QRunnable):
    """Loading activity."""

    def __init__(self, activity_path: str):
        super().__init__()

        self.args = (activity_path,)
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Execute activity loading."""
        result = parse_fit(self.args[0])

        self.signals.result.emit(result)


class MergeWorker(QRunnable):
    """Worker thread."""

    def __init__(self, position_elements: list[PositionPoint], data_elements: list[DataPoint], precision: float):
        super().__init__()

        self.args = (position_elements, data_elements, precision)
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        """Merge input data."""
        result = merge(*self.args)
        self.signals.result.emit(result)

from datetime import datetime, timezone
from pathlib import Path

from fitdecode import FIT_FRAME_DATA, FitDataMessage, FitReader

from ...classes.points import DataPoint
from ...logger import LOGGER
from ..errors import UnsupportedFileExtError
from ..zip import unzip

__max_delta_days = 120  # expected activity date range from now


def parse_fit(src: Path) -> list[DataPoint]:
    """Parse FIT file by given path."""
    if src.suffix.lower() == ".zip":
        src = unzip(src)

    if not src.suffix.lower() == ".fit":
        raise UnsupportedFileExtError(src)

    with FitReader(src) as fit:
        return FitParser(fit).process()


class FitParserRecreatedError(Exception):
    """__FitParser был создан второй раз."""


class FitParser:
    """FIT file parser."""

    def __init__(self, reader: FitReader):
        self._lap = 1  # track increasing lap value
        self._fit = reader
        self._closed = False
        self._reference_date = None

    def process(self):
        """Execute FIT file processing."""
        if self._closed:
            raise FitParserRecreatedError

        result = []

        for data in self._fit:
            point = self.__frame_to_point(data)

            if point is None or point.distance is None:
                continue

            if point.timestamp.tzinfo is None:
                point.timestamp = point.timestamp.replace(tzinfo=timezone.utc)

            result.append(point)

        self._closed = True

        result.sort(key=lambda x: x.distance)

        # expecting sorted list here
        self.__fix_timestamps(result)

        return result

    @staticmethod
    def __fix_timestamps(points: list[DataPoint]):
        err_index = []

        for i in range(1, len(points) - 1):
            if not _ts_ok(points[i - 1].timestamp, points[i].timestamp, points[i + 1].timestamp):
                err_index.append(i)  # not mutating slice during iteration  # noqa:PERF401  # too complex

        if size := len(err_index):
            LOGGER.error("found %d broken timestamps in activity", size)

        for idx in err_index:
            points[idx].timestamp = _fix_ts(points[idx].timestamp, points[idx - 1].timestamp, points[idx + 1].timestamp)

    def __frame_to_point(self, data: FitDataMessage) -> DataPoint | None:
        if data.frame_type != FIT_FRAME_DATA:
            return None

        if data.has_field("lap_trigger"):
            self._lap += 1

        if not data.has_field("distance"):
            LOGGER.debug(data.frame_type)
            LOGGER.debug([field.name for field in data.fields])

            return None

        return DataPoint(
            timestamp=data.get_value("timestamp").replace(tzinfo=timezone.utc),
            distance=data.get_value("distance"),
            speed=data.get_value("speed", fallback=None),
            power=data.get_value("power", fallback=None),
            heart_rate=data.get_value("heart_rate", fallback=None),
            cadence=data.get_value("cadence"),
            lap=self._lap,
        )


def _ts_ok(prev, curr, nxt):
    if prev > curr:
        return False

    # if next < prev, then next is broken
    if curr > nxt >= prev:
        return False

    return (curr - prev).days == 0


def _fix_ts(current: datetime, normal_previous: datetime, next_ts: datetime) -> datetime:
    current_fix_date = current.replace(year=normal_previous.year, month=normal_previous.month, day=normal_previous.day)

    if _ts_ok(normal_previous, current_fix_date, next_ts):
        LOGGER.debug("only date is broken: %s", current.ctime())
        return current_fix_date

    LOGGER.debug("full replace %s with %s", current.ctime(), normal_previous.ctime())
    return normal_previous

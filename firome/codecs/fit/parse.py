from fitdecode import FitReader, FitDataMessage, FIT_FRAME_DATA

from ..zip import unzip
from ..errors import UnsupportedFileExtError
from ...logger import LOGGER
from ...classes.points import DataPoint


def parse_fit(src: str) -> list[DataPoint]:
    if src.lower().endswith(".zip"):
        src = unzip(src)

    if not src.lower().endswith(".fit"):
        raise UnsupportedFileExtError(src)

    with FitReader(src) as fit:
        result = __FitParser(fit).process()

    return result


class __FitParser:
    def __init__(self, reader: FitReader):
        self._lap = 1  # track increasing lap value
        self._fit = reader
        self._closed = False

    def process(self):
        if self._closed:
            raise Exception("__FitParser reused")

        result = []

        for data in self._fit:
            point = self.__frame_to_point(data)

            if point is None:
                continue

            result.append(point)

        self._closed = True

        return result

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
            timestamp=data.get_value("timestamp"),
            distance=data.get_value("distance"),
            speed=data.get_value("speed", fallback=None),
            power=data.get_value("power", fallback=None),
            heart_rate=data.get_value("heart_rate", fallback=None),
            cadence=data.get_value("cadence"),
            lap=self._lap,
        )

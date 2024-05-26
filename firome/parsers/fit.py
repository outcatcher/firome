from fitdecode import FitReader, FitDataMessage, FIT_FRAME_DATA

from ..logging import LOGGER
from ..types.points import Point


def parse_fit(src: str) -> list[Point]:
    if not src.lower().endswith(".fit"):
        raise Exception("unsupported file type")

    result = []

    with FitReader(src) as fit:
        for data in fit:
            point = frames_to_point(data)

            if point is None:
                continue

            result.append(point)

    return result


_LAP = 1


def frames_to_point(data: FitDataMessage) -> Point | None:
    global _LAP  # TODO: в будущем убрать в класс?

    if data.frame_type != FIT_FRAME_DATA:
        return None

    if data.has_field("lap_trigger"):
        _LAP += 1

    if not data.has_field("distance"):
        LOGGER.debug(data.frame_type)
        LOGGER.debug([field.name for field in data.fields])

        return None

    return Point(
        timestamp=data.get_value("timestamp"),
        distance=data.get_value("distance"),
        speed=data.get_value("speed", fallback=None),
        power=data.get_value("power", fallback=None),
        heart_rate=data.get_value("heart_rate", fallback=None),
        cadence=data.get_value("cadence"),
        lap=_LAP,
    )

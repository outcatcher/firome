from fitdecode import FitReader, FitDataMessage, FIT_FRAME_DATA

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


def frames_to_point(data: FitDataMessage) -> Point | None:
    if data.frame_type != FIT_FRAME_DATA:
        return None

    if not data.has_field("distance"):
        return None

    return Point(
        timestamp=data.get_value("timestamp"),
        distance=data.get_value("distance"),
        speed=data.get_value("speed", fallback=None),
        power=data.get_value("power", fallback=None),
        heart_rate=data.get_value("heart_rate", fallback=None),
        cadence=data.get_value("cadence")
    )

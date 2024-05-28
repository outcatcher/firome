from .parsers.fit import parse_fit
from .parsers.gpx import parse_gpx
from .types.points import Point


def merge(route_path: str, recording_path: str) -> list[Point]:
    position_elements = parse_gpx(route_path)
    data_elements = parse_fit(recording_path)

    p_i = d_i = 0
    # todo: возможно, придётся пре-аллоцировать память, если будут большие файлы
    result = []  # [None] * (len(position_elements)+len(data_elements))

    last_timestamp = data_elements[0].timestamp

    while d_i < len(data_elements):
        if p_i < len(position_elements) and position_elements[p_i].distance < data_elements[d_i].distance:
            # допущение, ожидаемое число точек на треке намного меньше точек из FIT файла
            position_elements[p_i].timestamp = last_timestamp
            result.append(position_elements[p_i])
            p_i += 1

        result.append(data_elements[d_i])
        last_timestamp = data_elements[d_i].timestamp

        d_i += 1

    return result

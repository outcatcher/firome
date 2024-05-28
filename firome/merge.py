from .parsers.fit import parse_fit
from .parsers.gpx import parse_gpx
from .parsers.gpx_interpolate import interpolate
from .types.points import Point


def merge(route_path: str, recording_path: str) -> list[Point]:
    position_elements = interpolate(parse_gpx(route_path), 5.0)

    data_elements = parse_fit(recording_path)

    p_i = d_i = 0
    # todo: возможно, придётся пре-аллоцировать память, если будут большие файлы
    result = []  # [None] * (len(position_elements)+len(data_elements))

    last_point = data_elements[0]

    while d_i < len(data_elements):
        if p_i < len(position_elements) and position_elements[p_i].distance < data_elements[d_i].distance:
            # align position data with activity data
            position_elements[p_i].timestamp = last_point.timestamp
            position_elements[p_i].speed = last_point.speed
            position_elements[p_i].power = last_point.power
            position_elements[p_i].cadence = last_point.cadence
            position_elements[p_i].heart_rate = last_point.heart_rate
            result.append(position_elements[p_i])
            p_i += 1

        result.append(data_elements[d_i])
        last_point = data_elements[d_i]

        d_i += 1

    return result

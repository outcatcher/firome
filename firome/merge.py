import math

from .parsers.fit import parse_fit
from .parsers.gpx import parse_gpx
from .parsers.gpx_interpolate import interpolate
from .classes.points import DataPoint, PositionPoint


def merge(route_path: str, recording_path: str, precision: float) -> list[DataPoint]:
    """Merges positions into data recording"""

    position_elements = interpolate(parse_gpx(route_path), precision)

    data_elements = parse_fit(recording_path)

    _merge(position_elements, data_elements, precision)

    return data_elements


def _merge(position_elements: list[PositionPoint], data_elements: list[DataPoint], precision: float):
    p_start = d_i = 0

    p_len = len(position_elements)
    d_len = len(data_elements)

    while d_i < d_len:
        for p_i in range(p_start, p_len):
            if math.isclose(position_elements[p_i].distance, data_elements[d_i].distance, abs_tol=precision / 2):
                data_elements[d_i].position = position_elements[p_i].position
                data_elements[d_i].elevation = position_elements[p_i].elevation
                p_start = p_i

                break

        d_i += 1

import math

from .classes.points import DataPoint, PositionPoint


def merge(position_elements: list[PositionPoint], data_elements: list[DataPoint], precision: float):
    """Update data_elements points with position data"""

    p_start = d_i = 0

    p_len = len(position_elements)
    d_len = len(data_elements)

    while d_i < d_len:
        for p_i in range(p_start, p_len):
            if data_elements[d_i].distance is None:
                continue

            if math.isclose(position_elements[p_i].distance, data_elements[d_i].distance, abs_tol=precision / 2):
                data_elements[d_i].position = position_elements[p_i].position
                data_elements[d_i].elevation = position_elements[p_i].elevation
                p_start = p_i

                break

        d_i += 1

    return data_elements

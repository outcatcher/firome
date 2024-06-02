# MIT License
#
# Copyright (c) 2019 Remi Salmon, 2024 Anton Kachurin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Original implementation:
# https://github.com/remisalmon/gpx-interpolate/blob/00af3c636d566d049f6a140c093af4e91d0482d5/gpx_interpolate.py
from typing import Dict, List, Union

import numpy as np
from scipy.interpolate import pchip_interpolate

from firome.logger import LOGGER
from firome.classes.points import PositionPoint

# classes
GPXData = Dict[str, Union[List[float], None]]

# globals
_EARTH_RADIUS = 6371e3  # meters
_EPS = 1e-6  # seconds

_fields = ("lat", "lon", "ele", "dist")


def interpolate(track: list[PositionPoint], resolution: float) -> list[PositionPoint]:
    """
    Interpolates track with given resolution (m)
    """
    gpx_data = __from_track(track)
    gpx_data_nodup = __gpx_remove_duplicates(gpx_data)

    if not len(gpx_data_nodup["lat"]) == len(gpx_data["lat"]):
        LOGGER.warn("Removed {} duplicate trackpoint(s)".format(len(gpx_data["lat"]) - len(gpx_data_nodup["lat"])))

    gpx_data_interp = __gpx_interpolate(gpx_data_nodup, resolution)

    return __to_track(gpx_data_interp)


def __gpx_interpolate(gpx_data: GPXData, res: float = 5.0) -> GPXData:
    """
    Returns gpx_data interpolated with a spatial resolution res using piecewise cubic Hermite splines.

    if num is passed, gpx_data is interpolated to num points and res is ignored.
    """

    if all(gpx_data[i] in (None, []) for i in _fields):
        return gpx_data

    _gpx_data = __gpx_remove_duplicates(gpx_data)
    _gpx_dist = __gpx_calculate_distance(_gpx_data, use_ele=True)

    xi = np.cumsum(_gpx_dist)
    yi = np.array([_gpx_data[i] for i in _fields if _gpx_data[i]])

    num = int(np.ceil(xi[-1] / res))

    x = np.linspace(xi[0], xi[-1], num=num, endpoint=True)
    y = pchip_interpolate(xi, yi, x, axis=1)

    gpx_data_interp = {
        "lat": list(y[0, :]),
        "lon": list(y[1, :]),
        "ele": list(y[2, :]) if gpx_data["ele"] else None,
        "dist": list(y[3, :]),
    }

    return gpx_data_interp


def __gpx_calculate_distance(gpx_data: GPXData, use_ele: bool = True) -> List[float]:
    """
    Returns the distance between GPX trackpoints.

    if use_ele is True and gpx_data['ele'] is not None, the elevation data is used to compute the distance.
    """

    gpx_dist = np.zeros(len(gpx_data["lat"]))

    for i in range(len(gpx_dist) - 1):
        lat1 = np.radians(gpx_data["lat"][i])
        lon1 = np.radians(gpx_data["lon"][i])
        lat2 = np.radians(gpx_data["lat"][i + 1])
        lon2 = np.radians(gpx_data["lon"][i + 1])

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        c = 2.0 * np.arcsin(
            np.sqrt(np.sin(delta_lat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2.0) ** 2)
        )  # haversine formula

        dist_latlon = _EARTH_RADIUS * c  # great-circle distance

        if gpx_data["ele"] and use_ele:
            dist_ele = gpx_data["ele"][i + 1] - gpx_data["ele"][i]

            gpx_dist[i + 1] = np.sqrt(dist_latlon**2 + dist_ele**2)
        else:
            gpx_dist[i + 1] = dist_latlon

    return gpx_dist.tolist()


def __gpx_remove_duplicates(gpx_data: GPXData) -> GPXData:
    """
    Returns gpx_data where duplicate trackpoints are removed.
    """

    gpx_dist = __gpx_calculate_distance(gpx_data, use_ele=False)

    i_dist = np.concatenate(([0], np.nonzero(gpx_dist)[0]))  # keep gpx_dist[0] = 0.0

    if len(i_dist) == len(gpx_dist):
        return gpx_data

    gpx_data_nodup = dict.fromkeys(_fields, [])

    for k in _fields:
        gpx_data_nodup[k] = [gpx_data[k][i] for i in i_dist] if gpx_data[k] else None

    return gpx_data_nodup


def __from_track(track: list[PositionPoint]) -> GPXData:
    """
    Returns a GPXData structure from a GPX file.
    """

    # for some reason `dict.fromkeys(_fields, [])` not working, scipy tries to allocate a lot of data (40G+)
    gpx_data = {"lat": [], "lon": [], "ele": [], "dist": []}

    for point in track:
        gpx_data["lat"].append(point.position[0])
        gpx_data["lon"].append(point.position[1])
        gpx_data["ele"].append(point.elevation)
        gpx_data["dist"].append(point.distance)

    return gpx_data


def __to_track(gpx_data: GPXData) -> list[PositionPoint]:
    gpx_track = []

    for i in range(len(gpx_data["lat"])):
        lat = gpx_data["lat"][i]
        lon = gpx_data["lon"][i]
        dist = gpx_data["dist"][i]
        ele = gpx_data["ele"][i] if gpx_data["ele"] else None

        gpx_point = PositionPoint(position=(lat, lon), elevation=ele, distance=dist)

        gpx_track.append(gpx_point)

    return gpx_track

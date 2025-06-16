from pathlib import Path

from geopy.distance import geodesic
from lxml import etree

from ...classes.points import Position, PositionPoint
from ..errors import UnsupportedFileExtError
from ..xml import add_ns
from ..zip import unzip


def parse_gpx(src: Path) -> list[PositionPoint]:
    """Parse GPX file by given path."""
    if src.suffix.lower() == ".zip":
        src = unzip(src)

    if not src.suffix.lower() == ".gpx":
        raise UnsupportedFileExtError(src)

    result = []

    root = etree.parse(src).getroot()  # локальное приложение

    default_ns = root.nsmap[None]

    track_points = root.findall(
        "./" + add_ns("trk", default_ns) + "/" + add_ns("trkseg", default_ns) + "/" + add_ns("trkpt", default_ns),
    )

    prev = None

    for point in track_points:
        position = Position(float(point.attrib["lat"]), float(point.attrib["lon"]))

        elevation_element = point.find("./" + add_ns("ele", default_ns))

        gpx_point = PositionPoint(
            position=position,
            distance=__total_distance(position, prev),
        )

        if (elevation_element is not None) and (elevation_element.text is not None):
            gpx_point.elevation = float(elevation_element.text)

        result.append(gpx_point)

        prev = gpx_point

    return result


def __total_distance(current: Position, previous: PositionPoint | None) -> float:
    if previous is None:
        return 0

    distance = geodesic(current, previous.position)

    return distance.meters + previous.distance

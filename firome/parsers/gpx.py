from typing import Optional

from geopy.distance import geodesic
from lxml import etree

from ..types.points import Position, PositionPoint


def parse_gpx(src: str) -> list[PositionPoint]:
    result = []

    root: etree.ElementBase = etree.parse(src).getroot()

    default_ns = root.nsmap[None]

    track_points: list[etree.ElementBase] = root.findall(
        "./" + add_ns("trk", default_ns) + "/" + add_ns("trkseg", default_ns) + "/" + add_ns("trkpt", default_ns)
    )

    prev = None

    for point in track_points:
        position = (float(point.attrib["lat"]), float(point.attrib["lon"]))

        elevation_element: etree.ElementBase = point.find("./" + add_ns("ele", default_ns))

        gpx_point = PositionPoint(
            position=position,
            distance=total_distance(position, prev),
            elevation=float(elevation_element.text),
        )
        result.append(gpx_point)

        prev = gpx_point

    return result


def add_ns(tag, ns):
    return f"{{{ns}}}{tag}"


def total_distance(current: Position, previous: Optional[PositionPoint]) -> float:
    if previous is None:
        return 0

    distance = geodesic(current, previous.position)

    return distance.meters + previous.distance

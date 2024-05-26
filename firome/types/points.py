import dataclasses
import datetime

Position = tuple[float, float]


@dataclasses.dataclass(kw_only=True)
class Point:
    timestamp: datetime.datetime = None
    position: Position = None
    elevation: float = None
    distance: float = 0
    speed: float = None
    power: int = None
    heart_rate: int = None
    cadence: int = None
    lap: int = None

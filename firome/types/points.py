import dataclasses
import datetime

Position = tuple[float, float]


@dataclasses.dataclass
class DataPoint:
    timestamp: datetime.datetime = None
    speed: float = None
    power: int = None
    heart_rate: int = None
    cadence: int = None
    lap: int = None

    position: Position = None
    distance: float = 0
    elevation: float = None


@dataclasses.dataclass
class PositionPoint:
    position: Position
    distance: float
    elevation: float

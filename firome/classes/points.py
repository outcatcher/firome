from dataclasses import dataclass
from datetime import datetime

Position = tuple[float, float]


@dataclass
class DataPoint:
    timestamp: datetime = None
    speed: float = None
    power: int = None
    heart_rate: int = None
    cadence: int = None
    lap: int = None

    position: Position = None
    distance: float = 0
    elevation: float = None


@dataclass
class PositionPoint:
    position: Position
    distance: float
    elevation: float

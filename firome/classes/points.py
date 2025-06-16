from dataclasses import dataclass
from datetime import datetime


@dataclass
class Position:
    """GPS position."""

    latitude: float
    longitude: float

@dataclass
class DataPoint:
    """Single activity data point."""

    timestamp: datetime | None = None
    speed: float | None = None
    power: int | None = None
    heart_rate: int | None = None
    cadence: int | None = None
    lap: int | None = None

    position: Position | None = None
    distance: float = 0
    elevation: float | None = None


@dataclass
class PositionPoint:
    """Single position point."""

    position: Position
    distance: float
    elevation: float | None = None

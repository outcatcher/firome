from dataclasses import asdict, dataclass


@dataclass
class ExportFields:
    """Exported data fields."""

    altitude: bool = False
    distance: bool = True
    heart_rate: bool = True
    cadence: bool = True
    speed: bool = True
    power: bool = True

    @classmethod
    def list_fields(cls):
        """List of field names."""
        return asdict(cls()).keys()

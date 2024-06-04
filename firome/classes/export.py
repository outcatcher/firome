from dataclasses import dataclass, asdict


@dataclass
class ExportFields:
    altitude: bool = False
    distance: bool = True
    heart_rate: bool = True
    cadence: bool = True
    speed: bool = True
    power: bool = True

    @classmethod
    def list_fields(cls):
        return asdict(cls()).keys()

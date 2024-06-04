from dataclasses import dataclass, asdict


@dataclass
class ExportFields:
    Altitude: bool = False
    Distance: bool = True
    HeartRate: bool = True
    Cadence: bool = True
    Speed: bool = True
    Power: bool = True


def list_export_fields():
    return asdict(ExportFields()).keys()

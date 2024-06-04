from ..xml import add_ns

_namespaces = {
    # ref: https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd
    None: "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
    "ns5": "http://www.garmin.com/xmlschemas/ActivityGoals/v1",
    # ref: https://www8.garmin.com/xmlschemas/ActivityExtensionv2.xsd
    "ns3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2",
    "ns2": "http://www.garmin.com/xmlschemas/UserProfile/v2",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "ns4": "http://www.garmin.com/xmlschemas/ProfileExtension/v1",
}

_time_format = "%Y-%m-%dT%H:%M:%SZ"


def _with_ns(tag: str, ns_key: str | None = None) -> str:
    return add_ns(tag, _namespaces[ns_key])

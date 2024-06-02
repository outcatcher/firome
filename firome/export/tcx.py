from datetime import timezone

from lxml import etree
from lxml.etree import ElementBase

from ..classes.export import ExportFields
from ..classes.points import DataPoint

namespaces = {
    # ref: https://www8.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd
    None: "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
    "ns5": "http://www.garmin.com/xmlschemas/ActivityGoals/v1",
    # ref: https://www8.garmin.com/xmlschemas/ActivityExtensionv2.xsd
    "ns3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2",
    "ns2": "http://www.garmin.com/xmlschemas/UserProfile/v2",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "ns4": "http://www.garmin.com/xmlschemas/ProfileExtension/v1",
}

time_format = "%Y-%m-%dT%H:%M:%SZ"


def with_ns(tag: str, ns_key: str | None = None) -> str:
    return f"{{{namespaces[ns_key]}}}{tag}"


def export_as_tcx(points: list[DataPoint], destination: str, fields=ExportFields()):
    start_ts = points[0].timestamp.strftime(time_format)

    root_attrs = {
        etree.QName(
            "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"
        ): "http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2 "
        "http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"
    }
    root: ElementBase = etree.Element(with_ns("TrainingCenterDatabase"), root_attrs, nsmap=namespaces)

    activities = etree.SubElement(root, with_ns("Activities"))

    activity = etree.SubElement(activities, with_ns("Activity"), {"Sport": "Biking"})

    activity_id = etree.SubElement(activity, with_ns("Id"))
    activity_id.text = start_ts

    notes = etree.SubElement(activity, with_ns("Notes"))
    notes.text = "Merged by firome"

    lap_i = 0
    lap_track = None

    for p in points:
        if p.lap is None:
            if lap_track is None:
                continue

            p.lap = lap_i

        if p.lap != lap_i:
            lap_i = p.lap

            lap_track = new_lap(activity, start_ts)

        append_point(p, lap_track, fields)

    root.getroottree().write(destination, encoding="utf-8", xml_declaration=True)


def new_lap(activity: etree.ElementBase, start_ts: str) -> etree.ElementBase:
    lap = etree.SubElement(activity, with_ns("Lap"), {"StartTime": start_ts})

    lap_trigger_method = etree.SubElement(lap, with_ns("TriggerMethod"))
    lap_trigger_method.text = "Manual"

    lap_track = etree.SubElement(lap, with_ns("Track"))

    return lap_track


def append_point(point: DataPoint, base_element: etree.ElementBase, fields: ExportFields) -> etree.ElementBase:
    """Trackpoint example

    <Trackpoint>
      <Time>2014-11-30T05:51:36Z</Time>
      <Position>
        <LatitudeDegrees>51.791013</LatitudeDegrees>
        <LongitudeDegrees>39.199698</LongitudeDegrees>
      </Position>
      <AltitudeMeters>152</AltitudeMeters>
      <DistanceMeters>149567728363.23</DistanceMeters>
      <HeartRateBpm>
       <Value>168</Value>
      </HeartRateBpm>
      <Cadence>90</Cadence>
      <Extensions>
        <ns3:TPX>
          <ns3:Speed>0</ns3:Speed>
          <ns3:Watts>135</ns3:Watts>
        </ns3:TPX>
      </Extensions>
    </Trackpoint>
    """
    result = etree.SubElement(base_element, with_ns("Trackpoint"))

    # <Time>2014-11-30T05:51:36Z</Time>
    p_time = etree.SubElement(result, with_ns("Time"))
    p_time.text = point.timestamp.astimezone(timezone.utc).strftime(time_format)

    #   <Position>
    #     <LatitudeDegrees>51.791013</LatitudeDegrees>
    #     <LongitudeDegrees>39.199698</LongitudeDegrees>
    #   </Position>

    if point.position is not None:
        p_position = etree.SubElement(result, with_ns("Position"))
        p_pos_lat = etree.SubElement(p_position, with_ns("LatitudeDegrees"))
        p_pos_lat.text = str(point.position[0])
        p_pos_lon = etree.SubElement(p_position, with_ns("LongitudeDegrees"))
        p_pos_lon.text = str(point.position[1])

    #  <AltitudeMeters>152</AltitudeMeters>
    if fields.Altitude and point.elevation is not None:
        p_alt = etree.SubElement(result, with_ns("AltitudeMeters"))
        p_alt.text = str(point.elevation)

    # <DistanceMeters>14956.23</DistanceMeters>
    if fields.Distance:
        p_distance = etree.SubElement(result, with_ns("DistanceMeters"))
        p_distance.text = str(point.distance)

    #   <HeartRateBpm>
    #     <Value>168</Value>
    #   </HeartRateBpm>
    if fields.HeartRate and point.heart_rate is not None:
        p_hr = etree.SubElement(result, with_ns("HeartRateBpm"))
        p_hr_val = etree.SubElement(p_hr, with_ns("Value"))
        p_hr_val.text = str(point.heart_rate)

    # <Cadence>90</Cadence>
    if fields.Cadence and point.cadence is not None:
        p_cadence = etree.SubElement(result, with_ns("Cadence"))
        p_cadence.text = str(point.cadence)

    #   <Extensions>
    #       <ns3:TPX>
    #           <ns3:Speed>0</ns3:Speed>
    #           <ns3:Watts>135</ns3:Watts>
    #       </ns3:TPX>
    #   </Extensions>
    need_speed = fields.Speed and point.speed is not None
    need_pwr = fields.Power and point.power is not None
    if need_speed or need_pwr:
        p_ext = etree.SubElement(result, with_ns("Extensions"))
        p_ext_tpx = etree.SubElement(p_ext, with_ns("TPX", "ns3"))
        if need_speed:
            p_ext_tpx_speed = etree.SubElement(p_ext_tpx, with_ns("Speed", "ns3"))
            p_ext_tpx_speed.text = str(point.speed)
        if need_pwr:
            p_ext_watts = etree.SubElement(p_ext_tpx, with_ns("Watts", "ns3"))
            p_ext_watts.text = str(point.power)

    return result

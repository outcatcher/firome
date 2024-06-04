from datetime import timezone

from lxml import etree
from lxml.etree import ElementBase

from .common import _with_ns, _time_format, _namespaces
from ...classes.export import ExportFields
from ...classes.points import DataPoint


def export_as_tcx(points: list[DataPoint], destination: str, fields=ExportFields()):
    start_ts = points[0].timestamp.strftime(_time_format)

    root_attrs = {
        etree.QName(
            "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"
        ): "http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2 "
        "http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd"
    }
    root: ElementBase = etree.Element(_with_ns("TrainingCenterDatabase"), root_attrs, nsmap=_namespaces)

    activities = etree.SubElement(root, _with_ns("Activities"))

    activity = etree.SubElement(activities, _with_ns("Activity"), {"Sport": "Biking"})

    activity_id = etree.SubElement(activity, _with_ns("Id"))
    activity_id.text = start_ts

    notes = etree.SubElement(activity, _with_ns("Notes"))
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

            lap_track = _new_lap(activity, start_ts)

        _append_point(p, lap_track, fields)

    root.getroottree().write(destination, encoding="utf-8", xml_declaration=True)


def _new_lap(activity: etree.ElementBase, start_ts: str) -> etree.ElementBase:
    lap = etree.SubElement(activity, _with_ns("Lap"), {"StartTime": start_ts})

    lap_trigger_method = etree.SubElement(lap, _with_ns("TriggerMethod"))
    lap_trigger_method.text = "Manual"

    lap_track = etree.SubElement(lap, _with_ns("Track"))

    return lap_track


def _append_point(point: DataPoint, base_element: etree.ElementBase, fields: ExportFields) -> etree.ElementBase:
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
    result = etree.SubElement(base_element, _with_ns("Trackpoint"))

    # <Time>2014-11-30T05:51:36Z</Time>
    p_time = etree.SubElement(result, _with_ns("Time"))
    p_time.text = point.timestamp.astimezone(timezone.utc).strftime(_time_format)

    #   <Position>
    #     <LatitudeDegrees>51.791013</LatitudeDegrees>
    #     <LongitudeDegrees>39.199698</LongitudeDegrees>
    #   </Position>

    if point.position is not None:
        p_position = etree.SubElement(result, _with_ns("Position"))
        p_pos_lat = etree.SubElement(p_position, _with_ns("LatitudeDegrees"))
        p_pos_lat.text = str(point.position[0])
        p_pos_lon = etree.SubElement(p_position, _with_ns("LongitudeDegrees"))
        p_pos_lon.text = str(point.position[1])

    #  <AltitudeMeters>152</AltitudeMeters>
    if fields.altitude and point.elevation is not None:
        p_alt = etree.SubElement(result, _with_ns("AltitudeMeters"))
        p_alt.text = str(point.elevation)

    # <DistanceMeters>14956.23</DistanceMeters>
    if fields.distance:
        p_distance = etree.SubElement(result, _with_ns("DistanceMeters"))
        p_distance.text = str(point.distance)

    #   <HeartRateBpm>
    #     <Value>168</Value>
    #   </HeartRateBpm>
    if fields.heart_rate and point.heart_rate is not None:
        p_hr = etree.SubElement(result, _with_ns("HeartRateBpm"))
        p_hr_val = etree.SubElement(p_hr, _with_ns("Value"))
        p_hr_val.text = str(point.heart_rate)

    # <Cadence>90</Cadence>
    if fields.cadence and point.cadence is not None:
        p_cadence = etree.SubElement(result, _with_ns("Cadence"))
        p_cadence.text = str(point.cadence)

    #   <Extensions>
    #       <ns3:TPX>
    #           <ns3:Speed>0</ns3:Speed>
    #           <ns3:Watts>135</ns3:Watts>
    #       </ns3:TPX>
    #   </Extensions>
    need_speed = fields.speed and point.speed is not None
    need_pwr = fields.power and point.power is not None
    if need_speed or need_pwr:
        p_ext = etree.SubElement(result, _with_ns("Extensions"))
        p_ext_tpx = etree.SubElement(p_ext, _with_ns("TPX", "ns3"))
        if need_speed:
            p_ext_tpx_speed = etree.SubElement(p_ext_tpx, _with_ns("Speed", "ns3"))
            p_ext_tpx_speed.text = str(point.speed)
        if need_pwr:
            p_ext_watts = etree.SubElement(p_ext_tpx, _with_ns("Watts", "ns3"))
            p_ext_watts.text = str(point.power)

    return result

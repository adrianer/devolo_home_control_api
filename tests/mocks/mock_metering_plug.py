import json
import pathlib

import requests

from devolo_home_control_api.devices.zwave import Zwave
from devolo_home_control_api.properties.binary_switch_property import BinarySwitchProperty
from devolo_home_control_api.properties.consumption_property import ConsumptionProperty
from devolo_home_control_api.properties.multi_level_sensor_property import MultiLevelSensorProperty
from devolo_home_control_api.properties.settings_property import SettingsProperty

from .mock_gateway import MockGateway


def metering_plug(device_uid: str) -> Zwave:
    """
    Represent a metering plug in tests

    :param device_uid: Device UID this mock shall have
    :return: Metering Plug device
    """
    file = pathlib.Path(__file__).parent / ".." / "test_data.json"
    with file.open("r") as fh:
        test_data = json.load(fh)

    device = Zwave(**test_data.get("devices").get("mains").get("properties"))
    gateway = MockGateway(test_data.get("gateway").get("id"))
    session = requests.Session()

    device.binary_switch_property = {}
    device.consumption_property = {}
    device.multi_level_sensor_property = {}
    device.settings_property = {}

    device.binary_switch_property[f'devolo.BinarySwitch:{device_uid}'] = \
        BinarySwitchProperty(gateway=gateway,
                             session=session,
                             element_uid=f"devolo.BinarySwitch:{device_uid}",
                             state=test_data.get("devices").get("mains").get("properties").get("state"))
    device.consumption_property[f'devolo.Meter:{device_uid}'] = ConsumptionProperty(gateway=gateway,
                                                                                    session=session,
                                                                                    element_uid=f"devolo.Meter:{device_uid}",
                                                                                    current=test_data.get("devices").get(
                                                                                        "mains").get("properties").get(
                                                                                        "current_consumption"),
                                                                                    total=test_data.get("devices").get(
                                                                                        "mains").get("properties").get(
                                                                                        "total_consumption"),
                                                                                    total_since=test_data.get("devices").get(
                                                                                        "mains").get("properties").get(
                                                                                        "sinceTime"))
    device.multi_level_sensor_property[f'devolo.VoltageMultiLevelSensor:{device_uid}'] = \
        MultiLevelSensorProperty(gateway=gateway,
                                 session=session,
                                 element_uid=f"devolo.VoltageMultiLevelSensor:{device_uid}",
                                 current=test_data.get("devices").get("mains").get("properties").get("voltage"))
    device.settings_property["param_changed"] = SettingsProperty(gateway=gateway,
                                                                 session=session,
                                                                 element_uid=f"cps.{device_uid}")
    device.settings_property["general_device_settings"] = SettingsProperty(gateway=gateway,
                                                                           session=session,
                                                                           element_uid=f"gds.{device_uid}",
                                                                           events_enabled=test_data.get("devices").get(
                                                                               "mains").get("properties").get(
                                                                               "events_enabled"),
                                                                           icon=test_data.get("devices").get(
                                                                               "mains").get("properties").get(
                                                                               "icon"),
                                                                           name=test_data.get("devices").get(
                                                                               "mains").get("properties").get(
                                                                               "itemName"),
                                                                           zone_id=test_data.get("devices").get(
                                                                               "mains").get("properties").get(
                                                                               "zoneId"))
    device.settings_property["led"] = SettingsProperty(gateway=gateway,
                                                       session=session,
                                                       element_uid=f"lis.{device_uid}",
                                                       led_setting=test_data.get("devices").get("mains").get(
                                                           "properties").get("led_setting"))
    device.settings_property["protection"] = SettingsProperty(gateway=gateway,
                                                              session=session,
                                                              element_uid=f"ps.{device_uid}",
                                                              local_switching=test_data.get("devices").get("mains").get(
                                                                  "properties").get("local_switch"),
                                                              remote_switching=test_data.get("devices").get("mains").get(
                                                                  "properties").get("remote_switch"))

    return device

import pytest

from devolo_home_control_api.devices.zwave import Zwave, get_device_type_from_element_uid, get_device_uid_from_element_uid
from devolo_home_control_api.properties.binary_switch_property import BinarySwitchProperty


class TestZwave:
    @pytest.mark.usefixtures("home_control_instance")
    @pytest.mark.usefixtures("mock_mprmrest__extract_data_from_element_uid")
    @pytest.mark.usefixtures("mock_mydevolo__call")
    def test_get_property(self):
        device = Zwave(name=self.devices.get("mains").get("name"),
                       device_uid=self.devices.get("mains").get("uid"),
                       zone=self.devices.get("mains").get("zone"),
                       battery_level=-1,
                       icon=self.devices.get("mains").get("icon"),
                       online_state=2)

        device.binary_switch_property = {}
        element_uid = f'devolo.BinarySwitch:{self.devices.get("mains").get("uid")}'
        device.binary_switch_property[element_uid] = BinarySwitchProperty(element_uid=element_uid)

        assert isinstance(device.get_property("binary_switch")[0], BinarySwitchProperty)

    def test_get_property_invalid(self):
        device = Zwave(name=self.devices.get("mains").get("name"),
                       device_uid=self.devices.get("mains").get("uid"),
                       zone=self.devices.get("mains").get("zone"),
                       battery_level=-1,
                       icon=self.devices.get("mains").get("icon"),
                       online_state=2)

        with pytest.raises(AttributeError):
            device.get_property("binary_switch")

    def test_battery_level(self):
        # TODO: Use battery driven device
        device = Zwave(name=self.devices.get("mains").get("name"),
                       device_uid=self.devices.get("mains").get("uid"),
                       zone=self.devices.get("mains").get("zone"),
                       battery_level=55,
                       icon=self.devices.get("mains").get("icon"),
                       online_state=2)

        assert device.battery_level == 55

    def test_device_online_state_state(self):
        device = Zwave(name=self.devices.get("mains").get("name"),
                       device_uid=self.devices.get("mains").get("uid"),
                       zone=self.devices.get("mains").get("zone"),
                       battery_level=-1,
                       icon=self.devices.get("mains").get("icon"),
                       online_state=1)
        assert device.online == "offline"

        device = Zwave(name=self.devices.get("mains").get("name"),
                       device_uid=self.devices.get("mains").get("uid"),
                       zone=self.devices.get("mains").get("zone"),
                       battery_level=-1,
                       icon=self.devices.get("mains").get("icon"),
                       online_state=2)
        assert device.online == "online"

        device = Zwave(name=self.devices.get("mains").get("name"),
                       device_uid=self.devices.get("mains").get("uid"),
                       zone=self.devices.get("mains").get("zone"),
                       battery_level=-1,
                       icon=self.devices.get("mains").get("icon"),
                       online_state=27)
        device.online = "unknown state"



    def test_get_device_type_from_element_uid(self):
        assert get_device_type_from_element_uid("devolo.Meter:hdm:ZWave:F6BF9812/2#2") == "devolo.Meter"

    def test_get_device_uid_from_element_uid(self):
        assert get_device_uid_from_element_uid("devolo.Meter:hdm:ZWave:F6BF9812/2#2") == "hdm:ZWave:F6BF9812/2"

import pytest

from devolo_home_control_api.backend.mprm_rest import MprmRest, get_sub_device_uid_from_element_uid


@pytest.mark.usefixtures("mprm_instance")
@pytest.mark.usefixtures("mock_mprmrest__extract_data_from_element_uid")
@pytest.mark.usefixtures("mock_mydevolo__call")
class TestMprmRest:

    def test_singleton(self):
        MprmRest.del_instance()

        with pytest.raises(SyntaxError):
            MprmRest.get_instance()

        first = MprmRest(gateway_id=self.gateway.get("id"), url="https://homecontrol.mydevolo.com")
        with pytest.raises(SyntaxError):
            MprmRest(gateway_id=self.gateway.get("id"), url="https://homecontrol.mydevolo.com")

        second = MprmRest.get_instance()
        assert first is second

    @pytest.mark.usefixtures("mock_mprmrest__post")
    def test_get_name_and_element_uids(self):
        properties = self.mprm.get_name_and_element_uids("test")
        assert properties == {"itemName": "test_name",
                              "zone": "test_zone",
                              "batteryLevel": "test_battery",
                              "icon": "test_icon",
                              "elementUIDs": "test_element_uids",
                              "settingUIDs": "test_setting_uids",
                              "deviceModelUID": "test_device_model_uid",
                              "status": "test_status"}

    def test_get_sub_device_uid_from_element_uid(self):
        assert get_sub_device_uid_from_element_uid("devolo.Meter:hdm:ZWave:F6BF9812/2#2") == 2
        assert get_sub_device_uid_from_element_uid("devolo.Meter:hdm:ZWave:F6BF9812/2") is None

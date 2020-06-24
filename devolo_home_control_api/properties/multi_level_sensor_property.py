from datetime import datetime
from typing import Any

from requests import Session

from ..devices.gateway import Gateway
from ..exceptions.device import WrongElementError
from .sensor_property import SensorProperty


class MultiLevelSensorProperty(SensorProperty):
    """
    Object for multi level sensors. It stores the multi level sensor state.

    :param gateway: Instance of a Gateway object
    :param session: Instance of a requests.Session object
    :param element_uid: Element UID, something like devolo.MultiLevelSensor:hdm:ZWave:CBC56091/24#MultilevelSensor(1)
    :key value: Multi level value
    :type value: float
    :key unit: Unit of that value
    :type unit: int
    """

    def __init__(self, gateway: Gateway, session: Session, element_uid: str, **kwargs: Any):
        if not element_uid.startswith(("devolo.DewpointSensor:",
                                       "devolo.Meter:",
                                       "devolo.MultiLevelSensor:",
                                       "devolo.SirenMultiLevelSensor:",
                                       "devolo.VoltageMultiLevelSensor:")):
            raise WrongElementError(f"{element_uid} is not a Multi Level Sensor.")

        self._unit = ""

        super().__init__(gateway=gateway, session=session, element_uid=element_uid, **kwargs)
        if element_uid.startswith("devolo.Meter:"):
            self.current = kwargs.get("current")
            self.current_unit = "W"
            self.total = kwargs.get("total")
            self.total_since = datetime.fromtimestamp(kwargs.get("total_since", 0) / 1000)
            self.total_unit = "kWh"
        else:
            self.value = kwargs.get("value")
            self.unit = kwargs.get("unit")


    @property
    def unit(self) -> str:
        """ Human readable unit of the property. """
        return self._unit

    @unit.setter
    def unit(self, unit: int):
        """ Make the numeric unit human readable, if known. """
        units = {"dewpoint": {0: "°C"},
                 "humidity": {0: "%"},
                 "light": {0: "%", 1: "lx"},
                 "temperature": {0: "°C"},
                 "Seismic Intensity": {0: ""},
                 "voltage": {0: "V"}
                 }
        if units.get(self.sensor_type) is not None:
            self._unit = units[self.sensor_type].get(unit, str(unit))
        else:
            self._unit = str(unit)
        self._logger.debug(f"Unit of {self.element_uid} set to '{self._unit}'.")

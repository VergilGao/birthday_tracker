from homeassistant.components.sensor import SensorDeviceClass, SensorEntity

from ..const import ATTR_LUNAR_BIRTH_DATE, ATTR_SOLAR_BIRTH_DATE
from .birthday_tracker import BirthdayTracker


class SolarBirthDateSensor(BirthdayTracker, SensorEntity):
    def __init__(self, entry, device_info):
        super().__init__(entry, ATTR_SOLAR_BIRTH_DATE, device_info)
        self._attr_state_class = None
        self._attr_device_class = SensorDeviceClass.DATE
        self._attr_icon = "mdi:calendar-star"

    @property
    def native_value(self):
        return self.coordinator.data.get(ATTR_SOLAR_BIRTH_DATE)


class LunarBirthDateSensor(BirthdayTracker, SensorEntity):
    def __init__(self, entry, device_info):
        super().__init__(entry, ATTR_LUNAR_BIRTH_DATE, device_info)
        self._attr_state_class = None
        self._attr_device_class = None
        self._attr_icon = "mdi:calendar-multiple"

    @property
    def native_value(self):
        lunar = self.coordinator.data.get(ATTR_LUNAR_BIRTH_DATE)
        return lunar.toString() if lunar else None

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity

from ..const import ATTR_NEXT_LUNAR_BIRTHDAY, ATTR_NEXT_SOLAR_BIRTHDAY
from .birthday_tracker import BirthdayTracker


class NextSolarBirthdaySensor(BirthdayTracker, SensorEntity):
    def __init__(self, entry, device_info):
        super().__init__(entry, ATTR_NEXT_SOLAR_BIRTHDAY, device_info)
        self._attr_device_class = SensorDeviceClass.DATE
        self._attr_icon = "mdi:calendar-arrow-right"

    @property
    def native_value(self):
        return self.coordinator.data.get(ATTR_NEXT_SOLAR_BIRTHDAY)


class NextLunarBirthdaySensor(BirthdayTracker, SensorEntity):
    def __init__(self, entry, device_info):
        super().__init__(entry, ATTR_NEXT_LUNAR_BIRTHDAY, device_info)
        self._attr_device_class = SensorDeviceClass.DATE
        self._attr_icon = "mdi:calendar-arrow-right"

    @property
    def native_value(self):
        return self.coordinator.data.get(ATTR_NEXT_LUNAR_BIRTHDAY)

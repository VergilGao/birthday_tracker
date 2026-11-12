from homeassistant.components.binary_sensor import BinarySensorEntity

from ..const import (
    ATTR_IS_TODAY_LUNAR_BIRTHDAY,
    ATTR_IS_TODAY_SOLAR_BIRTHDAY,
)
from .birthday_tracker import BirthdayTracker


class IsTodaySolarSensor(BirthdayTracker, BinarySensorEntity):
    def __init__(self, entry, device_info):
        super().__init__(entry, ATTR_IS_TODAY_SOLAR_BIRTHDAY, device_info)

    @property
    def is_on(self):
        return self.coordinator.data.get(ATTR_IS_TODAY_SOLAR_BIRTHDAY)

    @property
    def icon(self):
        return "mdi:cake" if self.is_on else "mdi:calendar-blank"


class IsTodayLunarSensor(BirthdayTracker, BinarySensorEntity):
    def __init__(self, entry, device_info):
        super().__init__(entry, ATTR_IS_TODAY_LUNAR_BIRTHDAY, device_info)

    @property
    def is_on(self):
        return self.coordinator.data.get(ATTR_IS_TODAY_LUNAR_BIRTHDAY)

    @property
    def icon(self):
        return "mdi:cake" if self.is_on else "mdi:calendar-blank"

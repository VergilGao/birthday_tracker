from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_ENABLE_LUNAR
from .entity import get_device_info
from .helpers import get_entry_config
from .sensors import (
    AgeSensor,
    DaysUntilLunarSensor,
    DaysUntilSolarSensor,
    LunarBirthDateSensor,
    NextLunarBirthdaySensor,
    NextSolarBirthdaySensor,
    SolarBirthDateSensor,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up all birthday sensors for a single config entry."""
    config = get_entry_config(entry)
    device_info = get_device_info(entry)

    sensors = [
        AgeSensor(entry, device_info),
        DaysUntilSolarSensor(entry, device_info),
        SolarBirthDateSensor(entry, device_info),
        NextSolarBirthdaySensor(entry, device_info),
    ]

    if config.get(CONF_ENABLE_LUNAR, True):
        sensors.extend(
            [
                DaysUntilLunarSensor(entry, device_info),
                LunarBirthDateSensor(entry, device_info),
                NextLunarBirthdaySensor(entry, device_info),
            ]
        )

    async_add_entities(sensors)

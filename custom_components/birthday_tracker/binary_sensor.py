from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_ENABLE_LUNAR
from .entity import get_device_info
from .helpers import get_entry_config
from .sensors import IsTodayLunarSensor, IsTodaySolarSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up birthday binary sensors for a config entry."""
    config = get_entry_config(entry)
    device_info = get_device_info(entry)
    sensors: list[BinarySensorEntity] = [
        IsTodaySolarSensor(entry, device_info),
    ]

    if config.get(CONF_ENABLE_LUNAR, True):
        sensors.append(IsTodayLunarSensor(entry, device_info))

    async_add_entities(sensors)

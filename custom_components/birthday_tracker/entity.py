from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from .const import CONF_NAME, DOMAIN
from .helpers import get_entry_config


def get_device_info(entry: ConfigEntry) -> DeviceInfo:
    """Build device information from the effective entry configuration."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=get_entry_config(entry)[CONF_NAME],
        manufacturer="VergilGao",
        model="Birthday Tracker",
    )

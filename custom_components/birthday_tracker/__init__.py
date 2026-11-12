import logging
from uuid import uuid4

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_IS_TODAY_LUNAR_BIRTHDAY,
    ATTR_IS_TODAY_SOLAR_BIRTHDAY,
    CONF_ID,
    CONF_NAME,
    CONFIG_ENTRY_VERSION,
)
from .coordinator import BirthdayCoordinator
from .helpers import get_entry_config, validate_entry_config

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate legacy entries whose ignored options now take effect."""
    if entry.version > CONFIG_ENTRY_VERSION:
        return False

    if entry.version == 1:
        registry = er.async_get(hass)
        legacy_unique_ids = {
            f"{entry.entry_id}_{ATTR_IS_TODAY_SOLAR_BIRTHDAY}",
            f"{entry.entry_id}_{ATTR_IS_TODAY_LUNAR_BIRTHDAY}",
        }
        for entity_entry in er.async_entries_for_config_entry(registry, entry.entry_id):
            if (
                entity_entry.domain == Platform.SENSOR
                and entity_entry.unique_id in legacy_unique_ids
            ):
                registry.async_remove(entity_entry.entity_id)

        data = dict(entry.data)
        data.setdefault(CONF_ID, uuid4().hex)
        options = dict(entry.options)
        title = entry.title
        if options:
            try:
                validated_options = validate_entry_config(
                    get_entry_config(entry),
                    dt_util.now().date(),
                )
            except KeyError, TypeError, ValueError:
                _LOGGER.warning(
                    "Discarding invalid legacy options for %s", entry.entry_id
                )
                options = {}
            else:
                options = validated_options
                title = validated_options[CONF_NAME]

        hass.config_entries.async_update_entry(
            entry,
            data=data,
            options=options,
            title=title,
            unique_id=entry.unique_id or data[CONF_ID],
            version=CONFIG_ENTRY_VERSION,
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Birthday Tracker from a config entry."""
    try:
        config = validate_entry_config(
            get_entry_config(entry),
            dt_util.now().date(),
        )
    except (KeyError, TypeError, ValueError) as err:
        raise ConfigEntryError(
            f"Invalid birthday_tracker configuration for {entry.entry_id}"
        ) from err

    coordinator = BirthdayCoordinator(config)
    entry.runtime_data = coordinator

    async def midnight_refresh(_now) -> None:
        """Refresh the entry when Home Assistant enters a new local day."""
        coordinator.refresh()

    entry.async_on_unload(
        async_track_time_change(
            hass,
            midnight_refresh,
            hour=0,
            minute=0,
            second=0,
        )
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        entry.runtime_data = None
    return unload_ok

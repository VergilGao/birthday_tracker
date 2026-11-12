from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ..coordinator import BirthdayCoordinator


class BirthdayTracker:
    """Base class for all birthday-related sensors."""

    def __init__(self, entry: ConfigEntry, field: str, device_info: DeviceInfo):
        self._entry = entry
        self._field = field
        self._attr_should_poll = False
        self._attr_unique_id = f"{entry.entry_id}_{field}"
        self._attr_has_entity_name = True
        self._attr_translation_key = field
        self._attr_device_info = device_info
        self.coordinator: BirthdayCoordinator = entry.runtime_data

    async def async_added_to_hass(self):
        """Subscribe the entity to its config entry coordinator."""
        await super().async_added_to_hass()
        self.async_on_remove(self.coordinator.add_listener(self.async_write_ha_state))

    @property
    def available(self):
        return self.coordinator.data is not None

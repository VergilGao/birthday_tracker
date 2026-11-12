from __future__ import annotations

from typing import Any, override
from uuid import uuid4

import probatio
from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers import selector
from homeassistant.util import dt as dt_util

from .const import (
    CONF_BIRTH_DATE,
    CONF_ENABLE_LUNAR,
    CONF_ID,
    CONF_NAME,
    CONFIG_ENTRY_VERSION,
    DEFAULT_ENABLE_LUNAR,
    DOMAIN,
)
from .helpers import (
    get_entry_config,
    normalize_name,
    parse_birth_date,
    validate_entry_config,
)


def _build_schema() -> probatio.Schema:
    """Build the shared birthday configuration form."""
    return probatio.Schema(
        {
            probatio.Required(CONF_NAME): selector.TextSelector(),
            probatio.Required(CONF_BIRTH_DATE): selector.DateSelector(),
            probatio.Required(CONF_ENABLE_LUNAR): selector.BooleanSelector(),
        }
    )


def _validate_user_input(
    user_input: dict[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, str]]:
    """Validate form input and map parser errors to translation keys."""
    try:
        return validate_entry_config(user_input, dt_util.now().date()), {}
    except KeyError:
        return None, {CONF_BIRTH_DATE: "invalid_date"}
    except (TypeError, ValueError) as err:
        if str(err) == "name_required":
            return None, {CONF_NAME: "name_required"}
        if str(err) == "birth_date_in_future":
            return None, {CONF_BIRTH_DATE: "birth_date_in_future"}
        if str(err) == "invalid_boolean":
            return None, {"base": "invalid_input"}
        return None, {CONF_BIRTH_DATE: "invalid_date"}


def _values_match(
    config: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    """Compare normalized values used to identify a tracked person."""
    try:
        return normalize_name(str(config[CONF_NAME])).casefold() == normalize_name(
            str(candidate[CONF_NAME])
        ).casefold() and parse_birth_date(config[CONF_BIRTH_DATE]) == parse_birth_date(
            candidate[CONF_BIRTH_DATE]
        )
    except KeyError, TypeError, ValueError:
        return False


class BirthdayTrackerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Birthday Tracker config flows."""

    VERSION = CONFIG_ENTRY_VERSION

    @override
    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Add a birthday tracker entry."""
        errors: dict[str, str] = {}

        if user_input is not None:
            config, errors = _validate_user_input(user_input)
            if config is not None:
                entry_data = {**config, CONF_ID: uuid4().hex}
                await self.async_set_unique_id(entry_data[CONF_ID])
                self._abort_if_unique_id_configured()

                for entry in self.hass.config_entries.async_entries(DOMAIN):
                    if _values_match(get_entry_config(entry), config):
                        return self.async_abort(reason="already_configured")

                return self.async_create_entry(
                    title=config[CONF_NAME],
                    data=entry_data,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                _build_schema(),
                user_input or {CONF_ENABLE_LUNAR: DEFAULT_ENABLE_LUNAR},
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return BirthdayTrackerOptionsFlowHandler()


class BirthdayTrackerOptionsFlowHandler(config_entries.OptionsFlowWithReload):
    """Edit a birthday tracker entry."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Edit name, solar birth date and lunar support."""
        errors: dict[str, str] = {}
        existing = get_entry_config(self.config_entry)

        if user_input is not None:
            config, errors = _validate_user_input(user_input)
            if config is not None:
                for entry in self.hass.config_entries.async_entries(DOMAIN):
                    if entry.entry_id == self.config_entry.entry_id:
                        continue
                    if _values_match(get_entry_config(entry), config):
                        errors["base"] = "already_configured"
                        break

            if not errors and config is not None:
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    title=config[CONF_NAME],
                )
                return self.async_create_entry(title="", data=config)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                _build_schema(),
                user_input or existing,
            ),
            errors=errors,
        )

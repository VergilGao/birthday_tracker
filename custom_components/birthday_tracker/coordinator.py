from collections.abc import Callable
from datetime import date
from typing import Any

from homeassistant.util import dt as dt_util

from .const import (
    ATTR_AGE,
    ATTR_DAYS_UNTIL_LUNAR,
    ATTR_DAYS_UNTIL_SOLAR,
    ATTR_IS_TODAY_LUNAR_BIRTHDAY,
    ATTR_IS_TODAY_SOLAR_BIRTHDAY,
    ATTR_LUNAR_BIRTH_DATE,
    ATTR_NEXT_LUNAR_BIRTHDAY,
    ATTR_NEXT_SOLAR_BIRTHDAY,
    ATTR_SOLAR_BIRTH_DATE,
    CONF_BIRTH_DATE,
    CONF_ENABLE_LUNAR,
    CONF_NAME,
)
from .helpers import (
    calculate_age,
    get_days_until,
    get_lunar_birth_date,
    get_next_lunar_birthday,
    get_next_solar_birthday,
    is_today_birthday,
    parse_birth_date,
)


class BirthdayCoordinator:
    """Calculate and publish birthday data for one config entry."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config
        self._listeners: set[Callable[[], None]] = set()
        self._data: dict[str, Any] = {}
        self.refresh()

    @property
    def data(self) -> dict[str, Any]:
        """Return the latest calculated values."""
        return self._data

    def refresh(self, today: date | None = None) -> None:
        """Recalculate all values and notify subscribed entities."""
        today = today or dt_util.now().date()
        self._data = self._calculate_all_fields(
            self._config[CONF_NAME],
            parse_birth_date(self._config[CONF_BIRTH_DATE]),
            today,
            self._config.get(CONF_ENABLE_LUNAR, True),
        )
        for listener in tuple(self._listeners):
            listener()

    def add_listener(self, listener: Callable[[], None]) -> Callable[[], None]:
        """Subscribe an entity to coordinator updates."""
        self._listeners.add(listener)

        def remove_listener() -> None:
            self._listeners.discard(listener)

        return remove_listener

    def _calculate_all_fields(
        self, name: str, birth_date: date, today: date, enable_lunar: bool
    ) -> dict:
        """Compute all birthday-related fields."""
        next_solar = get_next_solar_birthday(birth_date, today)

        result = {
            CONF_NAME: name,
            ATTR_SOLAR_BIRTH_DATE: birth_date,
            ATTR_NEXT_SOLAR_BIRTHDAY: next_solar,
            ATTR_DAYS_UNTIL_SOLAR: get_days_until(next_solar, today),
            ATTR_AGE: calculate_age(birth_date, today),
            ATTR_IS_TODAY_SOLAR_BIRTHDAY: is_today_birthday(birth_date, today),
        }

        if enable_lunar:
            lunar_birth = get_lunar_birth_date(birth_date)
            next_lunar = get_next_lunar_birthday(lunar_birth, today)
            result.update(
                {
                    ATTR_LUNAR_BIRTH_DATE: lunar_birth,
                    ATTR_NEXT_LUNAR_BIRTHDAY: next_lunar,
                    ATTR_DAYS_UNTIL_LUNAR: get_days_until(next_lunar, today),
                    ATTR_IS_TODAY_LUNAR_BIRTHDAY: is_today_birthday(next_lunar, today),
                }
            )

        return result

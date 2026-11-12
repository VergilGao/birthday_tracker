from typing import Final

DOMAIN: Final[str] = "birthday_tracker"

CONF_NAME: Final[str] = "name"
CONF_BIRTH_DATE: Final[str] = "birth_date"
CONF_ENABLE_LUNAR: Final[str] = "enable_lunar"
CONF_ID: Final[str] = "person_id"

ATTR_AGE: Final[str] = "age"
ATTR_NEXT_SOLAR_BIRTHDAY: Final[str] = "next_solar_birthday"
ATTR_NEXT_LUNAR_BIRTHDAY: Final[str] = "next_lunar_birthday"
ATTR_DAYS_UNTIL_SOLAR: Final[str] = "days_until_solar_birthday"
ATTR_DAYS_UNTIL_LUNAR: Final[str] = "days_until_lunar_birthday"
ATTR_IS_TODAY_SOLAR_BIRTHDAY: Final[str] = "is_today_solar_birthday"
ATTR_IS_TODAY_LUNAR_BIRTHDAY: Final[str] = "is_today_lunar_birthday"
ATTR_SOLAR_BIRTH_DATE: Final[str] = "solar_birth_date"
ATTR_LUNAR_BIRTH_DATE: Final[str] = "lunar_birth_date"

DEFAULT_ENABLE_LUNAR: Final[bool] = True
CONFIG_ENTRY_VERSION: Final[int] = 2

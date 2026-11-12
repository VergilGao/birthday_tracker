from datetime import date, datetime, time
from typing import Any

from homeassistant.config_entries import ConfigEntry
from lunar_python import Lunar, LunarYear

from .const import CONF_BIRTH_DATE, CONF_ENABLE_LUNAR, CONF_NAME, DEFAULT_ENABLE_LUNAR


def normalize_name(name: str) -> str:
    """Normalize a person's name for storage and duplicate detection."""
    return " ".join(name.split())


def parse_birth_date(birth_date_value: str | date | datetime) -> date:
    """Parse a stored solar birth date."""
    if isinstance(birth_date_value, datetime):
        return birth_date_value.date()
    if isinstance(birth_date_value, date):
        return birth_date_value
    return datetime.strptime(birth_date_value, "%Y-%m-%d").date()


def get_entry_config(entry: ConfigEntry) -> dict[str, Any]:
    """Return the effective configuration, with options overriding initial data."""
    return {**entry.data, **entry.options}


def birthday_in_year(birth_date: date, year: int) -> date:
    """Return a birthday in the requested year, using Feb 28 for non-leap years."""
    try:
        return birth_date.replace(year=year)
    except ValueError:
        if birth_date.month == 2 and birth_date.day == 29:
            return date(year, 2, 28)
        raise


def calculate_age(birth_date: date, today: date) -> int:
    return (
        today.year
        - birth_date.year
        - (today < birthday_in_year(birth_date, today.year))
    )


def get_next_solar_birthday(birth_date: date, today: date) -> date:
    this_year_birthday = birthday_in_year(birth_date, today.year)
    if this_year_birthday < today:
        return birthday_in_year(birth_date, today.year + 1)
    return this_year_birthday


def get_days_until(target_date: date, today: date) -> int:
    return (target_date - today).days


def get_lunar_birth_date(solar_birth_date: date) -> Lunar:
    return Lunar.fromDate(datetime.combine(solar_birth_date, time()))


def get_lunar_birthday_in_year(lunar_birth: Lunar, lunar_year: int) -> Lunar:
    """Return the annual lunar birthday, handling leap and short months."""
    lunar_month = LunarYear.fromYear(lunar_year).getMonth(lunar_birth.getMonth())
    if lunar_month is None and lunar_birth.getMonth() < 0:
        lunar_month = LunarYear.fromYear(lunar_year).getMonth(
            abs(lunar_birth.getMonth())
        )
    if lunar_month is None:
        raise ValueError("invalid_lunar_birthday")

    return Lunar(
        lunar_year,
        lunar_month.getMonth(),
        min(lunar_birth.getDay(), lunar_month.getDayCount()),
        0,
        0,
        0,
    )


def get_next_lunar_birthday(lunar_birth: Lunar, today: date) -> date:
    lunar_year = Lunar.fromDate(datetime.combine(today, time())).getYear()
    lunar_this_year = get_lunar_birthday_in_year(lunar_birth, lunar_year)
    solar_this_year = lunar_this_year.getSolar()
    solar_date = date(
        solar_this_year.getYear(), solar_this_year.getMonth(), solar_this_year.getDay()
    )
    if solar_date < today:
        lunar_next_year = get_lunar_birthday_in_year(lunar_birth, lunar_year + 1)
        solar_next_year = lunar_next_year.getSolar()
        return date(
            solar_next_year.getYear(),
            solar_next_year.getMonth(),
            solar_next_year.getDay(),
        )
    return solar_date


def is_today_birthday(birthday: date, today: date) -> bool:
    return birthday.month == today.month and birthday.day == today.day


def validate_entry_config(config: dict[str, Any], today: date) -> dict[str, Any]:
    """Validate and normalize values stored in a config entry."""
    name_value = config.get(CONF_NAME)
    if not isinstance(name_value, str):
        raise TypeError("name_required")
    name = normalize_name(name_value)
    if not name:
        raise ValueError("name_required")

    birth_date = parse_birth_date(config[CONF_BIRTH_DATE])
    if birth_date > today:
        raise ValueError("birth_date_in_future")

    enable_lunar = config.get(CONF_ENABLE_LUNAR, DEFAULT_ENABLE_LUNAR)
    if not isinstance(enable_lunar, bool):
        raise TypeError("invalid_boolean")

    return {
        CONF_NAME: name,
        CONF_BIRTH_DATE: birth_date.isoformat(),
        CONF_ENABLE_LUNAR: enable_lunar,
    }

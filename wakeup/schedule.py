import wakeup.util as util
from wakeup.errors import InvalidScheduleError


class Schedule:
    """Immutable type"""

    def __init__(self, hours=0, minutes=0, days_of_week=None):
        if not days_of_week:
            days_of_week = get_all_weekdays()

        self.days_of_week = days_of_week
        self.hours = hours
        self.minutes = minutes

    def __eq__(self, other):
        if not isinstance(other, Schedule):
            return False

        return (
            self.hours == other.hours
            and self.minutes == other.minutes
            and self.days_of_week == other.days_of_week
        )

    def __repr__(self):
        return f"<{self.hours:02}:{self.minutes:02} on {self.days_of_week}>"


def parse_schedule(s: str) -> Schedule:
    time_str, days_str = _separate_time_and_days(s)
    hours, minutes = _parse_time(time_str)
    days = _parse_days(days_str)
    return Schedule(hours, minutes, days)


def _parse_days(days_str):
    days = _parse_days_with_default(days_str, get_all_weekdays())
    _ensure_days_are_valid(days)
    return days


def _separate_time_and_days(user_input):
    time_and_days = user_input.split(" ")

    time = time_and_days[0]

    if len(time_and_days) == 2:
        days = time_and_days[1]
    else:
        days = ""

    return time, days


def _parse_time(time):
    try:
        hours, minutes = _try_parse_time(time)
        _ensure_hours_in_range(hours)
        _ensure_minutes_in_range(minutes)
        return hours, minutes
    except ValueError:
        raise InvalidScheduleError("Invalid time format")


def _try_parse_time(time):
    hours_str, minutes_and_period = time.split(":")
    minutes_str, period = util.split_at(minutes_and_period, 2)

    hours = int(hours_str)
    if period.lower() == "pm":
        hours += 12

    minutes = int(minutes_str)

    return hours, minutes


def _ensure_hours_in_range(hours):
    if not (0 <= hours < 24):
        raise InvalidScheduleError(f"Hours out of range [0,23]: {hours}")


def _ensure_minutes_in_range(minutes):
    if not (0 <= minutes < 60):
        raise InvalidScheduleError(f"Minutes out of range [0,59]: {minutes}")


def _parse_days_with_default(days_input, default):
    if not days_input:
        return default
    days = set(days_input.split(","))
    return days


def _ensure_days_are_valid(days):
    valid_days = get_all_weekdays()
    for day in days:
        if day not in valid_days:
            raise InvalidScheduleError(f"Invalid day: {day}")


def get_all_weekdays():
    return {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}


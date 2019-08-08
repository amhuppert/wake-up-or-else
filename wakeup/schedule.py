import wakeup.util as util


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
    days = _parse_days_with_default(days_str, get_all_weekdays())
    return Schedule(hours, minutes, days)


def _separate_time_and_days(user_input):
    time_and_days = user_input.split(" ")

    time = time_and_days[0]

    if len(time_and_days) == 2:
        days = time_and_days[1]
    else:
        days = ""

    return time, days


def _parse_time(time):
    hours_str, minutes_and_period = time.split(":")
    minutes_str, period = util.split_at(minutes_and_period, 2)

    hours = int(hours_str)
    if period.lower() == "pm":
        hours += 12

    minutes = int(minutes_str)

    return hours, minutes


def _parse_days_with_default(days, default):
    if not days:
        return default
    return set(days.split(","))


def get_all_weekdays():
    return {"mon", "tues", "wed", "thurs", "fri", "sat", "sun"}


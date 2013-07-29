"""Useful things to do with dates"""
import datetime


def date_from_string(string, format_string=None):
    """Runs through a few common string formats for datetimes,
    and attempts to coerce them into a datetime. Alternatively,
    format_string can provide either a single string to attempt
    or an iterable of strings to attempt."""

    if isinstance(format_string, str):
        return datetime.datetime.strptime(string, format_string).date()

    elif format_string is None:
        format_string = [
            "%Y-%m-%d",
            "%m-%d-%Y",
            "%m/%d/%Y",
            "%d/%m/%Y",
        ]

    for format in format_string:
        try:
            return datetime.datetime.strptime(string, format).date()
        except ValueError:
            continue

    raise ValueError("Could not produce date from string: {}".format(string))


def to_datetime(plain_date, hours=0, minutes=0, seconds=0, ms=0):
    """given a datetime.date, gives back a datetime.datetime"""
    # don't mess with datetimes
    if isinstance(plain_date, datetime.datetime):
        return plain_date
    return datetime.datetime(
        plain_date.year,
        plain_date.month,
        plain_date.day,
        hours,
        minutes,
        seconds,
        ms,
    )


class TimePeriod(object):

    def __init__(self, earliest, latest):
        if not isinstance(earliest, datetime.date) and earliest is not None:
            raise TypeError("Earliest must be a date or None")
        if not isinstance(latest, datetime.date) and latest is not None:
            raise TypeError("Latest must be a date or None")

        # convert dates to datetimes, for to have better resolution
        if earliest is not None:
            earliest = to_datetime(earliest)
        if latest is not None:
            latest = to_datetime(latest, 23, 59, 59)

        if earliest is not None and latest is not None and earliest >= latest:
            raise ValueError("Earliest must be earlier than latest")

        self._earliest = earliest
        self._latest = latest

    def __contains__(self, key):
        if isinstance(key, datetime.date):
            key = to_datetime(key)

            if self._latest is None:
                upper_bounded = True
            else:
                upper_bounded = key <= self._latest

            if self._earliest is None:
                lower_bounded = True
            else:
                lower_bounded = self._earliest <= key

            return upper_bounded and lower_bounded

    def __eq__(self, other):
        return (self._earliest == other._earliest) and (self._latest == other._latest)

    def __repr__(self):
        return "<{}: {}-{}>".format(
            self.__class__.__name__,
            self._earliest,
            self._latest,
        )


def days_ago(days, give_datetime=True):
    delta = datetime.timedelta(days=days)
    dt = datetime.datetime.now() - delta
    if give_datetime:
        return dt
    else:
        return dt.date()


def days_ahead(days, give_datetime=True):
    delta = datetime.timedelta(days=days)
    dt = datetime.datetime.now() + delta
    if give_datetime:
        return dt
    else:
        return dt.date()

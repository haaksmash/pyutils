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
        ]

    for format in format_string:
        try:
            return datetime.datetime.strptime(string, format).date()
        except ValueError:
            continue

    raise ValueError("Could not produce date from string: {}".format(string))


class TimePeriod(object):

    def __init__(self, earliest, latest):
        if not isinstance(earliest, datetime.date) and earliest is not None:
            raise TypeError("Earliest must be a date or None")
        if not isinstance(latest, datetime.date) and latest is not None:
            raise TypeError("Latest must be a date or None")

        self._earliest = earliest
        self._latest = latest

    def __contains__(self, key):
        if not isinstance(key, datetime.date):
            raise TypeError("{} is not a date".format(key))

        if self._earliest <= key <= self._latest:
            return True

        return False


def days_ago(days, datetime=True):
    delta = datetime.timedelta(days=days)
    dt = datetime.datetime.now() - delta
    if datetime:
        return dt
    else:
        return dt.date()


def days_ahead(days, datetime=True):
    delta = datetime.timedelta(days=days)
    dt = datetime.datetime.now() - delta
    if datetime:
        return dt
    else:
        return dt.date()

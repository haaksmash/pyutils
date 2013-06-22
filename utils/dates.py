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

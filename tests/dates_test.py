from datetime import date, datetime, timedelta

import testify as T

from utils import dates


class DateFromStringTestCase(T.TestCase):

    def test_format_string_parsing(self):
        expected_date = date(2013, 5, 10)

        STRING_FORMAT_PAIRS = (
            ("2013-5-10", "%Y-%m-%d"),
            ("2013-05-10", "%Y-%m-%d"),
            ("5-10-2013", "%m-%d-%Y"),
            ("5/10/2013", "%m/%d/%Y"),
        )

        for string, format_string in STRING_FORMAT_PAIRS:
            produced_date = dates.date_from_string(string, format_string)
            T.assert_equal(produced_date, expected_date)

        BAD_FORMAT_PAIRS = (
            ("2013-5-10", "%m/%d/%Y"),
        )

        for string, format_string in BAD_FORMAT_PAIRS:
            with T.assert_raises(ValueError):
                dates.date_from_string(string, format_string)

    def test_default_formats(self):
        expected_date = date(2013, 5, 10)

        ENABLED_DEFAULTS = (
            "2013-5-10",
            "2013-05-10",
            "5-10-2013",
            "5/10/2013",
        )

        for string in ENABLED_DEFAULTS:
            produced_date = dates.date_from_string(string)
            T.assert_equal(produced_date, expected_date)


class ToDatetimeTestCase(T.TestCase):

    def test_conversion(self):
        provided_date = date(2013, 5, 10)
        expected_datetime = datetime(2013, 5, 10)

        produced_datetime = dates.to_datetime(provided_date)

        T.assert_equal(produced_datetime, expected_datetime)

    def test_given_datetime(self):
        provided_datetime = datetime(2013, 5, 10)
        produced_datetime = dates.to_datetime(provided_datetime)

        T.assert_equal(produced_datetime, provided_datetime)


class TimePeriodTestCase(T.TestCase):

    def test_initialization(self):
        # test all valid earliest and latest combos
        GOOD_EARLIEST_LATEST = (
            (None, None),
            (date(2013, 5, 10), None),
            (datetime(2013, 5, 10), None),
            (None, date(2013, 5, 10)),
            (None, datetime(2013, 5, 10)),
            (date(2013, 5, 10), date(2013, 5, 11)),
            (datetime(2013, 5, 10), datetime(2013, 5, 11)),
            (datetime(2013, 5, 10), date(2013, 5, 11)),
            (date(2013, 5, 10), datetime(2013, 5, 11)),
            (date(2013, 5, 10), date(2013, 5, 10)),
        )

        for earliest, latest in GOOD_EARLIEST_LATEST:
            dates.TimePeriod(earliest, latest)

        BAD_EARLIEST_LATEST = (
            (date(2013, 5, 11), date(2013, 5, 10)),
        )

        for earliest, latest in BAD_EARLIEST_LATEST:
            with T.assert_raises(ValueError):
                dates.TimePeriod(earliest, latest)

    def test_contains(self):
        contains_all = dates.TimePeriod(None, None)
        contains_past = dates.TimePeriod(None, date.today() - timedelta(days=1))
        contains_future = dates.TimePeriod(date.today() + timedelta(days=1), None)
        contains_month = dates.TimePeriod(
            date(2013, date.today().month, 1),
            date(2013, date.today().month + 1, 1) - timedelta(days=1),
        )

        T.assert_in(datetime.min, contains_all)
        T.assert_in(datetime.min, contains_past)
        T.assert_not_in(datetime.min, contains_future)
        T.assert_not_in(datetime.min, contains_month)

        T.assert_in(datetime.max, contains_all)
        T.assert_in(datetime.max, contains_future)
        T.assert_not_in(datetime.max, contains_past)
        T.assert_not_in(datetime.max, contains_month)

        T.assert_in(date.today(), contains_all)
        T.assert_in(date.today(), contains_month)
        T.assert_not_in(date.today(), contains_past)
        T.assert_not_in(date.today(), contains_future)

    def test_eq(self):
        T.assert_equal(dates.TimePeriod(None, None), dates.TimePeriod(None, None))
        T.assert_equal(dates.TimePeriod(date.today(), None), dates.TimePeriod(date.today(), None))

        T.assert_not_equal(dates.TimePeriod(None, None), dates.TimePeriod(date.today(), None))


class DaysAgoTestCase(T.TestCase):
    def test(self):
        DAYS = 15
        expected_result = datetime.now() - timedelta(days=DAYS)
        T.assert_equal(dates.days_ago(DAYS, False), expected_result.date())


class DaysAheadTestCase(T.TestCase):
    def test(self):
        DAYS = 15
        expected_result = datetime.now() + timedelta(days=DAYS)
        T.assert_equal(dates.days_ahead(DAYS, False), expected_result.date())


if __name__ == "__main__":
    T.run()

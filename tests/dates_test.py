from datetime import date, datetime, timedelta

import mock
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
        expected_date = date(2013, 5, 15)

        ENABLED_DEFAULTS = (
            "2013-5-15",
            "2013-05-15",
            "5-15-2013",
            "5/15/2013",
            "15/5/2013",
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

    def test_eq(self):
        T.assert_equal(dates.TimePeriod(None, None), dates.TimePeriod(None, None))
        T.assert_equal(dates.TimePeriod(date.today(), None), dates.TimePeriod(date.today(), None))

        T.assert_not_equal(dates.TimePeriod(None, None), dates.TimePeriod(date.today(), None))

    def test_get_containing_period_no_none(self):
        periods = [
            mock.Mock(
                dates.TimePeriod,
                instance=True,
                _latest=datetime(2013, 5, 10),
                _earliest=datetime(2013, 5, 5),
            ),
            mock.Mock(
                dates.TimePeriod,
                instance=True,
                _latest=datetime(2013, 5, 11),
                _earliest=datetime(2013, 5, 7),
            ),
        ]

        with mock.patch("utils.dates.TimePeriod.__init__") as init_patch:
            # need to do this, otherwise get a TypeError
            init_patch.return_value = None

            dates.TimePeriod.get_containing_period(*periods)
            init_patch.assert_called_once_with(datetime(2013, 5, 5), datetime(2013, 5, 11))

    def test_get_containing_period_nones(self):
        periods = [
            mock.Mock(
                dates.TimePeriod,
                instance=True,
                _latest=None,
                _earliest=datetime(2013, 5, 5),
            ),
            mock.Mock(
                dates.TimePeriod,
                instance=True,
                _latest=datetime(2013, 5, 11),
                _earliest=None,
            ),
        ]

        with mock.patch("utils.dates.TimePeriod.__init__") as init_patch:
            # need to do this, otherwise get a TypeError
            init_patch.return_value = None

            dates.TimePeriod.get_containing_period(*periods)
            init_patch.assert_called_once_with(None, None)


    def test_overlaps_no_overlap(self):
        tp1 = dates.TimePeriod(
            date(2013, 5, 11),
            date(2013, 5, 15),
        )
        tp2 = dates.TimePeriod(
            date(2013, 5, 16),
            date(2013, 5, 21)
        )

        T.assert_equal(tp1.overlaps(tp2), False)
        T.assert_equal(tp2.overlaps(tp1), False)

    def test_overlaps_overlap(self):
        tp1 = dates.TimePeriod(
            date(2013, 5, 11),
            date(2013, 5, 17),
        )
        tp2 = dates.TimePeriod(
            date(2013, 5, 16),
            date(2013, 5, 21)
        )

        T.assert_equal(tp1.overlaps(tp2), True)
        T.assert_equal(tp2.overlaps(tp1), True)


class TimePeriodContainsTestCase(T.TestCase):

    @T.setup
    def create_periods(self):
        self.contains_all = dates.TimePeriod(None, None)
        self.contains_past = dates.TimePeriod(None, date.today() - timedelta(days=1))
        self.contains_future = dates.TimePeriod(date.today() + timedelta(days=1), None)
        self.contains_month = dates.TimePeriod(
            date(2013, date.today().month, 1),
            date(2013, date.today().month + 1, 1) - timedelta(days=1),
        )

    def test_verbose_function(self):
        with mock.patch("utils.dates.TimePeriod.__contains__") as cpatch:
            dates.TimePeriod(None, None).contains(mock.sentinel.CONTAIN)

            cpatch.assert_called_once_with(mock.sentinel.CONTAIN)

    def test_all_contains_datetime(self):
        T.assert_in(datetime.min, self.contains_all)
        T.assert_in(datetime.max, self.contains_all)
        T.assert_in(date.today(), self.contains_all)

    def test_past_contains_datetime(self):
        T.assert_in(datetime.min, self.contains_past)
        T.assert_not_in(datetime.max, self.contains_past)
        T.assert_not_in(date.today(), self.contains_past)

    def test_future_contains_datetime(self):
        T.assert_not_in(datetime.min, self.contains_future)
        T.assert_in(datetime.max, self.contains_future)
        T.assert_not_in(date.today(), self.contains_future)

    def test_month_contains_datetime(self):
        T.assert_not_in(datetime.min, self.contains_month)
        T.assert_not_in(datetime.max, self.contains_month)
        T.assert_in(date.today(), self.contains_month)

    def test_contains_timeperiod(self):
        T.assert_in(self.contains_past, self.contains_all)
        T.assert_in(self.contains_month, self.contains_all)
        T.assert_in(self.contains_month, self.contains_month)
        T.assert_not_in(self.contains_all, self.contains_month)


class DiscontinuousTimePeriodTestCase(T.TestCase):

    def test_initialization_all_noncontinous(self):
        periods = [
            dates.TimePeriod(date(2013, 5, 10), date(2013, 5, 15)),
            dates.TimePeriod(date(2013, 5, 20), date(2013, 5, 25)),
            dates.TimePeriod(date(2013, 5, 26), date(2013, 5, 26)),
        ]
        dtp = dates.DiscontinuousTimePeriod(
            *periods
        )

        T.assert_equal(set(dtp._periods), set(periods))

    def test_initialization_not_some_contained(self):
        periods = [
            dates.TimePeriod(date(2013, 5, 10), date(2013, 5, 15)),
            dates.TimePeriod(date(2013, 5, 8), date(2013, 5, 16)),
        ]

        dtp = dates.DiscontinuousTimePeriod(
            *periods
        )

        T.assert_equal(dtp._periods, [periods[1]])

    def test_initialization_overlaps(self):
        periods = [
            dates.TimePeriod(date(2013, 5, 8), date(2013, 5, 15)),
            dates.TimePeriod(date(2013, 5, 10), date(2013, 5, 16)),
        ]

        dtp = dates.DiscontinuousTimePeriod(
            *periods
        )

        T.assert_equal(dtp._periods, [dates.TimePeriod(date(2013, 5, 8), date(2013, 5, 16))])


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

import mock
import testify as T

from utils.dicts import helpers


class FromKeyedIterableTestCase(T.TestCase):
    def test_basic(self):
        iterable = [
            mock.Mock(key=12),
            mock.Mock(key=12),
            mock.Mock(key="red"),
            mock.Mock(key="blue"),
        ]

        expected_dict = {
            12: [iterable[0], iterable[1]],
            "red": [iterable[2]],
            "blue": [iterable[3]],
        }

        T.assert_equal(helpers.from_keyed_iterable(iterable, "key"), expected_dict)

    def test_filter_func(self):
        iterable = [
            mock.Mock(key=12, keep=False),
            mock.Mock(key=12, keep=True),
            mock.Mock(key="red", keep=False),
            mock.Mock(key="blue", keep=True),
        ]

        filter_func = lambda e: e.keep

        expected_dict = {
            12: [iterable[1]],
            "blue": [iterable[3]],
        }

        T.assert_equal(helpers.from_keyed_iterable(iterable, "key", filter_func), expected_dict)


class SubtractByKeyTestCase(T.TestCase):
    def test(self):
        dict_a = {
            1: None,
            2: None,
            3: None,
        }

        dict_b = {
            1: None,
            5: None,
        }

        expected_dict = {
            2: None,
            3: None,
        }

        T.assert_equal(helpers.subtract_by_key(dict_a, dict_b), expected_dict)

    def test_empty(self):
        dict_a = {}
        dict_b = {1: None, 5: None}

        T.assert_equal(helpers.subtract_by_key(dict_a, dict_b), {})

        dict_a = {1: None, 5: None}
        dict_b = {}

        T.assert_equal(helpers.subtract_by_key(dict_a, dict_b), dict_a)


class SubtractTestCase(T.TestCase):
    @mock.patch("utils.dicts.helpers.subtract_by_key")
    def test_not_strict(self, sbk_patch):
        sbk_patch.return_value = mock.sentinel
        T.assert_equal(helpers.subtract(None, None, False), sbk_patch.return_value)
        sbk_patch.assert_called_once_with(None, None)

    def test(self):
        dict_a = {
            1: None,
            2: "Green",
            3: None,
            4: "Yellow"
        }

        dict_b = {
            1: None,
            4: "Blue",
            5: None,
        }

        expected_dict = {
            2: "Green",
            4: "Yellow",
            3: None,
        }

        T.assert_equal(helpers.subtract(dict_a, dict_b, True), expected_dict)

    def test_empty(self):
        dict_a = {}
        dict_b = {1: None, 5: None}

        dict_b = {}

        T.assert_equal(helpers.subtract(dict_a, dict_b, True), {})

        dict_a = {1: None, 5: None}
        dict_b = {}

        T.assert_equal(helpers.subtract(dict_a, dict_b, True), dict_a)


class WinnowByKeysTestCase(T.TestCase):
    @T.setup
    def dict_create(self):
        self.dct = {
            1: None,
            2: True,
            3: False,
            4: int,
        }

    def test(self):

        result = helpers.winnow_by_keys(self.dct, keys=[1, 4])

        T.assert_equal(result.has, {1: None, 4: int})
        T.assert_equal(result.has_not, {2: True, 3: False})

    def test_filter_func(self):

        result = helpers.winnow_by_keys(self.dct, filter_func=lambda k: k % 2 == 0)

        T.assert_equal(result.has, {2: True, 4: int})
        T.assert_equal(result.has_not, {1: None, 3: False})


class IntersectionTestCase(T.TestCase):
    @T.setup
    def dict_create(self):
        self.dict_a = {
            1: None,
            2: True,
            3: False,
            4: int,
        }

        self.dict_b = {
            1: None,
            3: False,
            4: bool,
            5: True,
        }

    def test(self):
        T.assert_equal(helpers.intersection(self.dict_a, self.dict_b), {1: None, 3: False})

    def test_not_strict(self):
        T.assert_equal(helpers.intersection(self.dict_a, self.dict_b, False), {1: None, 3: False, 4: int})


class SetDefaultsTestCase(T.TestCase):
    def test(self):
        target = {
            1: None,
            4: False,
        }

        defaults = {
            2: True,
            3: int,
            4: "RED",
        }

        result = helpers.setdefaults(target, defaults)

        T.assert_equal(result,{1: None, 2: True, 3: int, 4: False})

import testify as T

from utils import bools


class XORTestCase(T.TestCase):
    def test_odd(self):
        things = [
            True,
            True,
            True,
            False,
            False,
            False,
            False,
        ]

        T.assert_equal(bools.xor(*things), True)

    def test_even(self):
        things = [
            True,
            True,
            False,
            False,
            False,
        ]

        T.assert_equal(bools.xor(*things), False)

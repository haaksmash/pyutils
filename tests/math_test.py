import testify as T

from utils import math


class ProductTestCase(T.TestCase):
    def test_empty_sequence(self):
        T.assert_equal(math.product([]), 1)

    def test_non_iterable(self):
        with T.assert_raises(TypeError):
            math.product(None)

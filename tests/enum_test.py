import mock
import testify as T

from utils.enum import EnumItem, Enum


class EnumItemTestCase(T.TestCase):
    def test_equality(self):
        parent = mock.Mock()
        parent2 = mock.Mock()

        value1 = mock.Mock()
        value1.__eq__ = mock.Mock()
        value2 = mock.Mock()

        ei = EnumItem(parent, "name", value1)
        ei2 = EnumItem(parent2, "name", value2)
        parent.is_strict = False

        ei == ei2

        value1.__eq__.assert_called_once_with(value2)

    def test_equality_strict_enum(self):
        parent = mock.Mock()
        parent2 = mock.Mock()
        parent.is_strict = True

        ei = EnumItem(parent, "name", mock.ANY)
        ei2 = EnumItem(parent2, "name", mock.ANY)

        with T.assert_raises(ValueError):
            ei == ei2

    def test_equality_with_primitive(self):
        value = mock.Mock()
        value.__eq__ = mock.Mock()
        ei = EnumItem(mock.ANY, "name", value)

        ei == 1

        value.__eq__.assert_called_once_with(1)

class EnumTestCase(T.TestCase:
    pass

import mock
import testify as T

from utils import enum


class EnumItemTestCase(T.TestCase):
    def test_equality(self):
        parent = mock.Mock()
        parent2 = mock.Mock()

        value1 = mock.Mock()
        value1.__eq__ = mock.Mock()
        value2 = mock.Mock()

        ei = enum.EnumItem(parent, "name", value1)
        ei2 = enum.EnumItem(parent2, "name", value2)
        parent.is_strict = False

        ei == ei2

        value1.__eq__.assert_called_once_with(value2)

    def test_equality_strict_enum(self):
        """Test that an EnumItem with a strict parent will not compared to
        an EnumItem from another parent."""
        parent = mock.Mock()
        parent2 = mock.Mock()
        parent.is_strict = True

        ei = enum.EnumItem(parent, "name", mock.ANY)
        ei2 = enum.EnumItem(parent2, "name", mock.ANY)

        with T.assert_raises(ValueError):
            ei == ei2

    def test_equality_with_primitive(self):
        """Ensure that an enum's value is compared to a primitive"""
        value = mock.Mock()
        value.__eq__ = mock.Mock()
        ei = enum.EnumItem(mock.ANY, "name", value)

        ei == 1

        value.__eq__.assert_called_once_with(1)

class EnumClassTestCase(T.TestCase):
    @T.setup
    def create_enum(self):
        self.enum_item_mock = mock.create_autospec(enum.EnumItem)

        class TestEnum(enum.Enum):
            FLAG_ONE = 1
            FLAG_TWO = 2
            FLAG_THREE = 3
            FLAG_TRUE = True

        type.__setattr__(TestEnum, 'FLAG_MOCK', self.enum_item_mock)
        TestEnum.__enum_item_map__["FLAG_MOCK"] = self.enum_item_mock

        self.enum = TestEnum

    def test_attribute_acccess(self):
        """Ensure that we're actually dealing with EnumItem instances"""
        T.assert_is(self.enum.FLAG_MOCK, self.enum_item_mock)

    def test_attribute_set_fails(self):
        """Enums should default to frozen-type"""
        with T.assert_raises(TypeError):
            self.enum.FLAG_THREE = 4

    def test_name_value_map(self):
        expected_map = {
            "FLAG_ONE": 1,
            "FLAG_TWO": 2,
            "FLAG_THREE": 3,
            "FLAG_TRUE": True,
            self.enum_item_mock.name: self.enum_item_mock.value,
        }

        T.assert_equal(self.enum.get_name_value_map(), expected_map)

    def test_is_strict(self):
        """Enums should default to not-strict"""
        T.assert_equal(self.enum.is_strict, False)

class UnFrozenEnumClassTestCase(T.TestCase):
    @T.setup
    def create_enum(self):
        class TestEnum(enum.Enum):
            FLAG_ONE = 1
            FLAG_TWO = 2
            FLAG_THREE = 3
            FLAG_TRUE = True

            class Options:
                frozen = False

        self.enum = TestEnum

    def test_attribute_set(self):
        T.assert_equal(self.enum.FLAG_THREE, 3)
        self.enum.FLAG_THREE = 4
        T.assert_equal(self.enum.FLAG_THREE, 4)


class StrictEnumClassTestCase(T.TestCase):
    @T.setup
    def create_enum(self):
        class TestEnum(enum.Enum):
            FLAG_ONE = 1
            FLAG_TWO = 2
            FLAG_THREE = 3
            FLAG_TRUE = True

            class Options:
                strict = True

        self.enum = TestEnum

    def test_is_strict(self):
        """Strict enums should report as such"""
        T.assert_equal(self.enum.is_strict, True)


class EnumFactoryTestCase(T.TestCase):
    def test_creation(self):
        """Do we, in fact, create an Enum?"""
        new_enum = enum.enum("TestEnum")

        T.assert_equal(issubclass(new_enum, enum.Enum), True)
        T.assert_equal(new_enum.__name__, "TestEnum")

    def test_creation_with_args(self):
        """Test that args are used to create sequential EnumItems"""
        new_enum = enum.enum("TestEnum", "ZERO", "ONE")

        T.assert_equal(isinstance(new_enum.ONE, enum.EnumItem), True)
        T.assert_equal(new_enum.ZERO, 0)
        T.assert_equal(new_enum.ONE, 1)

    def test_creation_with_kwargs(self):
        new_enum = enum.enum("TestEnum", TRUE=True, NONE=None, ONE=1)

        T.assert_equal(isinstance(new_enum.TRUE, enum.EnumItem), True)

        T.assert_equal(new_enum.TRUE, True)
        T.assert_equal(new_enum.NONE, 0)
        T.assert_equal(new_enum.ONE, 1)

    def test_from_iterable(self):
        iterable = ["ONE", "TWO", "THREE"]
        with mock.patch("utils.enum._enum.__call__") as call_patch:
            enum.enum.from_iterable(iterable)

            call_patch.assert_has_calls([
                mock.call(*iterable),
            ])

    def test_from_dict(self):
        dct = {
            "ONE": 1,
            "TWO": 2,
            "THREE": 3,
        }

        with mock.patch("utils.enum._enum.__call__") as call_patch:
            enum.enum.from_dict(dct)

            call_patch.assert_has_calls([
                mock.call(**dct)
            ])

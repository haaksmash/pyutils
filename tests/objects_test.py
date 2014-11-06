import mock
import testify as T

from utils.objects import immutable
from utils.objects import get_attr


class ObjectsTestCase(T.TestCase):

    @T.let
    def simple_object(self):
        return mock.Mock(
            first=mock.sentinel.FIRST,
            second=mock.Mock(
                first=mock.sentinel.SECOND,
            ),
            third=mock.Mock(
                first=mock.Mock(
                    first=mock.sentinel.THIRD,
                ),
            ),
        )

    def test_get_attr_successful_one_level(self):
        T.assert_equal(
            get_attr(self.simple_object, 'first'),
            mock.sentinel.FIRST,
        )

    def test_get_attr_successful_two_level(self):
        T.assert_equal(
            get_attr(self.simple_object, 'second.first'),
            mock.sentinel.SECOND,
        )

    def test_get_attr_successful_three_level(self):
        T.assert_equal(
            get_attr(self.simple_object, 'third.first.first'),
            mock.sentinel.THIRD,
        )

    def test_get_attr_bad(self):
        class Empty(object): pass
        e = Empty()

        with T.assert_raises(AttributeError):
            get_attr(e, 'anything')

        e.first = Empty()
        with T.assert_raises(AttributeError):
            getattr(e, 'first.anything')

    def test_get_attr_with_default(self):
        class Empty(object): pass
        e = Empty()

        T.assert_equal(
            get_attr(e, 'anything', default=mock.sentinel.DEFAULT),
            mock.sentinel.DEFAULT,
        )
        # default shouldn't hide something that's actually there
        e.anything = mock.sentinel.ANYTHING
        T.assert_equal(
            get_attr(e, 'anything', default=mock.sentinel.DEFAULT),
            mock.sentinel.ANYTHING,
        )

        # default should cover deeper lookups
        T.assert_equal(
            get_attr(e, 'anything.anything', default=mock.sentinel.DEFAULT),
            mock.sentinel.DEFAULT,
        )


    def test_separator_can_be_specified(self):
        T.assert_equal(
            get_attr(self.simple_object, 'second|first', separator='|'),
            mock.sentinel.SECOND,
        )


class ImmutableTestCase(T.TestCase):

    def test_wrapper_blocks_writes(self):
        m = immutable(mock.Mock())

        with T.assert_raises(AttributeError):
            m.something = True

    def test_wrapper_is_recursive_by_default(self):
        m = immutable(mock.Mock(anything=mock.Mock()))

        with T.assert_raises(AttributeError):
            m.anything.something = True

    def test_wrapper_can_be_non_recursive(self):
        m = immutable(mock.Mock(), recursive=False)

        with T.assert_raises(AttributeError):
            m.anything = True

        m.anything.something = True

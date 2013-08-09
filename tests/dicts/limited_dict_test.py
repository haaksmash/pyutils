import testify as T

from utils.dicts.limited_dict import LimitedDict


class LimitedDictTestCase(T.TestCase):

    def test_init_with_args(self):
        with T.assert_raises(KeyError):
            ld = LimitedDict([(1, 2)])

        ld = LimitedDict([(1, 2)], keys=[1])

        T.assert_equal(ld[1], 2)

    def test_init_with_kwargs(self):
        with T.assert_raises(KeyError):
            ld = LimitedDict(the_key=True)

        ld = LimitedDict(the_key=True, keys=["the_key"])

        T.assert_equal(ld["the_key"], True)

    def test_defined_kes(self):
        keys = ["the_key", "another_key"]
        ld = LimitedDict(keys=keys)

        T.assert_equal(set(ld.defined_keys), set(keys))

    def test_setitem_legal_key(self):
        ld = LimitedDict(keys=["the_key"])

        ld["the_key"] = True

        T.assert_equal(ld["the_key"], True)

    def test_setitem_illegal_key(self):
        ld = LimitedDict()

        with T.assert_raises(KeyError):
            ld['any_old_key'] = None

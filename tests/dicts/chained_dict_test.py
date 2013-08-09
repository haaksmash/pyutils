import testify as T

from utils.dicts.chained_dict import ChainedDict


class ChainedDictTestCase(T.TestCase):

    def test_bare_initialization(self):
        ChainedDict()


    def test_contains_direct(self):
        cd = ChainedDict()
        cd["the_key"] = True

        T.assert_in("the_key", cd)
        T.assert_not_in("not_the_key", cd)

    def test_contains_ancestral(self):
        cd = ChainedDict(**{"the_key": True})
        cd2 = ChainedDict(parent=cd, **{"the_other_key": True})

        T.assert_in("the_key", cd2)
        T.assert_in("the_other_key", cd2)
        T.assert_not_in("the_other_key", cd)

    def test_setitem_direct_not_affect_ancestral(self):
        cd = ChainedDict(**{"the_key": True})
        cd2 = ChainedDict(parent=cd)

        cd2["the_key"] = False

        T.assert_equal(cd2["the_key"], False)
        T.assert_equal(cd["the_key"], True)

    def test_ancestor_delitem(self):
        cd = ChainedDict(**{"the_key": True})
        cd2 = ChainedDict(parent=cd, **{"the_other_key": True})

        del cd["the_key"]

        T.assert_not_in("the_key", cd2)

    def test_delitem(self):
        cd = ChainedDict({"the_key": True})
        del cd["the_key"]

        T.assert_not_in("the_key", cd)

    def test_delitem_invalid_key(self):
        cd = ChainedDict()

        with T.assert_raises(KeyError):
            del cd["anything"]

    def test_delitem_with_ancestor(self):
        cd = ChainedDict(**{"the_key": True})
        cd2 = ChainedDict(parent=cd)

        del cd2["the_key"]

        T.assert_not_in("the_key", cd2)
        T.assert_in("the_key", cd)

    def test_len(self):
        cd = ChainedDict(**{"the_key": True})

        T.assert_length(cd, 1)

    def test_len_with_ancestor(self):
        cd = ChainedDict(**{"the_key": True})
        cd2 = ChainedDict(parent=cd, **{"the_other_key": True})

        T.assert_length(cd2, 2)

    def test_iter(self):
        cd = ChainedDict(**{"the_key": True})

        T.assert_equal(set(key for key in cd), set(["the_key"]))

    def test_iter_with_ancestor(self):
        cd = ChainedDict(**{"the_key": True})
        cd2 = ChainedDict(parent=cd, **{"the_other_key": True})

        T.assert_equal(set(key for key in cd2), set(["the_key", "the_other_key"]))
        T.assert_equal(set(key for key in cd), set(["the_key"]))

    def test_iter_with_ancestor_with_deletion(self):
        cd = ChainedDict(**{"the_key": True})
        cd2 = ChainedDict(parent=cd, **{"the_other_key": True})

        del cd2["the_key"]

        T.assert_equal(set(key for key in cd2), set(["the_other_key"]))



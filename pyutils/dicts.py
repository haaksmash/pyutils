"""Helper functinos for dealing with dicts.

Things you always wished you could do more succinctly!
"""
from collections import namedtuple


def from_keyed_iterable(iterable, key, filter_func=None):
    """Construct a dictionary out of an iterable, using an attribute name as
    the key. Optionally provide a filter function, to determine what should be
    kept in the dictionary."""

    generated = {}

    for element in iterable:
        try:
            k = getattr(element, key)
        except AttributeError:
            raise RuntimeError("{} does not have the key attribute:{}".format(
                element, key
            ))

        if filter_func is None or filter_func(element):
            if k in generated:
                generated[k] += [element]
            else:
                generated[k] = [element]

    return generated


def subtract_by_key(dict_a, dict_b):
    """given two dicts, a and b, this function returns c = a - b, where
    a - b is defined as the key difference between a and b.

    e.g.,
    {1:None, 2:3, 3:"yellow", 4:True} - {2:4, 1:"green"} =
        {3:"yellow", 4:True}

    """
    difference_dict = {}
    for key in dict_a:
        if key not in dict_b:
            difference_dict[key] = dict_a[key]

    return difference_dict


def subtract(dict_a, dict_b, strict=False):
    """a stricter form of subtract_by_key(), this version will only remove an
    entry from dict_a if the key is in dict_b *and* the value at that key
    matches"""
    if not strict:
        return subtract_by_key(dict_a, dict_b)

    difference_dict = {}
    for key in dict_a:
        if key not in dict_b or dict_b[key] != dict_a[key]:
            difference_dict[key] = dict_a[key]

    return difference_dict


WinnowedResult = namedtuple("WinnowedResult", ['has', 'has_not'])
def winnow_by_keys(dct, keys):
    """separates a dict into has-keys and not-has-keys pairs"""
    has = {}
    has_not = {}

    for key in dct:
        if key in keys:
            has[key] = dct[key]
        else:
            has_not[key] = dct[key]

    return WinnowedResult(has, has_not)


def intersection(dict_a, dict_b, strict=True):
    intersection_dict = {}

    for key in dict_a:
        if key in dict_b:
            if not strict or dict_a[key] == dict_b[key]:
                intersection_dict[key] = dict_a[key]

    return intersection_dict

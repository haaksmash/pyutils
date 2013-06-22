"""Who hasn't needed a good, old-fashioned enum now and then?"""


class enum(object):

    def __init__(self, *args, **kwargs):
        if args and kwargs:
            raise TypeError("Enums can only be made from args XOR kwargs, not both")

        self.__enum_items = {}

        for val, arg in enumerate(args):
            self.__enum_items[arg] = val

        counter = 0
        for arg, val in kwargs.iteritems():
            if val is None:
                val = counter
                counter += 1
            elif isinstance(val, int):
                counter = val + 1

            self.__enum_items[arg] = val

    def __getattr__(self, attr_name):
        if attr_name in self.__enum_items:
            return self.__enum_items[attr_name]

        return super(enum, self).__getattr__(attr_name)

    @classmethod
    def from_iterable(cls, iterable):
        return cls(*iterable)

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)

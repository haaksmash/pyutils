"""Who hasn't needed a good, old-fashioned enum now and then?"""


class enum(object):

    def __init__(self, *args, **kwargs):
        if args and kwargs:
            raise TypeError("Enums can only be made from args XOR kwargs, not both")

        self.__enum_items = {}

        counter = 0
        for name, val in kwargs.iteritems():
            if val is None:
                val = counter
                counter += 1
            elif isinstance(val, int):
                counter = val + 1

            self.__enum_items[name] = EnumItem(self, name, val)

        for val, name in enumerate(args, start=counter):
            self.__enum_items[name] = EnumItem(self, name, val)

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

    def __iter__(self):
        for k, v in self.__enum_items.iteritems():
            yield k, v

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.__enum_items.values())


class EnumItem(object):

    def __init__(self, parent, name, value):
        self.__parent = parent
        self.__name = name
        self.__value = value

    def __repr__(self):
        return "<{}: {} [{}]>".format(self.__class__.__name__, self.name, self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.parent != other.parent:
                raise ValueError("Can't compare EnumItems from different enums")
            return self.value == other.value

        return self.value == other

    @property
    def value(self):
        return self.__value

    @property
    def name(self):
        return self.__name

    @property
    def parent(self):
        return self.__parent


class _EnumMeta(type):
    def __new__(cls, name, bases, attr_dict):
        print bases

        options = attr_dict.pop('Options', object)

        for attr_name, attr_value in attr_dict.items():
            if attr_name.startswith('__'):
                continue

            if getattr(options, 'force_uppercase', False):
                attr_name = attr_name.upper()
            attr_dict[attr_name] = EnumItem(name, attr_name, attr_value)

        if getattr(options, "frozen", False):
            attr_dict['__frozen__'] = True

        return super(_EnumMeta, cls).__new__(cls, name, bases, attr_dict)

    def __setattr__(self, name, val):
        if getattr(self, "__frozen__"):
            raise TypeError("can't set attributes on a frozen enum")


class Enum(object):
    __metaclass__ = _EnumMeta

from collections import MutableMapping


class LimitedDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        keys = kwargs.pop('keys', [])
        self.__keys = keys

        kwargs.update((key, val) for key, val in args)
        self.__data = kwargs

        super(LimitedDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, val):
        if key not in self.__keys:
            raise KeyError("Illegal key: {}".format(key))

        self.__data[key] = val

    def __getitem__(self, key):
        return self.__data[key]

    def __iter__(self):
        return self.__data.__iter__()

    def __delitem__(self, key):
        del self.__data[key]

    def __len__(self):
        return len(self.__data)

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, self.__keys, self.__data)

    @property
    def defined_keys(self):
        return self.__keys

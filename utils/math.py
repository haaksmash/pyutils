import operator


def prod(*args, **kwargs):
    """like the built-in sum, but for multiplication."""
    initial = kwargs.pop('initial', 1)

    return reduce(operator.mul, args, initial)

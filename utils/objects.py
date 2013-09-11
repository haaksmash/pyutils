_get_attr_raise_on_attribute_error = "RAISE ON EXCEPTION"

def get_attr(obj, string_rep, default=_get_attr_raise_on_attribute_error, separator="."):
    """ getattr via a chain of attributes like so:
    >>> import datetime
    >>> some_date = datetime.date.today()
    >>> get_attr(some_date, "month.numerator.__doc__")
    'int(x[, base]) -> integer\n\nConvert a string or number to an integer, ...
    """
    attribute_chain = string_rep.split(separator)

    current_obj = obj

    for attr in attribute_chain:
        try:
            current_obj = getattr(current_obj, attr)
        except AttributeError:
            if default is _get_attr_raise_on_attribute_error:
                raise AttributeError(
                    "Bad attribute \"{}\" in chain: \"{}\"".format(attr, string_rep)
                )
            return default

    return current_obj

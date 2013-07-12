"""List-related functions"""


def unlist(list_thing, complain=True):
    if complain and len(list_thing) > 1:
        raise ValueError("More than one element in {}".format(list_thing))
    elif len(list_thing) == 1:
        return list_thing[0]

    if complain:
        raise ValueError("Nothing in {}".format(list_thing))
    return None

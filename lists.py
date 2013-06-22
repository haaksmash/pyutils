"""List-related functions"""


def unlist(list_thing, complain=True):
    if complain and len(list_thing) > 1:
        raise ValueError("More than one element in {}".format(list_thing))

    return list_thing[0]

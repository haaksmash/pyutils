Utils
=====

Sometimes you write a function over and over again; sometimes you look up at
the ceiling and ask "why, Guido, why isn't this included in the standard
library?"

Well, we perhaps can't answer that question. But we can collect those functions
into a centralized place!

Provided things
+++++++++++++++

Utils is broken up into broad swathes of functionality, to ease the task of
remembering where exactly something lives.

enum
----

Python doesn't have a built-in way to define an enum, so this module provides (what I think) is a pretty clean way to go about them.

.. code-block:: python

    from utils import enum

    class Colors(enum.Enum):
        RED = 0
        GREEN = 1

        class Options:
            frozen = True

    ColorsAlso = enum.enum("RED", "GREEN")

math
----

Currently only has the multiplicative analogue of the built-in ``sum``.

dicts
-----

intersections, differences, winnowing, a few specialized dicts...

lists
-----

flatten and unlisting

bools
-----

currently only provides an ``xor`` function.

dates
-----

``TimePeriod``, from string, ``to_datetime``, and ``days_ago`` and ``_ahead``

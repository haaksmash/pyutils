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

        # Defining an Enum class allows you to specify a few
        # things about the way it's going to behave.
        class Options:
            frozen = True # can't change attributes
            strict = True # can only compare to itself; i.e., Colors.RED == Animals.COW
                          # will raise an exception.

    # or use the enum factory (no Options, though)
    ColorsAlso = enum.enum("RED", "GREEN")

Once defined, use is straightforward:

.. code-block:: python

    >>> Colors
    <class 'blahblah.Colors'>
    >>> Colors.RED
    <EnumItem: RED [0]>
    >>> Colors.RED == 0
    True
    >>> Colors.RED == Colors.RED
    True
    >>> Colors.RED = 2
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "utils/enum.py", line 114, in __setattr__
        raise TypeError("can't set attributes on a frozen enum")
    TypeError: can't set attributes on a frozen enum

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

Mostly cool for the ``TimePeriod`` classes:

.. code-block:: python

    >>> from datetime import date # will also work with datetimes
    >>> time_period = TimePeriod(date(2013, 5, 10), date(2013, 8, 11))
    >>> time_period
    <TimePeriod: 2013-05-10 00:00:00-2013-08-11 23:59:59>
    >>> date(2013, 6, 12) in time_period
    True
    >>> other_time_period = TimePeriod(date(2013, 6, 1), date(2013, 6, 30))
    >>> other_time_period in time_period
    True
    >>> another_time_period = TimePeriod(date(2013, 8, 1), date(2013, 8, 30))
    >>> time_period.overlaps(another_time_period)
    True
    >>> TimePeriod.get_containing_period(time_period, another_time_period)
    <TimePeriod: 2013-05-08 00:00:00-2013-08-30 23:59:59>


and so on and so forth. There's also a ``DiscontinousTimePeriod`` class, which
stores a collection of TimePeriods.

There's also helper functions for common operations like ``days_ahead`` and
``days_ago``, which pretty much do what they say on the tin.

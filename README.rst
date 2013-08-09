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

dicts
-----

intersections, differences, winnowing, a few specialized dicts...

lists
-----

flatten and unlisting

bools
~~~~~

currently only provides an ``xor`` function.

dates
~~~~~

TimePeriod, from string, ``to_datetime``, and ``days_ago`` and ``_ahead``

# coding=utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy

from enumfields import Enum, IntEnum


class Color(Enum):
    __order__ = 'RED GREEN BLUE'

    RED = 'r'
    GREEN = 'g'
    BLUE = 'b'

    class Labels:
        RED = 'Reddish'
        BLUE = ugettext_lazy('bluë')


class Taste(Enum):
    SWEET = 1
    SOUR = 2
    BITTER = 3
    SALTY = 4
    UMAMI = 5


class ZeroEnum(Enum):
    ZERO = 0
    ONE = 1


class IntegerEnum(IntEnum):
    A = 0
    B = 1

    class Labels:
        A = 'foo'


class LabeledEnum(Enum):
    FOO = 'foo'
    BAR = 'bar'
    FOOBAR = 'foobar'

    class Labels:
        FOO = 'Foo'
        BAR = 'Bar'
        # this is intentional. see test_nonunique_label
        FOOBAR = 'Foo'

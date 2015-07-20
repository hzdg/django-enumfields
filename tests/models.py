from django.db import models
from enum import Enum, IntEnum

from enumfields import EnumField, EnumIntegerField


class MyModel(models.Model):
    class Color(Enum):
        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

    color = EnumField(Color, max_length=1)

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

    taste = EnumField(Taste, default=Taste.SWEET)
    taste_null_default = EnumField(Taste, null=True, blank=True, default=None)
    taste_int = EnumIntegerField(Taste, default=Taste.SWEET)

    default_none = EnumIntegerField(Taste, default=None, null=True, blank=True)
    nullable = EnumIntegerField(Taste, null=True, blank=True)

    random_code = models.TextField(null=True, blank=True)

    zero_field = EnumIntegerField(ZeroEnum, null=True, default=None, blank=True)
    int_enum = EnumIntegerField(IntegerEnum, null=True, default=None, blank=True)

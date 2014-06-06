from django.db import models
from enum import Enum
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

    taste = EnumField(Taste, default=Taste.SWEET)
    taste_int = EnumIntegerField(Taste, default=Taste.SWEET)

    default_none = EnumIntegerField(Taste, default=None, null=True)
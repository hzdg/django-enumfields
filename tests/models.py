from django.db import models
from enum import Enum
from enumfields import EnumField


class MyModel(models.Model):

    class Color(Enum):
        RED = 'r'
        GREEN = 'g'
        BLUE = 'b'

    color = EnumField(Color, max_length=1)

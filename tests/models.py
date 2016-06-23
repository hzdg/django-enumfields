from django.db import models

from enumfields import EnumField, EnumIntegerField

from .enums import Color, IntegerEnum, LabeledEnum, Taste, ZeroEnum


class MyModel(models.Model):
    color = EnumField(Color, max_length=1)
    taste = EnumField(Taste, default=Taste.SWEET)
    taste_null_default = EnumField(Taste, null=True, blank=True, default=None)
    taste_int = EnumIntegerField(Taste, default=Taste.SWEET)

    default_none = EnumIntegerField(Taste, default=None, null=True, blank=True)
    nullable = EnumIntegerField(Taste, null=True, blank=True)

    random_code = models.TextField(null=True, blank=True)

    zero_field = EnumIntegerField(ZeroEnum, null=True, default=None, blank=True)
    int_enum = EnumIntegerField(IntegerEnum, null=True, default=None, blank=True)

    zero2 = EnumIntegerField(ZeroEnum, default=ZeroEnum.ZERO)
    labeled_enum = EnumField(LabeledEnum, blank=True, null=True)

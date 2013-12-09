from django.core.exceptions import ValidationError
from django.db import models
import six


class EnumFieldMixin(six.with_metaclass(models.SubfieldBase)):
    def __init__(self, enum, choices=None, max_length=10, **options):
        self.enum = enum
        if not choices:
            try:
                choices = enum.choices()
            except AttributeError:
                choices = [(m.value, getattr(m, 'label', m.name)) for m in enum]
        super(EnumFieldMixin, self).__init__(
            choices=choices, max_length=max_length, **options)

    def to_python(self, value):
        if value is None:
            return None
        for m in self.enum:
            if value == m:
                return value
            if value == m.value:
                return m
        raise ValidationError('%s is not a valid value for enum %s' % (value, self.enum))

    def get_prep_value(self, value):
        return None if value is None else value.value


class EnumField(EnumFieldMixin, models.CharField):
    pass


class EnumIntegerField(EnumFieldMixin, models.IntegerField):
    pass

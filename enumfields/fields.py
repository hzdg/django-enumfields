from django.core.exceptions import ValidationError
from django.db import models
from enum import Enum
import six


class EnumFieldMixin(six.with_metaclass(models.SubfieldBase)):
    def __init__(self, enum,  choices=None, max_length=10, **options):
        if isinstance(enum, basestring):
            module_name, class_name = enum.rsplit('.', 1)
            module = __import__(module_name, globals(), locals(), [class_name])
            self.enum = getattr(module, class_name)
        else:
            self.enum = enum

        if not choices:
            try:
                choices = self.enum.choices()
            except AttributeError:
                choices = [(m.value, getattr(m, 'label', m.name)) for m in self.enum]
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

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return str(value.value) if value else None



class EnumField(EnumFieldMixin, models.CharField):
    pass


class EnumIntegerField(EnumFieldMixin, models.IntegerField):
    def get_prep_value(self, value):
        if value is None:
            return None
        elif isinstance(value, Enum):
            return value.value
        else:
            return int(value)


# South compatibility stuff

def converter_func(enum_class):
    return "'%s.%s'" % (enum_class.__module__, enum_class.__name__)


rules = [
    (
        [EnumFieldMixin],
        [],
        {
            "enum": ["enum", {'is_django_function': True, "converter": converter_func}],
        },
    )
]

try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules(rules, ["^enumfields\.fields"])
except ImportError:
    pass

from django.core.exceptions import ValidationError
from django.db import models
from enum import Enum
import six
from django.db.models.fields import NOT_PROVIDED


class EnumFieldMixin(six.with_metaclass(models.SubfieldBase)):
    def __init__(self, enum, choices=None, max_length=10, **options):
        if isinstance(enum, six.string_types):
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
            if value == m.value or str(value) == str(m.value):
                return m
        raise ValidationError('%s is not a valid value for enum %s' % (value, self.enum))

    def get_prep_value(self, value):
        return None if value is None else value.value

    def value_to_string(self, obj):
        """
        This method is needed to support proper serialization. While its name is value_to_string()
        the real mening of the method is to convert the value to some serizlizable format.
        Since most of the enum values are strings or integers we WILL NOT convert it to string
        to enable integers to be serizlized natively.
        """
        value = self._get_val_from_obj(obj)
        return value.value if value else None

    def get_default(self):
        if self.has_default():
            if self.default is None:
                return None

            if isinstance(self.default, Enum):
                return self.default

            return self.enum(self.default)

        return super(EnumFieldMixin, self).get_default()


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


def enum_value(an_enum):
    return an_enum.value

rules = [
    (
        [EnumFieldMixin],
        [],
        {
            "enum": ["enum", {'is_django_function': True, "converter": converter_func}],
            "default": ['default', {'default': NOT_PROVIDED, 'ignore_dynamics': True,
                                    'converter': enum_value}]},
    )
]

try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules(rules, ["^enumfields\.fields"])
except ImportError:
    pass

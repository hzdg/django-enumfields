from django.core.exceptions import ValidationError
from django.db import models
from enum import Enum
import six
from django.db.models.fields import NOT_PROVIDED, BLANK_CHOICE_DASH

try:
    from django.utils.module_loading import import_string
except ImportError:
    from django.utils.module_loading import import_by_path as import_string


class EnumFieldMixin(six.with_metaclass(models.SubfieldBase)):
    def __init__(self, enum, **options):
        if isinstance(enum, six.string_types):
            self.enum = import_string(enum)
        else:
            self.enum = enum

        if "choices" not in options:
            options["choices"] = [(i, getattr(i, 'label', i.name)) for i in self.enum]  # choices for the TypedChoiceField

        super(EnumFieldMixin, self).__init__(**options)

    def to_python(self, value):
        if value is None or value == '':
            return None
        for m in self.enum:
            if value == m:
                return value
            if value == m.value or str(value) == str(m.value) or str(value) == str(m):
                return m
        raise ValidationError('%s is not a valid value for enum %s' % (value, self.enum))

    def get_prep_value(self, value):
        return None if value is None else value.value

    def value_to_string(self, obj):
        """
        This method is needed to support proper serialization. While its name is value_to_string()
        the real meaning of the method is to convert the value to some serializable format.
        Since most of the enum values are strings or integers we WILL NOT convert it to string
        to enable integers to be serialized natively.
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

    def deconstruct(self):
        name, path, args, kwargs = super(EnumFieldMixin, self).deconstruct()
        kwargs['enum'] = self.enum
        kwargs.pop('choices', None)
        if 'default' in kwargs:
            if hasattr(kwargs["default"], "value"):
                kwargs["default"] = kwargs["default"].value

        return name, path, args, kwargs

    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH):
        # Force enum fields' options to use the `value` of the enumeration
        # member as the `value` of SelectFields and similar.
        return [
            (i.value if i else i, display)
            for (i, display)
            in super(EnumFieldMixin, self).get_choices(include_blank, blank_choice)
        ]


class EnumField(EnumFieldMixin, models.CharField):
    def __init__(self, enum, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        super(EnumField, self).__init__(enum, **kwargs)
        self.validators = []


class EnumIntegerField(EnumFieldMixin, models.IntegerField):
    def get_prep_value(self, value):
        if value is None:
            return None

        if isinstance(value, Enum):
            return value.value

        try:
            return int(value)
        except ValueError:
            return self.to_python(value).value


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

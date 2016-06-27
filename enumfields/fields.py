from enum import Enum

import django
import six
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH, NOT_PROVIDED
from django.utils.functional import cached_property

from .compat import import_string
from .forms import EnumChoiceField


class CastOnAssignDescriptor(object):
    """
    A property descriptor which ensures that `field.to_python()` is called on _every_ assignment to the field.

    This used to be provided by the `django.db.models.subclassing.Creator` class, which in turn
    was used by the deprecated-in-Django-1.10 `SubfieldBase` class, hence the reimplementation here.
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)


class EnumFieldMixin(object):
    def __init__(self, enum, **options):
        if isinstance(enum, six.string_types):
            self.enum = import_string(enum)
        else:
            self.enum = enum

        if "choices" not in options:
            options["choices"] = [(i, getattr(i, 'label', i.name)) for i in self.enum]  # choices for the TypedChoiceField

        super(EnumFieldMixin, self).__init__(**options)

    def contribute_to_class(self, cls, name):
        super(EnumFieldMixin, self).contribute_to_class(cls, name)
        setattr(cls, name, CastOnAssignDescriptor(self))

    def to_python(self, value):
        if value is None or value == '':
            return None
        if isinstance(value, self.enum):
            return value
        for m in self.enum:
            if value == m:
                return m
            if value == m.value or str(value) == str(m.value) or str(value) == str(m):
                return m
        raise ValidationError('%s is not a valid value for enum %s' % (value, self.enum), code="invalid_enum_value")

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, self.enum):  # Already the correct type -- fast path
            return value.value
        return self.enum(value).value

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

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
            (i.value if isinstance(i, Enum) else i, display)
            for (i, display)
            in super(EnumFieldMixin, self).get_choices(include_blank, blank_choice)
        ]

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        if not choices_form_class:
            choices_form_class = EnumChoiceField

        if django.VERSION < (1, 6):
            # Use a better-compatible implementation of `formfield` for old versions of Django.
            # It's unfortunate that we need to do this, but since the project supports Django 1.5,
            # we have to do it.
            from .compat import formfield
            return formfield(db_field=self, form_class=form_class, choices_form_class=choices_form_class, **kwargs)

        return super(EnumFieldMixin, self).formfield(form_class=form_class, choices_form_class=choices_form_class, **kwargs)


class EnumField(EnumFieldMixin, models.CharField):
    def __init__(self, enum, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        super(EnumField, self).__init__(enum, **kwargs)
        self.validators = []


class EnumIntegerField(EnumFieldMixin, models.IntegerField):
    @cached_property
    def validators(self):
        # Skip IntegerField validators, since they will fail with
        #   TypeError: unorderable types: TheEnum() < int()
        # when used database reports min_value or max_value from
        # connection.ops.integer_field_range method.
        next = super(models.IntegerField, self)
        return next.validators

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
    if an_enum is None:
        return None

    if isinstance(an_enum, Enum):
        return an_enum.value

    raise ValueError("%s is not a enum" % an_enum)


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

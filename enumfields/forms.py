from django.forms import TypedChoiceField
from django.forms.fields import TypedMultipleChoiceField
from django.utils.encoding import force_str

from .enums import Enum

__all__ = ["EnumChoiceField", "EnumMultipleChoiceField"]


class EnumChoiceFieldMixin:
    def prepare_value(self, value):
        # Widgets expect to get strings as values.

        if value is None:
            return ''
        if hasattr(value, "value"):
            value = value.value
        return force_str(value)

    def valid_value(self, value):
        if hasattr(value, "value"):  # Try validation using the enum value first.
            if super().valid_value(value.value):
                return True
        return super().valid_value(value)

    def to_python(self, value):
        if isinstance(value, Enum):
            value = value.value
        return super().to_python(value)


class EnumChoiceField(EnumChoiceFieldMixin, TypedChoiceField):
    pass


class EnumMultipleChoiceField(EnumChoiceFieldMixin, TypedMultipleChoiceField):
    pass

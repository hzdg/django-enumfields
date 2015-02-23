# -- encoding: UTF-8 --
from django.forms import TypedChoiceField
from django.forms.fields import TypedMultipleChoiceField
from django.utils.encoding import force_text

__all__ = ["EnumChoiceField", "EnumMultipleChoiceField"]

class EnumChoiceFieldMixin(object):
    def prepare_value(self, value):
        # Widgets expect to get strings as values.

        if value is None:
            return ''
        if hasattr(value, "value"):
            value = value.value
        return force_text(value)

    def valid_value(self, value):
        if hasattr(value, "value"):  # Try validation using the enum value first.
            if super(EnumChoiceFieldMixin, self).valid_value(value.value):
                return True
        return super(EnumChoiceFieldMixin, self).valid_value(value)


class EnumChoiceField(EnumChoiceFieldMixin, TypedChoiceField):
    pass

class EnumMultipleChoiceField(EnumChoiceFieldMixin, TypedMultipleChoiceField):
    pass

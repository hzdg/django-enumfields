from enumfields.drf.fields import EnumField as EnumSerializerField
from enumfields.fields import EnumFieldMixin
from rest_framework.fields import ChoiceField


class EnumSupportSerializerMixin:
    enumfield_options = {}

    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = (
            super().build_standard_field(field_name, model_field)
        )
        if field_class == ChoiceField and isinstance(model_field, EnumFieldMixin):
            field_class = EnumSerializerField
            field_kwargs['enum'] = model_field.enum
            field_kwargs.update(self.enumfield_options)
        return field_class, field_kwargs

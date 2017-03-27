from enumfields.drf.fields import EnumField as EnumSerializerField
from enumfields.fields import EnumFieldMixin
from rest_framework.fields import ChoiceField


class EnumSupportSerializerMixin(object):
    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = (
            super(EnumSupportSerializerMixin, self).build_standard_field(field_name, model_field)
        )
        if field_class == ChoiceField and isinstance(model_field, EnumFieldMixin):
            field_class = EnumSerializerField
            field_kwargs['enum'] = model_field.enum
        return field_class, field_kwargs

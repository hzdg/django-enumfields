from rest_framework.fields import ChoiceField


class EnumField(ChoiceField):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        kwargs['choices'] = tuple(
            (e.value, getattr(e, 'label', e.name)) for e in self.enum)
        super(EnumField, self).__init__(**kwargs)

    def to_representation(self, instance):
        if instance in ('', None):
            return instance
        try:
            if not isinstance(instance, self.enum):
                instance = self.enum(instance)  # Try to cast it
            return instance.value
        except ValueError:
            raise ValueError('Invalid value [%r] of enum %s' % (
                instance, self.enum.__name__))

    def to_internal_value(self, data):
        # Let data goes through ChoiceField.to_internal_value first
        # So we don't need to handle int <-> str conversion (DRF behavior)
        cleaned_data = super(EnumField, self).to_internal_value(data)
        try:
            return self.enum(cleaned_data)
        except ValueError:
            self.fail('invalid_choice', input=data)

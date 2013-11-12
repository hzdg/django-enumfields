from enum import Enum as BaseEnum, EnumMeta as BaseEnumMeta
import six


class EnumMeta(BaseEnumMeta):
    def __new__(cls, name, bases, attrs):
        Labels = attrs.get('Labels')
        obj = BaseEnumMeta.__new__(cls, name, bases, attrs)
        for m in obj:
            try:
                m.label = getattr(Labels, m.name)
            except AttributeError:
                m.label = m.name.replace('_', ' ').title()
        return obj


class Enum(six.with_metaclass(EnumMeta, BaseEnum)):
    @classmethod
    def choices(cls):
        """
        Returns a list formatted for use as field choices.
        (See https://docs.djangoproject.com/en/dev/ref/models/fields/#choices)
        """
        return tuple((m.value, m.label) for m in cls)

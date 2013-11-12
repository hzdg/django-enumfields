from enum import Enum as BaseEnum, EnumMeta as BaseEnumMeta


class EnumMeta(BaseEnumMeta):
    def __new__(cls, name, bases, attrs):
        obj = BaseEnumMeta.__new__(cls, name, bases, attrs)
        Labels = attrs.pop('Labels', None)
        for m in obj:
            try:
                m.label = getattr(Labels, m.name)
            except AttributeError:
                m.label = m.name.replace('_', ' ').title()
        return obj


class Enum(BaseEnum):
    __metaclass__ = EnumMeta

    @classmethod
    def choices(cls):
        """
        Returns a list formatted for use as field choices.
        (See https://docs.djangoproject.com/en/dev/ref/models/fields/#choices)
        """
        return tuple((m.value, m.label) for m in cls)
